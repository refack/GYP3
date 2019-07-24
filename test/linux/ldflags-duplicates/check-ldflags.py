#!/usr/bin/env python

# Copyright (c) 2015 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Verifies duplicate ldflags are not removed.
"""

from __future__ import print_function

import sys

def CheckContainsFlags(args, substring):
  found = substring in args
  if not found:
    print('ERROR: Linker arguments "%s" are missing in "%s"' % (substring,
                                                                args))
  return found

if __name__ == '__main__':
  args = " ".join(sys.argv)
  print("args = " + args)
  if (not CheckContainsFlags(args, 'lib1.a -Wl,--no-whole-archive')
      or not CheckContainsFlags(args, 'lib2.a -Wl,--no-whole-archive')):
    sys.exit(1)
  sys.exit(0)
