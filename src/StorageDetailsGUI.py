#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Details Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_details_gui_import_function():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


# ----------------------------------- Storage - Storage Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Storage Details" window GUI objects and functions/signals) -----------------------------------
def storage_details_gui_function():

    # Storage Details window GUI objects
    global builder4101w, window4101w
    global label4101w, label4102w, label4103w, label4104w, label4105w, label4106w, label4107w, label4108w, label4109w, label4110w
    global label4111w, label4112w, label4113w, label4114w, label4115w, label4116w, label4117w, label4118w, label4119w, label4120w
    global label4121w, label4122w, label4123w, label4124w


    # Storage Details window GUI objects - get
    builder4101w = Gtk.Builder()
    builder4101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageDetailsWindow.ui")

    window4101w = builder4101w.get_object('window4101w')


    # Storage Details window GUI objects
    label4101w = builder4101w.get_object('label4101w')
    label4102w = builder4101w.get_object('label4102w')
    label4103w = builder4101w.get_object('label4103w')
    label4104w = builder4101w.get_object('label4104w')
    label4105w = builder4101w.get_object('label4105w')
    label4106w = builder4101w.get_object('label4106w')
    label4107w = builder4101w.get_object('label4107w')
    label4108w = builder4101w.get_object('label4108w')
    label4109w = builder4101w.get_object('label4109w')
    label4110w = builder4101w.get_object('label4110w')
    label4111w = builder4101w.get_object('label4111w')
    label4112w = builder4101w.get_object('label4112w')
    label4113w = builder4101w.get_object('label4113w')
    label4114w = builder4101w.get_object('label4114w')
    label4115w = builder4101w.get_object('label4115w')
    label4116w = builder4101w.get_object('label4116w')
    label4117w = builder4101w.get_object('label4117w')
    label4118w = builder4101w.get_object('label4118w')
    label4119w = builder4101w.get_object('label4119w')
    label4120w = builder4101w.get_object('label4120w')
    label4121w = builder4101w.get_object('label4121w')
    label4122w = builder4101w.get_object('label4122w')
    label4123w = builder4101w.get_object('label4123w')
    label4124w = builder4101w.get_object('label4124w')


    # Storage Details window GUI functions
    def on_window4101w_delete_event(widget, event):
        window4101w.hide()
        return True

    def on_window4101w_show(widget):
        storage_details_gui_reset_function()    # Call this function in order to reset Storage Details window. Data from previous storage/disk remains visible (for a short time) until getting and showing new storage/disk data if window is closed and opened for an another storage/disk because window is made hidden when close button is clicked.


    # Storage Details window GUI functions - connect
    window4101w.connect("delete-event", on_window4101w_delete_event)
    window4101w.connect("show", on_window4101w_show)


# ----------------------------------- Storage - Storage Details Window GUI Reset Function (resets Storage Details window) -----------------------------------
def storage_details_gui_reset_function():
    label4101w.set_text("--")
    label4102w.set_text("--")
    label4103w.set_text("--")
    label4104w.set_text("--")
    label4105w.set_text("--")
    label4106w.set_text("--")
    label4107w.set_text("--")
    label4108w.set_text("--")
    label4109w.set_text("--")
    label4110w.set_text("--")
    label4111w.set_text("--")
    label4112w.set_text("--")
    label4113w.set_text("--")
    label4114w.set_text("--")
    label4115w.set_text("--")
    label4116w.set_text("--")
    label4117w.set_text("--")
    label4118w.set_text("--")
    label4119w.set_text("--")
    label4120w.set_text("--")
    label4121w.set_text("--")
    label4122w.set_text("--")
    label4123w.set_text("--")
    label4124w.set_text("--")
