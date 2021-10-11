#!/usr/bin/env python3

# ----------------------------------- Startup - Startup GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def startup_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global MainGUI, Startup
    import MainGUI, Startup


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


# ----------------------------------- Startup - Startup GUI Function (the code of this module in order to avoid running them during module import and defines "Startup" tab GUI objects and functions/signals) -----------------------------------
def startup_gui_func():

    global grid5101, treeview5101, searchentry5101, button5101
    global radiobutton5101, radiobutton5102, radiobutton5103
    global label5101


    # Startup tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupTab.ui")

    # Startup tab GUI objects - get
    grid5101 = builder.get_object('grid5101')
    treeview5101 = builder.get_object('treeview5101')
    searchentry5101 = builder.get_object('searchentry5101')
    button5101 = builder.get_object('button5101')
    radiobutton5101 = builder.get_object('radiobutton5101')
    radiobutton5102 = builder.get_object('radiobutton5102')
    radiobutton5103 = builder.get_object('radiobutton5103')
    label5101 = builder.get_object('label5101')


    # Startup tab GUI functions
    def on_treeview5101_button_press_event(widget, event):                                    # Mouse button press event (on the treeview)
        if event.button == 3:                                                                 # Open Startup tab right click menu if mouse is right clicked on the treeview (and on any disk, otherwise menu will not be shown) and the mouse button is pressed.
            startup_open_right_click_menu_func(event)

    def on_treeview5101_button_release_event(widget, event):                                  # Mouse button press event (on the treeview)
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Startup.startup_treeview_column_order_width_row_sorting_func()

    def on_searchentry5101_changed(widget):
        radiobutton5101.set_active(True)
        Startup.startup_treeview_filter_search_func()

    def on_button5101_clicked(widget):                                                        # "Startup Tab Customizations" button
        if 'StartupMenuCustomizationsGUI' not in globals():                                   # Check if "StartupMenuCustomizationsGUI" module is imported. Therefore it is not reimported on every right click operation.
            global StartupMenuCustomizationsGUI
            import StartupMenuCustomizationsGUI
            StartupMenuCustomizationsGUI.startup_menu_customizations_import_func()
            StartupMenuCustomizationsGUI.startup_menu_customizations_gui_func()
        StartupMenuCustomizationsGUI.popover5101p.popup()

    def on_radiobutton5101_toggled(widget):                                                   # "Show all startup items" radiobutton
        if radiobutton5101.get_active() == True:
            searchentry5101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            Startup.startup_treeview_filter_show_all_func()

    def on_radiobutton5102_toggled(widget):                                                   # "Show all enabled (visible) startup items" radiobutton
        if radiobutton5102.get_active() == True:
            searchentry5101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            Startup.startup_treeview_filter_show_all_func()
            Startup.startup_treeview_filter_startup_visible_only()

    def on_radiobutton5103_toggled(widget):                                                   # "Show all disabled (hidden) startup items" radiobutton
        if radiobutton5103.get_active() == True:
            searchentry5101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            Startup.startup_treeview_filter_show_all_func()
            Startup.startup_treeview_filter_startup_hidden_only()



    # Startup tab GUI functions - connect
    treeview5101.connect("button-press-event", on_treeview5101_button_press_event)
    treeview5101.connect("button-release-event", on_treeview5101_button_release_event)
    searchentry5101.connect("changed", on_searchentry5101_changed)
    button5101.connect("clicked", on_button5101_clicked)
    radiobutton5101.connect("toggled", on_radiobutton5101_toggled)
    radiobutton5102.connect("toggled", on_radiobutton5102_toggled)
    radiobutton5103.connect("toggled", on_radiobutton5103_toggled)


    # Startup Tab - Treeview Properties
    treeview5101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview5101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview5101.set_headers_clickable(True)
    treeview5101.set_show_expanders(False)
    treeview5101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview5101.set_search_column(3)                                                         # This command used for searching by using entry.
    treeview5101.set_tooltip_column(3)


# ----------------------------------- ProceStartupsses - Open Right Click Menu Function (gets right clicked startup application file name and opens right click menu) -----------------------------------
def startup_open_right_click_menu_func(event):

    global model, treeiter
    try:                                                                                      # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview5101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview5101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is None:
        startup_no_startup_item_selected_dialog()
    if treeiter is not None:
        global selected_startup_application_file_name, selected_startup_application_visibility, selected_startup_application_name
        selected_startup_application_file_name = Startup.all_autostart_applications_list[Startup.startup_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "startup_data_rows" list to use it getting name of the startup application file name.
        selected_startup_application_visibility = Startup.startup_applications_visibility_list[Startup.startup_data_rows.index(model[treeiter][:])]
        selected_startup_application_name = model[treeiter][3]
        if 'StartupMenuRightClickGUI' not in globals():                                       # Check if "StartupMenuRightClickGUI" module is imported. Therefore it is not reimported on every right click operation.
            global StartupMenuRightClickGUI
            import StartupMenuRightClickGUI
            StartupMenuRightClickGUI.startup_menu_right_click_import_func()
            StartupMenuRightClickGUI.startup_menu_right_click_gui_func()
        StartupMenuRightClickGUI.menu5101m.popup(None, None, None, None, event.button, event.time)
        StartupMenuRightClickGUI.startup_set_checkmenuitem_func()
        StartupMenuRightClickGUI.startup_set_menu_labels_func()


# ----------------------------------- Startup - No Startup Item Selected Dialog Function (shows a dialog when Open Startup Item Right Click Menu is clicked without selecting a startup item) -----------------------------------
def startup_no_startup_item_selected_dialog():

    dialog5101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Select A Startup Item"), )
    dialog5101.format_secondary_text(_tr("Please select a startup item and try again for opening the menu"))
    dialog5101.run()
    dialog5101.destroy()
