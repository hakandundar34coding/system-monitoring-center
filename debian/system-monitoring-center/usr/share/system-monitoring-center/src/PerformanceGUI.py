#! /usr/bin/python3

# ----------------------------------- Performance - Performance GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_gui_import_func():

    global Gtk

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk


    global Config, MainGUI, Performance, PerformanceMenusGUI
    import Config, MainGUI, Performance, PerformanceMenusGUI


# ----------------------------------- Performance - Performance GUI Function (the code of this module in order to avoid running them during module import and defines "Performance" tab GUI objects and functions/signals) -----------------------------------
def performance_gui_func():

    # Performance tab GUI objects
    global stack1001
    global radiobutton1001, radiobutton1002, radiobutton1003, radiobutton1004, radiobutton1005, radiobutton1006
    global grid1001, grid1002, grid1003, grid1004, grid1005, grid1006, grid1007, grid1008


    # Performance tab GUI objects - get
    stack1001 = MainGUI.builder.get_object('stack1001')
    radiobutton1001 = MainGUI.builder.get_object('radiobutton1001')
    radiobutton1002 = MainGUI.builder.get_object('radiobutton1002')
    radiobutton1003 = MainGUI.builder.get_object('radiobutton1003')
    radiobutton1004 = MainGUI.builder.get_object('radiobutton1004')
    radiobutton1005 = MainGUI.builder.get_object('radiobutton1005')
    radiobutton1006 = MainGUI.builder.get_object('radiobutton1006')
    grid1001 = MainGUI.builder.get_object('grid1001')
    grid1002 = MainGUI.builder.get_object('grid1002')
    grid1003 = MainGUI.builder.get_object('grid1003')
    grid1004 = MainGUI.builder.get_object('grid1004')
    grid1005 = MainGUI.builder.get_object('grid1005')
    grid1006 = MainGUI.builder.get_object('grid1006')
    grid1007 = MainGUI.builder.get_object('grid1007')
    grid1008 = MainGUI.builder.get_object('grid1008')


    # Performance tab GUI functions
    def on_radiobutton1001_toggled(widget):
        if radiobutton1001.get_active() == True:
            MainGUI.main_gui_main_function_run_func()

    def on_radiobutton1002_toggled(widget):
        if radiobutton1002.get_active() == True:
            MainGUI.main_gui_main_function_run_func()

    def on_radiobutton1003_toggled(widget):
        if radiobutton1003.get_active() == True:
            MainGUI.main_gui_main_function_run_func()

    def on_radiobutton1004_toggled(widget):
        if radiobutton1004.get_active() == True:
            MainGUI.main_gui_main_function_run_func()

    def on_radiobutton1005_toggled(widget):
        if radiobutton1005.get_active() == True:
            MainGUI.main_gui_main_function_run_func()

    def on_radiobutton1006_toggled(widget):
        if radiobutton1006.get_active() == True:
            MainGUI.main_gui_main_function_run_func()



    # Performance tab GUI functions - connect
    radiobutton1001.connect("toggled", on_radiobutton1001_toggled)
    radiobutton1002.connect("toggled", on_radiobutton1002_toggled)
    radiobutton1003.connect("toggled", on_radiobutton1003_toggled)
    radiobutton1004.connect("toggled", on_radiobutton1004_toggled)
    radiobutton1005.connect("toggled", on_radiobutton1005_toggled)
    radiobutton1006.connect("toggled", on_radiobutton1006_toggled)
