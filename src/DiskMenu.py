#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

from Config import Config
from Performance import Performance
from Disk import Disk
from MainGUI import MainGUI


# Define class
class DiskMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskMenus.ui")

        # Get GUI objects
        self.popover1301p = builder.get_object('popover1301p')
        self.button1301p = builder.get_object('button1301p')
        self.button1303p = builder.get_object('button1303p')
        self.combobox1301p = builder.get_object('combobox1301p')
        self.checkbutton1301p = builder.get_object('checkbutton1301p')
        self.checkbutton1302p = builder.get_object('checkbutton1302p')
        self.checkbutton1304p = builder.get_object('checkbutton1304p')
        self.checkbutton1305p = builder.get_object('checkbutton1305p')
        self.radiobutton1301p = builder.get_object('radiobutton1301p')
        self.radiobutton1302p = builder.get_object('radiobutton1302p')
        self.radiobutton1303p = builder.get_object('radiobutton1303p')
        self.radiobutton1304p = builder.get_object('radiobutton1304p')
        self.colorchooserdialog1301 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1301p.connect("show", self.on_popover1301p_show)
        self.button1301p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1303p.connect("clicked", self.on_button1303p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def disk_tab_customization_popover_connect_signals_func(self):

        self.checkbutton1301p.connect("toggled", self.on_checkbutton1301p_toggled)
        self.checkbutton1302p.connect("toggled", self.on_checkbutton1302p_toggled)
        self.checkbutton1304p.connect("toggled", self.on_checkbutton1304p_toggled)
        self.checkbutton1305p.connect("toggled", self.on_checkbutton1305p_toggled)
        self.radiobutton1301p.connect("toggled", self.on_radiobutton1301p_toggled)
        self.radiobutton1302p.connect("toggled", self.on_radiobutton1302p_toggled)
        self.radiobutton1303p.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.radiobutton1304p.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.combobox1301p.connect("changed", self.on_combobox1301p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def disk_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton1301p.disconnect_by_func(self.on_checkbutton1301p_toggled)
        self.checkbutton1302p.disconnect_by_func(self.on_checkbutton1302p_toggled)
        self.checkbutton1304p.disconnect_by_func(self.on_checkbutton1304p_toggled)
        self.checkbutton1305p.disconnect_by_func(self.on_checkbutton1305p_toggled)
        self.radiobutton1301p.disconnect_by_func(self.on_radiobutton1301p_toggled)
        self.radiobutton1302p.disconnect_by_func(self.on_radiobutton1302p_toggled)
        self.radiobutton1303p.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.radiobutton1304p.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.combobox1301p.disconnect_by_func(self.on_combobox1301p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1301p_show(self, widget):

        try:
            self.disk_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.disk_tab_popover_set_gui()
        self.disk_tab_customization_popover_connect_signals_func()


    # ----------------------- "disk read speed" Checkbutton -----------------------
    def on_checkbutton1301p_toggled(self, widget):

        if widget.get_active() == True:
            Config.plot_disk_read_speed = 1
        if widget.get_active() == False:
            if self.checkbutton1302p.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_read_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "disk write speed" Checkbutton -----------------------
    def on_checkbutton1302p_toggled(self, widget):

        if widget.get_active() == True:
            Config.plot_disk_write_speed = 1
        if widget.get_active() == False:
            if self.checkbutton1301p.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_write_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Selected Device" Radiobutton -----------------------
    def on_radiobutton1301p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_disk_usage_per_disk = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "All Devices" Radiobutton -----------------------
    def on_radiobutton1302p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_disk_usage_per_disk = 1

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Precision" Combobox -----------------------
    def on_combobox1301p_changed(self, widget):

        Config.performance_disk_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Show units as powers of: 1024 or 1000" Radiobuttons -----------------------
    def on_data_unit_radiobuttons_toggled(self, widget):

        if self.radiobutton1303p.get_active() == True:
            Config.performance_disk_data_unit = 0
        elif self.radiobutton1304p.get_active() == True:
            Config.performance_disk_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Show speed units as multiples of bits" Checkbutton -----------------------
    def on_checkbutton1304p_toggled(self, widget):

        if widget.get_active() == True:
            Config.performance_disk_speed_bit = 1
        else:
            Config.performance_disk_speed_bit = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1301p:
            red, blue, green, alpha = Config.chart_line_color_disk_speed_usage
        self.colorchooserdialog1301.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1301.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1301.get_rgba()
            if widget == self.button1301p:
                Config.chart_line_color_disk_speed_usage = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1301.hide()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Hide loop, ramdisk, zram disks" Checkbutton -----------------------
    def on_checkbutton1305p_toggled(self, widget):

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


    # ----------------------- "Reset All" Button -----------------------
    def on_button1303p_clicked(self, widget):

        # Load default settings
        Config.config_default_performance_disk_func()
        Config.config_save_func()
        Performance.performance_set_selected_disk_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainGUI.main_gui_device_selection_list_func()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        self.disk_tab_customization_popover_disconnect_signals_func()
        self.disk_tab_popover_set_gui()
        self.disk_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def disk_tab_popover_set_gui(self):

        # Set active checkbuttons if disk read speed/disk write speed values are "1".
        if Config.plot_disk_read_speed == 1:
            self.checkbutton1301p.set_active(True)
        if Config.plot_disk_read_speed == 0:
            self.checkbutton1301p.set_active(False)
        if Config.plot_disk_write_speed == 1:
            self.checkbutton1302p.set_active(True)
        if Config.plot_disk_write_speed == 0:
            self.checkbutton1302p.set_active(False)

        # Set active checkbutton if "Hide loop, ramdisk, zram disks" option is enabled.
        if Config.hide_loop_ramdisk_zram_disks == 1:
            self.checkbutton1305p.set_active(True)
        if Config.hide_loop_ramdisk_zram_disks == 0:
            self.checkbutton1305p.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_disk_usage_per_disk == 0:
            self.radiobutton1301p.set_active(True)
        if Config.show_disk_usage_per_disk == 1:
            self.radiobutton1302p.set_active(True)

        # Set data unit checkbuttons and radiobuttons.
        if Config.performance_disk_data_unit == 0:
            self.radiobutton1303p.set_active(True)
        if Config.performance_disk_data_unit == 1:
            self.radiobutton1304p.set_active(True)
        if Config.performance_disk_speed_bit == 1:
            self.checkbutton1304p.set_active(True)
        if Config.performance_disk_speed_bit == 0:
            self.checkbutton1304p.set_active(False)

        # Add Disk data precision data into combobox.
        liststore1301p = Gtk.ListStore()
        liststore1301p.set_column_types([str, int])
        self.combobox1301p.set_model(liststore1301p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1301p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1301p.pack_start(renderer_text, True)
        self.combobox1301p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1301p.append([data[1], data[2]])
        self.combobox1301p.set_active(Config.performance_disk_data_precision)


# Generate object
DiskMenu = DiskMenu()

