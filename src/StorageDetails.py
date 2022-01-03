#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Details Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_details_import_func():

    global Gtk, GLib, os, subprocess, datetime

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    import subprocess
    from datetime import datetime


    global Config, Storage, MainGUI
    import Config, Storage, MainGUI


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Storage - Storage Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Storage Details" window GUI objects and functions/signals) -----------------------------------
def storage_details_gui_function():

    # Storage Details window GUI objects
    global builder4101w, window4101w
    global label4101w, label4102w, label4103w, label4104w, label4105w, label4106w, label4107w, label4108w, label4109w, label4110w
    global label4111w, label4112w, label4113w, label4114w, label4115w, label4116w, label4117w, label4118w, label4119w, label4120w
    global label4121w, label4122w, label4123w, label4124w


    # Storage Details window GUI objects - get
    builder4101w = Gtk.Builder()
    builder4101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageDetailsWindow.ui")

    window4101w = builder4101w.get_object('window4101w')


    # Storage Details window GUI objects
    label4101w = builder4101w.get_object('label4101w')
    label4102w = builder4101w.get_object('label4102w')
    label4103w = builder4101w.get_object('label4103w')
    label4104w = builder4101w.get_object('label4104w')
    label4105w = builder4101w.get_object('label4105w')
    label4106w = builder4101w.get_object('label4106w')
    label4107w = builder4101w.get_object('label4107w')
    label4108w = builder4101w.get_object('label4108w')
    label4109w = builder4101w.get_object('label4109w')
    label4110w = builder4101w.get_object('label4110w')
    label4111w = builder4101w.get_object('label4111w')
    label4112w = builder4101w.get_object('label4112w')
    label4113w = builder4101w.get_object('label4113w')
    label4114w = builder4101w.get_object('label4114w')
    label4115w = builder4101w.get_object('label4115w')
    label4116w = builder4101w.get_object('label4116w')
    label4117w = builder4101w.get_object('label4117w')
    label4118w = builder4101w.get_object('label4118w')
    label4119w = builder4101w.get_object('label4119w')
    label4120w = builder4101w.get_object('label4120w')
    label4121w = builder4101w.get_object('label4121w')
    label4122w = builder4101w.get_object('label4122w')
    label4123w = builder4101w.get_object('label4123w')
    label4124w = builder4101w.get_object('label4124w')


    # Storage Details window GUI functions
    def on_window4101w_delete_event(widget, event):
        window4101w.hide()
        return True

    def on_window4101w_show(widget):
        try:
            global update_interval
            del update_interval                                                               # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous process (if it was viewed) will be used.
        except NameError:
            pass
        storage_details_gui_reset_function()    # Call this function in order to reset Storage Details window. Data from previous storage/disk remains visible (for a short time) until getting and showing new storage/disk data if window is closed and opened for an another storage/disk because window is made hidden when close button is clicked.


    # Storage Details window GUI functions - connect
    window4101w.connect("delete-event", on_window4101w_delete_event)
    window4101w.connect("show", on_window4101w_show)


# ----------------------------------- Storage - Storage Details Window GUI Reset Function (resets Storage Details window) -----------------------------------
def storage_details_gui_reset_function():
    label4101w.set_text("--")
    label4102w.set_text("--")
    label4103w.set_text("--")
    label4104w.set_text("--")
    label4105w.set_text("--")
    label4106w.set_text("--")
    label4107w.set_text("--")
    label4108w.set_text("--")
    label4109w.set_text("--")
    label4110w.set_text("--")
    label4111w.set_text("--")
    label4112w.set_text("--")
    label4113w.set_text("--")
    label4114w.set_text("--")
    label4115w.set_text("--")
    label4116w.set_text("--")
    label4117w.set_text("--")
    label4118w.set_text("--")
    label4119w.set_text("--")
    label4120w.set_text("--")
    label4121w.set_text("--")
    label4122w.set_text("--")
    label4123w.set_text("--")
    label4124w.set_text("--")


# # ----------------------------------- Storage - Storage Details Tab Switch Control Function (controls if tab is switched and updates data on the last opened tab immediately without waiting end of the update interval. Signals of notebook for tab switching is not useful because it performs the action and after that it switches the tab. Data updating function does not recognizes tab switch due to this reason.) -----------------------------------
# def storage_details_tab_switch_control_func():
# 
#     global previous_page
#     if 'previous_page' not in globals():                                                      # For avoiding errors in the first loop of the control
#         previous_page = None
#         current_page = None
#     current_page = notebook4101w.get_current_page()
#     if current_page != previous_page and previous_page != None:                               # Check if tab is switched
#         StorageDetails.storage_details_foreground_func()                                      # Update the data on the tab
#     previous_page = current_page
#     if window4101w.get_visible() == True:
#         GLib.timeout_add(200, storage_details_tab_switch_control_func)                        # Check is performed in every 200 ms which is small enough for immediate update and not very frequent for avoiding high CPU usages.


# ----------------------------------- Storage - Storage Details Function (the code of this module in order to avoid running them during module import and defines "Storage" tab GUI objects and functions/signals) -----------------------------------
def storage_details_initial_func():

    storage_define_data_unit_converter_variables_func()                                       # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global disk_sector_size
    disk_sector_size = 512                                                                    # Disk data values from "/sys/class/block/[DISK_NAME]/" are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).

    global storage_image_ssd_hdd, storage_image_removable, storage_image_optical, storage_image_partition
    storage_image_ssd_hdd = "system-monitoring-center-disk-hdd-symbolic"
    storage_image_removable = "system-monitoring-center-disk-removable-symbolic"
    storage_image_optical = "system-monitoring-center-disk-optical-symbolic"
    storage_image_partition = "system-monitoring-center-disk-partition-symbolic"


# ----------------------------------- Storage - Storage Details Foreground Function (updates the process data on the "Storage Details" window) -----------------------------------
def storage_details_loop_func():

    global disk
    disk = Storage.selected_storage_kernel_name                                            # Get right clicked disk name

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global storage_disk_usage_data_precision, storage_disk_usage_data_unit
    storage_disk_usage_data_precision = Config.storage_disk_usage_data_precision
    storage_disk_usage_data_unit = Config.storage_disk_usage_data_unit

    # Get all disks (disks and partitions) including physical, optical and virtual disks
    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().split("\n")[2:-1]                               # Get without first 2 lines (header line and an empty line).
    disk_list = []
    for line in proc_partitions_lines:
        disk_list.append(line.split()[3])                                                     # Get disk list.    
    # Get disk path, mount point, file system and mode information
    with open("/proc/mounts") as reader:
        proc_mounts_lines = reader.read().strip().split("\n")
    # Get swap disk information
    with open("/proc/swaps") as reader:
        proc_swaps_lines = reader.read().split("\n")[1:-1]                                    # Get without first line (header line).
    swap_disk_list = []
    for line in proc_swaps_lines:
        swap_disk_list.append(line.split()[0].split("/")[-1])
    # Get disk device path
    disk_device_path_list = os.listdir("/dev/disk/by-path/")                                  # Some disks (such as zram0, zram1, etc. swap partitions) may not be present in "/dev/disk/by-path/" path.
    disk_device_path_disk_list = []
    for disk_device_path in disk_device_path_list:
        disk_device_path_disk_list.append(os.path.realpath("/dev/disk/by-path/" + disk_device_path).split("/")[-1])    # "os.readlink()" does not work with "/dev/disk/[folder_name]/[file_name]" files. "os.path.realpath()" is used for getting path.

    # Get disk specific data
    try:
        with open("/sys/class/block/" + disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")
    except FileNotFoundError:
        window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk symbol
    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            disk_type = _tr(line.split("=")[1].capitalize())                                  # "_tr()" is used for using translated strings (disk/partition)
            break
    disk_symbol = storage_image_ssd_hdd                                                       # Initial value of "disk_symbol" variable. This value will be used if disk type could not be detected. The same value is also used for non-USB and non-optical drives.
    if disk_type == _tr("Disk"):                                                              # "_tr()" is used for using translated strings (disk/partition)
        if disk not in disk_device_path_disk_list:                                            # This condition is used first in order to vaoid errors because of the "elif "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:" condition. Because some disks (such as zeam0, zram1, etc.) may not present in "/dev/disk/by-path/" path and in "disk_device_path_disk_list" list.
            disk_symbol = storage_image_ssd_hdd
        elif "loop" in disk or "sr" in disk:                                                  # Optical symbol is used as disk symbol if disk type is "disk (not partition)" and disk is a virtual disk or physical optical disk.
            disk_symbol = storage_image_optical
        elif "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
            disk_symbol = storage_image_removable
        else:
            disk_symbol = storage_image_ssd_hdd
    if disk_type == _tr("Partition"):                                                         # Same symbol image is used for all disk partitions.
        disk_symbol = storage_image_partition
    disk_physical_type = disk_symbol                                                          # Get disk type

    # Set Storage Details window title and window icon image
    window4101w.set_title(_tr("Storage Details") + ": " + disk)                               # Set window title
    window4101w.set_icon_name(disk_symbol)                                                    # Set StorageDetails window icon

    # Get disk parent name
    disk_parent_name = "-"                                                                    # Initial value of "disk_parent_name" variable. This value will be used if disk has no parent disk or disk parent name could not be detected.
    if disk_type == _tr("Partition"):
        for check_disk_dir in disk_list:
            if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + disk) == True:
                disk_parent_name = check_disk_dir
    # Get disk mount point which will be used for getting disk free, used spaces, used space percentage and also will be shown on the label as "disk mount point" information.
    disk_mount_point = _tr("[Not mounted]")                                                   # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
    for line in proc_mounts_lines:
        line_split = line.split()
        if line_split[0].split("/")[-1] == disk:
            disk_mount_point = bytes(line_split[1], "utf-8").decode("unicode_escape")         # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
    # Get if disk is system disk information
    disk_system_disk = _tr("No")                                                              # Initial value of "disk_system_disk" variable. This value will be used if disk mount point is not "/".
    for line in proc_mounts_lines:
        line_split = line.split()
        if line_split[0].split("/")[-1] == disk and line_split[1] == "/":
            disk_system_disk = _tr("Yes")
            break
    # Get disk transport type
    disk_transport_type = "-"                                                                 # Initial value of "disk_transport_type" variable. This value will be used if disk transport type could not be detected.
    if disk in disk_device_path_disk_list:
        if "-ata-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
            disk_transport_type = "SATA"
        if "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
            disk_transport_type = "USB"
    # Get disk file system
    disk_file_system = "-"                                                                    # Initial value of "disk_file_system" variable. This value will be used if disk file system could not be detected.
    for line in proc_mounts_lines:
        line_split = line.split()
        if line_split[0].split("/")[-1] == disk:
            disk_file_system = line_split[2]
    if disk_file_system  == "fuseblk":                                                        # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
        try:
            disk_for_file_system = "/dev/" + disk
            disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
        except:
            pass
    if disk in swap_disk_list:
        disk_file_system = _tr("[SWAP]")
    # Get disk total size
    try:
        with open("/sys/class/block/" + disk + "/size") as reader:
            disk_total_size = int(reader.read()) * disk_sector_size
    except FileNotFoundError:
        window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk free space
    try:
        if disk_mount_point != _tr("[Not mounted]"):
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
        else:
            disk_available = -9999                                                            # "-9999" value is used as "disk_available" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation.
    except:
        window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk used space
    try:
        if disk_mount_point != _tr("[Not mounted]"):
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_used = disk_size - disk_free
        else:
            disk_used = -9999                                                                 # "-9999" value is used as "disk_used" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation.
    except:
        window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk used space percentage
    try:
        if disk_mount_point != _tr("[Not mounted]"):
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
            # disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_used = disk_size - disk_free
            disk_usage_percent = disk_used / disk_size * 100                                  # Gives same result with "lsblk" command (mass storage values)
            # disk_usage_percent = disk_used / (disk_available + disk_used) * 100             # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values (same with "df" command output values). This is real usage percent.
        else:
            disk_usage_percent = -9999                                                        # "-9999" value is used as "disk_usage_percent" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation.
    except:
        window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk vendor and model
    disk_vendor_model = "-"                                                                   # Initial value of "disk_vendor_model" variable. This value will be used if disk vendor and model could not be detected. The same value is also used for disk partitions.
    if disk_type == _tr("Disk"):
        try:
            with open("/sys/class/block/" + disk + "/device/vendor") as reader:
                disk_vendor = reader.read().strip()
            with open("/sys/class/block/" + disk + "/device/model") as reader:
                disk_model = reader.read().strip()
            disk_vendor_model = disk_vendor + " - " +  disk_model
        except:
            disk_vendor_model = "-"
    # Get disk label
    disk_label = "-"                                                                          # Initial value of "disk_label" variable. This value will be used if disk label could not be detected.
    try:
        disk_label_list = os.listdir("/dev/disk/by-label/")
        for label in disk_label_list:
            if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == disk:
                disk_label = bytes(label, "utf-8").decode("unicode_escape")                   # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
    except FileNotFoundError:
        pass
    # Get disk partition label
    disk_partition_label = "-"                                                                # Initial value of "disk_partition_label" variable. This value will be used if disk partition label could not be detected.
    try:
        disk_partition_label_list = os.listdir("/dev/disk/by-partlabel/")
        for label in disk_partition_label_list:
            if os.path.realpath("/dev/disk/by-partlabel/" + label).split("/")[-1] == disk:
                disk_partition_label = label
    except FileNotFoundError:
        pass
    # Get disk path
    disk_path = "-"                                                                           # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
    try:
        if os.path.exists("/dev/" + disk) == True:
            disk_path = "/dev/" + disk
    except FileNotFoundError:
        window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk revision
    disk_revision = "-"                                                                       # Initial value of "disk_revision" variable. This value will be used if disk revision could not be detected. Disk partitions do not have disk revision.
    if disk_type == _tr("Disk"):
        try:
            with open("/sys/class/block/" + disk + "/device/rev") as reader:
                disk_revision = reader.read().strip()
        except:
            pass
    # Get disk serial number
    disk_serial_number = "-"                                                                  # Initial value of "disk_serial_number" variable. This value will be used if disk serial number could not be detected.
    if disk_type == _tr("Disk"):
        disk_id_list = os.listdir("/dev/disk/by-id/")
        for id in disk_id_list:
            if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == disk and ("/dev/disk/by-id/" + id).startswith("wwn-") == False:
                disk_serial_number = id.split("-")[-1]
                if "part" in disk_serial_number:
                    disk_serial_number = id.split("-")[-2]
    # Get disk mode (rw, ro, etc.)
    disk_mode = "-"                                                                           # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
    if disk_type == _tr("Disk"):
        for line in proc_mounts_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == disk:
                disk_mode = line_split[3]
    # Get disk removable information
    disk_removable = "-"                                                                      # Initial value of "disk_removable" variable. This value will be used if disk removable information could not be detected (if disk is a partition).
    if disk_type == _tr("Disk"):
        try:
            with open("/sys/class/block/" + disk + "/removable") as reader:
                disk_removable_as_number = reader.read().strip()
        except FileNotFoundError:
            window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
        if disk_removable_as_number == "1":
            disk_removable = _tr("Yes")
        if disk_removable_as_number == "0":
            disk_removable = _tr("No")
    # Get disk rotational information
    disk_rotational = "-"                                                                     # Initial value of "disk_rotational" variable. This value will be used if disk rotational information could not be detected (if disk is a partition).
    if disk_type == _tr("Disk"):
        try:
            with open("/sys/class/block/" + disk + "/queue/rotational") as reader:
                disk_rotational_as_number = reader.read().strip()
        except FileNotFoundError:
            window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
        if disk_rotational_as_number == "1":
            disk_rotational = _tr("Yes")
        if disk_rotational_as_number == "0":
            disk_rotational = _tr("No")
    # Get disk read-only information
    disk_read_only = "-"                                                                      # Initial value of "disk_read_only" variable. This value will be used if disk read-only information could not be detected (if disk is a partition).
    if disk_type == _tr("Disk"):
        try:
            with open("/sys/class/block/" + disk + "/ro") as reader:
                disk_read_only_as_number = reader.read().strip()
        except FileNotFoundError:
            window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
        if disk_read_only_as_number == "1":
            disk_read_only = _tr("Yes")
        if disk_read_only_as_number == "0":
            disk_read_only = _tr("No")
    # Get disk UUID
    disk_uuid = "-"                                                                           # Initial value of "disk_uuid" variable. This value will be used if disk disk_uuid could not be detected (for example: if an optical drive has no disk).
    try:
        disk_uuid_list = os.listdir("/dev/disk/by-uuid/")
        for uuid in disk_uuid_list:
            if os.path.realpath("/dev/disk/by-uuid/" + uuid).split("/")[-1] == disk:
                disk_uuid = uuid
    except FileNotFoundError:
        pass
    # Get disk unique storage id
    disk_unique_storage_id = "-"                                                              # Initial value of "disk_read_only" variable. This value will be used if disk read-only information could not be detected (if disk is a virtual disk).
    try:
        disk_id_list = os.listdir("/dev/disk/by-id/")
        for id in disk_id_list:
            if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == disk and id.startswith("wwn-") == True:
                disk_unique_storage_id = id.split("wwn-")[1]
    except FileNotFoundError:
        pass
    # Get disk major:minor device number
    disk_maj_min_number = "-"                                                                 # Initial value of "disk_maj_min_number" variable. This value will be used if disk major:minor device number could not be detected.
    for line in sys_class_block_disk_uevent_lines:
        if "MAJOR=" in line:
            disk_major_number = line.split("=")[1]
        if "MINOR=" in line:
            disk_minor_number = line.split("=")[1]
            disk_maj_min_number = disk_major_number + ":" + disk_minor_number
            break

    # Set label text by using storage/disk data
    label4101w.set_text(disk)
    label4102w.set_text(disk_parent_name)
    label4103w.set_text(disk_system_disk)
    label4104w.set_text(disk_type)
    label4105w.set_text(disk_transport_type)
    label4106w.set_text(disk_file_system)
    label4107w.set_text(f'{storage_data_unit_converter_func(disk_total_size, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')
    if disk_available == -9999:
        label4108w.set_text(_tr("[Not mounted]"))
        label4109w.set_text(_tr("[Not mounted]"))
        label4110w.set_text(_tr("[Not mounted]"))
    if disk_available != -9999:
        label4108w.set_text(f'{storage_data_unit_converter_func(disk_available, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')
        label4109w.set_text(f'{storage_data_unit_converter_func(disk_used, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')
        label4110w.set_text(f'{disk_usage_percent:.1f}%')
    label4111w.set_text(disk_vendor_model)
    label4112w.set_text(disk_label)
    label4113w.set_text(disk_partition_label)
    label4114w.set_text(disk_mount_point)
    label4115w.set_text(disk_path)
    label4116w.set_text(disk_revision)
    label4117w.set_text(disk_serial_number)
    label4118w.set_text(disk_mode)
    label4119w.set_text(disk_removable)
    label4120w.set_text(disk_rotational)
    label4121w.set_text(disk_read_only)
    label4122w.set_text(disk_uuid)
    label4123w.set_text(disk_unique_storage_id)
    label4124w.set_text(disk_maj_min_number)


# ----------------------------------- Storage Details Run Function (runs initial and loop functions) -----------------------------------
def storage_details_run_func():

    if "update_interval" not in globals():
        GLib.idle_add(storage_details_initial_func)
    if window4101w.get_visible() is True:
        GLib.idle_add(storage_details_loop_func)
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, storage_details_run_func)

# ----------------------------------- Storage - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def storage_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Storage - Data Details Unit Converter Function (converts byte and bit data units) -----------------------------------
def storage_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit >= 8:
        data = data * 8
    if unit in [0, 8]:
        unit_counter = unit + 1
        while data > 1024:
            unit_counter = unit_counter + 1
            data = data/1024
        unit = data_unit_list[unit_counter][2]
        if data == 0:
            precision = 0
        return f'{data:.{precision}f} {unit}'

    data = data / data_unit_list[unit][1]
    unit = data_unit_list[unit][2]
    if data == 0:
        precision = 0
    return f'{data:.{precision}f} {unit}'


# ----------------------------------- Storage - Storage Details No Such Storage Error Dialog Function (shows an error dialog and stops updating the "Storage Details window" when the storage/disk is not connected anymore) -----------------------------------
def storage_no_such_storage_error_dialog():

    error_dialog4101w = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Disk Is Not Connected Anymore"), )
    error_dialog4101w.format_secondary_text(_tr("Following disk is not connected anymore and storage details window is closed automatically:") + "\n\n    " + disk)
    error_dialog4101w.run()
    error_dialog4101w.destroy()
