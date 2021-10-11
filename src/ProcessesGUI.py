#!/usr/bin/env python3

# ----------------------------------- Processes - Processes GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_gui_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global Config, MainGUI, Processes
    import Config, MainGUI, Processes


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


# ----------------------------------- Processes - Processes GUI Function (the code of this module in order to avoid running them during module import and defines "Processes" tab GUI objects and functions/signals) -----------------------------------
def processes_gui_func():

    # Processes tab GUI objects
    global grid2101, treeview2101, searchentry2101, button2101, button2102
    global radiobutton2101, radiobutton2102, radiobutton2103, radiobutton2104, radiobutton2105, radiobutton2106
    global label2101


    # Processes tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesTab.ui")

    # Processes tab GUI objects - get
    grid2101 = builder.get_object('grid2101')
    treeview2101 = builder.get_object('treeview2101')
    searchentry2101 = builder.get_object('searchentry2101')
    button2101 = builder.get_object('button2101')
    button2102 = builder.get_object('button2102')
    radiobutton2101 = builder.get_object('radiobutton2101')
    radiobutton2102 = builder.get_object('radiobutton2102')
    radiobutton2103 = builder.get_object('radiobutton2103')
    radiobutton2104 = builder.get_object('radiobutton2104')
    radiobutton2105 = builder.get_object('radiobutton2105')
    radiobutton2106 = builder.get_object('radiobutton2106')
    label2101 = builder.get_object('label2101')


    # Processes tab GUI functions
    def on_treeview2101_button_press_event(widget, event):
        if event.button == 3:                                                                 # Open Processes tab right click menu if mouse is right clicked on the treeview (and on any process, otherwise menu will not be shown) and the mouse button is pressed.
            processes_open_right_click_menu_func(event)
        if event.type == Gdk.EventType._2BUTTON_PRESS:                                        # Open Process Details window if double click is performed.
            processes_open_process_details_window_func(event)

    def on_treeview2101_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Processes.processes_treeview_column_order_width_row_sorting_func()

    def on_searchentry2101_changed(widget):
        radiobutton2101.set_active(True)
        radiobutton2104.set_active(True)
        Processes.processes_treeview_filter_search_func()

    def on_button2101_clicked(widget):                                                        # "Processes Tab Customizations" button
        if 'ProcessesMenuCustomizationsGUI' not in globals():                                 # Check if "ProcessesMenuCustomizationsGUI" module is imported. Therefore it is not reimported on every right click operation.
            global ProcessesMenuCustomizationsGUI
            import ProcessesMenuCustomizationsGUI
            ProcessesMenuCustomizationsGUI.processes_menu_customizations_import_func()
            ProcessesMenuCustomizationsGUI.processes_menu_customizations_gui_func()
        ProcessesMenuCustomizationsGUI.popover2101p.popup()

    def on_button2102_clicked(widget):                                                        # "Define a window by clicking on it and highlight its process" button
        Processes.processes_define_window_func()

    def on_radiobutton2101_toggled(widget):                                                   # "Show all processes" radiobutton
        if radiobutton2101.get_active() == True:
            searchentry2101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            Processes.processes_treeview_filter_show_all_func()
            radiobutton2104.set_active(True)

    def on_radiobutton2102_toggled(widget):                                                   # "Show processes from this user" radiobutton
        if radiobutton2102.get_active() == True:
            searchentry2101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            Processes.processes_treeview_filter_show_all_func()
            Processes.processes_treeview_filter_this_user_only_func()
            radiobutton2104.set_active(True)

    def on_radiobutton2103_toggled(widget):                                                   # "Show processes from other users" radiobutton
        if radiobutton2103.get_active() == True:
            searchentry2101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            Processes.processes_treeview_filter_show_all_func()
            Processes.processes_treeview_filter_other_users_only_func()
            radiobutton2104.set_active(True)

    def on_radiobutton2104_toggled(widget):                                                   # "User defined expand" radiobutton
        if radiobutton2104.get_active() == True:
            pass

    def on_radiobutton2105_toggled(widget):                                                   # "Expand all" radiobutton
        if radiobutton2105.get_active() == True:
            treeview2101.expand_all()

    def on_radiobutton2106_toggled(widget):                                                   # "Collapse all" radiobutton
        if radiobutton2106.get_active() == True:
            treeview2101.collapse_all()


    # Processes tab GUI functions - connect
    treeview2101.connect("button-press-event", on_treeview2101_button_press_event)
    treeview2101.connect("button-release-event", on_treeview2101_button_release_event)
    searchentry2101.connect("changed", on_searchentry2101_changed)
    button2101.connect("clicked", on_button2101_clicked)
    button2102.connect("clicked", on_button2102_clicked)
    radiobutton2101.connect("toggled", on_radiobutton2101_toggled)
    radiobutton2102.connect("toggled", on_radiobutton2102_toggled)
    radiobutton2103.connect("toggled", on_radiobutton2103_toggled)
    radiobutton2104.connect("toggled", on_radiobutton2104_toggled)
    radiobutton2105.connect("toggled", on_radiobutton2105_toggled)
    radiobutton2106.connect("toggled", on_radiobutton2106_toggled)


    # Processes Tab - Treeview Properties
    treeview2101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview2101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview2101.set_headers_clickable(True)
    treeview2101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview2101.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview2101.set_tooltip_column(2)


    # Set "User defined expand, Expand all, Collapse all" buttons as "insensitive" on the Processes tab if "show_processes_as_tree" option is disabled. Because expanding/collapsing treeview rows has no effects when treeview items are listed as "list". Also change widget tooltips for better understandability
    if Config.show_processes_as_tree == 1:
        radiobutton2104.set_sensitive(True)
        radiobutton2105.set_sensitive(True)
        radiobutton2106.set_sensitive(True)
        radiobutton2104.set_tooltip_text(_tr("User defined expand"))
        radiobutton2105.set_tooltip_text(_tr("Expand all"))
        radiobutton2106.set_tooltip_text(_tr("Collapse all"))

    # Set "User defined expand, Expand all, Collapse all" buttons as "sensitive" on the Processes tab if "show_processes_as_tree" option is enabled. Therefore, expanding/collapsing treeview rows functions will be available for using by the user. Also change widget tooltips for better understandability
    if Config.show_processes_as_tree == 0:
        radiobutton2104.set_sensitive(False)
        radiobutton2105.set_sensitive(False)
        radiobutton2106.set_sensitive(False)
        radiobutton2104.set_tooltip_text(_tr("User defined expand\n(Usable if processes are listed as tree)"))
        radiobutton2105.set_tooltip_text(_tr("Expand all\n(Usable if processes are listed as tree)"))
        radiobutton2106.set_tooltip_text(_tr("Collapse all\n(Usable if processes are listed as tree)"))


# ----------------------------------- Processes - Open Right Click Menu Function (gets right clicked process PID and opens right click menu) -----------------------------------
def processes_open_right_click_menu_func(event):

    try:                                                                                      # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview2101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview2101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is None:
        processes_no_process_selected_dialog()
    if treeiter is not None:
        global selected_process_pid
        try:
            selected_process_pid = Processes.pid_list[Processes.processes_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "processes_data_rows" list to use it getting pid of the process.
        except ValueError:                                                                    # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'asush', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely. It is handled in this situation.
            print("not in list error")
            return
        if 'ProcessesMenuRightClickGUI' not in globals():                                     # Check if "ProcessesMenuRightClickGUI" module is imported. Therefore it is not reimported on every right click operation.
            global ProcessesMenuRightClickGUI
            import ProcessesMenuRightClickGUI
            ProcessesMenuRightClickGUI.processes_menu_right_click_import_func()
            ProcessesMenuRightClickGUI.processes_menu_right_click_gui_func()
        ProcessesMenuRightClickGUI.menu2101m.popup(None, None, None, None, event.button, event.time)
        ProcessesMenuRightClickGUI.processes_select_process_nice_option_func()


# ----------------------------------- Processes - Open Process Details Window Function (gets double clicked process PID and opens Process Details window) -----------------------------------
def processes_open_process_details_window_func(event):

    try:                                                                                      # "try-except" is used in order to prevent errors when double clicked on an empty area on the treeview.
        path, _, _, _ = treeview2101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview2101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is None:
        processes_no_process_selected_dialog()
    if treeiter is not None:
        global selected_process_pid
        try:
            selected_process_pid = Processes.pid_list[Processes.processes_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "processes_data_rows" list to use it getting pid of the process.
        except ValueError:                                                                    # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'asush', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely. It is handled in this situation.
            print("not in list error")
            return
        # Open Process Details window
        if 'ProcessesDetailsGUI' not in globals():                                            # Check if "ProcessesDetailsGUI" module is imported. Therefore it is not reimported for every double click on any process on the treeview if "ProcessesDetailsGUI" name is in globals().
            global ProcessesDetailsGUI, ProcessesDetails
            import ProcessesDetailsGUI, ProcessesDetails
            ProcessesDetailsGUI.processes_details_gui_import_function()
            ProcessesDetailsGUI.processes_details_gui_function()
            ProcessesDetails.processes_details_import_func()
        ProcessesDetailsGUI.window2101w.show()
        ProcessesDetails.process_details_foreground_thread_run_func()


# ----------------------------------- Processes - No Process Selected Dialog Function (shows a dialog when Open Process Right Click Menu is clicked without selecting a process) -----------------------------------
def processes_no_process_selected_dialog():

    dialog2101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Select A Process"), )
    dialog2101.format_secondary_text(_tr("Please select a process and try again for opening the menu"))
    dialog2101.run()
    dialog2101.destroy()
