#!/usr/bin/env python3

# ----------------------------------- MainMenusGUI - Main Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def main_menus_gui_import_func():

    global Gtk, os, signal, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import signal
    from threading import Thread


    global Config, MainGUI
    import Config, MainGUI


# ----------------------------------- MainMenusGUI - Main Menus GUI Function (the code of this module in order to avoid running them during module import and defines GUI functions/signals) -----------------------------------
def main_menus_gui_func():

    global builder1001
    global menu1001m

    global aboutdialog1001d


    builder1001 = Gtk.Builder()
    builder1001.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainMenusDialogs.ui")

    menu1001m = builder1001.get_object('menu1001m')
    menuitem1002m = builder1001.get_object('menuitem1002m')
    menuitem1003m = builder1001.get_object('menuitem1003m')
    menuitem1004m = builder1001.get_object('menuitem1004m')
    menuitem1005m = builder1001.get_object('menuitem1005m')
    menuitem1006m = builder1001.get_object('menuitem1006m')
    checkmenuitem1001m = builder1001.get_object('checkmenuitem1001m')


    builder1001d = Gtk.Builder()
    builder1001d.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainMenusDialogs.ui")
    aboutdialog1001d = builder1001d.get_object('aboutdialog1001d')


    def on_menu1001m_show(widget):
        checkmenuitem1001m.disconnect_by_func(on_checkmenuitem1001m_toggled)                  # Disconnect "on_checkmenuitem1001m_toggled" function in order to prevent it from sending event signals when toggling is performed by the code for reflecting the user preference about "Floating Window".
        if Config.show_floating_summary == 0:
            checkmenuitem1001m.set_active(False)
        if Config.show_floating_summary == 1:
            checkmenuitem1001m.set_active(True)
        checkmenuitem1001m.connect("toggled", on_checkmenuitem1001m_toggled)

    def on_menuitem1002m_activate(widget):                                                    # "Open Terminal" menu item
        open_terminal_thread = Thread(target=main_menus_gui_open_terminal_func, daemon=True).start()    # Terminal is run in another thread in order not to wait end of the run which occurs in single threaded code execution.

    def on_checkmenuitem1001m_toggled(widget):                                                # "Floating Summary" menu item
        if "FloatingSummary" not in globals():                                                # Floating Summary window might have been opened on the application start and user may want to hide it from the Main Menu of the application. Existance check of the "FloatingSummary" variable is performed before the "if checkmenuitem1001m.get_active() == False:" statement in order to avoid errors of FloatingSummary not defined.
            global FloatingSummary
            import FloatingSummary
        if checkmenuitem1001m.get_active() == True:
            FloatingSummary.floating_summary_import_func()
            FloatingSummary.floating_summary_initial_func()
            FloatingSummary.floating_summary_thread_run_func()
            FloatingSummary.floating_summary_window.show()
            Config.show_floating_summary = 1
        if checkmenuitem1001m.get_active() == False:
            FloatingSummary.floating_summary_window.hide()
            Config.show_floating_summary = 0
        Config.config_save_func()

    def on_menuitem1003m_activate(widget):                                                    # "Restart as Root" menu item
        def restart_as_root():                                                                # Running action is performed in a separate thread for letting rest of the function code to be run without waiting closing the new opened application.
           os.system("pkexec system-monitoring-center")                                       # For running application as root by using polkit authentication window 
        restart_as_root_thread = Thread(target=restart_as_root, daemon=True).start()          # Define a thread and run it
        os.kill(os.getpid(), signal.SIGTERM)                                                  # Get PID of the current application and end it

    def on_menuitem1004m_activate(widget):                                                    # "Settings" menu item
        if "SettingsGUI" not in globals():                                                    # Settings module is imported and the following functions are run only one time during application run. This statement is used in order to avoid them running on every window opening.
            global SettingsGUI
            import SettingsGUI
            SettingsGUI.settings_gui_import_func()
            SettingsGUI.settings_gui_func()
        SettingsGUI.window2001.show()

    def on_menuitem1005m_activate(widget):                                                    # "About" menu item
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except:
            pass
        aboutdialog1001d.set_version(software_version)
        aboutdialog1001d.run()
        aboutdialog1001d.hide()

    def on_menuitem1006m_activate(widget):                                                    # "Quit" menu item
        Gtk.main_quit()



    menu1001m.connect("show", on_menu1001m_show)
    menuitem1002m.connect("activate", on_menuitem1002m_activate)
    checkmenuitem1001m.connect("toggled", on_checkmenuitem1001m_toggled)
    menuitem1003m.connect("activate", on_menuitem1003m_activate)
    menuitem1004m.connect("activate", on_menuitem1004m_activate)
    menuitem1005m.connect("activate", on_menuitem1005m_activate)
    menuitem1006m.connect("activate", on_menuitem1006m_activate)


def main_menus_gui_open_terminal_func():
    os.system("x-terminal-emulator -e /bin/bash")
