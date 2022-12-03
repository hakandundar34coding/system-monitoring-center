#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from Disk import Disk
from MainWindow import MainWindow
import Common


class DiskMenu:

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

        # Label - menu title (Disk)
        label = Common.menu_title_label(_tr("Disk"))
        main_grid.attach(label, 0, 0, 2, 1)

        # Label (Graph - Show)
        label = Common.title_label(_tr("Graph - Show"))
        main_grid.attach(label, 0, 1, 2, 1)

        # Checkbutton (Read Speed)
        self.read_speed_cb = Gtk.CheckButton()
        self.read_speed_cb.set_label(_tr("Read Speed"))
        self.read_speed_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.read_speed_cb, 0, 2, 1, 1)

        # Checkbutton (Write Speed)
        self.write_speed_cb = Gtk.CheckButton()
        self.write_speed_cb.set_label(_tr("Write Speed"))
        self.write_speed_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.write_speed_cb, 1, 2, 1, 1)

        # Checkbutton (Selected Device)
        self.selected_device_cb = Gtk.CheckButton()
        self.selected_device_cb.set_group(None)
        self.selected_device_cb.set_label(_tr("Selected Device"))
        self.selected_device_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.selected_device_cb, 0, 3, 1, 1)

        # Checkbutton (All Devices)
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
        label = Common.title_label(_tr("Precision"))
        main_grid.attach(label, 0, 7, 2, 1)

        # DropDown - precision (Disk)
        item_list = ['0', '0.0', '0.00', '0.000']
        self.disk_precision_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.disk_precision_dd, 0, 8, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 9, 2, 1)

        # Label - title (Data Unit)
        label = Common.title_label(_tr("Data Unit"))
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

        # Label - title (Disk)
        label = Common.title_label(_tr("Disk"))
        main_grid.attach(label, 0, 15, 2, 1)

        # CheckButton (Hide loop, ramdisk, zram disks)
        self.hide_loop_ramdisk_zram_disks_cb = Gtk.CheckButton()
        self.hide_loop_ramdisk_zram_disks_cb.set_group(None)
        self.hide_loop_ramdisk_zram_disks_cb.set_label(_tr("Hide loop, ramdisk, zram disks"))
        self.hide_loop_ramdisk_zram_disks_cb.set_halign(Gtk.Align.START)
        main_grid.attach(self.hide_loop_ramdisk_zram_disks_cb, 0, 16, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(3)
        separator.set_margin_bottom(3)
        main_grid.attach(separator, 0, 17, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 18, 2, 1)

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

        self.read_speed_cb.connect("toggled", self.on_read_speed_cb_toggled)
        self.write_speed_cb.connect("toggled", self.on_write_speed_cb_toggled)
        self.selected_device_cb.connect("toggled", self.on_device_selection_cb)
        self.all_devices_cb.connect("toggled", self.on_device_selection_cb)
        self.data_power_of_1024_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.data_power_of_1000_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.data_bits_cb.connect("toggled", self.on_data_bits_cb_toggled)
        self.hide_loop_ramdisk_zram_disks_cb.connect("toggled", self.on_hide_loop_ramdisk_zram_disks_cb_toggled)
        self.disk_precision_dd.connect("notify::selected-item", self.on_selected_item_notify)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.read_speed_cb.disconnect_by_func(self.on_read_speed_cb_toggled)
        self.write_speed_cb.disconnect_by_func(self.on_write_speed_cb_toggled)
        self.selected_device_cb.disconnect_by_func(self.on_device_selection_cb)
        self.all_devices_cb.disconnect_by_func(self.on_device_selection_cb)
        self.data_power_of_1024_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.data_power_of_1000_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.data_bits_cb.disconnect_by_func(self.on_data_bits_cb_toggled)
        self.hide_loop_ramdisk_zram_disks_cb.disconnect_by_func(self.on_hide_loop_ramdisk_zram_disks_cb_toggled)
        self.disk_precision_dd.disconnect_by_func(self.on_selected_item_notify)


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


    def on_read_speed_cb_toggled(self, widget):
        """
        Show/Hide disk read speed line.
        """

        if widget.get_active() == True:
            Config.plot_disk_read_speed = 1
        if widget.get_active() == False:
            if self.write_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_read_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_write_speed_cb_toggled(self, widget):
        """
        Show/Hide disk write speed line.
        """

        if widget.get_active() == True:
            Config.plot_disk_write_speed = 1
        if widget.get_active() == False:
            if self.read_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_write_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_device_selection_cb(self, widget):
        """
        Set device selection (Selected/All) for showing speed data.
        """

        if widget.get_active() == True:
            if widget == self.selected_device_cb:
                Config.show_disk_usage_per_disk = 0
            if widget == self.all_devices_cb:
                Config.show_disk_usage_per_disk = 1

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_selected_item_notify(self, widget, parameter):
        """
        Change disk data/speed precision.
        Notify signal is sent when DropDown widget selection is changed.
        Currently GtkExpression parameter for DropDown can not be used because of PyGObject.
        """

        Config.performance_disk_data_precision = widget.get_selected()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_data_unit_radiobuttons_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection.
        """

        if self.data_power_of_1024_cb.get_active() == True:
            Config.performance_disk_data_unit = 0
        elif self.data_power_of_1000_cb.get_active() == True:
            Config.performance_disk_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_data_bits_cb_toggled(self, widget):
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


    def on_graph_color_button_clicked(self, widget):
        """
        Change graph foreground color.
        Also get current foreground color of the graph and set it as selected color of the dialog.
        """

        color = Gdk.RGBA()
        color.red, color.green, color.blue, color.alpha = Config.chart_line_color_disk_speed_usage
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
            Config.chart_line_color_disk_speed_usage = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog.hide()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    def on_hide_loop_ramdisk_zram_disks_cb_toggled(self, widget):
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


    def on_reset_button_clicked(self, widget):
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
        self.connect_signals()
        self.popover_set_gui()
        self.disconnect_signals()


    def popover_set_gui(self):
        """
        Set menu GUI items.
        """

        # Set active checkbuttons if disk read speed/disk write speed values are "1".
        if Config.plot_disk_read_speed == 1:
            self.read_speed_cb.set_active(True)
        if Config.plot_disk_read_speed == 0:
            self.read_speed_cb.set_active(False)
        if Config.plot_disk_write_speed == 1:
            self.write_speed_cb.set_active(True)
        if Config.plot_disk_write_speed == 0:
            self.write_speed_cb.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_disk_usage_per_disk == 0:
            self.selected_device_cb.set_active(True)
        if Config.show_disk_usage_per_disk == 1:
            self.all_devices_cb.set_active(True)

        # Set data unit checkbuttons and radiobuttons.
        if Config.performance_disk_data_unit == 0:
            self.data_power_of_1024_cb.set_active(True)
        if Config.performance_disk_data_unit == 1:
            self.data_power_of_1000_cb.set_active(True)
        if Config.performance_disk_speed_bit == 1:
            self.data_bits_cb.set_active(True)
        if Config.performance_disk_speed_bit == 0:
            self.data_bits_cb.set_active(False)

        # Set active checkbutton if "Hide loop, ramdisk, zram disks" option is enabled.
        if Config.hide_loop_ramdisk_zram_disks == 1:
            self.hide_loop_ramdisk_zram_disks_cb.set_active(True)
        if Config.hide_loop_ramdisk_zram_disks == 0:
            self.hide_loop_ramdisk_zram_disks_cb.set_active(False)

        self.disk_precision_dd.set_selected(Config.performance_disk_data_precision)


DiskMenu = DiskMenu()

