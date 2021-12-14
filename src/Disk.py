#!/usr/bin/env python3

# ----------------------------------- Disk - Disk Tab Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def disk_import_func():

    global Gtk, GLib, Thread, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os
    import subprocess


    global Config, MainGUI, Performance
    from . import Config, MainGUI, Performance


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


# ----------------------------------- Disk - Disk GUI Function (the code of this module in order to avoid running them during module import and defines "Disk" tab GUI objects and functions/signals) -----------------------------------
def disk_gui_func():

    # Disk tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/ui/DiskTab.ui")

    # Disk tab GUI objects
    global grid1301, drawingarea1301, drawingarea1302, button1301, label1301, label1302
    global label1303, label1304, label1305, label1306, label1307, label1308, label1309, label1310, label1311, label1312

    # Disk tab GUI objects - get
    grid1301 = builder.get_object('grid1301')
    drawingarea1301 = builder.get_object('drawingarea1301')
    drawingarea1302 = builder.get_object('drawingarea1302')
    button1301 = builder.get_object('button1301')
    label1301 = builder.get_object('label1301')
    label1302 = builder.get_object('label1302')
    label1303 = builder.get_object('label1303')
    label1304 = builder.get_object('label1304')
    label1305 = builder.get_object('label1305')
    label1306 = builder.get_object('label1306')
    label1307 = builder.get_object('label1307')
    label1308 = builder.get_object('label1308')
    label1309 = builder.get_object('label1309')
    label1310 = builder.get_object('label1310')
    label1311 = builder.get_object('label1311')
    label1312 = builder.get_object('label1312')


    # Disk tab GUI functions
    def on_button1301_clicked(widget):
        if 'DiskMenu' not in globals():
            global DiskMenu
            import DiskMenu
            DiskMenu.disk_menus_import_func()
            DiskMenu.disk_menus_gui_func()
            DiskMenu.popover1301p.set_relative_to(button1301)                                 # Set widget that popover menu will display at the edge of.
            DiskMenu.popover1301p.set_position(1)                                             # Show popover menu at the right edge of the caller button.
        DiskMenu.popover1301p.popup()                                                         # Show Disk tab popover GUI

    # ----------------------------------- Disk - Plot Disk read/write speed data as a Line Chart ----------------------------------- 
    def on_drawingarea1301_draw(drawingarea1301, chart1301):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))
        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the Disk module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            disk_read_speed = Performance.disk_read_speed[Performance.selected_disk_number]
            disk_write_speed = Performance.disk_write_speed[Performance.selected_disk_number]
        except AttributeError:
            return
        chart_line_color = Config.chart_line_color_disk_speed_usage
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

        chart1301_width = Gtk.Widget.get_allocated_width(drawingarea1301)
        chart1301_height = Gtk.Widget.get_allocated_height(drawingarea1301)

        chart1301.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1301.rectangle(0, 0, chart1301_width, chart1301_height)
        chart1301.fill()

        chart1301.set_line_width(1)
        chart1301.set_dash([4, 3])
        chart1301.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        for i in range(3):
            chart1301.move_to(0, chart1301_height/4*(i+1))
            chart1301.line_to(chart1301_width, chart1301_height/4*(i+1))
        for i in range(4):
            chart1301.move_to(chart1301_width/5*(i+1), 0)
            chart1301.line_to(chart1301_width/5*(i+1), chart1301_height)
        chart1301.stroke()

        chart1301_y_limit = 1.1 * ((max(max(disk_read_speed), max(disk_write_speed))) + 0.0000001)
        if Config.plot_disk_read_speed == 1 and Config.plot_disk_write_speed == 0:
            chart1301_y_limit = 1.1 * (max(disk_read_speed) + 0.0000001)
        if Config.plot_disk_read_speed == 0 and Config.plot_disk_write_speed == 1:
            chart1301_y_limit = 1.1 * (max(disk_write_speed) + 0.0000001)

        chart1301.set_dash([], 0)
        chart1301.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1301.rectangle(0, 0, chart1301_width, chart1301_height)
        chart1301.stroke()

        if Config.plot_disk_read_speed == 1:
            chart1301.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            chart1301.move_to(chart1301_width*chart_x_axis[0]/(chart_data_history-1), chart1301_height - chart1301_height*disk_read_speed[0]/chart1301_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1301a = (chart1301_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1301_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1301a = (chart1301_height*disk_read_speed[i+1]/chart1301_y_limit) - (chart1301_height*disk_read_speed[i]/chart1301_y_limit)
                chart1301.rel_line_to(delta_x_chart1301a, -delta_y_chart1301a)

            chart1301.rel_line_to(10, 0)
            chart1301.rel_line_to(0, chart1301_height+10)
            chart1301.rel_line_to(-(chart1301_width+20), 0)
            chart1301.rel_line_to(0, -(chart1301_height+10))
            chart1301.close_path()
            chart1301.stroke()

        if Config.plot_disk_write_speed == 1:
            chart1301.set_dash([3, 3])
            chart1301.move_to(chart1301_width*chart_x_axis[0]/(chart_data_history-1), chart1301_height - chart1301_height*disk_write_speed[0]/chart1301_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1301b = (chart1301_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1301_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1301b = (chart1301_height*disk_write_speed[i+1]/chart1301_y_limit) - (chart1301_height*disk_write_speed[i]/chart1301_y_limit)
                chart1301.rel_line_to(delta_x_chart1301b, -delta_y_chart1301b)

            chart1301.rel_line_to(10, 0)
            chart1301.rel_line_to(0, chart1301_height+10)
            chart1301.rel_line_to(-(chart1301_width+20), 0)
            chart1301.rel_line_to(0, -(chart1301_height+10))
            chart1301.close_path()
            chart1301.stroke()


    # ----------------------------------- Disk - Plot Disk usage data as a Bar Chart ----------------------------------- 
    def on_drawingarea1302_draw(drawingarea1302, chart1302):

        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the Disk module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            disk_usage_percent_check = disk_usage_percent
        except NameError:
            return

        chart_line_color = Config.chart_line_color_disk_speed_usage
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3]]

        chart1302_width = Gtk.Widget.get_allocated_width(drawingarea1302)
        chart1302_height = Gtk.Widget.get_allocated_height(drawingarea1302)

        chart1302.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1302.rectangle(0, 0, chart1302_width, chart1302_height)
        chart1302.fill()

        chart1302.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        chart1302.rectangle(0, 0, chart1302_width, chart1302_height)
        chart1302.stroke()
        chart1302.set_line_width(1)
        chart1302.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart1302.rectangle(0, 0, chart1302_width*disk_usage_percent/100, chart1302_height)
        chart1302.fill()


    # Disk tab GUI functions - connect
    button1301.connect("clicked", on_button1301_clicked)
    drawingarea1301.connect("draw", on_drawingarea1301_draw)
    drawingarea1302.connect("draw", on_drawingarea1302_draw)


# ----------------------------------- Disk - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def disk_initial_func():

    disk_define_data_unit_converter_variables_func()                                          # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global disk_list, selected_disk_number                                                    # These variables are defined as global variables because they will be used in "disk_loop_func" function and also they will be used by "disk_get_device_partition_model_name_mount_point_func" function.
    disk_list = Performance.disk_list
    selected_disk_number = Performance.selected_disk_number

    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    try:
        check_value = "/sys/class/block/" + disk_list[selected_disk_number]
    except:
        return
    # Read pci.ids file. Some disks such as NVMe SSDs have "vendor" file with device id content. pci.ids file will be used for getting disk vendor name by using these ids.
    global pci_ids_output
    try:                                                                                      # Find disk device model from "pci.ids" file by using vendor id and device id.
        with open("/usr/share/misc/pci.ids") as reader:                                       # Read "pci.ids" file if it is located in "/usr/share/misc/pci.ids" in order to use it as directory. This directory is used in Debian-like systems.
            pci_ids_output = reader.read()
    except FileNotFoundError:
        with open("/usr/share/hwdata/pci.ids") as reader:                                     # Read "pci.ids" file if it is located in "/usr/share/hwdata/pci.ids" in order to use it as directory. This directory is used in systems other than Debian-like systems.
            pci_ids_output = reader.read()
    # Get disk_vendor_model, disk_parent_name, disk_mount_point
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
            disk_for_file_system = "/dev/" + disk_list[selected_disk_number]
            disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
        except:
            pass
    # Get if_system_disk
    if disk_mount_point == "/":
        if_system_disk = _tr("Yes")
    else:
        if_system_disk = _tr("No")

    # Set Disk tab label texts by using information get
    label1301.set_text(disk_vendor_model)
    label1302.set_text(f'{disk_list[selected_disk_number]} ({disk_type})')
    label1307.set_text(disk_file_system)
    label1312.set_text(if_system_disk)


# ----------------------------------- Disk - Get Disk Data Function (gets Disk data, shows on the labels on the GUI) -----------------------------------
def disk_loop_func():

    disk_read_speed = Performance.disk_read_speed
    disk_write_speed = Performance.disk_write_speed

    performance_disk_speed_data_precision = Config.performance_disk_speed_data_precision
    performance_disk_usage_data_precision = Config.performance_disk_usage_data_precision
    performance_disk_speed_data_unit = Config.performance_disk_speed_data_unit
    performance_disk_usage_data_unit = Config.performance_disk_usage_data_unit

    drawingarea1301.queue_draw()
    drawingarea1302.queue_draw()

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
    label1303.set_text(f'{disk_data_unit_converter_func(disk_read_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
    label1304.set_text(f'{disk_data_unit_converter_func(disk_write_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
    label1305.set_text(f'{disk_time_unit_converter_func(disk_read_time)} ms')
    label1306.set_text(f'{disk_time_unit_converter_func(disk_write_time)} ms')
    if disk_mount_point != "":
        label1308.set_text(f'{disk_usage_percent:.0f}%')
    if disk_mount_point == "":
        label1308.set_text("-%")
    label1309.set_text(disk_data_unit_converter_func(disk_available, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
    label1310.set_text(disk_data_unit_converter_func(disk_used, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
    label1311.set_text(disk_data_unit_converter_func(disk_size, performance_disk_usage_data_unit, performance_disk_usage_data_precision))


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
    disk_loop_thread = Thread(target=disk_loop_thread_func, daemon=True)
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

    if time < 3600000:                                                                        # Return time in the following format if time is less than 1 hour.
        return f'{w_r_time_minutes_int:02}:{w_r_time_seconds_int:02}.{w_r_time_milliseconds_int:03}'
    if time >= 3600000 and time < 86400000:                                                   # Return time in the following format if time is more than 1 hour and less than 1 day.
        return f'{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}:{w_r_time_seconds_int:02}.{w_r_time_milliseconds_int:03}'
    if time >= 86400000:                                                                      # Return time in the following format if time is more than 1 day.
        return f'{w_r_time_days_int:02}:{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}.{w_r_time_seconds_int:02}:{w_r_time_milliseconds_int:03}'


# ----------------------------------- Disk - Get disk_vendor_model, disk_parent_name, disk_mount_point Values Function -----------------------------------
def disk_get_device_partition_model_name_mount_point_func():

    global disk_type, disk_vendor_model, disk_mount_point
    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    selected_disk_name = disk_list[selected_disk_number]                                      # This definition is made in order to reduce CPU usage because this value is used multiple times in this function.
    try:
        if os.path.isdir("/sys/class/block/" + selected_disk_name) == False:
            return
    except:
        return
    # Get disk type (Disk or Partition)
    with open("/sys/class/block/" + selected_disk_name + "/uevent") as reader:
        sys_class_block_disk_uevent_lines = reader.read().split("\n")
    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            disk_type = _tr(line.split("=")[1].capitalize())
            break
    # Get parent disk name of the disk
    disk_parent_name = ""                                                                     # Initial value of "disk_parent_name" variable. This value will be used if disk has no parent disk or disk parent name could not be detected.
    if disk_type == _tr("Partition"):
        for check_disk_dir in disk_list:
            if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk_name) == True:
                disk_parent_name = check_disk_dir
    # Get disk vendor and model
    if disk_type == _tr("Disk"):
        # Get disk vendor if selected disk is a disk
        try:
            with open("/sys/class/block/" + selected_disk_name + "/device/vendor") as reader:
                disk_vendor = reader.read().strip()
        except FileNotFoundError:                                                             # Some disks such as NVMe SSDs do not have "vendor" file under "/sys/class/block/" + selected_disk_name + "/device" directory. They have this file under "/sys/class/block/" + selected_disk_name + "/device/device/vendor" directory.
            try:
                with open("/sys/class/block/" + selected_disk_name + "/device/device/vendor") as reader:
                    disk_vendor_id = reader.read().strip().split("x")[-1]
                if disk_vendor_id in pci_ids_output:                                          # "vendor" information may not be present in the pci.ids file.
                    rest_of_the_pci_ids_output = pci_ids_output.split(disk_vendor_id)[1]
                    disk_vendor = rest_of_the_pci_ids_output.split("\n")[0].strip()
                if disk_vendor_id not in pci_ids_output:
                    disk_vendor = f'[{_tr("Unknown")}]'
            except:
                disk_vendor = f'[{_tr("Unknown")}]'
        # Get disk model if selected disk is a disk
        try:
            with open("/sys/class/block/" + selected_disk_name + "/device/model") as reader:
                disk_model = reader.read().strip()
        except:
            disk_model = f'[{_tr("Unknown")}]'
        disk_vendor_model = disk_vendor + " - " +  disk_model
    if disk_type == _tr("Partition"):
        # Get disk vendor if selected disk is a partition
        try:
            with open("/sys/class/block/" + disk_parent_name + "/device/vendor") as reader:
                disk_vendor = reader.read().strip()
        except FileNotFoundError:                                                             # Some disks such as NVMe SSDs do not have "vendor" file under "/sys/class/block/" + disk_parent_name + "/device" directory. They have this file under "/sys/class/block/" + disk_parent_name + "/device/device/vendor" directory.
            try:
                with open("/sys/class/block/" + disk_parent_name + "/device/device/vendor") as reader:
                    disk_vendor_id = reader.read().strip().split("x")[-1]
                if disk_vendor_id in pci_ids_output:                                          # "vendor" information may not be present in the pci.ids file.
                    rest_of_the_pci_ids_output = pci_ids_output.split(disk_vendor_id)[1]
                    disk_vendor = rest_of_the_pci_ids_output.split("\n")[0].strip()
                if disk_vendor_id not in pci_ids_output:
                    disk_vendor = "-"
            except:
                disk_vendor = "-"
        # Get disk model if selected disk is a partition
        try:
            with open("/sys/class/block/" + disk_parent_name + "/device/model") as reader:
                disk_model = reader.read().strip()
        except:
            disk_model = "-"
        disk_vendor_model = disk_vendor + " - " +  disk_model
    if "loop" in selected_disk_name:
        disk_vendor_model = "[Loop Device]"
    if "zram" in selected_disk_name:
        disk_vendor_model = _tr("[SWAP]")
    # Get disk mount point
    with open("/proc/mounts") as reader:
        proc_mounts_output_lines = reader.read().strip().split("\n")
        disk_mount_point = ""
        for line in proc_mounts_output_lines:
            if line.split()[0].strip() == ("/dev/" + selected_disk_name):
                disk_mount_point = bytes(line.split()[1].strip(), "utf-8").decode("unicode_escape")    # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                break                                                                         # System disk is listed twice with different mountpoint information on systems which are installed on disks with "btrfs" filesystem. "/" mountpoint information is used by using "break" code.


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
    if unit in [0, 8]:                                                                        # "if unit in [0, 8]:" is about %25 faster than "if unit == 0 or unit == 8:".                                                                     # "if unit in [0, 8]" is about %25 faster than "if unit == 0 or unit == 8:".
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
