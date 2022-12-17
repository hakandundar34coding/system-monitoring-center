#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow
import Common


class Disk:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.da_grid()

        self.information_grid()

        self.connect_signals()


    def tab_title_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Disk)
        label = Common.tab_title_label(_tr("Disk"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label()
        self.device_vendor_model_label.set_tooltip_text(_tr("Vendor-Model"))
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label()
        self.device_kernel_name_label.set_tooltip_text(_tr("Device Name In Kernel"))
        grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.tab_grid.attach(grid, 0, 1, 1, 1)

        # Label (drawingarea upper-left)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        grid.attach(label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        self.da_upper_right_label = Gtk.Label()
        self.da_upper_right_label.set_halign(Gtk.Align.END)
        self.da_upper_right_label.set_label("--")
        grid.attach(self.da_upper_right_label, 1, 0, 1, 1)

        # DrawingArea
        self.da_disk_speed = Common.drawingarea(Performance.performance_line_charts_draw, "da_disk_speed_usage")
        grid.attach(self.da_disk_speed, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.END)
        label.set_label("0")
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        self.tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Styled information widgets (Read Speed and Write Speed)
        # ScrolledWindow (Read Speed and Write Speed)
        scrolledwindow, self.read_speed_label, self.write_speed_label = Common.styled_information_scrolledwindow(_tr("Read Speed"), None, _tr("Write Speed"), None)
        performance_info_grid.attach(scrolledwindow, 0, 0, 1, 1)

        # Styled information widgets (Read Data and Written Data)
        # ScrolledWindow (Read Data and Written Data)
        scrolledwindow, self.read_data_label, self.write_data_label = Common.styled_information_scrolledwindow(_tr("Read Data"), _tr("Measured value since last system start"), _tr("Written Data"), _tr("Measured value since last system start"))
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Grid - Right information labels
        performance_info_right_grid = Gtk.Grid()
        performance_info_right_grid.set_column_homogeneous(True)
        #performance_info_right_grid.set_row_homogeneous(True)
        performance_info_right_grid.set_column_spacing(2)
        performance_info_right_grid.set_row_spacing(4)
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Labels - Right information labels
        # Label (System Disk)
        label = Common.static_information_label(_tr("System Disk") + ":")
        performance_info_right_grid.attach(label, 0, 0, 1, 1)
        # Label (System Disk)
        self.system_disk_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.system_disk_label, 1, 0, 1, 1)

        # Label (Used)
        label = Common.static_information_label(_tr("Used") + ":")
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label and DrawingArea (Used)
        grid_label_and_da = Gtk.Grid()
        grid_label_and_da.set_column_spacing(5)
        performance_info_right_grid.attach(grid_label_and_da, 1, 2, 1, 1)
        # DrawingArea (Used)
        self.da_disk_usage = Common.drawingarea(Performance.performance_bar_charts_draw, "da_disk_usage")
        self.da_disk_usage.set_vexpand(False)
        grid_label_and_da.attach(self.da_disk_usage, 0, 0, 1, 1)
        # Label (Used (percent))
        self.used_percent_label = Common.dynamic_information_label()
        grid_label_and_da.attach(self.used_percent_label, 1, 0, 1, 1)

        # Label (Free)
        label = Common.static_information_label(_tr("Free") + ":")
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (Free)
        self.free_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.free_label, 1, 3, 1, 1)

        # Label (Used)
        label = Common.static_information_label(_tr("Used") + ":")
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (Used)
        self.used_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.used_label, 1, 4, 1, 1)

        # Label (Capacity)
        label = Common.static_information_label(_tr("Capacity") + ":")
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (Capacity)
        self.capacity_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.capacity_label, 1, 5, 1, 1)

        # Label (Details...)
        label = Common.static_information_label(_tr("Details") + ":")
        performance_info_right_grid.attach(label, 0, 6, 1, 1)
        # Label (Show...)
        self.details_label = Common.clickable_label(_tr("Show..."))
        performance_info_right_grid.attach(self.details_label, 1, 6, 1, 1)


    def connect_signals(self):
        """
        Connect GUI signals.
        """

        self.da_disk_speed.set_draw_func(Performance.performance_line_charts_draw, "da_disk_speed_usage")
        self.da_disk_usage.set_draw_func(Performance.performance_bar_charts_draw, "da_disk_usage")

        # Drawingarea mouse events
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_disk_speed.add_controller(drawingarea_mouse_event)

        # "Show" label mouse events
        show_label_mouse_event = Gtk.GestureClick()
        show_label_mouse_event.connect("released", self.on_details_label_released)
        self.details_label.add_controller(show_label_mouse_event)


    def on_details_label_released(self, event, count, x, y):
        """
        Show Disk details window.
        """

        widget = event.get_widget()

        try:
            self.disk_details_window.present()
        except AttributeError:
            # Avoid generating window multiple times on every button click.
            self.disk_details_window_gui()
            self.disk_details_window.present()
        self.disk_details_info_get()
        self.disk_details_update()


    def disk_details_window_gui(self):
        """
        Disk details window GUI.
        """

        # Window
        self.disk_details_window = Gtk.Window()
        self.disk_details_window.set_default_size(400, 380)
        self.disk_details_window.set_title(_tr("Disk"))
        self.disk_details_window.set_icon_name("system-monitoring-center")
        self.disk_details_window.set_transient_for(MainWindow.main_window)
        self.disk_details_window.set_modal(True)
        self.disk_details_window.set_hide_on_close(True)

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.disk_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Common.window_main_grid()
        viewport.set_child(main_grid)

        # Information labels
        # Label (Disk)
        label = Common.static_information_label(_tr("Disk"))
        main_grid.attach(label, 0, 0, 1, 1)
        # Label (Disk)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 0, 1, 1)
        # Label (Disk)
        self.disk_details_disk_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_disk_label, 2, 0, 1, 1)

        # Label (Parent Name)
        label = Common.static_information_label(_tr("Parent Name"))
        main_grid.attach(label, 0, 1, 1, 1)
        # Label (Parent Name)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 1, 1, 1)
        # Label (Parent Name)
        self.disk_details_parent_disk_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_parent_disk_label, 2, 1, 1, 1)

        # Label (System Disk)
        label = Common.static_information_label(_tr("System Disk"))
        main_grid.attach(label, 0, 2, 1, 1)
        # Label (System Disk)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 2, 1, 1)
        # Label (System Disk)
        self.disk_details_system_disk_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_system_disk_label, 2, 2, 1, 1)

        # Label (Type)
        label = Common.static_information_label(_tr("Type"))
        main_grid.attach(label, 0, 3, 1, 1)
        # Label (Type)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 3, 1, 1)
        # Label (Type)
        self.disk_details_disk_type_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_disk_type_label, 2, 3, 1, 1)

        # Label (File System)
        label = Common.static_information_label(_tr("File System"))
        main_grid.attach(label, 0, 4, 1, 1)
        # Label (File System)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 4, 1, 1)
        # Label (File System)
        self.disk_details_file_system_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_file_system_label, 2, 4, 1, 1)

        # Label (Capacity)
        label = Common.static_information_label(_tr("Capacity"))
        main_grid.attach(label, 0, 5, 1, 1)
        # Label (Capacity)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 5, 1, 1)
        # Label (Capacity)
        self.disk_details_capacity_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_capacity_label, 2, 5, 1, 1)

        # Label (Capacity (Mass Storage))
        label = Common.static_information_label(_tr("Capacity") + "\n" + "(" + _tr("Mass Storage") + ")")
        main_grid.attach(label, 0, 6, 1, 1)
        # Label (Capacity (Mass Storage))
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 6, 1, 1)
        # Label (Capacity (Mass Storage))
        self.disk_details_capacity_mass_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_capacity_mass_label, 2, 6, 1, 1)

        # Label (Free)
        label = Common.static_information_label(_tr("Free"))
        main_grid.attach(label, 0, 7, 1, 1)
        # Label (Free)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 7, 1, 1)
        # Label (Free)
        self.disk_details_free_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_free_label, 2, 7, 1, 1)

        # Label (Used)
        label = Common.static_information_label(_tr("Used"))
        main_grid.attach(label, 0, 8, 1, 1)
        # Label (Used)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 8, 1, 1)
        # Label (Used)
        self.disk_details_used_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_used_label, 2, 8, 1, 1)

        # Label (Vendor-Model)
        label = Common.static_information_label(_tr("Vendor-Model"))
        main_grid.attach(label, 0, 9, 1, 1)
        # Label (Vendor-Model)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 9, 1, 1)
        # Label (Vendor-Model)
        self.disk_details_vendor_model_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_vendor_model_label, 2, 9, 1, 1)

        # Label (Label (File System))
        label = Common.static_information_label(_tr("Label (File System)"))
        main_grid.attach(label, 0, 10, 1, 1)
        # Label (Label (File System))
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 10, 1, 1)
        # Label (Label (File System))
        self.details_label_fs_label = Common.dynamic_information_label()
        main_grid.attach(self.details_label_fs_label, 2, 10, 1, 1)

        # Label (Mount Point)
        label = Common.static_information_label(_tr("Mount Point"))
        main_grid.attach(label, 0, 11, 1, 1)
        # Label (Mount Point)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 11, 1, 1)
        # Label (Mount Point)
        self.disk_details_mount_point_label = Common.dynamic_information_label()
        main_grid.attach(self.disk_details_mount_point_label, 2, 11, 1, 1)


    def disk_details_info_get(self):
        """
        Get disk details information.
        """

        # Get selected disk name and pci.ids file content
        selected_disk = self.selected_disk

        disk_sector_size = Performance.disk_sector_size

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        disk_list = Performance.disk_list

        # Get information
        disk_type = Disk.disk_type_func(selected_disk)
        disk_parent_name = Disk.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_file_system_information = Disk.disk_file_system_information_func(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point  = Disk.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_file_system_information, disk_list, selected_disk)
        if disk_file_system  == "fuseblk":
            disk_file_system = Disk.disk_file_system_fuseblk_func(selected_disk)
        disk_if_system_disk = Disk.disk_if_system_disk_func(selected_disk)
        disk_capacity_mass_storage = Disk.disk_capacity_mass_storage_func(selected_disk, disk_mount_point, disk_sector_size)
        disk_device_model_name = Disk.disk_device_model_name_func(selected_disk, disk_type, disk_parent_name)
        disk_label = Disk.disk_label_func(selected_disk)

        # Set Disk Details window title
        self.disk_details_window.set_title(_tr("Disk") + ": " + selected_disk)

        # Set label text by using storage/disk data
        self.disk_details_disk_label.set_label(selected_disk)
        self.disk_details_parent_disk_label.set_label(disk_parent_name)
        self.disk_details_system_disk_label.set_label(disk_if_system_disk)
        self.disk_details_disk_type_label.set_label(disk_type)
        self.disk_details_file_system_label.set_label(disk_file_system)
        self.disk_details_capacity_mass_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_capacity_mass_storage, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_capacity_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_free_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_used_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision)}  ( {disk_usage_percentage:.0f}% )')
        self.disk_details_vendor_model_label.set_label(disk_device_model_name)
        self.details_label_fs_label.set_label(disk_label)
        self.disk_details_mount_point_label.set_label(disk_mount_point)


    def disk_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        if self.disk_details_window.get_visible() == True:
            # Destroy GLib source for preventing it repeating the function.
            try:
                self.main_glib_source.destroy()
            # Prevent errors if this is first run of the function.
            except AttributeError:
                pass
            self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)
            self.disk_details_info_get()
            self.main_glib_source.set_callback(self.disk_details_update)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
            # A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    def disk_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        disk_list = Performance.disk_list
        selected_disk_number = Performance.selected_disk_number
        selected_disk = disk_list[selected_disk_number]
        # Definition to access to this variable from "DiskDetails" module.
        self.selected_disk = selected_disk

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            check_value = "/sys/class/block/" + selected_disk
        except Exception:
            return

        # Get information.
        disk_type = self.disk_type_func(selected_disk)
        disk_parent_name = self.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_device_model_name = self.disk_device_model_name_func(selected_disk, disk_type, disk_parent_name)
        if_system_disk = self.disk_if_system_disk_func(selected_disk)


        # Show information on labels.
        self.device_vendor_model_label.set_text(disk_device_model_name)
        self.device_kernel_name_label.set_text(f'{selected_disk}  ({disk_type})')
        self.system_disk_label.set_text(if_system_disk)

        self.initial_already_run = 1


    def disk_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        disk_list = Performance.disk_list
        selected_disk_number = Performance.selected_disk_number
        selected_disk = disk_list[selected_disk_number]
        disk_sector_size = Performance.disk_sector_size

        # Run "disk_initial_func" if selected disk is changed since the last loop.
        try:                                                                                      
            if self.selected_disk_prev != selected_disk:
                self.disk_initial_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_disk_prev = selected_disk

        disk_read_speed = Performance.disk_read_speed
        disk_write_speed = Performance.disk_write_speed

        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        performance_disk_speed_bit = Config.performance_disk_speed_bit

        self.da_disk_speed.queue_draw()
        self.da_disk_usage.queue_draw()

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        disk_list_system_ordered = Performance.disk_list_system_ordered
        try:                                                                                      
            if self.disk_list_system_ordered_prev != disk_list_system_ordered:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list" if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_list_system_ordered_prev = disk_list_system_ordered

        # Run "main_gui_device_selection_list" if "hide_loop_ramdisk_zram_disks" option is changed since the last loop.
        hide_loop_ramdisk_zram_disks = Config.hide_loop_ramdisk_zram_disks
        try:                                                                                      
            if self.hide_loop_ramdisk_zram_disks_prev != hide_loop_ramdisk_zram_disks:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list" if this is first loop of the function.
        except AttributeError:
            pass
        self.hide_loop_ramdisk_zram_disks_prev = hide_loop_ramdisk_zram_disks

        # Update disk usage percentages on disk list between Performance tab sub-tabs.
        self.disk_update_disk_usage_percentages_on_disk_list_func()

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            if os.path.isdir("/sys/class/block/" + selected_disk) == False:
                return
        except Exception:
            return


        # Get information.
        disk_read_data, disk_write_data = self.disk_read_write_data_func(selected_disk, disk_list)
        disk_file_system_information = self.disk_file_system_information_func(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, self.disk_usage_percentage, disk_mount_point  = self.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_file_system_information, disk_list, selected_disk)


        # Show information on labels.
        self.read_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_read_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.write_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_write_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.read_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_read_data, performance_disk_data_unit, performance_disk_data_precision))
        self.write_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_write_data, performance_disk_data_unit, performance_disk_data_precision))
        if disk_mount_point != "-":
            self.used_percent_label.set_text(f'{self.disk_usage_percentage:.0f}%')
        if disk_mount_point == "-":
            self.used_percent_label.set_text("-%")
        self.free_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision))
        self.used_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision))
        self.capacity_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision))


    def disk_type_func(self, selected_disk):
        """
        Get disk type (Disk or Partition).
        """

        with open("/sys/class/block/" + selected_disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")

        for line in sys_class_block_disk_uevent_lines:
            if "DEVTYPE" in line:
                disk_type = _tr(line.split("=")[1].capitalize())
                break

        return disk_type


    def disk_parent_name_func(self, selected_disk, disk_type, disk_list):
        """
        Get disk parent name.
        """

        disk_parent_name = "-"
        if disk_type == _tr("Partition"):
            for check_disk_dir in disk_list:
                if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk) == True:
                    disk_parent_name = check_disk_dir

        return disk_parent_name


    def disk_device_model_name_func(self, selected_disk, disk_type, disk_parent_name):
        """
        Get disk vendor and model.
        """

        if disk_type == _tr("Disk"):
            disk_or_parent_disk_name = selected_disk
        if disk_type == _tr("Partition"):
            disk_or_parent_disk_name = disk_parent_name

        # Get disk vendor and model.
        device_vendor_name = "-"
        device_model_name = "-"
        # Try to get device vendor model if this is a NVMe SSD. These disks do not have "modalias" or "model" files under "/sys/class/block/" + selected_disk + "/device" directory.
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = Common.device_vendor_model(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass
        # Try to get device vendor model if this is a SCSI, IDE or virtio device (on QEMU virtual machines).
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = Common.device_vendor_model(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass
        # Try to get device vendor model if this is a SCSI or IDE disk.
        if device_vendor_name == "[scsi_or_ide_disk]":
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/vendor") as reader:
                    device_vendor_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                device_vendor_name = "Unknown"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                    device_model_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                device_model_name = "Unknown"
        if device_vendor_name == "Unknown":
            device_vendor_name = "[" + _tr("Unknown") + "]"
        if device_model_name == "Unknown":
            device_model_name = "[" + _tr("Unknown") + "]"
        disk_device_model_name = f'{device_vendor_name} - {device_model_name}'
        # Get disk vendor and model if disk is loop device or swap disk.
        if selected_disk.startswith("loop"):
            disk_device_model_name = "[Loop Device]"
        if selected_disk.startswith("zram"):
            disk_device_model_name = "[" + _tr("Swap").upper() + "]"
        if selected_disk.startswith("ram"):
            disk_device_model_name = "[Ramdisk]"
        if selected_disk.startswith("dm-"):
            disk_device_model_name = "[Device Mapper]"
        if selected_disk.startswith("mmcblk"):
            # Read database file for MMC disk register values. For more info about CIDs: https://www.kernel.org/doc/Documentation/mmc/mmc-dev-attrs.txt
            with open(os.path.dirname(os.path.realpath(__file__)) + "/../database/sdcard.ids") as reader:
                ids_file_output = reader.read().strip()
            # Get device vendor, model names from device ID file content.
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/manfid") as reader:
                    disk_vendor_manfid = reader.read().strip()
                search_text1 = "MANFID " + disk_vendor_manfid.split("0x", 1)[-1]
                if search_text1 in ids_file_output:
                    disk_vendor = ids_file_output.split(search_text1, 1)[1].split("\n", 1)[0].strip()
                else:
                    disk_vendor = "-"
            except Exception:
                disk_vendor = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/name") as reader:
                    disk_name = reader.read().strip()
                disk_model = disk_name
            except FileNotFoundError:
                disk_model = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/type") as reader:
                    disk_card_type = reader.read().strip()
            except FileNotFoundError:
                disk_card_type = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/speed_class") as reader:
                    disk_card_speed_class = reader.read().strip()
            except FileNotFoundError:
                disk_card_speed_class = "-"
            disk_device_model_name = f'{disk_vendor} - {disk_model} ({disk_card_type} Card, Class {disk_card_speed_class})'

        return disk_device_model_name


    def disk_file_system_information_func(self, disk_list):
        """
        Get file system information (file systems, capacities, used, free, used percentages and mount points) of all disks.
        """

        # Get file system information of the mounted disks by using "df" command.
        command_list = ["df", "--output=source,fstype,size,used,avail,pcent,target"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        df_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

        # Remove command output title line. Only disk information will be left.
        del df_output_lines[0]

        # Get mounted disk list.
        mounted_disk_list = []
        for line in df_output_lines:
            disk_name = line.split()[0]
            mounted_disk_list.append(disk_name.split("/dev/")[-1])

        # Get file system information of the mounted and unmounted disks.
        disk_filesystem_information_list = []
        for disk in disk_list:
            if disk in mounted_disk_list:
                index = mounted_disk_list.index(disk)
                disk_file_system = df_output_lines[index].split()[1]
                disk_capacity = int(df_output_lines[index].split()[2]) * 1024
                disk_used = int(df_output_lines[index].split()[3]) * 1024
                disk_free = int(df_output_lines[index].split()[4]) * 1024
                disk_used_percentage = int(df_output_lines[index].split()[5].strip("%"))
                disk_mount_point = df_output_lines[index].split("% ", 1)[-1]
            else:
                disk_file_system = "[" + _tr("Not mounted") + "]"
                disk_capacity = "[" + _tr("Not mounted") + "]"
                disk_used = "[" + _tr("Not mounted") + "]"
                disk_free = "[" + _tr("Not mounted") + "]"
                disk_used_percentage = 0
                disk_mount_point = "[" + _tr("Not mounted") + "]"
            disk_filesystem_information_list.append([disk, disk_file_system, disk_capacity, disk_used, disk_free, disk_used_percentage, disk_mount_point])

        return disk_filesystem_information_list


    def disk_file_system_capacity_used_free_used_percent_mount_point_func(self, disk_filesystem_information_list, disk_list, selected_disk):
        """
        Get file file systems, capacities, used, free, used percentages and mount points of all disks.
        """

        disk_index = disk_list.index(selected_disk)
        disk_file_system = disk_filesystem_information_list[disk_index][1]
        disk_capacity = disk_filesystem_information_list[disk_index][2]
        disk_used = disk_filesystem_information_list[disk_index][3]
        disk_free = disk_filesystem_information_list[disk_index][4]
        disk_usage_percentage = disk_filesystem_information_list[disk_index][5]
        disk_mount_point = disk_filesystem_information_list[disk_index][6]

        return disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point


    def disk_mount_point_func(self, selected_disk):
        """
        Get disk mount point.
        """

        with open("/proc/mounts") as reader:
            proc_mounts_output = reader.read().strip()
        self.proc_mounts_output_lines = proc_mounts_output.split("\n")

        disk_mount_point = "-"
        disk_mount_point_list_scratch = []
        for line in self.proc_mounts_output_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == selected_disk:
                # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                disk_mount_point_list_scratch.append(bytes(line_split[1], "utf-8").decode("unicode_escape"))

        if len(disk_mount_point_list_scratch) == 1:
            disk_mount_point = disk_mount_point_list_scratch[0]

        # System disk is listed twice with different mountpoints on some systems (such as systems use btrfs filsystem or chroot). "/" mountpoint information is used.
        if len(disk_mount_point_list_scratch) > 1 and "/" in disk_mount_point_list_scratch:
            disk_mount_point = "/"

        # System disks on some devices such as ARM devices may not be listed in "/proc/mounts" file.
        if disk_mount_point == "-":
            system_disk = "-"
            with open("/proc/cmdline") as reader:
                proc_cmdline = reader.read()
            if "root=UUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk = os.path.realpath(f'/dev/disk/by-uuid/{disk_uuid_partuuid}').split("/")[-1].strip()
            if "root=PARTUUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk = os.path.realpath(f'/dev/disk/by-partuuid/{disk_uuid_partuuid}').split("/")[-1].strip()
            if system_disk != "-" and system_disk == selected_disk:
                if "/dev/root / " in proc_mounts_output:
                    disk_mount_point = "/"

        return disk_mount_point


    def disk_file_system_fuseblk_func(self, selected_disk):
        """
        Get disk file system if it is detected as 'fuseblk'.
        """

        # Try to get actual file system by using "lsblk" tool if file system
        # has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts"
        # file contains file system information as in user space. To be able to get the
        # actual file system, root access is needed for reading from some files or 
        # "lsblk" tool could be used.
        try:
            disk_for_file_system = "/dev/" + selected_disk
            if Config.environment_type == "flatpak":
                disk_file_system = (subprocess.check_output(["flatpak-spawn", "--host", "lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
            else:
                disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
        except Exception:
            disk_file_system = "fuseblk"

        return disk_file_system


    def disk_if_system_disk_func(self, selected_disk):
        """
        Get if system disk information.
        """

        if selected_disk in Performance.system_disk_list:
            if_system_disk = _tr("Yes")
        else:
            if_system_disk = _tr("No")

        return if_system_disk


    def disk_read_write_data_func(self, selected_disk, disk_list):
        """
        Get disk read data and disk write data.
        """

        disk_read_data = Performance.disk_read_data[disk_list.index(selected_disk)]
        disk_write_data = Performance.disk_write_data[disk_list.index(selected_disk)]

        return disk_read_data, disk_write_data


    def disk_capacity_mass_storage_func(self, selected_disk, disk_mount_point, disk_sector_size):
        """
        Get disk capacity (mass storage).
        """

        with open("/sys/class/block/" + selected_disk + "/size") as reader:
            disk_capacity_mass_storage = int(reader.read()) * disk_sector_size

        return disk_capacity_mass_storage


    def disk_label_func(self, selected_disk):
        """
        Get disk label.
        """

        disk_label = "-"
        try:
            disk_label_list = os.listdir("/dev/disk/by-label/")
            for label in disk_label_list:
                if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == selected_disk:
                    # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                    disk_label = bytes(label, "utf-8").decode("unicode_escape")
        except FileNotFoundError:
            pass

        return disk_label


    def disk_update_disk_usage_percentages_on_disk_list_func(self):
        """
        Update disk usage percentages on the disk list between Performance tab sub-tabs.
        """

        # Get disk usage percentages.
        device_list = Performance.disk_list_system_ordered
        disk_usage_percentage_list = []
        for device in device_list:
            disk_filesystem_information_list = self.disk_file_system_information_func(device_list)
            _, _, _, _, disk_usage_percentage, disk_mount_point = self.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_filesystem_information_list, device_list, device)
            # Append percentage number with no fractions in order to avoid updating the list very frequently.
            disk_usage_percentage_list.append(f'{disk_usage_percentage:.0f}')

        # Update disk usage percentages on disk list if disk usage percentages are changed since the last loop.
        try:                                                                                      
            if self.disk_usage_percentage_list_prev != disk_usage_percentage_list:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_usage_percentage_list_prev = disk_usage_percentage_list


Disk = Disk()

