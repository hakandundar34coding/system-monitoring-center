#! /usr/bin/python3

# ----------------------------------- RunApplication - RunApplication Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def run_application_import_func():

    global Gtk, Gdk, Gio, GdkPixbuf, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, Gio, GdkPixbuf
    import os


    global Config, RunApplicationGUI
    import Config, RunApplicationGUI


# ----------------------------------- RunApplication - RunApplication Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def run_application_func():

    global all_applications, application_name_list, application_icon_list, application_executable_list
    global pixbuf_for_no_icon_apps
    if RunApplicationGUI.window1001w.get_visible() == True:                                   # Hide and shown the window again if it is already visible. Thus "run program" window is brought front of the main window easily without using "wnck" module and codes which is relatively a more complex method.
        RunApplicationGUI.window1001w.hide()
        RunApplicationGUI.window1001w.show()
    if RunApplicationGUI.window1001w.get_visible() == False:
        RunApplicationGUI.window1001w.show()

    # Get applications, names, icons and executable lists by using Gio. Icons will be used when search text matches with an application name. Executable will be used for running the application.
    application_name_list = []
    application_icon_list = []
    application_executable_list = []
    all_applications = Gio.AppInfo.get_all()
    for application in all_applications:
        application_name_list.append(application.get_name())
        application_icon_list.append(application.get_icon())
        application_executable_list.append(application.get_executable())

    pixbuf_for_no_icon_apps = Gtk.IconTheme.get_default().load_icon("system-monitoring-center-search-symbolic", 48, 0)    # pixbuf will be used for displaying application icon on the window.

    # Treestore is used for search entry.
    treestore1001w = Gtk.TreeStore()
    treestore1001w.set_column_types([str])
    for i in range(len(application_name_list)):
        treestore1001w.append(None, [application_name_list[i]])

    # EntryCompletion and settings are defined
    entrycompletion1001w = Gtk.EntryCompletion()
    entrycompletion1001w.set_model(treestore1001w)
    entrycompletion1001w.set_text_column(0)
    entrycompletion1001w.set_inline_completion(True)
    entrycompletion1001w.set_inline_selection(True)
    RunApplicationGUI.searchentry1001w.set_completion(entrycompletion1001w)
