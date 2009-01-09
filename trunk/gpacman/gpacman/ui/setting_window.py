#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gtk.glade

from vte import Terminal
from config_manager import *

class setting_window:
    
    def __init__(self):
        
        cfg_manager = config_manager()
        glade_xml = gtk.glade.XML(DATA_DIR+"/"+cfg_manager.config_parser.get("General", "glade_file"))
        
        #Widgets
        self._window = glade_xml.get_widget("setting_window")
        
        events_dict = { 
    		"on_cancel_button_clicked": self.on_cancel_button_clicked}
        glade_xml.signal_autoconnect(events_dict)
        
    def show(self):
        self._window.show()
        
    """ --- EVENTS --- """
    
    def on_cancel_button_clicked(self, widget, data=None):
        self._window.hide()
