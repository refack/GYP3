#!/bin/bash -ex

python ../../../gyp_main.py --debug variables --format gypd --depth . commands-pymod_do_main.gyp > commands-pymod_do_main.gyp.stdout
/usr/bin/mv -f commands-pymod_do_main.gypd commands-pymod_do_main.gypd.golden
