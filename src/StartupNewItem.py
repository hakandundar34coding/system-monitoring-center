#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from locale import gettext as _tr

from Config import Config
import Startup


# Define class
class StartupNewItem:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder5101w = Gtk.Builder()
        builder5101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupNewItemWindow.ui")

        # Get GUI objects
        self.window5101w = builder5101w.get_object('window5101w')
        self.entry5101w = builder5101w.get_object('entry5101w')
        self.entry5102w = builder5101w.get_object('entry5102w')
        self.entry5103w = builder5101w.get_object('entry5103w')
        self.entry5104w = builder5101w.get_object('entry5104w')
        self.checkbutton5101w = builder5101w.get_object('checkbutton5101w')
        self.checkbutton5102w = builder5101w.get_object('checkbutton5102w')
        self.button5101w = builder5101w.get_object('button5101w')
        self.button5102w = builder5101w.get_object('button5102w')

        # Connect GUI signals
        self.window5101w.connect("delete-event", self.on_window5101w_delete_event)
        self.window5101w.connect("show", self.on_window5101w_show)
        self.entry5101w.connect("changed", self.on_name_command_entries_changed)
        self.entry5103w.connect("changed", self.on_name_command_entries_changed)
        self.button5101w.connect("clicked", self.on_button5101w_clicked)
        self.button5102w.connect("clicked", self.on_button5102w_clicked)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window5101w_delete_event(self, widget, event):

        self.window5101w.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window5101w_show(self, widget):

        # Reset GUI
        self.entry5101w.set_text("")
        self.entry5102w.set_text("")
        self.entry5103w.set_text("")
        self.entry5104w.set_text("")
        self.checkbutton5101w.set_active(False)
        self.checkbutton5102w.set_active(False)
        self.button5102w.set_sensitive(False)


    # ----------------------- Called for setting sensitivity of the "Save" button as "False" if "Name" and "Command" entries are empty. -----------------------
    def on_name_command_entries_changed(self, widget):

        if self.entry5101w.get_text() == "" or self.entry5103w.get_text() == "":
            self.button5102w.set_sensitive(False)
        if self.entry5101w.get_text() != "" and self.entry5103w.get_text() != "":
            self.button5102w.set_sensitive(True)


    # ----------------------- "Cancel" Button -----------------------
    def on_button5101w_clicked(self, widget):

        self.window5101w.hide()


    # ----------------------- "Save" Button -----------------------
    def on_button5102w_clicked(self, widget):

        # Get user-specific autostart application directory.
        current_user_home_directory = os.environ.get('HOME')
        current_user_autostart_directory = current_user_home_directory + "/.config/autostart/"

        # Get startup item infomation from the GUI.
        new_startup_application_name = self.entry5101w.get_text()
        new_startup_application_file_name = self.entry5101w.get_text() + ".desktop"
        new_startup_application_comment = self.entry5102w.get_text()
        new_startup_application_command = self.entry5103w.get_text()
        new_startup_application_icon = self.entry5104w.get_text()
        if self.checkbutton5101w.get_active() == True:
            new_startup_application_startup_notify = "True"
        else:
            new_startup_application_startup_notify = "False"
        if self.checkbutton5102w.get_active() == True:
            new_startup_application_terminal = "True"
        else:
            new_startup_application_terminal = "False"

        # Show a warning dialog if there is already a .desktop file with the same name.
        if os.path.isfile(current_user_autostart_directory + new_startup_application_file_name) == True:
            self.startup_overwrite_existing_startup_item_warning_dialog(new_startup_application_name, new_startup_application_file_name)
            if warning_dialog5102_response != Gtk.ResponseType.YES:
                return

        # Save ".desktop" file in order to add the new startup item
        with open(current_user_autostart_directory + new_startup_application_name + ".desktop", "w") as writer:
            writer.write("[Desktop Entry]" + "\n")
            writer.write("Type=Application" + "\n")
            writer.write("Name=" + new_startup_application_name + "\n")
            if new_startup_application_comment != "":
                writer.write("Comment=" + new_startup_application_comment + "\n")
            writer.write("Exec=" + new_startup_application_command + "\n")
            if new_startup_application_icon != "":
                writer.write("Icon=" + new_startup_application_icon + "\n")
            if new_startup_application_startup_notify == "True":
                writer.write("StartupNotify=true" + "\n")
            if new_startup_application_startup_notify == "False":
                writer.write("StartupNotify=false" + "\n")
            if new_startup_application_terminal == "True":
                writer.write("Terminal=true" + "\n")
            if new_startup_application_terminal == "False":
                writer.write("Terminal=false" + "\n")

        self.window5101w.hide()


    # ----------------------------------- Startup - Startup Overwrite Existing Startup Item Warning Dialog Function (shows a warning dialog when a new startup item file is tried to be generated with the same name of an existing one) -----------------------------------
    def startup_overwrite_existing_startup_item_warning_dialog(self, new_startup_application_name, new_startup_application_file_name):

        warning_dialog5102 = Gtk.MessageDialog(transient_for=Startup.grid5101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to overwrite the existing file?"))
        warning_dialog5102.format_secondary_text(_tr("There is already a '.desktop' file with the same name.") +
                                                 "\n\n    " + _tr("Startup Item") + ": " + new_startup_application_name +
                                                 "\n    " + _tr("File") + ": " + new_startup_application_file_name)
        self.warning_dialog5102_response = warning_dialog5102.run()
        warning_dialog5102.destroy()


# Generate object
StartupNewItem = StartupNewItem()

