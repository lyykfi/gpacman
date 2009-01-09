#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import os, re

from package import package
from constants import *
from repository import repository
from pacman_config_parser import pacman_config_parser

"""packages_manager"""
class pacman_manager():
    global PATH_TO_PACMAN_LIB, PATH_TO_PACMAN_LOCAL
    
    """ Init """
    def __init__(self):
        self._packages = []
        self._installed_packages = self._get_installed_packages() 
        self._repositaries = []
        self._pacman_config_parser = pacman_config_parser()
        
        self.refresh()
        
    """Grab all pacs from machine db, instatiate a package obj for each of them and order them by cols"""
    def _bind_all_packages(self):
        self._packages = []
        
        for repo in self._repositaries:
            
            pacs = self._get_repo_pacs(repo.name)
            
            if pacs != None:
                for pac in pacs:
                    pac1 = self._make_pac(pac, repo.name);
                    self._packages.append(pac1)
        
    """ _get_installed_packages """
    def _get_installed_packages(self):
        
        installed_packages = {}
        installed = os.listdir(PATH_TO_PACMAN_LOCAL)
        
        for pac in installed:
            name_n_ver = pac.split("-", pac.count("-")-1)
            ver = name_n_ver.pop()
            
            name = ""
            for part in name_n_ver:
                if name:
                    name = "-".join((name, part))
                else:
                    name = part
                    
            installed_packages[name] = "gf"
            
        return installed_packages
    
    """ _get_repo_pacs """
    def _get_repo_pacs(self, repo):
        
        global path_repo
        
        pacs = None
        path_repo = path = "/var/lib/pacman/sync"
        
        try:
            pacs = os.listdir("%s/%s" %(path, repo))
        except OSError:
            return
        try:
            pacs.remove(".lastupdate")
        except ValueError:
            pass
        try:
            date_file = open("%s/%s/.lastupdate" %(path, repo), 'r')
        except IOError:
            pacs.sort()
            return pacs
        
        date = int( date_file.readline() )
        date_file.close()

        pacs.sort()
        return pacs
    
    """ _make_pac """
    def _make_pac(self, pac, repo):

        name_n_ver = pac.split("-", pac.count("-")-1)
        ver = name_n_ver.pop()
        name = "-".join(name_n_ver)
        installed = False
        
        if name in self._installed_packages:
            installed = True
           
        pac_obj = package(name, ver, "", repo, installed, "")
        
        return pac_obj
    
    def get_all_packages(self):
        return self._packages
    
    """ get_package_by_name """
    def get_package_by_name(self, name):
        for package in self._packages:
            if package.name == name:
                return package
            
    """ get_packages_by_repositary_name """
    def get_packages_by_repositary_name(self, name):
        selected_packages = []
        
        for package in self._packages:
            if package.repo == name:
                selected_packages.append(package)
        
        return selected_packages
    
    """ get_packages_by_name_pattern """
    def get_packages_by_name_pattern(self, name):
        selected_packages = []
        p = re.compile(name)
        
        for package in self._packages:
            package_name = package.name
            result = re.match(p, package_name)
            if result <> None:
                select_package = self.get_package_by_name(package_name)
                selected_packages.append(select_package)
        
        return selected_packages
    
    """ get_packages_by_name_pattern """
    def get_repositaries(self):
        return self._repositaries
    
    """ refresh """    
    def refresh(self):
        self._repositaries = self._pacman_config_parser.parse()
        self._bind_all_packages()
