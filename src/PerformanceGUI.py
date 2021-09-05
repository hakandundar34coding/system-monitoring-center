#!/usr/bin/env python3

# ----------------------------------- Performance - Performance GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_gui_import_func():

    global Gtk, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import subprocess


    global Config, MainGUI, Performance, PerformanceMenusGUI, Sensors
    import Config, MainGUI, Performance, PerformanceMenusGUI, Sensors


# ----------------------------------- Performance - Performance GUI Function (the code of this module in order to avoid running them during module import and defines "Performance" tab GUI objects and functions/signals) -----------------------------------
def performance_gui_func():

    # Performance tab GUI objects
    global stack1001
    global radiobutton1001, radiobutton1002, radiobutton1003, radiobutton1004, radiobutton1005, radiobutton1006, radiobutton1007, radiobutton1008
    global grid1001, grid1002, grid1003, grid1004, grid1005, grid1006, grid1007, grid1008

    # CPU tab GUI objects
    global button1101, label1101, label1102
    global label1103, label1104, label1105, label1106, label1107, label1108, label1109, label1110, label1111, label1112
    global grid1101

    # RAM tab GUI objects
    global button1201, label1201, label1202
    global label1203, label1204, label1205, label1206, label1207, label1208, label1209, label1210

    # Disk tab GUI objects
    global button1301, label1301, label1302
    global label1303, label1304, label1305, label1306, label1307, label1308, label1309, label1310, label1311, label1312

    # Network tab GUI objects
    global button1401, label1401, label1402
    global label1403, label1404, label1405, label1406, label1407, label1408, label1409, label1410, label1411, label1412

    # GPU tab GUI objects
    global button1501, label1501, label1502
    global label1503, label1504, label1505, label1506, label1507, label1508, label1509, label1510, label1511, label1512
    global glarea1501

    # Sensors tab GUI objects
    global treeview1601, searchentry1601, button1601, button1603
    global radiobutton1601, radiobutton1602, radiobutton1603
    global label1601


    # Performance tab GUI objects - get
    stack1001 = MainGUI.builder.get_object('stack1001')
    radiobutton1001 = MainGUI.builder.get_object('radiobutton1001')
    radiobutton1002 = MainGUI.builder.get_object('radiobutton1002')
    radiobutton1003 = MainGUI.builder.get_object('radiobutton1003')
    radiobutton1004 = MainGUI.builder.get_object('radiobutton1004')
    radiobutton1005 = MainGUI.builder.get_object('radiobutton1005')
    radiobutton1006 = MainGUI.builder.get_object('radiobutton1006')
    radiobutton1007 = MainGUI.builder.get_object('radiobutton1007')
    radiobutton1008 = MainGUI.builder.get_object('radiobutton1008')
    grid1001 = MainGUI.builder.get_object('grid1001')
    grid1002 = MainGUI.builder.get_object('grid1002')
    grid1003 = MainGUI.builder.get_object('grid1003')
    grid1004 = MainGUI.builder.get_object('grid1004')
    grid1005 = MainGUI.builder.get_object('grid1005')
    grid1006 = MainGUI.builder.get_object('grid1006')
    grid1007 = MainGUI.builder.get_object('grid1007')
    grid1008 = MainGUI.builder.get_object('grid1008')

    # CPU tab GUI objects - get
    button1101 = MainGUI.builder.get_object('button1101')
    label1101 = MainGUI.builder.get_object('label1101')
    label1102 = MainGUI.builder.get_object('label1102')
    label1103 = MainGUI.builder.get_object('label1103')
    label1104 = MainGUI.builder.get_object('label1104')
    label1105 = MainGUI.builder.get_object('label1105')
    label1106 = MainGUI.builder.get_object('label1106')
    label1107 = MainGUI.builder.get_object('label1107')
    label1108 = MainGUI.builder.get_object('label1108')
    label1109 = MainGUI.builder.get_object('label1109')
    label1110 = MainGUI.builder.get_object('label1110')
    label1111 = MainGUI.builder.get_object('label1111')
    label1112 = MainGUI.builder.get_object('label1112')
    grid1101 = MainGUI.builder.get_object('grid1101')

    # RAM tab GUI objects - get
    button1201 = MainGUI.builder.get_object('button1201')
    label1201 = MainGUI.builder.get_object('label1201')
    label1202 = MainGUI.builder.get_object('label1202')
    label1203 = MainGUI.builder.get_object('label1203')
    label1204 = MainGUI.builder.get_object('label1204')
    label1205 = MainGUI.builder.get_object('label1205')
    label1206 = MainGUI.builder.get_object('label1206')
    label1207 = MainGUI.builder.get_object('label1207')
    label1208 = MainGUI.builder.get_object('label1208')
    label1209 = MainGUI.builder.get_object('label1209')
    label1210 = MainGUI.builder.get_object('label1210')

    # Disk tab GUI objects - get
    button1301 = MainGUI.builder.get_object('button1301')
    label1301 = MainGUI.builder.get_object('label1301')
    label1302 = MainGUI.builder.get_object('label1302')
    label1303 = MainGUI.builder.get_object('label1303')
    label1304 = MainGUI.builder.get_object('label1304')
    label1305 = MainGUI.builder.get_object('label1305')
    label1306 = MainGUI.builder.get_object('label1306')
    label1307 = MainGUI.builder.get_object('label1307')
    label1308 = MainGUI.builder.get_object('label1308')
    label1309 = MainGUI.builder.get_object('label1309')
    label1310 = MainGUI.builder.get_object('label1310')
    label1311 = MainGUI.builder.get_object('label1311')
    label1312 = MainGUI.builder.get_object('label1312')

    # Network tab GUI objects - get
    button1401 = MainGUI.builder.get_object('button1401')
    label1401 = MainGUI.builder.get_object('label1401')
    label1402 = MainGUI.builder.get_object('label1402')
    label1403 = MainGUI.builder.get_object('label1403')
    label1404 = MainGUI.builder.get_object('label1404')
    label1405 = MainGUI.builder.get_object('label1405')
    label1406 = MainGUI.builder.get_object('label1406')
    label1407 = MainGUI.builder.get_object('label1407')
    label1408 = MainGUI.builder.get_object('label1408')
    label1409 = MainGUI.builder.get_object('label1409')
    label1410 = MainGUI.builder.get_object('label1410')
    label1411 = MainGUI.builder.get_object('label1411')
    label1412 = MainGUI.builder.get_object('label1412')

    # GPU tab GUI objects - get
    button1501 = MainGUI.builder.get_object('button1501')
    label1501 = MainGUI.builder.get_object('label1501')
    label1502 = MainGUI.builder.get_object('label1502')
    label1503 = MainGUI.builder.get_object('label1503')
    label1504 = MainGUI.builder.get_object('label1504')
    label1505 = MainGUI.builder.get_object('label1505')
    label1506 = MainGUI.builder.get_object('label1506')
    label1507 = MainGUI.builder.get_object('label1507')
    label1508 = MainGUI.builder.get_object('label1508')
    label1509 = MainGUI.builder.get_object('label1509')
    label1510 = MainGUI.builder.get_object('label1510')
    label1511 = MainGUI.builder.get_object('label1511')
    label1512 = MainGUI.builder.get_object('label1512')
    glarea1501 = MainGUI.builder.get_object('glarea1501')

    # Sensors tab GUI objects - get
    treeview1601 = MainGUI.builder.get_object('treeview1601')
    searchentry1601 = MainGUI.builder.get_object('searchentry1601')
    button1601 = MainGUI.builder.get_object('button1601')
    button1603 = MainGUI.builder.get_object('button1603')
    radiobutton1601 = MainGUI.builder.get_object('radiobutton1601')
    radiobutton1602 = MainGUI.builder.get_object('radiobutton1602')
    radiobutton1603 = MainGUI.builder.get_object('radiobutton1603')
    label1601 = MainGUI.builder.get_object('label1601')


    # Performance tab GUI functions
    def on_treeview1601_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Sensors.sensors_treeview_column_order_width_row_sorting_func()

    def on_radiobutton1001_toggled(widget):
        if radiobutton1001.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1002_toggled(widget):
        if radiobutton1002.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1003_toggled(widget):
        if radiobutton1003.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1004_toggled(widget):
        if radiobutton1004.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1005_toggled(widget):
        if radiobutton1005.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1006_toggled(widget):
        if radiobutton1006.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1007_toggled(widget):
        if radiobutton1007.get_active() == True:
            performance_gui_function_run_func()

    def on_radiobutton1008_toggled(widget):
        if radiobutton1008.get_active() == True:
            performance_gui_function_run_func()


    # CPU tab GUI functions
    def on_button1101_clicked(widget):
        PerformanceMenusGUI.cpu_tab_popover_set_gui()                                         # Apply settings on the CPU tab popover GUI before showing it
        PerformanceMenusGUI.popover1101p.popup()                                              # Show CPU tab popover GUI

    # RAM tab GUI functions
    def on_button1201_clicked(widget):
        PerformanceMenusGUI.ram_tab_popover_set_gui()                                         # Apply settings on the RAM tab popover GUI before showing it
        PerformanceMenusGUI.popover1201p.popup()                                              # Show RAM tab popover GUI

    # Disk tab GUI functions
    def on_button1301_clicked(widget):
        PerformanceMenusGUI.disk_tab_popover_set_gui()                                        # Apply settings on the Disk tab popover GUI before showing it
        PerformanceMenusGUI.popover1301p.popup()                                              # Show Disk tab popover GUI

    # Network tab GUI functions
    def on_button1401_clicked(widget):
        PerformanceMenusGUI.network_tab_popover_set_gui()                                     # Apply settings on the Network tab popover GUI before showing it
        PerformanceMenusGUI.popover1401p.popup()                                              # Show Network tab popover GUI

    # GPU tab GUI functions
    def on_button1501_clicked(widget):
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                                  # Get gpu/graphics card list and set selected gpu
        PerformanceMenusGUI.gpu_tab_popover_set_gui()                                         # Apply settings on the GPU tab popover GUI before showing it
        PerformanceMenusGUI.popover1501p.popup()                                              # Show GPU tab popover GUI

    # Sensors tab GUI functions
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
        PerformanceMenusGUI.popover1601p2.popup()



    # Performance tab GUI functions - connect
    radiobutton1001.connect("toggled", on_radiobutton1001_toggled)
    radiobutton1002.connect("toggled", on_radiobutton1002_toggled)
    radiobutton1003.connect("toggled", on_radiobutton1003_toggled)
    radiobutton1004.connect("toggled", on_radiobutton1004_toggled)
    radiobutton1005.connect("toggled", on_radiobutton1005_toggled)
    radiobutton1006.connect("toggled", on_radiobutton1006_toggled)
    # CPU tab GUI functions - connect
    button1101.connect("clicked", on_button1101_clicked)
    # RAM tab GUI functions - connect
    button1201.connect("clicked", on_button1201_clicked)
    # Disk tab GUI functions - connect
    button1301.connect("clicked", on_button1301_clicked)
    # Network tab GUI functions - connect
    button1401.connect("clicked", on_button1401_clicked)
    # GPU tab GUI functions - connect
    button1501.connect("clicked", on_button1501_clicked)
    # Sensors tab GUI functions - connect
    global treeview1601_handler_id
    searchentry1601.connect("changed", on_searchentry1601_changed)
#     button1601.connect("clicked", on_button1601_clicked)
    button1603.connect("clicked", on_button1603_clicked)
    radiobutton1601.connect("toggled", on_radiobutton1601_toggled)
    radiobutton1602.connect("toggled", on_radiobutton1602_toggled)
    radiobutton1603.connect("toggled", on_radiobutton1603_toggled)


    # Sensors Tab on Performance Tab - Treeview Properties
    treeview1601.set_activate_on_single_click(True)
    treeview1601.set_show_expanders(False)            # This command is used for hiding expanders (arrows) at the beginning of the rows. For "Sensors" tab, "child rows" are not used and there is no need for these expanders (they are shown as empty spaces in this situation).
    treeview1601.set_fixed_height_mode(True)          # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview1601.set_headers_clickable(True)
    treeview1601.set_enable_search(True)              # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview1601.set_search_column(2)                 # This command used for searching by using entry.
    treeview1601.set_tooltip_column(2)


# ----------------------------------- Performance - Performance Functions Run Function (runs functions (CPU, RAM, Disk, Network, GPU, Sensors) when their stack page is selected) -----------------------------------
def performance_gui_function_run_func():
    MainGUI.main_gui_main_function_run_func()
    return

    if radiobutton1001.get_active() == True:
        stack1001.set_visible_child(grid1001)

    if radiobutton1002.get_active() == True:
        stack1001.set_visible_child(grid1002)

    if radiobutton1003.get_active() == True:
        stack1001.set_visible_child(grid1003)

    if radiobutton1004.get_active() == True:
        stack1001.set_visible_child(grid1004)

    if radiobutton1005.get_active() == True:
        stack1001.set_visible_child(grid1005)

    if radiobutton1006.get_active() == True:
        stack1001.set_visible_child(grid1006)
        import Sensors
        Sensors.sensors_import_func()
        Sensors.sensors_thread_run_func()

    Performance.performance_foreground_initial_func()
