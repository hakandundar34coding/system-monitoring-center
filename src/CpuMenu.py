#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

from Config import Config
from Performance import Performance
from Cpu import Cpu
from MainGUI import MainGUI


# Define class
class CpuMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/CpuMenus.ui")

        # Get GUI objects
        self.popover1101p = builder.get_object('popover1101p')
        self.radiobutton1101p = builder.get_object('radiobutton1101p')
        self.radiobutton1102p = builder.get_object('radiobutton1102p')
        self.button1101p = builder.get_object('button1101p')
        self.button1103p = builder.get_object('button1103p')
        self.combobox1101p = builder.get_object('combobox1101p')
        self.colorchooserdialog1101 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1101p.connect("show", self.on_popover1101p_show)
        self.button1101p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1103p.connect("clicked", self.on_button1103p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def cpu_tab_customization_popover_connect_signals_func(self):

        self.radiobutton1101p.connect("toggled", self.on_radiobutton1101p_toggled)
        self.radiobutton1102p.connect("toggled", self.on_radiobutton1102p_toggled)
        self.combobox1101p.connect("changed", self.on_combobox1101p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def cpu_tab_customization_popover_disconnect_signals_func(self):

        self.radiobutton1101p.disconnect_by_func(self.on_radiobutton1101p_toggled)
        self.radiobutton1102p.disconnect_by_func(self.on_radiobutton1102p_toggled)
        self.combobox1101p.disconnect_by_func(self.on_combobox1101p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1101p_show(self, widget):
 
        try:
            self.cpu_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.cpu_tab_popover_set_gui()
        self.cpu_tab_customization_popover_connect_signals_func()


    # ----------------------- "average CPU usage" Radiobutton -----------------------
    def on_radiobutton1101p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_cpu_usage_per_core = 0

            # Apply changes immediately (without waiting update interval).
            Cpu.cpu_initial_func()
            Cpu.cpu_loop_func()
            Config.config_save_func()


    # ----------------------- "CPU usage per core" Radiobutton -----------------------
    def on_radiobutton1102p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_cpu_usage_per_core = 1

            # Apply changes immediately (without waiting update interval).
            Cpu.cpu_initial_func()
            Cpu.cpu_loop_func()
            Config.config_save_func()


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1101p:
            red, blue, green, alpha = Config.chart_line_color_cpu_percent
        self.colorchooserdialog1101.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1101.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1101.get_rgba()
            if widget == self.button1101p:
                Config.chart_line_color_cpu_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1101.hide()

        # Apply changes immediately (without waiting update interval).
        Cpu.cpu_initial_func()
        Cpu.cpu_loop_func()
        Config.config_save_func()


    # ----------------------- "CPU usage percent precision" Combobox -----------------------
    def on_combobox1101p_changed(self, widget):

        Config.performance_cpu_usage_percent_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Cpu.cpu_initial_func()
        Cpu.cpu_loop_func()
        Config.config_save_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1103p_clicked(self, widget):

        # Load default settings
        Config.config_default_performance_cpu_func()
        Config.config_save_func()
        Performance.performance_set_selected_cpu_core_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainGUI.main_gui_device_selection_list_func()

        # Apply changes immediately (without waiting update interval).
        Cpu.cpu_initial_func()
        Cpu.cpu_loop_func()
        self.cpu_tab_customization_popover_disconnect_signals_func()
        self.cpu_tab_popover_set_gui()
        self.cpu_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def cpu_tab_popover_set_gui(self):

        # Select radiobutton appropriate for CPU usage chart setting
        if Config.show_cpu_usage_per_core == 0:
            self.radiobutton1101p.set_active(True)
        if Config.show_cpu_usage_per_core == 1:
            self.radiobutton1102p.set_active(True)

        # Add CPU usage percent data into combobox
        liststore1101p = Gtk.ListStore()
        liststore1101p.set_column_types([str, int])
        self.combobox1101p.set_model(liststore1101p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1101p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1101p.pack_start(renderer_text, True)
        self.combobox1101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1101p.append([data[1], data[2]])
        self.combobox1101p.set_active(Config.performance_cpu_usage_percent_precision)


# Generate object
CpuMenu = CpuMenu()

