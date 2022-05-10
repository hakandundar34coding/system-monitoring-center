#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
import Users


# Define class
class UsersMenuRightClick:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenuRightClick.ui")

        # Get GUI objects
        self.menu3101m = builder.get_object('menu3101m')
        self.menuitem3102m = builder.get_object('menuitem3102m')

        # Connect GUI signals
        self.menuitem3102m.connect("activate", self.on_menuitem3102m_activate)


    # ----------------------- "Details" item -----------------------
    def on_menuitem3102m_activate(self, widget):

        from UsersDetails import UsersDetails
        UsersDetails.window3101w.show()


# Generate object
UsersMenuRightClick = UsersMenuRightClick()

