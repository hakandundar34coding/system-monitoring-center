#!/usr/bin/env python3

# ----------------------------------- Users - Users GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_gui_import_func():

    global Gtk

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk


    global MainGUI, Users, UsersMenusGUI
    import MainGUI, Users, UsersMenusGUI


# ----------------------------------- Users - Users GUI Function (the code of this module in order to avoid running them during module import and defines "Users" tab GUI objects and functions/signals) -----------------------------------
def users_gui_func():

    global treeview3101, searchentry3101, button3101, button3102
    global radiobutton3101, radiobutton3102, radiobutton3103
    global label3101


    treeview3101 = MainGUI.builder.get_object('treeview3101')
    searchentry3101 = MainGUI.builder.get_object('searchentry3101')
    button3101 = MainGUI.builder.get_object('button3101')
    button3102 = MainGUI.builder.get_object('button3102')
    button3103 = MainGUI.builder.get_object('button3103')
    button3104 = MainGUI.builder.get_object('button3104')
    radiobutton3101 = MainGUI.builder.get_object('radiobutton3101')
    radiobutton3102 = MainGUI.builder.get_object('radiobutton3102')
    radiobutton3103 = MainGUI.builder.get_object('radiobutton3103')
    label3101 = MainGUI.builder.get_object('label3101')


    # Users tab GUI functions
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
