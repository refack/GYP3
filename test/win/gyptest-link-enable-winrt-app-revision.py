#!/usr/bin/env python

# Copyright (c) 2013 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Make sure msvs_application_type_revision works correctly.
"""

import TestGyp
from gyp.MSVS import VSSetup_PowerShell

test = TestGyp.TestGyp(formats=['msvs'])

vs = VSSetup_PowerShell()
if not any('UWP.Support' in p for p in vs['Packages']):
  test.skip_test("Skip because some machines don't have UWP tools")

if vs['CatalogVersion'] < '2013':
  test.skip_test('For MSVS version >= 2013')

CHDIR = 'winrt-app-type-revision'

test.run_gyp('winrt-app-type-revision.gyp', chdir=CHDIR)

test.build('winrt-app-type-revision.gyp', 'enable_winrt_81_revision_dll', chdir=CHDIR)

# Revision is set to 8.2 which is invalid for 2013 projects so compilation
# must fail.
test.build('winrt-app-type-revision.gyp', 'enable_winrt_82_revision_dll', chdir=CHDIR, status=1)

# Revision is set to an invalid value for 2013 projects so compilation
# must fail.
test.build('winrt-app-type-revision.gyp', 'enable_winrt_invalid_revision_dll', chdir=CHDIR, status=1)

test.pass_test()
