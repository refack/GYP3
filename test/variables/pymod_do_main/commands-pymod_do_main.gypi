# This file is included from commands-pymod_do_main.gyp to test evaluation order of includes.
{
  'variables': {
    'ret4': '<!pymod_do_main(GetConstantValue 4)',
  },
  'targets': [
    {
      'target_name': 'dummy',
      'type': 'none',
      'variables': {
        'ret5': '<!pymod_do_main(GetConstantValue 5)',
      },
    },
  ],
}
