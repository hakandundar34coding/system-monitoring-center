#!/usr/bin/env python3

# ----------------------------------- Common - Import Function -----------------------------------
def common_import_func():

    global Gtk, Gdk

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk


# ----------------------------------- Common - Mouse Actions On Treeview Function -----------------------------------
def common_mouse_actions_on_treeview_func(event, current_tab, current_treeview, tab_data_list, tab_data_rows):

    try:                                                                                      # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = current_treeview.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = current_treeview.get_model()
    treeiter = model.get_iter(path)
    if treeiter is not None:
        global selected_row_data
        try:
            if current_tab == "Processes":
                global selected_process_pid
                selected_process_pid = tab_data_list[tab_data_rows.index(model[treeiter][:])]
            if current_tab == "Users":
                global selected_user_uid, selected_username
                selected_user_uid = tab_data_list[tab_data_rows.index(model[treeiter][:])][0]
                selected_username = tab_data_list[tab_data_rows.index(model[treeiter][:])][1]
            if current_tab == "Startup":
                global selected_startup_application_file_name, selected_startup_application_visibility, selected_startup_application_name
                selected_startup_application_file_name = tab_data_list[0][tab_data_rows.index(model[treeiter][:])]
                selected_startup_application_visibility = tab_data_list[1][tab_data_rows.index(model[treeiter][:])]
                selected_startup_application_name = model[treeiter][3]
            if current_tab == "Services":
                global selected_service_name
                selected_service_name = tab_data_list[tab_data_rows.index(model[treeiter][:])]
        except ValueError:                                                                    # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'asush', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely. It is handled in this situation.
            return


    if event.button == 3:                                                                     # Open right click menu of the relevant tab if mouse is right clicked on any row on the treeview.
        common_right_click_menu_function(event, current_tab)
    if event.type == Gdk.EventType._2BUTTON_PRESS:                                            # Open details window of the relevant tab if double click is performed on any row on the treeview.
        common_details_window_function(current_tab)


# ----------------------------------- Common - Right Click Menu Function -----------------------------------
def common_right_click_menu_function(event, current_tab):

    if current_tab == "Processes":
        if 'ProcessesMenuRightClick' not in globals():
            global ProcessesMenuRightClick
            import ProcessesMenuRightClick
            ProcessesMenuRightClick.processes_menu_right_click_import_func()
            ProcessesMenuRightClick.processes_menu_right_click_gui_func()
        ProcessesMenuRightClick.menu2101m.popup(None, None, None, None, event.button, event.time)
        ProcessesMenuRightClick.processes_select_process_nice_option_func()
        return

    if current_tab == "Users":
        if 'UsersMenuRightClick' not in globals():
            global UsersMenuRightClick
            import UsersMenuRightClick
            UsersMenuRightClick.users_menu_right_click_import_func()
            UsersMenuRightClick.users_menu_right_click_gui_func()
        UsersMenuRightClick.menu3101m.popup(None, None, None, None, event.button, event.time)
        return

    if current_tab == "Startup":
        if 'StartupMenuRightClick' not in globals():
            global StartupMenuRightClick
            import StartupMenuRightClick
            StartupMenuRightClick.startup_menu_right_click_import_func()
            StartupMenuRightClick.startup_menu_right_click_gui_func()
        StartupMenuRightClick.menu5101m.popup(None, None, None, None, event.button, event.time)
        StartupMenuRightClick.startup_set_checkmenuitem_func()
        StartupMenuRightClick.startup_set_menu_labels_func()
        return

    if current_tab == "Services":
        if 'ServicesMenuRightClick' not in globals():
            global ServicesMenuRightClick
            import ServicesMenuRightClick
            ServicesMenuRightClick.services_menu_right_click_import_func()
            ServicesMenuRightClick.services_menu_right_click_gui_func()
        ServicesMenuRightClick.menu6101m.popup(None, None, None, None, event.button, event.time)
        ServicesMenuRightClick.services_set_checkmenuitem_func()
        return


# ----------------------------------- Common - Details Window Function -----------------------------------
def common_details_window_function(current_tab):

    if current_tab == "Processes":
        if 'ProcessesDetails' not in globals():
            global ProcessesDetails
            import ProcessesDetails
            ProcessesDetails.processes_details_import_func()
            ProcessesDetails.processes_details_gui_function()
        ProcessesDetails.window2101w.show()
        ProcessesDetails.process_details_run_func()
        return

    if current_tab == "Users":
        if 'UsersDetails' not in globals():
            global UsersDetails
            import UsersDetails
            UsersDetails.users_details_import_func()
            UsersDetails.users_details_gui_function()
        UsersDetails.window3101w.show()
        UsersDetails.users_details_run_func()
        return

    if current_tab == "Services":
        if 'ServicesDetails' not in globals():
            global ServicesDetails
            import ServicesDetails
            ServicesDetails.services_details_import_func()
            ServicesDetails.services_details_gui_function()
        ServicesDetails.window6101w.show()
        ServicesDetails.services_details_run_func()
        return
