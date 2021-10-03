#!/usr/bin/env python3

# ----------------------------------- Performance Summary Headerbar - Performance Summary Headerbar Grid GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_summary_headerbar_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Performance
    import Config, Performance


# ----------------------------------- Performance Summary Headerbar - Performance Summary Headerbar Grid GUI Function (the code of this module in order to avoid running them during module import and defines "Performance Summary Headerbar" grid GUI objects and functions/signals) -----------------------------------
def performance_summary_headerbar_gui_func():

    # Performance Summary Headerbar Grid GUI objects
    global grid101, drawingarea101, drawingarea102, label101, label102


    # Performance Summary Headerbar Grid GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/PerformanceSummaryHeaderBarGrid.ui")

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
