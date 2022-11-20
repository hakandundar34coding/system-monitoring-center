#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from Disk import Disk
from MainWindow import MainWindow


class DiskMenu:

    def __init__(self):

        # Menu GUI
        self.disk_menu_gui()


    def disk_menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.disk_menu_po = Gtk.Popover()

        # Main grid
        menu_main_grid = Gtk.Grid()
        menu_main_grid.set_row_spacing(5)
        menu_main_grid.set_margin_top(5)
        menu_main_grid.set_margin_bottom(5)
        menu_main_grid.set_margin_start(5)
        menu_main_grid.set_margin_end(5)
        self.disk_menu_po.set_child(menu_main_grid)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Menu title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Disk"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        menu_main_grid.attach(label, 0, 0, 2, 1)

        # Label (Chart - Show)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Graph - Show"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 1, 2, 1)

        # Checkbutton (Read Speed)
        self.disk_menu_read_speed_cb = Gtk.CheckButton()
        self.disk_menu_read_speed_cb.set_label(_tr("Read Speed"))
        self.disk_menu_read_speed_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_read_speed_cb, 0, 2, 1, 1)

        # Checkbutton (Write Speed)
        self.disk_menu_write_speed_cb = Gtk.CheckButton()
        self.disk_menu_write_speed_cb.set_label(_tr("Write Speed"))
        self.disk_menu_write_speed_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_write_speed_cb, 1, 2, 1, 1)

        # Checkbutton (Selected Device)
        self.disk_menu_selected_device_cb = Gtk.CheckButton()
        self.disk_menu_selected_device_cb.set_group(None)
        self.disk_menu_selected_device_cb.set_label(_tr("Selected Device"))
        self.disk_menu_selected_device_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_selected_device_cb, 0, 3, 1, 1)

        # Checkbutton (All Devices)
        self.disk_menu_all_devices_cb = Gtk.CheckButton()
        self.disk_menu_all_devices_cb.set_group(self.disk_menu_selected_device_cb)
        self.disk_menu_all_devices_cb.set_label(_tr("All Devices"))
        self.disk_menu_all_devices_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_all_devices_cb, 1, 3, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 4, 2, 1)

        # Button (Graph Color)
        self.disk_menu_graph_color_button = Gtk.Button()
        self.disk_menu_graph_color_button.set_label(_tr("Graph Color"))
        menu_main_grid.attach(self.disk_menu_graph_color_button, 0, 5, 2, 1)

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

        # ComboBox for precision (Disk)
        self.disk_menu_disk_precision_cb = Gtk.ComboBox()
        menu_main_grid.attach(self.disk_menu_disk_precision_cb, 0, 8, 2, 1)

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
        self.disk_menu_data_power_of_1024_cb = Gtk.CheckButton()
        self.disk_menu_data_power_of_1024_cb.set_group(None)
        self.disk_menu_data_power_of_1024_cb.set_label("1024")
        self.disk_menu_data_power_of_1024_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_data_power_of_1024_cb, 0, 12, 1, 1)

        # Checkbutton (1000)
        self.disk_menu_data_power_of_1000_cb = Gtk.CheckButton()
        self.disk_menu_data_power_of_1000_cb.set_group(self.disk_menu_data_power_of_1024_cb)
        self.disk_menu_data_power_of_1000_cb.set_label("1000")
        self.disk_menu_data_power_of_1000_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_data_power_of_1000_cb, 1, 12, 1, 1)

        # Checkbutton (Show speed units as multiples of bits)
        self.disk_menu_data_bits_cb = Gtk.CheckButton()
        self.disk_menu_data_bits_cb.set_group(None)
        self.disk_menu_data_bits_cb.set_label(_tr("Show speed units as multiples of bits"))
        self.disk_menu_data_bits_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_data_bits_cb, 0, 13, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 14, 2, 1)

        # Label (Disk)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Disk"))
        label.set_halign(Gtk.Align.START)
        menu_main_grid.attach(label, 0, 15, 2, 1)

        # Checkbutton (Hide loop, ramdisk, zram disks)
        self.disk_menu_hide_loop_ramdisk_zram_disks_cb = Gtk.CheckButton()
        self.disk_menu_hide_loop_ramdisk_zram_disks_cb.set_group(None)
        self.disk_menu_hide_loop_ramdisk_zram_disks_cb.set_label(_tr("Hide loop, ramdisk, zram disks"))
        self.disk_menu_hide_loop_ramdisk_zram_disks_cb.set_halign(Gtk.Align.START)
        menu_main_grid.attach(self.disk_menu_hide_loop_ramdisk_zram_disks_cb, 0, 16, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        menu_main_grid.attach(separator, 0, 17, 2, 1)

        # Button (Reset)
        self.disk_menu_reset_button = Gtk.Button()
        self.disk_menu_reset_button.set_label(_tr("Reset"))
        self.disk_menu_reset_button.set_halign(Gtk.Align.CENTER)
        menu_main_grid.attach(self.disk_menu_reset_button, 0, 18, 2, 1)

        # ColorChooserDialog
        self.colorchooserdialog = Gtk.ColorChooserDialog().new(title=None, parent=MainWindow.main_window)
        self.colorchooserdialog.set_transient_for(MainWindow.main_window)

        # Connect signals
        self.disk_menu_po.connect("show", self.on_disk_menu_po_show)
        self.disk_menu_graph_color_button.connect("clicked", self.on_chart_color_buttons_clicked)
        self.disk_menu_reset_button.connect("clicked", self.on_disk_menu_reset_button_clicked)
        self.colorchooserdialog.connect("response", self.on_colorchooserdialog_response)


    def customization_popover_connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.disk_menu_read_speed_cb.connect("toggled", self.on_disk_menu_read_speed_cb_toggled)
        self.disk_menu_write_speed_cb.connect("toggled", self.on_disk_menu_write_speed_cb_toggled)
        self.disk_menu_selected_device_cb.connect("toggled", self.on_disk_menu_device_selection_cb)
        self.disk_menu_all_devices_cb.connect("toggled", self.on_disk_menu_device_selection_cb)
        self.disk_menu_data_power_of_1024_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.disk_menu_data_power_of_1000_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.disk_menu_data_bits_cb.connect("toggled", self.on_disk_menu_data_bits_cb_toggled)
        self.disk_menu_hide_loop_ramdisk_zram_disks_cb.connect("toggled", self.on_disk_menu_hide_loop_ramdisk_zram_disks_cb_toggled)

        self.disk_menu_disk_precision_cb.connect("changed", self.on_disk_menu_disk_precision_cb_changed)


    def customization_popover_disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.disk_menu_read_speed_cb.disconnect_by_func(self.on_disk_menu_read_speed_cb_toggled)
        self.disk_menu_write_speed_cb.disconnect_by_func(self.on_disk_menu_write_speed_cb_toggled)
        self.disk_menu_selected_device_cb.disconnect_by_func(self.on_disk_menu_device_selection_cb)
        self.disk_menu_all_devices_cb.disconnect_by_func(self.on_disk_menu_device_selection_cb)
        self.disk_menu_data_power_of_1024_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.disk_menu_data_power_of_1000_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.disk_menu_data_bits_cb.disconnect_by_func(self.on_disk_menu_data_bits_cb_toggled)
        self.disk_menu_hide_loop_ramdisk_zram_disks_cb.disconnect_by_func(self.on_disk_menu_hide_loop_ramdisk_zram_disks_cb_toggled)
        self.disk_menu_disk_precision_cb.disconnect_by_func(self.on_disk_menu_disk_precision_cb_changed)


    def on_disk_menu_po_show(self, widget):
        """
        Run code when menu is shown.
        """

        try:
            self.customization_popover_disconnect_signals()
        except TypeError:
            pass
        self.popover_set_gui()
        self.customization_popover_connect_signals()


    def on_disk_menu_read_speed_cb_toggled(self, widget):
        """
        Show/Hide disk read speed line.
        """

        if widget.get_active() == True:
            Config.plot_disk_read_speed = 1
        if widget.get_active() == False:
            if self.disk_menu_write_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_read_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_disk_menu_write_speed_cb_toggled(self, widget):
        """
        Show/Hide disk write speed line.
        """

        if widget.get_active() == True:
            Config.plot_disk_write_speed = 1
        if widget.get_active() == False:
            if self.disk_menu_read_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_write_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_disk_menu_device_selection_cb(self, widget):
        """
        Set device selection (Selected/All) for showing speed data.
        """

        if widget.get_active() == True:
            if widget == self.disk_menu_selected_device_cb:
                Config.show_disk_usage_per_disk = 0
            if widget == self.disk_menu_all_devices_cb:
                Config.show_disk_usage_per_disk = 1

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_disk_menu_disk_precision_cb_changed(self, widget):
        """
        Change disk speed precision.
        """

        Config.performance_disk_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_data_unit_radiobuttons_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection.
        """

        if self.disk_menu_data_power_of_1024_cb.get_active() == True:
            Config.performance_disk_data_unit = 0
        elif self.disk_menu_data_power_of_1000_cb.get_active() == True:
            Config.performance_disk_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_disk_menu_data_bits_cb_toggled(self, widget):
        """
        Show speed units as multiples of bits/bytes.
        """

        if widget.get_active() == True:
            Config.performance_disk_speed_bit = 1
        else:
            Config.performance_disk_speed_bit = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_chart_color_buttons_clicked(self, widget):
        """
        Change graph foreground color.
        """

        # Get current foreground color of the graph and set it as selected color of the dialog when dialog is shown.
        red, blue, green, alpha = Config.chart_line_color_disk_speed_usage
        self.colorchooserdialog.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        self.colorchooserdialog.present()


    def on_colorchooserdialog_response(self, widget, response):
        """
        Get selected color, apply it to graph and save it.
        Dialog have to be hidden for "Cancel" response.
        """

        if response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog.get_rgba()
            Config.chart_line_color_disk_speed_usage = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog.hide()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_disk_menu_hide_loop_ramdisk_zram_disks_cb_toggled(self, widget):
        """
        Show/Hide loop, ramdisk, zram disks.
        """

        if widget.get_active() == True:
            Config.hide_loop_ramdisk_zram_disks = 1
        else:
            Config.hide_loop_ramdisk_zram_disks = 0

        # Reset selected device in order to update selected disk on disk list between Performance tab sub-tabs for avoiding no disk selection or wrong disk selection situation if selected disk is hidden or new disks are shown after the option is changed.
        Config.selected_disk = ""
        Performance.performance_set_selected_disk_func()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_disk_menu_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_disk_func()
        Config.config_save_func()
        Performance.performance_set_selected_disk_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        self.customization_popover_connect_signals()
        self.popover_set_gui()
        self.customization_popover_disconnect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Set active checkbuttons if disk read speed/disk write speed values are "1".
        if Config.plot_disk_read_speed == 1:
            self.disk_menu_read_speed_cb.set_active(True)
        if Config.plot_disk_read_speed == 0:
            self.disk_menu_read_speed_cb.set_active(False)
        if Config.plot_disk_write_speed == 1:
            self.disk_menu_write_speed_cb.set_active(True)
        if Config.plot_disk_write_speed == 0:
            self.disk_menu_write_speed_cb.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_disk_usage_per_disk == 0:
            self.disk_menu_selected_device_cb.set_active(True)
        if Config.show_disk_usage_per_disk == 1:
            self.disk_menu_all_devices_cb.set_active(True)

        # Set data unit checkbuttons and radiobuttons.
        if Config.performance_disk_data_unit == 0:
            self.disk_menu_data_power_of_1024_cb.set_active(True)
        if Config.performance_disk_data_unit == 1:
            self.disk_menu_data_power_of_1000_cb.set_active(True)
        if Config.performance_disk_speed_bit == 1:
            self.disk_menu_data_bits_cb.set_active(True)
        if Config.performance_disk_speed_bit == 0:
            self.disk_menu_data_bits_cb.set_active(False)

        # Set active checkbutton if "Hide loop, ramdisk, zram disks" option is enabled.
        if Config.hide_loop_ramdisk_zram_disks == 1:
            self.disk_menu_hide_loop_ramdisk_zram_disks_cb.set_active(True)
        if Config.hide_loop_ramdisk_zram_disks == 0:
            self.disk_menu_hide_loop_ramdisk_zram_disks_cb.set_active(False)

        # Add Disk data precision data into combobox.
        disk_menu_disk_precision_ls = Gtk.ListStore()
        disk_menu_disk_precision_ls.set_column_types([str, int])
        self.disk_menu_disk_precision_cb.set_model(disk_menu_disk_precision_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.disk_menu_disk_precision_cb.clear()
        renderer_text = Gtk.CellRendererText()
        self.disk_menu_disk_precision_cb.pack_start(renderer_text, True)
        self.disk_menu_disk_precision_cb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            disk_menu_disk_precision_ls.append([data[1], data[2]])
        self.disk_menu_disk_precision_cb.set_active(Config.performance_disk_data_precision)


DiskMenu = DiskMenu()

