#!/usr/bin/env python

# Copyright (c) 2012 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Verifies simple actions when using an explicit build target of 'all'.
"""

import glob
import os

import TestGyp

test = TestGyp.TestGyp()

test.run_gyp('actions.gyp', chdir='src')

# Some gyp files use an action that mentions an output but never writes it as a means to making the action run on every build.
# That doesn't mesh well with ninja's semantics.
# TODO(evan): figure out how to work always-run actions in to ninja.
test.build('actions.gyp', test.ALL, chdir='src')
test.must_match('src/subdir1/actions-out/action-counter.txt', '1')
test.must_match('src/subdir1/actions-out/action-counter_2.txt', '1')
if test.format not in ['ninja', 'xcode-ninja']:
  # Test that an "always run" action increases a counter on multiple
  # invocations, and that a dependent action updates in step.
  test.build('actions.gyp', test.ALL, chdir='src')
  test.must_match('src/subdir1/actions-out/action-counter.txt', '2')
  test.must_match('src/subdir1/actions-out/action-counter_2.txt', '2')

  # The "always run" action only counts to 2, but the dependent target
  # will count forever if it's allowed to run. This verifies that the
  # dependent target only runs when the "always run" action generates
  # new output, not just because the "always run" ran.
  test.build('actions.gyp', test.ALL, chdir='src')
  test.must_match('src/subdir1/actions-out/action-counter.txt', '2')
  test.must_match('src/subdir1/actions-out/action-counter_2.txt', '2')

expect = """\
Hello from program.c
Hello from make-prog1.py
Hello from make-prog2.py
"""

if test.format == 'xcode':
  chdir = 'src/subdir1'
else:
  chdir = 'src'
test.run_built_executable('program', chdir=chdir, stdout=expect)


test.must_match('src/subdir2/file.out', "Hello from make-file.py\n")


expect = "Hello from generate_main.py\n"

if test.format == 'xcode':
  chdir = 'src/subdir3'
else:
  chdir = 'src'
test.run_built_executable('null_input', chdir=chdir, stdout=expect)


# Clean out files which may have been created if test.ALL was run.
def clean_dep_files():
  for f in (glob.glob('src/dep*.txt')):
    os.remove(f)

# Confirm our clean.
clean_dep_files()
test.must_not_exist('src/dep_1.txt')
test.must_not_exist('src/deps_all_done_first_123.txt')

# Make sure all deps finish before an action is run on a 'None' target.
# If using the Make builder, add -j to make things more difficult.
arguments = []
if test.format == 'make':
  arguments = ['-j']
test.build('actions.gyp', 'action_with_dependencies_123', chdir='src', arguments=arguments)
test.must_exist('src/deps_all_done_first_123.txt')

# Try again with a target that has deps in reverse.  Output files from
# previous tests deleted.  Confirm this execution did NOT run the ALL
# target which would mess up our dep tests.
clean_dep_files()

arguments = []
if test.format == 'make':
  arguments = ['-j']
test.build('actions.gyp', 'action_with_dependencies_321', chdir='src', arguments=arguments)
test.must_exist('src/deps_all_done_first_321.txt')
test.must_not_exist('src/deps_all_done_first_123.txt')


test.pass_test()
