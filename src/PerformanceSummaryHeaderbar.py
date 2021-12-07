#!/usr/bin/env python3

# ----------------------------------- Performance Summary Headerbar - Performance Summary Headerbar GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_summary_headerbar_import_func():

    global Gtk, GLib, Thread, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os


    global Config, Performance
    import Config, Performance


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


# ----------------------------------- Performance Summary Headerbar - Performance Summary Headerbar Grid GUI Function (the code of this module in order to avoid running them during module import and defines "Performance Summary Headerbar" grid GUI objects and functions/signals) -----------------------------------
def performance_summary_headerbar_gui_func():

    # Performance Summary Headerbar Grid GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/PerformanceSummaryHeaderBarGrid.ui")

    # Performance Summary Headerbar Grid GUI objects
    global grid101, drawingarea101, drawingarea102, label101, label102

    # Performance Summary Headerbar Grid GUI objects - get
    grid101 = builder.get_object('grid101')
    drawingarea101 = builder.get_object('drawingarea101')
    drawingarea102 = builder.get_object('drawingarea102')
    label101 = builder.get_object('label101')
    label102 = builder.get_object('label102')


    # Performance Summary Headerbar Grid GUI functions
    # ----------------------------------- Performance Summary Headerbar - Plot Performance Summary as a Bar Chart On Headerbar - CPU usage data ----------------------------------- 
    def on_drawingarea101_draw(widget, chart101):

        try:
            cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
        except AttributeError:
            return

        chart_line_color = Config.chart_line_color_cpu_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3]]

        chart101_width = Gtk.Widget.get_allocated_width(drawingarea101)
        chart101_height = Gtk.Widget.get_allocated_height(drawingarea101)

        chart101.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart101.rectangle(0, 0, chart101_width, chart101_height)
        chart101.fill()

        chart101.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        chart101.rectangle(0, 0, chart101_width, chart101_height)
        chart101.stroke()

        chart101.set_line_width(1)
        chart101.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart101.rectangle(0, 0, chart101_width*cpu_usage_percent_ave[-1]/100, chart101_height)
        chart101.fill()


    # ----------------------------------- Performance Summary Headerbar - Plot Performance Summary as a Bar Chart On Headerbar - RAM usage data ----------------------------------- 
    def on_drawingarea102_draw(widget, chart102):

        try:
            ram_usage_percent = Performance.ram_usage_percent
        except AttributeError:
            return

        chart_line_color = Config.chart_line_color_ram_swap_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3]]

        chart102_width = Gtk.Widget.get_allocated_width(drawingarea102)
        chart102_height = Gtk.Widget.get_allocated_height(drawingarea102)

        chart102.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart102.rectangle(0, 0, chart102_width, chart102_height)
        chart102.fill()

        chart102.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        chart102.rectangle(0, 0, chart102_width, chart102_height)
        chart102.stroke()

        chart102.set_line_width(1)
        chart102.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart102.rectangle(0, 0, chart102_width*ram_usage_percent[-1]/100, chart102_height)
        chart102.fill()


    # Performance Summary Headerbar Grid tab GUI functions - connect
    drawingarea101.connect("draw", on_drawingarea101_draw)
    drawingarea102.connect("draw", on_drawingarea102_draw)


# ----------------------------------- Performance Summary Headerbar - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def performance_summary_headerbar_initial_func():

    performance_summary_headerbar_define_data_unit_converter_variables_func()                 # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.


# ----------------------------------- Performance Summary Headerbar - Get Performance Summary Headerbar Data Function (gets Performance Summary Headerbar data, shows on the labels on the GUI) -----------------------------------
def performance_summary_headerbar_loop_func():

    # Update performance data on the headerbar
    selected_disk_number = Performance.selected_disk_number
    selected_network_card_number = Performance.selected_network_card_number
    drawingarea101.queue_draw()
    drawingarea102.queue_draw()
    label101.set_text(f'{performance_summary_headerbar_data_unit_converter_func((Performance.disk_read_speed[selected_disk_number][-1] + Performance.disk_write_speed[selected_disk_number][-1]), 0, 0)}/s')
    label102.set_text(f'{performance_summary_headerbar_data_unit_converter_func((Performance.network_receive_speed[selected_network_card_number][-1] + Performance.network_send_speed[selected_network_card_number][-1]), 0, 0)}/s')


# ----------------------------------- Performance Summary Headerbar Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def performance_summary_headerbar_initial_thread_func():

    GLib.idle_add(performance_summary_headerbar_initial_func)


# ----------------------------------- Performance Summary Headerbar Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def performance_summary_headerbar_loop_thread_func(*args):

    if Config.performance_summary_on_the_headerbar == 1:
        global performance_summary_headerbar_glib_source, update_interval                     # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            performance_summary_headerbar_glib_source.destroy()                               # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        performance_summary_headerbar_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(performance_summary_headerbar_loop_func)
        performance_summary_headerbar_glib_source.set_callback(performance_summary_headerbar_loop_thread_func)
        performance_summary_headerbar_glib_source.attach(GLib.MainContext.default())          # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- Performance Summary Headerbar Thread Run Function (starts execution of the threads) -----------------------------------
def performance_summary_headerbar_thread_run_func():

    if "update_interval" not in globals():                                                    # To be able to run initial thread for only one time
        performance_summary_headerbar_initial_thread = Thread(target=performance_summary_headerbar_initial_thread_func, daemon=True)
        performance_summary_headerbar_initial_thread.start()
        performance_summary_headerbar_initial_thread.join()
    performance_summary_headerbar_loop_thread = Thread(target=performance_summary_headerbar_loop_thread_func, daemon=True)
    performance_summary_headerbar_loop_thread.start()


# ----------------------------------- Performance Summary Headerbar - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def performance_summary_headerbar_define_data_unit_converter_variables_func():


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


# ----------------------------------- Performance Summary Headerbar - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def performance_summary_headerbar_data_unit_converter_func(data, unit, precision):

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
