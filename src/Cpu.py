#!/usr/bin/env python3

# ----------------------------------- CPU - CPU Tab Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def cpu_import_func():

    global Gtk, GLib, os, platform

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    import platform


    global Config, Performance
    import Config, Performance


    # Import gettext module for defining translation texts which will be recognized by gettext application. These lines of code are enough to define this variable if another values are defined in another module (MainGUI) before importing this module.
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    from locale import gettext as _tr


# ----------------------------------- CPU - CPU GUI Function (the code of this module in order to avoid running them during module import and defines "CPU" tab GUI objects and functions/signals) -----------------------------------
def cpu_gui_func():

    # CPU tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/CpuTab.ui")

    # CPU tab GUI objects
    global grid1101, drawingarea1101, button1101, label1101, label1102
    global label1103, label1104, label1105, label1106, label1107, label1108, label1109, label1110, label1111, label1112, label1113

    # CPU tab GUI objects - get
    grid1101 = builder.get_object('grid1101')
    drawingarea1101 = builder.get_object('drawingarea1101')
    button1101 = builder.get_object('button1101')
    label1101 = builder.get_object('label1101')
    label1102 = builder.get_object('label1102')
    label1103 = builder.get_object('label1103')
    label1104 = builder.get_object('label1104')
    label1105 = builder.get_object('label1105')
    label1106 = builder.get_object('label1106')
    label1107 = builder.get_object('label1107')
    label1108 = builder.get_object('label1108')
    label1109 = builder.get_object('label1109')
    label1110 = builder.get_object('label1110')
    label1111 = builder.get_object('label1111')
    label1112 = builder.get_object('label1112')
    label1113 = builder.get_object('label1113')


    # CPU tab GUI functions
    def on_button1101_clicked(widget):                                                        # "CPU Tab Customizations" button
        if 'CpuMenu' not in globals():
            global CpuMenu
            import CpuMenu
            CpuMenu.cpu_menus_import_func()
            CpuMenu.cpu_menus_gui_func()
            CpuMenu.popover1101p.set_relative_to(button1101)                                  # Set widget that popover menu will display at the edge of.
            CpuMenu.popover1101p.set_position(1)                                              # Show popover menu at the right edge of the caller button in order not to hide CPU usage percentage when menu is shown. Becuse there is CPU usage percentage precision setting and user may want to see visual changes just in time.
        CpuMenu.popover1101p.popup()                                                          # Show CPU tab popover GUI

    # CPU tab GUI functions - connect
    button1101.connect("clicked", on_button1101_clicked)
    if Config.show_cpu_usage_per_core == 0:
        drawingarea1101.connect("draw", on_drawingarea1101_draw)
    # Connects different function to the drawingarea if "show cpu usage per core" setting is enabled
    if Config.show_cpu_usage_per_core == 1:
        drawingarea1101.connect("draw", on_drawingarea1101_draw_per_core)


# ----------------------------------- CPU - Plot CPU usage average data as a Line Chart ----------------------------------- 
def on_drawingarea1101_draw(widget, chart1101):

    # Get values from "Config and Peformance" modules and use this defined values in order to avoid multiple uses of variables from another module since CPU usage is higher for this way.
    chart_data_history = Config.chart_data_history
    chart_x_axis = list(range(0, chart_data_history))

    cpu_usage_percent_ave = Performance.cpu_usage_percent_ave

    chart_line_color = Config.chart_line_color_cpu_percent
    chart_background_color = Config.chart_background_color_all_charts

    # Chart foreground and chart fill below line colors may be set different for charts in different style (line, bar, etc.) and different places (tab pages, headerbar, etc.).
    # Set chart foreground color (chart outer frame and gridline colors) same as "chart_line_color" in multiplication with transparency factor "0.4".
    chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
    # Set chart fill below line color same as "chart_line_color" in multiplication with transparency factor "0.15".
    chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

    # Get drawingarea width and height. Therefore chart width and height is updated dynamically by using these values when window size is changed by user.
    chart1101_width = Gtk.Widget.get_allocated_width(drawingarea1101)
    chart1101_height = Gtk.Widget.get_allocated_height(drawingarea1101)

    # Set color for chart background, draw chart background rectangle and fill the inner area.
    # Only one drawing style with multiple properties (color, line width, dash style) can be set at the same time.
    # As a result style should be set, drawing should be done and another style shpuld be set for next drawing.
    chart1101.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
    chart1101.rectangle(0, 0, chart1101_width, chart1101_height)
    chart1101.fill()

    # Change line width, dash style (if [4, 3] is used, this means draw 4 pixels, skip 3 pixels) and color for chart gridlines.
    chart1101.set_line_width(1)
    chart1101.set_dash([4, 3])
    chart1101.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
    # Draw horizontal gridlines (range(3) means 3 gridlines will be drawn)
    for i in range(3):
        chart1101.move_to(0, chart1101_height/4*(i+1))
        chart1101.line_to(chart1101_width, chart1101_height/4*(i+1))
    # Draw vertical gridlines
    for i in range(4):
        chart1101.move_to(chart1101_width/5*(i+1), 0)
        chart1101.line_to(chart1101_width/5*(i+1), chart1101_height)
    chart1101.stroke()    # "stroke" command draws line (line or closed shapes with empty inner area). "fill" command should be used for filling inner areas.

    # Change line style (solid line) for chart foreground.
    chart1101.set_dash([], 0)
    # Draw chart outer rectange.
    chart1101.rectangle(0, 0, chart1101_width, chart1101_height)
    chart1101.stroke()

    # Change the color for drawing data line (curve).
    chart1101.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
    # Move drawing point (cairo context which is used for drawing on drawable objects) from data point to data point and connect them by a line in order to draw a curve.
    # First, move drawing point to the lower left corner of the chart and draw all data points one by one by going to the right direction.
    chart1101.move_to(chart1101_width*chart_x_axis[0]/(chart_data_history-1), chart1101_height - chart1101_height*cpu_usage_percent_ave[0]/100)
    # Move drawing point to the next data points and connect them by a line.
    for i in range(len(chart_x_axis) - 1):
        # Distance to move on the horizontal axis
        delta_x_chart1101 = (chart1101_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1101_width * chart_x_axis[i]/(chart_data_history-1))
        # Distance to move on the vertical axis
        delta_y_chart1101 = (chart1101_height*cpu_usage_percent_ave[i+1]/100) - (chart1101_height*cpu_usage_percent_ave[i]/100)
        # Move
        chart1101.rel_line_to(delta_x_chart1101, -delta_y_chart1101)

    # Move drawing point 10 pixel right in order to go out of the visible drawing area for drawing a closed shape for filling the inner area.
    chart1101.rel_line_to(10, 0)
    # Move drawing point "chart_height+10" down in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
    chart1101.rel_line_to(0, chart1101_height+10)
    # Move drawing point "chart1101_width+20" pixel left (by using a minus sign) in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
    chart1101.rel_line_to(-(chart1101_width+20), 0)
    # Move drawing point "chart_height+10" up in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
    chart1101.rel_line_to(0, -(chart1101_height+10))
    # Finally close the curve in order to fill the inner area which will represent a curve with a filled "below" area.
    chart1101.close_path()
    # Use "stroke_preserve" in order to use the same area for filling. 
    chart1101.stroke_preserve()
    # Change the color for filling operation.
    chart1101.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
    # Fill the area
    chart1101.fill()


# ----------------------------------- CPU - Plot CPU usage per core data as Bar Charts if "show cpu usage per core" setting is enabled. ----------------------------------- 
def on_drawingarea1101_draw_per_core(widget, chart1101):

    logical_core_list_system_ordered = Performance.logical_core_list_system_ordered

    logical_core_list = Performance.logical_core_list
    cpu_usage_percent_per_core = Performance.cpu_usage_percent_per_core

    chart_line_color = Config.chart_line_color_cpu_percent
    chart_background_color = Config.chart_background_color_all_charts

    chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.8 * chart_line_color[3]]
    chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]

    chart1101_width = Gtk.Widget.get_allocated_width(drawingarea1101)
    chart1101_height = Gtk.Widget.get_allocated_height(drawingarea1101)

    chart1101_width_per_core = chart1101_width / Performance.number_of_logical_cores
    chart1101_height_per_core = chart1101_height                                              # Chart height and chart height per core is same because charts for all cores will be bars next to each other (like columns).
    chart1101_width_per_core_w_spacing = chart1101_width_per_core - 10                        # Spacing 5 from left an right
    chart1101_height_per_core_w_spacing = chart1101_height - 10                               # Spacing 5 from top an bottom

    for i, cpu_core in enumerate(logical_core_list_system_ordered):
        chart1101.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1101.rectangle(i*chart1101_width_per_core, 0, chart1101_width_per_core, chart1101_height_per_core)
        chart1101.fill()

        chart1101.set_line_width(1)
        chart1101.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        chart1101.rectangle(i*chart1101_width_per_core+5, 5, chart1101_width_per_core_w_spacing, chart1101_height_per_core_w_spacing)
        chart1101.stroke()
        chart1101.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart1101.rectangle(i*chart1101_width_per_core+5, (chart1101_height_per_core_w_spacing-chart1101_height_per_core_w_spacing*cpu_usage_percent_per_core[logical_core_list.index(cpu_core)]/100)+5, chart1101_width_per_core_w_spacing, chart1101_height_per_core_w_spacing*cpu_usage_percent_per_core[logical_core_list.index(cpu_core)]/100)
        chart1101.fill()
        chart1101.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], 2*chart_foreground_color[3])
        chart1101.move_to(i*chart1101_width_per_core+8, 16)
        chart1101.show_text(f'{cpu_core.split("cpu")[-1]}')


# ----------------------------------- CPU - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def cpu_initial_func():

    logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
    selected_cpu_core = Performance.selected_cpu_core
    selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]

    # Get maximum and minimum frequencies of the selected CPU core
    try:
        with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_max_freq") as reader:
            cpu_max_frequency_selected_core = float(reader.read().strip()) / 1000000
        with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_min_freq") as reader:
            cpu_min_frequency_selected_core = float(reader.read().strip()) / 1000000
    except FileNotFoundError:
        cpu_max_frequency_selected_core = "-"
        cpu_min_frequency_selected_core = "-"

    # Get cache memory values of the selected CPU core
    # Get l1d cache value
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/type") as reader:
            cache_type = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "1" and cache_type == "Data":
            cpu_l1d_cache_value_selected_core = cache_size
    except FileNotFoundError:
        cpu_l1d_cache_value_selected_core = "-"
    # Get li cache value
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/type") as reader:
            cache_type = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "1" and cache_type == "Instruction":
            cpu_l1i_cache_value_selected_core = cache_size
    except FileNotFoundError:
        cpu_l1i_cache_value_selected_core = "-"
    # Get l2 cache value
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "2":
            cpu_l2_cache_value_selected_core = cache_size
    except FileNotFoundError:
        cpu_l2_cache_value_selected_core = "-"
    # Get l3 cache value
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "3":
            cpu_l3_cache_value_selected_core = cache_size
    except FileNotFoundError:
        cpu_l3_cache_value_selected_core = "-"

    # Get CPU architecture
    cpu_architecture = platform.processor()
    if cpu_architecture == "":
        cpu_architecture = platform.machine()
        if cpu_architecture == "":
            cpu_architecture = "-"

    # Set CPU tab label texts by using information get
    show_cpu_usage_per_core = Config.show_cpu_usage_per_core
    if show_cpu_usage_per_core == 0:
        label1113.set_text(_tr("CPU Usage (Average)"))
    if show_cpu_usage_per_core == 1:
        label1113.set_text(_tr("CPU Usage (Per Core)"))
    label1108.set_text(cpu_architecture)
    if isinstance(cpu_max_frequency_selected_core, str) is False:
        label1105.set_text(f'{cpu_min_frequency_selected_core:.2f} - {cpu_max_frequency_selected_core:.2f} GHz')
    if isinstance(cpu_max_frequency_selected_core, str) is True:
        label1105.set_text(f'{cpu_min_frequency_selected_core} - {cpu_max_frequency_selected_core}')
    label1109.set_text(f'{cpu_l1i_cache_value_selected_core} - {cpu_l1d_cache_value_selected_core}')
    label1110.set_text(f'{cpu_l2_cache_value_selected_core} - {cpu_l3_cache_value_selected_core}')


# ----------------------------------- CPU - Get CPU Data Function (gets CPU data, shows on the labels on the GUI) -----------------------------------
def cpu_loop_func():

    number_of_logical_cores = Performance.number_of_logical_cores
    cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
    selected_cpu_core_number = Performance.selected_cpu_core_number
    selected_cpu_core = Performance.selected_cpu_core
    selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]
    global selected_cpu_core_prev
    try:                                                                                      # try-except is used in order to avoid error if this is first loop of the function. Because "selected_cpu_core_prev" variable is not defined in this situation.
        if selected_cpu_core_prev != selected_cpu_core:                                       # Run "cpu_initial_func" if selected CPU core is changed since the last loop.
            cpu_initial_func()
    except NameError:
        pass
    selected_cpu_core_prev = selected_cpu_core

    drawingarea1101.queue_draw()

    # Get number of physical cores, number_of_cpu_sockets, cpu_model_names
    with open("/proc/cpuinfo") as reader:
        proc_cpuinfo_output = reader.read()
    proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")
    # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "x86_64" architecture. Physical and logical cores and model name per core information are tracked easily on this platform.
    if "physical id" in proc_cpuinfo_output:
        cpu_model_names = []
        number_of_physical_cores = 0
        physical_id = 0
        physical_id_prev = 0
        for line in proc_cpuinfo_output_lines:
            if line.startswith("physical id"):
                physical_id_prev = physical_id
                physical_id = line.split(":")[1].strip()
            if physical_id != physical_id_prev and line.startswith("cpu cores"):
                number_of_physical_cores = number_of_physical_cores + int(line.split(":")[1].strip())
            if line.startswith("model name"):
                cpu_model_names.append(line.split(":")[1].strip())
        number_of_cpu_sockets = int(physical_id) + 1
    # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture. Physical and logical cores and model name per core information are not tracked easily on this platform. Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
    if "physical id" not in proc_cpuinfo_output:
        cpu_model_names = []
        number_of_physical_cores = number_of_logical_cores
        number_of_cpu_sockets = f'[{_tr("Unknown")}]'                                         # Initial value of "number_of_cpu_sockets". This value may not be detected on systems with ARM CPUs.
        # Some processors have "processor", some processors have "Processor" and some processors have both "processor" and "Processor". "processor" is used for core number and "Processor" is used for model name. But "model name" is used for model name on some ARM processors. Model name is repeated for all cores on these processors. "Processor" is used for one time for the processor.
        if "model name" in proc_cpuinfo_output:
            for line in proc_cpuinfo_output_lines:
                if line.startswith("model name"):
                    cpu_model_names.append(line.split(":")[1].strip())
        if "model name" not in proc_cpuinfo_output and "Processor" in proc_cpuinfo_output:
            for line in proc_cpuinfo_output_lines:
                if line.startswith("Processor"):
                    cpu_model_names.append(line.split(":")[1].strip())
        if len(cpu_model_names) == 1:
            cpu_model_names = cpu_model_names * number_of_logical_cores
        if "Processor" in proc_cpuinfo_output:
            number_of_cpu_sockets = 0
            number_of_cpu_sockets = number_of_cpu_sockets + 1
        # Some ARM processors do not have model name information in "/proc/cpuinfo" file.
        if cpu_model_names == []:
            cpu_model_names = [_tr("Unknown")]

    # Get current frequency of the selected CPU core
    try:
        with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_cur_freq") as reader:
            cpu_current_frequency_selected_core = float(reader.read().strip()) / 1000000
    except FileNotFoundError:
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
        proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(selected_cpu_core_number_only)].split("\n")
        for line in proc_cpuinfo_all_cores_lines:
            if line.startswith("cpu MHz"):
                cpu_current_frequency_selected_core = float(line.split(":")[1].strip()) / 1000
                break

    # Get number_of_total_threads and number_of_total_processes
    thread_count_list = []
    pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
    for pid in pid_list:
        try:                                                                                  # try-except is used in order to skip to the next loop without application error if a "FileNotFoundError" error is encountered when process is ended after process list is get.
            with open("/proc/" + pid + "/status") as reader:
                proc_status_output = reader.read()
        except (FileNotFoundError, ProcessLookupError) as me:
            continue
        thread_count_list.append(int(proc_status_output.split("\nThreads:", 1)[1].split("\n", 1)[0].strip()))    # Append number of threads of the process
    number_of_total_processes = len(thread_count_list)
    number_of_total_threads = sum(thread_count_list)

    # Get system up time (sut) information
    with open("/proc/uptime") as reader:
        sut_read = float(reader.read().split(" ")[0].strip())
    sut_days = sut_read/60/60/24
    sut_days_int = int(sut_days)
    sut_hours = (sut_days -sut_days_int) * 24
    sut_hours_int = int(sut_hours)
    sut_minutes = (sut_hours - sut_hours_int) * 60
    sut_minutes_int = int(sut_minutes)
    sut_seconds = (sut_minutes - sut_minutes_int) * 60
    sut_seconds_int = int(sut_seconds)

    # Set and update CPU tab label texts by using information get
    label1101.set_text(cpu_model_names[selected_cpu_core_number])
    label1102.set_text(selected_cpu_core)
    label1111.set_text(f'{number_of_total_processes} - {number_of_total_threads}')
    label1112.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
    label1103.set_text(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
    label1104.set_text(f'{cpu_current_frequency_selected_core:.2f} GHz')
    label1106.set_text(f'{number_of_cpu_sockets}')
    label1107.set_text(f'{number_of_physical_cores} - {number_of_logical_cores}')


# ----------------------------------- CPU - Run Function (runs initial and loop functions) -----------------------------------
def cpu_run_func(*args):                                                                      # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if "update_interval" not in globals():                                                    # To be able to run initial function for only one time
        GLib.idle_add(cpu_initial_func)
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 0:
        global cpu_glib_source, update_interval                                               # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            cpu_glib_source.destroy()                                                         # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        cpu_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(cpu_loop_func)
        cpu_glib_source.set_callback(cpu_run_func)
        cpu_glib_source.attach(GLib.MainContext.default())                                    # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
