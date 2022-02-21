#!/usr/bin/env python3

# ----------------------------------- Startup - Startup New Item Window GUI Import Function -----------------------------------
def startup_new_item_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Startup
    import Startup


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Startup - Startup New Item Window GUI Function -----------------------------------
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
        button5102w.set_sensitive(False)

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
        # Get user-specific autostart application directory.
        current_user_home_directory = os.environ.get('HOME')
        current_user_autostart_directory = current_user_home_directory + "/.config/autostart/"

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

        # Show a warning dialog if there is already a .desktop file with the same name.
        if os.path.isfile(current_user_autostart_directory + new_startup_application_file_name) == True:
            startup_overwrite_existing_startup_item_warning_dialog(new_startup_application_name, new_startup_application_file_name)
            if warning_dialog5103_response == Gtk.ResponseType.YES:
                pass
            if warning_dialog5103_response == Gtk.ResponseType.NO:
                return
        # Save ".desktop" file in order to add new startup item
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
        window5101w.hide()


    # Startup New Item window GUI functions - connect
    window5101w.connect("delete-event", on_window5101w_delete_event)
    window5101w.connect("show", on_window5101w_show)
    entry5101w.connect("changed", on_entry5101w_changed)
    entry5103w.connect("changed", on_entry5103w_changed)
    button5101w.connect("clicked", on_button5101w_clicked)
    button5102w.connect("clicked", on_button5102w_clicked)


# ----------------------------------- Startup - Startup Overwrite Existing Startup Item Warning Dialog Function (shows a warning dialog when a new startup item file is tried to be generated with the same name of an existing one) -----------------------------------
def startup_overwrite_existing_startup_item_warning_dialog(new_startup_application_name, new_startup_application_file_name):

    warning_dialog5103 = Gtk.MessageDialog(transient_for=Startup.grid5101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to overwrite the existing file?"), )
    warning_dialog5103.format_secondary_text(_tr("There is already a '.desktop' file with the same name.") +
                                             "\n\n    " + _tr("Startup Item") + ": " + new_startup_application_name +
                                             "\n    " + _tr("'.desktop' File Name") + ": " + new_startup_application_file_name)
    global warning_dialog5103_response
    warning_dialog5103_response = warning_dialog5103.run()
    warning_dialog5103.destroy()
