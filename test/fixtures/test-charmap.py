from __future__ import print_function
import sys
import locale

try:
  reload           # Python 2
except NameError:  # Python 3
  from importlib import reload

reload(sys)


def main():
  encoding = locale.getdefaultlocale()[1]
  if not encoding:
    return False

  sys.setdefaultencoding(encoding)
  textmap = {
    'cp936': u'\u4e2d\u6587',
    'cp1252': u'Lat\u012Bna',
    'cp932': u'\u306b\u307b\u3093\u3054'
  }
  if encoding in textmap:
    print(textmap[encoding])
  return True

if __name__ == '__main__':
  print(main())
