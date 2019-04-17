# Copyright (c) 2016 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os

import TestGyp

test = TestGyp.TestGyp(formats=['msvs'])

test.skip_test('Skipping C++/CLI test')

if os.environ.get('GYP_MSVS_VERSION', 0) < 2015:
  test.skip_test('Skipping test for MSVS < 2015')

CHDIR = 'compiler-flags'

test.run_gyp('compile-as-winrt.gyp', chdir=CHDIR)

test.build('compile-as-winrt.gyp', 'test-compile-as-winrt', chdir=CHDIR)

test.pass_test()
