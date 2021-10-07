#! /usr/bin/python3

# ----------------------------------- Environment Variables - Environment Variables Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, EnvironmentVariables, EnvironmentVariablesGUI, EnvironmentVariablesInputGUI, MainGUI
    import Config, EnvironmentVariables, EnvironmentVariablesGUI, EnvironmentVariablesInputGUI, MainGUI


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


# ----------------------------------- Environment Variables - Environment Variables Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Environment Variables" tab menu/popover GUI objects and functions/signals) -----------------------------------
def environment_variables_menus_gui_func():

    # Define builder and get all objects (Environment Variables tab right click menu, Environment Variables tab customizations popover, Environment Variables tab search customizations popover) from GUI file.
    builder7101m = Gtk.Builder()
    builder7101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVariablesMenus.ui")


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Environment Variables tab right click menu
    # ********************** Define object names for Environment Variables tab right click menu **********************
    global menu7101m
    global menuitem7101m, menuitem7102m, menuitem7103m, menuitem7104m, menuitem7105m

    # ********************** Get object names for Environment Variables tab right click menu **********************
    menu7101m = builder7101m.get_object('menu7101m')
    menuitem7101m = builder7101m.get_object('menuitem7101m')
    menuitem7102m = builder7101m.get_object('menuitem7102m')
    menuitem7103m = builder7101m.get_object('menuitem7103m')
    menuitem7104m = builder7101m.get_object('menuitem7104m')
    menuitem7105m = builder7101m.get_object('menuitem7105m')


    # ********************** Define object functions for Environment Variables tab right click menu **********************
    def on_menuitem7101m_activate(widget):                                                    # "Add Environment Variable" item on the right click menu
        EnvironmentVariablesInputGUI.window7101w.set_title(_tr("Add New Persistent Environment Variable"))
        EnvironmentVariablesInputGUI.window7101w.show()

    def on_menuitem7102m_activate(widget):                                                    # "Edit Environment Variable" item on the right click menu
        selected_variable = EnvironmentVariablesGUI.selected_variable_value.split("=")[0]
        selected_variable_value = '='.join(EnvironmentVariablesGUI.selected_variable_value.split("=")[1:])    # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
        selected_variable_type = EnvironmentVariablesGUI.selected_variable_type
        EnvironmentVariablesInputGUI.window7101w.show()
        EnvironmentVariablesInputGUI.entry7101w.set_text(selected_variable)                   # Set label text as varible to be edited
        EnvironmentVariablesInputGUI.entry7102w.set_text(selected_variable_value)             # Set label text as varible value to be edited
        EnvironmentVariablesInputGUI.window7101w.set_title(_tr("Edit Persistent Environment Variable"))    # Set window title as written in the code because same window is used for both adding a new environment variable and editing an existing environment variable.

    def on_menuitem7103m_activate(widget):                                                    # "Delete Environment Variable" item on the right click menu
        selected_variable = EnvironmentVariablesGUI.selected_variable_value.split("=")[0]
        selected_variable_value = '='.join(EnvironmentVariablesGUI.selected_variable_value.split("=")[1:])    # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.

        environment_variables_delete_variable_warning_dialog(selected_variable, selected_variable_value)    # Show a warning dialog before deleting an environment variable.
        if warning_dialog7104_response == Gtk.ResponseType.YES:                               # Delete the variable (continue running the function) if "Yes" is clicked on the dialog.
            pass
        if warning_dialog7104_response == Gtk.ResponseType.NO:                                # Do nothing (stop running the function) if "No" is clicked on the dialog.
            return
        environment_variables_get_current_user_home_dir_func()                                # Run the function for getting home directory of the current user. This directory will be used for reading from/writing into ".bashrc" file.
        with open(current_user_homedir + "/.bashrc") as reader:
            bashrc_lines = reader.read().strip().split("\n")                                  # ".strip()" is used in order to prevent adding "\n" per function run (this new line is appended when data is written into file).
        with open(current_user_homedir + "/.bashrc", "w") as writer:                          # Rewrite ".bashrc" file content by skipping the line which contains the environment variable to be deleted.
            for line_write in bashrc_lines:
                if line_write.startswith("export " + selected_variable + "=") == False:
                    writer.write(line_write + "\n")

        current_working_directory = os.getcwd()                                               # Get current working directory which will be used for running a Python module in this directory by using bash.
        variables_to_pass = 'a=' + selected_variable + '; b=' + selected_variable_value + ';'    # To pass these variable to be used in the called Python module.
        try:
            subprocess.check_output(variables_to_pass + ' pkexec python3 ' + current_working_directory + '/' + 'EnvironmentVariablesDeleteForAllUsers.py "$a" "$b"', shell=True)    # Run the command for running a Python module with "root" privileges.
        except subprocess.CalledProcessError:                                                 # For handling the error which is generated if user clicks "cancel" on the password dialog for root privileges. This also suppresses other errors when subprocess is used. There may be additional work for handling specific errors which are generated when subprocess is used.
            pass

    def on_menuitem7104m_activate(widget):                                                    # "Copy Variable" item on the right click menu
        selected_variable = EnvironmentVariablesGUI.selected_variable_value.split("=")[0]
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(selected_variable, -1)
        clipboard.store()

    def on_menuitem7105m_activate(widget):                                                    # "Copy Value" item on the right click menu
        selected_value = '='.join(EnvironmentVariablesGUI.selected_variable_value.split("=")[1:])    # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(selected_value, -1)
        clipboard.store()

    # ********************** Connect signals to GUI objects for Environment Variables tab right click menu **********************
    menuitem7101m.connect("activate", on_menuitem7101m_activate)
    menuitem7102m.connect("activate", on_menuitem7102m_activate)
    menuitem7103m.connect("activate", on_menuitem7103m_activate)
    menuitem7104m.connect("activate", on_menuitem7104m_activate)
    menuitem7105m.connect("activate", on_menuitem7105m_activate)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Environment Variables tab customizations popover
    # ********************** Define object names for Environment Variables tab customizations popover **********************
    global popover7101p
    global checkbutton7101p, checkbutton7102p, checkbutton7103p
    global button7101p, button7102p

    # ********************** Get object names for Environment Variables tab customizations popover **********************
    popover7101p = builder7101m.get_object('popover7101p')
    checkbutton7101p = builder7101m.get_object('checkbutton7101p')
    checkbutton7102p = builder7101m.get_object('checkbutton7102p')
    checkbutton7103p = builder7101m.get_object('checkbutton7103p')
    button7101p = builder7101m.get_object('button7101p')
    button7102p = builder7101m.get_object('button7102p')

    # ********************** Define object functions for Environment Variables tab customizations popover Common GUI Objects **********************
    def on_button7101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_environment_variables_func()
        Config.config_save_func()
        environment_variables_tab_customization_popover_disconnect_signals_func()
        environment_variables_tab_popover_set_gui()
        environment_variables_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Environment Variables tab customizations popover View Tab **********************
    def on_button7102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_environment_variables_row_sort_column_order_func()
        environment_variables_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        environment_variables_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Environment Variables tab customizations popover Add/Remove Columns Tab **********************
    def on_checkbutton7101p_toggled(widget):                                                 # "Variable" checkbutton
        environment_variables_add_remove_columns_function()
    def on_checkbutton7102p_toggled(widget):                                                 # "Value" checkbutton
        environment_variables_add_remove_columns_function()
    def on_checkbutton7103p_toggled(widget):                                                 # "Variable Type" checkbutton
        environment_variables_add_remove_columns_function()

    # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover Common GUI Objects **********************
    button7101p.connect("clicked", on_button7101p_clicked)
    # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover View Tab **********************
    button7102p.connect("clicked", on_button7102p_clicked)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Environment Variables tab search customizations popover
    # ********************** Define object names for Environment Variables tab search customizations popover **********************
    global popover7101p2
    global radiobutton7101p2, radiobutton7102p2
    global checkbutton7101p2, checkbutton7102p2, checkbutton7103p2

    # ********************** Get object names for Environment Variables tab search customizations popover **********************
    popover7101p2 = builder7101m.get_object('popover7101p2')
    radiobutton7101p2 = builder7101m.get_object('radiobutton7101p2')
    radiobutton7102p2 = builder7101m.get_object('radiobutton7102p2')
    checkbutton7101p2 = builder7101m.get_object('checkbutton7101p2')
    checkbutton7102p2 = builder7101m.get_object('checkbutton7102p2')
    checkbutton7103p2 = builder7101m.get_object('checkbutton7103p2')

    # ********************** Define object functions for Environment Variables tab search customizations popover **********************
    def on_radiobutton7101p2_toggled(widget):                                                 # "Variable" radiobutton
        if radiobutton7101p2.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_search_func()

    def on_radiobutton7102p2_toggled(widget):                                                 # "Value" radiobutton
        if radiobutton7102p2.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_search_func()

    def on_checkbutton7101p2_toggled(widget):                                                 # "All variables" checkbutton
        environment_variables_popovers_checkbutton_behavior_func(checkbutton7101p2)

    def on_checkbutton7102p2_toggled(widget):                                                 # "Environment variables" checkbutton
        environment_variables_popovers_checkbutton_behavior_func( checkbutton7102p2)

    def on_checkbutton7103p2_toggled(widget):                                                 # "Shell variables" checkbutton
        environment_variables_popovers_checkbutton_behavior_func(checkbutton7103p2)

    # ********************** Connect signals to GUI objects for Environment Variables tab search customizations popover **********************
    radiobutton7101p2.connect("toggled", on_radiobutton7101p2_toggled)
    radiobutton7102p2.connect("toggled", on_radiobutton7102p2_toggled)
    global checkbutton7101p2_handler_id, checkbutton7102p2_handler_id, checkbutton7103p2_handler_id
    checkbutton7101p2_handler_id = checkbutton7101p2.connect("toggled", on_checkbutton7101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton7102p2_handler_id = checkbutton7102p2.connect("toggled", on_checkbutton7102p2_toggled)
    checkbutton7103p2_handler_id = checkbutton7103p2.connect("toggled", on_checkbutton7103p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Environment Variables tab **********************
    popover7101p.set_relative_to(EnvironmentVariablesGUI.button7101)
    popover7101p.set_position(1)
    # ********************** Popover settings for Environment Variables tab search customizations **********************
    popover7101p2.set_relative_to(EnvironmentVariablesGUI.button7103)
    popover7101p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



    # ********************** Define function for connecting Environment Variables tab customizations popover GUI signals **********************
    def environment_variables_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover Add/Remove Columns Tab **********************
        checkbutton7101p.connect("toggled", on_checkbutton7101p_toggled)
        checkbutton7102p.connect("toggled", on_checkbutton7102p_toggled)
        checkbutton7103p.connect("toggled", on_checkbutton7103p_toggled)


    # ********************** Define function for disconnecting Environment Variables tab customizations popover GUI signals **********************
    def environment_variables_tab_customization_popover_disconnect_signals_func():
        # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover Add/Remove Columns Tab **********************
        checkbutton7101p.disconnect_by_func(on_checkbutton7101p_toggled)
        checkbutton7102p.disconnect_by_func(on_checkbutton7102p_toggled)
        checkbutton7103p.disconnect_by_func(on_checkbutton7103p_toggled)


    environment_variables_tab_popover_set_gui()
    environment_variables_tab_customization_popover_connect_signals_func()


# ********************** Set Environment Variables tab customizations popover menu GUI object data/selections appropriate for settings **********************
def environment_variables_tab_popover_set_gui():
    # Set Environment Variables tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.environment_variables_treeview_columns_shown:
        checkbutton7101p.set_active(True)
    if 0 not in Config.environment_variables_treeview_columns_shown:
        checkbutton7101p.set_active(False)
    if 1 in Config.environment_variables_treeview_columns_shown:
        checkbutton7102p.set_active(True)
    if 1 not in Config.environment_variables_treeview_columns_shown:
        checkbutton7102p.set_active(False)
    if 2 in Config.environment_variables_treeview_columns_shown:
        checkbutton7103p.set_active(True)
    if 2 not in Config.environment_variables_treeview_columns_shown:
        checkbutton7103p.set_active(False)


# ----------------------------------- Environment Variables - Environment Variables Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def environment_variables_popovers_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton7101p2, checkbutton7102p2, checkbutton7103p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton7101p2.handler_block(checkbutton7101p2_handler_id) as p1, checkbutton7102p2.handler_block(checkbutton7102p2_handler_id) as p2, checkbutton7103p2.handler_block(checkbutton7103p2_handler_id) as p3:
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

    if EnvironmentVariablesGUI.searchentry7101.get_text() != "":                                         # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the "Show all ... variables" radiobuttons above the treeview.
        EnvironmentVariables.environment_variables_treeview_filter_search_func()


# ----------------------------------- Environment Variables - Environment Variables Add/Remove Columns Function (adds/removes environment variables treeview columns) -----------------------------------
def environment_variables_add_remove_columns_function():

    Config.environment_variables_treeview_columns_shown = []
    if checkbutton7101p.get_active() is True:
        Config.environment_variables_treeview_columns_shown.append(0)
    if checkbutton7102p.get_active() is True:
        Config.environment_variables_treeview_columns_shown.append(1)
    if checkbutton7103p.get_active() is True:
        Config.environment_variables_treeview_columns_shown.append(2)
    Config.config_save_func()


# ----------------------------------- Environment Variables - Get Current User Home Dir Function (gets home directory of the current user) -----------------------------------
def environment_variables_get_current_user_home_dir_func():
    # Get human and root user usernames and UIDs. This data will be used if application is run with "pkexec" command.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                               # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                          # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])

    # Get current username which will be used for determining current user home directory.
    global current_user_name
    current_user_name = os.environ.get('SUDO_USER')                                   # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                     # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                            # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    # Get startup item file directories. System default autostart directory is "system_autostart_directory". Startup items are copied into "current_user_autostart_directory" directory with modified values if user make modifications for the startup item. For the user, these values override system values for the user-modified startup item.
    global current_user_homedir
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        if line_splitted[0] == current_user_name:
            current_user_homedir = line_splitted[5]


# ----------------------------------- Environment Variables - Delete Variable Warning Dialog Function (shows a warning dialog when an environment variable is tried to be deleted) -----------------------------------
def environment_variables_delete_variable_warning_dialog(selected_variable, selected_variable_value):

    warning_dialog7104 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do You Want To Delete The Environment Variable?"), )
    warning_dialog7104.format_secondary_text(_tr("Environment variable will be deleted from following files:") + "\n" + "    /etc/environment" + "\n" + "    /home/[username]/.bashrc" + "\n" + _tr("Do you want to delete the following persistent environment variable?" + "\n" + _tr("    Variable: ") + selected_variable + "\n" + _tr("    Value: ") + selected_variable_value))
    global warning_dialog7104_response
    warning_dialog7104_response = warning_dialog7104.run()
    warning_dialog7104.destroy()
