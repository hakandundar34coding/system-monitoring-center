#!/usr/bin/env python3

# ----------------------------------- GPU - GPU GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def gpu_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Performance, Gpu
    import Config, Performance, Gpu 


# ----------------------------------- GPU - GPU GUI Function (the code of this module in order to avoid running them during module import and defines "GPU" tab GUI objects and functions/signals) -----------------------------------
def gpu_gui_func():

    # GPU tab GUI objects
    global grid1501, drawingarea1501, button1501, label1501, label1502
    global label1503, label1504, label1505, label1506, label1507, label1508, label1509, label1510, label1511, label1512
    global glarea1501


    # GPU tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuTab.ui")

    # GPU tab GUI objects - get
    grid1501 = builder.get_object('grid1501')
    drawingarea1501 = builder.get_object('drawingarea1501')
    button1501 = builder.get_object('button1501')
    label1501 = builder.get_object('label1501')
    label1502 = builder.get_object('label1502')
    label1503 = builder.get_object('label1503')
    label1504 = builder.get_object('label1504')
    label1505 = builder.get_object('label1505')
    label1506 = builder.get_object('label1506')
    label1507 = builder.get_object('label1507')
    label1508 = builder.get_object('label1508')
    label1509 = builder.get_object('label1509')
    label1510 = builder.get_object('label1510')
    label1511 = builder.get_object('label1511')
    label1512 = builder.get_object('label1512')
    glarea1501 = builder.get_object('glarea1501')


    # GPU tab GUI functions
    def on_button1501_clicked(widget):
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                      # Get gpu/graphics card list and set selected gpu
        if 'GpuMenusGUI' not in globals():
            global GpuMenusGUI
            import GpuMenusGUI
            GpuMenusGUI.gpu_menus_import_func()
            GpuMenusGUI.gpu_menus_gui_func()
            GpuMenusGUI.popover1501p.set_relative_to(button1501)                              # Set widget that popover menu will display at the edge of.
            GpuMenusGUI.popover1501p.set_position(1)                                          # Show popover menu at the right edge of the caller button.
        GpuMenusGUI.popover1501p.popup()                                                      # Show GPU tab popover GUI


    # ----------------------------------- GPU - Plot FPS data as a Line Chart on "GPU" tab ----------------------------------- 
    def on_drawingarea1501_draw(widget, chart1501):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))
        try:
            fps_count = Gpu.fps_count
        except AttributeError:
            return

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



    # GPU tab GUI functions - connect
    button1501.connect("clicked", on_button1501_clicked)
    drawingarea1501.connect("draw", on_drawingarea1501_draw)
