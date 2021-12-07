#!/usr/bin/env python3

# ----------------------------------- Users - Users Right Click Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_menu_right_click_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global Users, MainGUI
    import Users, MainGUI


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


# ----------------------------------- Users - Users Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def users_menu_right_click_gui_func():

    # Define builder and get all objects (Users tab right click menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenuRightClick.ui")

    # ********************** Define object names for Users tab right click menu **********************
    global menu3101m
    global menuitem3101m
    global menuitem3102m

    # ********************** Get object names for Users tab right click menu **********************
    menu3101m = builder.get_object('menu3101m')
    menuitem3101m = builder.get_object('menuitem3101m')
    menuitem3102m = builder.get_object('menuitem3102m')


    # ********************** Define object functions for Users tab right click menu **********************
    def on_menuitem3101m_activate(widget):                                                    # "End User Session" item on the right click menu
        selected_username = str(Users.selected_username)                                      # Get right clicked username
        selected_user_uid = str(Users.selected_user_uid)                                      # Get right clicked user UID
        users_end_user_session_warning_dialog(selected_username, selected_user_uid)
        if warning_dialog3102_response == Gtk.ResponseType.NO:
            return                                                                            # Do nothing (stop running the code and close the dialog) if "No" is clicked.
        try:
            (subprocess.check_output(["pkexec", "pkill", "-9", "--uid", selected_user_uid], stderr=subprocess.STDOUT, shell=False)).decode()    # End processes which has the specified UID.
        except Exception:
            users_end_user_session_root_privileges_warning_dialog()

    def on_menuitem3102m_activate(widget):                                                    # "Details" item on the right click menu
        if 'UsersDetails' not in globals():                                                   # Check if "UsersDetails" module is imported. Therefore it is not reimported for every click on "Details" menu item on right click menu if "UsersDetails" name is in globals().
            global UsersDetails
            import UsersDetails
            UsersDetails.users_details_import_func()
            UsersDetails.users_details_gui_function()
        UsersDetails.window3101w.show()
        UsersDetails.users_details_foreground_thread_run_func()


    # ********************** Connect signals to GUI objects for Users tab right click menu **********************
    menuitem3101m.connect("activate", on_menuitem3101m_activate)
    menuitem3102m.connect("activate", on_menuitem3102m_activate)


# ----------------------------------- Users - End User Session Root Privileges Warning Dialog Function (shows a warning dialog when an user session is tried to be ended without entering password on polkit dialog) -----------------------------------
def users_end_user_session_root_privileges_warning_dialog():

    warning_dialog3101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Access Denied"), )
    warning_dialog3101.format_secondary_text(_tr("Root privileges are needed for ending an user session."))
    global warning_dialog3101_response
    warning_dialog3101_response = warning_dialog3101.run()
    warning_dialog3101.destroy()


# ----------------------------------- Users - End User Session Warning Dialog Function (shows a warning dialog when an user session is tried to be ended) -----------------------------------
def users_end_user_session_warning_dialog(selected_username, selected_user_uid):

    warning_dialog3102 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do You Want To End User Session?"), )
    warning_dialog3102.format_secondary_text(_tr("This action will end all processes of the user immediately and may cause data loss for the user.") +
                                             "\n" + _tr("User session will be ended if you continue.") +
                                             "\n" + _tr("Do you want to continue?") +
                                             "\n\n    " + _tr("User Name:") + " " + selected_username +
                                             "\n    " + _tr("User UID:") + " " + selected_user_uid)
    global warning_dialog3102_response
    warning_dialog3102_response = warning_dialog3102.run()
    warning_dialog3102.destroy()
