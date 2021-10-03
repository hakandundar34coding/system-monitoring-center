#!/usr/bin/env python3

# ----------------------------------- Network - Network Tab Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def network_menus_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global Config, NetworkGUI, Network, Performance
    import Config, NetworkGUI, Network, Performance


# ----------------------------------- Network - Network Tab Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Network" tab menu/popover GUI objects and functions/signals) -----------------------------------
def network_menus_gui_func():

    # Define builder and get all objects (Performance tab Network sub-tab customizations popovers) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/NetworkMenus.ui")


    # Define a colorchooserdialog in order to set chart colors
    global colorchooserdialog1001
    colorchooserdialog1001 = Gtk.ColorChooserDialog()

    # ********************** Define object names for Network tab popover **********************
    global popover1401p
    global button1401p, button1402p, button1403p
    global combobox1401p, combobox1402p, combobox1403p, combobox1404p, combobox1405p
    global checkbutton1401p, checkbutton1402p

    # ********************** Get objects for Network tab popover **********************
    popover1401p = builder.get_object('popover1401p')
    button1401p = builder.get_object('button1401p')
    button1402p = builder.get_object('button1402p')
    button1403p = builder.get_object('button1403p')
    combobox1401p = builder.get_object('combobox1401p')
    combobox1402p = builder.get_object('combobox1402p')
    combobox1403p = builder.get_object('combobox1403p')
    combobox1404p = builder.get_object('combobox1404p')
    combobox1405p = builder.get_object('combobox1405p')
    checkbutton1401p = builder.get_object('checkbutton1401p')
    checkbutton1402p = builder.get_object('checkbutton1402p')

    # ********************** Define object functions for Network tab popover **********************
    def on_popover1401p_show(widget):                                                         # Perform following operations on popover menu show.
        try:
            network_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        network_tab_popover_set_gui()
        network_tab_customization_popover_connect_signals_func()

    def on_checkbutton1401p_toggled(widget):                                                  # Option for showing "network download speed" on the chart
        if checkbutton1401p.get_active() == True:
            Config.plot_network_download_speed = 1
        if checkbutton1401p.get_active() == False:
            if checkbutton1402p.get_active() == False:
                checkbutton1401p.set_active(True)
                return
            Config.plot_network_download_speed = 0
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_checkbutton1402p_toggled(widget):                                                  # Option for showing "network upload speed" on the chart
        if checkbutton1402p.get_active() == True:
            Config.plot_network_upload_speed = 1
        if checkbutton1402p.get_active() == False:
            if checkbutton1401p.get_active() == False:
                checkbutton1402p.set_active(True)
                return
            Config.plot_network_upload_speed = 0
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1401p_clicked(widget):                                                       # For setting chart foreground color
        red, blue, green, alpha = Config.chart_line_color_network_speed_data                  # Get current foreground color of the chart
        colorchooserdialog1001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart foregorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog1001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog1001.get_rgba()
            Config.chart_line_color_network_speed_data = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog1001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog1001.hide()
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).

    def on_button1402p_clicked(widget):                                                       # For setting chart background color
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
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).

    def on_combobox1401p_changed(widget):                                                     # Option for defining "network download/upload speed number precision" shown by using label
        Config.performance_network_speed_data_precision = Config.number_precision_list[combobox1401p.get_active()][2]
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1402p_changed(widget):                                                     # Option for defining "network download/upload data number precision" shown by using label
        Config.performance_network_data_data_precision = Config.number_precision_list[combobox1402p.get_active()][2]
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1403p_changed(widget):                                                     # Option for defining "network download/upload speed data units" shown by using label
        Config.performance_network_speed_data_unit = Config.data_speed_unit_list[combobox1403p.get_active()][2]
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1404p_changed(widget):                                                     # Option for defining "network download/upload data units" shown by using label
        Config.performance_network_data_data_unit = Config.data_unit_list[combobox1404p.get_active()][2]
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_combobox1405p_changed(widget):                                                     # Option for defining "selected network card" which affects information shown on the GUI
        Config.selected_network_card = Performance.network_card_list[combobox1405p.get_active()]
        Performance.set_selected_network_card = Config.selected_network_card
        Performance.performance_set_selected_network_card_func()                              # Call this function in order to apply changes
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).
        Config.config_save_func()

    def on_button1403p_clicked(widget):                                                       # For resetting all Network tab settings
        Config.config_default_performance_network_func()
        Config.config_save_func()
        Performance.performance_set_selected_network_card_func()                              # Call this function in order to apply changes
        network_tab_customization_popover_disconnect_signals_func()
        network_tab_popover_set_gui()
        network_tab_customization_popover_connect_signals_func()
        Network.network_initial_func()                                                        # Call this function in order to apply changes immediately (without waiting update interval).
        Network.network_loop_func()                                                           # Call this function in order to apply changes immediately (without waiting update interval).



    # ********************** Connect signals to GUI objects for Network tab **********************
    popover1401p.connect("show", on_popover1401p_show)
    button1401p.connect("clicked", on_button1401p_clicked)
    button1402p.connect("clicked", on_button1402p_clicked)
    button1403p.connect("clicked", on_button1403p_clicked)

    # ********************** Define function for connecting Performance tab Network sub-tab customizations popover GUI signals **********************
    def network_tab_customization_popover_connect_signals_func():
        checkbutton1401p.connect("toggled", on_checkbutton1401p_toggled)
        checkbutton1402p.connect("toggled", on_checkbutton1402p_toggled)
        combobox1401p.connect("changed", on_combobox1401p_changed)
        combobox1402p.connect("changed", on_combobox1402p_changed)
        combobox1403p.connect("changed", on_combobox1403p_changed)
        combobox1404p.connect("changed", on_combobox1404p_changed)
        combobox1405p.connect("changed", on_combobox1405p_changed)

    # ********************** Define function for disconnecting Performance tab Network sub-tab customizations popover GUI signals **********************
    def network_tab_customization_popover_disconnect_signals_func():
        checkbutton1401p.disconnect_by_func(on_checkbutton1401p_toggled)
        checkbutton1402p.disconnect_by_func(on_checkbutton1402p_toggled)
        combobox1401p.disconnect_by_func(on_combobox1401p_changed)
        combobox1402p.disconnect_by_func(on_combobox1402p_changed)
        combobox1403p.disconnect_by_func(on_combobox1403p_changed)
        combobox1404p.disconnect_by_func(on_combobox1404p_changed)
        combobox1405p.disconnect_by_func(on_combobox1405p_changed)


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
    liststore1405p.clear()
    for network_card in Performance.network_card_list:
        liststore1405p.append([network_card])
    combobox1405p.set_active(Performance.selected_network_card_number)
