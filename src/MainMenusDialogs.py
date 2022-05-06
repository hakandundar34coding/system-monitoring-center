#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Config import Config
from MainGUI import MainGUI


# Define class
class MainMenusDialogs:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainMenusDialogs.ui")

        # Get GUI objects
        self.popover1001p = builder.get_object('popover1001p')
        self.button1001p = builder.get_object('button1001p')
        self.button1002p = builder.get_object('button1002p')
        self.checkbutton1001p = builder.get_object('checkbutton1001p')
        self.aboutdialog1001d = builder.get_object('aboutdialog1001d')

        # Connect GUI signals
        self.popover1001p.connect("show", self.on_popover1001p_show)
        self.button1001p.connect("clicked", self.on_button1001p_clicked)
        self.button1002p.connect("clicked", self.on_button1002p_clicked)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1001p_show(self, widget):

        pass


    # ----------------------- "Settings" menu item -----------------------
    def on_button1001p_clicked(self, widget):

        self.popover1001p.hide()
        from SettingsGUI import SettingsGUI
        SettingsGUI.window2001.show()


    # ----------------------- "About" menu item -----------------------
    def on_button1002p_clicked(self, widget):

        self.popover1001p.hide()
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except Exception:
            pass
        self.aboutdialog1001d.set_version(software_version)
        self.aboutdialog1001d.set_transient_for(MainGUI.window1)
        self.aboutdialog1001d.run()
        self.aboutdialog1001d.hide()


# Generate object
MainMenusDialogs = MainMenusDialogs()

