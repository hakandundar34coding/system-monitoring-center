#!/usr/bin/env python3

# ----------------------------------- Disk - Disk Tab Import Function -----------------------------------
def disk_import_func():

    global Gtk, GLib, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gtk, GLib
    import os
    import subprocess


    global Config, Performance
    import Config, Performance


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Disk - Disk GUI Function -----------------------------------
def disk_gui_func():

    # Disk tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskTab.ui")

    # Disk tab GUI objects
    global grid1301, drawingarea1301, drawingarea1302, button1301, label1301, label1302
    global label1303, label1304, label1305, label1306, label1307, label1308, label1309, label1310, label1311, label1313, eventbox1301

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
    label1313 = builder.get_object('label1313')
    eventbox1301 = builder.get_object('eventbox1301')


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

    def on_eventbox1301_button_click_event(widget, event):                                    # Eventbox is used for defining signals for the widget ("Query..." label) placed on it.
        if event.button == 1:
            if 'DiskDetails' not in globals():                                                # Check if "DiskDetails" module is imported. Therefore it is not reimported for every mouse click if "DiskDetails" name is in globals().
                global DiskDetails
                import DiskDetails
                DiskDetails.disk_details_import_func()
                DiskDetails.disk_details_gui_func()
            DiskDetails.window1301w.show()
            DiskDetails.disk_details_run_func()


    # ----------------------------------- Disk - Plot Disk read/write speed data as a Line Chart ----------------------------------- 
    def on_drawingarea1301_draw(drawingarea1301, chart1301):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        disk_read_speed = Performance.disk_read_speed[Performance.selected_disk_number]
        disk_write_speed = Performance.disk_write_speed[Performance.selected_disk_number]

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

        # ---------- Start - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------
        # Chart maximum value is shown as multiples of 1, 10, 100 (For example, 1, 2, 3, ..., 10, 20, 30, ..., 100, 200, 300, ...) in order to simplify the value and avoid misunderstandings of performance data and chart maximum values.
        # Chart maximum value is get as calculated value (instead of Bytes) and number of digits is calculated by using integer part of this value.
        # Next multiple value is calculated, data unit is appended as string and value is shown on a label.
        # "chart1301_y_limit" value is updated by using new (multiple) value.
        data_unit_for_chart_y_limit = 0
        if Config.performance_disk_speed_data_unit >= 8:
            data_unit_for_chart_y_limit = 8
        try:                                                                                  # try-except is used in order to prevent errors if first initial function is not finished and "disk_data_unit_converter_func" is not run.
            chart1301_y_limit_str = f'{disk_data_unit_converter_func(chart1301_y_limit, data_unit_for_chart_y_limit, 0)}/s'
        except NameError:
            return
        chart1301_y_limit_split = chart1301_y_limit_str.split(" ")
        chart1301_y_limit_float = float(chart1301_y_limit_split[0])
        number_of_digits = len(str(int(chart1301_y_limit_split[0])))
        multiple = 10 ** (number_of_digits - 1)
        number_to_get_next_multiple = chart1301_y_limit_float + (multiple - 0.0001)           # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
        next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
        label1313.set_text(f'{next_multiple} {chart1301_y_limit_split[1]}')
        chart1301_y_limit = (chart1301_y_limit * next_multiple / (chart1301_y_limit_float + 0.0000001) + 0.0000001)    # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
        # ---------- End - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------

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

        try:
            disk_usage_percent_check = disk_usage_percent                                     # "disk_usage_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
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
    eventbox1301.connect("button-press-event", on_eventbox1301_button_click_event)


# ----------------------------------- Disk - Initial Function -----------------------------------
def disk_initial_func():

    disk_define_data_unit_converter_variables_func()                                          # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global disk_list, selected_disk
    disk_list = Performance.disk_list
    selected_disk_number = Performance.selected_disk_number
    selected_disk = disk_list[selected_disk_number]

    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    try:
        check_value = "/sys/class/block/" + selected_disk
    except Exception:
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
    # Get if_system_disk
    if disk_mount_point == "/":
        if_system_disk = _tr("Yes")
    else:
        if_system_disk = _tr("No")

    # Set Disk tab label texts by using information get
    label1301.set_text(disk_vendor_model)
    label1302.set_text(f'{selected_disk} ({disk_type})')
    label1307.set_text(if_system_disk)


# ----------------------------------- Disk - Get Disk Data Function -----------------------------------
def disk_loop_func():

    global disk_list, selected_disk, selected_disk_prev
    disk_list = Performance.disk_list
    selected_disk_number = Performance.selected_disk_number
    selected_disk = disk_list[selected_disk_number]
    try:                                                                                      # try-except is used in order to avoid error if this is first loop of the function. Because "selected_disk_prev" variable is not defined in this situation.
        if selected_disk_prev != selected_disk:                                               # Run "disk_initial_func" if selected disk is changed since the last loop.
            disk_initial_func()
    except NameError:
        pass
    selected_disk_prev = selected_disk

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
        if os.path.isdir("/sys/class/block/" + selected_disk) == False:
            return
    except Exception:
        return
    # Get disk_read_time, disk_write_time
    with open("/proc/diskstats") as reader:
        proc_diskstats_lines = reader.read().strip().split("\n")
        for line in proc_diskstats_lines:
            if line.split()[2].strip() == selected_disk:
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


# ----------------------------------- Disk - Run Function -----------------------------------
def disk_run_func(*args):

    if "update_interval" not in globals():
        GLib.idle_add(disk_initial_func)
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 2:
        global disk_glib_source, update_interval
        try:
            disk_glib_source.destroy()
        except NameError:
            pass
        update_interval = Config.update_interval
        disk_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(disk_loop_func)
        disk_glib_source.set_callback(disk_run_func)
        disk_glib_source.attach(GLib.MainContext.default())


# ----------------------------------- Disk - Define Time Unit Converter Variables Function -----------------------------------
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
    selected_disk_name = selected_disk
    try:
        if os.path.isdir("/sys/class/block/" + selected_disk_name) == False:
            return
    except Exception:
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
        disk_or_parent_disk_name = selected_disk_name
    if disk_type == _tr("Partition"):
        disk_or_parent_disk_name = disk_parent_name
    # Get disk vendor
    try:
        with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/vendor") as reader:
            disk_vendor = reader.read().strip()
        if disk_vendor.startswith("0x"):                                                      # Disk vendor information may be available as vendor id on some cases (such as on QEMU virtual machines).
            disk_vendor_id = "\n" + disk_vendor.split("x")[-1].strip() + "  "
            if disk_vendor_id in pci_ids_output:                                              # "vendor" information may not be present in the pci.ids file.
                rest_of_the_pci_ids_output = pci_ids_output.split(disk_vendor_id, 1)[1]       # "1" in the ".split("[string", 1)" is used in order to split only the first instance in the whole text for faster split operation.
                disk_vendor = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
            if disk_vendor_id not in pci_ids_output:
                disk_vendor = f'[{_tr("Unknown")}]'
    except FileNotFoundError:                                                                 # Some disks such as NVMe SSDs do not have "vendor" file under "/sys/class/block/" + selected_disk_name + "/device" directory. They have this file under "/sys/class/block/" + selected_disk_name + "/device/device/vendor" directory.
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/vendor") as reader:
                disk_vendor_id = "\n" + reader.read().strip().split("x")[-1] + "  "
            if disk_vendor_id in pci_ids_output:                                              # "vendor" information may not be present in the pci.ids file.
                rest_of_the_pci_ids_output = pci_ids_output.split(disk_vendor_id, 1)[1]
                disk_vendor = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
            if disk_vendor_id not in pci_ids_output:
                disk_vendor = f'[{_tr("Unknown")}]'
        except Exception:
            disk_vendor = f'[{_tr("Unknown")}]'
    # Get disk model
    try:
        with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
            disk_model = reader.read().strip()
        if disk_model.startswith("0x"):                                                       # Disk model information may be available as model id on some cases (such as on QEMU virtual machines).
            disk_model_id = "\n\t" + disk_model.split("x")[-1] + "  "
            if disk_vendor != f'[{_tr("Unknown")}]':
                if disk_model_id in rest_of_the_pci_ids_output:                               # "device name" information may not be present in the pci.ids file.
                    rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(disk_model_id, 1)[1]
                    disk_model = rest_of_the_rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                else:
                    disk_model = f'[{_tr("Unknown")}]'
            else:
                disk_model = f'[{_tr("Unknown")}]'
    except Exception:
        disk_model = f'[{_tr("Unknown")}]'
    disk_vendor_model = disk_vendor + " - " +  disk_model
    # Get disk vendor and model if disk is loop device or swap disk.
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


# ----------------------------------- Disk - Define Data Unit Converter Variables Function -----------------------------------
def disk_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Disk - Data Unit Converter Function -----------------------------------
def disk_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
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
