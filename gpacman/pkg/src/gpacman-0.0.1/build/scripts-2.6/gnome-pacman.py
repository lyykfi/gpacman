#!/usr/bin/python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gtk.gdk
import threading
import gobject
import gpacman, gpacman.ui

from gpacman.ui.main_window import *
from gpacman.constants import *

""" gnome_pacman """
class gnome_pacman():
    global ICONS_DIR_PATH
    
    def __init__(self):
        gtk.gdk.threads_init()
        gobject.threads_init()
        
        self._gpacmanGUI = gpacmanGUI()
    
    def run(self):
        self._gpacmanGUI.show()
        
        #Start main loop
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
            
""" gpacmanGUI """
class gpacmanGUI:
    def __init__(self):
        
        self._main_window = main_window()
       
        #Objects
        self._popup_menu = gtk.Menu()
        self._trayicon = gtk.status_icon_new_from_file(ICONS_DIR_PATH+"/"+"gpacman.png")
        
        #Inits
        self._init_tray()
        self._init_popup_menu()
        
    """ show """
    def show(self):
        self._main_window.window.show()
        self._main_window.window.maximize()
        
    """ _init_tray """
    def _init_tray(self):
        self._trayicon.set_visible(True)
        self._trayicon.connect('popup-menu', self.on_popup_menu)
        self._trayicon.connect('activate', self.on_popup_menu_activate)
        
    """ _init_popup_menu """
    def _init_popup_menu(self):
        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        quit.connect('activate', self.on_quit)
        
        self._popup_menu = gtk.Menu()
        self._popup_menu.append(quit)
        self._popup_menu.show_all()
        
    """ --- EVENTS --- """
    
    """ on_popup_menu """
    def on_popup_menu(self, obj, button, time):
        self._popup_menu.popup(None, None, None, button, time)
    
    """ on_quit """
    def on_quit(self, obj):
        gtk.main_quit()
    
    """ on_popup_menu_activate """
    def on_popup_menu_activate(self, icon):
        self._main_window.window.destroy()
        self._main_window = main_window()
            
        self._main_window.window.show()
        self._main_window.window.maximize()

if __name__ == "__main__":
    
    gnome_pacman = gnome_pacman()
    gnome_pacman.run()
    
