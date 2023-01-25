#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance


class Disk:

    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskTab.ui")

        # Get GUI objects
        self.grid1301 = builder.get_object('grid1301')
        self.drawingarea1301 = builder.get_object('drawingarea1301')
        self.drawingarea1302 = builder.get_object('drawingarea1302')
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
        self.drawingarea1301.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea1301.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea1301.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea1301.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)
        self.drawingarea1302.connect("draw", self.performance_bar_charts_draw_func)
        self.eventbox1301.connect("button-release-event", self.on_eventbox1301_button_release_event)
        self.eventbox1301.connect("enter-notify-event", self.on_eventbox1301_button_enter_notify_event)
        self.eventbox1301.connect("leave-notify-event", self.on_eventbox1301_button_leave_notify_event)

        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea1301.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)

        # "0" value of "initial_already_run" variable means that initial function is not run before or tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    # ----------------------- Called for opening Disk Details Window -----------------------
    def on_eventbox1301_button_release_event(self, widget, event):

        if event.button == 1:
            from DiskDetails import DiskDetails
            DiskDetails.window1301w.show()


    def on_eventbox1301_button_enter_notify_event(self, widget, event):
        """
        Set mouse cursor (pointer) when it is moved inside of the eventbox of "Show..." label.
        """

        cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "pointer")
        window = Gdk.Window.at_pointer()[0]
        try:
            window.set_cursor(cursor)
        except Exception:
            pass


    def on_eventbox1301_button_leave_notify_event(self, widget, event):
        """
        Set mouse cursor (default) when it is moved outside of the eventbox of "Show..." label.
        """

        cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "default")
        window = Gdk.Window.at_pointer()[0]
        try:
            window.set_cursor(cursor)
        except Exception:
            pass


    # ----------------------------------- Disk - Initial Function -----------------------------------
    def disk_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

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
        disk_type = self.disk_type_func(selected_disk)
        disk_parent_name = self.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_device_model_name = self.disk_device_model_name_func(selected_disk, disk_type, disk_parent_name)
        if_system_disk = self.disk_if_system_disk_func(selected_disk)


        # Show information on labels.
        self.label1301.set_text(disk_device_model_name)
        self.label1302.set_text(f'{selected_disk}  ({disk_type})')
        self.label1307.set_text(if_system_disk)

        self.initial_already_run = 1


    # ----------------------------------- Disk - Get Disk Data Function -----------------------------------
    def disk_loop_func(self):

        disk_list = Performance.disk_list
        selected_disk = Performance.selected_disk
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
        disk_list = Performance.disk_list
        try:                                                                                      
            if self.disk_list_prev != disk_list:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_list_prev = disk_list

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


        # Get information.
        disk_read_data, disk_write_data = self.disk_read_write_data_func(selected_disk)
        disk_file_system_information = self.disk_file_system_information_func(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, self.disk_usage_percentage, disk_mount_point  = self.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_file_system_information, disk_list, selected_disk)


        # Show information on labels.
        self.label1303.set_text(f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_read_speed[selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.label1304.set_text(f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_write_speed[selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.label1305.set_text(self.performance_data_unit_converter_func("data", "none", disk_read_data, performance_disk_data_unit, performance_disk_data_precision))
        self.label1306.set_text(self.performance_data_unit_converter_func("data", "none", disk_write_data, performance_disk_data_unit, performance_disk_data_precision))
        if disk_mount_point != "-":
            self.label1308.set_text(f'{self.disk_usage_percentage:.0f}%')
        if disk_mount_point == "-":
            self.label1308.set_text("-%")
        self.label1309.set_text(self.performance_data_unit_converter_func("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision))
        self.label1310.set_text(self.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision))
        self.label1311.set_text(self.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision))


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
        disk_device_model_name = "-"

        # Get device vendor model if this is a NVMe SSD.
        # These disks do not have "modalias" or "vendor" files under "/sys/class/block/" + selected_disk + "/device" directory.
        if os.path.isdir("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/") == True:
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/modalias") as reader:
                    modalias_output = reader.read().strip()
                device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
            except (FileNotFoundError, NotADirectoryError) as me:
                pass

            if "-" not in [device_vendor_name, device_model_name] or "Unknown" not in [device_vendor_name, device_model_name]:
                disk_device_model_name = f'{device_vendor_name} - {device_model_name}'

            # Get device vendor-model if this is a NVMe SSD and vendor or model is not found in hardware database.
            if "-" in [device_vendor_name, device_model_name] or "Unknown" in [device_vendor_name, device_model_name]:
                device_vendor_name = "-"
                device_model_name = "-"
                try:
                    with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                        device_model_name = reader.read().strip()
                except (FileNotFoundError, NotADirectoryError) as me:
                    pass

                if device_model_name != "-":
                    disk_device_model_name = device_model_name
                else:
                    device_vendor_name = "[" + _tr("Unknown") + "]"
                    device_model_name = "[" + _tr("Unknown") + "]"
                    disk_device_model_name = f'{device_vendor_name} - {device_model_name}'

        # Get device vendor model if this is a SCSI, IDE or virtio device (on QEMU virtual machines).
        if os.path.isdir("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/") == False:
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/modalias") as reader:
                    modalias_output = reader.read().strip()
                device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
            except (FileNotFoundError, NotADirectoryError) as me:
                pass

            # Get device vendor model if this is a SCSI or IDE disk.
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
            disk_device_model_name = "[" + "zram" + "]"
            # zram disks may be used as swap disk, disk for temporary files (/tmp), etc.
            # Check if disk name is in "/proc/swaps" file in order to determine if it is used as swap disk.
            with open("/proc/swaps") as reader:
                proc_swaps_lines = reader.read().split("\n")
            # Delete header indormation which is get from "/proc/swaps" file.
            del proc_swaps_lines[0]
            for line in proc_swaps_lines:
                if line.split()[0].split("/")[-1] == selected_disk:
                    disk_device_model_name = "[" + "zram - " + _tr("Swap").upper() + "]"
                    break
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


    # ----------------------- Get file system information (file systems, capacities, used, free, used percentages and mount points) of all disks -----------------------
    def disk_file_system_information_func(self, disk_list):

        # Get file system information of the mounted disks by using "df" command.
        # Online drives are excluded from "df" command output for avoiding long command runs and GUI blockings.
        # Currently, "fuse.onedriver" filesystems (generated by Onedriver application) are excluded.
        # More filesystems can be excluded by using the parameter multiple times (comma-separated filesystems
        # for excluding are not supported by "df").
        command_list = ["df", "--exclude-type=fuse.onedriver", "--output=source,fstype,size,used,avail,pcent,target"]
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


    # ----------------------- Get file file systems, capacities, used, free, used percentages and mount points of all disks -----------------------
    def disk_file_system_capacity_used_free_used_percent_mount_point_func(self, disk_filesystem_information_list, disk_list, selected_disk):

        disk_index = disk_list.index(selected_disk)
        disk_file_system = disk_filesystem_information_list[disk_index][1]
        disk_capacity = disk_filesystem_information_list[disk_index][2]
        disk_used = disk_filesystem_information_list[disk_index][3]
        disk_free = disk_filesystem_information_list[disk_index][4]
        disk_usage_percentage = disk_filesystem_information_list[disk_index][5]
        disk_mount_point = disk_filesystem_information_list[disk_index][6]

        return disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point


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


    # ----------------------- Get disk file system if it is detected as 'fuseblk'. -----------------------
    def disk_file_system_fuseblk_func(self, selected_disk):

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


    # ----------------------- Get if system disk -----------------------
    def disk_if_system_disk_func(self, selected_disk):

        if selected_disk in Performance.system_disk_list:
            if_system_disk = _tr("Yes")
        else:
            if_system_disk = _tr("No")

        return if_system_disk


    # ----------------------- Get disk read data and disk write data -----------------------
    def disk_read_write_data_func(self, selected_disk):

        disk_io = Performance.disk_io()

        disk_read_data = disk_io[selected_disk]["read_bytes"]
        disk_write_data = disk_io[selected_disk]["write_bytes"]

        return disk_read_data, disk_write_data


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
        device_list = Performance.disk_list
        disk_usage_percentage_list = []
        for device in device_list:
            disk_filesystem_information_list = self.disk_file_system_information_func(device_list)
            _, _, _, _, disk_usage_percentage, disk_mount_point = self.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_filesystem_information_list, device_list, device)
            # Append percentage number with no fractions in order to avoid updating the list very frequently.
            disk_usage_percentage_list.append(f'{disk_usage_percentage:.0f}')

        # Update disk usage percentages on disk list if disk usage percentages are changed since the last loop.
        try:                                                                                      
            if self.disk_usage_percentage_list_prev != disk_usage_percentage_list:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_usage_percentage_list_prev = disk_usage_percentage_list


Disk = Disk()

