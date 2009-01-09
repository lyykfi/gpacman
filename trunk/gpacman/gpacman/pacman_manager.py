#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import os, re
import urllib

from package import package, package_bilder
from repository import repository
from config_manager import config_manager

"""packages_manager"""
class pacman_manager():
    
    """ Init """
    def __init__(self):
        self._packages = []
        self._installed_packages = self.get_installed_packages() 
        self._repositaries = []
        self._pacman_config_parser = pacman_config_parser()
        
        self.refresh()
        
    """ check_update """
    def check_update(self, repositoryrepositories):
        for repository in repositories:
            
            db_flag  = False
            
            try:
                db_file = urllib.urlretrieve(repository.serverURL+"/"+repository.name+ '.db.tar.gz')
                db_flag = True
            except IOError:
                db_flag = False
            
            if db_flag == True:
                repo_db = tarfile.open(db_file, 'r:gz')
                
        urllib.urlcleanup()
        
    """Grab all pacs from machine db, instatiate a package obj for each of them and order them by cols"""
    def _bind_all_packages(self):
        self._packages = []
        
        for repositary in self._repositaries:
            
            package_name_list = self.get_from_repositary_package_name_list(repositary.name)
            
            if package_name_list != None:
                for package_name in package_name_list:
                    new_package = package_bilder.create_package_by_string(package_name, 
                                                                          repositary.name, 
                                                                          self._installed_packages)
                    self._packages.append(new_package)
        
    """ get_installed_packages """
    def get_installed_packages(self):
        
        cfg_manager = config_manager()
        installed_packages = []
        installed = os.listdir(cfg_manager.config_parser.get("General", "path_to_pacman_lib")+"local")
        
        for package_full_name in installed:
            name_n_ver = package_full_name.split("-", package_full_name.count("-")-1)
            ver = name_n_ver.pop()
            
            name = ""
            for part in name_n_ver:
                if name:
                    name = "-".join((name, part))
                else:
                    name = part
                    
            installed_packages.append(name)
            
        return installed_packages
    
    """ get_from_repositary_package_name_list """
    def get_from_repositary_package_name_list(self, repository_name):

        package_list = None
        cfg_manager = config_manager()
        
        try:
            package_list = os.listdir("%s/%s" %(cfg_manager.config_parser.get("General", "path_to_pacman_lib")+"sync", repository_name))
        except OSError:
            return False
        try:
            package_list.remove(".lastupdate")
        except ValueError:
            pass
        #try:
            #date_file = open("%s/%s/.lastupdate" %(PATH_TO_PACMAN_SYNC, repository_name), 'r')
        #except IOError:
            #package_list.sort()
            #return package_list
        
        #date = int( date_file.readline() )
        #date_file.close()

        package_list.sort()
        return package_list
    
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

""" pacman_config_parser """
class pacman_config_parser:
    
    def parse(self):
        repositaries = []
        
        cfg_manager = config_manager()
        conf_file = file(cfg_manager.config_parser.get("General", "path_conf_file"), "r").read()
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
                        cfg_manager = config_manager()
                        serverUrl = conf_file_lines[i+1].replace(cfg_manager.config_parser.get("General", "server_indificator"), "")
                        repositaries.append(repository(name, serverUrl))
                
            i+=1
            
        return repositaries