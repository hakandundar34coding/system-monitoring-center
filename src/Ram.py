#!/usr/bin/env python3

# ----------------------------------- RAM - RAM Tab Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def ram_import_func():

    global Gtk, GLib, Thread, os, Gdk

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib, Gdk
    from threading import Thread
    import os


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


# ----------------------------------- RAM - RAM GUI Function (the code of this module in order to avoid running them during module import and defines "RAM" tab GUI objects and functions/signals) -----------------------------------
def ram_gui_func():

    # RAM tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RamTab.ui")

    # RAM tab GUI objects
    global grid1201, drawingarea1201, drawingarea1202, button1201, label1201, label1202
    global label1203, label1204, label1205, label1206, label1207, label1208, label1209, label1210, eventbox1201, eventbox1202

    # RAM tab GUI objects - get
    grid1201 = builder.get_object('grid1201')
    drawingarea1201 = builder.get_object('drawingarea1201')
    drawingarea1202 = builder.get_object('drawingarea1202')
    button1201 = builder.get_object('button1201')
    label1201 = builder.get_object('label1201')
    label1202 = builder.get_object('label1202')
    label1203 = builder.get_object('label1203')
    label1204 = builder.get_object('label1204')
    label1205 = builder.get_object('label1205')
    label1206 = builder.get_object('label1206')
    label1207 = builder.get_object('label1207')
    label1208 = builder.get_object('label1208')
    label1209 = builder.get_object('label1209')
    label1210 = builder.get_object('label1210')
    eventbox1201 = builder.get_object('eventbox1201')
    eventbox1202 = builder.get_object('eventbox1202')


    # RAM tab GUI functions
    def on_button1201_clicked(widget):
        if 'RamMenu' not in globals():
            global RamMenu
            from . import RamMenu
            RamMenu.ram_menus_import_func()
            RamMenu.ram_menus_gui_func()
            RamMenu.popover1201p.set_relative_to(button1201)                                  # Set widget that popover menu will display at the edge of.
            RamMenu.popover1201p.set_position(1)                                              # Show popover menu at the right edge of the caller button.
        RamMenu.popover1201p.popup()                                                          # Show RAM tab popover GUI

    def on_eventbox1201_button_click_event(widget, event):                                    # Eventbox is used for defining signals for the widget ("Query..." label) placed on it.
        if event.button == 1:
            if 'RamHardwareInformation' not in globals():                                     # Check if "RamHardwareInformation" module is imported. Therefore it is not reimported for every mouse click on relevant GUI object on the RAM tab if "RamHardwareInformation" name is in globals().
                global RamHardwareInformation
                from . import RamHardwareInformation
                RamHardwareInformation.ram_hardware_information_import_func()
                RamHardwareInformation.ram_hardware_information_gui_func()
            RamHardwareInformation.ram_hardware_information_get_func()
            if RamHardwareInformation.memory_hardware_information_text != "":                 # This statement is used in order to avoid errors if user closes polkit window without entering password.
                RamHardwareInformation.window1201w.show()

    def on_eventbox1202_button_click_event(widget, event):                                    # Eventbox is used for defining signals for the widget ("Query..." label) placed on it.
        if event.button == 1:
            if 'RamSwapDetails' not in globals():                                             # Check if "RamSwapDetails" module is imported. Therefore it is not reimported for every mouse click on relevant GUI object on the RAM tab if "RamSwapDetails" name is in globals().
                global RamSwapDetails
                from . import RamSwapDetails
                RamSwapDetails.ram_swap_details_import_func()
                RamSwapDetails.ram_swap_details_gui_func()
            RamSwapDetails.ram_swap_details_get_func()                                        # Run this function in order to get RAM hardware information.
            RamSwapDetails.window1201w2.show()


    # ----------------------------------- RAM - Plot RAM usage data as a Line Chart ----------------------------------- 
    def on_drawingarea1201_draw(widget, chart1201):

        chart_data_history = Config.chart_data_history

        chart_x_axis = list(range(0, chart_data_history))
        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the RAM module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            ram_usage_percent = Performance.ram_usage_percent
        except AttributeError:
            return

        chart_line_color = Config.chart_line_color_ram_swap_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

        chart1201_width = Gtk.Widget.get_allocated_width(drawingarea1201)
        chart1201_height = Gtk.Widget.get_allocated_height(drawingarea1201)

        chart1201.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1201.rectangle(0, 0, chart1201_width, chart1201_height)
        chart1201.fill()

        chart1201.set_line_width(1)
        chart1201.set_dash([4, 3])
        chart1201.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        for i in range(3):
            chart1201.move_to(0, chart1201_height/4*(i+1))
            chart1201.line_to(chart1201_width, chart1201_height/4*(i+1))
        for i in range(4):
            chart1201.move_to(chart1201_width/5*(i+1), 0)
            chart1201.line_to(chart1201_width/5*(i+1), chart1201_height)
        chart1201.stroke()

        chart1201.set_dash([], 0)
        chart1201.rectangle(0, 0, chart1201_width, chart1201_height)
        chart1201.stroke()

        chart1201.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1201.move_to(chart1201_width*chart_x_axis[0]/(chart_data_history-1), chart1201_height - chart1201_height*ram_usage_percent[0]/100)
        for i in range(len(chart_x_axis) - 1):
            delta_x_chart1201 = (chart1201_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1201_width * chart_x_axis[i]/(chart_data_history-1))
            delta_y_chart1201 = (chart1201_height*ram_usage_percent[i+1]/100) - (chart1201_height*ram_usage_percent[i]/100)
            chart1201.rel_line_to(delta_x_chart1201, -delta_y_chart1201)

        chart1201.rel_line_to(10, 0)
        chart1201.rel_line_to(0, chart1201_height+10)
        chart1201.rel_line_to(-(chart1201_width+20), 0)
        chart1201.rel_line_to(0, -(chart1201_height+10))
        chart1201.close_path()
        chart1201.stroke_preserve()
        chart1201.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart1201.fill()


    # ----------------------------------- RAM - Plot Swap usage data as a Bar Chart ----------------------------------- 
    def on_drawingarea1202_draw(drawingarea1202, chart1202):

        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the RAM module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            swap_percent_check = swap_percent
        except NameError:
            return

        chart_line_color = Config.chart_line_color_ram_swap_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3]]

        chart1202_width = Gtk.Widget.get_allocated_width(drawingarea1202)
        chart1202_height = Gtk.Widget.get_allocated_height(drawingarea1202)

        chart1202.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1202.rectangle(0, 0, chart1202_width, chart1202_height)
        chart1202.fill()

        chart1202.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        chart1202.rectangle(0, 0, chart1202_width, chart1202_height)
        chart1202.stroke()
        chart1202.set_line_width(1)
        chart1202.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart1202.rectangle(0, 0, chart1202_width*swap_percent/100, chart1202_height)
        chart1202.fill()



    # RAM tab GUI functions - connect
    button1201.connect("clicked", on_button1201_clicked)
    drawingarea1201.connect("draw", on_drawingarea1201_draw)
    drawingarea1202.connect("draw", on_drawingarea1202_draw)
    eventbox1201.connect("button-press-event", on_eventbox1201_button_click_event)
    eventbox1202.connect("button-press-event", on_eventbox1202_button_click_event)


# ----------------------------------- RAM - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def ram_initial_func():

    ram_define_data_unit_converter_variables_func()                                           # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
    performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit

    # Get total_physical_ram value (this value is very similar to RAM hardware size which is a bit different than ram_total value)
    with open("/sys/devices/system/memory/block_size_bytes") as reader:                       # "memory block size" is read from this file and size of the blocks depend on architecture (For more information see: https://www.kernel.org/doc/html/latest/admin-guide/mm/memory-hotplug.html).
        block_size = int(reader.read().strip(), 16)                                           # Value in this file is in hex form and it is converted into integer (byte)
    total_online_memory = 0
    total_offline_memory = 0
    files_in_sys_devices_system_memory = os.listdir("/sys/devices/system/memory/")            # Number of folders (of which name start with "memory") in this folder is multiplied with the integer value of "block_size_bytes" file content (hex value).
    for file in files_in_sys_devices_system_memory:
        if os.path.isdir("/sys/devices/system/memory/" + file) and file.startswith("memory"):
            with open("/sys/devices/system/memory/" + file + "/online") as reader:
                if reader.read().strip() == "1":
                    total_online_memory = total_online_memory + block_size
                if reader.read().strip() == "0":
                    total_offline_memory = total_offline_memory + block_size
    total_physical_ram = (total_online_memory + total_offline_memory)                         # Summation of total online and offline memories gives RAM hardware size. RAM harware size and total RAM value get from proc file system of by using "free" command are not same thing. Because some of the RAM may be reserved for harware and/or by the OS kernel.
    # Get ram_total and swap_total values
    with open("/proc/meminfo") as reader:
        proc_memory_info_output_lines = reader.read().split("\n")
        for line in proc_memory_info_output_lines:
            if "MemTotal:" in line:
                ram_total = int(line.split()[1]) * 1024                                       # Values in this file are in "KiB" unit. These values are multiplied with 1024 in order to obtain byte (nearly) values.
            if "SwapTotal:" in line:
                swap_total = int(line.split()[1]) * 1024

    # Set RAM tab label texts by using information get
    label1201.set_text(_tr("Total Physical RAM: ") + str(ram_data_unit_converter_func(total_physical_ram, 0, 1)))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.
    label1202.set_text(_tr("Reserved Swap Memory: ") + str(ram_data_unit_converter_func(swap_total, 0, 1)))
    label1205.set_text(ram_data_unit_converter_func(ram_total, performance_ram_swap_data_unit, performance_ram_swap_data_precision))


# ----------------------------------- RAM - Get RAM Data Function (gets RAM data, shows on the labels on the GUI) -----------------------------------
def ram_loop_func():

    ram_used = Performance.ram_used
    ram_usage_percent = Performance.ram_usage_percent
    ram_available = Performance.ram_available
    ram_free = Performance.ram_free

    performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
    performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit
    global swap_percent

    drawingarea1201.queue_draw()
    drawingarea1202.queue_draw()

    # Get RAM usage values
    with open("/proc/meminfo") as reader:                                                     # Read total swap area and free swap area from /proc/meminfo file
        memory_info = reader.read().split("\n")
    for line in memory_info:
        if line.startswith("SwapTotal:"):
            swap_total = int(line.split()[1]) * 1024
        if line.startswith("SwapFree:"):
            swap_free = int(line.split()[1]) * 1024
    if swap_free != 0:                                                                        # Calculate values if swap memory exists.
        swap_used = swap_total - swap_free
        swap_percent = swap_used / swap_total * 100
    if swap_free == 0:                                                                        # Set values as "0" if swap memory does not exist.
        swap_used = 0
        swap_percent = 0

    # Set and update RAM tab label texts by using information get
    label1203.set_text(f'{ram_data_unit_converter_func(ram_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)} ({ram_usage_percent[-1]:.0f}%)')
    label1204.set_text(ram_data_unit_converter_func(ram_available, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
    label1206.set_text(ram_data_unit_converter_func(ram_free, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
    label1207.set_text(f'{swap_percent:.0f}%')
    label1208.set_text(f'{ram_data_unit_converter_func(swap_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)}')
    label1209.set_text(ram_data_unit_converter_func(swap_free, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
    label1210.set_text(ram_data_unit_converter_func((swap_total), performance_ram_swap_data_unit, performance_ram_swap_data_precision))


# ----------------------------------- RAM Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def ram_initial_thread_func():

    GLib.idle_add(ram_initial_func)


# ----------------------------------- RAM Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def ram_loop_thread_func(*args):                                                              # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1002.get_active() == True:
        global ram_glib_source, update_interval                                               # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            ram_glib_source.destroy()                                                         # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        ram_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(ram_loop_func)
        ram_glib_source.set_callback(ram_loop_thread_func)
        ram_glib_source.attach(GLib.MainContext.default())                                    # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- RAM Thread Run Function (starts execution of the threads) -----------------------------------
def ram_thread_run_func():

    if "update_interval" not in globals():                                                    # To be able to run initial thread for only one time
        ram_initial_thread = Thread(target=ram_initial_thread_func, daemon=True)
        ram_initial_thread.start()
        ram_initial_thread.join()
    ram_loop_thread = Thread(target=ram_loop_thread_func, daemon=True)
    ram_loop_thread.start()


# ----------------------------------- RAM - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def ram_define_data_unit_converter_variables_func():

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


# ----------------------------------- RAM - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def ram_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit in [0, 8]:                                                                        # "if unit in [0, 8]:" is about %25 faster than "if unit == 0 or unit == 8:".
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
