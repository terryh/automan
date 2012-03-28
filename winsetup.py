#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import sys

filename = 'automan.py'
#... this creates the filename of your .exe file in the dist folder
#
if filename.endswith(".py"):
    distribution = filename[:-3]
elif filename.endswith(".pyw"):
    distribution = filename[:-4]

# if run without args, build executables in quiet mode
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

opts = {
        "py2exe":{
        "compressed": 1,
        #"ascii": 1,
        "optimize": 2,
        "bundle_files": 1,

        }
        }

setup(
    version = "0.4",
    author ="TerryH",
    author_email ="terryh.tp@gmail.com",
    name = "AutoMan",
    options = opts,
    zipfile = None,
    windows=["automan.py"],
    #console=["autohts.py"],
    )

