#!/usr/bin/env python3

# ----------------------------------- RAM - RAM Tab Menus GUI Import Function -----------------------------------
def ram_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, Ram, Performance
    import Config, Ram, Performance


# ----------------------------------- RAM - RAM Tab Menus GUI Function -----------------------------------
def ram_menus_gui_func():

    # Define builder and get all objects (Performance tab RAM sub-tab customizations popovers) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RamMenus.ui")


    # Define a colorchooserdialog in order to set chart colors
    global colorchooserdialog1001
    colorchooserdialog1001 = Gtk.ColorChooserDialog()

    # ********************** Define object names for RAM tab popover **********************
    global popover1201p
    global button1201p, button1202p, button1203p
    global combobox1201p, combobox1202p

    # ********************** Get objects for RAM tab popover **********************
    popover1201p = builder.get_object('popover1201p')
    button1201p = builder.get_object('button1201p')
    button1202p = builder.get_object('button1202p')
    button1203p = builder.get_object('button1203p')
    combobox1201p = builder.get_object('combobox1201p')
    combobox1202p = builder.get_object('combobox1202p')

    # ********************** Define object functions for RAM tab popover **********************
    def on_popover1201p_show(widget):                                                         # Perform following operations on popover menu show.
        try:
            ram_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        ram_tab_popover_set_gui()
        ram_tab_customization_popover_connect_signals_func()

    def on_button1201p_clicked(widget):                                                       # For setting chart foreground color
        red, blue, green, alpha = Config.chart_line_color_ram_swap_percent                    # Get current foreground color of the chart
        colorchooserdialog1001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart foregorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog1001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog1001.get_rgba()
            Config.chart_line_color_ram_swap_percent = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog1001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog1001.hide()
        Ram.ram_initial_func()
        Ram.ram_loop_func()

    def on_button1202p_clicked(widget):                                                       # For setting chart background color
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
        Ram.ram_initial_func()
        Ram.ram_loop_func()

    def on_combobox1201p_changed(widget):                                                     # Option for defining "RAM/Swap data number precision" shown by using labels
        Config.performance_ram_swap_data_precision = Config.number_precision_list[combobox1201p.get_active()][2]
        Ram.ram_initial_func()
        Ram.ram_loop_func()
        Config.config_save_func()

    def on_combobox1202p_changed(widget):                                                     # Option for defining "RAM/Swap data units" shown by using labels
        Config.performance_ram_swap_data_unit = Config.data_unit_list[combobox1202p.get_active()][2]
        Ram.ram_initial_func()
        Ram.ram_loop_func()
        Config.config_save_func()

    def on_button1203p_clicked(widget):                                                       # For resetting all RAM tab settings
        Config.config_default_performance_ram_func()
        Config.config_save_func()
        ram_tab_customization_popover_disconnect_signals_func()
        ram_tab_popover_set_gui()                                                             # Apply setting changes on the RAM tab popover GUI
        ram_tab_customization_popover_connect_signals_func()
        Ram.ram_initial_func()
        Ram.ram_loop_func()


    # ********************** Connect signals to GUI objects for RAM tab **********************
    popover1201p.connect("show", on_popover1201p_show)
    button1201p.connect("clicked", on_button1201p_clicked)
    button1202p.connect("clicked", on_button1202p_clicked)
    button1203p.connect("clicked", on_button1203p_clicked)

    # ********************** Define function for connecting Performance tab RAM sub-tab customizations popover GUI signals **********************
    def ram_tab_customization_popover_connect_signals_func():
        combobox1201p_handler_id = combobox1201p.connect("changed", on_combobox1201p_changed)
        combobox1202p_handler_id = combobox1202p.connect("changed", on_combobox1202p_changed)

    # ********************** Define function for disconnecting Performance tab RAM sub-tab customizations popover GUI signals **********************
    def ram_tab_customization_popover_disconnect_signals_func():
        combobox1201p.disconnect_by_func(on_combobox1201p_changed)
        combobox1202p.disconnect_by_func(on_combobox1202p_changed)


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
    for data_list in Config.data_unit_list:
        if data_list[2] == Config.performance_ram_swap_data_unit:      
            combobox1202p.set_active(data_list[0])
