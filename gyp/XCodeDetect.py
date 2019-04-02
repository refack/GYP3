"""Simplify access to Xcode information."""
import subprocess
from common import memoize


def run(*cmd_args):
  return subprocess.check_output(cmd_args, stderr=subprocess.PIPE).decode('utf-8').strip()


@memoize
def Version():
  version = ''
  try:
    lines = run('xcodebuild', '-version').splitlines()
    version = ''.join(lines[0].split()[-1].split('.'))
    version = (version + '0' * (3 - len(version))).zfill(4)
  except subprocess.CalledProcessError:
    pass
  try:
    lines = run('pkgutil', '--pkg-info=com.apple.pkg.CLTools_Executables').splitlines()
    for l in lines:
      n, v = l.split(': ', 1)
      if n != 'version':
        continue
      parts = v.split('.', 4)
      version = '%s%s%s%s' % tuple(parts[0:4])
      break
  except subprocess.CalledProcessError:
    pass
  return version


@memoize
def GetSdkVersionInfoItem(sdk, item):
  # xcodebuild requires Xcode and can't run on Command Line Tools-only systems from 10.7 onward.
  # Since the CLT has no SDK paths anyway, returning None is the most sensible route and should still do the right thing.
  try:
    return run('xcrun', '--sdk', sdk, item)
  except subprocess.CalledProcessError:
    return None


@memoize
def SDKVersion():
  try:
    out = run('xcrun', '--show-sdk-version')
  except subprocess.CalledProcessError:
    try:
      out = run('xcodebuild', '-version', '-sdk', '', 'SDKVersion')
    except subprocess.CalledProcessError:
      return None
  version = out.strip()
  return version


@memoize
def IPhoneSDKPath():
  try:
    path = GetSdkVersionInfoItem('iphoneos', '--show-sdk-path')
  except subprocess.CalledProcessError:
    return None
  return path


@memoize
def GetIOSCodeSignIdentityKey(identity):
  if not identity:
    return None
  output = run('security', 'find-identity', '-p', 'codesigning', '-v')
  output_lines = output.splitlines()
  match_lines = [line for line in output_lines if identity in line]
  assert len(match_lines) == 1, ("Not exactly one codesigning fingerprints for identity: %s \n%s" % (identity, output))
  fingerprint = match_lines[0].split()[1]
  return fingerprint


@memoize
def BuildMachineOSBuild():
  return run('sw_vers', '-buildVersion')
