#!/usr/bin/env python3

# ----------------------------------- Startup - Startup New Item Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def startup_new_item_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global MainGUI
    import MainGUI


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


# ----------------------------------- Startup - Startup New Item Window GUI Function (the code of this module in order to avoid running them during module import and defines "Startup" tab GUI objects and functions/signals) -----------------------------------
def startup_new_item_gui_func():

    global builder5101w, window5101w
    global entry5101w, entry5102w, entry5103w, entry5104w, checkbutton5101w, checkbutton5102w, button5101w, button5102w

    builder5101w = Gtk.Builder()
    builder5101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupNewItemWindow.ui")

    # Startup New Item window GUI objects - get
    window5101w = builder5101w.get_object('window5101w')
    entry5101w = builder5101w.get_object('entry5101w')
    entry5102w = builder5101w.get_object('entry5102w')
    entry5103w = builder5101w.get_object('entry5103w')
    entry5104w = builder5101w.get_object('entry5104w')
    checkbutton5101w = builder5101w.get_object('checkbutton5101w')
    checkbutton5102w = builder5101w.get_object('checkbutton5102w')
    radiobutton5101w = builder5101w.get_object('radiobutton5101w')
    radiobutton5102w = builder5101w.get_object('radiobutton5102w')
    button5101w = builder5101w.get_object('button5101w')
    button5102w = builder5101w.get_object('button5102w')


    # Startup New Item window GUI functions
    def on_window5101w_delete_event(widget, event):
        window5101w.hide()
        return True

    def on_window5101w_show(widget):                                                          # Reset window GUI content on window show. Because window is hidden when close button is clicked and content will be shown again when window is reopened.
        entry5101w.set_text("")
        entry5102w.set_text("")
        entry5103w.set_text("")
        entry5104w.set_text("")
        checkbutton5101w.set_active(False)
        checkbutton5102w.set_active(False)
        radiobutton5101w.set_active(True)
        button5102w.set_sensitive(False)
        entry5101w.set_can_focus(True)                                                        # Set flag to be able to enable grabing focus to be ready for typing directly without clicking on it. Otherwise, entry has to be clicked on it for typing in it.
        entry5101w.grab_focus()                                                               # Enable grabing focus to be ready for typing directly without clicking on it. Otherwise, entry has to be clicked on it for typing in it.


    def on_entry5101w_changed(widget):                                                        # Set sensitivity of the "Save" button as "False" if "Name" and "Command" entries are empty.
        if entry5101w.get_text() == "" or entry5103w.get_text() == "":
            button5102w.set_sensitive(False)
        if entry5101w.get_text() != "" and entry5103w.get_text() != "":
            button5102w.set_sensitive(True)

    def on_entry5103w_changed(widget):                                                        # Set sensitivity of the "Save" button as "False" if "Name" and "Command" entries are empty.
        if entry5101w.get_text() == "" or entry5103w.get_text() == "":
            button5102w.set_sensitive(False)
        if entry5101w.get_text() != "" and entry5103w.get_text() != "":
            button5102w.set_sensitive(True)

    def on_button5101w_clicked(widget):                                                       # "Cancel" button
        window5101w.hide()

    def on_button5102w_clicked(widget):                                                       # "Save" button
        startup_get_system_and_user_autostart_directories_func()

        new_startup_application_name = entry5101w.get_text()
        new_startup_application_file_name = entry5101w.get_text() + ".desktop"
        new_startup_application_comment = entry5102w.get_text()
        new_startup_application_command = entry5103w.get_text()
        new_startup_application_icon = entry5104w.get_text()
        if checkbutton5101w.get_active() == True:
            new_startup_application_startup_notify = "True"
        if checkbutton5101w.get_active() == False:
            new_startup_application_startup_notify = "False"
        if checkbutton5102w.get_active() == True:
            new_startup_application_terminal = "True"
        if checkbutton5102w.get_active() == False:
            new_startup_application_terminal = "False"

        if radiobutton5101w.get_active() == True:
            system_or_current_user_autostart_directory = current_user_autostart_directory
        if radiobutton5102w.get_active() == True:
            system_or_current_user_autostart_directory = system_autostart_directory

        # Show a warning dialog if there is already a .desktop file with the same name.
        if os.path.isfile(system_or_current_user_autostart_directory + new_startup_application_file_name) == True:
            startup_overwrite_existing_startup_item_warning_dialog(new_startup_application_name, new_startup_application_file_name)
            if warning_dialog5103_response == Gtk.ResponseType.YES:
                pass                                                                          # Continue running the code if "Yes" is clicked on the dialog.
            if warning_dialog5103_response == Gtk.ResponseType.NO:
                return                                                                        # Do nothing (stop running the code and close the dialog) if "No" is clicked.
        # Save ".desktop" file in order to add new startup item
        python_file_and_path = os.path.dirname(os.path.realpath(__file__)) + "/../src/StartupNewItemSave.py"
        if radiobutton5101w.get_active() == True:
            try:
                (subprocess.check_output(["python3", python_file_and_path,
                                          system_or_current_user_autostart_directory,
                                          new_startup_application_file_name, new_startup_application_name,
                                          new_startup_application_comment, new_startup_application_command, new_startup_application_icon,
                                          new_startup_application_startup_notify, new_startup_application_terminal
                                          ], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:                                             # For handling the error which is generated if user clicks "cancel" on the password dialog for root privileges. This also suppresses other errors when subprocess is used. There may be additional work for handling specific errors which are generated when subprocess is used.
                pass
        if radiobutton5102w.get_active() == True:
            try:
                (subprocess.check_output(["pkexec", "python3", python_file_and_path,
                                          system_or_current_user_autostart_directory,
                                          new_startup_application_file_name, new_startup_application_name,
                                          new_startup_application_comment, new_startup_application_command, new_startup_application_icon,
                                          new_startup_application_startup_notify, new_startup_application_terminal
                                          ], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:                                             # For handling the error which is generated if user clicks "cancel" on the password dialog for root privileges. This also suppresses other errors when subprocess is used. There may be additional work for handling specific errors which are generated when subprocess is used.
                pass
        window5101w.hide()


    # Startup New Item window GUI functions - connect
    window5101w.connect("delete-event", on_window5101w_delete_event)
    window5101w.connect("show", on_window5101w_show)
    entry5101w.connect("changed", on_entry5101w_changed)
    entry5103w.connect("changed", on_entry5103w_changed)
    button5101w.connect("clicked", on_button5101w_clicked)
    button5102w.connect("clicked", on_button5102w_clicked)


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


# ----------------------------------- Startup - Startup Overwrite Existing Startup Item Warning Dialog Function (shows a warning dialog when a new startup item file is tried to be generated with the same name of an existing one) -----------------------------------
def startup_overwrite_existing_startup_item_warning_dialog(new_startup_application_name, new_startup_application_file_name):

    warning_dialog5103 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do You Want To Overwrite Existing File?"), )
    warning_dialog5103.format_secondary_text(_tr("There is already a '.desktop' file with the same name.") +
                                             "\n" + _tr("Existing file will be overwritten if you continue.") +
                                             "\n" + _tr("Do you want to continue?") +
                                             "\n\n    " + _tr("Existing Startup Item:") + " " + new_startup_application_name +
                                             "\n    " + _tr("Existing '.desktop' File Name:") + " " + new_startup_application_file_name)
    global warning_dialog5103_response
    warning_dialog5103_response = warning_dialog5103.run()
    warning_dialog5103.destroy()
