#!/usr/bin/env python3

# ----------------------------------- Performance Summary Headerbar - Performance Summary Headerbar GUI Import Function -----------------------------------
def performance_summary_headerbar_import_func():

    global Gtk, GLib, os

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gtk, GLib
    import os


    global Config, Performance
    import Config, Performance


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Performance Summary Headerbar - Performance Summary Headerbar Grid GUI Function -----------------------------------
def performance_summary_headerbar_gui_func():

    # Performance Summary Headerbar Grid GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/PerformanceSummaryHeaderBarGrid.ui")

    # Performance Summary Headerbar Grid GUI objects
    global grid101, drawingarea101, drawingarea102, label101, label102, label103, label104, label105, label106

    # Performance Summary Headerbar Grid GUI objects - get
    grid101 = builder.get_object('grid101')
    drawingarea101 = builder.get_object('drawingarea101')
    drawingarea102 = builder.get_object('drawingarea102')
    label101 = builder.get_object('label101')
    label102 = builder.get_object('label102')
    label103 = builder.get_object('label103')
    label104 = builder.get_object('label104')
    label105 = builder.get_object('label105')
    label106 = builder.get_object('label106')


    # Performance Summary Headerbar Grid GUI functions
    # ----------------------------------- Performance Summary Headerbar - Plot Performance Summary as a Bar Chart On Headerbar - CPU usage data ----------------------------------- 
    def on_drawingarea101_draw(widget, chart101):

        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave

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

        ram_usage_percent = Performance.ram_usage_percent

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


# ----------------------------------- Performance Summary Headerbar - Initial Function -----------------------------------
def performance_summary_headerbar_initial_func():

    # Set empty characters at the right side of the labels
    label103.set_text(f'{_tr("CPU"):<5}')
    label104.set_text(f'{_tr("RAM"):<5}')
    label105.set_text(f'{_tr("Disk"):<10}')                                                   # Empty characters are placed at right side of the label by using "f'value:<[number of characters]'" in order to prevent movement of the label when data numbers change. Total length of the string is set as [number of characters] characters if actual length is smaller. This code has no effect if length of the string equals to this value or bigger.
    label106.set_text(f'{_tr("Network"):<10}')

    performance_summary_headerbar_define_data_unit_converter_variables_func()                 # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.


# ----------------------------------- Performance Summary Headerbar - Get Performance Summary Headerbar Data Function -----------------------------------
def performance_summary_headerbar_loop_func():

    # Update performance data on the headerbar
    selected_disk_number = Performance.selected_disk_number
    selected_network_card_number = Performance.selected_network_card_number
    drawingarea101.queue_draw()
    drawingarea102.queue_draw()
    label101.set_text(f'{performance_summary_headerbar_data_unit_converter_func((Performance.disk_read_speed[selected_disk_number][-1] + Performance.disk_write_speed[selected_disk_number][-1]), 0, 0)}/s')
    label102.set_text(f'{performance_summary_headerbar_data_unit_converter_func((Performance.network_receive_speed[selected_network_card_number][-1] + Performance.network_send_speed[selected_network_card_number][-1]), 0, 0)}/s')


# ----------------------------------- Performance Summary Headerbar - Run Function -----------------------------------
def performance_summary_headerbar_run_func(*args):

    if "update_interval" not in globals():
        GLib.idle_add(performance_summary_headerbar_initial_func)
    if Config.performance_summary_on_the_headerbar == 1:
        global performance_summary_headerbar_glib_source, update_interval
        try:
            performance_summary_headerbar_glib_source.destroy()
        except NameError:
            pass
        update_interval = Config.update_interval
        performance_summary_headerbar_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(performance_summary_headerbar_loop_func)
        performance_summary_headerbar_glib_source.set_callback(performance_summary_headerbar_run_func)
        performance_summary_headerbar_glib_source.attach(GLib.MainContext.default())


# ----------------------------------- Performance Summary Headerbar - Define Data Unit Converter Variables Function -----------------------------------
def performance_summary_headerbar_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Performance Summary Headerbar - Data Unit Converter Function -----------------------------------
def performance_summary_headerbar_data_unit_converter_func(data, unit, precision):

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
