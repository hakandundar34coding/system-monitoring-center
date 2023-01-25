#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Config import Config
from MainGUI import MainGUI


class MainMenusDialogs:

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

        # Get software version
        self.popover1001p.hide()
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except Exception:
            pass

        # Define translators dictionary
        translators_dict = {"cs": "panmourovaty",
                           "de": "Baumfinder",
                           "es": "haggen88",
                           "fa": "MasterKia",
                           "fr": "Metoto Sakamoto",
                           "hu": "Kálmán Szalai",
                           "pl": "ski007, K0RR, sdorpl",
                           "pt_BR": "Bruno do Nascimento",
                           "pt_PT": "Hugo Carvalho, Ricardo Simões",
                           "ru_RU": "badcast, akorny",
                           "tr": "Hakan Dündar"
                           }

        # Get GUI language for getting translator name
        application_language = Config.language
        if application_language == "system":
            application_language = os.environ.get("LANG")
        application_language_code = application_language.split(".")[0]
        application_language_code_split = application_language_code.split("_")[0]

        # Define translators list
        try:
            translators = '\n'.join(translators_dict[application_language_code].split(", "))
        except Exception:
            try:
                translators = '\n'.join(translators_dict[application_language_code_split].split(", "))
            except Exception:
                translators = "-"

        self.aboutdialog1001d.set_version(software_version)
        self.aboutdialog1001d.set_translator_credits(translators)
        self.aboutdialog1001d.set_transient_for(MainGUI.window1)
        self.aboutdialog1001d.run()
        self.aboutdialog1001d.hide()


MainMenusDialogs = MainMenusDialogs()

