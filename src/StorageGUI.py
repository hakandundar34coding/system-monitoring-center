#!/usr/bin/env python3

# ----------------------------------- Storage - Storage GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_gui_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global MainGUI, Storage, StorageMenusGUI
    import MainGUI, Storage, StorageMenusGUI


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


# ----------------------------------- Storage - Storage GUI Function (the code of this module in order to avoid running them during module import and defines "Storage" tab GUI objects and functions/signals) -----------------------------------
def storage_gui_func():

    global grid4101, treeview4101, searchentry4101, button4101, button4103
    global radiobutton4101, radiobutton4102, radiobutton4103, radiobutton4104, radiobutton4105, radiobutton4106, radiobutton4107
    global label4101


    # Storage tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageTab.ui")

    # Storage tab GUI objects - get
    grid4101 = builder.get_object('grid4101')
    treeview4101 = builder.get_object('treeview4101')
    searchentry4101 = builder.get_object('searchentry4101')
    button4101 = builder.get_object('button4101')
    button4103 = builder.get_object('button4103')
    radiobutton4101 = builder.get_object('radiobutton4101')
    radiobutton4102 = builder.get_object('radiobutton4102')
    radiobutton4103 = builder.get_object('radiobutton4103')
    radiobutton4104 = builder.get_object('radiobutton4104')
    radiobutton4105 = builder.get_object('radiobutton4105')
    radiobutton4106 = builder.get_object('radiobutton4106')
    radiobutton4107 = builder.get_object('radiobutton4107')
    label4101 = builder.get_object('label4101')


    # Storage tab GUI functions
    def on_treeview4101_button_press_event(widget, event):                                    # Mouse button press event (on the treeview)
        if event.button == 3:                                                                 # Open Storage tab right click menu if mouse is right clicked on the treeview (and on any disk, otherwise menu will not be shown) and the mouse button is pressed.
            storage_open_right_click_menu_func(event)
        if event.type == Gdk.EventType._2BUTTON_PRESS:                                        # Open Storage Details window if double click is performed.
            storage_open_storage_details_window_func(event)

    def on_treeview4101_button_release_event(widget, event):                                  # Mouse button press event (on the treeview)
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            Storage.storage_treeview_column_order_width_row_sorting_func()

    def on_searchentry4101_changed(widget):                                                   # Search entry change event (called when text in the search entry is changed)
        radiobutton4101.set_active(True)
        radiobutton4105.set_active(True)
        Storage.storage_treeview_filter_search_func()

    def on_button4101_clicked(widget):                                                        # "Storage Tab Customizations" button
        StorageMenusGUI.popover4101p.popup()

    def on_radiobutton4101_toggled(widget):                                                   # "Show all disks/partitions" radiobutton
        if radiobutton4101.get_active() == True:
            Storage.storage_treeview_filter_show_all_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4102_toggled(widget):                                                   # "Show all non-removable disks/partitions" radiobutton
        if radiobutton4102.get_active() == True:
            Storage.storage_treeview_filter_show_all_func()
            Storage.storage_treeview_filter_non_removable_disks_only_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4103_toggled(widget):                                                   # "Show all removable disks/partitions" radiobutton
        if radiobutton4103.get_active() == True:
            Storage.storage_treeview_filter_show_all_func()
            Storage.storage_treeview_filter_removable_disks_only_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4104_toggled(widget):                                                   # "Show all optical and virtual disks/partitions" radiobutton
        if radiobutton4104.get_active() == True:
            Storage.storage_treeview_filter_show_all_func()
            Storage.storage_treeview_filter_optical_virtual_disks_only_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4105_toggled(widget):                                                   # "User defined expand" radiobutton
        if radiobutton4105.get_active() == True:
            pass

    def on_radiobutton4106_toggled(widget):                                                   # "Expand all" radiobutton
        if radiobutton4106.get_active() == True:
            treeview4101.expand_all()

    def on_radiobutton4107_toggled(widget):                                                   # "Collapse all" radiobutton
        if radiobutton4107.get_active() == True:
            treeview4101.collapse_all()

    def on_button4103_clicked(widget):                                                        # "Storage Tab Search Customizations" button
        StorageMenusGUI.popover4101p2.popup()



    # ********************** Connect signals to GUI objects for Storage tab right click menu **********************
    treeview4101.connect("button-press-event", on_treeview4101_button_press_event)
    treeview4101.connect("button-release-event", on_treeview4101_button_release_event)
    searchentry4101.connect("changed", on_searchentry4101_changed)
    button4101.connect("clicked", on_button4101_clicked)
    button4103.connect("clicked", on_button4103_clicked)
    radiobutton4101.connect("toggled", on_radiobutton4101_toggled)
    radiobutton4102.connect("toggled", on_radiobutton4102_toggled)
    radiobutton4103.connect("toggled", on_radiobutton4103_toggled)
    radiobutton4104.connect("toggled", on_radiobutton4104_toggled)
    radiobutton4105.connect("toggled", on_radiobutton4105_toggled)
    radiobutton4106.connect("toggled", on_radiobutton4106_toggled)
    radiobutton4107.connect("toggled", on_radiobutton4107_toggled)


    # Storage Tab - Treeview Properties
    treeview4101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview4101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview4101.set_headers_clickable(True)
    treeview4101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview4101.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview4101.set_tooltip_column(2)
    treeview4101.set_show_expanders(True)                                                     # Show expander arrows because rows on the Storage tab are alwaus shown as tree structure.


# ----------------------------------- Storage - Open Right Click Menu Function (gets right clicked storage kernel name and opens right click menu) -----------------------------------
def storage_open_right_click_menu_func(event):

    path, _, _, _ = treeview4101.get_path_at_pos(int(event.x), int(event.y))
    model = treeview4101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is None:
        storage_no_disk_selected_dialog()
    if treeiter is not None:
        global selected_storage_kernel_name
        selected_storage_kernel_name = Storage.disk_list[Storage.storage_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "storage_data_rows" list to use it getting name of the disk.
        StorageMenusGUI.menu4101m.popup(None, None, None, None, event.button, event.time)


# ----------------------------------- Storage - Open Storage Details Window Function (gets double clicked storage kernel name and opens Storage Details window) -----------------------------------
def storage_open_storage_details_window_func(event):

    if event.type == Gdk.EventType._2BUTTON_PRESS:                                            # Check if double click is performed
        path, _, _, _ = treeview4101.get_path_at_pos(int(event.x), int(event.y))
        model = treeview4101.get_model()
        treeiter = model.get_iter(path)
        if treeiter is None:
            storage_no_disk_selected_dialog()
        if treeiter is not None:
            global selected_storage_kernel_name
            selected_storage_kernel_name = Storage.disk_list[Storage.storage_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "storage_data_rows" list to use it getting name of the disk.
            # Open Storage Details window
            if 'StorageDetailsGUI' not in globals():                                          # Check if "StorageDetailsGUI" module is imported. Therefore it is not reimported for every double click on any user on the treeview if "StorageDetailsGUI" name is in globals().
                global StorageDetailsGUI, StorageDetails
                import StorageDetailsGUI, StorageDetails
                StorageDetailsGUI.storage_details_gui_import_function()
                StorageDetailsGUI.storage_details_gui_function()
                StorageDetails.storage_details_import_func()
            StorageDetailsGUI.window4101w.show()
            StorageDetails.storage_details_foreground_thread_run_func()


# ----------------------------------- Storage - No Disk Selected Dialog Function (shows a dialog when Open Storage Right Click Menu is clicked without selecting a storage/disk) -----------------------------------
def storage_no_disk_selected_dialog():

    dialog4101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Select A Disk/Partition"), )
    dialog4101.format_secondary_text(_tr("Please select a disk/partition and try again for opening the menu"))
    dialog4101.run()
    dialog4101.destroy()
