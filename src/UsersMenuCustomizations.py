#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Config import Config
#from Users import Users
import Users


# Define class
class UsersMenuCustomizations:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenuCustomizations.ui")

        # Get GUI objects
        self.popover3101p = builder.get_object('popover3101p')
        self.button3101p = builder.get_object('button3101p')
        self.checkbutton3101p = builder.get_object('checkbutton3101p')
        self.checkbutton3102p = builder.get_object('checkbutton3102p')
        self.checkbutton3103p = builder.get_object('checkbutton3103p')
        self.checkbutton3104p = builder.get_object('checkbutton3104p')
        self.checkbutton3105p = builder.get_object('checkbutton3105p')
        self.checkbutton3106p = builder.get_object('checkbutton3106p')
        self.checkbutton3107p = builder.get_object('checkbutton3107p')
        self.checkbutton3108p = builder.get_object('checkbutton3108p')
        self.checkbutton3109p = builder.get_object('checkbutton3109p')
        self.checkbutton3110p = builder.get_object('checkbutton3110p')
        self.checkbutton3111p = builder.get_object('checkbutton3111p')

        # Connect GUI signals
        self.popover3101p.connect("show", self.on_popover3101p_show)
        self.button3101p.connect("clicked", self.on_button3101p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def users_tab_customization_popover_connect_signals_func(self):

        self.checkbutton3101p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3102p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3103p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3104p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3105p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3106p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3107p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3108p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3109p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3110p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3111p.connect("toggled", self.on_add_remove_checkbuttons_toggled)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def users_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton3101p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3102p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3103p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3104p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3105p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3106p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3107p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3108p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3109p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3110p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton3111p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover3101p_show(self, widget):
 
        try:
            self.users_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.users_tab_popover_set_gui()
        self.users_tab_customization_popover_connect_signals_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button3101p_clicked(self, widget):

        # Load default settings
        Config.config_default_users_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Users.users_initial_func()
        Users.users_loop_func()
        self.users_tab_customization_popover_disconnect_signals_func()
        self.users_tab_popover_set_gui()
        self.users_tab_customization_popover_connect_signals_func()


    # ----------------------- "Add/Remove Columns (User Name, Full Name,, etc.)" Checkbuttons -----------------------
    def on_add_remove_checkbuttons_toggled(self, widget):

        self.users_add_remove_columns_function()


    # ----------------------- Called for setting menu GUI items -----------------------
    def users_tab_popover_set_gui(self):

        # Set GUI objects on Add/Remove Column tab
        if 0 in Config.users_treeview_columns_shown:
            self.checkbutton3101p.set_active(True)
        else:
            self.checkbutton3101p.set_active(False)
        if 1 in Config.users_treeview_columns_shown:
            self.checkbutton3102p.set_active(True)
        else:
            self.checkbutton3102p.set_active(False)
        if 2 in Config.users_treeview_columns_shown:
            self.checkbutton3103p.set_active(True)
        else:
            self.checkbutton3103p.set_active(False)
        if 3 in Config.users_treeview_columns_shown:
            self.checkbutton3104p.set_active(True)
        else:
            self.checkbutton3104p.set_active(False)
        if 4 in Config.users_treeview_columns_shown:
            self.checkbutton3105p.set_active(True)
        else:
            self.checkbutton3105p.set_active(False)
        if 5 in Config.users_treeview_columns_shown:
            self.checkbutton3106p.set_active(True)
        else:
            self.checkbutton3106p.set_active(False)
        if 6 in Config.users_treeview_columns_shown:
            self.checkbutton3107p.set_active(True)
        else:
            self.checkbutton3107p.set_active(False)
        if 7 in Config.users_treeview_columns_shown:
            self.checkbutton3108p.set_active(True)
        else:
            self.checkbutton3108p.set_active(False)
        if 8 in Config.users_treeview_columns_shown:
            self.checkbutton3109p.set_active(True)
        else:
            self.checkbutton3109p.set_active(False)
        if 9 in Config.users_treeview_columns_shown:
            self.checkbutton3110p.set_active(True)
        else:
            self.checkbutton3110p.set_active(False)
        if 10 in Config.users_treeview_columns_shown:
            self.checkbutton3111p.set_active(True)
        else:
            self.checkbutton3111p.set_active(False)


    # ----------------------- Called for adding/removing treeview columns -----------------------
    def users_add_remove_columns_function(self):

        Config.users_treeview_columns_shown = []

        if self.checkbutton3101p.get_active() == True:
            Config.users_treeview_columns_shown.append(0)
        if self.checkbutton3102p.get_active() == True:
            Config.users_treeview_columns_shown.append(1)
        if self.checkbutton3103p.get_active() == True:
            Config.users_treeview_columns_shown.append(2)
        if self.checkbutton3104p.get_active() == True:
            Config.users_treeview_columns_shown.append(3)
        if self.checkbutton3105p.get_active() == True:
            Config.users_treeview_columns_shown.append(4)
        if self.checkbutton3106p.get_active() == True:
            Config.users_treeview_columns_shown.append(5)
        if self.checkbutton3107p.get_active() == True:
            Config.users_treeview_columns_shown.append(6)
        if self.checkbutton3108p.get_active() == True:
            Config.users_treeview_columns_shown.append(7)
        if self.checkbutton3109p.get_active() == True:
            Config.users_treeview_columns_shown.append(8)
        if self.checkbutton3110p.get_active() == True:
            Config.users_treeview_columns_shown.append(9)
        if self.checkbutton3111p.get_active() == True:
            Config.users_treeview_columns_shown.append(10)

        # Apply changes immediately (without waiting update interval).
        Users.users_treeview_column_order_width_row_sorting_func()
        Users.users_initial_func()
        Users.users_loop_func()
        Config.config_save_func()


 # Generate object
UsersMenuCustomizations = UsersMenuCustomizations()

