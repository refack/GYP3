# Copyright (c) 2014 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
TestMac.py:  a collection of helper function shared between test on Mac OS X.
"""

from __future__ import print_function

import re
import subprocess

__all__ = ['Xcode', 'CheckFileType']


def CheckFileType(test, file, archs):
  """Check that |file| contains exactly |archs| or fails |test|."""
  proc = subprocess.Popen(['lipo', '-info', file], stdout=subprocess.PIPE)
  o = proc.communicate()[0].decode('utf-8').strip()
  assert not proc.returncode
  if len(archs) == 1:
    pattern = re.compile('^Non-fat file: (.*) is architecture: (.*)$')
  else:
    pattern = re.compile('^Architectures in the fat file: (.*) are: (.*)$')
  match = pattern.match(o)
  if match is None:
    print('Output does not match expected pattern: %s' % pattern.pattern)
    test.fail_test()
  else:
    found_file, found_archs = match.groups()
    if found_file != file or set(found_archs.split()) != set(archs):
      print('Expected file %s with arch %s, got %s with arch %s' % (file, ' '.join(archs), found_file, found_archs))
      test.fail_test()


def run(*cmd_args):
  return subprocess.check_output(cmd_args, stderr=subprocess.PIPE).decode('utf-8')


class Xcode(object):
  """Simplify access to Xcode information."""
  _cache = {}

  @staticmethod
  def Version():
    if 'Version' not in Xcode._cache:
      version = ''
      try:
        lines = run('xcodebuild', '-version').splitlines()
        version = ''.join(lines[0].decode('utf-8').split()[-1].split('.'))
        version = (version + '0' * (3 - len(version))).zfill(4)
      except subprocess.CalledProcessError:
        pass
      try:
        lines = run('pkgutil', '--pkg-info=com.apple.pkg.CLTools_Executables').splitlines()
        for l in lines:
          n, v = l.split(': ', 1)
          if n != 'version':
            continue
          parts = v.split('.',4)
          version = '%s%s%s%s' % tuple(parts[0:4])
          break
      except subprocess.CalledProcessError:
        pass
      Xcode._cache['Version'] = version
    return Xcode._cache['Version']

  @staticmethod
  def SDKVersion():
    if 'SDKVersion' not in Xcode._cache:
      out = ''
      try:
        out = run('xcrun', '--show-sdk-version')
      except subprocess.CalledProcessError:
        pass
      try:
        out = run('xcodebuild', '-version', '-sdk', '', 'SDKVersion')
      except subprocess.CalledProcessError:
        pass
      Xcode._cache['SDKVersion'] = out.strip()
    return Xcode._cache['SDKVersion']

  @staticmethod
  def HasIPhoneSDK():
    if 'HasIPhoneSDK' not in Xcode._cache:
      try:
        out = run('xcrun', '--sdk', 'iphoneos', '--show-sdk-path')
      except subprocess.CalledProcessError:
        out = 1
      Xcode._cache['HasIPhoneSDK'] = out == 0
    return Xcode._cache['HasIPhoneSDK']


