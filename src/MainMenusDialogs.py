#!/usr/bin/env python3

# ----------------------------------- MainMenusGUI - Main Menus GUI Import Function -----------------------------------
def main_menus_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config
    import Config


# ----------------------------------- MainMenusGUI - Main Menus GUI Function -----------------------------------
def main_menus_gui_func():

    # Define builder and get all objects (Main Menu GUI and About Dialog) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainMenusDialogs.ui")


    # ********************** Define object names for Main Menu GUI and About Dialog **********************
    global popover1001p
    global button1001p, button1002p, button1003p, checkbutton1001p

    global aboutdialog1001d

    # ********************** Get objects for Main Menu GUI and About Dialog **********************
    popover1001p = builder.get_object('popover1001p')
    button1001p = builder.get_object('button1001p')
    button1002p = builder.get_object('button1002p')
    button1003p = builder.get_object('button1003p')
    checkbutton1001p = builder.get_object('checkbutton1001p')

    aboutdialog1001d = builder.get_object('aboutdialog1001d')


    # ********************** Define object functions for Main Menu GUI **********************
    def on_popover1001p_show(widget):                                                         # On popover show
        if Config.show_floating_summary == 0:
            checkbutton1001p.set_active(False)
        else:                                                                                 # Do not use "if" here in order to avoid multiple "set_active" actions.
            checkbutton1001p.set_active(True)

    def on_button1003p_clicked(widget):                                                       # "Floating Summary" menu item
        popover1001p.hide()
        if "FloatingSummary" not in globals():                                                # Floating Summary window might have been opened on the application start and user may want to hide it from the Main Menu of the application. Existance check of the "FloatingSummary" variable is performed before the "if checkbutton1001p.get_active() == False:" statement in order to avoid errors of FloatingSummary not defined.
            global FloatingSummary
            import FloatingSummary
        if Config.show_floating_summary == 0:
            checkbutton1001p.set_active(True)
            FloatingSummary.floating_summary_import_func()
            FloatingSummary.floating_summary_gui_func()
            FloatingSummary.window3001.show()                                                 # Window has to be shown before running loop thread of the Floating Summary window. Because window visibility data is controlled to continue repeating "floating_summary_thread_run_func" function.
            FloatingSummary.floating_summary_run_func()
            Config.show_floating_summary = 1
        else:
            checkbutton1001p.set_active(False)
            FloatingSummary.window3001.hide()
            Config.show_floating_summary = 0
        Config.config_save_func()

    def on_button1001p_clicked(widget):                                                       # "Settings" menu item
        popover1001p.hide()
        if "SettingsGUI" not in globals():                                                    # Settings module is imported and the following functions are run only one time during application run. This statement is used in order to avoid them running on every window opening.
            global SettingsGUI
            import SettingsGUI
            SettingsGUI.settings_gui_import_func()
            SettingsGUI.settings_gui_func()
        SettingsGUI.window2001.show()

    def on_button1002p_clicked(widget):                                                       # "About" menu item
        popover1001p.hide()
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except Exception:
            pass
        aboutdialog1001d.set_version(software_version)
        aboutdialog1001d.run()
        aboutdialog1001d.hide()


    # ********************** Connect signals to GUI objects for Main Menu GUI **********************
    popover1001p.connect("show", on_popover1001p_show)
    button1001p.connect("clicked", on_button1001p_clicked)
    button1002p.connect("clicked", on_button1002p_clicked)
    button1003p.connect("clicked", on_button1003p_clicked)
