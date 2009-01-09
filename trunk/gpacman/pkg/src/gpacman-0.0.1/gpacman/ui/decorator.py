#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gobject

""" decorator """
class decorator:
    
    @staticmethod
    def bold(text):
        if type(text) is str:
            return "<b>"+text+"</b>"
        else:
            return text
    
    @staticmethod
    def unbold(text):
        if type(text) is str:
            return text.replace("<b>","").replace("</b>","")
        else:
            return text
