"""
Verifies that the user can override the compiler using CC/CXX environment variables.
"""

import TestGyp

test = TestGyp.TestGyp(formats=['ninja', 'make'], platforms=['!win32'])

expected = ['"ccache cc"']

# Check that CC, CXX and LD set target compiler
with TestGyp.LocalEnv({
  'CC': expected[0],
}):
  test.run_gyp('compiler-exe.gyp')
  if test.format == 'make':
    expected_status = 2
  else:
    expected_status = 1
  test.build('compiler-exe.gyp', verbose=True, status=expected_status, match=lambda a, b: True)
  test.must_contain_all_lines(test.stdout(), expected)


test.pass_test()
