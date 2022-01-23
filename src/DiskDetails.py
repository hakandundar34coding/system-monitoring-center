#!/usr/bin/env python3

# ----------------------------------- Disk - Disk Details Import Function -----------------------------------
def disk_details_import_func():

    global Gtk, GLib, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    import subprocess


    global Config, Disk, MainGUI
    import Config, Disk, MainGUI


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Disk - Disk Details Window GUI Function -----------------------------------
def disk_details_gui_func():

    # Disk Details window GUI objects
    global builder1301w, window1301w
    global label1301w, label1302w, label1303w, label1304w, label1305w, label1306w, label1307w, label1308w, label1309w, label1310w
    global label1311w, label1312w, label1313w, label1314w, label1315w, label1316w, label1317w, label1322w


    # Disk Details window GUI objects - get
    builder1301w = Gtk.Builder()
    builder1301w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskDetailsWindow.ui")

    window1301w = builder1301w.get_object('window1301w')


    # Disk Details window GUI objects
    label1301w = builder1301w.get_object('label1301w')
    label1302w = builder1301w.get_object('label1302w')
    label1303w = builder1301w.get_object('label1303w')
    label1304w = builder1301w.get_object('label1304w')
    label1305w = builder1301w.get_object('label1305w')
    label1306w = builder1301w.get_object('label1306w')
    label1307w = builder1301w.get_object('label1307w')
    label1308w = builder1301w.get_object('label1308w')
    label1309w = builder1301w.get_object('label1309w')
    label1310w = builder1301w.get_object('label1310w')
    label1311w = builder1301w.get_object('label1311w')
    label1312w = builder1301w.get_object('label1312w')
    label1313w = builder1301w.get_object('label1313w')
    label1314w = builder1301w.get_object('label1314w')
    label1315w = builder1301w.get_object('label1315w')
    label1316w = builder1301w.get_object('label1316w')
    label1317w = builder1301w.get_object('label1317w')
    label1322w = builder1301w.get_object('label1322w')


    # Disk Details window GUI functions
    def on_window1301w_delete_event(widget, event):
        window1301w.hide()
        return True

    def on_window1301w_show(widget):
        try:
            global update_interval
            del update_interval                                                               # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous process (if it was viewed) will be used.
        except NameError:
            pass
        disk_details_gui_reset_func()                                                         # Call this function in order to reset Disk Details window. Data from previous storage/disk remains visible (for a short time) until getting and showing new storage/disk data if window is closed and opened for an another storage/disk because window is made hidden when close button is clicked.


    # Disk Details window GUI functions - connect
    window1301w.connect("delete-event", on_window1301w_delete_event)
    window1301w.connect("show", on_window1301w_show)


# ----------------------------------- Disk - Disk Details Window GUI Reset Function -----------------------------------
def disk_details_gui_reset_func():
    label1301w.set_text("--")
    label1302w.set_text("--")
    label1303w.set_text("--")
    label1304w.set_text("--")
    label1305w.set_text("--")
    label1306w.set_text("--")
    label1307w.set_text("--")
    label1308w.set_text("--")
    label1309w.set_text("--")
    label1310w.set_text("--")
    label1311w.set_text("--")
    label1312w.set_text("--")
    label1313w.set_text("--")
    label1314w.set_text("--")
    label1315w.set_text("--")
    label1316w.set_text("--")
    label1317w.set_text("--")
    label1322w.set_text("--")


# ----------------------------------- Disk - Disk Details Function -----------------------------------
def disk_details_initial_func():

    disk_define_data_unit_converter_variables_func()                                          # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global disk_sector_size
    disk_sector_size = 512                                                                    # Disk data values from "/sys/class/block/[DISK_NAME]/" are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).


# ----------------------------------- Disk - Disk Details Foreground Function -----------------------------------
def disk_details_loop_func():

    global disk
    disk = Disk.selected_disk                                                                 # Get right clicked disk name

    # Set Disk Details window title
    window1301w.set_title(_tr("Disk Details") + ": " + disk)                                  # Set window title

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global performance_disk_usage_data_precision, performance_disk_usage_data_unit
    performance_disk_usage_data_precision = Config.performance_disk_usage_data_precision
    performance_disk_usage_data_unit = Config.performance_disk_usage_data_unit

    # Get all disks (disks and partitions)
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
        window1301w.hide()
        return
    # Get disk type
    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            disk_type = _tr(line.split("=")[1].capitalize())                                  # "_tr()" is used for using translated strings (disk/partition)
            break
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
    disk_in_proc_mounts_lines = "no"                                                          # This variable (initial value) is defined here because system disk may not be detected by checking if mount point is "/" on some systems such as some ARM devices. "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
    for line in proc_mounts_lines:
        line_split = line.split(" ", 2)
        if line_split[0].split("/")[-1] == disk:
            disk_in_proc_mounts_lines = "yes"
            if line_split[1] == "/":
                disk_system_disk = _tr("Yes")
                break
    if disk_in_proc_mounts_lines == "no":
        for line in proc_mounts_lines:
            line_split = line.split(" ", 1)
            if line_split[0] == "dev/root":
                with open("/proc/cmdline") as reader:
                    proc_cmdline = reader.read()
                if "root=UUID=" in proc_cmdline:
                    disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                    system_disk = os.path.realpath("/dev/disk/by-uuid/" + disk_uuid_partuuid).split("/")[-1].strip()
                if "root=PARTUUID=" in proc_cmdline:
                    disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                    system_disk = os.path.realpath("/dev/disk/by-partuuid/" + disk_uuid_partuuid).split("/")[-1].strip()
                if system_disk == disk:
                    disk_system_disk = _tr("Yes")
    # Get disk file system
    disk_file_system = _tr("[Not mounted]")                                                   # Initial value of the variable.
    for line in proc_mounts_lines:
        if line.split()[0].strip() == ("/dev/" + disk):
            disk_file_system = line.split()[2].strip()
            break
    if disk_file_system == _tr("[Not mounted]"):
        with open("/proc/swaps") as reader:                                                   # Show "[SWAP]" information for swap disks (if selected swap area is partition (not file))
            proc_swaps_output_lines = reader.read().strip().split("\n")
        swap_disk_list = []
        for line in proc_swaps_output_lines:
            if line.split()[1].strip() == "partition":
                swap_disk_list.append(line.split()[0].strip().split("/")[-1])
        if len(swap_disk_list) > 0 and disk in swap_disk_list:
            disk_file_system = _tr("[SWAP]")
    if disk_file_system  == "fuseblk":                                                        # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
        try:
            disk_for_file_system = "/dev/" + disk
            disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
        except:
            pass
    # Get disk capacity (mass storage)
    try:
        with open("/sys/class/block/" + disk + "/size") as reader:
            disk_capacity_mass_storage = int(reader.read()) * disk_sector_size
    except FileNotFoundError:
        window1301w.hide()
        return
    # Get disk capacity, free, available and used space
    try:
        if disk_mount_point != _tr("[Not mounted]"):
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_capacity = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
            disk_used = disk_capacity - disk_free
            disk_usage_percent = disk_used / (disk_available + disk_used) * 100               # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values (same with "df" command output values). This is real usage percent.
            disk_usage_percent_mass_storage = disk_used / disk_capacity * 100                 # Gives same result with "lsblk" command (mass storage values)
        else:
            disk_available = -9999                                                            # "-9999" value is used as "disk_available" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation.
            disk_used = -9999
            disk_usage_percent = -9999
            disk_usage_percent_mass_storage = -9999
    except:
        window1301w.hide()
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
        window1301w.hide()
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
    # Get disk UUID
    disk_uuid = "-"                                                                           # Initial value of "disk_uuid" variable. This value will be used if disk disk_uuid could not be detected (for example: if an optical drive has no disk).
    try:
        disk_uuid_list = os.listdir("/dev/disk/by-uuid/")
        for uuid in disk_uuid_list:
            if os.path.realpath("/dev/disk/by-uuid/" + uuid).split("/")[-1] == disk:
                disk_uuid = uuid
    except FileNotFoundError:
        pass

    # Set label text by using storage/disk data
    label1301w.set_text(disk)
    label1302w.set_text(disk_parent_name)
    label1303w.set_text(disk_system_disk)
    label1304w.set_text(disk_type)
    label1305w.set_text(f'{disk_data_unit_converter_func(disk_capacity_mass_storage, performance_disk_usage_data_unit, performance_disk_usage_data_precision)}')
    label1306w.set_text(disk_file_system)
    if disk_available == -9999:
        label1307w.set_text(_tr("[Not mounted]"))
        label1308w.set_text(_tr("[Not mounted]"))
        label1309w.set_text(_tr("[Not mounted]"))
        label1310w.set_text(_tr("[Not mounted]"))
    if disk_available != -9999:
        label1307w.set_text(f'{disk_data_unit_converter_func(disk_capacity, performance_disk_usage_data_unit, performance_disk_usage_data_precision)}')
        label1308w.set_text(f'{disk_data_unit_converter_func(disk_available, performance_disk_usage_data_unit, performance_disk_usage_data_precision)}')
        label1309w.set_text(f'{disk_data_unit_converter_func(disk_used, performance_disk_usage_data_unit, performance_disk_usage_data_precision)} - {disk_usage_percent:.1f}%')
        label1310w.set_text(f'{disk_usage_percent_mass_storage:.1f}%')
    label1311w.set_text(disk_vendor_model)
    label1312w.set_text(disk_label)
    label1313w.set_text(disk_partition_label)
    label1314w.set_text(disk_mount_point)
    label1315w.set_text(disk_path)
    label1316w.set_text(disk_revision)
    label1317w.set_text(disk_serial_number)
    label1322w.set_text(disk_uuid)


# ----------------------------------- Disk Details - Run Function -----------------------------------
def disk_details_run_func():

    if "update_interval" not in globals():
        GLib.idle_add(disk_details_initial_func)
    if window1301w.get_visible() is True:
        GLib.idle_add(disk_details_loop_func)
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, disk_details_run_func)


# ----------------------------------- Disk - Define Data Unit Converter Variables Function -----------------------------------
def disk_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Disk - Data Details Unit Converter Function -----------------------------------
def disk_data_unit_converter_func(data, unit, precision):

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
