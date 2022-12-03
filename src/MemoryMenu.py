#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from Memory import Memory
from MainWindow import MainWindow
import Common


class MemoryMenu:

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

        # Label - menu title (Memory)
        label = Common.menu_title_label(_tr("Memory"))
        main_grid.attach(label, 0, 0, 2, 1)

        # Label (Graph - Show)
        label = Common.title_label(_tr("Graph - Show"))
        main_grid.attach(label, 0, 1, 2, 1)

        # CheckButton (RAM)
        self.ram_usage_cb = Gtk.CheckButton()
        self.ram_usage_cb.set_group(None)
        self.ram_usage_cb.set_label(_tr("RAM"))
        self.ram_usage_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.ram_usage_cb, 0, 2, 1, 1)

        # CheckButton (Memory)
        self.memory_usage_cb = Gtk.CheckButton()
        self.memory_usage_cb.set_group(self.ram_usage_cb)
        self.memory_usage_cb.set_label(_tr("Memory"))
        self.memory_usage_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.memory_usage_cb, 1, 2, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 3, 2, 1)

        # Button (Graph Color)
        self.graph_color_button = Gtk.Button()
        self.graph_color_button.set_label(_tr("Graph Color"))
        main_grid.attach(self.graph_color_button, 0, 4, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 5, 2, 1)

        # Label - title (Precision)
        label = Common.title_label(_tr("Precision"))
        main_grid.attach(label, 0, 6, 2, 1)

        # DropDown - precision (Memory)
        item_list = ['0', '0.0', '0.00', '0.000']
        self.memory_precision_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.memory_precision_dd, 0, 7, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 8, 2, 1)

        # Label - title (Data Unit)
        label = Common.title_label(_tr("Data Unit"))
        main_grid.attach(label, 0, 9, 2, 1)

        # Label (Show data as powers of:)
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 10, 2, 1)

        # CheckButton (1024)
        self.data_power_of_1024_cb = Gtk.CheckButton()
        self.data_power_of_1024_cb.set_group(None)
        self.data_power_of_1024_cb.set_label("1024")
        self.data_power_of_1024_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.data_power_of_1024_cb, 0, 11, 1, 1)

        # CheckButton (1000)
        self.data_power_of_1000_cb = Gtk.CheckButton()
        self.data_power_of_1000_cb.set_group(self.data_power_of_1024_cb)
        self.data_power_of_1000_cb.set_label("1000")
        self.data_power_of_1000_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.data_power_of_1000_cb, 1, 11, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 12, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 13, 2, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Common.menu_colorchooserdialog(_tr("Graph Color"), MainWindow.main_window)

        # Connect signals
        self.menu_po.connect("show", self.on_menu_po_show)
        self.graph_color_button.connect("clicked", self.on_graph_color_button_clicked)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.ram_usage_cb.connect("toggled", self.on_memory_type_cb_toggled)
        self.memory_usage_cb.connect("toggled", self.on_memory_type_cb_toggled)
        self.data_power_of_1024_cb.connect("toggled", self.on_data_power_of_cb_toggled)
        self.data_power_of_1000_cb.connect("toggled", self.on_data_power_of_cb_toggled)
        self.memory_precision_dd.connect("notify::selected-item", self.on_selected_item_notify)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.ram_usage_cb.disconnect_by_func(self.on_memory_type_cb_toggled)
        self.memory_usage_cb.disconnect_by_func(self.on_memory_type_cb_toggled)
        self.data_power_of_1024_cb.disconnect_by_func(self.on_data_power_of_cb_toggled)
        self.data_power_of_1000_cb.disconnect_by_func(self.on_data_power_of_cb_toggled)
        self.memory_precision_dd.disconnect_by_func(self.on_selected_item_notify)


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


    def on_memory_type_cb_toggled(self, widget):
        """
        Change memory type.
        """

        if widget.get_active() == True:
            if widget == self.ram_usage_cb:
                Config.show_memory_usage_per_memory = 0
            if widget == self.memory_usage_cb:
                Config.show_memory_usage_per_memory = 1

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_graph_color_button_clicked(self, widget):
        """
        Change graph foreground color.
        Also get current foreground color of the graph and set it as selected color of the dialog.
        """

        color = Gdk.RGBA()
        color.red, color.green, color.blue, color.alpha = Config.chart_line_color_memory_percent
        self.colorchooserdialog.set_rgba(color)

        self.menu_po.popdown()
        self.colorchooserdialog.present()


    def on_colorchooserdialog_response(self, widget, response):
        """
        Get selected color, apply it to graph and save it.
        Dialog have to be hidden for "Cancel" response.
        """

        if response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog.get_rgba()
            Config.chart_line_color_memory_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog.hide()

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_selected_item_notify(self, widget, parameter):
        """
        Change memory usage percent precision.
        Notify signal is sent when DropDown widget selection is changed.
        Currently GtkExpression parameter for DropDown can not be used because of PyGObject.
        """

        Config.performance_memory_data_precision = widget.get_selected()

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_data_power_of_cb_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection.
        """

        if self.data_power_of_1024_cb.get_active() == True:
            Config.performance_memory_data_unit = 0
        elif self.data_power_of_1000_cb.get_active() == True:
            Config.performance_memory_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_memory_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        self.disconnect_signals()
        self.popover_set_gui()
        self.connect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_memory_usage_per_memory == 0:
            self.ram_usage_cb.set_active(True)
        if Config.show_memory_usage_per_memory == 1:
            self.memory_usage_cb.set_active(True)

        # Set data unit checkboxes.
        if Config.performance_memory_data_unit == 0:
            self.data_power_of_1024_cb.set_active(True)
        if Config.performance_memory_data_unit == 1:
            self.data_power_of_1000_cb.set_active(True)

        self.memory_precision_dd.set_selected(Config.performance_memory_data_precision)


MemoryMenu = MemoryMenu()

