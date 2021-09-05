#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Details Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_details_import_func():

    global Gtk, GLib, os, Thread, subprocess, datetime

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    from threading import Thread
    import subprocess
    from datetime import datetime


    global Config, Storage, StorageGUI, StorageDetailsGUI, MainGUI
    import Config, Storage, StorageGUI, StorageDetailsGUI, MainGUI


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


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
def storage_details_foreground_func():

    global disk
    disk = StorageGUI.selected_storage_kernel_name                                            # Get right clicked disk name

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
    disk_device_path_list = os.listdir("/dev/disk/by-path/")
    disk_device_path_disk_list = []
    for disk_device_path in disk_device_path_list:
        disk_device_path_disk_list.append(os.path.realpath("/dev/disk/by-path/" + disk_device_path).split("/")[-1])    # "os.readlink()" does not work with "/dev/disk/[folder_name]/[file_name]" files. "os.path.realpath()" is used for getting path.

    # Get disk specific data
    try:
        with open("/sys/class/block/" + disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")
    except FileNotFoundError:
        StorageDetailsGUI.window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk symbol
    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            disk_type = line.split("=")[1]
            break
    disk_symbol = storage_image_ssd_hdd                                                       # Initial value of "disk_symbol" variable. This value will be used if disk type could not be detected. The same value is also used for non-USB and non-optical drives.
    if disk_type == "disk":
        if "loop" in disk or "sr" in disk:                                                    # Optical symbol is used as disk symbol if disk type is "disk (not partition)" and disk is a virtual disk or physical optical disk.
            disk_symbol = storage_image_optical
        elif "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
            disk_symbol = storage_image_removable
        else:
            disk_symbol = storage_image_ssd_hdd
    if disk_type == "partition":                                                              # Same symbol image is used for all disk partitions.
        disk_symbol = storage_image_partition
    disk_physical_type = disk_symbol                                                          # Get disk type

    # Set Storage Details window title and window icon image
    StorageDetailsGUI.window4101w.set_title(f'Storage Details: {disk}')                       # Set window title
    StorageDetailsGUI.window4101w.set_icon_name(disk_symbol)                                  # Set StorageDetails window icon

    # Get disk parent name
    disk_parent_name = "-"                                                                    # Initial value of "disk_parent_name" variable. This value will be used if disk has no parent disk or disk parent name could not be detected.
    if disk_type == "partition":
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
            disk_file_system_from_lsblk = (subprocess.check_output("lsblk -no FSTYPE /dev/" + disk, shell=True).strip()).decode()
            disk_file_system = disk_file_system + " (" + disk_file_system_from_lsblk + ")"
        except:
            pass
    if disk in swap_disk_list:
        disk_file_system = _tr("[SWAP]")
    # Get disk total size
    try:
        with open("/sys/class/block/" + disk + "/size") as reader:
            disk_size = int(reader.read()) * disk_sector_size
    except FileNotFoundError:
        StorageDetailsGUI.window4101w.hide()
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
        storage_no_such_storage_error_dialog()
        return
    # Get disk used space
    try:
        if disk_mount_point != _tr("[Not mounted]"):
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_used = disk_size - disk_free
        else:
            disk_used = -9999                                                                 # "-9999" value is used as "disk_used" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation.
    except:
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
        storage_no_such_storage_error_dialog()
        return
    # Get disk vendor and model
    disk_vendor_model = "-"                                                                   # Initial value of "disk_vendor_model" variable. This value will be used if disk vendor and model could not be detected. The same value is also used for disk partitions.
    if disk_type == "disk":
        try:
            with open("/sys/class/block/" + disk + "/device/vendor") as reader:
                disk_vendor = reader.read().strip()
            with open("/sys/class/block/" + disk + "/device/model") as reader:
                disk_model = reader.read().strip()
            disk_vendor_model = disk_vendor + "-" +  disk_model
        except FileNotFoundError:
            StorageDetailsGUI.window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
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
    disk_partition_label_list = os.listdir("/dev/disk/by-partlabel/")
    for label in disk_partition_label_list:
        if os.path.realpath("/dev/disk/by-partlabel/" + label).split("/")[-1] == disk:
            disk_partition_label = label
    # Get disk path
    disk_path = "-"                                                                           # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
    try:
        if os.path.exists("/dev/" + disk) == True:
            disk_path = "/dev/" + disk
    except FileNotFoundError:
        StorageDetailsGUI.window4101w.hide()
        storage_no_such_storage_error_dialog()
        return
    # Get disk revision
    disk_revision = "-"                                                                       # Initial value of "disk_revision" variable. This value will be used if disk revision could not be detected. Disk partitions do not have disk revision.
    if disk_type == "disk":
        try:
            with open("/sys/class/block/" + disk + "/device/rev") as reader:
                disk_revision = reader.read().strip()
        except FileNotFoundError:
            StorageDetailsGUI.window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
        except:
            pass
    # Get disk serial number
    disk_serial_number = "-"                                                                  # Initial value of "disk_serial_number" variable. This value will be used if disk serial number could not be detected.
    if disk_type == "disk":
        disk_id_list = os.listdir("/dev/disk/by-id/")
        for id in disk_id_list:
            if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == disk and ("/dev/disk/by-id/" + id).startswith("wwn-") == False:
                disk_serial_number = id.split("-")[-1]
                if "part" in disk_serial_number:
                    disk_serial_number = id.split("-")[-2]
    # Get disk mode (rw, ro, etc.)
    disk_mode = "-"                                                                           # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
    if disk_type == "disk":
        for line in proc_mounts_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == disk:
                disk_mode = line_split[3]
    # Get disk removable information
    disk_removable = "-"                                                                      # Initial value of "disk_removable" variable. This value will be used if disk removable information could not be detected (if disk is a partition).
    if disk_type == "disk":
        try:
            with open("/sys/class/block/" + disk + "/removable") as reader:
                disk_removable_as_number = reader.read().strip()
        except FileNotFoundError:
            StorageDetailsGUI.window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
        if disk_removable_as_number == "1":
            disk_removable = _tr("Yes")
        if disk_removable_as_number == "0":
            disk_removable = _tr("No")
    # Get disk rotational information
    disk_rotational = "-"                                                                     # Initial value of "disk_rotational" variable. This value will be used if disk rotational information could not be detected (if disk is a partition).
    if disk_type == "disk":
        try:
            with open("/sys/class/block/" + disk + "/queue/rotational") as reader:
                disk_rotational_as_number = reader.read().strip()
        except FileNotFoundError:
            StorageDetailsGUI.window4101w.hide()
            storage_no_such_storage_error_dialog()
            return
        if disk_rotational_as_number == "1":
            disk_rotational = _tr("Yes")
        if disk_rotational_as_number == "0":
            disk_rotational = _tr("No")
    # Get disk read-only information
    disk_read_only = "-"                                                                      # Initial value of "disk_read_only" variable. This value will be used if disk read-only information could not be detected (if disk is a partition).
    if disk_type == "disk":
        try:
            with open("/sys/class/block/" + disk + "/ro") as reader:
                disk_read_only_as_number = reader.read().strip()
        except FileNotFoundError:
            StorageDetailsGUI.window4101w.hide()
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
    StorageDetailsGUI.label4101w.set_text(disk)
    StorageDetailsGUI.label4102w.set_text(disk_parent_name)
    StorageDetailsGUI.label4103w.set_text(disk_system_disk)
    StorageDetailsGUI.label4104w.set_text(disk_type)
    StorageDetailsGUI.label4105w.set_text(disk_transport_type)
    StorageDetailsGUI.label4106w.set_text(disk_file_system)
    StorageDetailsGUI.label4107w.set_text(f'{storage_data_unit_converter_func(disk_size, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')
    if disk_available == -9999:
        StorageDetailsGUI.label4108w.set_text(_tr("[Not mounted]"))
        StorageDetailsGUI.label4109w.set_text(_tr("[Not mounted]"))
        StorageDetailsGUI.label4110w.set_text(_tr("[Not mounted]"))
    if disk_available != -9999:
        StorageDetailsGUI.label4108w.set_text(f'{storage_data_unit_converter_func(disk_available, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')
        StorageDetailsGUI.label4109w.set_text(f'{storage_data_unit_converter_func(disk_used, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')
        StorageDetailsGUI.label4110w.set_text(f'{disk_usage_percent:.1f}%')
    StorageDetailsGUI.label4111w.set_text(disk_vendor_model)
    StorageDetailsGUI.label4112w.set_text(disk_label)
    StorageDetailsGUI.label4113w.set_text(disk_partition_label)
    StorageDetailsGUI.label4114w.set_text(disk_mount_point)
    StorageDetailsGUI.label4115w.set_text(disk_path)
    StorageDetailsGUI.label4116w.set_text(disk_revision)
    StorageDetailsGUI.label4117w.set_text(disk_serial_number)
    StorageDetailsGUI.label4118w.set_text(disk_mode)
    StorageDetailsGUI.label4119w.set_text(disk_removable)
    StorageDetailsGUI.label4120w.set_text(disk_rotational)
    StorageDetailsGUI.label4121w.set_text(disk_read_only)
    StorageDetailsGUI.label4122w.set_text(disk_uuid)
    StorageDetailsGUI.label4123w.set_text(disk_unique_storage_id)
    StorageDetailsGUI.label4124w.set_text(disk_maj_min_number)


# ----------------------------------- Storage - Storage Details Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def storage_details_loop_func():

    if StorageDetailsGUI.window4101w.get_visible() is True:
        GLib.idle_add(storage_details_foreground_func)
        GLib.timeout_add(Config.update_interval * 1000, storage_details_loop_func)


# ----------------------------------- Storage Details Foreground Thread Run Function (starts execution of the threads) -----------------------------------
def storage_details_foreground_thread_run_func():

    storage_details_initial_thread = Thread(target=storage_details_initial_func, daemon=True)
    storage_details_initial_thread.start()
    storage_details_initial_thread.join()
    storage_details_loop_thread = Thread(target=storage_details_loop_func, daemon=True)
    storage_details_loop_thread.start()


# ----------------------------------- Storage - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def storage_define_data_unit_converter_variables_func():

    global data_unit_list
    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Storage - Data Details Unit Converter Function (converts byte and bit data units) -----------------------------------
def storage_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit == 0 or unit == 8:
        unit_counter = unit + 1
        while data > 1024:
            unit_counter = unit_counter + 1
            data = data/1024
        unit = data_unit_list[unit_counter][2]
        return f'{data:.{precision}f} {unit}'

    data = data / data_unit_list[unit][1]
    unit = data_unit_list[unit][2]
    return f'{data:.{precision}f} {unit}'


# ----------------------------------- Storage - Storage Details No Such Storage Error Dialog Function (shows an error dialog and stops updating the "Storage Details window" when the storage/disk is not connected anymore) -----------------------------------
def storage_no_such_storage_error_dialog():

    error_dialog4101w = Gtk.MessageDialog(transient_for=MainGUI.window1, title="Error", flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text="Disk Is Not Connected Anymore", )
    error_dialog4101w.format_secondary_text(_tr("Following disk is not connected anymore \nand storage details window is closed automatically:\n  ") + disk)
    error_dialog4101w.run()
    error_dialog4101w.destroy()
