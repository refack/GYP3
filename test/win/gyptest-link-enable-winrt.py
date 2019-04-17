#!/usr/bin/env python

# Copyright (c) 2013 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Make sure msvs_enable_winrt works correctly.
"""

import TestGyp
from gyp.MSVS import VSSetup_PowerShell

test = TestGyp.TestGyp(formats=['msvs'])

vs = VSSetup_PowerShell()
if not any('UWP.Support' in p for p in vs['Packages']):
  test.skip_test("Skip because some machines don't have UWP tools")

if vs['CatalogVersion'] < '2013':
  test.skip_test('For MSVS version >= 2013')

CHDIR = 'enable-winrt'

test.run_gyp('enable-winrt.gyp', chdir=CHDIR)

test.build('enable-winrt.gyp', 'enable_winrt_dll', chdir=CHDIR)

test.build('enable-winrt.gyp', 'enable_winrt_missing_dll', chdir=CHDIR, status=1)

test.build('enable-winrt.gyp', 'enable_winrt_winphone_dll', chdir=CHDIR)

test.pass_test()
