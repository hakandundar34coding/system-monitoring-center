#!/usr/bin/env python3

# ----------------------------------- Network - Network GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def network_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Performance
    import Config, Performance


# ----------------------------------- Network - Network GUI Function (the code of this module in order to avoid running them during module import and defines "Network" tab GUI objects and functions/signals) -----------------------------------
def network_gui_func():

    # Network tab GUI objects
    global grid1401, drawingarea1401, button1401, label1401, label1402
    global label1403, label1404, label1405, label1406, label1407, label1408, label1409, label1410, label1411, label1412


    # Network tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/NetworkTab.ui")

    # Network tab GUI objects - get
    grid1401 = builder.get_object('grid1401')
    drawingarea1401 = builder.get_object('drawingarea1401')
    button1401 = builder.get_object('button1401')
    label1401 = builder.get_object('label1401')
    label1402 = builder.get_object('label1402')
    label1403 = builder.get_object('label1403')
    label1404 = builder.get_object('label1404')
    label1405 = builder.get_object('label1405')
    label1406 = builder.get_object('label1406')
    label1407 = builder.get_object('label1407')
    label1408 = builder.get_object('label1408')
    label1409 = builder.get_object('label1409')
    label1410 = builder.get_object('label1410')
    label1411 = builder.get_object('label1411')
    label1412 = builder.get_object('label1412')


    # Network tab GUI functions
    def on_button1401_clicked(widget):
        if 'NetworkMenusGUI' not in globals():
            global NetworkMenusGUI
            import NetworkMenusGUI
            NetworkMenusGUI.network_menus_import_func()
            NetworkMenusGUI.network_menus_gui_func()
            NetworkMenusGUI.popover1401p.set_relative_to(button1401)                          # Set widget that popover menu will display at the edge of.
            NetworkMenusGUI.popover1401p.set_position(1)                                      # Show popover menu at the right edge of the caller button.
        NetworkMenusGUI.popover1401p.popup()                                                  # Show Network tab popover GUI

    # ----------------------------------- Network - Plot Network download/upload speed data as a Line Chart on "Network" tab ----------------------------------- 
    def on_drawingarea1401_draw(drawingarea1401, chart1401):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the Network module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            network_receive_speed = Performance.network_receive_speed[Performance.selected_network_card_number]
            network_send_speed = Performance.network_send_speed[Performance.selected_network_card_number]
        except AttributeError:
            return

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
        if Config.plot_network_download_speed == 0 and Config.plot_network_upload_speed == 1:
            chart1401_y_limit = 1.1 * (max(network_send_speed) + 0.0000001)

        chart1401.set_dash([], 0)
        chart1401.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1401.rectangle(0, 0, chart1401_width, chart1401_height)
        chart1401.stroke()

        if Config.plot_network_download_speed == 1:
            chart1401.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            chart1401.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_receive_speed[0]/chart1401_y_limit)
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
            chart1401.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_send_speed[0]/chart1401_y_limit)
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



    # Network tab GUI functions - connect
    button1401.connect("clicked", on_button1401_clicked)
    drawingarea1401.connect("draw", on_drawingarea1401_draw)
