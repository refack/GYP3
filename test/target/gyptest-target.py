#!/usr/bin/env python

# Copyright (c) 2009 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Verifies simplest-possible build of a "Hello, world!" program
using non-default extension. In particular, verifies how
target_extension is used to avoid MSB8012 for msvs.
"""

import TestGyp

test = TestGyp.TestGyp(platforms=['win32'])

test.run_gyp('target.gyp')
test.build('target.gyp')

# executables
test.built_file_must_exist('hello1.stuff', test.EXECUTABLE, bare=True)
test.built_file_must_exist('hello2.exe', test.EXECUTABLE, bare=True)
test.built_file_must_not_exist('hello2.stuff', test.EXECUTABLE, bare=True)

# check msvs log for errors
if test.format == "msvs":
  if test.check_log(lambda c: "MSB8012" in c):
    test.fail("MSB8012 in link output")

test.pass_test()
