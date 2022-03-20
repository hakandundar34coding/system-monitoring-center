#!/usr/bin/env python3

# ----------------------------------- Startup - Startup Right Click Menu GUI Import Function -----------------------------------
def startup_menu_right_click_import_func():

    global Gtk, Gdk, Gio, os, subprocess, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gio', '2.0')
    from gi.repository import Gtk, Gdk, Gio
    import os
    import subprocess
    from threading import Thread


    global Startup
    import Startup


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Startup - Startup Right Click Menu GUI Function -----------------------------------
def startup_menu_right_click_gui_func():

    # Define builder and get all objects (Startup tab right click menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupMenuRightClick.ui")

    # ********************** Define object names for Startup tab right click menu **********************
    global menu5101m
    global menuitem5102m, menuitem5103m, menuitem5105m, menuitem5106m, sub_menuitem5101m

    # ********************** Get object names for Startup tab right click menu **********************
    menu5101m = builder.get_object('menu5101m')
    menuitem5102m = builder.get_object('menuitem5102m')
    menuitem5103m = builder.get_object('menuitem5103m')
    menuitem5105m = builder.get_object('menuitem5105m')
    menuitem5106m = builder.get_object('menuitem5106m')
    sub_menuitem5101m = builder.get_object('sub_menuitem5101m')

    # ********************** Define object functions for Startup tab right click menu **********************
    def on_menuitem5102m_activate(widget):                                                    # "Add" item on the right click menu
        if 'StartupNewItem' not in globals():
            global StartupNewItem
            import StartupNewItem
            StartupNewItem.startup_new_item_import_func()
            StartupNewItem.startup_new_item_gui_func()
        StartupNewItem.window5101w.show()

    def on_menuitem5103m_activate(widget):                                                    # "Delete" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name
        selected_startup_application_exec_value = ""                                          # Initial value of "selected_startup_application_exec_value". This value will be used if it can not be get.
        with open(selected_startup_application_file_name) as reader:
            desktop_file_lines = reader.read().strip("").split("\n")
        for line in desktop_file_lines:
            if "Exec=" in line:
                selected_startup_application_exec_value = line.split("=")[1]
        message_text = _tr("Do you want to delete this startup item?")
        startup_delete_startup_item_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_exec_value)
        if warning_dialog5102_response == Gtk.ResponseType.YES:
            try:
                (subprocess.check_output(["rm", selected_startup_application_file_name], stderr=subprocess.STDOUT, shell=False)).decode()
            except Exception:
                pass
        if warning_dialog5102_response == Gtk.ResponseType.NO:
            return       

    def on_menuitem5106m_activate(widget):                                                    # "Run now" item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name
        selected_startup_application_exec_value = ""                                          # Initial value of "selected_startup_application_exec_value". This value will be used if it can not be get.
        with open(selected_startup_application_file_name) as reader:                          # Get content of the ".desktop" file in the system autostart directory
            desktop_file_system_lines = reader.read().strip("").split("\n")
        for line in desktop_file_system_lines:
            if "Exec=" in line:
                selected_startup_application_exec_value = line.split("=")[1]
        startup_run_startup_item_warning_dialog(selected_startup_application_name, selected_startup_application_exec_value)
        if warning_dialog5101_response == Gtk.ResponseType.YES:
            try:
                subprocess.Popen([selected_startup_application_exec_value], shell=False)      # Run the command of the startup item. If "Yes" is clicked. "shell=False" is used in order to prevent "shell injection" which may cause security problems.
            except FileNotFoundError:
                message_text = _tr("An error has been encountered while running the command.")
                startup_run_now_error_dialog(message_text, selected_startup_application_file_name, selected_startup_application_exec_value)
        if warning_dialog5101_response == Gtk.ResponseType.NO:
            return                                                                            # Do nothing (close the dialog) if "No" is clicked.

    def on_sub_menuitem5101m_activate(widget):                                                # "System-wide values file: " item on the right click menu
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')       # Get applications which support "text/plain" MIME type. This is MIME type of ".desktop" files. This code gives "default application list" in the order of "open with ..." applications list. Last used application is the first application but more investigation may be done for validity of this observation.
#         default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')     # Default application for the MIME type could be get. But it may give an application other than desired application for viewing/editing ".desktop" files if a text editor is not set default for this file.
        def open_file():                                                                      # Running action is performed in a separate thread for without waiting closing the new opened application.
           subprocess.call([default_app_list_for_content_type[0].get_executable(), selected_startup_application_file_name])    # Open the file with "0th" appliation in the list.
        try:
            open_file_thread = Thread(target=open_file, daemon=True).start()                  # Define a thread and run it
        except FileNotFoundError:
            pass


    # ********************** Connect signals to GUI objects for Startup tab right click menu **********************
    menuitem5102m.connect("activate", on_menuitem5102m_activate)
    menuitem5103m.connect("activate", on_menuitem5103m_activate)
    menuitem5106m.connect("activate", on_menuitem5106m_activate)
    sub_menuitem5101m.connect("activate", on_sub_menuitem5101m_activate)


# ----------------------------------- Startup - Set Menu Labels Function (sets widget sensitivity of "Remove" menuitem and widget sensitivity and labels (system-wide and user-specific .desktop file names) of sub-menu items of "Browse '.desktop' File..." menu item when right click operation is performed on startup item row on the treeview) -----------------------------------
def startup_set_menu_labels_func():

    selected_startup_application_file_name = Startup.selected_startup_application_file_name
    selected_startup_application_directory = selected_startup_application_file_name.rsplit("/", 1)[0] + "/"
    if selected_startup_application_directory == "/etc/xdg/autostart/":
        menuitem5103m.set_sensitive(False)
    else:
        menuitem5103m.set_sensitive(True)
    sub_menuitem5101m.set_label(selected_startup_application_file_name)


# ----------------------------------- Startup - Startup Run Startup Item Warning Dialog Function -----------------------------------
def startup_run_startup_item_warning_dialog(selected_startup_application_name, selected_startup_application_exec_value):

    warning_dialog5101 = Gtk.MessageDialog(transient_for=Startup.grid5101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to run this startup item now?"), )
    warning_dialog5101.format_secondary_text(_tr("Startup Item") + ": " + selected_startup_application_name +
                                             "\n" + _tr("Command") + ": " + selected_startup_application_exec_value)
    global warning_dialog5101_response
    warning_dialog5101_response = warning_dialog5101.run()
    warning_dialog5101.destroy()


# ----------------------------------- Startup - Startup Delete Startup Item Warning Dialog Function -----------------------------------
def startup_delete_startup_item_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_exec_value):

    warning_dialog5102 = Gtk.MessageDialog(transient_for=Startup.grid5101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=message_text, )
    warning_dialog5102.format_secondary_text(_tr("Startup Item") + ": " + selected_startup_application_name +
                                             "\n" + _tr("Command") + ": " + selected_startup_application_exec_value)
    global warning_dialog5102_response
    warning_dialog5102_response = warning_dialog5102.run()
    warning_dialog5102.destroy()


# ----------------------------------- Startup - Startup Run Now Error Dialog Function -----------------------------------
def startup_run_now_error_dialog(message_text, selected_startup_application_name, selected_startup_application_exec_value):

    error_dialog5101 = Gtk.MessageDialog(transient_for=Startup.grid5101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=message_text, )
    error_dialog5101.format_secondary_text(_tr("Startup Item") + ": " + selected_startup_application_name +
                                           "\n" + _tr("Command") + ": " + selected_startup_application_exec_value)
    error_dialog5101.run()
    error_dialog5101.destroy()
