#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gtk.glade

from vte import Terminal
from gpacman.constants import *

class setting_window:
    global GLADE_FILE_PATH
    
    def __init__(self, main_window, flag=0):
        
        glade_xml = gtk.glade.XML(GLADE_FILE_PATH)
        
        #Widgets
        self._window = glade_xml.get_widget("setting_window")
        
        events_dict = { 
    		"on_cancel_button_clicked": self.on_cancel_button_clicked}
        glade_xml.signal_autoconnect(events_dict)
        
        #Main window
        self._main_window = main_window
        
    def show(self):
        self._window.show()
        
    """ --- EVENTS --- """
    
    def on_cancel_button_clicked(self, widget, data=None):
        self._window.hide()
