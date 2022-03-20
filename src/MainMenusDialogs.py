#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Config import Config


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
        self.button1003p = builder.get_object('button1003p')
        self.checkbutton1001p = builder.get_object('checkbutton1001p')
        self.aboutdialog1001d = builder.get_object('aboutdialog1001d')

        # Connect GUI signals
        self.popover1001p.connect("show", self.on_popover1001p_show)
        self.button1001p.connect("clicked", self.on_button1001p_clicked)
        self.button1002p.connect("clicked", self.on_button1002p_clicked)
        self.button1003p.connect("clicked", self.on_button1003p_clicked)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1001p_show(self, widget):

        if Config.show_floating_summary == 0:
            self.checkbutton1001p.set_active(False)
        # Do not use "if" here in order to avoid multiple "set_active" actions.
        else:
            self.checkbutton1001p.set_active(True)


    # ----------------------- "Floating Summary" menu item -----------------------
    def on_button1003p_clicked(self, widget):

        self.popover1001p.hide()
        from FloatingSummary import FloatingSummary
        if Config.show_floating_summary == 0:
            self.checkbutton1001p.set_active(True)
            # Window has to be shown before running loop thread of the Floating Summary window. Because window visibility data is controlled to continue repeating "floating_summary_thread_run_func" function.
            FloatingSummary.window3001.show()
            Config.show_floating_summary = 1
        else:
            self.checkbutton1001p.set_active(False)
            FloatingSummary.window3001.hide()
            Config.show_floating_summary = 0
        Config.config_save_func()


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
        self.aboutdialog1001d.run()
        self.aboutdialog1001d.hide()


# Generate object
MainMenusDialogs = MainMenusDialogs()

