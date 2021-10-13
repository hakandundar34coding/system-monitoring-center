#!/usr/bin/env python3

# ----------------------------------- Disk - Disk Tab GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def disk_import_func():

    global Gtk, GLib, Thread, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os


    global Config, MainGUI, Performance, DiskGUI
    import Config, MainGUI, Performance, DiskGUI


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


# ----------------------------------- Disk - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def disk_initial_func():

    disk_define_data_unit_converter_variables_func()                                          # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global disk_list, selected_disk_number                                                  # These variables are defined as global variables because they will be used in "disk_loop_func" function and also they will be used by "disk_get_device_partition_model_name_mount_point_func" function.
    disk_list = Performance.disk_list
    selected_disk_number = Performance.selected_disk_number

    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    try:
        if os.path.isdir("/sys/class/block/" + disk_list[selected_disk_number]) == False:
            return
    except:
        return
    # Get disk_model_name, parent_disk, disk_mount_point
    disk_get_device_partition_model_name_mount_point_func()
    # Get disk_file_system
    with open("/proc/mounts") as reader:                                                      # Get file systems for mounted disks
        proc_mounts_output_lines = reader.read().strip().split("\n")
        for line in proc_mounts_output_lines:
            if line.split()[0].strip() == ("/dev/" + disk_list[selected_disk_number]):
                disk_file_system = line.split()[2].strip()
                break
            else:
                disk_file_system = _tr("[Not mounted]")
    with open("/proc/swaps") as reader:                                                       # Show "[SWAP]" information for swap disks (if selected swap area is partition (not file))
        proc_swaps_output_lines = reader.read().strip().split("\n")
        swap_disk_list = []
        for line in proc_swaps_output_lines:
            if line.split()[1].strip() == "partition":
                swap_disk_list.append(line.split()[0].strip().split("/")[-1])
    if len(swap_disk_list) > 0 and disk_list[selected_disk_number] in swap_disk_list:
        disk_file_system = _tr("[SWAP]")
    if disk_file_system  == "fuseblk":                                                        # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
        try:
            disk_file_system_from_lsblk = (subprocess.check_output("lsblk -no FSTYPE /dev/" + disk_list[selected_disk_number], shell=True).strip()).decode()
            disk_file_system = disk_file_system + " (" + disk_file_system_from_lsblk + ")"
        except:
            pass
    # Get if_system_disk
    if disk_mount_point == "/":
        if_system_disk = _tr("Yes")
    else:
        if_system_disk = _tr("No")

    # Set Disk tab label texts by using information get
    DiskGUI.label1301.set_text(disk_model_name)
    DiskGUI.label1302.set_text(f'{disk_list[selected_disk_number]} ({disk_device_or_partition})')
    DiskGUI.label1307.set_text(disk_file_system)
    DiskGUI.label1312.set_text(if_system_disk)


# ----------------------------------- Disk - Get Disk Data Function (gets Disk data, shows on the labels on the GUI) -----------------------------------
def disk_loop_func():

    disk_read_speed = Performance.disk_read_speed
    disk_write_speed = Performance.disk_write_speed

    performance_disk_speed_data_precision = Config.performance_disk_speed_data_precision
    performance_disk_usage_data_precision = Config.performance_disk_usage_data_precision
    performance_disk_speed_data_unit = Config.performance_disk_speed_data_unit
    performance_disk_usage_data_unit = Config.performance_disk_usage_data_unit

    DiskGUI.drawingarea1301.queue_draw()
    DiskGUI.drawingarea1302.queue_draw()

    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    try:
        if os.path.isdir("/sys/class/block/" + disk_list[selected_disk_number]) == False:
            return
    except:
        return
    # Get disk_read_time, disk_write_time
    with open("/proc/diskstats") as reader:
        proc_diskstats_lines = reader.read().strip().split("\n")
        for line in proc_diskstats_lines:
            if line.split()[2].strip() == disk_list[selected_disk_number]:
                disk_read_time = int(line.split()[6])
                disk_write_time = int(line.split()[10])
    # Get disk_size, disk_available, disk_free, disk_used, disk_usage_percent
    disk_get_device_partition_model_name_mount_point_func()
    global disk_usage_percent
    if disk_mount_point != "":
        statvfs_disk_usage_values = os.statvfs(disk_mount_point)                              # Values are calculated for filesystem size values (as df command does). lsblk command shows values of mass storage.
        fragment_size = statvfs_disk_usage_values.f_frsize
        disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
        disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
        disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
        disk_used = disk_size - disk_free
        #disk_usage_percent = disk_used / disk_size * 100                                     # Gives same result with "lsblk" command
        disk_usage_percent = disk_used / (disk_available + disk_used) * 100                   # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values. This is real usage percent.
    if disk_mount_point == "":
        disk_size = _tr("[Not mounted]")
        disk_available = _tr("[Not mounted]")
        disk_free = _tr("[Not mounted]")
        disk_used = _tr("[Not mounted]")
        disk_usage_percent = 0

    # Set and update Disk tab label texts by using information get
    DiskGUI.label1303.set_text(f'{disk_data_unit_converter_func(disk_read_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
    DiskGUI.label1304.set_text(f'{disk_data_unit_converter_func(disk_write_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
    DiskGUI.label1305.set_text(f'{disk_time_unit_converter_func(disk_read_time)} ms')
    DiskGUI.label1306.set_text(f'{disk_time_unit_converter_func(disk_write_time)} ms')
    if disk_mount_point != "":
        DiskGUI.label1308.set_text(f'{disk_usage_percent:.0f} %')
    if disk_mount_point == "":
        DiskGUI.label1308.set_text("- %")
    DiskGUI.label1309.set_text(disk_data_unit_converter_func(disk_available, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
    DiskGUI.label1310.set_text(disk_data_unit_converter_func(disk_used, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
    DiskGUI.label1311.set_text(disk_data_unit_converter_func(disk_size, performance_disk_usage_data_unit, performance_disk_usage_data_precision))


# ----------------------------------- Disk Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def disk_initial_thread_func():

    GLib.idle_add(disk_initial_func)


# ----------------------------------- Disk Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def disk_loop_thread_func(*args):                                                             # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1003.get_active() == True:
        global disk_glib_source, update_interval                                              # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            disk_glib_source.destroy()                                                        # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        disk_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(disk_loop_func)
        disk_glib_source.set_callback(disk_loop_thread_func)
        disk_glib_source.attach(GLib.MainContext.default())                                   # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- Disk Thread Run Function (starts execution of the threads) -----------------------------------
def disk_thread_run_func():

    if "update_interval" not in globals():                                                    # To be able to run initial thread for only one time
        disk_initial_thread = Thread(target=disk_initial_thread_func, daemon=True)
        disk_initial_thread.start()
        disk_initial_thread.join()
    disk_loop_thread = Thread(target=disk_loop_thread_func(), daemon=True)
    disk_loop_thread.start()


# ----------------------------------- Disk - Define Time Unit Converter Variables Function (contains time unit variables) -----------------------------------
def disk_time_unit_converter_func(time):

    w_r_time_days = time / 24 / 60 / 60 / 1000
    w_r_time_days_int = int(w_r_time_days)
    w_r_time_hours = (w_r_time_days - w_r_time_days_int) * 24
    w_r_time_hours_int = int(w_r_time_hours)
    w_r_time_minutes = (w_r_time_hours - w_r_time_hours_int) * 60
    w_r_time_minutes_int = int(w_r_time_minutes)
    w_r_time_seconds = (w_r_time_minutes - w_r_time_minutes_int) * 60
    w_r_time_seconds_int = int(w_r_time_seconds)
    w_r_time_milliseconds = (w_r_time_seconds - w_r_time_seconds_int) * 1000
    w_r_time_milliseconds_int = int(w_r_time_milliseconds)
    
    if w_r_time_days_int != 0:
        return f'{w_r_time_days_int:02}:{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}.{w_r_time_seconds_int:02}:{w_r_time_milliseconds_int:03}'
    if w_r_time_days_int == 0:
        return f'{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}:{w_r_time_seconds_int:02}.{w_r_time_milliseconds_int:03}'


# ----------------------------------- Disk - Get disk_model_name, parent_disk, disk_mount_point Values Function -----------------------------------
def disk_get_device_partition_model_name_mount_point_func():
    # Get disk_model_name, parent_disk, disk_mount_point values
    global disk_device_or_partition, disk_model_name, disk_mount_point
    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    selected_disk_name = disk_list[selected_disk_number]                                      # This definition is made in order to reduce CPU usage because this value is used multiple times in this function.
    try:
        if os.path.isdir("/sys/class/block/" + selected_disk_name) == False:
            return
    except:
        return
    if os.path.isdir("/sys/class/block/" + selected_disk_name + "/device"):                   # Checking "DEVTYPE" information in "/sys/class/block/[DISKNAME]/uevent" causes getting wrong "parent-child disk" information for "loop" devices. Checking "/device" folder is a more secure way.
        disk_device_or_partition = _tr("disk")
        parent_disk = ""
        with open("/sys/class/block/" + selected_disk_name + "/device/model") as reader:
            disk_model_name = reader.read().strip()
    elif "loop" in selected_disk_name:
        disk_device_or_partition = _tr("disk")
        parent_disk = ""
        disk_model_name = "[Loop Device]"
    elif "zram" in selected_disk_name:                                                        # SWAP partitions on some systems are named as "zram0, zram1, etc.) and these partitions are defined as "disk" instead pf "partition" in the "uevent" file.
        for check_disk_dir in disk_list:
            if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk_name) == True:
                parent_disk = check_disk_dir
    else:
        disk_device_or_partition = _tr("partition")
        parent_disk = selected_disk_name.rstrip('0123456789')                                 # Split string with numbers at the end of it.
        with open("/sys/class/block/" + parent_disk + "/device/model") as reader:
            disk_model_name = reader.read().strip()
    with open("/proc/mounts") as reader:
        proc_mounts_output_lines = reader.read().strip().split("\n")
        disk_mount_point = ""
        for line in proc_mounts_output_lines:
            if line.split()[0].strip() == ("/dev/" + selected_disk_name):
                disk_mount_point = line.split()[1].strip().replace("\\040", " ")              # Disk mount point is get with containing "\\040" characters if there are spaces in the name of the loop disk. ".replace("\\040", " ")" code is used in order to replace these characters with a space for avoidng errors.


# ----------------------------------- Disk - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def disk_define_data_unit_converter_variables_func():

    global data_unit_list

    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently.

    # Unit Name    Abbreviation    bytes   
    # byte         B               1
    # kilobyte     KB              1024
    # megabyte     MB              1.04858E+06
    # gigabyte     GB              1.07374E+09
    # terabyte     TB              1.09951E+12
    # petabyte     PB              1.12590E+15
    # exabyte      EB              1.15292E+18

    # Unit Name    Abbreviation    bytes    
    # bit          b               8
    # kilobit      Kb              8192
    # megabit      Mb              8,38861E+06
    # gigabit      Gb              8,58993E+09
    # terabit      Tb              8,79609E+12
    # petabit      Pb              9,00720E+15
    # exabit       Eb              9,22337E+18

    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Disk - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def disk_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit == 0 or unit == 8:
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
