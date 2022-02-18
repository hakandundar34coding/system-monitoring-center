#!/usr/bin/env python3

# ----------------------------------- Startup - Import Function -----------------------------------
def startup_import_func():

    global Gtk, GLib, os

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gtk, GLib
    import os


    global Config
    import Config


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Startup - Startup GUI Function -----------------------------------
def startup_gui_func():

    global grid5101, treeview5101, searchentry5101, button5101
    global radiobutton5101, radiobutton5102, radiobutton5103


    # Startup tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupTab.ui")

    # Startup tab GUI objects - get
    grid5101 = builder.get_object('grid5101')
    treeview5101 = builder.get_object('treeview5101')
    searchentry5101 = builder.get_object('searchentry5101')
    button5101 = builder.get_object('button5101')
    radiobutton5101 = builder.get_object('radiobutton5101')
    radiobutton5102 = builder.get_object('radiobutton5102')
    radiobutton5103 = builder.get_object('radiobutton5103')


    # Startup tab GUI functions
    def on_treeview5101_button_press_event(widget, event):                                    # Mouse button press event (on the treeview)
        # Get right/double clicked row data
        try:                                                                                  # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
            path, _, _, _ = treeview5101.get_path_at_pos(int(event.x), int(event.y))
        except TypeError:
            return
        model = treeview5101.get_model()
        treeiter = model.get_iter(path)
        # Get right/double clicked startup item file name, visibility and name
        if treeiter == None:
            return
        global selected_startup_application_file_name, selected_startup_application_visibility, selected_startup_application_name
        try:
            selected_startup_application_file_name = all_autostart_applications_list[startup_data_rows.index(model[treeiter][:])]
            selected_startup_application_visibility = startup_applications_visibility_list[startup_data_rows.index(model[treeiter][:])]
            selected_startup_application_name = model[treeiter][3]
        except ValueError:
            return
        # Open right click menu if right clicked on a row
        if event.button == 3:
            if 'StartupMenuRightClick' not in globals():
                global StartupMenuRightClick
                import StartupMenuRightClick
                StartupMenuRightClick.startup_menu_right_click_import_func()
                StartupMenuRightClick.startup_menu_right_click_gui_func()
            StartupMenuRightClick.menu5101m.popup(None, None, None, None, event.button, event.time)
            StartupMenuRightClick.startup_set_checkmenuitem_func()
            StartupMenuRightClick.startup_set_menu_labels_func()

    def on_treeview5101_button_release_event(widget, event):                                  # Mouse button press event (on the treeview)
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            startup_treeview_column_order_width_row_sorting_func()

    def on_searchentry5101_changed(widget):
        radiobutton5101.set_active(True)
        startup_treeview_filter_search_func()

    def on_button5101_clicked(widget):                                                        # "Startup Tab Customizations" button
        if 'StartupMenuCustomizations' not in globals():
            global StartupMenuCustomizations
            import StartupMenuCustomizations
            StartupMenuCustomizations.startup_menu_customizations_import_func()
            StartupMenuCustomizations.startup_menu_customizations_gui_func()
        StartupMenuCustomizations.popover5101p.popup()

    def on_radiobutton5101_toggled(widget):                                                   # "Show all startup items" radiobutton
        if radiobutton5101.get_active() == True:
            searchentry5101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            startup_treeview_filter_show_all_func()

    def on_radiobutton5102_toggled(widget):                                                   # "Show all enabled (visible) startup items" radiobutton
        if radiobutton5102.get_active() == True:
            searchentry5101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            startup_treeview_filter_show_all_func()
            startup_treeview_filter_startup_visible_only()

    def on_radiobutton5103_toggled(widget):                                                   # "Show all disabled (hidden) startup items" radiobutton
        if radiobutton5103.get_active() == True:
            searchentry5101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            startup_treeview_filter_show_all_func()
            startup_treeview_filter_startup_hidden_only()


    # Startup tab GUI functions - connect
    treeview5101.connect("button-press-event", on_treeview5101_button_press_event)
    treeview5101.connect("button-release-event", on_treeview5101_button_release_event)
    searchentry5101.connect("changed", on_searchentry5101_changed)
    button5101.connect("clicked", on_button5101_clicked)
    radiobutton5101.connect("toggled", on_radiobutton5101_toggled)
    radiobutton5102.connect("toggled", on_radiobutton5102_toggled)
    radiobutton5103.connect("toggled", on_radiobutton5103_toggled)


    # Startup Tab - Treeview Properties
    treeview5101.set_activate_on_single_click(True)
    treeview5101.set_fixed_height_mode(True)
    treeview5101.set_headers_clickable(True)
    treeview5101.set_show_expanders(False)
    treeview5101.set_enable_search(True)
    treeview5101.set_search_column(3)
    treeview5101.set_tooltip_column(3)


# ----------------------------------- Startup - Initial Function -----------------------------------
def startup_initial_func():

    global startup_data_list
    startup_data_list = [
                        [0, _tr('Name'), 4, 3, 4, [bool, bool, str, str], ['internal_column', 'CellRendererToggle', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'active', 'icon_name', 'text'], [0, 1, 2, 3], ['no_cell_alignment', 0.0, 0.0, 0.0], ['no_set_expand', False, False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function', 'no_cell_function']],
                        [1, _tr('Comment'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [2, _tr('Command'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                        ]

    global startup_data_rows_prev, all_autostart_applications_list_prev, piter_list, startup_treeview_columns_shown_prev, startup_data_row_sorting_column_prev, startup_data_row_sorting_order_prev, startup_data_column_order_prev, startup_data_column_widths_prev
    startup_data_rows_prev = []
    all_autostart_applications_list_prev = []
    piter_list = []
    startup_treeview_columns_shown_prev = []
    startup_data_row_sorting_column_prev = ""
    startup_data_row_sorting_order_prev = ""
    startup_data_column_order_prev = []
    startup_data_column_widths_prev = []

    global startup_image_no_icon
    startup_image_no_icon = "system-monitoring-center-application-startup-symbolic"           # Will be used as image of the startup items that has no icons.

    # Get current desktop environment
    global supported_desktop_environments_list
    supported_desktop_environments_list = ["XFCE", "GNOME", "X-CINNAMON", "CINNAMON", "MATE", "KDE", "UBUNTU:GNOME", "GNOME-CLASSIC:GNOME", "zorin:GNOME", "LXQT", "LXDE"]    # Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
    global current_desktop_environment
    current_desktop_environment = [os.environ.get('XDG_CURRENT_DESKTOP')]
    if current_desktop_environment != [None]:
        current_desktop_environment[0] = current_desktop_environment[0].strip().upper()       # "current_desktop_environment" is defined as list because some dektop environmens takes into account more than one name.
    if current_desktop_environment == ["X-CINNAMON"] or current_desktop_environment == ["CINNAMON"]:
        current_desktop_environment = ["X-CINNAMON", "CINNAMON", "GNOME"]                     # These names are taked into account by Cinnamon desktop environment.
    if current_desktop_environment == ["UBUNTU:GNOME"]:
        current_desktop_environment = ["GNOME", "UBUNTU:GNOME"]
    if current_desktop_environment == ["GNOME-CLASSIC:GNOME"]:
        current_desktop_environment = ["GNOME", "GNOME-CLASSIC:GNOME"]
    if current_desktop_environment == ["zorin:GNOME"]:
        current_desktop_environment = ["GNOME", "zorin:GNOME"]
    if current_desktop_environment == [None]:
        # Get human and root user usernames and UIDs only one time at the per loop in order to avoid running it per startup item loop (it is different than main loop = startup_loop_func) which increases CPU consumption. This data will be used if application is run with "pkexec" command.
        usernames_username_list = []
        usernames_uid_list = []
        with open("/etc/passwd") as reader:                                                   # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
            etc_passwd_lines = reader.read().strip().split("\n")                              # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
        for line in etc_passwd_lines:
            line_splitted = line.split(":", 3)
            usernames_username_list.append(line_splitted[0])
            usernames_uid_list.append(line_splitted[2])

        # Get current username which will be used for determining current user home directory.
        global current_user_name
        current_user_name = os.environ.get('SUDO_USER')                                       # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
        if current_user_name is None:                                                         # Get username in the following way if current application has not been run by root privileges.
            current_user_name = os.environ.get('USER')
        pkexec_uid = os.environ.get('PKEXEC_UID')
        if current_user_name == "root" and pkexec_uid != None:                                # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
            current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

        # Get "current_desktop_environment"
        current_desktop_session = "-"                                                         # Set an initial string in order to avoid errors in case of undetected current desktop session.
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]      # Get process PID list.
        for pid in pid_list:
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/comm") as reader:
                    process_name = reader.read().strip()
                with open("/proc/" + pid + "/status") as reader:                              # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                    proc_pid_status_lines = reader.read().split("\n")
            except FileNotFoundError:
                continue
            for line in proc_pid_status_lines:
                if "Uid:\t" in line:
                    real_user_id = line.split(":")[1].split()[0].strip()                      # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
            if process_username == current_user_name:
                if process_name == "xfce4-session":
                    current_desktop_session = ["XFCE"]
                if process_name.startswith("gnome-session-b"):
                    current_desktop_session = ["GNOME", "UBUNTU:GNOME", "GNOME-CLASSIC:GNOME", "zorin:GNOME"]
                if process_name == "cinnamon-session":
                    current_desktop_session = ["X-CINNAMON", "CINNAMON", "GNOME"]             # Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
                if process_name == "mate-session":
                    current_desktop_session = ["MATE"]
                if process_name == "plasmashell":
                    current_desktop_session = ["KDE"]
                if process_name == "lxqt-session":
                    current_desktop_session = ["LXQT"]
                if process_name == "lxsession":
                    current_desktop_session = ["LXDE"]
        current_desktop_environment = current_desktop_session

    global filter_column
    filter_column = startup_data_list[0][2] - 1                                                # Search filter is "Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.


# ----------------------------------- Startup - Get Startup Data Function -----------------------------------
def startup_loop_func():

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview5101

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global startup_treeview_columns_shown
    global startup_treeview_columns_shown_prev, startup_data_row_sorting_column_prev, startup_data_row_sorting_order_prev, startup_data_column_order_prev, startup_data_column_widths_prev
    startup_treeview_columns_shown = Config.startup_treeview_columns_shown
    startup_data_row_sorting_column = Config.startup_data_row_sorting_column
    startup_data_row_sorting_order = Config.startup_data_row_sorting_order
    startup_data_column_order = Config.startup_data_column_order
    startup_data_column_widths = Config.startup_data_column_widths

    # Get human and root user usernames and UIDs only one time at the per loop in order to avoid running it per startup item loop (it is different than main loop = startup_loop_func) which increases CPU consumption. This data will be used if application is run with "pkexec" command.
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

    # Define global variables and empty lists for the current loop
    global startup_data_rows, startup_data_rows_prev, all_autostart_applications_list, all_autostart_applications_list_prev, startup_applications_visibility_list
    startup_data_rows = []
    startup_applications_visibility_list = []

    # Get startup item file directories. System default autostart directory is "system_autostart_directory". Startup items are copied into "current_user_autostart_directory" directory with modified values if user make modifications for the startup item. For the user, these values override system values for the user-modified startup item.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        if line_splitted[0] == current_user_name:
            current_user_homedir = line_splitted[5]
    current_user_autostart_directory = current_user_homedir + "/.config/autostart/"
    system_autostart_directory = "/etc/xdg/autostart/"

    # Define application "name" and "comment" strings for searching in ".desktop" files in different locale formats. ".desktop" files for some applications do not contain localized name and comment information. Some of these data are avaible for only language (such as "[tr]". Some of them avaible for language and country (such as "[tr_TR]"). Following definitions are made in order to handle these data differences.
    system_locale = os.environ.get("LANG")
    system_language = system_locale.split("_")[0]
    name_language_country = "Name[" + system_locale + "]="
    name_language = "Name[" + system_language + "]="
    comment_language_country = "Comment[" + system_locale + "]="
    comment_language = "Comment[" + system_language + "]="

    # In order to avoid errors, stop the loop function if current desktop session is not one of these in the "supported_desktop_environments_list" list. Currently other dektop environments are not tested for "Startup" tab. Dekstop environments may have specific lines in the ".desktop" files.
    if set(current_desktop_environment).intersection(supported_desktop_environments_list) == 0:
        searchentry5101.set_placeholder_text(_tr("This desktop environment is not supported") + ": " + current_desktop_environment[0])
        return

    # There are user startup applications and system wide startup applications in linux. They are in different directories. Modifications in directory of system wide startup applications require root access.
    # To be able to make system wide startup application preferences user specific, updates (enabling/disabling startup preferences) on the .desktop files are saved in user startup application directory.
    # If same file is in both directories, .desktop file settings in user startup application directory override system wide startup application settings. For more information about this multiple instance files behavior, see: https://specifications.freedesktop.org/autostart-spec/autostart-spec-latest.html
    system_autostart_directory_applications = [filename for filename in os.listdir(system_autostart_directory) if os.path.isfile(system_autostart_directory + filename)]
    for filename in system_autostart_directory_applications[:]:                               # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
        if filename.endswith(".desktop") == False:
            system_autostart_directory_applications.remove(filename)
    current_user_autostart_directory_applications = []                                        # This list is defined in order to prevent errors while performing subtraction operations if current_user_autostart_directory does not exist.
    if os.path.isdir(current_user_autostart_directory) == True:                               # Check if current user autostart directory exists. By default, this directory does not exists if no modifications are made for startup items since system installation.
        current_user_autostart_directory_applications = [filename for filename in os.listdir(current_user_autostart_directory) if os.path.isfile(current_user_autostart_directory + filename)]
    for filename in current_user_autostart_directory_applications[:]:                         # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
        if filename.endswith(".desktop") == False:
            current_user_autostart_directory_applications.remove(filename)
    system_autostart_applications = sorted(set(system_autostart_directory_applications) - set(current_user_autostart_directory_applications))          # Autostart application files (only unmodified system autostart applications - there is no another copy of these files in the user autostart directory)
    current_user_autostart_applications = sorted(set(current_user_autostart_directory_applications) - set(system_autostart_directory_applications))    # Autostart application files (only user autostart applications - there is no another copy of these files in the system autostart directory)
    modified_system_applications = sorted(set(system_autostart_directory_applications).intersection(current_user_autostart_directory_applications))    # Autostart application files (modified autostart applications - there is one copy of these application files in both system and user autostart directories)
    all_autostart_applications = sorted(set(system_autostart_directory_applications + current_user_autostart_directory_applications))                  # Autostart application files (all files including the ones in system and user autostart directories)

    # Get autostart application data
    for desktop_file in all_autostart_applications:
        # Read files of the autostart application
        if desktop_file in system_autostart_directory_applications:                           # Read autostart file content if it is in the system autostart directory
            with open(system_autostart_directory + desktop_file) as input_file:
                file_data_system_lines = input_file.read().strip().split("\n")
        if desktop_file in current_user_autostart_directory_applications:                     # Read autostart file content if it is in the user autostart directory
            with open(current_user_autostart_directory + desktop_file) as input_file:
                file_data_user_lines = input_file.read().strip().split("\n")

        # Perform loop operation per autostart application file in the system autostart directory and get information for appending into a list (startup_data_row).
        if desktop_file in system_autostart_directory_applications:
            # Data in the system autostart directory is read for the application. These are system-wide values. Data in the user autostart directory is read if same file name exists in this directory. Values in this file overwrite the values from system autostart directory. These values are valid only for the current user. Also values from user autostart directory are read if file name exits only in the user autostart directory. This means, this application is first appended by this user.
            name_value_system = ""                                                            # Initial value of "name_value_system" variable. This value will be used if "name_value_system" could not be detected. For more information about these files, see: https://specifications.freedesktop.org/desktop-entry-spec/latest/ar01s06.html
            name_language_value_system = ""
            name_language_country_value_system = ""
            comment_value_system = ""
            comment_language_value_system = ""
            comment_language_country_value_system = ""
            icon_value_system = startup_image_no_icon                                         # Will be used as image of the startup items that has no icons.
            exec_value_system = ""
            hidden_value_system = ""
            not_show_in_value_system = ""
            only_show_in_value_system = ""
            xfce_autostart_override_value_system = ""
            gnome_autostart_enabled_value_system = ""
            for line in file_data_system_lines:
                if "Name=" in line:                                                           # Value of "Name=" entry is get to be used as application name.
                    name_value_system = line.split("=")[1]
                if name_language in line:                                                     # Value of "Name[language]=" entry is get to be used as application name (if it exists, otherwise English application name is used).
                    name_language_value_system = line.split("=")[1]
                if name_language_country in line:                                             # Value of "Name[language_country]=" entry is get to be used as application name (if it exists, otherwise value of "Name[language]=" entry or English application name is used respectively).
                    name_language_country_value_system = line.split("=")[1]
                if "Comment=" in line:                                                        # Application "comment (explanation)" values are read in the same manner (name values).
                    comment_value_system = line.split("=")[1]
                if comment_language in line:
                    comment_language_value_system = line.split("=")[1]
                if comment_language_country in line:
                    comment_language_country_value_system = line.split("=")[1]
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
        # Perform loop operation per autostart application file in the user autostart directory and get information for appending into a list (startup_data_row).
        if desktop_file in current_user_autostart_directory_applications:
            name_value_user = ""                                                              # Initial value of "name_value_system" variable. This value will be used if "name_value_system" could not be detected.
            name_language_value_user = ""
            name_language_country_value_user = ""
            comment_value_user = ""
            comment_language_value_user = ""
            comment_language_country_value_user = ""
            icon_value_user = startup_image_no_icon
            exec_value_user = ""
            hidden_value_user = ""
            not_show_in_value_user = ""
            only_show_in_value_user = ""
            xfce_autostart_override_value_user = ""
            gnome_autostart_enabled_value_user = ""
            for line in file_data_user_lines:
                if "Name=" in line:
                    name_value_user = line.split("=")[1]
                if name_language in line:
                    name_language_value_user = line.split("=")[1]
                if name_language_country in line:
                    name_language_country_value_user = line.split("=")[1]
                if "Comment=" in line:
                    comment_value_user = line.split("=")[1]
                if comment_language in line:
                    comment_language_value_user = line.split("=")[1]
                if comment_language_country in line:
                    comment_language_country_value_user = line.split("=")[1]
                if "Icon=" in line:
                    icon_value_user = line.split("=")[1]
                if "Exec=" in line:
                    exec_value_user = line.split("=")[1]
                if "Hidden=" in line:
                    hidden_value_user = line.split("=")[1]
                if "NotShowIn" in line:
                    not_show_in_value_user = line.split("=")[1].strip(";").split(";")
                if "OnlyShowIn" in line:
                    only_show_in_value_user = line.split("=")[1].strip(";").split(";")
                if "X-XFCE-Autostart-Override" in line:
                    xfce_autostart_override_value_user = line.split("=")[1]
                if "X-GNOME-Autostart-enabled" in line:
                    gnome_autostart_enabled_value_user = line.split("=")[1]
        # Process and get data of the startup application if it is in the system autostart directory. This data will be overwritten if same application name exists in the user autostart directory.
        if desktop_file in system_autostart_directory_applications:
            # Get startup application visibility (which is different from application data treeview row visibility data)
            startup_application_visibility = True
            if len(set(current_desktop_environment).intersection(only_show_in_value_system)) == 0 and only_show_in_value_system != "":
                startup_application_visibility = False
            if len(set(current_desktop_environment).intersection(not_show_in_value_system)) > 0 and len(set(current_desktop_environment).intersection(["X_CINNAMON", "CINNAMON"])) == 0:    # "Cinnamon" desktop environment takes into account "GNOME" desktop environment name but this is not valid for "NotShowIn" line in the .desktop file.
                startup_application_visibility = False
            if xfce_autostart_override_value_system == "true" and len(set(current_desktop_environment).intersection(["XFCE"])) > 0:
                startup_application_visibility = True
            if gnome_autostart_enabled_value_system == "false" and len(set(current_desktop_environment).intersection(["X-CINNAMON", "CINNAMON", "GNOME", "UBUNTU:GNOME", "zorin:GNOME"])) > 0:
                startup_application_visibility = False
            if hidden_value_system == "true":
                startup_application_visibility = False
            # Get application icon
            startup_application_icon = icon_value_system
            # Get startup application name
            startup_application_name = name_language_country_value_system
            if name_language_country_value_system == "":
                startup_application_name = name_language_value_system
            if name_language_value_system == "":
                startup_application_name = name_value_system
            # Get startup application comment
            startup_application_comment = comment_language_country_value_system
            if comment_language_country_value_system == "":
                startup_application_comment = comment_language_value_system
            if comment_language_value_system == "":
                startup_application_comment = comment_value_system
            # Get startup application exec
            startup_application_exec = exec_value_system
        # Process and get data of the startup application if it is in the user autostart directory. This data will overwrite if same application name exists in the system autostart directory.
        if desktop_file in current_user_autostart_applications:
            # Get startup application visibility (which is different from application data treeview row visibility data)
            startup_application_visibility = True
            if len(set(current_desktop_environment).intersection(only_show_in_value_user)) == 0 and only_show_in_value_user != "":
                startup_application_visibility = False
            if len(set(current_desktop_environment).intersection(not_show_in_value_user)) > 0 and len(set(current_desktop_environment).intersection(["X_CINNAMON", "CINNAMON"])) == 0:    # "Cinnamon" desktop environment takes into account "GNOME" desktop environment name but this is not valid for "NotShowIn" line in the .desktop file.
                startup_application_visibility = False
            if xfce_autostart_override_value_user == "true" and len(set(current_desktop_environment).intersection(["XFCE"])) > 0:
                startup_application_visibility = True
            if gnome_autostart_enabled_value_user == "false" and len(set(current_desktop_environment).intersection(["X-CINNAMON", "CINNAMON", "GNOME", "UBUNTU:GNOME", "zorin:GNOME"])) > 0:
                startup_application_visibility = False
            if hidden_value_user == "true":
                startup_application_visibility = False
            # Get application icon
            startup_application_icon = icon_value_user
            # Get startup application name
            startup_application_name = name_language_country_value_user
            if name_language_country_value_user == "":
                startup_application_name = name_language_value_user
            if name_language_value_user == "":
                startup_application_name = name_value_user
            # Get startup application comment
            startup_application_comment = comment_language_country_value_user
            if comment_language_country_value_user == "":
                startup_application_comment = comment_language_value_user
            if comment_language_value_user == "":
                startup_application_comment = comment_value_user
            # Get startup application exec
            startup_application_exec = exec_value_user
        # Overwrite application data which is get from system autostart directory if same application name exists in both system and user autostart directories. New values are get from user autostart directory.
        if desktop_file in modified_system_applications:
            # Get startup application visibility (which is different from application data treeview row visibility data)
            name_value_modified = name_value_system                                           # Initial value of "name_value_system" variable. This value will be used if "name_value_system" could not be detected.
            name_language_value_modified = name_language_value_system
            name_language_country_value_modified = name_language_country_value_system
            comment_value_modified = comment_value_system
            comment_language_value_modified = comment_language_value_system
            comment_language_country_value_modified = comment_language_country_value_system
            icon_value_modified = icon_value_system
            exec_value_modified = exec_value_system
            hidden_value_modified = hidden_value_system
            not_show_in_value_modified = not_show_in_value_system
            only_show_in_value_modified = only_show_in_value_system
            xfce_autostart_override_value_modified = xfce_autostart_override_value_system
            gnome_autostart_enabled_value_modified = gnome_autostart_enabled_value_system
            if name_value_user != "":
                name_value_modified = name_value_user
            if name_language_value_user != "":
                name_language_value_modified = name_language_value_user
            if name_language_country_value_user != "":
                name_language_country_value_modified = name_language_country_value_user
            if comment_value_user != "":
                comment_value_modified = comment_value_user
            if comment_language_value_user != "":
                comment_language_value_modified = comment_language_value_user
            if comment_language_country_value_user != "":
                comment_language_country_value_modified = comment_language_country_value_user
            if icon_value_user != "" and icon_value_user != startup_image_no_icon:
                icon_value_modified = icon_value_user
            if exec_value_user != "":
                exec_value_modified = exec_value_user
            if hidden_value_user != "":
                hidden_value_modified = hidden_value_user
            if not_show_in_value_user != "":
                not_show_in_value_modified = not_show_in_value_user
            if only_show_in_value_user != "":
                only_show_in_value_modified = only_show_in_value_user
            if xfce_autostart_override_value_user != "":
                xfce_autostart_override_value_modified = xfce_autostart_override_value_user
            if gnome_autostart_enabled_value_user != "":
                gnome_autostart_enabled_value_modified = gnome_autostart_enabled_value_user
            # Get startup application visibility
            startup_application_visibility = True
            if len(set(current_desktop_environment).intersection(only_show_in_value_modified)) == 0 and only_show_in_value_modified != "":
                startup_application_visibility = False
            if len(set(current_desktop_environment).intersection(not_show_in_value_modified)) > 0 and len(set(current_desktop_environment).intersection(["X_CINNAMON", "CINNAMON"])) == 0:    # "Cinnamon" desktop environment takes into account "GNOME" desktop environment name but this is not valid for "NotShowIn" line in the .desktop file.
                startup_application_visibility = False
            if xfce_autostart_override_value_modified == "true" and len(set(current_desktop_environment).intersection(["XFCE"])) > 0:
                startup_application_visibility = True
            if gnome_autostart_enabled_value_modified == "false" and len(set(current_desktop_environment).intersection(["X-CINNAMON", "CINNAMON", "GNOME", "UBUNTU:GNOME", "zorin:GNOME"])) > 0:
                startup_application_visibility = False
            if hidden_value_modified == "true":
                startup_application_visibility = False
            # Get application icon
            startup_application_icon = icon_value_modified
            # Get startup application name
            startup_application_name = name_language_country_value_modified
            if name_language_country_value_modified == "":
                startup_application_name = name_language_value_modified
            if name_language_value_modified == "":
                startup_application_name = name_value_modified
            # Get startup application comment
            startup_application_comment = comment_language_country_value_modified
            if comment_language_country_value_modified == "":
                startup_application_comment = comment_language_value_modified
            if comment_language_value_modified == "":
                startup_application_comment = comment_value_modified
            # Get startup application exec
            startup_application_exec = exec_value_modified
        startup_applications_visibility_list.append(startup_application_visibility)

        # Append autostart application visibility data (which is different from row visibility data), application icon and application name
        startup_data_row = [True, startup_application_visibility, startup_application_icon, startup_application_name]    # Startup application data treeview row visibility data (True/False) is always appended into the list. True is an initial value and it is modified later.
        # Append autostart application comment
        if 1 in startup_treeview_columns_shown:
            startup_data_row.append(startup_application_comment)
        # Append autostart application executable (commandline) data
        if 2 in startup_treeview_columns_shown:
            startup_data_row.append(startup_application_exec)
        # Append all data of the startup applications into a list which will be appended into a treestore for showing the data on a treeview.
        startup_data_rows.append(startup_data_row)

    # Add/Remove treeview columns appropriate for user preferences
    treeview5101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if startup_treeview_columns_shown != startup_treeview_columns_shown_prev:                 # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview5101.get_columns():                                             # Remove all columns in the treeview.
            treeview5101.remove_column(column)
        for i, column in enumerate(startup_treeview_columns_shown):
            if startup_data_list[column][0] in startup_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + startup_data_list[column][2]
            startup_treeview_column = Gtk.TreeViewColumn(startup_data_list[column][1])        # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(startup_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                if cell_renderer_type == "CellRendererToggle":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererToggle()
                cell_renderer.set_alignment(startup_data_list[column][9][i], 0.5)             # Vertical alignment is set 0.5 in order to leave it as unchanged.
                startup_treeview_column.pack_start(cell_renderer, startup_data_list[column][10][i])    # Set if column will allocate unused space
                startup_treeview_column.add_attribute(cell_renderer, startup_data_list[column][7][i], cumulative_internal_data_id)
                if startup_data_list[column][11][i] != "no_cell_function":
                    startup_treeview_column.set_cell_data_func(cell_renderer, startup_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            startup_treeview_column.set_sizing(2)                                             # Set column sizing (2 = auto sizing which is required for "treeview5101.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            startup_treeview_column.set_sort_column_id(cumulative_sort_column_id)             # Be careful with lists contain same element more than one.
            startup_treeview_column.set_resizable(True)                                       # Set columns resizable by the user when column title button edge handles are dragged.
            startup_treeview_column.set_reorderable(True)                                     # Set columns reorderable by the user when column title buttons are dragged.
            startup_treeview_column.set_min_width(40)                                         # Set minimum column widths as "40 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            startup_treeview_column.connect("clicked", on_column_title_clicked)               # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview5101.append_column(startup_treeview_column)                               # Append column into treeview

        # Get column data types for appending startup data into treestore
        startup_data_column_types = []
        for column in sorted(startup_treeview_columns_shown):
            internal_column_count = len(startup_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                startup_data_column_types.append(startup_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore5101                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore5101 = Gtk.TreeStore()
        treestore5101.set_column_types(startup_data_column_types)                             # Set column types of the columns which will be appended into treestore
        treemodelfilter5101 = treestore5101.filter_new()
        treemodelfilter5101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort5101 = Gtk.TreeModelSort(treemodelfilter5101)
        treeview5101.set_model(treemodelsort5101)
        all_autostart_applications_list_prev = []                                             # Redefine (clear) "all_autostart_applications_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    treeview5101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if startup_treeview_columns_shown_prev != startup_treeview_columns_shown or startup_data_column_order_prev != startup_data_column_order:
        startup_treeview_columns = treeview5101.get_columns()                                 # Get shown columns on the treeview in order to use this data for reordering the columns.
        startup_treeview_columns_modified = treeview5101.get_columns()
        treeview_column_titles = []
        for column in startup_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for order in reversed(sorted(startup_data_column_order)):                             # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if startup_data_column_order.index(order) <= len(startup_treeview_columns) - 1 and startup_data_column_order.index(order) in startup_treeview_columns_shown:
                column_number_to_move = startup_data_column_order.index(order)
                column_title_to_move = startup_data_list[column_number_to_move][1]
                column_to_move = startup_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                column_title_to_move = column_to_move.get_title()
                for data in startup_data_list:
                    if data[1] == column_title_to_move:
                        treeview5101.move_column_after(column_to_move, None)                  # Column is moved at the beginning of the treeview if "None" is used.

    # Sort startup rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if startup_treeview_columns_shown_prev != startup_treeview_columns_shown or startup_data_row_sorting_column_prev != startup_data_row_sorting_column or startup_data_row_sorting_order != startup_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        startup_treeview_columns = treeview5101.get_columns()                                 # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in startup_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if startup_data_row_sorting_column in startup_treeview_columns_shown:
                for data in startup_data_list:
                    if data[0] == startup_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if startup_data_row_sorting_column not in startup_treeview_columns_shown:
                column_title_for_sorting = startup_data_list[0][1]
            column_for_sorting = startup_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if startup_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if startup_treeview_columns_shown_prev != startup_treeview_columns_shown or startup_data_column_widths_prev != startup_data_column_widths:
        startup_treeview_columns = treeview5101.get_columns()
        treeview_column_titles = []
        for column in startup_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, startup_data in enumerate(startup_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == startup_data[1]:
                   column_width = startup_data_column_widths[i]
                   startup_treeview_columns[j].set_fixed_width(column_width)                  # Set column width in pixels. Fixed width is unset if value is "-1".

    # Get new/deleted(ended) startup applications for updating treestore/treeview
    all_autostart_applications_list = all_autostart_applications                              # For consistency with other tabs treeview code (Processes, Startup, Storage, etc.)
    all_autostart_applications_list_prev_set = set(all_autostart_applications_list_prev)
    all_autostart_applications_list_set = set(all_autostart_applications_list)
    deleted_startup_application = sorted(list(all_autostart_applications_list_prev_set - all_autostart_applications_list_set))
    new_startup_application = sorted(list(all_autostart_applications_list_set - all_autostart_applications_list_prev_set))
    existing_startup_application = sorted(list(all_autostart_applications_list_set.intersection(all_autostart_applications_list_prev)))
    updated_existing_startup_app_index = [[all_autostart_applications_list.index(i), all_autostart_applications_list_prev.index(i)] for i in existing_startup_application]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    startup_app_data_rows_row_length = len(startup_data_rows[0])
    # Append/Remove/Update startup applications data into treestore
    treeview5101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global startup_application_search_text, filter_column
    if len(piter_list) > 0:
        for i, j in updated_existing_startup_app_index:
            if startup_data_rows[i] != startup_data_rows_prev[j]:
                for k in range(1, startup_app_data_rows_row_length):                          # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                    if startup_data_rows_prev[j][k] != startup_data_rows[i][k]:
                        treestore5101.set_value(piter_list[j], k, startup_data_rows[i][k])
    if len(deleted_startup_application) > 0:
        for startup_application in reversed(sorted(list(deleted_startup_application))):
            treestore5101.remove(piter_list[all_autostart_applications_list_prev.index(startup_application)])
            piter_list.remove(piter_list[all_autostart_applications_list_prev.index(startup_application)])
    if len(new_startup_application) > 0:
        for startup_application in new_startup_application:
            # /// Start /// This block of code is used for determining if the newly added startup_application will be shown on the treeview (user search actions and/or search customizations and/or "Show all visible/hidden startup items" preference affect startup item visibility).
            if radiobutton5102.get_active() == True and startup_applications_visibility_list[all_autostart_applications_list.index(startup_application)] != True:    # Hide startup_application (set the visibility value as "False") if "Show all visible startup items" option is selected on the GUI and startup_application visibility is not "True".
                startup_data_rows[all_autostart_applications_list.index(startup_application)][0] = False
            if radiobutton5103.get_active() == True and startup_applications_visibility_list[all_autostart_applications_list.index(startup_application)] == True:    # Hide startup_application (set the visibility value as "False") if "Show all hidden startup items" option is selected on the GUI and startup_application visibility is "True".
                startup_data_rows[all_autostart_applications_list.index(startup_application)][0] = False
            if searchentry5101.get_text() != "":
                startup_application_search_text = searchentry5101.get_text()
                startup_item_data_text_in_model = startup_data_rows[all_autostart_applications_list.index(startup_application)][filter_column]
                if startup_application_search_text not in str(startup_item_data_text_in_model).lower():    # Hide startup_application (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the startup_application data.
                    startup_data_rows[all_autostart_applications_list.index(startup_application)][0] = False
            # \\\ End \\\ This block of code is used for determining if the newly added startup_application will be shown on the treeview (user search actions and/or search customizations and/or "Show all visible/hidden startup items" preference affect startup_application visibility).
            piter_list.insert(all_autostart_applications_list.index(startup_application), treestore5101.insert(None, all_autostart_applications_list.index(startup_application), startup_data_rows[all_autostart_applications_list.index(startup_application)]))    # "insert" have to be used for appending element into both "piter_list" and "treestore" in order to avoid data index problems which are caused by sorting of ".desktop" file names (this sorting is performed for getting list differences).
    treeview5101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.
    all_autostart_applications_list_prev = all_autostart_applications_list                    # For using values in the next loop
    startup_data_rows_prev = startup_data_rows
    startup_treeview_columns_shown_prev = startup_treeview_columns_shown
    startup_data_row_sorting_column_prev = startup_data_row_sorting_column
    startup_data_row_sorting_order_prev = startup_data_row_sorting_order
    startup_data_column_order_prev = startup_data_column_order
    startup_data_column_widths_prev = startup_data_column_widths

    # Get number of startup items and show this information on the searchentry as placeholder text
    number_of_all_startup_applications = len(startup_applications_visibility_list)
    searchentry5101.set_placeholder_text(_tr("Search...") + "          " + "(" + _tr("Startup Items") + ": " + str(number_of_all_startup_applications) + ")")


# ----------------------------------- Startup - Run Function -----------------------------------
def startup_run_func(*args):

    if "startup_data_rows" not in globals():
        GLib.idle_add(startup_initial_func)
    if Config.current_main_tab == 3:
        global startup_glib_source, update_interval
        try:
            startup_glib_source.destroy()
        except NameError:
            pass
        update_interval = Config.update_interval
        startup_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(startup_loop_func)
        startup_glib_source.set_callback(startup_run_func)
        startup_glib_source.attach(GLib.MainContext.default())


# ----------------------------------- Startup - Treeview Filter Show All Function -----------------------------------
def startup_treeview_filter_show_all_func():

    for piter in piter_list:
        treestore5101.set_value(piter, 0, True)


# ----------------------------------- Startup - Treeview Filter Show All Enabled (Visible) Startup Items Function -----------------------------------
def startup_treeview_filter_startup_visible_only():

    for piter in piter_list:
        if startup_applications_visibility_list[piter_list.index(piter)] != True:
            treestore5101.set_value(piter, 0, False)


# ----------------------------------- Startup - Treeview Filter Show All Disabled (Hidden) Startup Items Function -----------------------------------
def startup_treeview_filter_startup_hidden_only():

    for piter in piter_list:
        if startup_applications_visibility_list[piter_list.index(piter)] == True:
            treestore5101.set_value(piter, 0, False)


# ----------------------------------- Startup - Treeview Filter Search Function -----------------------------------
def startup_treeview_filter_search_func():

    global filter_column
    startup_application_search_text = searchentry5101.get_text().lower()
    # Set visible/hidden startup items
    for piter in piter_list:
        treestore5101.set_value(piter, 0, False)
        startup_item_data_text_in_model = treestore5101.get_value(piter, filter_column)
        if startup_application_search_text in str(startup_item_data_text_in_model).lower():
            treestore5101.set_value(piter, 0, True)


# ----------------------------------- Startup - Column Title Clicked Function -----------------------------------
def on_column_title_clicked(widget):

    startup_data_row_sorting_column_title = widget.get_title()                                # Get column title which will be used for getting column number
    for data in startup_data_list:
        if data[1] == startup_data_row_sorting_column_title:
            Config.startup_data_row_sorting_column = data[0]                                  # Get column number
    Config.startup_data_row_sorting_order = int(widget.get_sort_order())                      # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Startup - Treeview Column Order-Width Row Sorting Function -----------------------------------
def startup_treeview_column_order_width_row_sorting_func():

    startup_treeview_columns = treeview5101.get_columns()
    treeview_column_titles = []
    for column in startup_treeview_columns:
        treeview_column_titles.append(column.get_title())
    for i, startup_data in enumerate(startup_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == startup_data[1]:
                Config.startup_data_column_order[i] = j
                Config.startup_data_column_widths[i] = startup_treeview_columns[j].get_width()
                break
    Config.config_save_func()
