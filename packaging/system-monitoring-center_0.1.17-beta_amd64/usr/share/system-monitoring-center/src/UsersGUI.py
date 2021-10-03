#!/usr/bin/env python3

# ----------------------------------- Users - Users GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_gui_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global MainGUI, Users, UsersMenusGUI, UsersDetails, UsersDetailsGUI
    import MainGUI, Users, UsersMenusGUI, UsersDetails, UsersDetailsGUI


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


# ----------------------------------- Users - Users GUI Function (the code of this module in order to avoid running them during module import and defines "Users" tab GUI objects and functions/signals) -----------------------------------
def users_gui_func():

    global grid3101, treeview3101, searchentry3101, button3101, button3102
    global radiobutton3101, radiobutton3102, radiobutton3103
    global label3101


    # Users tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersTab.ui")

    # Users tab GUI objects - get
    grid3101 = builder.get_object('grid3101')
    treeview3101 = builder.get_object('treeview3101')
    searchentry3101 = builder.get_object('searchentry3101')
    button3101 = builder.get_object('button3101')
    button3102 = builder.get_object('button3102')
    button3103 = builder.get_object('button3103')
    radiobutton3101 = builder.get_object('radiobutton3101')
    radiobutton3102 = builder.get_object('radiobutton3102')
    radiobutton3103 = builder.get_object('radiobutton3103')
    label3101 = builder.get_object('label3101')


    # Users tab GUI functions
    def on_treeview3101_button_press_event(widget, event):
        if event.button == 3:                                                                 # Open Users tab right click menu if mouse is right clicked on the treeview (and on any user, otherwise menu will not be shown) and the mouse button is pressed.
            users_open_right_click_menu_func(event)
        if event.type == Gdk.EventType._2BUTTON_PRESS:                                        # Open User Details window if double click is performed.
            users_open_user_details_window_func(event)

    def on_treeview3101_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Users.users_treeview_column_order_width_row_sorting_func()

    def on_searchentry3101_changed(widget):
        radiobutton3101.set_active(True)
        Users.users_treeview_filter_search_func()

    def on_button3101_clicked(widget):                                                        # "Users Tab Customizations" button
        UsersMenusGUI.popover3101p.popup()

    def on_radiobutton3101_toggled(widget):                                                   # "Show all users" radiobutton
        if radiobutton3101.get_active() == True:
            Users.users_treeview_filter_show_all_func()

    def on_radiobutton3102_toggled(widget):                                                   # "Show only users logged in" radiobutton
        if radiobutton3102.get_active() == True:
            Users.users_treeview_filter_show_all_func()
            Users.users_treeview_filter_users_logged_in_only()

    def on_radiobutton3103_toggled(widget):                                                   # "Show only users logged out" radiobutton
        if radiobutton3103.get_active() == True:
            Users.users_treeview_filter_show_all_func()
            Users.users_treeview_filter_users_logged_out_only()

    def on_button3102_clicked(widget):                                                        # "Users Tab Search Customizations" button
        UsersMenusGUI.popover3101p2.popup()



    # Users tab GUI functions - connect
    treeview3101.connect("button-press-event", on_treeview3101_button_press_event)
    treeview3101.connect("button-release-event", on_treeview3101_button_release_event)
    searchentry3101.connect("changed", on_searchentry3101_changed)
    button3101.connect("clicked", on_button3101_clicked)
    button3102.connect("clicked", on_button3102_clicked)
    radiobutton3101.connect("toggled", on_radiobutton3101_toggled)
    radiobutton3102.connect("toggled", on_radiobutton3102_toggled)
    radiobutton3103.connect("toggled", on_radiobutton3103_toggled)


    # Users Tab - Treeview Properties
    treeview3101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview3101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview3101.set_headers_clickable(True)
    treeview3101.set_show_expanders(False)
    treeview3101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview3101.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview3101.set_tooltip_column(2)


# ----------------------------------- Users - Open Right Click Menu Function (gets right clicked user UID and opens right click menu) -----------------------------------
def users_open_right_click_menu_func(event):

    path, _, _, _ = treeview3101.get_path_at_pos(int(event.x), int(event.y))
    model = treeview3101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is None:
        users_no_user_selected_dialog()
    if treeiter is not None:
        global selected_user_uid
        selected_user_uid = Users.uid_username_list[Users.users_data_rows.index(model[treeiter][:])][0]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "user_data_rows" list to use it getting UID of the user.
        UsersMenusGUI.menu3101m.popup(None, None, None, None, event.button, event.time)


# ----------------------------------- Users - Open User Details Window Function (gets double clicked user UID and opens User Details window) -----------------------------------
def users_open_user_details_window_func(event):

    if event.type == Gdk.EventType._2BUTTON_PRESS:                                            # Check if double click is performed
        path, _, _, _ = treeview3101.get_path_at_pos(int(event.x), int(event.y))
        model = treeview3101.get_model()
        treeiter = model.get_iter(path)
        if treeiter is None:
            users_no_user_selected_dialog()
        if treeiter is not None:
            global selected_user_uid
            selected_user_uid = Users.uid_username_list[Users.users_data_rows.index(model[treeiter][:])][0]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "users_data_rows" list to use it getting UID of the user.
            # Open Users Details window
            UsersDetailsGUI.users_details_gui_function()
            UsersDetailsGUI.window3101w.show()
            UsersDetails.users_details_foreground_thread_run_func()

# ----------------------------------- Users - No User Selected Dialog Function (shows a dialog when Open Users Right Click Menu is clicked without selecting an user) -----------------------------------
def users_no_user_selected_dialog():

    dialog3101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Select An User"), )
    dialog3101.format_secondary_text(_tr("Please select an user and try again for opening the menu"))
    dialog3101.run()
    dialog3101.destroy()
