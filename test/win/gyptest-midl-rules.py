#!/usr/bin/env python

# Copyright (c) 2012 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Handle default .idl build rules.
"""

import TestGyp
from gyp.MSVS import VSSetup_PowerShell

test = TestGyp.TestGyp(formats=['msvs', 'ninja'], platforms=['win32'])

CHDIR = 'idl-rules'
target_platforms = ['Win32', 'x64']

vs = VSSetup_PowerShell()
if any('VC.Tools.ARM64' in p for p in vs['Packages']):
  target_platforms.append('ARM64')

test.run_gyp('basic-idl.gyp', chdir=CHDIR)
for platform in target_platforms:
  test.set_configuration('Debug|%s' % platform)
  test.build('basic-idl.gyp', test.ALL, chdir=CHDIR)

  # Make sure ninja win_tool.py filters out noisy lines.
  if test.format == 'ninja' and 'Processing' in test.stdout():
    test.fail_test()

test.pass_test()
