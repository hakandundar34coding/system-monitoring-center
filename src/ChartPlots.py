#!/usr/bin/env python3

# ----------------------------------- ChartPlots - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def chart_plots_import_func():

    global Gtk, GLib, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread


    global MainGUI, Config, Performance
    import MainGUI, Config, Performance


# ----------------------------------- ChartPlots - ChartPlots GUI Function (draws chart by using a drawing area -This function is called automatically when there is changes/updates on the same window such as window resize, tab change, button click, widget updates, mouse hover on some widgets, window maximize/minimize, etc.-) -----------------------------------
def charts_gui_func():

    global drawingarea1101, drawingarea1201, drawingarea1202, drawingarea1301, drawingarea1302, drawingarea1401, drawingarea1501
    global drawingarea101, drawingarea102
    drawingarea1101 = MainGUI.builder.get_object('drawingarea1101')
    drawingarea1201 = MainGUI.builder.get_object('drawingarea1201')
    drawingarea1202 = MainGUI.builder.get_object('drawingarea1202')
    drawingarea1301 = MainGUI.builder.get_object('drawingarea1301')
    drawingarea1302 = MainGUI.builder.get_object('drawingarea1302')
    drawingarea1401 = MainGUI.builder.get_object('drawingarea1401')
    drawingarea1501 = MainGUI.builder.get_object('drawingarea1501')
    drawingarea101 = MainGUI.builder.get_object('drawingarea101')
    drawingarea102 = MainGUI.builder.get_object('drawingarea102')


# ----------------------------------- ChartPlots - Plot CPU usage average data as a Line Chart on "Performance" tab ----------------------------------- 
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


# ----------------------------------- ChartPlots - Plot CPU usage per core data as Bar Charts on "Performance" tab if "show cpu usage per core" setting is enabled. ----------------------------------- 
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


# ----------------------------------- ChartPlots - Plot RAM usage data as a Line Chart on "Performance" tab ----------------------------------- 
def on_drawingarea1201_draw(widget, chart1201):

    chart_data_history = Config.chart_data_history
    chart_x_axis = list(range(0, chart_data_history))
    ram_usage_percent = Performance.ram_usage_percent

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


# ----------------------------------- ChartPlots - Plot Swap usage data as a Bar Chart on "Performance" tab ----------------------------------- 
def on_drawingarea1202_draw(drawingarea1202, chart1202):

    try:
        swap_percent = Performance.swap_percent
    except:
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


# ----------------------------------- ChartPlots - Plot Disk read/write speed data as a Line Chart on "Performance" tab ----------------------------------- 
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
    if Config.plot_disk_read_speed == 1 and Config.plot_disk_write_speed == 0:
        chart1301_y_limit = 1.1 * (max(disk_write_speed) + 0.0000001)

    chart1301.set_dash([], 0)
    chart1301.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
    chart1301.rectangle(0, 0, chart1301_width, chart1301_height)
    chart1301.stroke()

    if Config.plot_disk_read_speed == 1:
        chart1301.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1301.move_to(chart1301_width*chart_x_axis[0]/(chart_data_history-1), chart1301_height - chart1301_height*disk_read_speed[0]/100)
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
        chart1301.move_to(chart1301_width*chart_x_axis[0]/(chart_data_history-1), chart1301_height - chart1301_height*disk_write_speed[0]/100)
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


# ----------------------------------- ChartPlots - Plot Disk usage data as a Bar Chart on "Performance" tab ----------------------------------- 
def on_drawingarea1302_draw(drawingarea1302, chart1302):

    try:
        disk_usage_percent = Performance.disk_usage_percent
    except:
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


# ----------------------------------- ChartPlots - Plot Network download/upload speed data as a Line Chart on "Performance" tab ----------------------------------- 
def on_drawingarea1401_draw(drawingarea1401, chart1401):

    chart_data_history = Config.chart_data_history
    chart_x_axis = list(range(0, chart_data_history))
    network_receive_speed = Performance.network_receive_speed[Performance.selected_network_card_number]
    network_send_speed = Performance.network_send_speed[Performance.selected_network_card_number]

    chart_line_color = Config.chart_line_color_network_speed_data
    chart_background_color = Config.chart_background_color_all_charts

    chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
    chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

    chart1401_width = Gtk.Widget.get_allocated_width(drawingarea1401)
    chart1401_height = Gtk.Widget.get_allocated_height(drawingarea1401)

    chart1401.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
    chart1401.rectangle(0, 0, chart1401_width, chart1401_height)
    chart1401.fill()

    chart1401.set_line_width(1)
    chart1401.set_dash([4, 3])
    chart1401.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
    for i in range(3):
        chart1401.move_to(0, chart1401_height/4*(i+1))
        chart1401.line_to(chart1401_width, chart1401_height/4*(i+1))
    for i in range(4):
        chart1401.move_to(chart1401_width/5*(i+1), 0)
        chart1401.line_to(chart1401_width/5*(i+1), chart1401_height)
    chart1401.stroke()

    chart1401_y_limit = 1.1 * ((max(max(network_receive_speed), max(network_send_speed))) + 0.0000001)
    if Config.plot_network_download_speed == 1 and Config.plot_network_upload_speed == 0:
        chart1401_y_limit = 1.1 * (max(network_receive_speed) + 0.0000001)
    if Config.plot_network_download_speed == 1 and Config.plot_network_upload_speed == 0:
        chart1401_y_limit = 1.1 * (max(network_send_speed) + 0.0000001)

    chart1401.set_dash([], 0)
    chart1401.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
    chart1401.rectangle(0, 0, chart1401_width, chart1401_height)
    chart1401.stroke()

    if Config.plot_network_download_speed == 1:
        chart1401.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1401.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_receive_speed[0]/100)
        for i in range(len(chart_x_axis) - 1):
            delta_x_chart1401a = (chart1401_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1401_width * chart_x_axis[i]/(chart_data_history-1))
            delta_y_chart1401a = (chart1401_height*network_receive_speed[i+1]/chart1401_y_limit) - (chart1401_height*network_receive_speed[i]/chart1401_y_limit)
            chart1401.rel_line_to(delta_x_chart1401a, -delta_y_chart1401a)

        chart1401.rel_line_to(10, 0)
        chart1401.rel_line_to(0, chart1401_height+10)
        chart1401.rel_line_to(-(chart1401_width+20), 0)
        chart1401.rel_line_to(0, -(chart1401_height+10))
        chart1401.close_path()
        chart1401.stroke()

    if Config.plot_network_upload_speed == 1:
        chart1401.set_dash([3, 3])
        chart1401.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_send_speed[0]/100)
        for i in range(len(chart_x_axis) - 1):
            delta_x_chart1401b = (chart1401_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1401_width * chart_x_axis[i]/(chart_data_history-1))
            delta_y_chart1401b = (chart1401_height*network_send_speed[i+1]/chart1401_y_limit) - (chart1401_height*network_send_speed[i]/chart1401_y_limit)
            chart1401.rel_line_to(delta_x_chart1401b, -delta_y_chart1401b)

        chart1401.rel_line_to(10, 0)
        chart1401.rel_line_to(0, chart1401_height+10)
        chart1401.rel_line_to(-(chart1401_width+20), 0)
        chart1401.rel_line_to(0, -(chart1401_height+10))
        chart1401.close_path()
        chart1401.stroke()


# ----------------------------------- ChartPlots - Plot FPS data as a Line Chart on "Performance" tab ----------------------------------- 
def on_drawingarea1501_draw(widget, chart1501):

    chart_data_history = Config.chart_data_history
    chart_x_axis = list(range(0, chart_data_history))
    fps_count = Performance.fps_count

    chart_line_color = Config.chart_line_color_fps
    chart_background_color = Config.chart_background_color_all_charts

    chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
    chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

    chart1501_width = Gtk.Widget.get_allocated_width(drawingarea1501)
    chart1501_height = Gtk.Widget.get_allocated_height(drawingarea1501)

    chart1501.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
    chart1501.rectangle(0, 0, chart1501_width, chart1501_height)
    chart1501.fill()

    chart1501.set_line_width(1)
    chart1501.set_dash([4, 3])
    chart1501.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
    for i in range(3):
        chart1501.move_to(0, chart1501_height/4*(i+1))
        chart1501.line_to(chart1501_width, chart1501_height/4*(i+1))
    for i in range(4):
        chart1501.move_to(chart1501_width/5*(i+1), 0)
        chart1501.line_to(chart1501_width/5*(i+1), chart1501_height)
    chart1501.stroke()

    chart1501.set_dash([], 0)
    chart1501.rectangle(0, 0, chart1501_width, chart1501_height)
    chart1501.stroke()

    chart1501.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
    chart1501.move_to(chart1501_width*chart_x_axis[0]/(chart_data_history-1), chart1501_height - chart1501_height*fps_count[0]/100)
    for i in range(len(chart_x_axis) - 1):
        delta_x_chart1501 = (chart1501_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1501_width * chart_x_axis[i]/(chart_data_history-1))
        delta_y_chart1501 = (chart1501_height*fps_count[i+1]/100) - (chart1501_height*fps_count[i]/100)
        chart1501.rel_line_to(delta_x_chart1501, -delta_y_chart1501)

    chart1501.rel_line_to(10, 0)
    chart1501.rel_line_to(0, chart1501_height+10)
    chart1501.rel_line_to(-(chart1501_width+20), 0)
    chart1501.rel_line_to(0, -(chart1501_height+10))
    chart1501.close_path()
    chart1501.stroke_preserve()
    chart1501.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
    chart1501.fill()



# ----------------------------------- ChartPlots - Plot Performance Summary as a Bar Chart On Headerbar - CPU usage data ----------------------------------- 
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


# ----------------------------------- ChartPlots - Plot Performance Summary as a Bar Chart On Headerbar - RAM usage data ----------------------------------- 
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


# ----------------------------------- ChartPlots - Plot Drawingarea Signal Connect Function (connects drawing area signals) ----------------------------------- 
def chart_plots_drawingarea_signal_connect_func():

    # These drawingarea signals are connected via a repeated threaded function in order to avoid "not defined" error for some variables in "Performance" module.
    # Some "Performance" module background and foreground function threads are checked if they are not alive before running this function.
    # Drawingarea functions run very fast and they could not find some variables in the first "Performance" module loop even if drawingarea function signals are connected
    # just after running "Performance" module foreground functions. This "thread not alive check" solution helps avoiding this errors.
    # This thread control is performed in every 1 milliseconds. Signals are connected if they are not alive.
    drawingarea101.connect("draw", on_drawingarea101_draw)
    drawingarea102.connect("draw", on_drawingarea102_draw)
    drawingarea1201.connect("draw", on_drawingarea1201_draw)
    drawingarea1202.connect("draw", on_drawingarea1202_draw)
    drawingarea1301.connect("draw", on_drawingarea1301_draw)
    drawingarea1302.connect("draw", on_drawingarea1302_draw)
    drawingarea1401.connect("draw", on_drawingarea1401_draw)
    drawingarea1501.connect("draw", on_drawingarea1501_draw)
    if Config.show_cpu_usage_per_core == 0:
        drawingarea1101.connect("draw", on_drawingarea1101_draw)
    # Connects different function to the drawingarea if "show cpu usage per core" setting is enabled
    if Config.show_cpu_usage_per_core == 1:
        drawingarea1101.connect("draw", on_drawingarea1101_draw_per_core)


# ----------------------------------- ChartPlots - Drawingarea Signal Connect Loop Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def chart_plots_drawingarea_signal_connect_loop_func():

    if not Performance.performance_background_initial_thread.is_alive():
        if not Performance.performance_foreground_initial_thread.is_alive():
            GLib.idle_add(chart_plots_drawingarea_signal_connect_func)
            return
    GLib.timeout_add(1, chart_plots_drawingarea_signal_connect_loop_func)


# ----------------------------------- ChartPlots - Thread Run Function (starts execution of the threads) -----------------------------------
def chart_plots_drawingarea_signal_connect_thread_func():

    chart_plots_drawingarea_signal_connect_thread = Thread(target=chart_plots_drawingarea_signal_connect_loop_func, daemon=True)
    chart_plots_drawingarea_signal_connect_thread.start()
