#! /usr/bin/python3

import os, sys

sys.path.insert(1, os.path.expanduser("~/.notes_cfg/exe/configLib"))
from config_reader import *

target = "code_styles.concat.js"
stylesArr = get_code_styles()

try:
  os.remove(target)
except OSError:
  pass

f = open(target, "a")

for style in stylesArr:
  f.write(open(style, "r").read())
