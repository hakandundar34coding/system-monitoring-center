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

        # Menu GUI
        self.gpu_menu_gui()


    def gpu_menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.gpu_menu_po = Gtk.Popover()

        # Main grid
        menu_main_grid = Gtk.Grid()
        menu_main_grid.set_row_spacing(5)
        menu_main_grid.set_margin_top(5)
        menu_main_grid.set_margin_bottom(5)
        menu_main_grid.set_margin_start(5)
        menu_main_grid.set_margin_end(5)
        self.gpu_menu_po.set_child(menu_main_grid)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Menu title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("GPU"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        menu_main_grid.attach(label, 0, 0, 2, 1)

        # Button (Graph Color)
        self.gpu_menu_graph_color_button = Gtk.Button()
        self.gpu_menu_graph_color_button.set_label(_tr("Graph Color"))
        menu_main_grid.attach(self.gpu_menu_graph_color_button, 0, 4, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 5, 2, 1)

        # Button (Reset)
        self.gpu_menu_reset_button = Gtk.Button()
        self.gpu_menu_reset_button.set_label(_tr("Reset"))
        self.gpu_menu_reset_button.set_halign(Gtk.Align.CENTER)
        menu_main_grid.attach(self.gpu_menu_reset_button, 0, 14, 2, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Gtk.ColorChooserDialog().new(title=None, parent=MainWindow.main_window)
        self.colorchooserdialog.set_transient_for(MainWindow.main_window)

        # Connect signals
        self.gpu_menu_graph_color_button.connect("clicked", self.on_chart_color_buttons_clicked)
        self.gpu_menu_reset_button.connect("clicked", self.on_gpu_menu_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def on_chart_color_buttons_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_fps
        self.colorchooserdialog.set_rgba(Gdk.RGBA(red, blue, green, alpha))

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


    def on_gpu_menu_reset_button_clicked(self, widget):
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

