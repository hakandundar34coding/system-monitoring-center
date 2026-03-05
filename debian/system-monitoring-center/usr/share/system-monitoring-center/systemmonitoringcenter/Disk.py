import tkinter as tk
from tkinter import ttk

import os
import subprocess

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Disk:

    def __init__(self):

        self.name = "Disk"

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.disk_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.da_frame()

        self.information_frame()


    def tab_title_frame(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        """frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)"""

        # Label (Disk)
        label = Common.tab_title_label(frame, _tr("Disk"))

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label(frame)
        tooltip = Common.tooltip(self.device_vendor_model_label, _tr("Vendor-Model"))

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label(frame)
        tooltip = Common.tooltip(self.device_kernel_name_label, _tr("Device Name In Kernel"))


    def da_frame(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Frame (drawingarea)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 10))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(frame, _tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        self.da_upper_right_label  = Common.da_upper_lower_label(frame, "--")
        self.da_upper_right_label .grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.da_disk_speed = Common.drawingarea(frame, "da_disk_speed")
        self.da_disk_speed.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(frame, "0")
        label.grid(row=2, column=1, sticky="e")


    def information_frame(self):
        """
        Generate performance/information labels.
        """

        # Frame (performance/information labels)
        performance_info_grid = ttk.Frame(self.tab_frame)
        performance_info_grid.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        performance_info_grid.columnconfigure((0, 1), weight=1, uniform="equal")
        performance_info_grid.rowconfigure((0, 1), weight=1, uniform="equal")
        #performance_info_grid.rowconfigure(0, weight=1)

        # Styled information widgets (Read Speed and Write Speed)
        # ScrolledWindow (Read Speed and Write Speed)
        _frame, self.read_speed_label, self.write_speed_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Read Speed"), None, _tr("Write Speed"), None)
        _frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=(0, 5))

        # Styled information widgets (Read Data and Written Data)
        # ScrolledWindow (Read Data and Written Data)
        _frame, self.read_data_label, self.write_data_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Read Data"), _tr("Measured value since last system start"), _tr("Written Data"), _tr("Measured value since last system start"))
        _frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=(5, 0))

        # Frame - Right information labels
        performance_info_right_frame = ttk.Frame(performance_info_grid)
        performance_info_right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=0, pady=0)
        performance_info_right_frame.columnconfigure((0, 1), weight=1, uniform="equal")

        # Labels - Right information labels
        # Label (System Disk)
        label = Common.static_information_label(performance_info_right_frame, _tr("System Disk") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (System Disk)
        self.system_disk_label = Common.dynamic_information_label(performance_info_right_frame)
        self.system_disk_label.grid(row=0, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Used)
        label = Common.static_information_label(performance_info_right_frame, _tr("Used") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label and DrawingArea (Used)
        frame_label_and_da = ttk.Frame(performance_info_right_frame)
        frame_label_and_da.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        # Moving widgets problem is fixed by using the following configurations.
        frame_label_and_da.columnconfigure((0,1), weight=2, uniform="equal")
        frame_label_and_da.columnconfigure(1, weight=1)
        # DrawingArea (Used)
        self.da_disk_usage = ttk.Label(frame_label_and_da)
        self.da_disk_usage.grid(row=0, column=0, sticky="nsew", padx=0, pady=2)
        # Label (Used (percent))
        self.used_percent_label = Common.dynamic_information_label(frame_label_and_da)
        self.used_percent_label.grid(row=0, column=1, sticky="e", padx=(4, 0), pady=(0, 4))

        # Label (Free)
        label = Common.static_information_label(performance_info_right_frame, _tr("Free") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Free)
        self.free_label = Common.dynamic_information_label(performance_info_right_frame)
        self.free_label.grid(row=2, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Used)
        label = Common.static_information_label(performance_info_right_frame, _tr("Used") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Used)
        self.used_label = Common.dynamic_information_label(performance_info_right_frame)
        self.used_label.grid(row=3, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Capacity)
        label = Common.static_information_label(performance_info_right_frame, _tr("Capacity") + ":")
        label.grid(row=4, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Capacity)
        self.capacity_label = Common.dynamic_information_label(performance_info_right_frame)
        self.capacity_label.grid(row=4, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Details...)
        label = Common.static_information_label(performance_info_right_frame, _tr("Details") + ":")
        label.grid(row=5, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Show...)
        self.details_label = Common.clickable_label(performance_info_right_frame, self.on_details_label_released)
        self.details_label.grid(row=5, column=1, sticky="w", padx=(4, 0), pady=(0, 4))


    def on_details_label_released(self, event):
        """
        Show Disk details window.
        """

        self.disk_details_window_gui()
        self.disk_details_info_get()
        self.disk_details_update()


    def disk_details_window_gui(self):
        """
        Disk details window GUI.
        """

        # Window
        self.disk_details_window, frame = Common.window(MainWindow.main_window, _tr("Disk"))

        # Information labels
        # Label (Disk)
        label = Common.static_information_label(frame, _tr("Disk"))
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Disk)
        label = Common.static_information_label(frame, ":")
        label.grid(row=0, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Disk)
        self.disk_details_disk_label = Common.dynamic_information_label(frame)
        self.disk_details_disk_label.grid(row=0, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Parent Name)
        label = Common.static_information_label(frame, _tr("Parent Name"))
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Parent Name)
        label = Common.static_information_label(frame, ":")
        label.grid(row=1, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Parent Name)
        self.disk_details_parent_disk_label = Common.dynamic_information_label(frame)
        self.disk_details_parent_disk_label.grid(row=1, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (System Disk)
        label = Common.static_information_label(frame, _tr("System Disk"))
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (System Disk)
        label = Common.static_information_label(frame, ":")
        label.grid(row=2, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (System Disk)
        self.disk_details_system_disk_label = Common.dynamic_information_label(frame)
        self.disk_details_system_disk_label.grid(row=2, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Type)
        label = Common.static_information_label(frame, _tr("Type"))
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Type)
        label = Common.static_information_label(frame, ":")
        label.grid(row=3, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Type)
        self.disk_details_disk_type_label = Common.dynamic_information_label(frame)
        self.disk_details_disk_type_label.grid(row=3, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (File System)
        label = Common.static_information_label(frame, _tr("File System"))
        label.grid(row=4, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (File System)
        label = Common.static_information_label(frame, ":")
        label.grid(row=4, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (File System)
        self.disk_details_file_system_label = Common.dynamic_information_label(frame)
        self.disk_details_file_system_label.grid(row=4, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Capacity)
        label = Common.static_information_label(frame, _tr("Capacity"))
        label.grid(row=5, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Capacity)
        label = Common.static_information_label(frame, ":")
        label.grid(row=5, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Capacity)
        self.disk_details_capacity_label = Common.dynamic_information_label(frame)
        self.disk_details_capacity_label.grid(row=5, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Capacity (Mass Storage))
        label = Common.static_information_label(frame, _tr("Capacity") + "\n" + "(" + _tr("Mass Storage") + ")")
        label.grid(row=6, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Capacity (Mass Storage))
        label = Common.static_information_label(frame, ":")
        label.grid(row=6, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Capacity (Mass Storage))
        self.disk_details_capacity_mass_label = Common.dynamic_information_label(frame)
        self.disk_details_capacity_mass_label.grid(row=6, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Free)
        label = Common.static_information_label(frame, _tr("Free"))
        label.grid(row=7, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Free)
        label = Common.static_information_label(frame, ":")
        label.grid(row=7, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Free)
        self.disk_details_free_label = Common.dynamic_information_label(frame)
        self.disk_details_free_label.grid(row=7, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Used)
        label = Common.static_information_label(frame, _tr("Used"))
        label.grid(row=8, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Used)
        label = Common.static_information_label(frame, ":")
        label.grid(row=8, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Used)
        self.disk_details_used_label = Common.dynamic_information_label(frame)
        self.disk_details_used_label.grid(row=8, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Vendor-Model)
        label = Common.static_information_label(frame, _tr("Vendor - Model"))
        label.grid(row=9, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Vendor-Model)
        label = Common.static_information_label(frame, ":")
        label.grid(row=9, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Vendor-Model)
        self.disk_details_vendor_model_label = Common.dynamic_information_label(frame)
        self.disk_details_vendor_model_label.grid(row=9, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Label (File System))
        label = Common.static_information_label(frame, _tr("Label (File System)"))
        label.grid(row=10, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Label (File System))
        label = Common.static_information_label(frame, ":")
        label.grid(row=10, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Label (File System))
        self.details_label_fs_label = Common.dynamic_information_label(frame)
        self.details_label_fs_label.grid(row=10, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Mount Point)
        label = Common.static_information_label(frame, _tr("Mount Point"))
        label.grid(row=11, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Mount Point)
        label = Common.static_information_label(frame, ":")
        label.grid(row=11, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Mount Point)
        self.disk_details_mount_point_label = Common.dynamic_information_label(frame)
        self.disk_details_mount_point_label.grid(row=11, column=2, sticky="w", padx=0, pady=(0, 4))


    def disk_details_info_get(self):
        """
        Get disk details information.
        """

        # Get selected disk name and pci.ids file content
        selected_disk = self.selected_disk

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        disk_list = Performance.disk_list

        # Get information
        disk_type = Libsysmon.get_disk_type(selected_disk)
        disk_parent_name = Libsysmon.get_disk_parent_name(selected_disk, disk_type, disk_list)
        disk_file_system_information = Libsysmon.get_disk_file_system_information(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point, encrypted_disk_name  = Libsysmon.get_disk_file_system_capacity_used_free_used_percent_mount_point(disk_file_system_information, disk_list, selected_disk)
        if disk_file_system  == "fuseblk":
            disk_file_system = Libsysmon.get_disk_file_system_fuseblk(selected_disk)
        disk_if_system_disk = Libsysmon.get_disk_if_system_disk(selected_disk, Performance.system_disk_list)
        disk_capacity_mass_storage = Libsysmon.get_disk_capacity_mass_storage(selected_disk)
        disk_device_model_name = Libsysmon.get_disk_device_model_name(selected_disk, disk_type, disk_parent_name)
        disk_label = Libsysmon.get_disk_label(selected_disk)

        # Set Disk Details window title
        self.disk_details_window.title(_tr("Disk") + ": " + selected_disk)

        # Set label text by using storage/disk data
        # Set label text by using storage/disk data
        if encrypted_disk_name != "":
            self.disk_details_disk_label.set_label(text=selected_disk + " - " + encrypted_disk_name)
        else:
            self.disk_details_disk_label.config(text=selected_disk)
        self.disk_details_parent_disk_label.config(text=disk_parent_name)
        self.disk_details_system_disk_label.config(text=disk_if_system_disk)
        self.disk_details_disk_type_label.config(text=disk_type)
        self.disk_details_file_system_label.config(text=disk_file_system)
        self.disk_details_capacity_mass_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", disk_capacity_mass_storage, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_capacity_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_free_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_used_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision)}  ( {disk_usage_percentage:.0f}% )')
        self.disk_details_vendor_model_label.config(text=disk_device_model_name)
        self.details_label_fs_label.config(text=disk_label)
        self.disk_details_mount_point_label.config(text=disk_mount_point)


    def disk_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        if self.disk_details_window.state() == "normal":
            self.disk_details_info_get()
            self.disk_details_window.after(int(Config.update_interval*1000), self.disk_details_update)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        disk_list = Performance.disk_list
        selected_disk = Performance.selected_disk
        # Definition to access to this variable from "DiskDetails" module.
        self.selected_disk = selected_disk

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            check_value = "/sys/class/block/" + selected_disk
        except Exception:
            return

        # Get information.
        disk_type = Libsysmon.get_disk_type(selected_disk)
        disk_parent_name = Libsysmon.get_disk_parent_name(selected_disk, disk_type, disk_list)
        disk_device_model_name = Libsysmon.get_disk_device_model_name(selected_disk, disk_type, disk_parent_name)
        if_system_disk = Libsysmon.get_disk_if_system_disk(selected_disk, Performance.system_disk_list)


        # Show information on labels.
        self.device_vendor_model_label.config(text=disk_device_model_name)
        self.device_kernel_name_label.config(text=f'{selected_disk}  ({disk_type})')
        self.system_disk_label.config(text=if_system_disk)

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        disk_list = Performance.disk_list
        selected_disk = Performance.selected_disk

        # Run "initial_func" if selected disk is changed since the last loop.
        try:                                                                                      
            if self.selected_disk_prev != selected_disk:
                self.initial_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_disk_prev = selected_disk

        disk_read_speed = Performance.disk_read_speed
        disk_write_speed = Performance.disk_write_speed

        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        performance_disk_speed_bit = Config.performance_disk_speed_bit

        Performance.performance_line_charts_draw(self.da_disk_speed, "da_disk_speed")
        Performance.performance_bar_charts_draw(self.da_disk_usage, "da_disk_usage")

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        disk_list = Performance.disk_list
        try:                                                                                      
            if self.disk_list_prev != disk_list:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list" if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_list_prev = disk_list

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
        self.get_disk_update_disk_usage_percentages_on_disk_list()

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            if os.path.isdir("/sys/class/block/" + selected_disk) == False:
                return
        except Exception:
            return


        # Get information.
        disk_read_data, disk_write_data = Libsysmon.get_disk_read_write_data(selected_disk)
        disk_file_system_information = Libsysmon.get_disk_file_system_information(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, self.disk_usage_percentage, disk_mount_point, encrypted_disk_name  = Libsysmon.get_disk_file_system_capacity_used_free_used_percent_mount_point(disk_file_system_information, disk_list, selected_disk)


        # Show information on labels.
        self.read_speed_label.config(text=f'{Libsysmon.data_unit_converter("speed", performance_disk_speed_bit, disk_read_speed[selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.write_speed_label.config(text=f'{Libsysmon.data_unit_converter("speed", performance_disk_speed_bit, disk_write_speed[selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.read_data_label.config(text=Libsysmon.data_unit_converter("data", "none", disk_read_data, performance_disk_data_unit, performance_disk_data_precision))
        self.write_data_label.config(text=Libsysmon.data_unit_converter("data", "none", disk_write_data, performance_disk_data_unit, performance_disk_data_precision))
        if disk_mount_point != "-":
            self.used_percent_label.config(text=f'{self.disk_usage_percentage:.0f}%')
        if disk_mount_point == "-":
            self.used_percent_label.config(text="-%")
        self.free_label.config(text=Libsysmon.data_unit_converter("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision))
        self.used_label.config(text=Libsysmon.data_unit_converter("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision))
        self.capacity_label.config(text=Libsysmon.data_unit_converter("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision))


    def get_disk_update_disk_usage_percentages_on_disk_list(self):
        """
        Update disk usage percentages on the disk list between Performance tab sub-tabs.
        """

        # Get disk usage percentages.
        device_list = Performance.disk_list
        disk_usage_percentage_list = []
        disk_filesystem_information_list = Libsysmon.get_disk_file_system_information(device_list)
        for device in device_list:
            _, _, _, _, disk_usage_percentage, disk_mount_point, _ = Libsysmon.get_disk_file_system_capacity_used_free_used_percent_mount_point(disk_filesystem_information_list, device_list, device)
            # Append percentage number with no fractions in order to avoid updating the list very frequently.
            disk_usage_percentage_list.append(f'{disk_usage_percentage:.0f}')

        # Update disk usage percentages on disk list if disk usage percentages are changed since the last loop.
        try:                                                                                      
            if self.disk_usage_percentage_list_prev != disk_usage_percentage_list:
                MainWindow.main_gui_device_selection_list()
        # Avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_usage_percentage_list_prev = list(disk_usage_percentage_list)


Disk = Disk()

