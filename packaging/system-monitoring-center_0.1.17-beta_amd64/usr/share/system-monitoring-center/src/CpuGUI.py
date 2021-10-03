#!/usr/bin/env python3

# ----------------------------------- CPU - CPU GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def cpu_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Performance
    import Config, Performance


# ----------------------------------- CPU - CPU GUI Function (the code of this module in order to avoid running them during module import and defines "CPU" tab GUI objects and functions/signals) -----------------------------------
def cpu_gui_func():

    # CPU tab GUI objects
    global grid1101, drawingarea1101, button1101, label1101, label1102
    global label1103, label1104, label1105, label1106, label1107, label1108, label1109, label1110, label1111, label1112, label1113


    # CPU tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/CpuTab.ui")

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
        if 'CpuMenusGUI' not in globals():
            global CpuMenusGUI
            import CpuMenusGUI
            CpuMenusGUI.cpu_menus_import_func()
            CpuMenusGUI.cpu_menus_gui_func()
            CpuMenusGUI.popover1101p.set_relative_to(button1101)                              # Set widget that popover menu will display at the edge of.
            CpuMenusGUI.popover1101p.set_position(1)                                          # Show popover menu at the right edge of the caller button in order not to hide CPU usage percentage when menu is shown. Becuse there is CPU usage percentage precision setting and user may want to see visual changes just in time.
        CpuMenusGUI.popover1101p.popup()                                                      # Show CPU tab popover GUI

    # CPU tab GUI functions - connect
    button1101.connect("clicked", on_button1101_clicked)
    if Config.show_cpu_usage_per_core == 0:
        drawingarea1101.connect("draw", on_drawingarea1101_draw)
    # Connects different function to the drawingarea if "show cpu usage per core" setting is enabled
    if Config.show_cpu_usage_per_core == 1:
        drawingarea1101.connect("draw", on_drawingarea1101_draw_per_core)



# ----------------------------------- CPU - Plot CPU usage average data as a Line Chart on "RAM" tab ----------------------------------- 
def on_drawingarea1101_draw(widget, chart1101):

    # Get values from "Config and Peformance" modules and use this defined values in order to avoid multiple uses of variables from another module since CPU usage is higher for this way.
    chart_data_history = Config.chart_data_history
    chart_x_axis = list(range(0, chart_data_history))
    try:
        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
    except AttributeError:
        return
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


# ----------------------------------- CPU - Plot CPU usage per core data as Bar Charts on "RAM" tab if "show cpu usage per core" setting is enabled. ----------------------------------- 
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
    chart1101_height_per_core = chart1101_height      # Chart height and chart height per core is same because charts for all cores will be bars next to each other (like columns).
    chart1101_width_per_core_w_spacing = chart1101_width_per_core - 10     # Spacing 5 from left an right
    chart1101_height_per_core_w_spacing = chart1101_height - 10            # Spacing 5 from top an bottom

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
        chart1101.show_text(f'{cpu_core}')
