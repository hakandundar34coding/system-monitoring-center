#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

from Config import Config
from Gpu import Gpu
from MainGUI import MainGUI


class GpuMenu:

    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuMenus.ui")

        # Get GUI objects
        self.popover1501p = builder.get_object('popover1501p')
        self.button1501p = builder.get_object('button1501p')
        self.button1503p = builder.get_object('button1503p')

        self.colorchooserdialog1501 = Gtk.ColorChooserDialog(parent=MainGUI.window1)

        self.colorchooserdialog1501.set_modal(True)

        # Connect GUI signals
        self.button1501p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1503p.connect("clicked", self.on_button1503p_clicked)


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Hide the customizations menu
        self.popover1501p.popdown()

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_fps
        self.colorchooserdialog1501.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1501.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1501.get_rgba()
            if widget == self.button1501p:
                Config.chart_line_color_fps = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

            # Apply changes immediately (without waiting update interval).
            Gpu.gpu_initial_func()
            Gpu.gpu_loop_func()
            Config.config_save_func()

        self.colorchooserdialog1501.hide()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1503p_clicked(self, widget):

        Config.config_default_performance_gpu_func()
        Config.config_save_func()
        Gpu.gpu_set_selected_gpu_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainGUI.main_gui_device_selection_list_func()

        # Apply changes immediately (without waiting update interval).
        Gpu.gpu_initial_func()
        Gpu.gpu_loop_func()


GpuMenu = GpuMenu()

