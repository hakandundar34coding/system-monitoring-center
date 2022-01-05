#!/usr/bin/env python3

# ----------------------------------- Disk - Disk Tab Menus GUI Import Function -----------------------------------
def disk_menus_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global Config, Disk, Performance
    import Config, Disk, Performance


# ----------------------------------- Disk - Disk Tab Menus GUI Function -----------------------------------
def disk_menus_gui_func():

    # Define builder and get all objects (Performance tab Disk sub-tab customizations popovers) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskMenus.ui")


    # Define a colorchooserdialog in order to set chart colors
    global colorchooserdialog1001
    colorchooserdialog1001 = Gtk.ColorChooserDialog()

    # ********************** Define object names for Disk tab popover **********************
    global popover1301p
    global button1301p, button1302p, button1303p
    global combobox1301p, combobox1302p, combobox1303p, combobox1304p, combobox1305p
    global checkbutton1301p, checkbutton1302p

    # ********************** Get objects for Disk tab popover **********************
    popover1301p = builder.get_object('popover1301p')
    button1301p = builder.get_object('button1301p')
    button1302p = builder.get_object('button1302p')
    button1303p = builder.get_object('button1303p')
    combobox1301p = builder.get_object('combobox1301p')
    combobox1302p = builder.get_object('combobox1302p')
    combobox1303p = builder.get_object('combobox1303p')
    combobox1304p = builder.get_object('combobox1304p')
    combobox1305p = builder.get_object('combobox1305p')
    checkbutton1301p = builder.get_object('checkbutton1301p')
    checkbutton1302p = builder.get_object('checkbutton1302p')

    # ********************** Define object functions for Disk tab popover **********************
    def on_popover1301p_show(widget):                                                         # Perform following operations on popover menu show.
        try:
            disk_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        disk_tab_popover_set_gui()
        disk_tab_customization_popover_connect_signals_func()

    def on_checkbutton1301p_toggled(widget):                                                  # Option for showing "disk read speed" on the chart
        if checkbutton1301p.get_active() == True:
            Config.plot_disk_read_speed = 1
        if checkbutton1301p.get_active() == False:
            if checkbutton1302p.get_active() == False:
                checkbutton1301p.set_active(True)
                return
            Config.plot_disk_read_speed = 0
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_checkbutton1302p_toggled(widget):                                                  # Option for showing "disk write speed" on the chart
        if checkbutton1302p.get_active() == True:
            Config.plot_disk_write_speed = 1
        if checkbutton1302p.get_active() == False:
            if checkbutton1301p.get_active() == False:
                checkbutton1302p.set_active(True)
                return
            Config.plot_disk_write_speed = 0
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1301p_clicked(widget):                                                       # For setting chart foreground color
        red, blue, green, alpha = Config.chart_line_color_disk_speed_usage                    # Get current foreground color of the chart
        colorchooserdialog1001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart foregorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog1001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog1001.get_rgba()
            Config.chart_line_color_disk_speed_usage = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog1001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog1001.hide()
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1302p_clicked(widget):                                                       # For setting chart background color
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
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).

    def on_combobox1301p_changed(widget):                                                     # Option for defining "disk read/write speed number precision" shown by using label
        Config.performance_disk_speed_data_precision = Config.number_precision_list[combobox1301p.get_active()][2]
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1302p_changed(widget):                                                     # Option for defining "disk read/write data number precision" shown by using label
        Config.performance_disk_usage_data_precision = Config.data_unit_list[combobox1302p.get_active()][2]
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1303p_changed(widget):                                                     # Option for defining "disk read/write speed data units" shown by using label
        Config.performance_disk_speed_data_unit = Config.data_speed_unit_list[combobox1303p.get_active()][2]
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1304p_changed(widget):                                                     # Option for defining "disk read/write data units" shown by using label
        Config.performance_disk_usage_data_unit = Config.data_unit_list[combobox1304p.get_active()][2]
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1305p_changed(widget):                                                     # Option for defining "selected disk" which affects information shown on the GUI
        Config.selected_disk = Performance.disk_list_system_ordered[combobox1305p.get_active()]
        Disk.selected_disk_number = Config.selected_disk
        Performance.performance_set_selected_disk_func()
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1303p_clicked(widget):                                                       # For resetting all Disk tab settings
        Config.config_default_performance_disk_func()
        Config.config_save_func()
        Performance.performance_set_selected_disk_func()
        disk_tab_customization_popover_disconnect_signals_func()
        disk_tab_popover_set_gui()
        disk_tab_customization_popover_connect_signals_func()
        Disk.disk_initial_func()                                                              # Call this function in order to apply changes immediately (without waiting update interval).
        Disk.disk_loop_func()                                                                 # Call this function in order to apply changes immediately (without waiting update interval).


    # ********************** Connect signals to GUI objects for Disk tab **********************
    popover1301p.connect("show", on_popover1301p_show)
    button1301p.connect("clicked", on_button1301p_clicked)
    button1302p.connect("clicked", on_button1302p_clicked)
    button1303p.connect("clicked", on_button1303p_clicked)

    # ********************** Define function for connecting Performance tab Disk sub-tab customizations popover GUI signals **********************
    def disk_tab_customization_popover_connect_signals_func():
        checkbutton1301p.connect("toggled", on_checkbutton1301p_toggled)
        checkbutton1302p.connect("toggled", on_checkbutton1302p_toggled)
        combobox1301p.connect("changed", on_combobox1301p_changed)
        combobox1302p.connect("changed", on_combobox1302p_changed)
        combobox1303p.connect("changed", on_combobox1303p_changed)
        combobox1304p.connect("changed", on_combobox1304p_changed)
        combobox1305p.connect("changed", on_combobox1305p_changed)

    # ********************** Define function for disconnecting Performance tab Disk sub-tab customizations popover GUI signals **********************
    def disk_tab_customization_popover_disconnect_signals_func():
        checkbutton1301p.disconnect_by_func(on_checkbutton1301p_toggled)
        checkbutton1302p.disconnect_by_func(on_checkbutton1302p_toggled)
        combobox1301p.disconnect_by_func(on_combobox1301p_changed)
        combobox1302p.disconnect_by_func(on_combobox1302p_changed)
        combobox1303p.disconnect_by_func(on_combobox1303p_changed)
        combobox1304p.disconnect_by_func(on_combobox1304p_changed)
        combobox1305p.disconnect_by_func(on_combobox1305p_changed)


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
    liststore1305p.clear()
    for disk in Performance.disk_list_system_ordered:
        liststore1305p.append([disk])
    combobox1305p.set_active(Performance.selected_disk_number)
