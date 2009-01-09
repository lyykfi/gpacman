#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import os, ConfigParser

""" config_manager """
class config_manager:
    
    __instance = None
    
    """ Implementation of the singleton interface """
    class __impl:
        
        def __init__(self):
            self.config_parser = ConfigParser.ConfigParser()
            
            self._config_file = "~/.gpacman"
            self._real_config_file_path = os.path.expanduser(self._config_file)
                
            if os.path.exists(self._real_config_file_path) == True:
                self.config_parser.read(self._real_config_file_path)
            else:
                config = ConfigParser.RawConfigParser()
                    
                config.add_section('General')
                config.set('General', 'tray', 'true')
                config.set('General', 'install_string', 'Install')
                config.set('General', 'remove_string', 'Remove')
                config.set('General', 'glade_file', 'gpacman.glade')
                config.set('General', 'path_to_pacman_lib', '/var/lib/pacman/')
                config.set('General', 'path_conf_file', '/etc/pacman.conf')
                config.set('General', 'server_indificator', 'Server')
                config.set('General', 'version', '0.0.1')
                config.set('General', 'data_dir', '/usr/share/gpacman')
                    
                configfile = open(self._real_config_file_path, 'wb')
                config.write(configfile)
                
                configfile.close()
                self.config_parser.read(self._real_config_file_path)
        
    """ __init__ """
    def __init__(self):
        if config_manager.__instance is None:
            config_manager.__instance = config_manager.__impl()

    """ Delegate access to implementation """
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    """ Delegate access to implementation """
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

if os.path.exists(os.getcwd()+"/data"):
    DATA_DIR = os.getcwd()+"/data"
else:
    DATA_DIR = config_manager.config_parser.get("General", "DATA_DIR")

 
