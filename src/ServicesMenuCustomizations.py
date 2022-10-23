#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Config import Config
#from Services import Services
import Services


# Define class
class ServicesMenuCustomizations:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesMenuCustomizations.ui")

        # Get GUI objects
        self.popover6101p = builder.get_object('popover6101p')
        self.checkbutton6101p = builder.get_object('checkbutton6101p')
        self.checkbutton6102p = builder.get_object('checkbutton6102p')
        self.checkbutton6103p = builder.get_object('checkbutton6103p')
        self.checkbutton6104p = builder.get_object('checkbutton6104p')
        self.checkbutton6105p = builder.get_object('checkbutton6105p')
        self.checkbutton6106p = builder.get_object('checkbutton6106p')
        self.checkbutton6107p = builder.get_object('checkbutton6107p')
        self.checkbutton6108p = builder.get_object('checkbutton6108p')
        self.button6101p = builder.get_object('button6101p')

        # Connect GUI signals
        self.popover6101p.connect("show", self.on_popover6101p_show)
        self.button6101p.connect("clicked", self.on_button6101p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def services_tab_customization_popover_connect_signals_func(self):

        self.checkbutton6101p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6102p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6103p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6104p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6105p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6106p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6107p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6108p.connect("toggled", self.on_add_remove_checkbuttons_toggled)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def services_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton6101p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6102p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6103p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6104p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6105p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6106p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6107p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton6108p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover6101p_show(self, widget):
 
        try:
            self.services_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.services_tab_popover_set_gui()
        self.services_tab_customization_popover_connect_signals_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button6101p_clicked(self, widget):

        # Load default settings
        Config.config_default_services_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
#        Services.services_initial_func()
#        Services.services_loop_func()
        self.services_tab_customization_popover_disconnect_signals_func()
        self.services_tab_popover_set_gui()
        self.services_tab_customization_popover_connect_signals_func()


    # ----------------------- "Add/Remove Columns (Service Name, State, Main PID, etc.)" Checkbuttons -----------------------
    def on_add_remove_checkbuttons_toggled(self, widget):

        self.services_add_remove_columns_function()


    # ----------------------- Called for setting menu GUI items -----------------------
    def services_tab_popover_set_gui(self):

        if 0 in Config.services_treeview_columns_shown:
            self.checkbutton6101p.set_active(True)
        else:
            self.checkbutton6101p.set_active(False)
        if 1 in Config.services_treeview_columns_shown:
            self.checkbutton6102p.set_active(True)
        else:
            self.checkbutton6102p.set_active(False)
        if 2 in Config.services_treeview_columns_shown:
            self.checkbutton6103p.set_active(True)
        else:
            self.checkbutton6103p.set_active(False)
        if 3 in Config.services_treeview_columns_shown:
            self.checkbutton6104p.set_active(True)
        else:
            self.checkbutton6104p.set_active(False)
        if 4 in Config.services_treeview_columns_shown:
            self.checkbutton6105p.set_active(True)
        else:
            self.checkbutton6105p.set_active(False)
        if 5 in Config.services_treeview_columns_shown:
            self.checkbutton6106p.set_active(True)
        else:
            self.checkbutton6106p.set_active(False)
        if 6 in Config.services_treeview_columns_shown:
            self.checkbutton6107p.set_active(True)
        else:
            self.checkbutton6107p.set_active(False)
        if 7 in Config.services_treeview_columns_shown:
            self.checkbutton6108p.set_active(True)
        else:
            self.checkbutton6108p.set_active(False)


    # ----------------------- Called for adding/removing treeview columns -----------------------
    def services_add_remove_columns_function(self):

        Config.services_treeview_columns_shown = []

        if self.checkbutton6101p.get_active() == True:
            Config.services_treeview_columns_shown.append(0)
        if self.checkbutton6102p.get_active() == True:
            Config.services_treeview_columns_shown.append(1)
        if self.checkbutton6103p.get_active() == True:
            Config.services_treeview_columns_shown.append(2)
        if self.checkbutton6104p.get_active() == True:
            Config.services_treeview_columns_shown.append(3)
        if self.checkbutton6105p.get_active() == True:
            Config.services_treeview_columns_shown.append(4)
        if self.checkbutton6106p.get_active() == True:
            Config.services_treeview_columns_shown.append(5)
        if self.checkbutton6107p.get_active() == True:
            Config.services_treeview_columns_shown.append(6)
        if self.checkbutton6108p.get_active() == True:
            Config.services_treeview_columns_shown.append(7)

        # Apply changes immediately (without waiting update interval).
        Services.services_treeview_column_order_width_row_sorting_func()
#        Services.services_initial_func()
#        Services.services_loop_func()
        Config.config_save_func()


# Generate object
ServicesMenuCustomizations = ServicesMenuCustomizations()

