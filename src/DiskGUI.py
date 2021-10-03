#!/usr/bin/env python3

# ----------------------------------- Disk - Disk GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def disk_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Performance, Disk
    import Config, Performance, Disk


# ----------------------------------- Disk - Disk GUI Function (the code of this module in order to avoid running them during module import and defines "Disk" tab GUI objects and functions/signals) -----------------------------------
def disk_gui_func():

    # Disk tab GUI objects
    global grid1301, drawingarea1301, drawingarea1302, button1301, label1301, label1302
    global label1303, label1304, label1305, label1306, label1307, label1308, label1309, label1310, label1311, label1312


    # Disk tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskTab.ui")

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
        if 'DiskMenusGUI' not in globals():
            global DiskMenusGUI
            import DiskMenusGUI
            DiskMenusGUI.disk_menus_import_func()
            DiskMenusGUI.disk_menus_gui_func()
            DiskMenusGUI.popover1301p.set_relative_to(button1301)                             # Set widget that popover menu will display at the edge of.
            DiskMenusGUI.popover1301p.set_position(1)                                         # Show popover menu at the right edge of the caller button.
        DiskMenusGUI.popover1301p.popup()                                                     # Show Disk tab popover GUI

    # ----------------------------------- Disk - Plot Disk read/write speed data as a Line Chart on "Disk" tab ----------------------------------- 
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


    # ----------------------------------- Disk - Plot Disk usage data as a Bar Chart on "Disk" tab ----------------------------------- 
    def on_drawingarea1302_draw(drawingarea1302, chart1302):

        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the Disk module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            disk_usage_percent = Disk.disk_usage_percent
        except AttributeError:
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
