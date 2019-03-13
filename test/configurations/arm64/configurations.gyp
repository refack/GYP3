# Copyright (c) 2009 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'target_defaults': {
    'configurations': {
      'Debug': {
        'msvs_configuration_platform': 'ARM64',
      },
    },
  },
  'targets': [
    {
      'target_name': 'configurationsARM64',
      'type': 'executable',
      'sources': [
        'configurations.c',
      ],
    },
  ],
}
