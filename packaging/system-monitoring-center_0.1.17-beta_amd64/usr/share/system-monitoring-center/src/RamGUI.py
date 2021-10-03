#!/usr/bin/env python3

# ----------------------------------- RAM - RAM GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def ram_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Performance, Ram
    import Config, Performance, Ram


# ----------------------------------- RAM - RAM GUI Function (the code of this module in order to avoid running them during module import and defines "RAM" tab GUI objects and functions/signals) -----------------------------------
def ram_gui_func():

    # RAM tab GUI objects
    global grid1201, drawingarea1201, drawingarea1202, button1201, label1201, label1202
    global label1203, label1204, label1205, label1206, label1207, label1208, label1209, label1210


    # RAM tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RamTab.ui")

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


    # RAM tab GUI functions
    def on_button1201_clicked(widget):
        if 'RamMenusGUI' not in globals():
            global RamMenusGUI
            import RamMenusGUI
            RamMenusGUI.ram_menus_import_func()
            RamMenusGUI.ram_menus_gui_func()
            RamMenusGUI.popover1201p.set_relative_to(button1201)                              # Set widget that popover menu will display at the edge of.
            RamMenusGUI.popover1201p.set_position(1)                                          # Show popover menu at the right edge of the caller button.
        RamMenusGUI.popover1201p.popup()                                                      # Show RAM tab popover GUI

    # ----------------------------------- RAM - Plot RAM usage data as a Line Chart on "RAM" tab ----------------------------------- 
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


    # ----------------------------------- RAM - Plot Swap usage data as a Bar Chart on "RAM" tab ----------------------------------- 
    def on_drawingarea1202_draw(drawingarea1202, chart1202):

        try:
            swap_percent = Ram.swap_percent
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



    # RAM tab GUI functions - connect
    button1201.connect("clicked", on_button1201_clicked)
    drawingarea1201.connect("draw", on_drawingarea1201_draw)
    drawingarea1202.connect("draw", on_drawingarea1202_draw)
