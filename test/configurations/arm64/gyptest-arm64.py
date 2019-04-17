#!/usr/bin/env python

# Copyright (c) 2012 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Verifies build of an executable for ARM64 configurations.
"""

import TestGyp
from gyp.MSVS import VSSetup_PowerShell

test = TestGyp.TestGyp(formats=['msvs','ninja'], platforms=['win32'])

vs = VSSetup_PowerShell()
if not any('VC.Tools.ARM64' in p for p in vs['Packages']):
  test.skip_test("Skip because some machines don't have arm64")

test.run_gyp('configurations.gyp')
test.set_configuration('Debug|ARM64')
test.build('configurations.gyp', test.ALL)

output = test.run_dumpbin('/headers', test.built_file_path('configurations%s.exe' % 'ARM64'))
if 'AA64 machine (ARM64)' not in output:
  test.fail_test()
test.pass_test()
