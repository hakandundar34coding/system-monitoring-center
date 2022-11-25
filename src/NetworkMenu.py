#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from Network import Network
from MainWindow import MainWindow


class NetworkMenu:

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
        main_grid.set_row_spacing(2)
        main_grid.set_margin_top(2)
        main_grid.set_margin_bottom(2)
        main_grid.set_margin_start(2)
        main_grid.set_margin_end(2)
        self.menu_po.set_child(main_grid)

        # Bold label atributes
        attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        attribute_list_bold.insert(attribute)

        # Label - menu title (Network)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("Network"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        main_grid.attach(label, 0, 0, 2, 1)

        # Label (Graph - Show)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("Graph - Show"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 1, 2, 1)

        # CheckButton (Download Speed)
        self.download_speed_cb = Gtk.CheckButton()
        self.download_speed_cb.set_label(_tr("Download Speed"))
        self.download_speed_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.download_speed_cb, 0, 2, 1, 1)

        # CheckButton (Upload Speed)
        self.upload_speed_cb = Gtk.CheckButton()
        self.upload_speed_cb.set_label(_tr("Upload Speed"))
        self.upload_speed_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.upload_speed_cb, 1, 2, 1, 1)

        # CheckButton (Selected Device)
        self.selected_device_cb = Gtk.CheckButton()
        self.selected_device_cb.set_group(None)
        self.selected_device_cb.set_label(_tr("Selected Device"))
        self.selected_device_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.selected_device_cb, 0, 3, 1, 1)

        # CheckButton (All Devices)
        self.all_devices_cb = Gtk.CheckButton()
        self.all_devices_cb.set_group(self.selected_device_cb)
        self.all_devices_cb.set_label(_tr("All Devices"))
        self.all_devices_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.all_devices_cb, 1, 3, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 4, 2, 1)

        # Button (Graph Color)
        self.graph_color_button = Gtk.Button()
        self.graph_color_button.set_label(_tr("Graph Color"))
        main_grid.attach(self.graph_color_button, 0, 5, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 6, 2, 1)

        # Label - title (Precision)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("Precision"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 7, 2, 1)

        # ComboBox - precision (Network)
        self.network_precision_cmb = Gtk.ComboBox()
        main_grid.attach(self.network_precision_cmb, 0, 8, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 9, 2, 1)

        # Label - title (Data Unit)
        label = Gtk.Label()
        label.set_attributes(attribute_list_bold)
        label.set_label(_tr("Data Unit"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 10, 2, 1)

        # Label (Show data as powers of:)
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 11, 2, 1)

        # CheckButton (1024)
        self.data_power_of_1024_cb = Gtk.CheckButton()
        self.data_power_of_1024_cb.set_group(None)
        self.data_power_of_1024_cb.set_label("1024")
        self.data_power_of_1024_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.data_power_of_1024_cb, 0, 12, 1, 1)

        # CheckButton (1000)
        self.data_power_of_1000_cb = Gtk.CheckButton()
        self.data_power_of_1000_cb.set_group(self.data_power_of_1024_cb)
        self.data_power_of_1000_cb.set_label("1000")
        self.data_power_of_1000_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.data_power_of_1000_cb, 1, 12, 1, 1)

        # CheckButton (Show speed units as multiples of bits)
        self.data_bits_cb = Gtk.CheckButton()
        self.data_bits_cb.set_group(None)
        self.data_bits_cb.set_label(_tr("Show speed units as multiples of bits"))
        self.data_bits_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.data_bits_cb, 0, 13, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 14, 2, 1)

        # Button (Reset)
        self.reset_button = Gtk.Button()
        self.reset_button.set_label(_tr("Reset"))
        self.reset_button.set_halign(Gtk.Align.CENTER)
        main_grid.attach(self.reset_button, 0, 18, 2, 1)

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

        self.download_speed_cb.connect("toggled", self.on_download_speed_cb_toggled)
        self.upload_speed_cb.connect("toggled", self.on_upload_speed_cb_toggled)
        self.selected_device_cb.connect("toggled", self.on_network_menu_device_selection_cb)
        self.all_devices_cb.connect("toggled", self.on_network_menu_device_selection_cb)
        self.data_power_of_1024_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.data_power_of_1000_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.data_bits_cb.connect("toggled", self.on_data_bits_cb_toggled)
        self.network_precision_cmb.connect("changed", self.on_network_precision_cmb_changed)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.download_speed_cb.disconnect_by_func(self.on_download_speed_cb_toggled)
        self.upload_speed_cb.disconnect_by_func(self.on_upload_speed_cb_toggled)
        self.selected_device_cb.disconnect_by_func(self.on_network_menu_device_selection_cb)
        self.all_devices_cb.disconnect_by_func(self.on_network_menu_device_selection_cb)
        self.data_power_of_1024_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.data_power_of_1000_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.data_bits_cb.disconnect_by_func(self.on_data_bits_cb_toggled)
        self.network_precision_cmb.disconnect_by_func(self.on_network_precision_cmb_changed)


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


    def on_download_speed_cb_toggled(self, widget):
        """
        Show/Hide network read speed line.
        """

        if widget.get_active() == True:
            Config.plot_network_download_speed = 1
        if widget.get_active() == False:
            if self.upload_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_download_speed = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_upload_speed_cb_toggled(self, widget):
        """
        Show/Hide network write speed line.
        """

        if widget.get_active() == True:
            Config.plot_network_upload_speed = 1
        if widget.get_active() == False:
            if self.download_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_upload_speed = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_network_menu_device_selection_cb(self, widget):
        """
        Set device selection (Selected/All) for showing speed data.
        """

        if widget.get_active() == True:
            if widget == self.selected_device_cb:
                Config.show_network_usage_per_network_card = 0
            if widget == self.all_devices_cb:
                Config.show_network_usage_per_network_card = 1

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_network_precision_cmb_changed(self, widget):
        """
        Change network speed precision.
        """

        Config.performance_network_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_data_unit_radiobuttons_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection.
        """

        if self.data_power_of_1024_cb.get_active() == True:
            Config.performance_network_data_unit = 0
        elif self.data_power_of_1000_cb.get_active() == True:
            Config.performance_network_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_data_bits_cb_toggled(self, widget):
        """
        Show speed units as multiples of bits/bytes.
        """

        if widget.get_active() == True:
            Config.performance_network_speed_bit = 1
        else:
            Config.performance_network_speed_bit = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_graph_color_button_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_network_speed_data
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
            Config.chart_line_color_network_speed_data = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog.hide()

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_network_func()
        Config.config_save_func()
        Performance.performance_set_selected_network_card_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        self.connect_signals()
        self.popover_set_gui()
        self.disconnect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Set active checkbuttons if network download speed/network upload speed values are "1"
        if Config.plot_network_download_speed == 1:
            self.download_speed_cb.set_active(True)
        if Config.plot_network_download_speed == 0:
            self.download_speed_cb.set_active(False)
        if Config.plot_network_upload_speed == 1:
            self.upload_speed_cb.set_active(True)
        if Config.plot_network_upload_speed == 0:
            self.upload_speed_cb.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_network_usage_per_network_card == 0:
            self.selected_device_cb.set_active(True)
        if Config.show_network_usage_per_network_card == 1:
            self.all_devices_cb.set_active(True)

        # Set data unit radiobuttons and checkbuttons.
        if Config.performance_network_data_unit == 0:
            self.data_power_of_1024_cb.set_active(True)
        if Config.performance_network_data_unit == 1:
            self.data_power_of_1000_cb.set_active(True)
        if Config.performance_network_speed_bit == 1:
            self.data_bits_cb.set_active(True)
        if Config.performance_network_speed_bit == 0:
            self.data_bits_cb.set_active(False)

        # Add Network data precision data to combobox
        liststore = Gtk.ListStore()
        liststore.set_column_types([str, int])
        self.network_precision_cmb.set_model(liststore)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.network_precision_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.network_precision_cmb.pack_start(renderer_text, True)
        self.network_precision_cmb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore.append([data[1], data[2]])
        self.network_precision_cmb.set_active(Config.performance_network_data_precision)


NetworkMenu = NetworkMenu()

