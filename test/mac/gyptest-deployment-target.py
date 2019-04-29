#!/usr/bin/env python

# Copyright (c) 2013 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Verifies that MACOSX_DEPLOYMENT_TARGET works.
"""

import TestGyp

test = TestGyp.TestGyp(formats=['make', 'ninja', 'xcode'], platforms=['darwin'])

test.run_gyp('deployment-target.gyp', chdir='deployment-target')

test.build('deployment-target.gyp', test.ALL, chdir='deployment-target')

test.pass_test()

