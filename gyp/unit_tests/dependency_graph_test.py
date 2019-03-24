import unittest

from gyp import dependency_graph


class TestFindCycles(unittest.TestCase):
  def setUp(self):
    self.nodes = {}
    for x in ('a', 'b', 'c', 'd', 'e'):
      self.nodes[x] = dependency_graph.DependencyGraphNode(x)

  @staticmethod
  def _create_dependency(dependent, dependency):
    dependent.dependencies.append(dependency)
    dependency.dependents.append(dependent)

  def test_no_cycle_empty_graph(self):
    for label, node in self.nodes.items():
      self.assertEqual([], node.FindCycles())

  def test_no_cycle_line(self):
    self._create_dependency(self.nodes['a'], self.nodes['b'])
    self._create_dependency(self.nodes['b'], self.nodes['c'])
    self._create_dependency(self.nodes['c'], self.nodes['d'])

    for label, node in self.nodes.items():
      self.assertEqual([], node.FindCycles())

  def test_no_cycle_dag(self):
    self._create_dependency(self.nodes['a'], self.nodes['b'])
    self._create_dependency(self.nodes['a'], self.nodes['c'])
    self._create_dependency(self.nodes['b'], self.nodes['c'])

    for label, node in self.nodes.items():
      self.assertEqual([], node.FindCycles())

  def test_cycle_self_reference(self):
    self._create_dependency(self.nodes['a'], self.nodes['a'])

    self.assertEqual(
      [[self.nodes['a'], self.nodes['a']]],
      self.nodes['a'].FindCycles()
    )

  def test_cycle_two_nodes(self):
    self._create_dependency(self.nodes['a'], self.nodes['b'])
    self._create_dependency(self.nodes['b'], self.nodes['a'])

    self.assertEqual(
      [[self.nodes['a'], self.nodes['b'], self.nodes['a']]],
      self.nodes['a'].FindCycles()
    )
    self.assertEqual(
      [[self.nodes['b'], self.nodes['a'], self.nodes['b']]],
      self.nodes['b'].FindCycles()
    )

  def test_two_cycles(self):
    self._create_dependency(self.nodes['a'], self.nodes['b'])
    self._create_dependency(self.nodes['b'], self.nodes['a'])

    self._create_dependency(self.nodes['b'], self.nodes['c'])
    self._create_dependency(self.nodes['c'], self.nodes['b'])

    cycles = self.nodes['a'].FindCycles()
    self.assertTrue([self.nodes['a'], self.nodes['b'], self.nodes['a']] in cycles)
    self.assertTrue([self.nodes['b'], self.nodes['c'], self.nodes['b']] in cycles)
    self.assertEqual(2, len(cycles))

  def test_big_cycle(self):
    self._create_dependency(self.nodes['a'], self.nodes['b'])
    self._create_dependency(self.nodes['b'], self.nodes['c'])
    self._create_dependency(self.nodes['c'], self.nodes['d'])
    self._create_dependency(self.nodes['d'], self.nodes['e'])
    self._create_dependency(self.nodes['e'], self.nodes['a'])

    self.assertEqual(
      [
        [
          self.nodes['a'],
          self.nodes['b'],
          self.nodes['c'],
          self.nodes['d'],
          self.nodes['e'],
          self.nodes['a']
        ]
      ],
      self.nodes['a'].FindCycles())


if __name__ == '__main__':
  unittest.main()
