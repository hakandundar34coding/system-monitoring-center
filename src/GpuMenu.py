#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

from Config import Config
from Gpu import Gpu


# Define class
class GpuMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuMenus.ui")

        # Get GUI objects
        self.popover1501p = builder.get_object('popover1501p')
        self.button1501p = builder.get_object('button1501p')
        self.button1502p = builder.get_object('button1502p')
        self.button1503p = builder.get_object('button1503p')

        self.combobox1501p = builder.get_object('combobox1501p')
        self.colorchooserdialog1501 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1501p.connect("show", self.on_popover1501p_show)
        self.button1501p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1502p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1503p.connect("clicked", self.on_button1503p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def gpu_tab_customization_popover_connect_signals_func(self):

        self.combobox1501p.connect("changed", self.on_combobox1501p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def gpu_tab_customization_popover_disconnect_signals_func(self):

        self.combobox1501p.disconnect_by_func(self.on_combobox1501p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1501p_show(self, widget):

        try:
            self.gpu_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.gpu_tab_popover_set_gui()
        self.gpu_tab_customization_popover_connect_signals_func()


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1501p:
            red, blue, green, alpha = Config.chart_line_color_fps
        if widget == self.button1502p:
            red, blue, green, alpha = Config.chart_background_color_all_charts
        self.colorchooserdialog1501.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1501.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1501.get_rgba()
            if widget == self.button1501p:
                Config.chart_line_color_fps = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            if widget == self.button1502p:
                Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1501.hide()

        # Apply changes immediately (without waiting update interval).
        Gpu.gpu_initial_func()
        Gpu.gpu_loop_func()
        Config.config_save_func()


    # ----------------------- "Selected Device" Combobox -----------------------
    def on_combobox1501p_changed(self, widget):

        Config.selected_gpu = Gpu.gpu_list[widget.get_active()]
        Gpu.set_selected_gpu = Config.selected_gpu
        Gpu.gpu_get_gpu_list_and_boot_vga_func()

        # Apply changes immediately (without waiting update interval).
        Gpu.gpu_initial_func()
        Gpu.gpu_loop_func()
        Config.config_save_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1503p_clicked(self, widget):

        Config.config_default_performance_gpu_func()
        Config.config_save_func()
        Gpu.gpu_set_selected_gpu_func()

        # Apply changes immediately (without waiting update interval).
        Gpu.gpu_initial_func()
        Gpu.gpu_loop_func()
        self.gpu_tab_customization_popover_disconnect_signals_func()
        self.gpu_tab_popover_set_gui()
        self.gpu_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def gpu_tab_popover_set_gui(self):

        # Add GPU/graphics card list into combobox
        liststore1501p = Gtk.ListStore()
        liststore1501p.set_column_types([str])
        self.combobox1501p.set_model(liststore1501p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1501p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1501p.pack_start(renderer_text, True)
        self.combobox1501p.add_attribute(renderer_text, "text", 0)
        liststore1501p.clear()
        for gpu in Gpu.gpu_list:
            liststore1501p.append([gpu])
        self.combobox1501p.set_active(Gpu.selected_gpu_number)


# Generate object
GpuMenu = GpuMenu()

