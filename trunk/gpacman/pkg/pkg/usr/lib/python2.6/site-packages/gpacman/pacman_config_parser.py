#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import os
from constants import *
from repository import repository

class pacman_config_parser:
    global PATH_CONF_FILE, SERVER_INDIFICATOR
    
    def parse(self):
        repositaries = []
		
        conf_file = file(PATH_CONF_FILE, "r").read()
        conf_file_lines = conf_file.splitlines()
        
        i = 0;
        
        for line in conf_file_lines:
            if line.startswith("["):
                begin = line.index("[") + len("[")
                end = line.index("]")
                name = line[begin:end].strip()
                
                """ Fix [options] """
                if name != "options":
                    next_line = conf_file_lines[i+1]
                    
                    if next_line.startswith(""):
            			serverUrl = conf_file_lines[i+1].replace(SERVER_INDIFICATOR, "")
            			repositaries.append(repository(name, serverUrl))
                
            i+=1
            
        return repositaries
