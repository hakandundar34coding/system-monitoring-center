import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


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
        label = Common.da_upper_lower_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)", Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        self.da_upper_right_label = Common.da_upper_lower_label("--", Gtk.Align.END)
        grid.attach(self.da_upper_right_label, 1, 0, 1, 1)

        # DrawingArea
        self.da_disk_speed = Common.drawingarea(Performance.performance_line_charts_draw, "da_disk_speed")
        grid.attach(self.da_disk_speed, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Common.performance_info_grid()
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
        performance_info_right_grid = Common.performance_info_right_grid()
        performance_info_right_grid.set_row_homogeneous(False)
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
        self.details_label = Common.clickable_label(_tr("Show..."), self.on_details_label_released)
        performance_info_right_grid.attach(self.details_label, 1, 6, 1, 1)


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
        self.disk_details_window.set_title(_tr("Disk") + ": " + selected_disk)

        # Set label text by using storage/disk data
        if encrypted_disk_name != "":
            self.disk_details_disk_label.set_label(selected_disk + " - " + encrypted_disk_name)
        else:
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
        self.device_vendor_model_label.set_label(disk_device_model_name)
        self.device_kernel_name_label.set_label(f'{selected_disk}  ({disk_type})')
        self.system_disk_label.set_label(if_system_disk)

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

        self.da_disk_speed.queue_draw()
        self.da_disk_usage.queue_draw()

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
        self.read_speed_label.set_label(f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_read_speed[selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.write_speed_label.set_label(f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_write_speed[selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.read_data_label.set_label(Performance.performance_data_unit_converter_func("data", "none", disk_read_data, performance_disk_data_unit, performance_disk_data_precision))
        self.write_data_label.set_label(Performance.performance_data_unit_converter_func("data", "none", disk_write_data, performance_disk_data_unit, performance_disk_data_precision))
        if disk_mount_point != "-":
            self.used_percent_label.set_label(f'{self.disk_usage_percentage:.0f}%')
        if disk_mount_point == "-":
            self.used_percent_label.set_label("-%")
        self.free_label.set_label(Performance.performance_data_unit_converter_func("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision))
        self.used_label.set_label(Performance.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision))
        self.capacity_label.set_label(Performance.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision))


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

