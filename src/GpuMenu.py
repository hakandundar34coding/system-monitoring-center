#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk

from locale import gettext as _tr

from Config import Config
from Gpu import Gpu
from MainWindow import MainWindow
import Common


class GpuMenu:

    def __init__(self):

        self.menu_gui()


    def menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.menu_po = Gtk.Popover()

        # Grid (main)
        main_grid = Common.menu_main_grid()
        self.menu_po.set_child(main_grid)

        # Label - menu title (GPU)
        label = Common.menu_title_label(_tr("GPU"))
        main_grid.attach(label, 0, 0, 2, 1)

        # Button (Graph Color)
        self.graph_color_button = Common.graph_color_button()
        main_grid.attach(self.graph_color_button, 0, 4, 2, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 5, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 14, 2, 1)

        # Connect signals
        self.reset_button.connect("clicked", self.on_reset_button_clicked)


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        Config.config_default_performance_gpu_func()
        Config.config_save_func()
        Gpu.gpu_set_selected_gpu_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        Gpu.gpu_initial_func()
        Gpu.gpu_loop_func()


GpuMenu = GpuMenu()

