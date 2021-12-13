#!/usr/bin/env python3

# ----------------------------------- Startup - Startup Right Click Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def startup_menu_right_click_import_func():

    global Gtk, Gdk, Gio, os, subprocess, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, Gio
    import os
    import subprocess
    from threading import Thread


    global MainGUI, Startup
    from . import MainGUI, Startup


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


# ----------------------------------- Startup - Startup Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Startup" tab menu/popover GUI objects and functions/signals) -----------------------------------
def startup_menu_right_click_gui_func():

    # Define builder and get all objects (Startup tab right click menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupMenuRightClick.ui")

    # ********************** Define object names for Startup tab right click menu **********************
    global menu5101m
    global checkmenuitem5101m, menuitem5102m, menuitem5103m, menuitem5105m, menuitem5106m, sub_menuitem5101m, sub_menuitem5102m

    # ********************** Get object names for Startup tab right click menu **********************
    menu5101m = builder.get_object('menu5101m')
    checkmenuitem5101m = builder.get_object('checkmenuitem5101m')
    menuitem5102m = builder.get_object('menuitem5102m')
    menuitem5103m = builder.get_object('menuitem5103m')
    menuitem5105m = builder.get_object('menuitem5105m')
    menuitem5106m = builder.get_object('menuitem5106m')
    sub_menuitem5101m = builder.get_object('sub_menuitem5101m')
    sub_menuitem5102m = builder.get_object('sub_menuitem5102m')
    sub_menuitem5103m = builder.get_object('sub_menuitem5103m')
    sub_menuitem5104m = builder.get_object('sub_menuitem5104m')
    sub_menuitem5105m = builder.get_object('sub_menuitem5105m')

    # ********************** Define object functions for Startup tab right click menu **********************
    def on_checkmenuitem5101m_toggled(widget):                                                # "Enable/Disable" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        treestore5101 = Startup.treestore5101
        startup_get_system_and_user_autostart_directories_func()
        name_value_system = ""
        icon_value_system = ""
        exec_value_system = ""
        hidden_value_system = ""
        not_show_in_value_system = ""
        only_show_in_value_system = ""
        xfce_autostart_override_value_system = ""
        gnome_autostart_enabled_value_system = ""
        if os.path.exists(system_autostart_directory + selected_startup_application_file_name) == True:
            with open(system_autostart_directory + selected_startup_application_file_name) as reader:    # Get content of the ".desktop" file in the system autostart directory
                desktop_file_system_lines = reader.read().strip("").split("\n")
            try:
                desktop_file_system_lines.remove("")                                          # Remove empty lines (if exist)
            except:
                pass
            for line in desktop_file_system_lines:
                if "Name=" in line:                                                           # Value of "Name=" entry is get to be used as application name.
                    name_value_system = line.split("=")[1]
                if "Icon=" in line:                                                           # Application icon name
                    icon_value_system = line.split("=")[1]
                if "Exec=" in line:                                                           # Application executable (command) name
                    exec_value_system = line.split("=")[1]
                if "Hidden=" in line:                                                         # Application "hidden" value. Application is not started on the system start if this value is "true". This value overrides "NotShowIn" and "OnlyShowIn" values.
                    hidden_value_system = line.split("=")[1]
                if "NotShowIn" in line:                                                       # Application "NotShowIn" value. Application is not started on the system start if name of the current desktop session (XFCE, GNOME, etc.) is in this value. Desktop session name may not exist in both "NotShowIn" and "OnlyShowIn" values. Application is not started on the system start in this situation.
                    not_show_in_value_system = line.split("=")[1].strip(";").split(";")
                if "OnlyShowIn" in line:                                                      # Application "OnlyShowIn" value. Application is started on the system start only if name of the current desktop session (XFCE, GNOME, etc.) is in this value. Desktop session name may not exist in both "NotShowIn" and "OnlyShowIn" values. Application is not started on the system start in this situation.
                    only_show_in_value_system = line.split("=")[1].strip(";").split(";")
                if "X-XFCE-Autostart-Override" in line:                                       # Application "X-XFCE-Autostart-Override". If this value is "true", application is started on the system start if current desktop session name is in "NotShowIn" value or not in "OnlyShowIn" value.
                    xfce_autostart_override_value_system = line.split("=")[1]
                if "X-GNOME-Autostart-enabled" in line:                                       # Application "X-GNOME-Autostart-enabled". If this value is "true", application is started on the system start if current desktop session name is in "NotShowIn" value or not in "OnlyShowIn" value.
                    gnome_autostart_enabled_value_system = line.split("=")[1]
        name_value_user = ""
        icon_value_user = ""
        exec_value_user = ""
        hidden_value_user = ""
        not_show_in_value_user = ""
        only_show_in_value_user = ""
        xfce_autostart_override_value_user = ""
        gnome_autostart_enabled_value_user = ""
        if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
            with open(current_user_autostart_directory + selected_startup_application_file_name) as reader:    # Get content of the ".desktop" file in the user autostart directory
                desktop_file_user_lines = reader.read().strip("").split("\n")
            try:
                desktop_file_user_lines.remove("")                                            # Remove empty lines (if exist)
            except:
                pass
            for line in desktop_file_user_lines:
                if "Name=" in line:                                                           # Value of "Name=" entry is get to be used as application name.
                    name_value_user = line.split("=")[1]
                if "Icon=" in line:                                                           # Application icon name
                    icon_value_user = line.split("=")[1]
                if "Exec=" in line:                                                           # Application executable (command) name
                    exec_value_user = line.split("=")[1]
                if "Hidden=" in line:
                    hidden_value_user = line.split("=")[1]
                if "NotShowIn" in line:
                    not_show_in_value_user = line.split("=")[1].strip(";").split(";")
                if "OnlyShowIn" in line:
                    only_show_in_value_user = line.split("=")[1].strip(";").split(";")
                if "X-XFCE-Autostart-Override" in line:
                    xfce_autostart_override_value_user = line.split("=")[1]
                if "X-GNOME-Autostart-enabled" in line:                                       # Application "X-GNOME-Autostart-enabled". If this value is "true", application is started on the system start if current desktop session name is in "NotShowIn" value or not in "OnlyShowIn" value.
                    gnome_autostart_enabled_value_user = line.split("=")[1]
        if checkmenuitem5101m.get_active() == True:
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == False:
                with open(current_user_autostart_directory + selected_startup_application_file_name, 'w') as writer:
                    writer.write("[Desktop Entry]" + "\n")
                    writer.write("Name=" + name_value_system + "\n")
                    writer.write("Icon=" + icon_value_system + "\n")
                    writer.write("Exec=" + exec_value_system + "\n")
                    if len(set(Startup.current_desktop_environment).intersection(not_show_in_value_system)) > 0 or (len(set(Startup.current_desktop_environment).intersection(only_show_in_value_system)) == 0 and only_show_in_value_system != ""): 
                        if len(set(Startup.current_desktop_environment).intersection(["XFCE"])) > 0:
                            writer.write("X-XFCE-Autostart-Override=true" + "\n")
                    if len(set(Startup.current_desktop_environment).intersection(["X-CINNAMON", "CINNAMON", "GNOME", "UBUNTU:GNOME", "GNOME-CLASSIC:GNOME"])) > 0 and gnome_autostart_enabled_value_system == "false":
                        writer.write("X-GNOME-Autostart-enabled=true" + "\n")
                    if len(set(Startup.current_desktop_environment).intersection(not_show_in_value_system)) > 0:
                        for desktop_environment in Startup.current_desktop_environment:
                            if desktop_environment in not_show_in_value_system:
                                not_show_in_value_system.remove(desktop_environment)
                        writer.write("NotShowIn=" + ";".join(not_show_in_value_system) + ";" + "\n")
                    if len(set(Startup.current_desktop_environment).intersection(only_show_in_value_system)) == 0 and only_show_in_value_system != "":
                        only_show_in_value_system = only_show_in_value_system + [Startup.current_desktop_environment[0]]
                        writer.write("OnlyShowIn=" + ";".join(only_show_in_value_system) + ";" + "\n")
                    if hidden_value_system == "true":
                        writer.write("Hidden=false" + "\n")
                    return
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
                if len(set(Startup.current_desktop_environment).intersection(not_show_in_value_system)) > 0 or (len(set(Startup.current_desktop_environment).intersection(only_show_in_value_system)) == 0 and only_show_in_value_system != ""):
                    if xfce_autostart_override_value_user != "":
                        for line in desktop_file_user_lines:                                  # Search for visibility value
                            if "X-XFCE-Autostart-Override" in line:
                                desktop_file_user_lines.remove(line)                          # Remove old value from the list
                                desktop_file_user_lines.append("X-XFCE-Autostart-Override=true")    # Append new value into the list
                if len(set(Startup.current_desktop_environment).intersection(["X-CINNAMON", "CINNAMON", "GNOME", "UBUNTU:GNOME", "GNOME-CLASSIC:GNOME"])) > 0 and (gnome_autostart_enabled_value_system == "false" or gnome_autostart_enabled_value_user != ""):
                    for line in desktop_file_user_lines:                                      # Search for visibility value
                        if "X-GNOME-Autostart-enabled" in line:
                            desktop_file_user_lines.remove(line)                              # Remove old value from the list
                            desktop_file_user_lines.append("X-GNOME-Autostart-enabled=true")    # Append new value into the list
                for line in desktop_file_user_lines:                                          # Search for visibility value
                    if "NotShowIn=" in line:
                        desktop_file_user_lines.remove(line)                                  # Remove old value from the list
                if len(set(Startup.current_desktop_environment).intersection(not_show_in_value_system)) > 0:
                    for desktop_environment in Startup.current_desktop_environment:
                        if desktop_environment in not_show_in_value_system:
                            not_show_in_value_system.remove(desktop_environment)
                    desktop_file_user_lines.append("NotShowIn=" + ";".join(not_show_in_value_system) + ";")    # Append new value into the list
                for line in desktop_file_user_lines:                                          # Search for visibility value
                    if "OnlyShowIn=" in line:
                        desktop_file_user_lines.remove(line)                                  # Remove old value from the list
                if len(set(Startup.current_desktop_environment).intersection(only_show_in_value_system)) == 0 and only_show_in_value_system != "":
                    only_show_in_value_system = only_show_in_value_system + [Startup.current_desktop_environment[0]]
                    desktop_file_user_lines.append("OnlyShowIn=" + ";".join(only_show_in_value_system) + ";")    # Append new value into the list
                for line in desktop_file_user_lines:                                          # Search for visibility value
                    if "Hidden=" in line:
                        desktop_file_user_lines.remove(line)                                  # Remove old value from the list
                if hidden_value_system == "true" or hidden_value_system == "" or hidden_value_user == "true" or hidden_value_user == "":
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
                    writer.write("Name=" + name_value_system + "\n")
                    writer.write("Icon=" + icon_value_system + "\n")
                    writer.write("Exec=" + exec_value_system + "\n")
                    if xfce_autostart_override_value_system == "true":
                        if len(set(Startup.current_desktop_environment).intersection(["XFCE"])) > 0:
                            writer.write("X-XFCE-Autostart-Override=false" + "\n")
                    if hidden_value_system == "false" or hidden_value_system == "":
                        writer.write("Hidden=true" + "\n")
                    return
            if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
                if xfce_autostart_override_value_user != "" and len(set(Startup.current_desktop_environment).intersection(["XFCE"])) > 0:
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
        if 'StartupNewItem' not in globals():                                                 # Check if "StartupNewItem" module is imported. Therefore it is not reimported for every click on "Add" menu item if "StartupNewItem" name is in globals().
            global StartupNewItem
            import StartupNewItem
            StartupNewItem.startup_new_item_import_func()
            StartupNewItem.startup_new_item_gui_func()
        StartupNewItem.window5101w.show()

    def on_menuitem5103m_activate(widget):                                                    # "Delete" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        startup_get_system_and_user_autostart_directories_func()
        if os.path.exists(system_autostart_directory + selected_startup_application_file_name) == True:
            sub_menuitem5103m.set_sensitive(True)
        if os.path.exists(system_autostart_directory + selected_startup_application_file_name) == False:
            sub_menuitem5103m.set_sensitive(False)
            sub_menuitem5105m.set_sensitive(False)
        if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
            sub_menuitem5104m.set_sensitive(True)
        if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == False:
            sub_menuitem5104m.set_sensitive(False)
            sub_menuitem5105m.set_sensitive(False)
        if os.path.exists(system_autostart_directory + selected_startup_application_file_name) == True and os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
            sub_menuitem5105m.set_sensitive(True)

    def on_sub_menuitem5103m_activate(widget):                                                # "Delete System-Wide Values File" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name
        message_text = _tr("Do you want to delete system-wide values file of the following startup item?")
        startup_delete_startup_item_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_file_name)
        if warning_dialog5102_response == Gtk.ResponseType.YES:
            try:
                (subprocess.check_output(["pkexec", "rm", desktop_file_system_full_path], stderr=subprocess.STDOUT, shell=False)).decode()
                os.remove(desktop_file_system_full_path)
            except:
                pass
        if warning_dialog5102_response == Gtk.ResponseType.NO:
            return                                                                            # Do nothing (close the dialog) if "No" is clicked.

    def on_sub_menuitem5104m_activate(widget):                                                # "Delete User-Specific Values File" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name
        message_text = _tr("Do you want to delete user-specific values file of the following startup item?")
        startup_delete_startup_item_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_file_name)
        if warning_dialog5102_response == Gtk.ResponseType.YES:
            try:
                (subprocess.check_output(["rm", desktop_file_user_full_path], stderr=subprocess.STDOUT, shell=False)).decode()
            except:
                pass
        if warning_dialog5102_response == Gtk.ResponseType.NO:
            return                                                                            # Do nothing (close the dialog) if "No" is clicked.

    def on_sub_menuitem5105m_activate(widget):                                                # "Delete Both Files" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name
        message_text = _tr("Do you want to delete system-wide and user-specific value files of the following startup item?")
        startup_delete_startup_item_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_file_name)
        if warning_dialog5102_response == Gtk.ResponseType.YES:
            try:
                (subprocess.check_output(["pkexec", "rm", desktop_file_system_full_path], stderr=subprocess.STDOUT, shell=False)).decode()
            except:
                pass
            try:
                (subprocess.check_output(["rm", desktop_file_user_full_path], stderr=subprocess.STDOUT, shell=False)).decode()
            except:
                pass
        if warning_dialog5102_response == Gtk.ResponseType.NO:
            return   

    def on_menuitem5106m_activate(widget):                                                    # "Run now" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name
        startup_get_system_and_user_autostart_directories_func()
        global selected_startup_application_exec_value
        selected_startup_application_exec_value = ""                                          # Initial value of "selected_startup_application_exec_value". This value will be used if it can not be get.
        if os.path.exists(system_autostart_directory + selected_startup_application_file_name) == True:
            with open(system_autostart_directory + selected_startup_application_file_name) as reader:    # Get content of the ".desktop" file in the system autostart directory
                desktop_file_system_lines = reader.read().strip("").split("\n")
            for line in desktop_file_system_lines:
                if "Exec=" in line:                                                           # Application "hidden" value. Application is not started on the system start if this value is "true". This value overrides "NotShowIn" and "OnlyShowIn" values.
                    selected_startup_application_exec_value = line.split("=")[1]
        if os.path.exists(current_user_autostart_directory + selected_startup_application_file_name) == True:
            with open(current_user_autostart_directory + selected_startup_application_file_name) as reader:    # Get content of the ".desktop" file in the user autostart directory
                desktop_file_user_lines = reader.read().strip("").split("\n")
            for line in desktop_file_user_lines:
                if "Exec=" in line:
                    selected_startup_application_exec_value = line.split("=")[1]
        startup_run_startup_item_warning_dialog(selected_startup_application_name, selected_startup_application_exec_value)
        if warning_dialog5101_response == Gtk.ResponseType.YES:
            try:
                subprocess.Popen([selected_startup_application_exec_value], shell=False)      # Run the command of the startup item. If "Yes" is clicked. "shell=False" is used in order to prevent "shell injection" which may cause security problems.
            except FileNotFoundError:
                startup_run_now_error_dialog(selected_startup_application_file_name, selected_startup_application_exec_value)
        if warning_dialog5101_response == Gtk.ResponseType.NO:
            return                                                                            # Do nothing (close the dialog) if "No" is clicked.

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
    menuitem5106m.connect("activate", on_menuitem5106m_activate)
    sub_menuitem5101m.connect("activate", on_sub_menuitem5101m_activate)
    sub_menuitem5102m.connect("activate", on_sub_menuitem5102m_activate)
    sub_menuitem5103m.connect("activate", on_sub_menuitem5103m_activate)
    sub_menuitem5104m.connect("activate", on_sub_menuitem5104m_activate)
    sub_menuitem5105m.connect("activate", on_sub_menuitem5105m_activate)


# ----------------------------------- Startup - Set System And User Autostart Directories Function (gets system and user autostart directories) -----------------------------------
def startup_get_system_and_user_autostart_directories_func():
    # Get human and root user usernames and UIDs. This data will be used if application is run with "pkexec" command.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                       # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])

    # Get current username which will be used for determining current user home directory.
    global current_user_name
    current_user_name = os.environ.get('SUDO_USER')                                           # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                             # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                                    # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    # Get startup item file directories. System default autostart directory is "system_autostart_directory". Startup items are copied into "current_user_autostart_directory" directory with modified values if user make modifications for the startup item. For the user, these values override system values for the user-modified startup item.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        if line_splitted[0] == current_user_name:
            current_user_homedir = line_splitted[5]

    global current_user_autostart_directory, system_autostart_directory
    current_user_autostart_directory = current_user_homedir + "/.config/autostart/"
    system_autostart_directory = "/etc/xdg/autostart/"


# ----------------------------------- Startup - Set Checkmenuitems (acivates/deactivates checkmenuitem (Enable/Disable checkbox for startup application visibility) on the popup menu when right click operation is performed on startup item row on the treeview) -----------------------------------
def startup_set_checkmenuitem_func():

    startup_application_file_name = Startup.selected_startup_application_file_name
    startup_application_visibility = Startup.selected_startup_application_visibility
    with checkmenuitem5101m.handler_block(checkmenuitem5101m_handler_id):
        if startup_application_visibility == True:
            checkmenuitem5101m.set_active(True)
        if startup_application_visibility == False:
            checkmenuitem5101m.set_active(False)


# ----------------------------------- Startup - Set Menu Labels Function (sets widget sensitivity of "Remove" menuitem and widget sensitivity and labels (system-wide and user-specific .desktop file names) of sub-menu items of "Browse '.desktop' File..." menu item when right click operation is performed on startup item row on the treeview) -----------------------------------
def startup_set_menu_labels_func():

    selected_startup_application_file_name = Startup.selected_startup_application_file_name
    startup_get_system_and_user_autostart_directories_func()
    global desktop_file_system_full_path, desktop_file_user_full_path
    desktop_file_system_full_path = system_autostart_directory + selected_startup_application_file_name
    desktop_file_user_full_path = current_user_autostart_directory + selected_startup_application_file_name

    # ------------------------- Set menu labels for "Browse '.desktop' File..." sub-menu items ----------------------------------------
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


# ----------------------------------- Startup - Startup Run Startup Item Warning Dialog Function (shows a warning dialog when a startup item is tried to be run) -----------------------------------
def startup_run_startup_item_warning_dialog(selected_startup_application_name, selected_startup_application_exec_value):

    warning_dialog5101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Run Startup Item Now?"), )
    warning_dialog5101.format_secondary_text(_tr("Do you want to run the following startup item?") +
                                             "\n\n    " + _tr("Startup Item:") + " " + selected_startup_application_name +
                                             "\n    " + _tr("Command:") + " " + selected_startup_application_exec_value)
    global warning_dialog5101_response
    warning_dialog5101_response = warning_dialog5101.run()
    warning_dialog5101.destroy()


# ----------------------------------- Startup - Startup Delete Startup Item Warning Dialog Function (shows a warning dialog when a startup item is tried to be deleted) -----------------------------------
def startup_delete_startup_item_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_exec_value):

    warning_dialog5102 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Delete Startup Item?"), )
    warning_dialog5102.format_secondary_text(message_text +
                                             "\n\n    " + _tr("Startup Item:") + " " + selected_startup_application_name +
                                             "\n    " + _tr("Command:") + " " + selected_startup_application_exec_value)
    global warning_dialog5102_response
    warning_dialog5102_response = warning_dialog5102.run()
    warning_dialog5102.destroy()


# ----------------------------------- Startup - Startup Reset To System Default Warning Dialog Function (shows a warning dialog when a startup item is tried to be reset to system default which means user specific desktop file of the startup application will be deleted (system-wide values file will be untouched)) -----------------------------------
def startup_run_now_error_dialog(selected_startup_application_file_name, selected_startup_application_exec_value):

    error_dialog5101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Error While Running Startup Item Command"), )
    error_dialog5101.format_secondary_text(_tr("Error is encountered while running the following command:") +
                                           "\n\n    " + _tr("'.desktop' File Name:") + " " + selected_startup_application_file_name +
                                           "\n    " + _tr("Startup Item Command:") + " " + selected_startup_application_exec_value)
    error_dialog5101.run()
    error_dialog5101.destroy()
