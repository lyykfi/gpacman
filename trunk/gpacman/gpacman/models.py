#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gobject


""" packagers_store """
class packagers_store(gtk.ListStore):
    
    def __init__(self, packages_list):
        gtk.ListStore.__init__(self, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
        
        for package in packages_list:
            self.append([package.installed, package.name, package.version, package.repo, package.installed])

""" repositaries_store """
class repositaries_store(gtk.ListStore):
    
    def __init__(self, repositaries_list):
        gtk.ListStore.__init__(self, gobject.TYPE_STRING)
        
        for repositary in repositaries_list:
            self.append([repositary.name])
            
""" _actions_store """
class actions_store(gtk.ListStore):
    global INSTALL_STRING, REMOVE_STRING
    
    def __init__(self, actions_list=None):
        gtk.ListStore.__init__(self, gobject.TYPE_STRING, gobject.TYPE_STRING)
        
        if actions_list <> None:
            for action in actions_list:
                self.append(action_list[0], action_list[1])
                    
    def count(self):
        i = 0
        for item in self:
            i+=1
            
        return i
    
    def isset(self, action):
        iter = self.get_iter_first()
        
        while iter <> None:
            item_name = self.get_value(iter, 1)
            item_state = self.get_value(iter, 0)
            
            if item_name == action[1]:
                if item_state <> action[0]:
                    return True
                
            iter = self.iter_next(iter)
        
        return False
    
    def remove_by_name(self, name):
        iter = self.get_iter_first()
        
        while iter <> None:
            item_name = self.get_value(iter, 1)
            
            if item_name == name:
                self.remove(iter)
                return True
                
            iter = self.iter_next(iter)
        
        return False