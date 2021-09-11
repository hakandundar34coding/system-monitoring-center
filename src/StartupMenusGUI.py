#!/usr/bin/env python3

# ----------------------------------- Startup - Startup Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def startup_menus_import_func():

    global Gtk, Gdk, Gio, os, subprocess, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, Gio
    import os
    import subprocess
    from threading import Thread


    global Config, MainGUI, Startup, StartupGUI, StartupNewItemGUI
    import Config, MainGUI, Startup, StartupGUI, StartupNewItemGUI


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


# ----------------------------------- Startup - Startup Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Startup" tab menu/popover GUI objects and functions/signals) -----------------------------------
def startup_menus_gui_func():

    # Define builder and get all objects (Startup tab right click menu, Startup tab customizations popover, Startup tab search customizations popover) from GUI file.
    builder5101m = Gtk.Builder()
    builder5101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupMenus.ui")

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Startup tab right click menu
    # ********************** Define object names for Startup tab right click menu **********************
    global menu5101m
    global checkmenuitem5101m, menuitem5102m, menuitem5103m, menuitem5105m, sub_menuitem5101m, sub_menuitem5102m

    # ********************** Get object names for Startup tab right click menu **********************
    menu5101m = builder5101m.get_object('menu5101m')
    checkmenuitem5101m = builder5101m.get_object('checkmenuitem5101m')
    menuitem5102m = builder5101m.get_object('menuitem5102m')
    menuitem5103m = builder5101m.get_object('menuitem5103m')
    menuitem5105m = builder5101m.get_object('menuitem5105m')
    sub_menuitem5101m = builder5101m.get_object('sub_menuitem5101m')
    sub_menuitem5102m = builder5101m.get_object('sub_menuitem5102m')

    # ********************** Define object functions for Startup tab right click menu **********************
    def on_checkmenuitem5101m_toggled(widget):                                                # "Enable/Disable" item on the right click menu
        selected_startup_application_file_name = StartupGUI.selected_startup_application_file_name
        treestore5101 = Startup.treestore5101
        startup_get_system_and_user_autostart_directories_func()
        hidden_value_system = ""
        not_show_in_value_system = ""
        only_show_in_value_system = ""
        xfce_autostart_override_value_system = ""
        if os.path.exists(system_autostart_directory + selected_startup_application_file_name) == True:
            with open(system_autostart_directory + selected_startup_application_file_name) as reader:    # Get content of the ".desktop" file in the system autostart directory
                desktop_file_system_lines = reader.read().strip("").split("\n")
            try:
                desktop_file_system_lines.remove("")                                          # Remove empty lines (if exist)
            except:
                pass
            for line in desktop_file_system_lines:
                if "Hidden=" in line:                                                         # Application "hidden" value. Application is not started on the system start if this value is "true". This value overrides "NotShowIn" and "OnlyShowIn" values.
                    hidden_value_system = line.split("=")[1]
                if "NotShowIn" in line:                                                       # Application "NotShowIn" value. Application is not started on the system start if name of the current desktop session (XFCE, GNOME, etc.) is in this value. Desktop session name may not exist in both "NotShowIn" and "OnlyShowIn" values. Application is not started on the system start in this situation.
                    not_show_in_value_system = line.split("=")[1].split(";")
                if "OnlyShowIn" in line:                                                      # Application "OnlyShowIn" value. Application is started on the system start only if name of the current desktop session (XFCE, GNOME, etc.) is in this value. Desktop session name may not exist in both "NotShowIn" and "OnlyShowIn" values. Application is not started on the system start in this situation.
                    only_show_in_value_system = line.split("=")[1].split(";")
                if "X-XFCE-Autostart-Override" in line:                                       # Application "X-XFCE-Autostart-Override". If this value is "true", application is started on the system start if current desktop session name is in "NotShowIn" value or not in "OnlyShowIn" value.
                    xfce_autostart_override_value_system = line.split("=")[1]
        hidden_value_user = ""
        not_show_in_value_user = ""
        only_show_in_value_user = ""
        xfce_autostart_override_value_user = ""
        if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
            with open(current_user_autostart_directory + selected_startup_application_file_name) as reader:    # Get content of the ".desktop" file in the user autostart directory
                desktop_file_user_lines = reader.read().strip("").split("\n")
            try:
                desktop_file_user_lines.remove("")                                            # Remove empty lines (if exist)
            except:
                pass
            for line in desktop_file_user_lines:
                if "Hidden=" in line:
                    hidden_value_user = line.split("=")[1]
                if "NotShowIn" in line:
                    not_show_in_value_user = line.split("=")[1].startup_datasplit(";")
                if "OnlyShowIn" in line:
                    only_show_in_value_user = line.split("=")[1].split(";")
                if "X-XFCE-Autostart-Override" in line:
                    xfce_autostart_override_value_user = line.split("=")[1]
        if checkmenuitem5101m.get_active() == True:
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == False:
                with open(current_user_autostart_directory + selected_startup_application_file_name, 'w') as writer:
                    writer.write("[Desktop Entry]" + "\n")
                    if Startup.current_desktop_environment in not_show_in_value_system or (Startup.current_desktop_environment not in only_show_in_value_system and only_show_in_value_system != ""):
                        if Startup.current_desktop_environment == "XFCE":
                            writer.write("X-XFCE-Autostart-Override=true" + "\n")
                    if hidden_value_system == "true":
                        writer.write("Hidden=false" + "\n")
                    return
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
                if Startup.current_desktop_environment in not_show_in_value_system or (Startup.current_desktop_environment not in only_show_in_value_system and only_show_in_value_system != ""):
                    if xfce_autostart_override_value_user != "":
                        for line in desktop_file_user_lines:                                  # Search for visibility value
                            if "X-XFCE-Autostart-Override" in line:
                                desktop_file_user_lines.remove(line)                          # Remove old value from the list
                                desktop_file_user_lines.append("X-XFCE-Autostart-Override=true")    # Append new value into the list
                for line in desktop_file_user_lines:                                          # Search for visibility value
                    if "Hidden=" in line:
                        desktop_file_user_lines.remove(line)                                  # Remove old value from the list
                if hidden_value_system == "true" or hidden_value_user == "true":
                    desktop_file_user_lines.append("Hidden=false")                            # Append new value into the list
                with open(current_user_autostart_directory + selected_startup_application_file_name, 'w') as writer:
                    writer.write('\n'.join(desktop_file_user_lines))
            treestore5101.set_value(Startup.piter_list[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)], 1, True)    # Update startup application visibility (Enabled/Disabled on startup) value in "treestore5101". This will update checkbox on the treeview.
            Startup.startup_applications_visibility_list[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)] = True    # Update startup application visibility (Enabled/Disabled on startup) value in "startup_applications_visibility_list".
            Startup.startup_data_rows[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)][1] = True    # Update startup application visibility (Enabled/Disabled on startup) value in "startup_data_rows". This will prevent errors when right click on the newly enabled/disabled startup item is performed before treeview is updated.

        if checkmenuitem5101m.get_active() == False:
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == False:
                with open(current_user_autostart_directory + selected_startup_application_file_name, 'w') as writer:
                    writer.write("[Desktop Entry]" + "\n")
                    if xfce_autostart_override_value_system == "true":
                        if Startup.current_desktop_environment == "XFCE":
                            writer.write("X-XFCE-Autostart-Override=false" + "\n")
                    if hidden_value_system == "false":
                        writer.write("Hidden=true" + "\n")
                    return
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
                if xfce_autostart_override_value_user != "":
                    for line in desktop_file_user_lines:                                      # Search for visibility value
                        if "X-XFCE-Autostart-Override" in line:
                            desktop_file_user_lines.remove(line)                              # Remove old value from the list
                            desktop_file_user_lines.append("X-XFCE-Autostart-Override=false") # Append new value into the list
                for line in desktop_file_user_lines:                                          # Search for visibility value
                    if "Hidden=" in line:
                        desktop_file_user_lines.remove(line)                                  # Remove old value from the list
                if xfce_autostart_override_value_user == "" and hidden_value_user == "":
                    desktop_file_user_lines.append("Hidden=true")                             # Append new value into the list
                if hidden_value_user == "false":
                    desktop_file_user_lines.append("Hidden=true")                             # Append new value into the list
                with open(current_user_autostart_directory + selected_startup_application_file_name, 'w') as writer:
                    writer.write('\n'.join(desktop_file_user_lines))
            treestore5101.set_value(Startup.piter_list[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)], 1, False)    # Update startup application visibility (Enabled/Disabled on startup) value in "treestore5101". This will update checkbox on the treeview.
            Startup.startup_applications_visibility_list[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)] = False    # Update startup application visibility (Enabled/Disabled on startup) value in "startup_applications_visibility_list".
            Startup.startup_data_rows[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)][1] = False    # Update startup application visibility (Enabled/Disabled on startup) value in "startup_data_rows". This will prevent errors when right click on the newly enabled/disabled startup item is performed before treeview is updated.

        if checkmenuitem5101m.get_active() == False:
            treestore5101.set_value(Startup.piter_list[Startup.all_autostart_applications_list.index(selected_startup_application_file_name)], 1, False)

    def on_menuitem5102m_activate(widget):                                                    # "Add" item on the right click menu
        StartupNewItemGUI.window5101w.show()

    def on_menuitem5103m_activate(widget):                                                    # "Remove" item on the right click menu
        startup_get_system_and_user_autostart_directories_func()
        # Get full name of the startup item and delete its ".desktop" file
        selected_startup_application_file_name = StartupGUI.selected_startup_application_file_name
        os.remove(current_user_autostart_directory + selected_startup_application_file_name)

    def on_sub_menuitem5101m_activate(widget):                                                # "System-wide values file: " item on the right click menu
        default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')       # Get applications which support "text/plain" MIME type. This is MIME type of ".desktop" files. This code gives "default application list" in the order of "open with ..." applications list. Last used application is the first application but more investigation may be done for validity of this observation.
#         default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')     # Default application for the MIME type could be get. But it may give an application other than desired application for viewing/editing ".desktop" files if a text editor is not set default for this file.
        def open_file():                                                                      # Running action is performed in a separate thread for without waiting closing the new opened application.
           subprocess.call([default_app_list_for_content_type[0].get_executable(), desktop_file_system_full_path])    # Open the file with "0th" appliation in the list.
        try:
            open_file_thread = Thread(target=open_file, daemon=True).start()                  # Define a thread and run it
        except FileNotFoundError:
            pass

    def on_sub_menuitem5102m_activate(widget):                                                # "User-specific values file: " item on the right click menu
        default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')       # Get applications which support "text/plain" MIME type. This is MIME type of ".desktop" files. This code gives "default application list" in the order of "open with ..." applications list. Last used application is the first application but more investigation may be done for validity of this observation.
#         default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')     # Default application for the MIME type could be get. But it may give an application other than desired application for viewing/editing ".desktop" files if a text editor is not set default for this file.
        def open_file():                                                                      # Running action is performed in a separate thread for without waiting closing the new opened application.
           subprocess.call([default_app_list_for_content_type[0].get_executable(), desktop_file_user_full_path])    # Open the file with "0th" appliation in the list.
        try:
            open_file_thread = Thread(target=open_file, daemon=True).start()                  # Define a thread and run it
        except FileNotFoundError:
            pass

    # ********************** Connect signals to GUI objects for Startup tab right click menu **********************
    global checkmenuitem5101m_handler_id
    checkmenuitem5101m_handler_id = checkmenuitem5101m.connect("toggled", on_checkmenuitem5101m_toggled)    # Handler id is defined in order to block signals of the checkmenuitem. Because checkmenuitem is set as "activated/deactivated" appropriate with relevant startup application visibility when right click and mouse button release action is finished. This action triggers unwanted event signals.
    menuitem5102m.connect("activate", on_menuitem5102m_activate)
    menuitem5103m.connect("activate", on_menuitem5103m_activate)
    sub_menuitem5101m.connect("activate", on_sub_menuitem5101m_activate)
    sub_menuitem5102m.connect("activate", on_sub_menuitem5102m_activate)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Startup tab customizations popover
    # ********************** Define object names for Startup tab customizations popover **********************
    global popover5101p
    global checkbutton5101p, checkbutton5102p, checkbutton5103p
    global button5101p, button5102p

    # ********************** Get object names for Startup tab customizations popover **********************
    popover5101p = builder5101m.get_object('popover5101p')
    checkbutton5101p = builder5101m.get_object('checkbutton5101p')
    checkbutton5102p = builder5101m.get_object('checkbutton5102p')
    checkbutton5103p = builder5101m.get_object('checkbutton5103p')
    button5101p = builder5101m.get_object('button5101p')
    button5102p = builder5101m.get_object('button5102p')

    # ********************** Define object functions for Startup tab customizations popover Common GUI Objects **********************
    def on_button5101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_startup_func()
        Config.config_save_func()
        startup_tab_customization_popover_disconnect_signals_func()
        startup_tab_popover_set_gui()
        startup_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Startup tab customizations popover View Tab **********************
    def on_button5102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_startup_row_sort_column_order_func()
        startup_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        startup_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Startup tab customizations popover Add/Remove Columns Tab **********************
    def on_checkbutton5101p_toggled(widget):                                                  # "Name" checkbutton
        startup_add_remove_columns_function()
    def on_checkbutton5102p_toggled(widget):                                                  # "Comment" checkbutton
        startup_add_remove_columns_function()
    def on_checkbutton5103p_toggled(widget):                                                  # "Command (Exec)" checkbutton
        startup_add_remove_columns_function()

    # ********************** Connect signals to GUI objects for Startup tab customizations popover Common GUI Objects **********************
    button5101p.connect("clicked", on_button5101p_clicked)
    button5102p.connect("clicked", on_button5102p_clicked)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Startup tab search customizations popover
    # ********************** Define object names for Startup tab search customizations popover **********************
    global popover5101p2
    global radiobutton5101p2, radiobutton5102p2, radiobutton5103p2
    global checkbutton5101p2, checkbutton5102p2, checkbutton5103p2

    # ********************** Get object names for Startup tab search customizations popover **********************
    popover5101p2 = builder5101m.get_object('popover5101p2')
    radiobutton5101p2 = builder5101m.get_object('radiobutton5101p2')
    radiobutton5102p2 = builder5101m.get_object('radiobutton5102p2')
    radiobutton5103p2 = builder5101m.get_object('radiobutton5103p2')
    checkbutton5101p2 = builder5101m.get_object('checkbutton5101p2')
    checkbutton5102p2 = builder5101m.get_object('checkbutton5102p2')
    checkbutton5103p2 = builder5101m.get_object('checkbutton5103p2')

    # ********************** Define object functions for Startup tab search customizations popover **********************
    def on_radiobutton5101p2_toggled(widget):
        if radiobutton5101p2.get_active() == True:
            Startup.startup_treeview_filter_search_func()

    def on_radiobutton5102p2_toggled(widget):
        if radiobutton5102p2.get_active() == True:
            Startup.startup_treeview_filter_search_func()

    def on_radiobutton5103p2_toggled(widget):
        if radiobutton5103p2.get_active() == True:
            Startup.startup_treeview_filter_search_func()

    def on_checkbutton5101p2_toggled(widget):
        startup_popovers_checkbutton_behavior_func(checkbutton5101p2)

    def on_checkbutton5102p2_toggled(widget):
        startup_popovers_checkbutton_behavior_func( checkbutton5102p2)

    def on_checkbutton5103p2_toggled(widget):
        startup_popovers_checkbutton_behavior_func(checkbutton5103p2)

    # ********************** Connect signals to GUI objects for Startup tab search customizations popover **********************
    radiobutton5101p2.connect("toggled", on_radiobutton5101p2_toggled)
    radiobutton5102p2.connect("toggled", on_radiobutton5102p2_toggled)
    radiobutton5103p2.connect("toggled", on_radiobutton5103p2_toggled)
    global checkbutton5101p2_handler_id, checkbutton5102p2_handler_id, checkbutton5103p2_handler_id
    checkbutton5101p2_handler_id = checkbutton5101p2.connect("toggled", on_checkbutton5101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton5102p2_handler_id = checkbutton5102p2.connect("toggled", on_checkbutton5102p2_toggled)
    checkbutton5103p2_handler_id = checkbutton5103p2.connect("toggled", on_checkbutton5103p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Startup tab **********************
    popover5101p.set_relative_to(StartupGUI.button5101)
    popover5101p.set_position(1)
    # ********************** Popover settings for Startup tab search customizations **********************
    popover5101p2.set_relative_to(StartupGUI.button5104)
    popover5101p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



    # ********************** Define function for connecting Startup tab customizations popover GUI signals **********************
    def startup_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Startup tab customizations popover Add/Remove Columns Tab **********************
        checkbutton5101p.connect("toggled", on_checkbutton5101p_toggled)
        checkbutton5102p.connect("toggled", on_checkbutton5102p_toggled)
        checkbutton5103p.connect("toggled", on_checkbutton5103p_toggled)


    # ********************** Define function for disconnecting Startup tab customizations popover GUI signals **********************
    def startup_tab_customization_popover_disconnect_signals_func():
        # ********************** Disconnect signals of GUI objects for Startup tab customizations popover Add/Remove Columns Tab **********************
        checkbutton5101p.disconnect_by_func(on_checkbutton5101p_toggled)
        checkbutton5102p.disconnect_by_func(on_checkbutton5102p_toggled)
        checkbutton5103p.disconnect_by_func(on_checkbutton5103p_toggled)


    startup_tab_popover_set_gui()
    startup_tab_customization_popover_connect_signals_func()


# ********************** Set Startup tab customizations popover menu GUI object data/selections appropriate for settings **********************
def startup_tab_popover_set_gui():
    # Set Startup tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.startup_treeview_columns_shown:
        checkbutton5101p.set_active(True)
    if 0 not in Config.startup_treeview_columns_shown:
        checkbutton5101p.set_active(False)
    if 1 in Config.startup_treeview_columns_shown:
        checkbutton5102p.set_active(True)
    if 1 not in Config.startup_treeview_columns_shown:
        checkbutton5102p.set_active(False)
    if 2 in Config.startup_treeview_columns_shown:
        checkbutton5103p.set_active(True)
    if 2 not in Config.startup_treeview_columns_shown:
        checkbutton5103p.set_active(False)


# ----------------------------------- Startup - Startup Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def startup_popovers_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton5101p2, checkbutton5102p2, checkbutton5103p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton5101p2.handler_block(checkbutton5101p2_handler_id) as p1, checkbutton5102p2.handler_block(checkbutton5102p2_handler_id) as p2, checkbutton5103p2.handler_block(checkbutton5103p2_handler_id) as p3:
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

    if StartupGUI.searchentry5101.get_text() != "":                                         # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the "show all ... disks" radiobuttons above the treeview.
        Startup.startup_treeview_filter_search_func()


# ----------------------------------- Startup - Startup Add/Remove Columns Function (adds/removes storage treeview columns) -----------------------------------
def startup_add_remove_columns_function():

    Config.startup_treeview_columns_shown = []
    if checkbutton5101p.get_active() is True:
        Config.startup_treeview_columns_shown.append(0)
    if checkbutton5102p.get_active() is True:
        Config.startup_treeview_columns_shown.append(1)
    if checkbutton5103p.get_active() is True:
        Config.startup_treeview_columns_shown.append(2)

    Config.config_save_func()


# ----------------------------------- Startup - Set Checkmenuitems (acivates/deactivates checkmenuitem (Enable/Disable checkbox for startup application visibility) on the popup menu when right click operation is performed on startup item row on the treeview) -----------------------------------
def startup_set_checkmenuitem_func():

    startup_application_file_name = StartupGUI.selected_startup_application_file_name
    startup_application_visibility = StartupGUI.selected_startup_application_visibility
    with checkmenuitem5101m.handler_block(checkmenuitem5101m_handler_id):
        if startup_application_visibility == True:
            checkmenuitem5101m.set_active(True)
        if startup_application_visibility == False:
            checkmenuitem5101m.set_active(False)


# ----------------------------------- Startup - Set Menu Labels Function (sets widget sensitivity of "Remove" menuitem and widget sensitivity and labels (system-wide and user-specific .desktop file names) of sub-menu items of "Browse '.desktop' File..." menu item when right click operation is performed on startup item row on the treeview) -----------------------------------
def startup_set_menu_labels_func():

    selected_startup_application_file_name = StartupGUI.selected_startup_application_file_name
    startup_get_system_and_user_autostart_directories_func()
    global desktop_file_system_full_path, desktop_file_user_full_path
    desktop_file_system_full_path = system_autostart_directory + selected_startup_application_file_name
    desktop_file_user_full_path = current_user_autostart_directory + selected_startup_application_file_name
    # Set menu item label (Remove item) as "sensitive" if selected application has only user-pecific desktop file. Otherwise sensitivity is set as "False".
    if os.path.exists(desktop_file_system_full_path) == False and os.path.exists(desktop_file_user_full_path) == True:
        menuitem5103m.set_sensitive(True)
    if os.path.exists(desktop_file_system_full_path) == True or os.path.exists(desktop_file_user_full_path) == False:
        menuitem5103m.set_sensitive(False)
    # Set sub-menu item labels (System-wide values file: and User-specific values file:  items) as "sensitive" (also set label texts as file names) if related desktop files exist. Otherwise sensitivities are set as "False".
    if os.path.exists(desktop_file_system_full_path) == True:
        sub_menuitem5101m.set_sensitive(True)
        sub_menuitem5101m.set_label(_tr("System-wide values file: ") + desktop_file_system_full_path)
    if os.path.exists(desktop_file_system_full_path) == False:
        sub_menuitem5101m.set_sensitive(False)
        sub_menuitem5101m.set_label(_tr("System-wide values file: ") + _tr("None"))
    if os.path.exists(desktop_file_user_full_path) == True:
        sub_menuitem5102m.set_sensitive(True)
        sub_menuitem5102m.set_label(_tr("User-specific values file: ") + desktop_file_user_full_path)
    if os.path.exists(desktop_file_user_full_path) == False:
        sub_menuitem5102m.set_sensitive(False)
        sub_menuitem5102m.set_label(_tr("User-specific values file: ") + _tr("None"))


# ----------------------------------- Startup - Set System And User Autostart Directories Function (gets system and user autostart directories) -----------------------------------
def startup_get_system_and_user_autostart_directories_func():
    # Get current username which will be used for determining current user home directory.
    global current_user_name
    current_user_name = os.environ.get('SUDO_USER')                                       # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                         # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                                # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_startup_applications_visibility_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    # Get human and root user usernames and UIDs. This data will be used if application is run with "pkexec" command.
    usernames_startup_applications_visibility_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                   # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                              # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_startup_applications_visibility_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])

    # Get startup item file directories. System default autostart directory is "system_autostart_directory". Startup items are copied into "current_user_autostart_directory" directory with modified values if user make modifications for the startup item. For the user, these values override system values for the user-modified startup item.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        if line_splitted[0] == current_user_name:
            current_user_homedir = line_splitted[5]

    global current_user_autostart_directory, system_autostart_directory
    current_user_autostart_directory = current_user_homedir + "/.config/autostart/"
    system_autostart_directory = "/etc/xdg/autostart/"
