#!/usr/bin/env python

# Copyright (c) 2015 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Make sure msvs_target_platform_version works correctly.
"""

import TestGyp
from gyp.MSVS import VSSetup_PowerShell

test = TestGyp.TestGyp(formats=['msvs'])

vs = VSSetup_PowerShell()
if not any('UWP.Support' in p for p in vs['Packages']):
  test.skip_test("Skip because some machines don't have UWP tools")

if vs['CatalogVersion'] < '2015':
  test.skip_test('For MSVS version >= 2015')

CHDIR = 'winrt-target-platform-version'

test.run_gyp('winrt-target-platform-version.gyp', chdir=CHDIR)

test.build('winrt-target-platform-version.gyp', 'enable_winrt_10_platversion_dll', chdir=CHDIR)

# Target Platform without Minimum Target Platform version defaults to a valid
# Target Platform and compiles.
test.build('winrt-target-platform-version.gyp', 'enable_winrt_10_platversion_nominver_dll', chdir=CHDIR)

# Target Platform is set to 9.0 which is invalid for 2015 projects so
# compilation must fail.
test.build('winrt-target-platform-version.gyp', 'enable_winrt_9_platversion_dll', chdir=CHDIR, status=1)

# Missing Target Platform for 2015 projects must fail.
test.build('winrt-target-platform-version.gyp', 'enable_winrt_missing_platversion_dll', chdir=CHDIR, status=1)

test.pass_test()
