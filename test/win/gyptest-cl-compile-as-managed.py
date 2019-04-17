#!/usr/bin/env python

# Copyright (c) 2015 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Make sure compile as managed (clr) settings are extracted properly.
"""

import TestGyp

test = TestGyp.TestGyp(platforms=['win32'])

test.skip_test('Skipping C++/CLI test')

CHDIR = 'compiler-flags'
test.run_gyp('compile-as-managed.gyp', chdir=CHDIR)
test.build('compile-as-managed.gyp', "test-compile-as-managed", chdir=CHDIR)
# Must fail.
test.build('compile-as-managed.gyp', "test-compile-as-unmanaged",
  chdir=CHDIR, status=1)
test.pass_test()
