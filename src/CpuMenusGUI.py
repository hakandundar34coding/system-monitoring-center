#!/usr/bin/env python3

# ----------------------------------- CPU - CPU Tab Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def cpu_menus_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global Config, CpuGUI, Cpu, Performance
    import Config, CpuGUI, Cpu, Performance


# ----------------------------------- CPU - CPU Tab Menus GUI Function (the code of this module in order to avoid running them during module import and defines "CPU" tab menu/popover GUI objects and functions/signals) -----------------------------------
def cpu_menus_gui_func():

    # Define builder and get all objects (Performance tab CPU sub-tab customizations popovers) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/CpuMenus.ui")


    # Define a colorchooserdialog in order to set chart colors
    global colorchooserdialog1001
    colorchooserdialog1001 = Gtk.ColorChooserDialog()

    # ********************** Define object names for CPU tab popover **********************
    global popover1101p
    global radiobutton1101p, radiobutton1102p
    global button1101p, button1102p, button1103p
    global combobox1101p, combobox1102p

    # ********************** Get objects for CPU tab popover **********************
    popover1101p = builder.get_object('popover1101p')
    radiobutton1101p = builder.get_object('radiobutton1101p')
    radiobutton1102p = builder.get_object('radiobutton1102p')
    button1101p = builder.get_object('button1101p')
    button1102p = builder.get_object('button1102p')
    button1103p = builder.get_object('button1103p')
    combobox1101p = builder.get_object('combobox1101p')
    combobox1102p = builder.get_object('combobox1102p')

    # ********************** Define object functions for CPU tab popover **********************
    def on_popover1101p_show(widget):                                                         # Perform following operations on popover menu show.
        try:
            cpu_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        cpu_tab_popover_set_gui()
        cpu_tab_customization_popover_connect_signals_func()

    def on_radiobutton1101p_toggled(widget):                                                  # Option for drawing "average CPU usage"
        if radiobutton1101p.get_active() == True:
            Config.show_cpu_usage_per_core = 0                                                # Make this definition before calling the following function in order to prevent problems because of the unchanged setting.
            CpuGUI.drawingarea1101.disconnect_by_func(CpuGUI.on_drawingarea1101_draw_per_core)    # Disconnect "on_drawingarea1101_draw_per_core" function in order to connect "on_drawingarea1101_draw" function which draws cpu usage percent average.
            CpuGUI.drawingarea1101.connect("draw", CpuGUI.on_drawingarea1101_draw)            # Connect "on_drawingarea1101_draw" function in order to draw cpu usage percent average.
            Cpu.cpu_initial_func()                                                            # Call this function in order to apply changes
            Cpu.cpu_loop_func()                                                               # Call this function in order to apply changes immediately (without waiting update interval).
            Config.config_save_func()

    def on_radiobutton1102p_toggled(widget):                                                  # Option for drawing "CPU usage per core"
        if radiobutton1102p.get_active() == True:
            Config.show_cpu_usage_per_core = 1                                                # Make this definition before calling the following function in order to prevent problems because of the unchanged setting.
            try:
                CpuGUI.drawingarea1101.disconnect_by_func(CpuGUI.on_drawingarea1101_draw)     # Disconnect "on_drawingarea1101_draw" function in order to connect "on_drawingarea1101_draw_per_core" function for drawing cpu usage percent per core.
            except TypeError:
                pass
            CpuGUI.drawingarea1101.connect("draw", CpuGUI.on_drawingarea1101_draw_per_core)    # Connect "on_drawingarea1101_draw_per_core" function in order to draw cpu usage percent per core.
            Cpu.cpu_initial_func()                                                            # Call this function in order to apply changes
            Cpu.cpu_loop_func()                                                               # Call this function in order to apply changes immediately (without waiting update interval).
            Config.config_save_func()

    def on_button1101p_clicked(widget):                                                       # For setting chart foreground color
        red, blue, green, alpha = Config.chart_line_color_cpu_percent                         # Get current foreground color of the chart
        colorchooserdialog1001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart foregorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog1001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog1001.get_rgba()
            Config.chart_line_color_cpu_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog1001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog1001.hide()
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1102p_clicked(widget):                                                       # For setting chart background color
        red, blue, green, alpha = Config.chart_background_color_all_charts                    # Get current background color of the chart
        colorchooserdialog1001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart backgorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog1001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog1001.get_rgba()
            Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog1001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog1001.hide()
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).

    def on_combobox1101p_changed(widget):                                                     # Option for defining "CPU usage number precision" shown by using a label
        Config.performance_cpu_usage_percent_precision = Config.number_precision_list[combobox1101p.get_active()][2]
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes immediately (without waiting update interval).
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1102p_changed(widget):                                                     # Option for defining "selected CPU core" which affects information shown on the GUI
        Config.selected_cpu_core = Performance.logical_core_list_system_ordered[combobox1102p.get_active()]
        Cpu.cpu_cpu_core_number = Config.selected_cpu_core
        Performance.performance_set_selected_cpu_core_func()                                  # Call this function in order to apply selected CPU core changes
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes immediately (without waiting update interval).
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1103p_clicked(widget):                                                       # For resetting all CPU tab settings
        Config.config_default_performance_cpu_func()                                          # Load default settings in Config module
        Config.config_save_func()
        cpu_set_default_cpu_usage_type_func()
        Performance.performance_set_selected_cpu_core_func()                                  # Call this function in order to apply selected CPU core changes
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes immediately (without waiting update interval).
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).
        try:
            cpu_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        cpu_tab_popover_set_gui()                                                             # Apply setting changes on the CPU tab popover GUI
        cpu_tab_customization_popover_connect_signals_func()



    # ********************** Connect signals to GUI objects for CPU tab **********************
    popover1101p.connect("show", on_popover1101p_show)
    button1101p.connect("clicked", on_button1101p_clicked)
    button1102p.connect("clicked", on_button1102p_clicked)
    button1103p.connect("clicked", on_button1103p_clicked)

    # ********************** Define function for connecting Performance tab CPU sub-tab customizations popover GUI signals **********************
    def cpu_tab_customization_popover_connect_signals_func():
        radiobutton1101p.connect("toggled", on_radiobutton1101p_toggled)
        radiobutton1102p.connect("toggled", on_radiobutton1102p_toggled)
        combobox1101p.connect("changed", on_combobox1101p_changed)
        combobox1102p.connect("changed", on_combobox1102p_changed)

    # ********************** Define function for disconnecting Performance tab CPU sub-tab customizations popover GUI signals **********************
    def cpu_tab_customization_popover_disconnect_signals_func():
        radiobutton1101p.disconnect_by_func(on_radiobutton1101p_toggled)
        radiobutton1102p.disconnect_by_func(on_radiobutton1102p_toggled)
        combobox1101p.disconnect_by_func(on_combobox1101p_changed)
        combobox1102p.disconnect_by_func(on_combobox1102p_changed)


# ********************** Set CPU tab popover menu GUI object data/selections appropriate for settings **********************
def cpu_tab_popover_set_gui():

    # Select radiobutton appropriate for CPU usage chart setting
    if Config.show_cpu_usage_per_core == 0:
        radiobutton1101p.set_active(True)
    if Config.show_cpu_usage_per_core == 1:
        radiobutton1102p.set_active(True)

    # Add CPU usage percent data into combobox on the CPU tab on the Performance tab
    if "liststore1101p" not in globals():         # Check if "liststore1101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
        global liststore1101p
        liststore1101p = Gtk.ListStore()
        liststore1101p.set_column_types([str, int])
        combobox1101p.set_model(liststore1101p)
        renderer_text = Gtk.CellRendererText()
        combobox1101p.pack_start(renderer_text, True)
        combobox1101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1101p.append([data[1], data[2]])
    combobox1101p.set_active(Config.performance_cpu_usage_percent_precision)

    # Add CPU core list into combobox on CPU tab
    if "liststore1102p" not in globals():         # Check if "liststore1101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
        global liststore1102p
        liststore1102p = Gtk.ListStore()
        liststore1102p.set_column_types([str])
        combobox1102p.set_model(liststore1102p)
        renderer_text = Gtk.CellRendererText()
        combobox1102p.pack_start(renderer_text, True)
        combobox1102p.add_attribute(renderer_text, "text", 0)
    liststore1102p.clear()
    for cpu_core in Performance.logical_core_list_system_ordered:
        liststore1102p.append([cpu_core])
    combobox1102p.set_active(Performance.selected_cpu_core_number)


# ----------------------------------- CPU - Set Default CPU Usage Type Function (sets default CPU usage type (average CPU usage or CPU usage per core) when user resets this settings) -----------------------------------
def cpu_set_default_cpu_usage_type_func():

    if Config.show_cpu_usage_per_core == 0:
        try:
            CpuGUI.drawingarea1101.disconnect_by_func(CpuGUI.on_drawingarea1101_draw_per_core)    # Disconnect "on_drawingarea1101_draw_per_core" function in order to connect "on_drawingarea1101_draw" function which draws cpu usage percent average.
        except TypeError:
            return                                                                            # Function run is stopped here if there is no "on_drawingarea1101_draw_per_core" signals connected to the widget which means "show_cpu_usage_per_core = 0".
        CpuGUI.drawingarea1101.connect("draw", CpuGUI.on_drawingarea1101_draw)                # Connect "on_drawingarea1101_draw" function in order to draw cpu usage percent average.
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).
    if Config.show_cpu_usage_per_core == 1:
        try:
            CpuGUI.drawingarea1101.disconnect_by_func(CpuGUI.on_drawingarea1101_draw)         # Disconnect "on_drawingarea1101_draw" function in order to connect "on_drawingarea1101_draw_per_core" function for drawing cpu usage percent per core.
        except TypeError:
            return                                                                            # Function run is stopped here if there is no "on_drawingarea1101_draw_per_core" signals connected to the widget which means "show_cpu_usage_per_core = 0".
        CpuGUI.drawingarea1101.connect("draw", CpuGUI.on_drawingarea1101_draw_per_core)       # Connect "on_drawingarea1101_draw_per_core" function in order to draw cpu usage percent per core.
        Cpu.cpu_initial_func()                                                                # Call this function in order to apply changes
        Cpu.cpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).
