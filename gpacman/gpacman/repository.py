#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

""" repository """
class repository:
    
    def __init__(self, name, serverURL=""):

        self.name = name
        self.serverURL = serverURL