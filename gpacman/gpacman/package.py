#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import os, re, time
from config_manager import *

""" package """
class package:
    
    def __init__(self, name,  version, inst_ver=None, repo=None, inst=True,isold=False):

        self.name = name
        self.version = version
        self.repo = repo
        self.installed = inst
        
        if inst_ver:
            self.inst_ver = inst_ver
        elif inst:
            self.inst_ver = version
        else:
            self.inst_ver = "-"
        self.isold = isold
        
        self.filelist = ""
        self.isorphan = None
        self.req_by = ""
        self.dependencies = ""
        self.conflict = None
        self.prop_setted = False
        
        self.dates = [None, None]
        
        self.explicitly = ["", None]
        
        self.flag = None
        self.size = ""
        self.url = ""
    
    """ get_description """
    def get_description(self):
    
        desc = self._get_description_line_by_package("desc")
    
        try:
            begin = desc.index("%DESC%") + len("%DESC%")
            end = desc.index("%", begin)
            description = unicode(desc[begin:end].strip(), errors="ignore")
            
            return description
        except Exception:
            pass
        return ''
    
    """ _get_description_line_by_package """
    def _get_description_line_by_package(self, line):
    
        cfg_manager = config_manager()
        name_n_ver = self.name + '-' + self.version
        
        if self.installed == False:
            path = "%s/sync/%s/%s/%s" %(cfg_manager.config_parser.get("General", "path_to_pacman_lib"), self.repo, name_n_ver, line)
        else:
            path = cfg_manager.config_parser.get("General", "path_to_pacman_lib")+"local"+'/%s/%s' %(name_n_ver, line)
        
        try:
            raw_file = open(path).read()
        except IOError, msg:
            return
            
        return raw_file
    
""" package_bulder """
class package_bilder:
    
    """ create_package """
    @staticmethod
    def create_package_by_string(package_string, repositary, installed_packages):

        name_n_ver = package_string.split("-", package_string.count("-")-1)
        ver = name_n_ver.pop()
        name = "-".join(name_n_ver)
        installed = False
        
        if name in installed_packages:
            installed = True
           
        pac_obj = package(name, ver, "", repositary, installed, "")
        
        return pac_obj
    