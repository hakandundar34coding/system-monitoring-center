#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Disk:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskTab.ui")

        # Get GUI objects
        self.grid1301 = builder.get_object('grid1301')
        self.drawingarea1301 = builder.get_object('drawingarea1301')
        self.drawingarea1302 = builder.get_object('drawingarea1302')
        self.button1301 = builder.get_object('button1301')
        self.label1301 = builder.get_object('label1301')
        self.label1302 = builder.get_object('label1302')
        self.label1303 = builder.get_object('label1303')
        self.label1304 = builder.get_object('label1304')
        self.label1305 = builder.get_object('label1305')
        self.label1306 = builder.get_object('label1306')
        self.label1307 = builder.get_object('label1307')
        self.label1308 = builder.get_object('label1308')
        self.label1309 = builder.get_object('label1309')
        self.label1310 = builder.get_object('label1310')
        self.label1311 = builder.get_object('label1311')
        self.label1313 = builder.get_object('label1313')
        self.eventbox1301 = builder.get_object('eventbox1301')

        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-radius: 8px 8px 8px 8px;}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        self.viewport1301 = builder.get_object('viewport1301')
        self.viewport1301.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.viewport1302 = builder.get_object('viewport1302')
        self.viewport1302.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        self.separator1301 = builder.get_object('separator1301')
        self.separator1301.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1302 = builder.get_object('separator1302')
        self.separator1302.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1303 = builder.get_object('separator1303')
        self.separator1303.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1304 = builder.get_object('separator1304')
        self.separator1304.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_line_charts_draw_func = Performance.performance_line_charts_draw_func
        self.performance_line_charts_enter_notify_event_func = Performance.performance_line_charts_enter_notify_event_func
        self.performance_line_charts_leave_notify_event_func = Performance.performance_line_charts_leave_notify_event_func
        self.performance_line_charts_motion_notify_event_func = Performance.performance_line_charts_motion_notify_event_func
        self.performance_bar_charts_draw_func = Performance.performance_bar_charts_draw_func

        # Connect GUI signals
        self.button1301.connect("clicked", self.on_button1301_clicked)
        self.drawingarea1301.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea1301.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea1301.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea1301.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)
        self.drawingarea1302.connect("draw", self.performance_bar_charts_draw_func)
        self.eventbox1301.connect("button-release-event", self.on_eventbox1301_button_release_event)

        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea1301.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)

        # "0" value of "initial_already_run" variable means that initial function is not run before or tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1301_clicked(self, widget):

        from DiskMenu import DiskMenu
        DiskMenu.popover1301p.set_relative_to(widget)
        DiskMenu.popover1301p.set_position(1)
        DiskMenu.popover1301p.popup()


    # ----------------------- Called for opening Disk Details Window -----------------------
    def on_eventbox1301_button_release_event(self, widget, event):

        if event.button == 1:
            from DiskDetails import DiskDetails
            DiskDetails.window1301w.show()


    # ----------------------------------- Disk - Initial Function -----------------------------------
    def disk_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

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
        disk_mount_point = self.disk_mount_point_func(selected_disk)
        if_system_disk = self.disk_if_system_disk_func(selected_disk)


        # Show information on labels.
        self.label1301.set_text(disk_device_model_name)
        self.label1302.set_text(f'{selected_disk} ({disk_type})')
        self.label1307.set_text(if_system_disk)

        self.initial_already_run = 1


    # ----------------------------------- Disk - Get Disk Data Function -----------------------------------
    def disk_loop_func(self):

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

        self.drawingarea1301.queue_draw()
        self.drawingarea1302.queue_draw()

        # Run "main_gui_device_selection_list_func" if selected device list is changed since the last loop.
        disk_list_system_ordered = Performance.disk_list_system_ordered
        try:                                                                                      
            if self.disk_list_system_ordered_prev != disk_list_system_ordered:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_list_system_ordered_prev = disk_list_system_ordered

        # Run "main_gui_device_selection_list_func" if "hide_loop_ramdisk_zram_disks" option is changed since the last loop.
        hide_loop_ramdisk_zram_disks = Config.hide_loop_ramdisk_zram_disks
        try:                                                                                      
            if self.hide_loop_ramdisk_zram_disks_prev != hide_loop_ramdisk_zram_disks:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
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

        # Get content of "/proc/mounts" file which is used by Disk and DiskDetails modules.
        with open("/proc/mounts") as reader:
            self.proc_mounts_output_lines = reader.read().strip().split("\n")


        # Get information.
        disk_read_data, disk_write_data = self.disk_read_write_data_func(selected_disk, disk_list)
        disk_mount_point = self.disk_mount_point_func(selected_disk)
        disk_capacity, disk_size, disk_available, disk_free, disk_used, self.disk_usage_percent = self.disk_disk_capacity_size_available_free_used_usage_percent_func(disk_mount_point)


        # Show information on labels.
        self.label1303.set_text(f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_read_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.label1304.set_text(f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_write_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.label1305.set_text(self.performance_data_unit_converter_func("data", "none", disk_read_data, performance_disk_data_unit, performance_disk_data_precision))
        self.label1306.set_text(self.performance_data_unit_converter_func("data", "none", disk_write_data, performance_disk_data_unit, performance_disk_data_precision))
        if disk_mount_point != "-":
            self.label1308.set_text(f'{self.disk_usage_percent:.0f}%')
        if disk_mount_point == "-":
            self.label1308.set_text("-%")
        self.label1309.set_text(self.performance_data_unit_converter_func("data", "none", disk_available, performance_disk_data_unit, performance_disk_data_precision))
        self.label1310.set_text(self.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision))
        self.label1311.set_text(self.performance_data_unit_converter_func("data", "none", disk_size, performance_disk_data_unit, performance_disk_data_precision))


    # ----------------------- Get disk type (Disk or Partition) -----------------------
    def disk_type_func(self, selected_disk):

        with open("/sys/class/block/" + selected_disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")

        for line in sys_class_block_disk_uevent_lines:
            if "DEVTYPE" in line:
                disk_type = _tr(line.split("=")[1].capitalize())
                break

        return disk_type


    # ----------------------- Get disk parent name -----------------------
    def disk_parent_name_func(self, selected_disk, disk_type, disk_list):

        disk_parent_name = "-"
        if disk_type == _tr("Partition"):
            for check_disk_dir in disk_list:
                if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk) == True:
                    disk_parent_name = check_disk_dir

        return disk_parent_name


    # ----------------------- Get disk vendor and model -----------------------
    def disk_device_model_name_func(self, selected_disk, disk_type, disk_parent_name):

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
            device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass
        # Try to get device vendor model if this is a SCSI, IDE or virtio device (on QEMU virtual machines).
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
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


    # ----------------------- Get disk mount point -----------------------
    def disk_mount_point_func(self, selected_disk):

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


    # ----------------------- Get if system disk -----------------------
    def disk_if_system_disk_func(self, selected_disk):

        if selected_disk in Performance.system_disk_list:
            if_system_disk = _tr("Yes")
        else:
            if_system_disk = _tr("No")

        return if_system_disk


    # ----------------------- Get disk file system -----------------------
    def disk_file_system_func(self, selected_disk):

        disk_file_system = _tr("[Not mounted]")
        for line in self.proc_mounts_output_lines:
            if line.split()[0].strip() == ("/dev/" + selected_disk):
                disk_file_system = line.split()[2].strip()
                break

        if disk_file_system == _tr("[Not mounted]"):
            # Show "[SWAP]" information for swap disks (if selected swap area is partition (not file))
            with open("/proc/swaps") as reader:
                proc_swaps_output_lines = reader.read().strip().split("\n")
            swap_disk_list = []
            for line in proc_swaps_output_lines:
                if line.split()[1].strip() == "partition":
                    swap_disk_list.append(line.split()[0].strip().split("/")[-1])
            if len(swap_disk_list) > 0 and selected_disk in swap_disk_list:
                disk_file_system = "[" + _tr("Swap").upper() + "]"

        # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
        if disk_file_system  == "fuseblk":
            try:
                disk_for_file_system = "/dev/" + selected_disk
                disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
            except Exception:
                pass

        return disk_file_system


    # ----------------------- Get disk read data and disk write data -----------------------
    def disk_read_write_data_func(self, selected_disk, disk_list):

        disk_read_data = Performance.disk_read_data[disk_list.index(selected_disk)]
        disk_write_data = Performance.disk_write_data[disk_list.index(selected_disk)]

        return disk_read_data, disk_write_data


    # ----------------------- Get disk capacity, size, disk_available, disk_free, disk_used, disk_usage_percent -----------------------
    def disk_disk_capacity_size_available_free_used_usage_percent_func(self, disk_mount_point):

        if disk_mount_point != "-":
            # Values are calculated for filesystem size values (as df command does). lsblk command shows values of mass storage.
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_capacity = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_used = disk_size - disk_free
            # Gives same result with "lsblk" command
            #self.disk_usage_percent = disk_used / disk_size * 100
            # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values. This is real usage percent.
            self.disk_usage_percent = disk_used / (disk_available + disk_used) * 100

        if disk_mount_point == "-":
            disk_capacity = _tr("[Not mounted]")
            disk_size = _tr("[Not mounted]")
            disk_available = _tr("[Not mounted]")
            disk_free = _tr("[Not mounted]")
            disk_used = _tr("[Not mounted]")
            self.disk_usage_percent = 0

        return disk_capacity, disk_size, disk_available, disk_free, disk_used, self.disk_usage_percent


    # ----------------------- Get disk capacity (mass storage) -----------------------
    def disk_capacity_mass_storage_func(self, selected_disk, disk_mount_point, disk_sector_size):

        with open("/sys/class/block/" + selected_disk + "/size") as reader:
            disk_capacity_mass_storage = int(reader.read()) * disk_sector_size

        return disk_capacity_mass_storage


    # ----------------------- Get disk label -----------------------
    def disk_label_func(self, selected_disk):

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


    # ----------------------- Update disk usage percentages on disk list between Performance tab sub-tabs -----------------------
    def disk_update_disk_usage_percentages_on_disk_list_func(self):

        # Get disk usage percentages.
        device_list = Performance.disk_list_system_ordered
        disk_usage_percentage_list = []
        for device in device_list:
            disk_mount_point = self.disk_mount_point_func(device)
            _, _, _, _, _, disk_usage_percent = self.disk_disk_capacity_size_available_free_used_usage_percent_func(disk_mount_point)
            # Append percentage number with no fractions in order to avoid updating the list very frequently.
            disk_usage_percentage_list.append(f'{disk_usage_percent:.0f}')

        # Update disk usage percentages on disk list if disk usage percentages are changed since the last loop.
        try:                                                                                      
            if self.disk_usage_percentage_list_prev != disk_usage_percentage_list:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_usage_percentage_list_prev = disk_usage_percentage_list


# Generate object
Disk = Disk()

