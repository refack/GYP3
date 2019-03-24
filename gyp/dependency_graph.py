from collections import OrderedDict

from gyp.common import OrderedSet, linkable_types, GypError, BuildFile, ExceptionAppend


class DependencyGraphNode(object):
  """

  Attributes:
    ref: A reference to an object that this DependencyGraphNode represents.
    dependencies: List of DependencyGraphNodes on which this one depends.
    dependents: List of DependencyGraphNodes that depend on this one.
  """

  class CircularException(GypError):
    pass

  def __init__(self, ref):
    self.ref = ref
    self.dependencies = []
    self.dependents = []

  def __repr__(self):
    return '<DependencyGraphNode: %r>' % self.ref

  def __lt__(self, other):
    return self.ref < other.ref

  def FlattenToList_NoCycles(self, nodes):
    # flat_list is the sorted list of dependencies - actually, the list items
    # are the "ref" attributes of DependencyGraphNodes.  Every target will
    # appear in flat_list after all of its dependencies, and before all of its
    # dependents.
    flat_list = OrderedSet()

    # in_degree_zeros is the list of DependencyGraphNodes that have no
    # dependencies not in flat_list.  Initially, it is a copy of the children
    # of this node, because when the graph was built, nodes with no
    # dependencies were made implicit dependents of the root node.
    in_degree_zeros = sorted(self.dependents[:])

    while in_degree_zeros:
      # Nodes in in_degree_zeros have no dependencies not in flat_list, so they
      # can be appended to flat_list.  Take these nodes out of in_degree_zeros
      # as work progresses, so that the next node to process from the list can
      # always be accessed at a consistent position.
      node = in_degree_zeros.pop()
      flat_list.add(node.ref)

      # Look at dependents of the node just added to flat_list.  Some of them
      # may now belong in in_degree_zeros.
      for node_dependent in sorted(node.dependents):
        is_in_degree_zero = True
        # TODO: We want to check through the
        # node_dependent.dependencies list but if it's long and we
        # always start at the beginning, then we get O(n^2) behaviour.
        for node_dependent_dependency in sorted(node_dependent.dependencies):
          if not node_dependent_dependency.ref in flat_list:
            # The dependent one or more dependencies not in flat_list.  There
            # will be more chances to add it to flat_list when examining
            # it again as a dependent of those other dependencies, provided
            # that there are no cycles.
            is_in_degree_zero = False
            break

        if is_in_degree_zero:
          # All of the dependent's dependencies are already in flat_list.  Add
          # it to in_degree_zeros where it will be processed in a future
          # iteration of the outer loop.
          in_degree_zeros += [node_dependent]

    if len(flat_list) != len(nodes) and len(nodes) != 0:
      # If there's anything left unvisited, there must be a circular dependency (cycle).
      if not self.dependents:
        # If all files have dependencies, add the first file as a dependent
        # of root_node so that the cycle can be discovered from root_node.
        first_node = nodes.popitem()[1]
        first_node.dependencies.append(self)
        self.dependents.append(first_node)

      cycles = []
      for cycle in self.FindCycles():
        paths = [n.ref for n in cycle]
        cycles.append('Cycle: %s' % ' -> '.join(paths))
      raise DependencyGraphNode.CircularException('Cycles in dependency graph detected:\n' + '\n'.join(cycles))

    return list(flat_list)

  def FindCycles(self):
    """
    Returns a list of cycles in the graph, where each cycle is its own list.
    """
    results = []
    visited = OrderedSet()

    def Visit(node, path):
      for child in node.dependents:
        if child in path:
          results.append([child] + path[:path.index(child) + 1])
        elif not child in visited:
          visited.add(child)
          Visit(child, [child] + path)

    visited.add(self)
    Visit(self, [self])

    return results

  def DirectDependencies(self, dependencies=None):
    """Returns a list of just direct dependencies."""
    if dependencies is None:
      dependencies = []

    for dependency in self.dependencies:
      # Check for None, corresponding to the root node.
      if dependency.ref is not None and dependency.ref not in dependencies:
        dependencies.append(dependency.ref)

    return dependencies

  @staticmethod
  def _AddImportedDependencies(targets, dependencies=None):
    """Given a list of direct dependencies, adds indirect dependencies that
    other dependencies have declared to export their settings.

    This method does not operate on self.  Rather, it operates on the list
    of dependencies in the |dependencies| argument.  For each dependency in
    that list, if any declares that it exports the settings of one of its
    own dependencies, those dependencies whose settings are "passed through"
    are added to the list.  As new items are added to the list, they too will
    be processed, so it is possible to import settings through multiple levels
    of dependencies.

    This method is not terribly useful on its own, it depends on being
    "primed" with a list of direct dependencies such as one provided by
    DirectDependencies.  DirectAndImportedDependencies is intended to be the
    public entry point.
    """

    if dependencies is None:
      dependencies = []

    index = 0
    while index < len(dependencies):
      dependency = dependencies[index]
      dependency_dict = targets[dependency]
      # Add any dependencies whose settings should be imported to the list
      # if not already present.  Newly-added items will be checked for
      # their own imports when the list iteration reaches them.
      # Rather than simply appending new items, insert them after the
      # dependency that exported them.  This is done to more closely match
      # the depth-first method used by DeepDependencies.
      add_index = 1
      for imported_dependency in dependency_dict.get('export_dependent_settings', []):
        if imported_dependency not in dependencies:
          dependencies.insert(index + add_index, imported_dependency)
          add_index = add_index + 1
      index = index + 1

    return dependencies

  def DirectAndImportedDependencies(self, targets, dependencies=None):
    """Returns a list of a target's direct dependencies and all indirect
    dependencies that a dependency has advertised settings should be exported
    through the dependency for.
    """

    dependencies = self.DirectDependencies(dependencies)
    return self._AddImportedDependencies(targets, dependencies)

  def DeepDependencies(self, dependencies=None):
    """Returns an OrderedSet of all of a target's dependencies, recursively."""
    if dependencies is None:
      # Using a list to get ordered output and a set to do fast "is it
      # already added" checks.
      dependencies = OrderedSet()

    for dependency in self.dependencies:
      # Check for None, corresponding to the root node.
      if dependency.ref is None:
        continue
      if dependency.ref not in dependencies:
        dependency.DeepDependencies(dependencies)
        dependencies.add(dependency.ref)

    return dependencies

  def _LinkDependenciesInternal(self, targets, include_shared_libraries, dependencies=None, initial=True):
    """Returns an OrderedSet of dependency targets that are linked
    into this target.

    This function has a split personality, depending on the setting of
    |initial|.  Outside callers should always leave |initial| at its default
    setting.

    When adding a target to the list of dependencies, this function will
    recurse into itself with |initial| set to False, to collect dependencies
    that are linked into the linkable target for which the list is being built.

    If |include_shared_libraries| is False, the resulting dependencies will not
    include shared_library targets that are linked into this target.
    """
    if dependencies is None:
      # Using a list to get ordered output and a set to do fast "is it
      # already added" checks.
      dependencies = OrderedSet()

    # Check for None, corresponding to the root node.
    if self.ref is None:
      return dependencies

    # It's kind of sucky that |targets| has to be passed into this function,
    # but that's presently the easiest way to access the target dicts so that
    # this function can find target types.

    if 'target_name' not in targets[self.ref]:
      raise GypError("Missing 'target_name' field in target.")

    if 'type' not in targets[self.ref]:
      raise GypError("Missing 'type' field in target %s" % targets[self.ref]['target_name'])

    target_type = targets[self.ref]['type']

    is_linkable = target_type in linkable_types

    if initial and not is_linkable:
      # If this is the first target being examined and it's not linkable,
      # return an empty list of link dependencies, because the link
      # dependencies are intended to apply to the target itself (initial is
      # True) and this target won't be linked.
      return dependencies

    # Don't traverse 'none' targets if explicitly excluded.
    if target_type == 'none' and not targets[self.ref].get('dependencies_traverse', True):
      dependencies.add(self.ref)
      return dependencies

    # Executables, mac kernel extensions, windows drivers and loadable modules
    # are already fully and finally linked. Nothing else can be a link
    # dependency of them, there can only be dependencies in the sense that a
    # dependent target might run an executable or load the loadable_module.
    if not initial and target_type in ('executable', 'loadable_module', 'mac_kernel_extension', 'windows_driver'):
      return dependencies

    # Shared libraries are already fully linked.  They should only be included
    # in |dependencies| when adjusting static library dependencies (in order to
    # link against the shared_library's import lib), but should not be included
    # in |dependencies| when propagating link_settings.
    # The |include_shared_libraries| flag controls which of these two cases we
    # are handling.
    if not initial and target_type == 'shared_library' and not include_shared_libraries:
      return dependencies

    # The target is linkable, add it to the list of link dependencies.
    if self.ref not in dependencies:
      dependencies.add(self.ref)
      if initial or not is_linkable:
        # If this is a subsequent target and it's linkable, don't look any
        # further for linkable dependencies, as they'll already be linked into
        # this target linkable.  Always look at dependencies of the initial
        # target, and always look at dependencies of non-linkables.
        for dependency in self.dependencies:
          # noinspection PyProtectedMember
          dependency._LinkDependenciesInternal(targets, include_shared_libraries, dependencies, False)
    return dependencies

  def DependenciesForLinkSettings(self, targets):
    """
    Returns a list of dependency targets whose link_settings should be merged
    into this target.
    """

    # TODO(sbaig) Currently, chrome depends on the bug that shared libraries'
    # link_settings are propagated.  So for now, we will allow it, unless the
    # 'allow_sharedlib_linksettings_propagation' flag is explicitly set to
    # False.  Once chrome is fixed, we can remove this flag.
    include_shared_libraries = targets[self.ref].get('allow_sharedlib_linksettings_propagation', True)
    return self._LinkDependenciesInternal(targets, include_shared_libraries)

  def DependenciesToLinkAgainst(self, targets):
    """
    Returns a list of dependency targets that are linked into this target.
    """
    return self._LinkDependenciesInternal(targets, True)


def VerifyNoGYPFileCircularDependencies(targets):
  # Create a DependencyGraphNode for each gyp file containing a target.  Put
  # it into a dict for easy access.
  dependency_nodes = OrderedDict()
  for target in targets.keys():
    build_file = BuildFile(target)
    if not build_file in dependency_nodes:
      dependency_nodes[build_file] = DependencyGraphNode(build_file)

  # Set up the dependency links.
  for target, spec in targets.items():
    build_file = BuildFile(target)
    build_file_node = dependency_nodes[build_file]
    target_dependencies = spec.get('dependencies', [])
    for dependency in target_dependencies:
      try:
        dependency_build_file = BuildFile(dependency)
      except GypError as e:
        ExceptionAppend(e, 'while computing dependencies of .gyp file %s' % build_file)
        raise

      if dependency_build_file == build_file:
        # A .gyp file is allowed to refer back to itself.
        continue
      dependency_node = dependency_nodes.get(dependency_build_file)
      if not dependency_node:
        raise GypError("Dependency '%s' not found" % dependency_build_file)
      if dependency_node not in build_file_node.dependencies:
        build_file_node.dependencies.append(dependency_node)
        dependency_node.dependents.append(build_file_node)

  # Files that have no dependencies are treated as dependent on root_node.
  root_node = DependencyGraphNode(None)
  for build_file_node in dependency_nodes.values():
    if len(build_file_node.dependencies) == 0:
      build_file_node.dependencies.append(root_node)
      root_node.dependents.append(build_file_node)

  root_node.FlattenToList_NoCycles(dependency_nodes)


def BuildDependencyGraph(targets):
  # Create a DependencyGraphNode for each target.  Put it into a dict for easy access.
  VerifyNoGYPFileCircularDependencies(targets)

  dependency_nodes = OrderedDict()
  for target in targets.keys():
    if target not in dependency_nodes:
      dependency_nodes[target] = DependencyGraphNode(target)

  # Set up the dependency links.  Targets that have no dependencies are treated as dependent on root_node.
  root_node = DependencyGraphNode(None)
  for target, spec in targets.items():
    target_node = dependency_nodes[target]
    dependencies = spec.get('dependencies')
    if not dependencies:
      target_node.dependencies = [root_node]
      root_node.dependents.append(target_node)
    else:
      for dependency in dependencies:
        dependency_node = dependency_nodes.get(dependency)
        if not dependency_node:
          raise GypError("Dependency '%s' not found while trying to load target %s" % (dependency, target))
        target_node.dependencies.append(dependency_node)
        dependency_node.dependents.append(target_node)

  flat_list = root_node.FlattenToList_NoCycles(dependency_nodes)
  return dict(dependency_nodes), flat_list
