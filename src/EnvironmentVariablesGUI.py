#!/usr/bin/env python3

# ----------------------------------- EnvironmentVariables - EnvironmentVariables GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_gui_import_func():

    global Gtk

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk


    global MainGUI, EnvironmentVariables, EnvironmentVariablesMenusGUI
    import MainGUI, EnvironmentVariables, EnvironmentVariablesMenusGUI


# ----------------------------------- EnvironmentVariables - EnvironmentVariables GUI Function (the code of this module in order to avoid running them during module import and defines "EnvironmentVariables" tab GUI objects and functions/signals) -----------------------------------
def environment_variables_gui_func():

    # Environment Variables tab GUI objects
    global treeview7101, searchentry7101, button7101, button7103, button7104
    global radiobutton7101, radiobutton7102, radiobutton7103
    global label7101


    # Environment Variables tab GUI objects - get
    treeview7101 = MainGUI.builder.get_object('treeview7101')
    searchentry7101 = MainGUI.builder.get_object('searchentry7101')
    button7101 = MainGUI.builder.get_object('button7101')
    button7103 = MainGUI.builder.get_object('button7103')
    button7104 = MainGUI.builder.get_object('button7104')
    radiobutton7101 = MainGUI.builder.get_object('radiobutton7101')
    radiobutton7102 = MainGUI.builder.get_object('radiobutton7102')
    radiobutton7103 = MainGUI.builder.get_object('radiobutton7103')
    label7101 = MainGUI.builder.get_object('label7101')


    # Environment Variables tab GUI functions
    def on_treeview7101_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            EnvironmentVariables.environment_variables_treeview_column_order_width_row_sorting_func()
        if event.button == 3:                                                                 # Open Environment Variables tab right click menu if mouse is right clicked on the treeview (and on any variable, otherwise menu will not be shown) and the mouse button is released.
            environment_variables_open_right_click_menu_func(event)

    def on_searchentry7101_changed(widget):
        radiobutton7101.set_active(True)
        EnvironmentVariables.environment_variables_treeview_filter_search_func()

    def on_button7101_clicked(widget):                                                        # "Environment Variables Tab Customizations" button
        EnvironmentVariablesMenusGUI.popover7101p.popup()

    def on_button7103_clicked(widget):                                                        # "Environment Variables Tab Search Customizations" button
        EnvironmentVariablesMenusGUI.popover7101p2.popup()

    def on_button7104_button_release_event(widget, event):                                    # Open Variable Right Click Menu" button
        if event.button == 1:                                                                 # Open Environment Variables tab right click menu if mouse is right clicked on the treeview (and on any variable, otherwise menu will not be shown) and the mouse button is released.
            environment_variables_open_right_click_menu_func(event)

    def on_radiobutton7101_toggled(widget):                                                   # "Show all environment/shell variables" radiobutton
        if radiobutton7101.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_show_all_func()

    def on_radiobutton7102_toggled(widget):                                                   # "Show all environment variables" radiobutton
        if radiobutton7102.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_show_all_func()
            EnvironmentVariables.environment_variables_treeview_filter_environment_variables_logged_in_only()

    def on_radiobutton7103_toggled(widget):                                                   # "Show all shell variables" radiobutton
        if radiobutton7103.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_show_all_func()
            EnvironmentVariables.environment_variables_treeview_filter_environment_variables_logged_out_only()



    # Environment Variables tab GUI functions - connect
    treeview7101.connect("button-release-event", on_treeview7101_button_release_event)
    searchentry7101.connect("changed", on_searchentry7101_changed)
    button7101.connect("clicked", on_button7101_clicked)
    button7103.connect("clicked", on_button7103_clicked)
    button7104.connect("button-release-event", on_button7104_button_release_event)
    radiobutton7101.connect("toggled", on_radiobutton7101_toggled)
    radiobutton7102.connect("toggled", on_radiobutton7102_toggled)
    radiobutton7103.connect("toggled", on_radiobutton7103_toggled)


    # Environment Variables Tab - Treeview Properties
    treeview7101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview7101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview7101.set_headers_clickable(True)
    treeview7101.set_show_expanders(False)
    treeview7101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview7101.set_search_column(1)                                                         # This command used for searching by using entry.
    treeview7101.set_tooltip_column(1)


# ----------------------------------- Environment Variables - Open Right Click Menu Function (gets right clicked variable name and opens right click menu) -----------------------------------
def environment_variables_open_right_click_menu_func(event):

    model, treeiter = treeview7101.get_selection().get_selected()
    if treeiter is not None:
        global selected_environment_variable
        selected_environment_variable = EnvironmentVariables.variable_list[EnvironmentVariables.environment_variables_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "environment_variables_data_rows" list to use it getting name of the variable.
        EnvironmentVariablesMenusGUI.menu7101m.popup(None, None, None, None, event.button, event.time)
