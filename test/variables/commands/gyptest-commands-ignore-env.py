#!/usr/bin/env python

# Copyright (c) 2012 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Test that environment variables are ignored when --ignore-environment is
specified.
"""

from __future__ import print_function
import os
import sys

import TestGyp

test = TestGyp.TestGyp(format='gypd')

os.environ['GYP_DEFINES'] = 'FOO=BAR'
os.environ['GYP_GENERATORS'] = 'foo'
os.environ['GYP_GENERATOR_FLAGS'] = 'genflag=foo'
os.environ['GYP_GENERATOR_OUTPUT'] = 'somedir'

expect = test.read('commands.gyp.ignore-env.stdout').replace('\r\n', '\n')

stdout, stderr = test.run_gyp('commands.gyp', '--debug', 'variables', '--ignore-environment')
if sys.version_info.major == 2:
  if not (TestGyp.match_modulo_line_numbers(expect, stdout)):
    test.diff(expect, stdout, 'commands.gyp ')


# Verify the commands.gypd against the checked-in expected contents.
#
# Normally, we should canonicalize line endings in the expected
# contents file setting the Subversion svn:eol-style to native,
# but that would still fail if multiple systems are sharing a single
# workspace on a network-mounted file system.  Consequently, we
# massage the Windows line endings ('\r\n') in the output to the
# checked-in UNIX endings ('\n').
if sys.version_info.major == 2:
  contents = test.read('commands.gypd').replace('\r', '')
  expect = test.read('commands.gypd.golden').replace('\r', '')
  if not test.match(contents, expect):
    print("Unexpected contents of `commands.gypd'")
    test.diff(expect, contents, 'commands.gypd ')
  test.pass_test()
else:
  test.skip_test("fix compare for Python 3")
