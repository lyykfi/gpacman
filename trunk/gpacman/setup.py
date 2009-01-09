#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

from distutils.core import setup
import os

setup(
      name="gpacman",
      version="0.0.1",
      packages=["gpacman", "gpacman.ui"],
      scripts=["gnome-pacman.py"],
      data_files=[('share/gpacman/icons', ["data/icons/gpacman.png"]),
                  ('share/gpacman', ["data/gpacman.glade"]),
                  ('share/applications', ["data/gpacman.desktop"])]
      )
