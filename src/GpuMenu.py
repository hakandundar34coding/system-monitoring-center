#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

from locale import gettext as _tr

from Config import Config
from Gpu import Gpu
from MainWindow import MainWindow


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
        main_grid = Gtk.Grid()
        main_grid.set_row_spacing(3)
        main_grid.set_margin_top(3)
        main_grid.set_margin_bottom(3)
        main_grid.set_margin_start(3)
        main_grid.set_margin_end(3)
        self.menu_po.set_child(main_grid)

        # Bold label atributes
        attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        attribute_list_bold.insert(attribute)

        # Label - menu title (GPU)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("GPU"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        main_grid.attach(label, 0, 0, 2, 1)

        # Button (Graph Color)
        self.graph_color_button = Gtk.Button()
        self.graph_color_button.set_label(_tr("Graph Color"))
        main_grid.attach(self.graph_color_button, 0, 4, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 5, 2, 1)

        # Button (Reset)
        self.reset_button = Gtk.Button()
        self.reset_button.set_label(_tr("Reset"))
        self.reset_button.set_halign(Gtk.Align.CENTER)
        main_grid.attach(self.reset_button, 0, 14, 2, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Gtk.ColorChooserDialog().new(title=None, parent=MainWindow.main_window)
        self.colorchooserdialog.set_transient_for(MainWindow.main_window)

        # Connect signals
        self.graph_color_button.connect("clicked", self.on_graph_color_button_clicked)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def on_graph_color_button_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_fps
        self.colorchooserdialog.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        self.menu_po.popdown()
        self.colorchooserdialog.present()


    def on_colorchooserdialog_response(self, widget, response):
        """
        Get selected color, apply it to graph and save it.
        Dialog have to be hidden for "Cancel" response.
        """

        if response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog.get_rgba()
            Config.chart_line_color_fps = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog.hide()

        # Apply changes immediately (without waiting update interval).
        Gpu.gpu_initial_func()
        Gpu.gpu_loop_func()
        Config.config_save_func()


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

