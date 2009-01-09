#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gtk.glade
from config_manager import *

class about_dialog:

    def __init__(self):
        
        cfg_manager = config_manager()
        glade = gtk.glade.XML(DATA_DIR+"/"+cfg_manager.config_parser.get("General", "glade_file"))
        
        self.about_window = glade.get_widget("about_dialog")
