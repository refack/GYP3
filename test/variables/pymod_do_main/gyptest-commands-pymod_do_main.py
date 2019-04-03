"""
Test variable expansion of '<!pymod_do_main()' syntax commands.
"""

from __future__ import print_function

import TestGyp

test = TestGyp.TestGyp(format='gypd')

expect = test.read('commands-pymod_do_main.gyp.stdout')

test.run_gyp('commands-pymod_do_main.gyp', '--debug', 'variables', stdout=expect, ignore_line_numbers=True)

# Verify the commands.gypd against the checked-in expected contents.
#
# Normally, we should canonicalize line endings in the expected
# contents file setting the Subversion svn:eol-style to native,
# but that would still fail if multiple systems are sharing a single
# workspace on a network-mounted file system.  Consequently, we
# massage the Windows line endings ('\r\n') in the output to the
# checked-in UNIX endings ('\n').

contents = test.read('commands-pymod_do_main.gypd')
expect = test.read('commands-pymod_do_main.gypd.golden')
if not test.match(contents, expect):
  print("Unexpected contents of `commands-pymod_do_main.gypd'")
  test.diff(expect, contents, 'commands-pymod_do_main.gypd ')
  test.fail_test()

test.pass_test()
