#!/usr/bin/env python3

# ----------------------------------- Services - Services GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_gui_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global MainGUI, Services, ServicesMenusGUI, ServicesDetails, ServicesDetailsGUI
    import MainGUI, Services, ServicesMenusGUI, ServicesDetails, ServicesDetailsGUI


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- Services - Services GUI Function (the code of this module in order to avoid running them during module import and defines "Services" tab GUI objects and functions/signals) -----------------------------------
def services_gui_func():

    # Services tab GUI objects
    global treeview6101, searchentry6101, button6101, button6102, button6103
    global radiobutton6101, radiobutton6102, radiobutton6103
    global label6101


    # Services tab GUI objects - get
    treeview6101 = MainGUI.builder.get_object('treeview6101')
    searchentry6101 = MainGUI.builder.get_object('searchentry6101')
    button6101 = MainGUI.builder.get_object('button6101')
    button6102 = MainGUI.builder.get_object('button6102')
    button6103 = MainGUI.builder.get_object('button6103')
    radiobutton6101 = MainGUI.builder.get_object('radiobutton6101')
    radiobutton6102 = MainGUI.builder.get_object('radiobutton6102')
    radiobutton6103 = MainGUI.builder.get_object('radiobutton6103')
    label6101 = MainGUI.builder.get_object('label6101')


    # Services tab GUI functions
    def on_treeview6101_button_press_event(widget, event):
        if event.button == 3:                                                                 # Open Services tab right click menu if mouse is right clicked on the treeview (and on any service, otherwise menu will not be shown) and the mouse button is pressed.
            services_open_right_click_menu_func(event)
        if event.type == Gdk.EventType._2BUTTON_PRESS:                                        # Open Service Details window if double click is performed.
            services_open_service_details_window_func(event)

    def on_treeview6101_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Services.services_treeview_column_order_width_row_sorting_func()

    def on_searchentry6101_changed(widget):
        radiobutton6101.set_active(True)
        Services.services_treeview_filter_search_func()

    def on_button6101_clicked(widget):                                                        # "Services Tab Customizations" button
        ServicesMenusGUI.popover6101p.popup()

    def on_button6102_clicked(widget):                                                        # "Services Tab Search Customizations" button
        ServicesMenusGUI.popover6101p2.popup()

    def on_button6103_clicked(widget):                                                        # "Refresh" button
        Services.services_thread_run_func()

    def on_radiobutton6101_toggled(widget):                                                   # "Show all services" radiobutton
        if radiobutton6101.get_active() == True:
            Services.services_treeview_filter_show_all_func()

    def on_radiobutton6102_toggled(widget):                                                   # "Show all loaded services" radiobutton
        if radiobutton6102.get_active() == True:
            Services.services_treeview_filter_show_all_func()
            Services.services_treeview_filter_services_loaded_only()

    def on_radiobutton6103_toggled(widget):                                                   # "Show all non-loaded services" radiobutton
        if radiobutton6103.get_active() == True:
            Services.services_treeview_filter_show_all_func()
            Services.services_treeview_filter_services_not_loaded_only()



    # Services tab GUI functions - connect
    treeview6101.connect("button-press-event", on_treeview6101_button_press_event)
    treeview6101.connect("button-release-event", on_treeview6101_button_release_event)
    searchentry6101.connect("changed", on_searchentry6101_changed)
    button6101.connect("clicked", on_button6101_clicked)
    button6102.connect("clicked", on_button6102_clicked)
    button6103.connect("clicked", on_button6103_clicked)
    radiobutton6101.connect("toggled", on_radiobutton6101_toggled)
    radiobutton6102.connect("toggled", on_radiobutton6102_toggled)
    radiobutton6103.connect("toggled", on_radiobutton6103_toggled)


    # Services Tab - Treeview Properties
    treeview6101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview6101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview6101.set_headers_clickable(True)
    treeview6101.set_show_expanders(False)
    treeview6101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview6101.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview6101.set_tooltip_column(2)


# ----------------------------------- Services - Open Right Click Menu Function (gets right clicked service name and opens right click menu) -----------------------------------
def services_open_right_click_menu_func(event):

    path, _, _, _ = treeview6101.get_path_at_pos(int(event.x), int(event.y))
    model = treeview6101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is None:
        services_no_service_selected_dialog()
    if treeiter is not None:
        global selected_service_name
        selected_service_name = Services.service_list[Services.services_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "services_data_rows" list to use it getting name of the service.
        ServicesMenusGUI.menu6101m.popup(None, None, None, None, event.button, event.time)
        ServicesMenusGUI.services_set_checkmenuitem_func()


# ----------------------------------- Services - Open Service Details Window Function (gets double clicked service nam and opens Service Details window) -----------------------------------
def services_open_service_details_window_func(event):

    if event.type == Gdk.EventType._2BUTTON_PRESS:                                            # Check if double click is performed
        path, _, _, _ = treeview6101.get_path_at_pos(int(event.x), int(event.y))
        model = treeview6101.get_model()
        treeiter = model.get_iter(path)
        if treeiter is None:
            services_no_service_selected_dialog()
        if treeiter is not None:
            global selected_service_name
            selected_service_name = Services.service_list[Services.services_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "services_data_rows" list to use it getting name of the service.
            # Open Service Details window
            ServicesDetailsGUI.services_details_gui_function()
            ServicesDetailsGUI.window6101w.show()
            ServicesDetails.services_details_foreground_thread_run_func()


# ----------------------------------- Services - No Service Selected Dialog Function (shows a dialog when Open Services Right Click Menu is clicked without selecting a service) -----------------------------------
def services_no_service_selected_dialog():

    dialog6101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Select A Service"), )
    dialog6101.format_secondary_text(_tr("Please select a service and try again for opening the menu"))
    dialog6101.run()
    dialog6101.destroy()
