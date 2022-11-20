#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from Memory import Memory
from MainWindow import MainWindow


class MemoryMenu:

    def __init__(self):

        # Menu GUI
        self.memory_menu_gui()


    def memory_menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.memory_menu_po = Gtk.Popover()

        # Main grid
        menu_main_grid = Gtk.Grid()
        menu_main_grid.set_row_spacing(5)
        menu_main_grid.set_margin_top(5)
        menu_main_grid.set_margin_bottom(5)
        menu_main_grid.set_margin_start(5)
        menu_main_grid.set_margin_end(5)
        self.memory_menu_po.set_child(menu_main_grid)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Menu title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Memory"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        menu_main_grid.attach(label, 0, 0, 2, 1)

        # Label (Chart - Show)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Graph - Show"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 1, 2, 1)

        # Checkbutton (RAM)
        self.memory_menu_ram_usage_cb = Gtk.CheckButton()
        self.memory_menu_ram_usage_cb.set_group(None)
        self.memory_menu_ram_usage_cb.set_label(_tr("RAM"))
        self.memory_menu_ram_usage_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.memory_menu_ram_usage_cb, 0, 2, 1, 1)

        # Checkbutton (Memory)
        self.memory_menu_memory_usage_cb = Gtk.CheckButton()
        self.memory_menu_memory_usage_cb.set_group(self.memory_menu_ram_usage_cb)
        self.memory_menu_memory_usage_cb.set_label(_tr("Memory"))
        self.memory_menu_memory_usage_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.memory_menu_memory_usage_cb, 1, 2, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 3, 2, 1)

        # Button (Graph Color)
        self.memory_menu_graph_color_button = Gtk.Button()
        self.memory_menu_graph_color_button.set_label(_tr("Graph Color"))
        menu_main_grid.attach(self.memory_menu_graph_color_button, 0, 4, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 5, 2, 1)

        # Label for precision (Precision)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Precision"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 6, 2, 1)

        # ComboBox for precision (Memory)
        self.memory_menu_memory_precision_cb = Gtk.ComboBox()
        menu_main_grid.attach(self.memory_menu_memory_precision_cb, 0, 7, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 8, 2, 1)

        # Label for precision (Data Unit)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Data Unit"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 9, 2, 1)

        # Label for data unit (Show data as powers of:)
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 10, 2, 1)

        # Checkbutton (1024)
        self.memory_menu_data_power_of_1024_cb = Gtk.CheckButton()
        self.memory_menu_data_power_of_1024_cb.set_group(None)
        self.memory_menu_data_power_of_1024_cb.set_label("1024")
        self.memory_menu_data_power_of_1024_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.memory_menu_data_power_of_1024_cb, 0, 11, 1, 1)

        # Checkbutton (1000)
        self.memory_menu_data_power_of_1000_cb = Gtk.CheckButton()
        self.memory_menu_data_power_of_1000_cb.set_group(self.memory_menu_data_power_of_1024_cb)
        self.memory_menu_data_power_of_1000_cb.set_label("1000")
        self.memory_menu_data_power_of_1000_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.memory_menu_data_power_of_1000_cb, 1, 11, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 12, 2, 1)

        # Button (Reset)
        self.memory_menu_reset_button = Gtk.Button()
        self.memory_menu_reset_button.set_label(_tr("Reset"))
        self.memory_menu_reset_button.set_halign(Gtk.Align.CENTER)
        menu_main_grid.attach(self.memory_menu_reset_button, 0, 13, 2, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Gtk.ColorChooserDialog().new(title=None, parent=MainWindow.main_window)
        self.colorchooserdialog.set_transient_for(MainWindow.main_window)

        # Connect signals
        self.memory_menu_po.connect("show", self.on_memory_menu_po_show)
        self.memory_menu_graph_color_button.connect("clicked", self.on_chart_color_buttons_clicked)
        self.memory_menu_reset_button.connect("clicked", self.on_memory_menu_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def customization_popover_connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.memory_menu_ram_usage_cb.connect("toggled", self.on_memory_menu_memory_type_cb_toggled)
        self.memory_menu_memory_usage_cb.connect("toggled", self.on_memory_menu_memory_type_cb_toggled)
        self.memory_menu_data_power_of_1024_cb.connect("toggled", self.on_memory_menu_data_power_of_cb_toggled)
        self.memory_menu_data_power_of_1000_cb.connect("toggled", self.on_memory_menu_data_power_of_cb_toggled)
        self.memory_menu_memory_precision_cb.connect("changed", self.on_memory_menu_memory_precision_cb_changed)


    def customization_popover_disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.memory_menu_ram_usage_cb.disconnect_by_func(self.on_memory_menu_memory_type_cb_toggled)
        self.memory_menu_memory_usage_cb.disconnect_by_func(self.on_memory_menu_memory_type_cb_toggled)
        self.memory_menu_data_power_of_1024_cb.disconnect_by_func(self.on_memory_menu_data_power_of_cb_toggled)
        self.memory_menu_data_power_of_1000_cb.disconnect_by_func(self.on_memory_menu_data_power_of_cb_toggled)
        self.memory_menu_memory_precision_cb.disconnect_by_func(self.on_memory_menu_memory_precision_cb_changed)


    def on_memory_menu_po_show(self, widget):
        """
        Run code when menu is shown.
        """

        try:
            self.customization_popover_disconnect_signals()
        except TypeError:
            pass
        self.popover_set_gui()
        self.customization_popover_connect_signals()


    def on_memory_menu_memory_type_cb_toggled(self, widget):
        """
        Change memory type.
        """

        if widget.get_active() == True:
            if widget == self.memory_menu_ram_usage_cb:
                Config.show_memory_usage_per_memory = 0
            if widget == self.memory_menu_memory_usage_cb:
                Config.show_memory_usage_per_memory = 1

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_chart_color_buttons_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_memory_percent
        self.colorchooserdialog.set_rgba(Gdk.RGBA(red, blue, green, alpha))

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


    def on_memory_menu_memory_precision_cb_changed(self, widget):
        """
        Change memory precision.
        """

        Config.performance_memory_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_memory_menu_data_power_of_cb_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection.
        """

        if self.memory_menu_data_power_of_1024_cb.get_active() == True:
            Config.performance_memory_data_unit = 0
        elif self.memory_menu_data_power_of_1000_cb.get_active() == True:
            Config.performance_memory_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        Config.config_save_func()


    def on_memory_menu_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_memory_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Memory.memory_initial_func()
        Memory.memory_loop_func()
        self.customization_popover_disconnect_signals()
        self.popover_set_gui()
        self.customization_popover_connect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_memory_usage_per_memory == 0:
            self.memory_menu_ram_usage_cb.set_active(True)
        if Config.show_memory_usage_per_memory == 1:
            self.memory_menu_memory_usage_cb.set_active(True)

        # Set data unit checkboxes.
        if Config.performance_memory_data_unit == 0:
            self.memory_menu_data_power_of_1024_cb.set_active(True)
        if Config.performance_memory_data_unit == 1:
            self.memory_menu_data_power_of_1000_cb.set_active(True)

        # Add Memory usage data precision data into combobox
        memory_menu_memory_precision_ls = Gtk.ListStore()
        memory_menu_memory_precision_ls.set_column_types([str, int])
        self.memory_menu_memory_precision_cb.set_model(memory_menu_memory_precision_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.memory_menu_memory_precision_cb.clear()
        renderer_text = Gtk.CellRendererText()
        self.memory_menu_memory_precision_cb.pack_start(renderer_text, True)
        self.memory_menu_memory_precision_cb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            memory_menu_memory_precision_ls.append([data[1], data[2]])
        self.memory_menu_memory_precision_cb.set_active(Config.performance_memory_data_precision)


MemoryMenu = MemoryMenu()

