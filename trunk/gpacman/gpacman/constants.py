#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import os

TRAY = True
INSTALLED = True
INSTALL_STRING = "Install"
REMOVE_STRING = "Remove"
GLADE_FILE = "gpacman.glade" 
PATH_TO_PACMAN_LIB = "/var/lib/pacman/"
PATH_TO_PACMAN_LOCAL = PATH_TO_PACMAN_LIB+"local"
PATH_TO_PACMAN_SYNC = PATH_TO_PACMAN_LIB+"sync"
PATH_CONF_FILE = "/etc/pacman.conf"
SERVER_INDIFICATOR = "Server="

VERSION = "0.0.1"


if INSTALLED == False:
    DATA_DIR = os.getcwd()+"/data"
else:
    DATA_DIR = '/usr/share/gpacman'
    
GLADE_FILE_PATH = DATA_DIR+"/"+GLADE_FILE
ICONS_DIR_PATH = DATA_DIR+"/icons"
