#!/usr/bin/env python3

# ----------------------------------- GPU - GPU Tab Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def gpu_menus_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global Config, Gpu, Performance
    from . import Config, Gpu, Performance


# ----------------------------------- GPU - GPU Tab Menus GUI Function (the code of this module in order to avoid running them during module import and defines "GPU" tab menu/popover GUI objects and functions/signals) -----------------------------------
def gpu_menus_gui_func():

    # Define builder and get all objects (Performance tab GPU sub-tab customizations popovers) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuMenus.ui")

    # Define a colorchooserdialog in order to set chart colors
    global colorchooserdialog1001
    colorchooserdialog1001 = Gtk.ColorChooserDialog()

    # ********************** Define object names for GPU tab popover **********************
    global popover1501p
    global button1501p, button1502p, button1503p, button1504p
    global combobox1501p

    # ********************** Get objects for GPU tab popover **********************
    popover1501p = builder.get_object('popover1501p')
    button1501p = builder.get_object('button1501p')
    button1502p = builder.get_object('button1502p')
    button1503p = builder.get_object('button1503p')
    button1504p = builder.get_object('button1504p')
    combobox1501p = builder.get_object('combobox1501p')


    # ********************** Define object functions for GPU tab popover **********************
    def on_popover1501p_show(widget):                                                         # Perform following operations on popover menu show.
        try:
            gpu_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        gpu_tab_popover_set_gui()
        gpu_tab_customization_popover_connect_signals_func()

    def on_button1502p_clicked(widget):                                                       # For setting chart foreground color
        red, blue, green, alpha = Config.chart_line_color_fps                                 # Get current foreground color of the chart
        colorchooserdialog1001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart foregorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog1001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog1001.get_rgba()
            Config.chart_line_color_fps = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog1001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog1001.hide()
        Gpu.gpu_initial_func()                                                                # Call this function in order to apply changes
        Gpu.gpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1503p_clicked(widget):                                                       # For setting chart background color
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
        Gpu.gpu_initial_func()                                                                # Call this function in order to apply changes
        Gpu.gpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).

    def on_combobox1501p_changed(widget):                                                     # Option for defining "selected gpu/graphics card" which affects information shown on the GUI
        Config.selected_gpu = Performance.gpu_list[combobox1501p.get_active()]
        Performance.set_selected_gpu = Config.selected_gpu
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                      # Call this function in order to apply changes
        Gpu.gpu_initial_func()                                                                # Call this function in order to apply changes
        Gpu.gpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1504p_clicked(widget):                                                       # For resetting all GPU tab settings
        Config.config_default_performance_gpu_func()
        Config.config_save_func()
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                      # Call this function in order to apply changes
        gpu_tab_customization_popover_disconnect_signals_func()
        gpu_tab_popover_set_gui()
        gpu_tab_customization_popover_connect_signals_func()
        Gpu.gpu_initial_func()                                                                # Call this function in order to apply changes
        Gpu.gpu_loop_func()                                                                   # Call this function in order to apply changes immediately (without waiting update interval).


    # ********************** Connect signals to GUI objects for GPU tab **********************
    popover1501p.connect("show", on_popover1501p_show)
    button1502p.connect("clicked", on_button1502p_clicked)
    button1503p.connect("clicked", on_button1503p_clicked)
    button1504p.connect("clicked", on_button1504p_clicked)

    # ********************** Define function for connecting Performance tab GPU sub-tab customizations popover GUI signals **********************
    def gpu_tab_customization_popover_connect_signals_func():
        combobox1501p.connect("changed", on_combobox1501p_changed)

    # ********************** Define function for disconnecting Performance tab GPU sub-tab customizations popover GUI signals **********************
    def gpu_tab_customization_popover_disconnect_signals_func():
        combobox1501p.disconnect_by_func(on_combobox1501p_changed)


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
    liststore1501p.clear()
    for gpu in Performance.gpu_list:
        liststore1501p.append([gpu])
    combobox1501p.set_active(Performance.selected_gpu_number)
