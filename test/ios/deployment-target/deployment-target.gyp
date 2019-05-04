# Copyright (c) 2013 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
{
  'xcode_settings': {
    'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
    'CLANG_CXX_LANGUAGE_STANDARD': 'c++14',
    'CLANG_CXX_LIBRARY': 'libc++',
    'ALWAYS_SEARCH_USER_PATHS': 'NO',
    'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
    'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
                                              # (Equivalent to -fPIC)
    'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',        # -fno-exceptions
    'GCC_ENABLE_CPP_RTTI': 'NO',              # -fno-rtti
    'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings
    'PREBINDING': 'NO',                       # No -Wl,-prebind
    'USE_HEADERMAP': 'NO',
    'OTHER_CFLAGS': [
      '-fembed-bitcode',
      '-fno-strict-aliasing',
    ],
    'WARNING_CFLAGS': [
      '-Wall',
      '-Wendif-labels',
      '-W',
      '-Wno-unused-parameter',
    ],
  },
  'targets': [
    {
      'target_name': 'iphoneos-version-min-8.0',
      'type': 'executable',
      'mac_bundle': 1,
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_IOS_VERSION_MIN=__IPHONE_8_0', ],
      'xcode_settings': {
        'ARCHS': ['arm64'],
        'SDKROOT': 'iphoneos',
        'IPHONEOS_DEPLOYMENT_TARGET': '8.0',
      },
      'target_conditions': [
        ['_type!="static_library"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-fembed-bitcode',
            ],
          },
        }],
      ],
    },
    {
      'target_name': 'libiphoneos-version-min-8.0',
      'type': 'static_library',
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_IOS_VERSION_MIN=__IPHONE_8_0', ],
      'xcode_settings': {
        'ARCHS': ['arm64'],
        'SDKROOT': 'iphoneos',
        'IPHONEOS_DEPLOYMENT_TARGET': '8.0',
      },
      'target_conditions': [
        ['_type!="static_library"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-fembed-bitcode',
            ],
          },
        }],
      ],
    },
    {
      'target_name': 'libiphonesimulator-version-min-8.0',
      'type': 'static_library',
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_IOS_VERSION_MIN=__IPHONE_8_0', ],
      'xcode_settings': {
        'ARCHS': ['x86_64'],
        'SDKROOT': 'iphonesimulator',
        'IPHONEOS_DEPLOYMENT_TARGET': '8.0',
      },
      'target_conditions': [
        ['_type!="static_library"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-fembed-bitcode',
            ],
          },
        }],
      ],
    },
    {
      'target_name': 'iphoneos-version-min-12.0',
      'type': 'executable',
      'mac_bundle': 1,
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_IOS_VERSION_MIN=__IPHONE_12_0', ],
      'xcode_settings': {
        'ARCHS': ['arm64'],
        'SDKROOT': 'iphoneos',
        'IPHONEOS_DEPLOYMENT_TARGET': '12.0',
      },
      'target_conditions': [
        ['_type!="static_library"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-fembed-bitcode',
            ],
          },
        }],
      ],
    },
    {
      'target_name': 'libiphoneos-version-min-12.0',
      'type': 'static_library',
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_IOS_VERSION_MIN=__IPHONE_12_0', ],
      'xcode_settings': {
        'ARCHS': ['arm64'],
        'SDKROOT': 'iphoneos',
        'IPHONEOS_DEPLOYMENT_TARGET': '12.0',
      },
      'target_conditions': [
        ['_type!="static_library"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-fembed-bitcode',
            ],
          },
        }],
      ],
    },
    {
      'target_name': 'libiphonesimulator-version-min-12.0',
      'type': 'static_library',
      'sources': [ 'check-version-min.c', ],
      'defines': [ 'GYPTEST_IOS_VERSION_MIN=__IPHONE_12_0', ],
      'xcode_settings': {
        'ARCHS': ['x86_64'],
        'SDKROOT': 'iphonesimulator',
        'IPHONEOS_DEPLOYMENT_TARGET': '12.0',
      },
      'target_conditions': [
        ['_type!="static_library"', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-fembed-bitcode',
            ],
          },
        }],
      ],
    },
  ],
}

