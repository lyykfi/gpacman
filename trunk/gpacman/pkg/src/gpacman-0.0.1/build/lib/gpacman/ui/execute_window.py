#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gtk.glade

from gpacman.constants import *
from vte import Terminal

class execute_window:
    global GLADE_FILE_PATH

    def __init__(self, main_window, flag=0):
        
        glade_xml = gtk.glade.XML(GLADE_FILE_PATH)
        
        #Widgets
        self._window = glade_xml.get_widget("execute_window")
        self._exit_button = glade_xml.get_widget("exit_button")
        self._hbox = glade_xml.get_widget("hbox1")
        self._flag = 0
        
        events_dict = {
            "on_exit_button_clicked": self.on_exit_button_clicked }
        glade_xml.signal_autoconnect(events_dict)
        
        #Main window
        self._main_window = main_window
        
        #Create terminal
        self._create_terminal()
        
    def _create_terminal(self):
    
        #Terminal
        self._terminal = Terminal()
        
        self._terminal.fork_command('bash')
        self._terminal.set_sensitive(False)
        self._terminal.connect("child-exited", self.on_terminal_child_exited)
        self._terminal.show()
        
        self._hbox.pack_start(self._terminal, False, False, 0)
        
    def show(self):
        self._window.show()
        
    def set_flag(self, flag):
       self._flag = flag 
    
    def execute(self, commands):
        
        for command in commands:
            self._terminal.feed_child(command)
        
    """ --- EVENTS --- """
            
    """ on_exit_button_clicked """
    def on_exit_button_clicked(self, widget, data=None):
        self._window.hide()
        
    """ self.on_terminal_child_exited() """
    def on_terminal_child_exited(self, term):
        self._main_window.update_packages_tree()
        self._exit_button.show()
        
        if self._flag == 1:
            self._main_window.clear_actions_store()
