#!/usr/bin/env python3

# ----------------------------------- Performance - Performance Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_menus_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global Config, PerformanceGUI, ChartPlots, Performance, Sensors
    import Config, PerformanceGUI, ChartPlots, Performance, Sensors


# ----------------------------------- Performance - Performance Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def performance_menus_gui_func():

    # ********************** Define object names for CPU tab popover **********************
    global popover1101p
    global radiobutton1101p, radiobutton1102p
    global button1101p, button1102p, button1103p, button1104p
    global combobox1101p, combobox1102p

    # ********************** Define object names for RAM tab popover **********************
    global popover1201p
    global button1201p, button1202p, button1203p, button1204p
    global combobox1201p, combobox1202p

    # ********************** Define object names for Disk tab popover **********************
    global popover1301p
    global button1301p, button1302p, button1303p, button1304p
    global combobox1301p, combobox1302p, combobox1303p, combobox1304p, combobox1305p
    global checkbutton1301p, checkbutton1302p

    # ********************** Define object names for Network tab popover **********************
    global popover1401p
    global button1401p, button1402p, button1403p
    global combobox1401p, combobox1402p, combobox1403p, combobox1404p, combobox1405p
    global checkbutton1401p, checkbutton1402p

    # ********************** Define object names for GPU tab popover **********************
    global popover1501p
    global button1501p, button1502p, button1503p, button1504p, button1505p
    global combobox1501p

    # ********************** Define object names for Sensors tab popover **********************
    global popover1601p
    global button1602p#, button1601p

    # ********************** Define object names for Sensors tab search customizations popover **********************
    global popover1601p2
    global radiobutton1601p2, radiobutton1602p2
    global checkbutton1601p2, checkbutton1602p2, checkbutton1603p2

    builder1101m = Gtk.Builder()
    builder1101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/PerformanceMenus.glade")


    # ********************** Get objects for CPU tab popover **********************
    popover1101p = builder1101m.get_object('popover1101p')
    radiobutton1101p = builder1101m.get_object('radiobutton1101p')
    radiobutton1102p = builder1101m.get_object('radiobutton1102p')
    button1101p = builder1101m.get_object('button1101p')
    button1102p = builder1101m.get_object('button1102p')
    button1103p = builder1101m.get_object('button1103p')
    button1104p = builder1101m.get_object('button1104p')
    combobox1101p = builder1101m.get_object('combobox1101p')
    combobox1102p = builder1101m.get_object('combobox1102p')

    # ********************** Get objects for RAM tab popover **********************
    popover1201p = builder1101m.get_object('popover1201p')
    button1201p = builder1101m.get_object('button1201p')
    button1202p = builder1101m.get_object('button1202p')
    button1203p = builder1101m.get_object('button1203p')
    button1204p = builder1101m.get_object('button1204p')
    combobox1201p = builder1101m.get_object('combobox1201p')
    combobox1202p = builder1101m.get_object('combobox1202p')

    # ********************** Get objects for Disk tab popover **********************
    popover1301p = builder1101m.get_object('popover1301p')
    button1301p = builder1101m.get_object('button1301p')
    button1302p = builder1101m.get_object('button1302p')
    button1303p = builder1101m.get_object('button1303p')
    button1304p = builder1101m.get_object('button1304p')
    combobox1301p = builder1101m.get_object('combobox1301p')
    combobox1302p = builder1101m.get_object('combobox1302p')
    combobox1303p = builder1101m.get_object('combobox1303p')
    combobox1304p = builder1101m.get_object('combobox1304p')
    combobox1305p = builder1101m.get_object('combobox1305p')
    checkbutton1301p = builder1101m.get_object('checkbutton1301p')
    checkbutton1302p = builder1101m.get_object('checkbutton1302p')

    # ********************** Get objects for Network tab popover **********************
    popover1401p = builder1101m.get_object('popover1401p')
    button1401p = builder1101m.get_object('button1401p')
    button1402p = builder1101m.get_object('button1402p')
    button1403p = builder1101m.get_object('button1403p')
    button1404p = builder1101m.get_object('button1404p')
    combobox1401p = builder1101m.get_object('combobox1401p')
    combobox1402p = builder1101m.get_object('combobox1402p')
    combobox1403p = builder1101m.get_object('combobox1403p')
    combobox1404p = builder1101m.get_object('combobox1404p')
    combobox1405p = builder1101m.get_object('combobox1405p')
    checkbutton1401p = builder1101m.get_object('checkbutton1401p')
    checkbutton1402p = builder1101m.get_object('checkbutton1402p')

    # ********************** Get objects for GPU tab popover **********************
    popover1501p = builder1101m.get_object('popover1501p')
    button1501p = builder1101m.get_object('button1501p')
    button1502p = builder1101m.get_object('button1502p')
    button1503p = builder1101m.get_object('button1503p')
    button1504p = builder1101m.get_object('button1504p')
    button1505p = builder1101m.get_object('button1505p')
    combobox1501p = builder1101m.get_object('combobox1501p')

    # ********************** Get objects for Sensors tab popover **********************
    popover1601p = builder1101m.get_object('popover1601p')
#     button1601p = builder1101m.get_object('button1601p')
    button1602p = builder1101m.get_object('button1602p')

    # ********************** Get objects for Sensors tab search popover **********************
    popover1601p2 = builder1101m.get_object('popover1601p2')
    radiobutton1601p2 = builder1101m.get_object('radiobutton1601p2')
    radiobutton1602p2 = builder1101m.get_object('radiobutton1602p2')
    checkbutton1601p2 = builder1101m.get_object('checkbutton1601p2')
    checkbutton1602p2 = builder1101m.get_object('checkbutton1602p2')
    checkbutton1603p2 = builder1101m.get_object('checkbutton1603p2')

    # Define a colorchooserdialog in order to set chart colors (same colorchooserdialog is used for all Performance tab popovers)
    global colorchooserdialog1001
    colorchooserdialog1001 = Gtk.ColorChooserDialog()


    # ********************** Define object functions for CPU tab popover **********************
    def on_radiobutton1101p_toggled(widget):                                                  # Option for drawing a"verage CPU usage"
        if radiobutton1101p.get_active() == True:
            Config.show_cpu_usage_per_core = 0                                                # Make this definition before calling the following function in order to prevent problems because of the uncganged setting.
            ChartPlots.drawingarea1101.disconnect_by_func(ChartPlots.on_drawingarea1101_draw_per_core)    # Disconnect "on_drawingarea1101_draw_per_core" function in order to connect "on_drawingarea1101_draw" function which draws cpu usage percent average.
            ChartPlots.drawingarea1101.connect("draw", ChartPlots.on_drawingarea1101_draw)    # Connect "on_drawingarea1101_draw" function in order to draw cpu usage percent average.
            Performance.performance_foreground_func()                                         # Call this function in order to apply changes immediately (without waiting update interval).
            Config.config_save_func()

    def on_radiobutton1102p_toggled(widget):                                                  # Option for drawing "CPU usage per core"
        if radiobutton1102p.get_active() == True:
            Config.show_cpu_usage_per_core = 1                                                # Make this definition before calling the following function in order to prevent problems because of the uncganged setting.
            ChartPlots.drawingarea1101.disconnect_by_func(ChartPlots.on_drawingarea1101_draw) # Disconnect "on_drawingarea1101_draw" function in order to connect "on_drawingarea1101_draw_per_core" function for drawing cpu usage percent per core.
            ChartPlots.drawingarea1101.connect("draw", ChartPlots.on_drawingarea1101_draw_per_core)       # Connect "on_drawingarea1101_draw_per_core" function in order to draw cpu usage percent per core.
            Performance.performance_foreground_func()                                         # Call this function in order to apply changes immediately (without waiting update interval).
            Config.config_save_func()

    def on_button1101p_clicked(widget):                                                       # For setting chart foreground color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("cpu_percent")                          # "cpu_percent" variable passed to the function in order to use settings for CPU chart
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_button1102p_clicked(widget):                                                       # For setting chart background color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("all_charts_background")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_combobox1101p_changed(widget):                                                     # Option for defining "CPU usage number precision" shown by using a label
        Config.performance_cpu_usage_percent_precision = Config.number_precision_list[combobox1101p.get_active()][2]
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1102p_changed(widget):                                                     # Option for defining "selected CPU core" which affects information shown on the GUI
        Config.selected_cpu_core = Performance.logical_core_list_system_ordered[combobox1102p.get_active()]
        Performance.selected_cpu_core_number = Config.selected_cpu_core
        Performance.performance_set_selected_cpu_core_func()                                  # Call this function in order to apply selected CPU core changes
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1103p_clicked(widget):                                                       # For resetting all CPU tab settings
        Config.config_default_performance_cpu_func()                                          # Load default settings in Config module
        Performance.performance_set_selected_cpu_core_func()                                  # Call this function in order to apply selected CPU core changes
        cpu_tab_popover_set_gui()                                                             # Apply setting changes on the CPU tab popover GUI
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1104p_clicked(widget):                                                       # For listing CPU information by using "lscpu" command on the system default terminal
        process = subprocess.Popen("x-terminal-emulator -e /bin/bash -c \'lscpu; exec bash\'", stdout=subprocess.PIPE, stderr=None, shell=True)


    # ********************** Define object functions for RAM tab popover **********************
    def on_button1201p_clicked(widget):                                                       # For setting chart foreground color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("ram_swap_percent")                     # "ram_swap_percent" variable passed to the function in order to use settings for RAM chart
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_button1202p_clicked(widget):                                                       # For setting chart background color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("all_charts_background")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_combobox1201p_changed(widget):                                                     # Option for defining "RAM/Swap data number precision" shown by using labels
        Config.performance_ram_swap_data_precision = Config.number_precision_list[combobox1201p.get_active()][2]
        Performance.performance_foreground_initial_func()
        Performance.performance_foreground_func()
        Config.config_save_func()

    def on_combobox1202p_changed(widget):                                                     # Option for defining "RAM/Swap data units" shown by using labels
        Config.performance_ram_swap_data_unit = Config.data_unit_list[combobox1202p.get_active()][2]
        Performance.performance_foreground_initial_func()
        Performance.performance_foreground_func()
        Config.config_save_func()

    def on_button1203p_clicked(widget):                                                       # For resetting all RAM tab settings
        Config.config_default_performance_ram_func()
        ram_tab_popover_set_gui()                                                             # Apply setting changes on the RAM tab popover GUI
        Performance.performance_foreground_initial_func()
        Performance.performance_foreground_func()

    def on_button1204p_clicked(widget):                                                       # For listing RAM information by using "dmidecode" command on the system default terminal
        process = subprocess.Popen("x-terminal-emulator -e pkexec /bin/bash -c \'sudo dmidecode --type memory; exec bash\'", stdout=subprocess.PIPE, stderr=None, shell=True)


    # ********************** Define object functions for Disk tab popover **********************
    def on_checkbutton1301p_toggled(widget):                                                  # Option for showing "disk read speed" on the chart
        if checkbutton1301p.get_active() == True:
            Config.plot_disk_read_speed = 1
        if checkbutton1301p.get_active() == False:
            if checkbutton1302p.get_active() == False:
                checkbutton1301p.set_active(True)
                return
            Config.plot_disk_read_speed = 0
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_checkbutton1302p_toggled(widget):                                                  # Option for showing "disk write speed" on the chart
        if checkbutton1302p.get_active() == True:
            Config.plot_disk_write_speed = 1
        if checkbutton1302p.get_active() == False:
            if checkbutton1301p.get_active() == False:
                checkbutton1302p.set_active(True)
                return
            Config.plot_disk_write_speed = 0
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1301p_clicked(widget):                                                       # For setting chart foreground color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("disk_speed_usage")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_button1302p_clicked(widget):                                                       # For setting chart background color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("all_charts_background")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_combobox1301p_changed(widget):                                                     # Option for defining "disk read/write speed number precision" shown by using label
        Config.performance_disk_speed_data_precision = Config.number_precision_list[combobox1301p.get_active()][2]
        Performance.performance_foreground_initial_func()
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1302p_changed(widget):                                                     # Option for defining "disk read/write data number precision" shown by using label
        Config.performance_disk_usage_data_precision = Config.data_unit_list[combobox1302p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1303p_changed(widget):                                                     # Option for defining "disk read/write speed data units" shown by using label
        Config.performance_disk_speed_data_unit = Config.data_speed_unit_list[combobox1303p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1304p_changed(widget):                                                     # Option for defining "disk read/write data units" shown by using label
        Config.performance_disk_usage_data_unit = Config.data_unit_list[combobox1304p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1305p_changed(widget):                                                     # Option for defining "selected disk" which affects information shown on the GUI
        Config.selected_disk = Performance.disk_list_system_ordered[combobox1305p.get_active()]
        Performance.selected_disk_number = Config.selected_disk
        Performance.performance_set_selected_disk_func()
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1303p_clicked(widget):                                                       # For resetting all Disk tab settings
        Config.config_default_performance_disk_func()
        Performance.performance_set_selected_disk_func()
        disk_tab_popover_set_gui()
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1304p_clicked(widget):                                                       # For listing disk information by using "lsblk" command on the system default terminal
        process = subprocess.Popen("x-terminal-emulator -e /bin/bash -c \'lsblk -o NAME,PATH,MOUNTPOINT,TYPE,FSTYPE,SIZE,FSUSE%,MODEL,LABEL,PARTLABEL; exec bash\'", stdout=subprocess.PIPE, stderr=None, shell=True)


    # ********************** Define object functions for Network tab popover **********************
    def on_checkbutton1401p_toggled(widget):                                                  # Option for showing "network download speed" on the chart
        if checkbutton1401p.get_active() == True:
            Config.plot_network_download_speed = 1
        if checkbutton1401p.get_active() == False:
            if checkbutton1402p.get_active() == False:
                checkbutton1401p.set_active(True)
                return
            Config.plot_network_download_speed = 0
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_checkbutton1402p_toggled(widget):                                                  # Option for showing "network upload speed" on the chart
        if checkbutton1402p.get_active() == True:
            Config.plot_network_upload_speed = 1
        if checkbutton1402p.get_active() == False:
            if checkbutton1401p.get_active() == False:
                checkbutton1402p.set_active(True)
                return
            Config.plot_network_upload_speed = 0
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1401p_clicked(widget):                                                       # For setting chart foreground color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("network_speed")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_button1402p_clicked(widget):                                                       # For setting chart background color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("all_charts_background")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_combobox1401p_changed(widget):                                                     # Option for defining "network download/upload speed number precision" shown by using label
        Config.performance_network_speed_data_precision = Config.number_precision_list[combobox1401p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1402p_changed(widget):                                                     # Option for defining "network download/upload data number precision" shown by using label
        Config.performance_network_data_data_precision = Config.number_precision_list[combobox1402p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1403p_changed(widget):                                                     # Option for defining "network download/upload speed data units" shown by using label
        Config.performance_network_speed_data_unit = Config.data_speed_unit_list[combobox1403p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1404p_changed(widget):                                                     # Option for defining "network download/upload data units" shown by using label
        Config.performance_network_data_data_unit = Config.data_unit_list[combobox1404p.get_active()][2]
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1405p_changed(widget):                                                     # Option for defining "selected network card" which affects information shown on the GUI
        Config.selected_network_card = Performance.network_card_list[combobox1405p.get_active()]
        Performance.set_selected_network_card = Config.selected_network_card
        Performance.performance_set_selected_network_card_func()                              # Call this function in order to apply changes
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1403p_clicked(widget):                                                       # For resetting all Network tab settings
        Config.config_default_performance_network_func()
        Performance.performance_set_selected_network_card_func()                              # Call this function in order to apply changes
        network_tab_popover_set_gui()
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1404p_clicked(widget):                                                       # For listing network information by using "lspci" command on the system default terminal
        process = subprocess.Popen("x-terminal-emulator -e /bin/bash -c \'lspci | grep -i net \n ip a; exec bash\'", stdout=subprocess.PIPE, stderr=None, shell=True)


    # ********************** Define object functions for GPU tab popover **********************
    def on_button1502p_clicked(widget):                                                       # For setting chart foreground color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("fps")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_button1503p_clicked(widget):                                                       # For setting chart background color
        if colorchooserdialog1001.run() == Gtk.ResponseType.OK:
            on_colorchooserdialog1001_color_activated("all_charts_background")
            colorchooserdialog1001.hide()
            Config.config_save_func()

    def on_combobox1501p_changed(widget):                                                     # For resetting all GPU tab settings                                             # Option for defining "selected gpu/graphics card" which affects information shown on the GUI
        Config.selected_gpu = Performance.gpu_list[combobox1501p.get_active()]
        Performance.set_selected_gpu = Config.selected_gpu
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                      # Call this function in order to apply changes
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1504p_clicked(widget):
        Config.config_default_performance_gpu_func()
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                      # Call this function in order to apply changes
        gpu_tab_popover_set_gui()
        Performance.performance_foreground_initial_func()                                     # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                             # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1505p_clicked(widget):                                                       # For listing gpu/graphics card information by using "glxinfo" command on the system default terminal
        process = subprocess.Popen("x-terminal-emulator -e /bin/bash -c \'DRI_PRIME=0 glxinfo -B; DRI_PRIME=1 glxinfo -B; exec bash\'", stdout=subprocess.PIPE, stderr=None, shell=True)


    # ********************** Define object functions for Sensors tab customizations popover **********************
#     def on_button1601p_clicked(widget):                                                       # "Reset" button
#         Config.config_default_performance_sensors_row_column_func()
#         Config.config_save_func()

    def on_button1602p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_performance_sensors_row_column_func()
        Config.config_save_func()


    # ********************** Define object functions for Sensors tab search customizations popover **********************
    def on_radiobutton1601p2_toggled(widget):
        if radiobutton1601p2.get_active() == True:
            Sensors.sensors_treeview_filter_search_func()

    def on_radiobutton1602p2_toggled(widget):
        if radiobutton1602p2.get_active() == True:
            Sensors.sensors_treeview_filter_search_func()

    def on_checkbutton1601p2_toggled(widget):
        performance_popovers_checkbutton_behavior_func("sensors", checkbutton1601p2)

    def on_checkbutton1602p2_toggled(widget):
        performance_popovers_checkbutton_behavior_func("sensors", checkbutton1602p2)

    def on_checkbutton1603p2_toggled(widget):
        performance_popovers_checkbutton_behavior_func("sensors", checkbutton1603p2)



    # ********************** Connect signals to GUI objects for CPU tab **********************
    radiobutton1101p.connect("toggled", on_radiobutton1101p_toggled)
    radiobutton1102p.connect("toggled", on_radiobutton1102p_toggled)
    button1101p.connect("clicked", on_button1101p_clicked)
    button1102p.connect("clicked", on_button1102p_clicked)
    button1103p.connect("clicked", on_button1103p_clicked)
    button1104p.connect("clicked", on_button1104p_clicked)
    global combobox1101p_handler_id, combobox1102p_handler_id
    combobox1101p_handler_id = combobox1101p.connect("changed", on_combobox1101p_changed)
    combobox1102p_handler_id = combobox1102p.connect("changed", on_combobox1102p_changed)

    # ********************** Connect signals to GUI objects for RAM tab **********************
    button1201p.connect("clicked", on_button1201p_clicked)
    button1202p.connect("clicked", on_button1202p_clicked)
    button1203p.connect("clicked", on_button1203p_clicked)
    button1204p.connect("clicked", on_button1204p_clicked)
    global combobox1201p_handler_id, combobox1202p_handler_id
    combobox1201p_handler_id = combobox1201p.connect("changed", on_combobox1201p_changed)
    combobox1202p_handler_id = combobox1202p.connect("changed", on_combobox1202p_changed)

    # ********************** Connect signals to GUI objects for Disk tab **********************
    checkbutton1301p.connect("toggled", on_checkbutton1301p_toggled)
    checkbutton1302p.connect("toggled", on_checkbutton1302p_toggled)
    button1301p.connect("clicked", on_button1301p_clicked)
    button1302p.connect("clicked", on_button1302p_clicked)
    button1303p.connect("clicked", on_button1303p_clicked)
    button1304p.connect("clicked", on_button1304p_clicked)
    global combobox1301p_handler_id, combobox1302p_handler_id, combobox1303p_handler_id, combobox1304p_handler_id, combobox1305p_handler_id
    combobox1301p_handler_id = combobox1301p.connect("changed", on_combobox1301p_changed)
    combobox1302p_handler_id = combobox1302p.connect("changed", on_combobox1302p_changed)
    combobox1303p_handler_id = combobox1303p.connect("changed", on_combobox1303p_changed)
    combobox1304p_handler_id = combobox1304p.connect("changed", on_combobox1304p_changed)
    combobox1305p_handler_id = combobox1305p.connect("changed", on_combobox1305p_changed)

    # ********************** Connect signals to GUI objects for Network tab **********************
    checkbutton1401p.connect("toggled", on_checkbutton1401p_toggled)
    checkbutton1402p.connect("toggled", on_checkbutton1402p_toggled)
    button1401p.connect("clicked", on_button1401p_clicked)
    button1402p.connect("clicked", on_button1402p_clicked)
    button1403p.connect("clicked", on_button1403p_clicked)
    button1404p.connect("clicked", on_button1404p_clicked)
    global combobox1401p_handler_id, combobox1402p_handler_id, combobox1403p_handler_id, combobox1404p_handler_id, combobox1405p_handler_id
    combobox1401p_handler_id = combobox1401p.connect("changed", on_combobox1401p_changed)
    combobox1402p_handler_id = combobox1402p.connect("changed", on_combobox1402p_changed)
    combobox1403p_handler_id = combobox1403p.connect("changed", on_combobox1403p_changed)
    combobox1404p_handler_id = combobox1404p.connect("changed", on_combobox1404p_changed)
    combobox1405p_handler_id = combobox1405p.connect("changed", on_combobox1405p_changed)

    # ********************** Connect signals to GUI objects for GPU tab **********************
    button1502p.connect("clicked", on_button1502p_clicked)
    button1503p.connect("clicked", on_button1503p_clicked)
    button1504p.connect("clicked", on_button1504p_clicked)
    button1505p.connect("clicked", on_button1505p_clicked)
    global combobox1501p_handler_id
    combobox1501p_handler_id = combobox1501p.connect("changed", on_combobox1501p_changed)

    # ********************** Connect signals to GUI objects for Sensors tab customizations popover **********************
#     button1601p.connect("clicked", on_button1601p_clicked)
    button1602p.connect("clicked", on_button1602p_clicked)

    # ********************** Connect signals to GUI objects for Sensors tab search customizations popover **********************
    radiobutton1601p2.connect("toggled", on_radiobutton1601p2_toggled)
    radiobutton1602p2.connect("toggled", on_radiobutton1602p2_toggled)
    global checkbutton1601p2_handler_id, checkbutton1602p2_handler_id, checkbutton1603p2_handler_id
    checkbutton1601p2_handler_id = checkbutton1601p2.connect("toggled", on_checkbutton1601p2_toggled)   # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton1602p2_handler_id = checkbutton1602p2.connect("toggled", on_checkbutton1602p2_toggled)
    checkbutton1603p2_handler_id = checkbutton1603p2.connect("toggled", on_checkbutton1603p2_toggled)



    # ********************** Popover settings for CPU tab **********************
    popover1101p.set_relative_to(PerformanceGUI.button1101)       # Set widget that popover menu will display at the edge of.
    popover1101p.set_position(1)                                  # Show popover menu at the right edge of the caller button in order not to hide CPU usage percentage when menu is shown. Becuse there is CPU usage percentage precision setting and user may want to see visual changes just in time.
    # ********************** Popover settings for RAM tab **********************
    popover1201p.set_relative_to(PerformanceGUI.button1201)
    popover1201p.set_position(1)
    # ********************** Popover settings for Disk tab **********************
    popover1301p.set_relative_to(PerformanceGUI.button1301)
    popover1301p.set_position(1)
    # ********************** Popover settings for Network tab **********************
    popover1401p.set_relative_to(PerformanceGUI.button1401)
    popover1401p.set_position(1)
    # ********************** Popover settings for GPU tab **********************
    popover1501p.set_relative_to(PerformanceGUI.button1501)
    popover1501p.set_position(1)
    # ********************** Popover settings for Sensors tab **********************
#     popover1601p.set_relative_to(PerformanceGUI.button1601)
#     popover1601p.set_position(1)
    # ********************** Popover settings for Sensors tab search customizations **********************
    popover1601p2.set_relative_to(PerformanceGUI.button1603)
    popover1601p2.set_position(3)        # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).

# ----------------------------------- Performance - Color Chooser Dialog Function (gets color from color chooser dialog and sets chart colors) -----------------------------------
def on_colorchooserdialog1001_color_activated(set_color):

    selected_color = colorchooserdialog1001.get_rgba()
    if set_color == "cpu_percent":
        Config.chart_line_color_cpu_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
    if set_color == "ram_swap_percent":
        Config.chart_line_color_ram_swap_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
    if set_color == "disk_speed_usage":
        Config.chart_line_color_disk_speed_usage = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
    if set_color == "network_speed":
        Config.chart_line_color_network_speed_data = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
    if set_color == "fps":
        Config.chart_line_color_fps = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
    if set_color == "all_charts_background":
        Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]


# ----------------------------------- Performance -Performance Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def performance_popovers_checkbutton_behavior_func(caller_tab, caller_checkbutton):

    if caller_tab == "sensors":
        checkbutton_list = [checkbutton1601p2, checkbutton1602p2, checkbutton1603p2]
        select_all_checkbutton = checkbutton_list[0]
        sub_checkbutton_list = checkbutton_list
        sub_checkbutton_list.remove(select_all_checkbutton)
        checkbutton_active_state_list = []
        for checkbutton in sub_checkbutton_list:
            if checkbutton != select_all_checkbutton:
                checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton1601p2.handler_block(checkbutton1601p2_handler_id) as p1, checkbutton1602p2.handler_block(checkbutton1602p2_handler_id) as p2, checkbutton1603p2.handler_block(checkbutton1603p2_handler_id) as p3:
        if caller_checkbutton != select_all_checkbutton and caller_checkbutton.get_active() == False:
            if True not in checkbutton_active_state_list:
                caller_checkbutton.set_active(True)
                checkbutton_active_state_list[sub_checkbutton_list.index(caller_checkbutton)] = True

        if caller_checkbutton != select_all_checkbutton and False not in checkbutton_active_state_list:
            select_all_checkbutton.set_active(True)
            select_all_checkbutton.set_inconsistent(False)

        if caller_checkbutton != select_all_checkbutton and False in checkbutton_active_state_list:
            select_all_checkbutton.set_active(False)
            select_all_checkbutton.set_inconsistent(True)

        if select_all_checkbutton.get_active() == True:
            select_all_checkbutton.set_inconsistent(False)
            for i, checkbutton in enumerate(sub_checkbutton_list):
                checkbutton.set_active(True)
                checkbutton_active_state_list[i] = True

        if select_all_checkbutton.get_active() == False:
            if False not in checkbutton_active_state_list:
                select_all_checkbutton.set_active(True)

    if PerformanceGUI.searchentry1601.get_text() != "":            # Search filter updating is prevented, if any text is not inserted into searchentry.
                                                                   # This is due to prevent user frustration because of the temperature/fan only buttons above the treeview.
        Sensors.sensors_treeview_filter_search_func()


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
    with combobox1101p.handler_block(combobox1101p_handler_id):                               # Prevent widget signal when setting active an item
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
    with combobox1102p.handler_block(combobox1102p_handler_id):                               # Prevent widget signal when setting active an item
        liststore1102p.clear()
        for cpu_core in Performance.logical_core_list_system_ordered:
            liststore1102p.append([cpu_core])
        combobox1102p.set_active(Performance.selected_cpu_core_number)


# ********************** Set RAM tab popover menu GUI object data/selections appropriate for settings **********************
def ram_tab_popover_set_gui():

    # Add RAM usage data precision data into combobox on the RAM tab on the Performance tab
    if "liststore1201p" not in globals():
        global liststore1201p
        liststore1201p = Gtk.ListStore()
        liststore1201p.set_column_types([str, int])
        combobox1201p.set_model(liststore1201p)
        renderer_text = Gtk.CellRendererText()
        combobox1201p.pack_start(renderer_text, True)
        combobox1201p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1201p.append([data[1], data[2]])
    with combobox1201p.handler_block(combobox1201p_handler_id):                               # Prevent widget signal when setting active an item
        combobox1201p.set_active(Config.performance_ram_swap_data_precision)

    # Add RAM usage data unit data into combobox on the RAM tab on the Performance tab
    if "liststore1202p" not in globals():
        global liststore1202p
        liststore1202p = Gtk.ListStore()
        liststore1202p.set_column_types([str, int])
        combobox1202p.set_model(liststore1202p)
        renderer_text = Gtk.CellRendererText()
        combobox1202p.pack_start(renderer_text, True)
        combobox1202p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore1202p.append([data[1], data[2]])
    with combobox1202p.handler_block(combobox1202p_handler_id):                               # Prevent widget signal when setting active an item
        for data_list in Config.data_unit_list:
            if data_list[2] == Config.performance_ram_swap_data_unit:      
                combobox1202p.set_active(data_list[0])


# ********************** Set Disk tab popover menu GUI object data/selections appropriate for settings **********************
def disk_tab_popover_set_gui():

    # Set active comboboxes if disk read speed/disk write speed values are "1"
    if Config.plot_disk_read_speed == 1:
        checkbutton1301p.set_active(True)
    if Config.plot_disk_read_speed == 0:
        checkbutton1301p.set_active(False)
    if Config.plot_disk_write_speed == 1:
        checkbutton1302p.set_active(True)
    if Config.plot_disk_write_speed == 0:
        checkbutton1302p.set_active(False)

    # Add Disk speed data precision data into combobox on the Disk tab on the Performance tab
    if "liststore1301p" not in globals():
        global liststore1301p
        liststore1301p = Gtk.ListStore()
        liststore1301p.set_column_types([str, int])
        combobox1301p.set_model(liststore1301p)
        renderer_text = Gtk.CellRendererText()
        combobox1301p.pack_start(renderer_text, True)
        combobox1301p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1301p.append([data[1], data[2]])
    with combobox1301p.handler_block(combobox1301p_handler_id):                               # Prevent widget signal when setting active an item
        combobox1301p.set_active(Config.performance_disk_speed_data_precision)

    # Add Disk usage data precision data into combobox on the Disk tab on the Performance tab
    if "liststore1302p" not in globals():
        global liststore1302p
        liststore1302p = Gtk.ListStore()
        liststore1302p.set_column_types([str, int])
        combobox1302p.set_model(liststore1302p)
        renderer_text = Gtk.CellRendererText()
        combobox1302p.pack_start(renderer_text, True)
        combobox1302p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1302p.append([data[1], data[2]])
    with combobox1302p.handler_block(combobox1302p_handler_id):                               # Prevent widget signal when setting active an item
        combobox1302p.set_active(Config.performance_disk_usage_data_precision)

    # Add Disk speed data unit data into combobox on the Disk tab on the Performance tab
    if "liststore1303p" not in globals():
        global liststore1303p
        liststore1303p = Gtk.ListStore()
        liststore1303p.set_column_types([str, int])
        combobox1303p.set_model(liststore1303p)
        renderer_text = Gtk.CellRendererText()
        combobox1303p.pack_start(renderer_text, True)
        combobox1303p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_speed_unit_list:
            liststore1303p.append([data[1], data[2]])
    with combobox1303p.handler_block(combobox1303p_handler_id):                               # Prevent widget signal when setting active an item
        for data_list in Config.data_speed_unit_list:
            if data_list[2] == Config.performance_disk_speed_data_unit:      
                combobox1303p.set_active(data_list[0])

    # Add Disk usage data unit data into combobox on the Disk tab on the Performance tab
    if "liststore1304p" not in globals():
        global liststore1304p
        liststore1304p = Gtk.ListStore()
        liststore1304p.set_column_types([str, int])
        combobox1304p.set_model(liststore1304p)
        renderer_text = Gtk.CellRendererText()
        combobox1304p.pack_start(renderer_text, True)
        combobox1304p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore1304p.append([data[1], data[2]])
    with combobox1304p.handler_block(combobox1304p_handler_id):                               # Prevent widget signal when setting active an item 
        for data_list in Config.data_unit_list:
            if data_list[2] == Config.performance_disk_usage_data_unit:      
                combobox1304p.set_active(data_list[0])

    # Add Disk list into combobox on the Disk tab on the Performance tab
    if "liststore1305p" not in globals():
        global liststore1305p
        liststore1305p = Gtk.ListStore()
        liststore1305p.set_column_types([str])
        combobox1305p.set_model(liststore1305p)
        renderer_text = Gtk.CellRendererText()
        combobox1305p.pack_start(renderer_text, True)
        combobox1305p.add_attribute(renderer_text, "text", 0)
    with combobox1305p.handler_block(combobox1305p_handler_id):                               # Prevent widget signal when setting active an item
        liststore1305p.clear()
        for disk in Performance.disk_list_system_ordered:
            liststore1305p.append([disk])
        combobox1305p.set_active(Performance.selected_disk_number)


# ********************** Set Network tab popover menu GUI object data/selections appropriate for settings **********************
def network_tab_popover_set_gui():

    # Set active comboboxes if network download speed/network upload speed values are "1"
    if Config.plot_network_download_speed == 1:
        checkbutton1401p.set_active(True)
    if Config.plot_network_download_speed == 0:
        checkbutton1401p.set_active(False)
    if Config.plot_network_upload_speed == 1:
        checkbutton1402p.set_active(True)
    if Config.plot_network_upload_speed == 0:
        checkbutton1402p.set_active(False)

    # Add Network speed data precision data into combobox on the Network tab on the Performance tab
    if "liststore1401p" not in globals():
        global liststore1401p
        liststore1401p = Gtk.ListStore()
        liststore1401p.set_column_types([str, int])
        combobox1401p.set_model(liststore1401p)
        renderer_text = Gtk.CellRendererText()
        combobox1401p.pack_start(renderer_text, True)
        combobox1401p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1401p.append([data[1], data[2]])
    with combobox1401p.handler_block(combobox1401p_handler_id):                               # Prevent widget signal when setting active an item
        combobox1401p.set_active(Config.performance_network_speed_data_precision)

    # Add Network data data precision data into combobox on the Network tab on the Performance tab
    if "liststore1402p" not in globals():
        global liststore1402p
        liststore1402p = Gtk.ListStore()
        liststore1402p.set_column_types([str, int])
        combobox1402p.set_model(liststore1402p)
        renderer_text = Gtk.CellRendererText()
        combobox1402p.pack_start(renderer_text, True)
        combobox1402p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1402p.append([data[1], data[2]])
    with combobox1402p.handler_block(combobox1402p_handler_id):                               # Prevent widget signal when setting active an item
        combobox1402p.set_active(Config.performance_network_data_data_precision)

    # Add Network speed data unit data into combobox on the Network tab on the Performance tab
    if "liststore1403p" not in globals():
        global liststore1403p
        liststore1403p = Gtk.ListStore()
        liststore1403p.set_column_types([str, int])
        combobox1403p.set_model(liststore1403p)
        renderer_text = Gtk.CellRendererText()
        combobox1403p.pack_start(renderer_text, True)
        combobox1403p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_speed_unit_list:
            liststore1403p.append([data[1], data[2]])
    with combobox1403p.handler_block(combobox1403p_handler_id):                               # Prevent widget signal when setting active an item
        for data_list in Config.data_speed_unit_list:
            if data_list[2] == Config.performance_network_speed_data_unit:      
                combobox1403p.set_active(data_list[0])

    # Add Network data data unit data into combobox on the Network tab on the Performance tab
    if "liststore1404p" not in globals():
        global liststore1404p
        liststore1404p = Gtk.ListStore()
        liststore1404p.set_column_types([str, int])
        combobox1404p.set_model(liststore1404p)
        renderer_text = Gtk.CellRendererText()
        combobox1404p.pack_start(renderer_text, True)
        combobox1404p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore1404p.append([data[1], data[2]])
    with combobox1404p.handler_block(combobox1404p_handler_id):                               # Prevent widget signal when setting active an item
        for data_list in Config.data_unit_list:
            if data_list[2] == Config.performance_network_data_data_unit:      
                combobox1404p.set_active(data_list[0])

    # Add Network Card list into combobox on Network tab
    if "liststore1405p" not in globals():
        global liststore1405p
        liststore1405p = Gtk.ListStore()
        liststore1405p.set_column_types([str])
        combobox1405p.set_model(liststore1405p)
        renderer_text = Gtk.CellRendererText()
        combobox1405p.pack_start(renderer_text, True)
        combobox1405p.add_attribute(renderer_text, "text", 0)
    with combobox1405p.handler_block(combobox1405p_handler_id):                               # Prevent widget signal when setting active an item
        liststore1405p.clear()
        for network_card in Performance.network_card_list:
            liststore1405p.append([network_card])
        combobox1405p.set_active(Performance.selected_network_card_number)


# ********************** Set GPU tab popover menu GUI object data/selections appropriate for settings **********************
def gpu_tab_popover_set_gui():

    # Add GPU/graphics card list into combobox on GPU tab
    if "liststore1501p" not in globals():
        global liststore1501p
        liststore1501p = Gtk.ListStore()
        liststore1501p.set_column_types([str])
        combobox1501p.set_model(liststore1501p)
        renderer_text = Gtk.CellRendererText()
        combobox1501p.pack_start(renderer_text, True)
        combobox1501p.add_attribute(renderer_text, "text", 0)
    with combobox1501p.handler_block(combobox1501p_handler_id):                               # Prevent widget signal when setting active an item
        liststore1501p.clear()
        for gpu in Performance.gpu_list:
            liststore1501p.append([gpu])
        combobox1501p.set_active(Performance.selected_gpu_number)
