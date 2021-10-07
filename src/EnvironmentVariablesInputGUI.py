#!/usr/bin/env python3

# ----------------------------------- Environment Variables - Environment Variables New Item Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_input_gui_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global EnvironmentVariablesGUI, MainGUI
    import EnvironmentVariablesGUI, MainGUI


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


# ----------------------------------- Environment Variables - Environment Variables New Item Window GUI Function (the code of this module in order to avoid running them during module import and defines "Environment Variables" tab GUI objects and functions/signals) -----------------------------------
def environment_variables_input_gui_func():

    global builder7101w, window7101w
    global entry7101w, entry7102w, radiobutton7101w, radiobutton7102w, checkbutton7101w, button7101w, button7102w

    builder7101w = Gtk.Builder()
    builder7101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVariablesInputWindow.ui")

    # Environment Variables New Item window GUI objects - get
    window7101w = builder7101w.get_object('window7101w')
    entry7101w = builder7101w.get_object('entry7101w')
    entry7102w = builder7101w.get_object('entry7102w')
    radiobutton7101w = builder7101w.get_object('radiobutton7101w')
    radiobutton7102w = builder7101w.get_object('radiobutton7102w')
    checkbutton7101w = builder7101w.get_object('checkbutton7101w')
    button7101w = builder7101w.get_object('button7101w')
    button7102w = builder7101w.get_object('button7102w')


    # Environment Variables New Item window GUI functions
    def on_window7101w_delete_event(widget, event):
        window7101w.hide()
        return True

    def on_window7101w_show(widget):                                                          # Reset window GUI content on window show. Because window is hidden when close button is clicked and content will be shown again when window is reopened.
        entry7101w.set_text("")
        entry7102w.set_text("")
        radiobutton7101w.set_active(True)
        button7102w.set_sensitive(False)

    def on_entry7101w_changed(widget):                                                        # Set sensitivity of the "Save" button as "False" if "Name" and "Command" entries are empty.
        if entry7101w.get_text() == "":
            button7102w.set_sensitive(False)
        if entry7101w.get_text() != "":
            button7102w.set_sensitive(True)

    def on_radiobutton7101w_toggled(widget):                                                  # "Only current user" radiobutton
        if radiobutton7101w.get_active() == True:
            checkbutton7101w.set_sensitive(False)
            checkbutton7101w.set_active(False)

    def on_radiobutton7102w_toggled(widget):                                                  # "All users" radiobutton
        if radiobutton7102w.get_active() == True:
            checkbutton7101w.set_sensitive(True)
            checkbutton7101w.set_active(False)
            environment_variables_variable_for_all_users_warning_dialog()
            if warning_dialog7103_response == Gtk.ResponseType.YES:
                pass                                                                          # Leave the option (checkbutton) as "All Users" if "Yes" is clicked on the dialog.
            if warning_dialog7103_response == Gtk.ResponseType.NO:
                radiobutton7101w.set_active(True)                                             # Set the option as "Only Current User" if "No" is clicked on the dialog.

    def on_button7101w_clicked(widget):                                                       # "Cancel" button
        window7101w.hide()

    def on_button7102w_clicked(widget):                                                       # "Save" button
        new_variable = entry7101w.get_text().upper()                                          # Environment variables are uppercase.
        new_value = entry7102w.get_text()

        # Get human and root user usernames and UIDs. This data will be used if application is run with "pkexec" command.
        usernames_username_list = []
        usernames_uid_list = []
        with open("/etc/passwd") as reader:                                                   # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
            etc_passwd_lines = reader.read().strip().split("\n")                              # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
        for line in etc_passwd_lines:
            line_splitted = line.split(":")
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

        # Get startup item file directories. System default autostart directory is "system_autostart_directory". Startup items are copied into "current_user_autostart_directory" directory with modified values if user make modifications for the startup item. For the user, these values override system values for the user-modified startup item.
        for line in etc_passwd_lines:
            line_splitted = line.split(":")
            if line_splitted[0] == current_user_name:
                current_user_homedir = line_splitted[5]

        # If "add environment variable for only current user" is preferred
        if radiobutton7101w.get_active():
            with open(current_user_homedir + "/.bashrc") as reader:
                bashrc_lines = reader.read().strip().split("\n")                              # ".strip()" is used in order to prevent adding "\n" per function run (this new line is appended when data is written into file).
            for line in bashrc_lines:
                if line.startswith("export " + new_variable + "=") == True:                   # Check if there is already an environment variable with the same name.
                    existing_variable_value = line.split("export ")[-1]
                    existing_variable = existing_variable_value.split("=")[0]
                    existing_value = '='.join(existing_variable_value.split("=")[1:])         # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
                    environment_variables_overwrite_existing_environment_variable_warning_dialog(existing_variable, existing_value, new_variable, new_value)
                    if warning_dialog7102_response == Gtk.ResponseType.YES:                   # Continue running the code and overwrite existing variable if "Yes" is clicked on the dialog.
                        continue
                    if warning_dialog7102_response == Gtk.ResponseType.NO:
                        return                                                                # Stop running the code and do not overwrite existing variable if "No" is clicked on the dialog.
            with open(current_user_homedir + "/.bashrc", "w") as writer:
                for line_write in bashrc_lines:
                    if line_write.startswith("export " + new_variable + "=") == False:        # Write exiting lines into the file.
                        writer.write("\n" + line_write)
                writer.write("\n" + "export " + new_variable + "=" + new_value)               # Write new variable into the file.

        # If "add environment variable for all users" is preferred
        if radiobutton7102w.get_active():
            with open("/etc/environment") as reader:
                etc_environment_lines = reader.read().strip().split("\n")                     # ".strip()" is used in order to prevent adding "\n" per function run (this new line is appended when data is written into file).
            for line in etc_environment_lines:
                if line.startswith(new_variable + "=") == True:                               # Check if there is already an environment variable with the same name.
                    existing_variable = line.split("=")[0]
                    existing_value = '='.join(line.split("=")[1:])                            # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
                    environment_variables_overwrite_existing_environment_variable_warning_dialog(existing_variable, existing_value, new_variable, new_value)
                    if warning_dialog7102_response == Gtk.ResponseType.YES:                   # Continue running the code and overwrite existing variable if "Yes" is clicked on the dialog.
                        continue
                    if warning_dialog7102_response == Gtk.ResponseType.NO:                    # Stop running the code and do not overwrite existing variable if "No" is clicked on the dialog.
                        return
            current_working_directory = os.getcwd()                                           # Get current working directory which will be used for running a Python module in this directory by using bash.
            variables_to_pass = 'a=' + new_variable + '; b=' + new_value + ';'                # To pass these variable to be used in the called Python module.
            try:
                subprocess.check_output(variables_to_pass + ' pkexec python3 ' + current_working_directory + '/' + 'EnvironmentVariablesAddForAllUsers.py "$a" "$b"', shell=True)    # Run the command for running a Python module with "root" privileges.
            except subprocess.CalledProcessError:                                             # For handling the error which is generated if user clicks "cancel" on the password dialog for root privileges. This also suppresses other errors when subprocess is used. There may be additional work for handling specific errors which are generated when subprocess is used.
                pass

        window7101w.hide()



    # Environment Variables New Item window GUI functions - connect
    window7101w.connect("delete-event", on_window7101w_delete_event)
    window7101w.connect("show", on_window7101w_show)
    entry7101w.connect("changed", on_entry7101w_changed)
    radiobutton7101w.connect("toggled", on_radiobutton7101w_toggled)
    radiobutton7102w.connect("toggled", on_radiobutton7102w_toggled)
    button7101w.connect("clicked", on_button7101w_clicked)
    button7102w.connect("clicked", on_button7102w_clicked)


# ----------------------------------- Environment Variables - Environment Variables Overwrite Existing Environment Variables Warning Dialog Function (shows a warning dialog when a new environment variable is tried to be generated with the same name of an existing one) -----------------------------------
def environment_variables_overwrite_existing_environment_variable_warning_dialog(existing_variable, existing_value, new_variable, new_value):

    warning_dialog7102 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do You Want To Overwrite Existing Environment Variable?"), )
    warning_dialog7102.format_secondary_text(_tr("There is already an environment variable with the same name.\nExisting variable will be overwritten if you continue.\nDo you want to continue?") + "\n" + _tr("    Existing Environment Variable: ") + existing_variable + "\n" + _tr("    Existing Environment Variable Value: ") + existing_value + "\n" + _tr("    New Environment Variable: ") + new_variable + "\n" + _tr("    New Environment Variable Value: ") + new_value)
    global warning_dialog7102_response
    warning_dialog7102_response = warning_dialog7102.run()
    warning_dialog7102.destroy()


# ----------------------------------- Environment Variables - Environment Variables Variable For All Users Warning Dialog Function (shows a warning dialog when a new environment variable is tried to be generated for all users on the system because changing/overwriting system-wide variables could make system unusable.) -----------------------------------
def environment_variables_variable_for_all_users_warning_dialog():

    warning_dialog7103 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do You Want To Add Environment Variable For All Users?"), )
    warning_dialog7103.format_secondary_text(_tr("You may make your system unusable if you edit/overwrite some of the system variables.\nVariable will be added/edited for all users if this option is enabled.\nThis warning is also shown when an environment variable for all users is tried to be edited.\nDo you want to enable/keep enabled this option?"))
    global warning_dialog7103_response
    warning_dialog7103_response = warning_dialog7103.run()
    warning_dialog7103.destroy()
