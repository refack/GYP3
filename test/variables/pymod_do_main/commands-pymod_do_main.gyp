{
  'variables': {
    'names': [
      "arguments",
      "array",
      "array-copywithin",
      "array-filter",
      "array-find",
      "array-findindex",
      "array-foreach",
      "array-join",
      "array-map",
      "array-of",
      "array-reverse",
      "array-slice",
      "array-splice",
      "array-unshift",
      "array-lastindexof",
      "base",
      "collections",
      "data-view",
      "extras-utils",
      "growable-fixed-array",
      "iterator",
      "object",
      "string",
      "typed-array",
      "typed-array-createtypedarray",
      "typed-array-filter",
      "typed-array-foreach",
      "typed-array-reduce",
      "typed-array-reduceright",
      "typed-array-slice",
      "typed-array-subarray",
    ],
    'output_root': 'real-output-root',
    'ret1': [
      '<!@pymod_do_main(ForEachFormat "<(output_root)/%s-from-name.cc" <@(names))',
      '<!@pymod_do_main(ForEachFormat "<(output_root)/%s-from-name.hpp" <@(names))'
    ],
    'ret1+': [ '<!@pymod_do_main(ForEachFormat "<(output_root)/%s-from-name.h" <@(names))' ],
  },
  'includes': [
    'commands-pymod_do_main.gypi',
  ],
  'targets': [
    {
      'target_name': 'foo',
      'type': 'none',
      'variables': {
        'ret2': '<!pymod_do_main(GetConstantValue 2)',
      },
      # 'actions': [
      #   {
      #     'action_name': 'test_action',
      #     'variables': {
      #       'ret3': '<!pymod_do_main(GetConstantValue 3)',
      #     },
      #     'inputs' : [
      #       '<@(ret1)',
      #     ],
      #     'outputs': [
      #       '<(ret2)',
      #       '<(ret3)',
      #       '<(ret4)',
      #     ],
      #     'action': [
      #       'echo',
      #       '<@(_inputs)',
      #       '<@(_outputs)',
      #     ],
      #   },
      # ],
    },
  ],
}
