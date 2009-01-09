#!/usr/bin/env python

# gpacman is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# gpacman is copyright (C)2008 by Andre Makar

import gtk, gtk.glade
import pango
import gobject

from gpacman.pacman_manager import *
from gpacman.config_manager import *
from gpacman.command_builder import *
from gpacman.models import *

from gpacman.ui.about_dialog import about_dialog
from gpacman.ui.execute_window import execute_window
from gpacman.ui.setting_window import setting_window

from os import chdir, geteuid, curdir
from os.path import exists
from pwd import getpwuid
from decorator import decorator

""" main_window """
class main_window:
    
    def __init__(self):

        # Glade
        cfg_manager = config_manager()
        glade_xml = gtk.glade.XML(DATA_DIR+"/"+cfg_manager.config_parser.get("General", "glade_file"), "main_window")
        
        self.window = glade_xml.get_widget("main_window")
        
        events_dict = {
            "on_repositaries_tree_cursor_changed": self.on_repositaries_tree_cursor_changed,
            "on_close_menuitem_activate": self.on_close_menuitem_activate,
            "on_about_menuitem_activate": self.on_about_menuitem_activate,
            "on_main_window_hide": self.on_main_window_hide,
            "on_refresh_button_clicked": self.on_refresh_button_clicked,
            "on_update_button_clicked": self.on_update_button_clicked,
            "on_packages_tree_cursor_changed": self.on_packages_tree_cursor_changed,
            "on_find_button_clicked": self.on_find_button_clicked,
            "on_setting_menuitem_activate": self.on_setting_menuitem_activate,
            "on_remove_to_actions_button_clicked": self.on_remove_to_actions_button_clicked,
            "on_clear_execute_button_clicked": self.on_clear_execute_button_clicked,
            "on_execute_toolbutton_clicked": self.on_execute_toolbutton_clicked }
        glade_xml.signal_autoconnect(events_dict)
        
        #Get elements
        self._package_tree = glade_xml.get_widget("packages_tree")
        self._actions_tree = glade_xml.get_widget("actions_tree")
        self._repositaries_tree = glade_xml.get_widget("repositaries_tree")
        self._execute_button = glade_xml.get_widget("execute_button")
        self._description_text = glade_xml.get_widget("description_text")
        self._find_entry = glade_xml.get_widget("find_entry")
        self._remove_to_actions_button = glade_xml.get_widget("remove_to_actions_button")
        self._actions_execute_button = glade_xml.get_widget("actions_execute_button")
        self._clear_execute_button = glade_xml.get_widget("clear_execute_button")
        self._execute_toolbutton = glade_xml.get_widget("execute_toolbutton")
        
        #Packages manager
        self._packages_manager = pacman_manager()
        
        #Setup secondary gui elements
        self._init_repositaries_tree()
        self._init_package_tree()
        self._init_actions_tree()
        
        self._about_dialog = about_dialog()
        self._execute_window = execute_window(self)
        self._setting_window = setting_window()
        
        #Builder
        self._command_builder = command_builder()
        
        #Models
        self._package_tree.set_model(packagers_store(self._packages_manager.get_all_packages()))
        self._repositaries_tree.set_model(repositaries_store(self._packages_manager.get_repositaries()))
        self._repositaries_tree.get_model().append(["all"])
        
    """ _init_package_tree """  
    def _init_package_tree(self):
        
        # Installed
        cell = gtk.CellRendererToggle()
        
        cell.set_property('activatable', True)
        cell.connect('toggled', self.on_package_tree_toggled)
        
        column = gtk.TreeViewColumn("", cell )
		
        column.set_clickable(True)
        column.add_attribute(cell, "active", 0)
        column.set_reorderable(True)
        column.set_sort_column_id(0)

        self._package_tree.append_column(column)
        
        # Name
        cell = gtk.CellRendererText()
        
        name_column = gtk.TreeViewColumn("Name", cell, markup=1)
        
        #name_column.set_cell_data_func(cell, self.on_packages_tree_cell_funcion)
        name_column.set_resizable(True)
        name_column.set_reorderable(True)
        name_column.set_clickable(True)
        name_column.set_sort_column_id(1)
        
        self._package_tree.append_column(name_column)
        
        # Version
        cell = gtk.CellRendererText()
        
        version_column = gtk.TreeViewColumn("Version", cell, markup=2)
         
        #version_column.set_cell_data_funon_window_delete_eventc(cell, self.on_packages_tree_cell_funcion)
        version_column.set_resizable(True)
        version_column.set_reorderable(True)
        version_column.set_clickable(True)
        version_column.set_sort_column_id(2)
        
        self._package_tree.append_column(version_column)
        
        # Repositaries
        cell = gtk.CellRendererText()
            
        repositaries_column = gtk.TreeViewColumn("Repositaries", cell, markup=3)
            
        #repositaries_column.set_cell_data_func(cell, self.on_packages_tree_cell_funcion)
        repositaries_column.set_resizable(True)
        repositaries_column.set_reorderable(True)
        repositaries_column.set_clickable(True)
        repositaries_column.set_sort_column_id(3)
            
        self._package_tree.append_column(repositaries_column)
        
    """ _init_actions_tree """  
    def _init_actions_tree(self):
        
        # Type
        cell = gtk.CellRendererText()
        
        type_column = gtk.TreeViewColumn("Type", cell, text=0)
        
        #name_column.set_cell_data_func(cell, self.on_packages_tree_cell_funcion)
        type_column.set_resizable(True)
        type_column.set_reorderable(True)
        type_column.set_clickable(True)
        type_column.set_sort_column_id(1)
        
        self._actions_tree.append_column(type_column)
        
        # Name
        cell = gtk.CellRendererText()
        
        name_column = gtk.TreeViewColumn("Name", cell, text=1)
         
        #version_column.set_cell_data_func(cell, self.on_packages_tree_cell_funcion)
        name_column.set_resizable(True)
        name_column.set_reorderable(True)
        name_column.set_clickable(True)
        name_column.set_sort_column_id(2)
        
        self._actions_tree.append_column(name_column)
        
    """ _init_repositaries_tree """
    def _init_repositaries_tree(self):

        # Name
        cell = gtk.CellRendererText()
        
        name_column = gtk.TreeViewColumn("Name", cell, text=0)
         
        #version_column.set_cell_data_func(cell, self.on_packages_tree_cell_funcion)
        name_column.set_resizable(True)
        name_column.set_reorderable(True)
        name_column.set_clickable(True)
        name_column.set_sort_column_id(2)
        
        self._repositaries_tree.append_column(name_column)
        
    """ update_packages_tree """
    def update_packages_tree(self):
        self._packages_manager.refresh()
        self._package_tree.set_model(packagers_store(self._packages_manager.get_all_packages()))
        self._package_tree.set_model(packagers_store(self._packages_manager.get_all_packages()))
        
    """ update_packages_tree """
    def clear_actions_store(self):
        self._actions_tree.set_model(actions_store())
        
    """ --- EVENTS --- """
    
    """ on_repositaries_tree_cursor_changed """
    def on_repositaries_tree_cursor_changed(self, treeview):
        path, focus = treeview.get_cursor()
        iter = treeview.get_model().get_iter(path)
        selected_repositary_name = treeview.get_model().get_value(iter, 0)
        
        if selected_repositary_name == "all":
            selected_packages = self._packages_manager.get_all_packages()
        else:
            selected_packages = self._packages_manager.get_packages_by_repositary_name(selected_repositary_name)
            
        self._package_tree.set_model(packagers_store(selected_packages))
        
        self._find_entry.set_text("")
        
    """ on_packages_tree_cell_funcion """
    def on_packages_tree_cell_funcion(self, column, cell, model, iter):
        installed = model.get_value(iter, 1)
            
    """ on_main_window_hide """
    def on_main_window_hide(self, widget, data=None):
        if constants.TRAY == False:
            gtk.main_quit()
        else:
            self.window.iconify()
        
    """ on_close_menuitem_activate """
    def on_close_menuitem_activate(self, widget, data=None):
        gtk.main_quit()
        
    """ on_setting_menuitem_activate """
    def on_setting_menuitem_activate(self, widget, data=None):
		self._setting_window.show()
       
    """ on_execute_toolbutton_clicked """
    def on_execute_toolbutton_clicked(self, widget, data=None):
        self._execute_window = execute_window(self)
        self._execute_window.set_flag(1)
    
        self._execute_window.show()
        self._execute_window.execute(self._command_builder.build_action_commands(self._actions_tree.get_model()))
        
    """ on_refresh_button_clicked """
    def on_refresh_button_clicked(self, widget, data=None):
        self._execute_window = execute_window(self)
        self._execute_window.set_flag(0)
        
        self._execute_window.show()
        self._execute_window.execute(self._command_builder.build_refresh_commands())
        
    """ on_packages_tree_cursor_changed """
    def on_packages_tree_cursor_changed(self, treeview):
        path, focus = treeview.get_cursor()
        iter = treeview.get_model().get_iter(path)
        name_package = decorator.unbold(treeview.get_model().get_value(iter, 1))
        package = self._packages_manager.get_package_by_name(name_package)
        
        if package <> None:
            description = package.get_description()
        
        if description <> None:
            self._description_text.get_buffer().set_text(description)
        
    """ on_update_button_clicked """
    def on_update_button_clicked(self, widget, data=None):
        self._execute_window = execute_window(self)
        self._execute_window.set_flag(0)
    
        self._execute_window.show()
        self._execute_window.execute(self._command_builder.build_update_commands())
        
    """ on_find_button_clicked """
    def on_find_button_clicked(self, widget, data=None):
        find_text = self._find_entry.get_text()
        packages = self._packages_manager.get_packages_by_name_pattern(find_text)
        
        self._package_tree.set_model(packagers_store(packages))
        
    """ on_remove_to_actions_button_clicked """
    def on_remove_to_actions_button_clicked(self, widget, data=None):
        path, focus = self._actions_tree.get_cursor()
        
        if path <> None:
            iter = self._actions_tree.get_model().get_iter(path)
            
            actions_model = self._actions_tree.get_model()
            action_item_name = actions_model.get_value(iter, 1)
            
            package_model = self._package_tree.get_model()
            iter_model = package_model.get_iter_first()
            
            self._actions_tree.get_model().remove(iter)
        
            while iter_model <> None:
                item_current_state = package_model.get_value(iter_model, 0)
                item_prevosion_state = package_model.get_value(iter_model, 4)
                item_name = decorator.unbold(package_model.get_value(iter_model, 1))
                
                if item_name == action_item_name:
                    if item_current_state <> item_prevosion_state:
                        package_model.set_value(iter_model,0 , not package_model.get_value(iter_model, 0))
                        
                        for i in range(0, package_model.get_n_columns()):
                            package_path = package_model.get_path(iter_model)
                            package_model[package_path][i] = decorator.unbold(package_model[package_path][i])
                    
                iter_model = package_model.iter_next(iter_model)
            
            if  actions_model.count() < 1:
                self._remove_to_actions_button.set_sensitive(False)
                self._clear_execute_button.set_sensitive(False)
                self._execute_toolbutton.set_sensitive(False)
            
    """ on_clear_execute_button_clicked """
    def on_clear_execute_button_clicked(self, widget, data=None):
        
        package_model = self._package_tree.get_model()
        iter_package = package_model.get_iter_first()
            
        while iter_package <> None:
            item_current_state = package_model.get_value(iter_package, 0)
            item_prevosion_state = package_model.get_value(iter_package, 4)
            item_name = decorator.unbold(package_model.get_value(iter_package, 1))
            
            if item_current_state <> item_prevosion_state:
                package_model.set_value(iter_package,0 , not package_model.get_value(iter_package, 0))
                        
                for i in range(0, package_model.get_n_columns()):
                    package_path = package_model.get_path(iter_package)
                    package_model[package_path][i] = decorator.unbold(package_model[package_path][i])
                    
            iter_package = package_model.iter_next(iter_package)
        
        actions_model = self._actions_tree.set_model(actions_store())
        
        self._remove_to_actions_button.set_sensitive(False)
        self._clear_execute_button.set_sensitive(False)
        self._execute_toolbutton.set_sensitive(False)
        self._execute_toolbutton.set_sensitive(False)
        
    """ on_about_menuitem_activate """
    def on_about_menuitem_activate(self, widget, data=None):
        self._about_dialog = about_dialog()
        
        result = self._about_dialog.about_window.run()
        if result == -6:
            self._about_dialog.about_window.destroy()
            
    """ on_package_tree_toggled """
    def on_package_tree_toggled(self, cell, path):
        
        #Get values
        package_model = self._package_tree.get_model()
        actions_model = self._actions_tree.get_model()
        
        cfg_manager = config_manager()
        package_model[path][0] = not package_model[path][0]
        add = True
        state = cfg_manager.config_parser.get("General", "remove_string")
        
        action_store = actions_store()
        
        #Set model
        if actions_model <> None:
            action_store = actions_model
        
        if package_model[path][0] == True:
            state = cfg_manager.config_parser.get("General", "install_string")
        
        if action_store.isset([state, package_model[path][1].replace("<b>","").replace("</b>","")]) == True:
           add = False
           action_store.remove_by_name(package_model[path][1].replace("<b>","").replace("</b>",""))
            
        if add == True:
            action_store.append([state, package_model[path][1].replace("<b>","").replace("</b>","")])
        
        if package_model[path][0] <> package_model[path][4]:
            for i in range(0, package_model.get_n_columns()):
                package_model[path][i] = decorator.bold(package_model[path][i])
        else:
            for i in range(0, package_model.get_n_columns()):
                package_model[path][i] = decorator.unbold(package_model[path][i])

        self._actions_tree.set_model(action_store)
        actions_model = self._actions_tree.get_model()
            
        if actions_model <> None:
            if actions_model.count() > 0:
                self._remove_to_actions_button.set_sensitive(True)
                self._clear_execute_button.set_sensitive(True)
                self._execute_toolbutton.set_sensitive(True)
            else:
                self._remove_to_actions_button.set_sensitive(False)
                self._clear_execute_button.set_sensitive(False)
                self._execute_toolbutton.set_sensitive(False)
        
