#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os
import subprocess

from Config import Config
from Performance import Performance
from Memory import Memory


# Define class
class MemoryMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MemoryMenus.ui")

        # Get GUI objects
        self.popover1201p = builder.get_object('popover1201p')
        self.button1201p = builder.get_object('button1201p')
        self.button1203p = builder.get_object('button1203p')
        self.combobox1201p = builder.get_object('combobox1201p')
        self.radiobutton1201p = builder.get_object('radiobutton1201p')
        self.radiobutton1202p = builder.get_object('radiobutton1202p')
        self.radiobutton1203p = builder.get_object('radiobutton1203p')
        self.radiobutton1204p = builder.get_object('radiobutton1204p')
        self.colorchooserdialog1201 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1201p.connect("show", self.on_popover1201p_show)
        self.button1201p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1203p.connect("clicked", self.on_button1203p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def memory_tab_customization_popover_connect_signals_func(self):

        self.radiobutton1201p.connect("toggled", self.on_radiobutton1201p_toggled)
        self.radiobutton1202p.connect("toggled", self.on_radiobutton1202p_toggled)
        self.radiobutton1203p.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.radiobutton1204p.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.combobox1201p.connect("changed", self.on_combobox1201p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def memory_tab_customization_popover_disconnect_signals_func(self):

        self.radiobutton1201p.disconnect_by_func(self.on_radiobutton1201p_toggled)
        self.radiobutton1202p.disconnect_by_func(self.on_radiobutton1202p_toggled)
        self.radiobutton1203p.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.radiobutton1204p.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.combobox1201p.disconnect_by_func(self.on_combobox1201p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1201p_show(self, widget):

        try:
            self.memory_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.memory_tab_popover_set_gui()
        self.memory_tab_customization_popover_connect_signals_func()


    # ----------------------- "RAM" Radiobutton -----------------------
    def on_radiobutton1201p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_memory_usage_per_memory = 0

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    # ----------------------- "Memory" Radiobutton -----------------------
    def on_radiobutton1202p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_memory_usage_per_memory = 1

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    # ----------------------- "Precision" Combobox -----------------------
    def on_combobox1201p_changed(self, widget):

        Config.performance_memory_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    # ----------------------- "Show units as powers of: 1024 or 1000" Radiobuttons -----------------------
    def on_data_unit_radiobuttons_toggled(self, widget):

        if self.radiobutton1203p.get_active() == True:
            Config.performance_memory_data_unit = 0
        elif self.radiobutton1204p.get_active() == True:
            Config.performance_memory_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    # ----------------------- "Graph Color" Button -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1201p:
            red, blue, green, alpha = Config.chart_line_color_memory_percent
        self.colorchooserdialog1201.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1201.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1201.get_rgba()
            if widget == self.button1201p:
                Config.chart_line_color_memory_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1201.hide()

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1203p_clicked(self, widget):

        # Load default settings
        Config.config_default_performance_memory_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        self.memory_tab_customization_popover_disconnect_signals_func()
        self.memory_tab_popover_set_gui()
        self.memory_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def memory_tab_popover_set_gui(self):

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_memory_usage_per_memory == 0:
            self.radiobutton1201p.set_active(True)
        if Config.show_memory_usage_per_memory == 1:
            self.radiobutton1202p.set_active(True)

        # Set data unit checkboxes.
        if Config.performance_memory_data_unit == 0:
            self.radiobutton1203p.set_active(True)
        if Config.performance_memory_data_unit == 1:
            self.radiobutton1204p.set_active(True)

        # Add Memory usage data precision data into combobox
        liststore1201p = Gtk.ListStore()
        liststore1201p.set_column_types([str, int])
        self.combobox1201p.set_model(liststore1201p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1201p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1201p.pack_start(renderer_text, True)
        self.combobox1201p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1201p.append([data[1], data[2]])
        self.combobox1201p.set_active(Config.performance_memory_data_precision)


# Generate object
MemoryMenu = MemoryMenu()

