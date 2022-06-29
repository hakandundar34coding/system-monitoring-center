#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Disk import Disk
from Performance import Performance


# Define class
class DiskDetails:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder1301w = Gtk.Builder()
        builder1301w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskDetailsWindow.ui")

        # Get GUI objects
        self.window1301w = builder1301w.get_object('window1301w')
        self.label1301w = builder1301w.get_object('label1301w')
        self.label1302w = builder1301w.get_object('label1302w')
        self.label1303w = builder1301w.get_object('label1303w')
        self.label1304w = builder1301w.get_object('label1304w')
        self.label1305w = builder1301w.get_object('label1305w')
        self.label1306w = builder1301w.get_object('label1306w')
        self.label1307w = builder1301w.get_object('label1307w')
        self.label1308w = builder1301w.get_object('label1308w')
        self.label1309w = builder1301w.get_object('label1309w')
        self.label1311w = builder1301w.get_object('label1311w')
        self.label1312w = builder1301w.get_object('label1312w')
        self.label1314w = builder1301w.get_object('label1314w')

        # Connect GUI signals
        self.window1301w.connect("delete-event", self.on_window1301w_delete_event)
        self.window1301w.connect("show", self.on_window1301w_show)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window1301w_delete_event(self, widget, event):

        widget.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window1301w_show(self, widget):

        # Call this function in order to reset Disk Details window. Data from previous storage/disk remains visible (for a short time) until getting and showing new storage/disk data if window is closed and opened for an another storage/disk because window is made hidden when close button is clicked.
        self.disk_details_gui_reset_func()

        # Get and show disk information.
        self.disk_details_run_func()


    # ----------------------- Called for reseting labels on the GUI when window is shown -----------------------
    def disk_details_gui_reset_func(self):

        self.label1301w.set_text("--")
        self.label1302w.set_text("--")
        self.label1303w.set_text("--")
        self.label1304w.set_text("--")
        self.label1305w.set_text("--")
        self.label1306w.set_text("--")
        self.label1307w.set_text("--")
        self.label1308w.set_text("--")
        self.label1309w.set_text("--")
        self.label1311w.set_text("--")
        self.label1312w.set_text("--")
        self.label1314w.set_text("--")


    # ----------------------------------- Disk - Disk Details Foreground Function -----------------------------------
    def disk_details_loop_func(self):

        # Get selected disk name and pci.ids file content
        selected_disk = Disk.selected_disk

        disk_sector_size = Performance.disk_sector_size

        # Set Disk Details window title
        self.window1301w.set_title(_tr("Disk") + ": " + selected_disk)

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        disk_list = Performance.disk_list


        # Get information.
        disk_type = Disk.disk_type_func(selected_disk)
        disk_parent_name = Disk.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_mount_point = Disk.disk_mount_point_func(selected_disk)
        disk_file_system = Disk.disk_file_system_func(selected_disk)
        disk_if_system_disk = Disk.disk_if_system_disk_func(selected_disk)
        disk_capacity_mass_storage = Disk.disk_capacity_mass_storage_func(selected_disk, disk_mount_point, disk_sector_size)
        disk_capacity, disk_size, disk_available, disk_free, disk_used, disk_usage_percent = Disk.disk_disk_capacity_size_available_free_used_usage_percent_func(disk_mount_point)
        disk_device_model_name = Disk.disk_device_model_name_func(selected_disk, disk_type, disk_parent_name)
        disk_label = Disk.disk_label_func(selected_disk)


        # Set label text by using storage/disk data
        self.label1301w.set_text(selected_disk)
        self.label1302w.set_text(disk_parent_name)
        self.label1303w.set_text(disk_if_system_disk)
        self.label1304w.set_text(disk_type)
        self.label1305w.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", disk_capacity_mass_storage, performance_disk_data_unit, performance_disk_data_precision)}')
        self.label1306w.set_text(disk_file_system)
        self.label1307w.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision)}')
        self.label1308w.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", disk_available, performance_disk_data_unit, performance_disk_data_precision)}')
        self.label1309w.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision)} - {disk_usage_percent:.1f}%')
        self.label1311w.set_text(disk_device_model_name)
        self.label1312w.set_text(disk_label)
        self.label1314w.set_text(disk_mount_point)


    # ----------------------------------- Disk Details - Run Function -----------------------------------
    def disk_details_run_func(self):

        if self.window1301w.get_visible() == True:
            try:
                GLib.idle_add(self.disk_details_loop_func)
            # Hide Disk Details window and stop the function if some of the disk is not found which means disk is removed.
            except FileNotFoundError:
                window1301w.hide()
                print("_disk_removed_")
                return
            GLib.timeout_add(Config.update_interval * 1000, self.disk_details_run_func)


# Generate object
DiskDetails = DiskDetails()

