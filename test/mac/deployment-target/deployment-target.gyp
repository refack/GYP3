# Copyright (c) 2013 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
{
  'xcode_settings': {
    'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
    'CLANG_CXX_LANGUAGE_STANDARD': 'c++14',
    'CLANG_CXX_LIBRARY': 'libc++',
  },
  'targets': [
    {
      'target_name': 'macosx-version-min-10.9',
      'type': 'executable',
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_MAC_VERSION_MIN=__MAC_10_9', ],
      'xcode_settings': {
        'SDKROOT': 'macosx',
        'MACOSX_DEPLOYMENT_TARGET': '10.9',
      },
    },
    {
      'target_name': 'macosx-version-min-10.14',
      'type': 'executable',
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_MAC_VERSION_MIN=__MAC_10_14', ],
      'xcode_settings': {
        'SDKROOT': 'macosx',
        'MACOSX_DEPLOYMENT_TARGET': '10.14',
      },
    },
  ],
}

