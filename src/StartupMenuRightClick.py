#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Gio
import os
import subprocess
from threading import Thread

from locale import gettext as _tr

from Config import Config
import Startup


# Define class
class StartupMenuRightClick:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupMenuRightClick.ui")

        # Get GUI objects
        self.menu5101m = builder.get_object('menu5101m')
        self.menuitem5102m = builder.get_object('menuitem5102m')
        self.menuitem5103m = builder.get_object('menuitem5103m')
        self.menuitem5105m = builder.get_object('menuitem5105m')
        self.sub_menuitem5101m = builder.get_object('sub_menuitem5101m')

        # Connect GUI signals
        self.menuitem5102m.connect("activate", self.on_menuitem5102m_activate)
        self.menuitem5103m.connect("activate", self.on_menuitem5103m_activate)
        self.sub_menuitem5101m.connect("activate", self.on_sub_menuitem5101m_activate)


    # ----------------------- "Add" item -----------------------
    def on_menuitem5102m_activate(self, widget):

        from StartupNewItem import StartupNewItem
        StartupNewItem.window5101w.show()


    # ----------------------- "Delete" item -----------------------
    def on_menuitem5103m_activate(self, widget):

        # Get startup application file name and application name.
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_name = Startup.selected_startup_application_name

        # Get startup application exec value
        # Initial value of "selected_startup_application_exec_value". This value will be used if it can not be get.
        selected_startup_application_exec_value = ""
        with open(selected_startup_application_file_name) as reader:
            desktop_file_lines = reader.read().strip("").split("\n")
        for line in desktop_file_lines:
            if "Exec=" in line:
                selected_startup_application_exec_value = line.split("=")[1]

        # Show a warning dialog before deleting the startup item.
        message_text = _tr("Do you want to delete this startup item?")
        self.startup_warning_dialog(message_text, selected_startup_application_name, selected_startup_application_exec_value)
        if self.warning_dialog5101_response == Gtk.ResponseType.YES:
            try:
                (subprocess.check_output(["rm", selected_startup_application_file_name], stderr=subprocess.STDOUT, shell=False)).decode()
            except Exception:
                pass   


    # ----------------------- "Open .desktop File" item -----------------------
    def on_sub_menuitem5101m_activate(self, widget):

        # Get startup application file name.
        selected_startup_application_file_name = Startup.selected_startup_application_file_name

        # Get applications which support "text/plain" MIME type. This is MIME type of ".desktop" files. This code gives "default application list" in the order of "open with ..." applications list. Last used application is the first application.
        default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')

        # Default application for the MIME type could be get. But it may give an application other than desired application for viewing/editing ".desktop" files if a text editor is not set default for this file.
#         default_app_list_for_content_type = Gio.app_info_get_all_for_type('text/plain')

        # Running action is performed in a separate thread for without waiting closing the new opened application.
        def open_file():
            # Open the file with "0th" appliation in the list.
           subprocess.call([default_app_list_for_content_type[0].get_executable(), selected_startup_application_file_name])

        # Define a thread and run it
        try:
            open_file_thread = Thread(target=open_file, daemon=True).start()
        except FileNotFoundError:
            pass


    # ----------------------------------- Startup - Set Menu Labels Function (sets widget sensitivity of "Remove" menuitem and widget sensitivity and labels (system-wide and user-specific .desktop file names) of sub-menu items of "Browse '.desktop' File..." menu item when right click operation is performed on startup item row on the treeview) -----------------------------------
    def startup_set_menu_labels_func(self):

        # Get startup application file name and directory.
        selected_startup_application_file_name = Startup.selected_startup_application_file_name
        selected_startup_application_directory = selected_startup_application_file_name.rsplit("/", 1)[0] + "/"

        # Check if this is a user-specific startup item and set "Run" menu item as sensitive/insensitive.
        if selected_startup_application_directory == "/etc/xdg/autostart/":
            self.menuitem5103m.set_sensitive(False)
        else:
            self.menuitem5103m.set_sensitive(True)

        # Set menu item label by using startup item file path.
        self.sub_menuitem5101m.set_label(selected_startup_application_file_name)


    # ----------------------------------- Startup - Startup Run Startup Item Warning Dialog Function -----------------------------------
    def startup_warning_dialog(self, message_text, selected_startup_application_name, selected_startup_application_exec_value):

        warning_dialog5101 = Gtk.MessageDialog(transient_for=Startup.grid5101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.YES_NO, text=message_text)
        warning_dialog5101.format_secondary_text(_tr("Startup Item") + ": " + selected_startup_application_name +
                                                 "\n" + _tr("Command") + ": " + selected_startup_application_exec_value)
        self.warning_dialog5101_response = warning_dialog5101.run()
        warning_dialog5101.destroy()


# Generate object
StartupMenuRightClick = StartupMenuRightClick()

