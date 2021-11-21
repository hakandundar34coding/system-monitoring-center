#!/usr/bin/env python3

# ----------------------------------- MainMenusGUI - Main Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def main_menus_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config
    import Config

    global MainGUI
    import MainGUI


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- MainMenusGUI - Main Menus GUI Function (the code of this module in order to avoid running them during module import and defines GUI functions/signals) -----------------------------------
def main_menus_gui_func():

    # Define builder and get all objects (Main Menu GUI and About Dialog) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainMenusDialogs.ui")


    # ********************** Define object names for Main Menu GUI and About Dialog **********************
    global menu1001m
    global menuitem1002m, menuitem1003m, menuitem1004m, menuitem1005m, menuitem1006m, checkmenuitem1001m

    global aboutdialog1001d

    # ********************** Get objects for Main Menu GUI and About Dialog **********************
    menu1001m = builder.get_object('menu1001m')
    menuitem1002m = builder.get_object('menuitem1002m')
    menuitem1003m = builder.get_object('menuitem1003m')
    menuitem1004m = builder.get_object('menuitem1004m')
    menuitem1005m = builder.get_object('menuitem1005m')
    menuitem1006m = builder.get_object('menuitem1006m')
    checkmenuitem1001m = builder.get_object('checkmenuitem1001m')

    aboutdialog1001d = builder.get_object('aboutdialog1001d')


    # ********************** Define object functions for Main Menu GUI **********************
    def on_menu1001m_show(widget):
        checkmenuitem1001m.disconnect_by_func(on_checkmenuitem1001m_toggled)                  # Disconnect "on_checkmenuitem1001m_toggled" function in order to prevent it from sending event signals when toggling is performed by the code for reflecting the user preference about "Floating Window".
        if Config.show_floating_summary == 0:
            checkmenuitem1001m.set_active(False)
        if Config.show_floating_summary == 1:
            checkmenuitem1001m.set_active(True)
        checkmenuitem1001m.connect("toggled", on_checkmenuitem1001m_toggled)

    def on_menuitem1002m_activate(widget):                                                    # "Open Terminal" menu item
        if 'subprocess' not in globals():
            global subprocess
            import subprocess
        if 'Thread' not in globals():
            global Thread
            from threading import Thread
        def main_menus_gui_open_terminal_func():
            try:                                                                              # "try-catch" is used in order to avoid errors and show an error dialog to user if default terminal on the system can not be detected.
                (subprocess.call(["x-terminal-emulator"], shell=False))
            except:
                main_menus_gui_system_default_terminal_detection_error_dialog()
        open_terminal_thread = Thread(target=main_menus_gui_open_terminal_func, daemon=True).start()    # Terminal is run in another thread in order not to wait end of the run which occurs in single threaded code execution.

    def on_checkmenuitem1001m_toggled(widget):                                                # "Floating Summary" menu item
        if "FloatingSummary" not in globals():                                                # Floating Summary window might have been opened on the application start and user may want to hide it from the Main Menu of the application. Existance check of the "FloatingSummary" variable is performed before the "if checkmenuitem1001m.get_active() == False:" statement in order to avoid errors of FloatingSummary not defined.
            global FloatingSummary
            import FloatingSummary
        if checkmenuitem1001m.get_active() == True:
            FloatingSummary.floating_summary_import_func()
            FloatingSummary.floating_summary_gui_func()
            FloatingSummary.window3001.show()                                                 # Window has to be shown before running loop thread of the Floating Summary window. Because window visibility data is controlled to continue repeating "floating_summary_thread_run_func" function.
            FloatingSummary.floating_summary_thread_run_func()
            Config.show_floating_summary = 1
        if checkmenuitem1001m.get_active() == False:
            FloatingSummary.window3001.hide()
            Config.show_floating_summary = 0
        Config.config_save_func()

    def on_menuitem1003m_activate(widget):                                                    # "Restart as Root" menu item
        if 'signal' not in globals():
            global signal
            import signal
        if 'Thread' not in globals():
            global Thread
            from threading import Thread
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


    # ********************** Connect signals to GUI objects for Main Menu GUI **********************
    menu1001m.connect("show", on_menu1001m_show)
    menuitem1002m.connect("activate", on_menuitem1002m_activate)
    checkmenuitem1001m.connect("toggled", on_checkmenuitem1001m_toggled)
    menuitem1003m.connect("activate", on_menuitem1003m_activate)
    menuitem1004m.connect("activate", on_menuitem1004m_activate)
    menuitem1005m.connect("activate", on_menuitem1005m_activate)
    menuitem1006m.connect("activate", on_menuitem1006m_activate)


# ----------------------------------- MainMenusGUI - Main Menu GUI System Default Terminal Detection Error Dialog Function (shows a warning dialog when a startup item is tried to be reset to system default which means user specific desktop file of the startup application will be deleted (system-wide values file will be untouched)) -----------------------------------
def main_menus_gui_system_default_terminal_detection_error_dialog():

    error_dialog1001 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Default Terminal Application Not Detected"), )
    error_dialog1001.format_secondary_text(_tr("Default terminal application on this system could not be detected."))
    error_dialog1001.run()
    error_dialog1001.destroy()
