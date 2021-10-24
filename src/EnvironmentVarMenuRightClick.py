#!/usr/bin/env python3

# ----------------------------------- Environment Variables - Environment Variables Right Click GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_menu_right_click_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global EnvironmentVariables, MainGUI
    import EnvironmentVariables, MainGUI


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


# ----------------------------------- Environment Variables - Environment Variables Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Environment Variables" tab menu/popover GUI objects and functions/signals) -----------------------------------
def environment_variables_menu_right_click_gui_func():

    # Define builder and get all objects (Environment Variables tab right click menu) from GUI file.
    builder7101m = Gtk.Builder()
    builder7101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVarMenuRightClick.ui")


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
        if 'EnvironmentVariablesInput' not in globals():                                      # Check if "EnvironmentVariablesInput" module is imported. Therefore it is not reimported for every click on "Add Environment Variable" menu item if "EnvironmentVariablesInput" name is in globals().
            global EnvironmentVariablesInput
            import EnvironmentVariablesInput
            EnvironmentVariablesInput.environment_variables_input_gui_import_func()
            EnvironmentVariablesInput.environment_variables_input_gui_func()
        EnvironmentVariablesInput.window7101w.set_title(_tr("Add New Persistent Environment Variable"))
        EnvironmentVariablesInput.window7101w.show()

    def on_menuitem7102m_activate(widget):                                                    # "Edit Environment Variable" item on the right click menu
        selected_variable = EnvironmentVariables.selected_variable_value.split("=")[0]
        selected_variable_value = '='.join(EnvironmentVariables.selected_variable_value.split("=")[1:])    # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
        selected_variable_type = EnvironmentVariables.selected_variable_type
        if 'EnvironmentVariablesInput' not in globals():                                      # Check if "EnvironmentVariablesInput" module is imported. Therefore it is not reimported for every click on "Edit Environment Variable" menu item if "EnvironmentVariablesInput" name is in globals().
            global EnvironmentVariablesInput
            import EnvironmentVariablesInput
            EnvironmentVariablesInput.environment_variables_input_gui_import_func()
            EnvironmentVariablesInput.environment_variables_input_gui_func()
        EnvironmentVariablesInput.window7101w.show()
        EnvironmentVariablesInput.entry7101w.set_text(selected_variable)                      # Set label text as varible to be edited
        EnvironmentVariablesInput.entry7102w.set_text(selected_variable_value)                # Set label text as varible value to be edited
        EnvironmentVariablesInput.window7101w.set_title(_tr("Edit Persistent Environment Variable"))    # Set window title as written in the code because same window is used for both adding a new environment variable and editing an existing environment variable.

    def on_menuitem7103m_activate(widget):                                                    # "Delete Environment Variable" item on the right click menu
        selected_variable = EnvironmentVariables.selected_variable_value.split("=")[0]
        selected_variable_value = '='.join(EnvironmentVariables.selected_variable_value.split("=")[1:])    # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.

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
        selected_variable = EnvironmentVariables.selected_variable_value.split("=")[0]
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(selected_variable, -1)
        clipboard.store()

    def on_menuitem7105m_activate(widget):                                                    # "Copy Value" item on the right click menu
        selected_value = '='.join(EnvironmentVariables.selected_variable_value.split("=")[1:])    # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(selected_value, -1)
        clipboard.store()

    # ********************** Connect signals to GUI objects for Environment Variables tab right click menu **********************
    menuitem7101m.connect("activate", on_menuitem7101m_activate)
    menuitem7102m.connect("activate", on_menuitem7102m_activate)
    menuitem7103m.connect("activate", on_menuitem7103m_activate)
    menuitem7104m.connect("activate", on_menuitem7104m_activate)
    menuitem7105m.connect("activate", on_menuitem7105m_activate)


# ----------------------------------- Environment Variables - Get Current User Home Dir Function (gets home directory of the current user) -----------------------------------
def environment_variables_get_current_user_home_dir_func():
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
