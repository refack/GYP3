#!/bin/bash
# Copyright (c) 2014 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

set -e

# Xcode version is newer than 5.0, check that SDKROOT is set.
[[ "${SDKROOT}" == "$(xcodebuild -version -sdk '' Path)" ]]
