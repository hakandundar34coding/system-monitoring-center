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

        # Menu GUI
        self.network_menu_gui()


    def network_menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.network_menu_po = Gtk.Popover()

        # Main grid
        menu_main_grid = Gtk.Grid()
        menu_main_grid.set_row_spacing(5)
        menu_main_grid.set_margin_top(5)
        menu_main_grid.set_margin_bottom(5)
        menu_main_grid.set_margin_start(5)
        menu_main_grid.set_margin_end(5)
        self.network_menu_po.set_child(menu_main_grid)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Menu title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Network"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        menu_main_grid.attach(label, 0, 0, 2, 1)

        # Label (Chart - Show)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Graph - Show"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 1, 2, 1)

        # Checkbutton (Download Speed)
        self.network_menu_download_speed_cb = Gtk.CheckButton()
        self.network_menu_download_speed_cb.set_label(_tr("Download Speed"))
        self.network_menu_download_speed_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_download_speed_cb, 0, 2, 1, 1)

        # Checkbutton (Upload Speed)
        self.network_menu_upload_speed_cb = Gtk.CheckButton()
        self.network_menu_upload_speed_cb.set_label(_tr("Upload Speed"))
        self.network_menu_upload_speed_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_upload_speed_cb, 1, 2, 1, 1)

        # Checkbutton (Selected Device)
        self.network_menu_selected_device_cb = Gtk.CheckButton()
        self.network_menu_selected_device_cb.set_group(None)
        self.network_menu_selected_device_cb.set_label(_tr("Selected Device"))
        self.network_menu_selected_device_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_selected_device_cb, 0, 3, 1, 1)

        # Checkbutton (All Devices)
        self.network_menu_all_devices_cb = Gtk.CheckButton()
        self.network_menu_all_devices_cb.set_group(self.network_menu_selected_device_cb)
        self.network_menu_all_devices_cb.set_label(_tr("All Devices"))
        self.network_menu_all_devices_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_all_devices_cb, 1, 3, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 4, 2, 1)

        # Button (Graph Color)
        self.network_menu_graph_color_button = Gtk.Button()
        self.network_menu_graph_color_button.set_label(_tr("Graph Color"))
        menu_main_grid.attach(self.network_menu_graph_color_button, 0, 5, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 6, 2, 1)

        # Label for precision (Precision)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Precision"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 7, 2, 1)

        # ComboBox for precision (Network)
        self.network_menu_network_precision_cb = Gtk.ComboBox()
        menu_main_grid.attach(self.network_menu_network_precision_cb, 0, 8, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 9, 2, 1)

        # Label for precision (Data Unit)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Data Unit"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 10, 2, 1)

        # Label for data unit (Show data as powers of:)
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 11, 2, 1)

        # Checkbutton (1024)
        self.network_menu_data_power_of_1024_cb = Gtk.CheckButton()
        self.network_menu_data_power_of_1024_cb.set_group(None)
        self.network_menu_data_power_of_1024_cb.set_label("1024")
        self.network_menu_data_power_of_1024_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_data_power_of_1024_cb, 0, 12, 1, 1)

        # Checkbutton (1000)
        self.network_menu_data_power_of_1000_cb = Gtk.CheckButton()
        self.network_menu_data_power_of_1000_cb.set_group(self.network_menu_data_power_of_1024_cb)
        self.network_menu_data_power_of_1000_cb.set_label("1000")
        self.network_menu_data_power_of_1000_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_data_power_of_1000_cb, 1, 12, 1, 1)

        # Checkbutton (Show speed units as multiples of bits)
        self.network_menu_data_bits_cb = Gtk.CheckButton()
        self.network_menu_data_bits_cb.set_group(None)
        self.network_menu_data_bits_cb.set_label(_tr("Show speed units as multiples of bits"))
        self.network_menu_data_bits_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.network_menu_data_bits_cb, 0, 13, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 14, 2, 1)

        # Button (Reset)
        self.network_menu_reset_button = Gtk.Button()
        self.network_menu_reset_button.set_label(_tr("Reset"))
        self.network_menu_reset_button.set_halign(Gtk.Align.CENTER)
        menu_main_grid.attach(self.network_menu_reset_button, 0, 18, 2, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Gtk.ColorChooserDialog().new(title=None, parent=MainWindow.main_window)
        self.colorchooserdialog.set_transient_for(MainWindow.main_window)

        # Connect signals
        self.network_menu_po.connect("show", self.on_network_menu_po_show)
        self.network_menu_graph_color_button.connect("clicked", self.on_chart_color_buttons_clicked)
        self.network_menu_reset_button.connect("clicked", self.on_network_menu_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def customization_popover_connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.network_menu_download_speed_cb.connect("toggled", self.on_network_menu_download_speed_cb_toggled)
        self.network_menu_upload_speed_cb.connect("toggled", self.on_network_menu_upload_speed_cb_toggled)
        self.network_menu_selected_device_cb.connect("toggled", self.on_network_menu_device_selection_cb)
        self.network_menu_all_devices_cb.connect("toggled", self.on_network_menu_device_selection_cb)
        self.network_menu_data_power_of_1024_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.network_menu_data_power_of_1000_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.network_menu_data_bits_cb.connect("toggled", self.on_network_menu_data_bits_cb_toggled)
        self.network_menu_network_precision_cb.connect("changed", self.on_network_menu_network_precision_cb_changed)


    def customization_popover_disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.network_menu_download_speed_cb.disconnect_by_func(self.on_network_menu_download_speed_cb_toggled)
        self.network_menu_upload_speed_cb.disconnect_by_func(self.on_network_menu_upload_speed_cb_toggled)
        self.network_menu_selected_device_cb.disconnect_by_func(self.on_network_menu_device_selection_cb)
        self.network_menu_all_devices_cb.disconnect_by_func(self.on_network_menu_device_selection_cb)
        self.network_menu_data_power_of_1024_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.network_menu_data_power_of_1000_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.network_menu_data_bits_cb.disconnect_by_func(self.on_network_menu_data_bits_cb_toggled)
        self.network_menu_network_precision_cb.disconnect_by_func(self.on_network_menu_network_precision_cb_changed)


    def on_network_menu_po_show(self, widget):
        """
        Run code when menu is shown.
        """

        try:
            self.customization_popover_disconnect_signals()
        except TypeError:
            pass
        self.popover_set_gui()
        self.customization_popover_connect_signals()


    def on_network_menu_download_speed_cb_toggled(self, widget):
        """
        Show/Hide network read speed line.
        """

        if widget.get_active() == True:
            Config.plot_network_download_speed = 1
        if widget.get_active() == False:
            if self.network_menu_upload_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_download_speed = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_network_menu_upload_speed_cb_toggled(self, widget):
        """
        Show/Hide network write speed line.
        """

        if widget.get_active() == True:
            Config.plot_network_upload_speed = 1
        if widget.get_active() == False:
            if self.network_menu_download_speed_cb.get_active() == False:
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
            if widget == self.network_menu_selected_device_cb:
                Config.show_network_usage_per_network_card = 0
            if widget == self.network_menu_all_devices_cb:
                Config.show_network_usage_per_network_card = 1

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_network_menu_network_precision_cb_changed(self, widget):
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

        if self.network_menu_data_power_of_1024_cb.get_active() == True:
            Config.performance_network_data_unit = 0
        elif self.network_menu_data_power_of_1000_cb.get_active() == True:
            Config.performance_network_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    def on_network_menu_data_bits_cb_toggled(self, widget):
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


    def on_chart_color_buttons_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_network_speed_data
        self.colorchooserdialog.set_rgba(Gdk.RGBA(red, blue, green, alpha))

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


    def on_network_menu_reset_button_clicked(self, widget):
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
        self.customization_popover_connect_signals()
        self.popover_set_gui()
        self.customization_popover_disconnect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Set active checkbuttons if network download speed/network upload speed values are "1"
        if Config.plot_network_download_speed == 1:
            self.network_menu_download_speed_cb.set_active(True)
        if Config.plot_network_download_speed == 0:
            self.network_menu_download_speed_cb.set_active(False)
        if Config.plot_network_upload_speed == 1:
            self.network_menu_upload_speed_cb.set_active(True)
        if Config.plot_network_upload_speed == 0:
            self.network_menu_upload_speed_cb.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_network_usage_per_network_card == 0:
            self.network_menu_selected_device_cb.set_active(True)
        if Config.show_network_usage_per_network_card == 1:
            self.network_menu_all_devices_cb.set_active(True)

        # Set data unit radiobuttons and checkbuttons.
        if Config.performance_network_data_unit == 0:
            self.network_menu_data_power_of_1024_cb.set_active(True)
        if Config.performance_network_data_unit == 1:
            self.network_menu_data_power_of_1000_cb.set_active(True)
        if Config.performance_network_speed_bit == 1:
            self.network_menu_data_bits_cb.set_active(True)
        if Config.performance_network_speed_bit == 0:
            self.network_menu_data_bits_cb.set_active(False)

        # Add Network data precision data into combobox
        network_menu_network_precision_ls = Gtk.ListStore()
        network_menu_network_precision_ls.set_column_types([str, int])
        self.network_menu_network_precision_cb.set_model(network_menu_network_precision_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.network_menu_network_precision_cb.clear()
        renderer_text = Gtk.CellRendererText()
        self.network_menu_network_precision_cb.pack_start(renderer_text, True)
        self.network_menu_network_precision_cb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            network_menu_network_precision_ls.append([data[1], data[2]])
        self.network_menu_network_precision_cb.set_active(Config.performance_network_data_precision)


NetworkMenu = NetworkMenu()

