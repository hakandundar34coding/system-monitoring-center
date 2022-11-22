#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from Cpu import Cpu
from MainWindow import MainWindow


class CpuMenu:

    def __init__(self):

        self.menu_gui()


    def menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.menu_po = Gtk.Popover()

        # Grid (main)
        menu_main_grid = Gtk.Grid()
        menu_main_grid.set_row_spacing(5)
        menu_main_grid.set_margin_top(5)
        menu_main_grid.set_margin_bottom(5)
        menu_main_grid.set_margin_start(5)
        menu_main_grid.set_margin_end(5)
        self.menu_po.set_child(menu_main_grid)

        # Bold label atributes
        attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        attribute_list_bold.insert(attribute)

        # Label - menu title (CPU)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("CPU"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        menu_main_grid.attach(label, 0, 0, 1, 1)

        # Label (Graph - Show)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("Graph - Show"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 1, 1, 1)

        # CheckButton (CPU Usage (Average))
        self.cpu_usage_average_cb = Gtk.CheckButton()
        self.cpu_usage_average_cb.set_group(None)
        self.cpu_usage_average_cb.set_label(_tr("CPU Usage (Average)"))
        self.cpu_usage_average_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.cpu_usage_average_cb, 0, 2, 1, 1)

        # CheckButton (CPU Usage (Per Core))
        self.cpu_usage_per_core_cb = Gtk.CheckButton()
        self.cpu_usage_per_core_cb.set_group(self.cpu_usage_average_cb)
        self.cpu_usage_per_core_cb.set_label(_tr("CPU Usage (Per Core)"))
        self.cpu_usage_per_core_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.cpu_usage_per_core_cb, 0, 3, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 4, 1, 1)

        # Button (Graph Color)
        self.graph_color_button = Gtk.Button()
        self.graph_color_button.set_label(_tr("Graph Color"))
        menu_main_grid.attach(self.graph_color_button, 0, 5, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 6, 1, 1)

        # Label - title (Precision)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("Precision"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 7, 1, 1)

        # Label - precision (CPU)
        label = Gtk.Label()
        label.set_label(_tr("CPU"))
        label.set_halign(Gtk.Align.CENTER)
        menu_main_grid.attach(label, 0, 8, 1, 1)

        # ComboBox - precision (CPU)
        self.cpu_precision_cmb = Gtk.ComboBox()
        menu_main_grid.attach(self.cpu_precision_cmb, 0, 9, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 10, 1, 1)

        # Button (Reset)
        self.reset_button = Gtk.Button()
        self.reset_button.set_label(_tr("Reset"))
        self.reset_button.set_halign(Gtk.Align.CENTER)
        menu_main_grid.attach(self.reset_button, 0, 11, 1, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Gtk.ColorChooserDialog().new(title=None, parent=MainWindow.main_window)
        self.colorchooserdialog.set_transient_for(MainWindow.main_window)

        # Connect signals
        self.menu_po.connect("show", self.on_menu_po_show)
        self.graph_color_button.connect("clicked", self.on_graph_color_button_clicked)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.cpu_usage_average_cb.connect("toggled", self.on_cpu_usage_cb_toggled)
        self.cpu_usage_per_core_cb.connect("toggled", self.on_cpu_usage_cb_toggled)
        self.cpu_precision_cmb.connect("changed", self.on_cpu_precision_cmb_changed)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.cpu_usage_average_cb.disconnect_by_func(self.on_cpu_usage_cb_toggled)
        self.cpu_usage_per_core_cb.disconnect_by_func(self.on_cpu_usage_cb_toggled)
        self.cpu_precision_cmb.disconnect_by_func(self.on_cpu_precision_cmb_changed)


    def on_menu_po_show(self, widget):
        """
        Run code when menu is shown.
        """

        try:
            self.disconnect_signals()
        except TypeError:
            pass
        self.popover_set_gui()
        self.connect_signals()


    def on_cpu_usage_cb_toggled(self, widget):
        """
        Change CPU usage type.
        """

        if widget.get_active() == True:
            if widget == self.cpu_usage_average_cb:
                Config.show_cpu_usage_per_core = 0
            if widget == self.cpu_usage_per_core_cb:
                Config.show_cpu_usage_per_core = 1

            # Apply changes immediately (without waiting update interval).
            Cpu.cpu_initial_func()
            Cpu.cpu_loop_func()
            Config.config_save_func()


    def on_graph_color_button_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_cpu_percent
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
            Config.chart_line_color_cpu_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog.hide()

        # Apply changes immediately (without waiting update interval).
        Cpu.cpu_initial_func()
        Cpu.cpu_loop_func()
        Config.config_save_func()


    def on_cpu_precision_cmb_changed(self, widget):
        """
        Change CPU usage percent precision.
        """

        Config.performance_cpu_usage_percent_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Cpu.cpu_initial_func()
        Cpu.cpu_loop_func()
        Config.config_save_func()


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_cpu_func()
        Config.config_save_func()
        Performance.performance_set_selected_cpu_core_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        Cpu.cpu_initial_func()
        Cpu.cpu_loop_func()
        self.disconnect_signals()
        self.popover_set_gui()
        self.connect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Select checkbutton appropriate for CPU usage chart setting
        if Config.show_cpu_usage_per_core == 0:
            self.cpu_usage_average_cb.set_active(True)
        if Config.show_cpu_usage_per_core == 1:
            self.cpu_usage_per_core_cb.set_active(True)

        # Add CPU usage percent data to combobox
        liststore = Gtk.ListStore()
        liststore.set_column_types([str, int])
        self.cpu_precision_cmb.set_model(liststore)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.cpu_precision_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.cpu_precision_cmb.pack_start(renderer_text, True)
        self.cpu_precision_cmb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore.append([data[1], data[2]])
        self.cpu_precision_cmb.set_active(Config.performance_cpu_usage_percent_precision)


CpuMenu = CpuMenu()

