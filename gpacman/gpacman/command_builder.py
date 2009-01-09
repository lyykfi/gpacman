#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar


class command_builder:
    global INSTALL_STRING, REMOVE_STRING, GLADE_FILE

    def build_action_commands(self, model):
        command_list = []
        remove_command = "sudo pacman --noconfirm -R "
        add_command = "sudo pacman --noconfirm -S "
        
        count_add = 0
        count_remove = 0
        
        iter = model.get_iter_first()

        while ( iter != None ):
            value_type = model.get_value(iter, 0)
            value_name = model.get_value(iter, 1)
                
            if value_type == INSTALL_STRING:
                add_command = add_command+value_name
                count_add+= 1
            else:
                remove_command = remove_command+value_name
                count_remove+= 1
                
            iter = model.iter_next(iter)
            
            if iter != None:
                add_command+=", "
                remove_command+=", "
        
        if count_remove > 0:
            command_list.append(remove_command+"\n")
        
        if count_add > 0:
            command_list.append(add_command+"\n")
            
        command_list.append(self._append_exit())
        
        return command_list
        
    def build_refresh_commands(self):
        command_list = ["sudo pacman -Sy --noconfirm \n", self._append_exit()]
        
        return command_list
        
    def build_update_commands(self):
        command_list = ["sudo pacman -Suy --noconfirm \n", self._append_exit()]
        
        return command_list
        
    def _append_exit(self):
        return "exit \n"
