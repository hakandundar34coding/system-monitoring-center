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
from Ram import Ram


# Define class
class RamMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RamMenus.ui")

        # Get GUI objects
        self.popover1201p = builder.get_object('popover1201p')
        self.button1201p = builder.get_object('button1201p')
        self.button1202p = builder.get_object('button1202p')
        self.button1203p = builder.get_object('button1203p')
        self.combobox1201p = builder.get_object('combobox1201p')
        self.combobox1202p = builder.get_object('combobox1202p')
        self.colorchooserdialog1201 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1201p.connect("show", self.on_popover1201p_show)
        self.button1201p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1202p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1203p.connect("clicked", self.on_button1203p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def ram_tab_customization_popover_connect_signals_func(self):

        self.combobox1201p.connect("changed", self.on_combobox1201p_changed)
        self.combobox1202p.connect("changed", self.on_combobox1202p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def ram_tab_customization_popover_disconnect_signals_func(self):

        self.combobox1201p.disconnect_by_func(self.on_combobox1201p_changed)
        self.combobox1202p.disconnect_by_func(self.on_combobox1202p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1201p_show(self, widget):

        try:
            self.ram_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.ram_tab_popover_set_gui()
        self.ram_tab_customization_popover_connect_signals_func()


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1201p:
            red, blue, green, alpha = Config.chart_line_color_ram_swap_percent
        if widget == self.button1202p:
            red, blue, green, alpha = Config.chart_background_color_all_charts
        self.colorchooserdialog1201.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1201.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1201.get_rgba()
            if widget == self.button1201p:
                Config.chart_line_color_ram_swap_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            if widget == self.button1202p:
                Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1201.hide()

        # Apply changes immediately (without waiting update interval).
        Ram.ram_initial_func()
        Ram.ram_loop_func()
        Config.config_save_func()


    # ----------------------- "RAM/Swap data number precision" Combobox -----------------------
    def on_combobox1201p_changed(self, widget):

        Config.performance_ram_swap_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Ram.ram_initial_func()
        Ram.ram_loop_func()
        Config.config_save_func()


    # ----------------------- "RAM/Swap data units" Combobox -----------------------
    def on_combobox1202p_changed(self, widget):

        Config.performance_ram_swap_data_unit = Config.data_unit_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Ram.ram_initial_func()
        Ram.ram_loop_func()
        Config.config_save_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1203p_clicked(self, widget):

        # Load default settings
        Config.config_default_performance_ram_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Ram.ram_initial_func()
        Ram.ram_loop_func()
        self.ram_tab_customization_popover_disconnect_signals_func()
        self.ram_tab_popover_set_gui()
        self.ram_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def ram_tab_popover_set_gui(self):

        # Add RAM usage data precision data into combobox
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
        self.combobox1201p.set_active(Config.performance_ram_swap_data_precision)

        # Add RAM usage data unit data into combobox
        liststore1202p = Gtk.ListStore()
        liststore1202p.set_column_types([str, int])
        self.combobox1202p.set_model(liststore1202p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1202p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1202p.pack_start(renderer_text, True)
        self.combobox1202p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore1202p.append([data[1], data[2]])
        for data_list in Config.data_unit_list:
            if data_list[2] == Config.performance_ram_swap_data_unit:      
                self.combobox1202p.set_active(data_list[0])


# Generate object
RamMenu = RamMenu()

