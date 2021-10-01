#!/usr/bin/env python3

# ----------------------------------- Sensors - Sensors GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def sensors_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Sensors, SensorsMenusGUI
    import Config, Sensors, SensorsMenusGUI


# ----------------------------------- Sensors - Sensors GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab GUI objects and functions/signals) -----------------------------------
def sensors_gui_func():

    # Sensors tab GUI objects
    global grid1601, treeview1601, searchentry1601, button1601, button1603
    global radiobutton1601, radiobutton1602, radiobutton1603
    global label1601


    # Sensors tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SensorsTab.ui")

    # Sensors tab GUI objects - get
    grid1601 = builder.get_object('grid1601')
    treeview1601 = builder.get_object('treeview1601')
    searchentry1601 = builder.get_object('searchentry1601')
    button1601 = builder.get_object('button1601')
    button1603 = builder.get_object('button1603')
    radiobutton1601 = builder.get_object('radiobutton1601')
    radiobutton1602 = builder.get_object('radiobutton1602')
    radiobutton1603 = builder.get_object('radiobutton1603')
    label1601 = builder.get_object('label1601')


    # Sensors tab GUI functions
    def on_treeview1601_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Sensors.sensors_treeview_column_order_width_row_sorting_func()

    def on_searchentry1601_changed(widget):
        radiobutton1601.set_active(True)
        Sensors.sensors_treeview_filter_search_func()

    def on_button1601_clicked(widget):                                                        # "Sensors Tab Customizations" button
        PerformanceMenusGUI.popover1601p.popup()

    def on_radiobutton1601_toggled(widget):                                                   # "Show all sensors" radiobutton
        if radiobutton1601.get_active() == True:
            Sensors.sensors_treeview_filter_show_all_func()

    def on_radiobutton1602_toggled(widget):                                                   # "Show all temperature sensors" radiobutton
        if radiobutton1602.get_active() == True:
            Sensors.sensors_treeview_filter_show_all_func()
            Sensors.sensors_treeview_filter_only_temperature_sensors_func()

    def on_radiobutton1603_toggled(widget):                                                   # "Show all fan sensors" radiobutton
        if radiobutton1603.get_active() == True:
            Sensors.sensors_treeview_filter_show_all_func()
            Sensors.sensors_treeview_filter_only_fan_sensors_func()

    def on_button1603_clicked(widget):
        SensorsMenusGUI.popover1601p2.popup()



    # Sensors tab GUI functions - connect
    searchentry1601.connect("changed", on_searchentry1601_changed)
    button1603.connect("clicked", on_button1603_clicked)
    radiobutton1601.connect("toggled", on_radiobutton1601_toggled)
    radiobutton1602.connect("toggled", on_radiobutton1602_toggled)
    radiobutton1603.connect("toggled", on_radiobutton1603_toggled)


    # Sensors Tab on Sensors Tab - Treeview Properties
    treeview1601.set_activate_on_single_click(True)
    treeview1601.set_show_expanders(False)                                                    # This command is used for hiding expanders (arrows) at the beginning of the rows. For "Sensors" tab, "child rows" are not used and there is no need for these expanders (they are shown as empty spaces in this situation).
    treeview1601.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview1601.set_headers_clickable(True)
    treeview1601.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview1601.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview1601.set_tooltip_column(2)
