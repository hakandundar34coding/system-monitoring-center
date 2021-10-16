#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Customizations Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_menu_customizations_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Storage
    import Config, Storage


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


# ----------------------------------- Storage - Storage Customizations Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Storage" tab menu/popover GUI objects and functions/signals) -----------------------------------
def storage_menu_customizations_gui_func():

    # Define builder and get all objects (Storage tab search customizations popover) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageMenuCustomizations.ui")


    # ********************** Define object names for Storage tab customizations popover **********************
    global popover4101p
    global checkbutton4101p, checkbutton4102p, checkbutton4103p, checkbutton4104p, checkbutton4105p, checkbutton4106p
    global checkbutton4107p, checkbutton4108p, checkbutton4109p, checkbutton4110p, checkbutton4111p, checkbutton4112p
    global checkbutton4113p, checkbutton4114p, checkbutton4115p, checkbutton4116p, checkbutton4117p, checkbutton4118p
    global checkbutton4119p, checkbutton4120p, checkbutton4121p, checkbutton4122p, checkbutton4123p, checkbutton4124p
    global button4101p, button4102p
    global combobox4101p, combobox4102p

    # ********************** Get object names for Storage tab customizations popover **********************
    popover4101p = builder.get_object('popover4101p')
    checkbutton4101p = builder.get_object('checkbutton4101p')
    checkbutton4102p = builder.get_object('checkbutton4102p')
    checkbutton4103p = builder.get_object('checkbutton4103p')
    checkbutton4104p = builder.get_object('checkbutton4104p')
    checkbutton4105p = builder.get_object('checkbutton4105p')
    checkbutton4106p = builder.get_object('checkbutton4106p')
    checkbutton4107p = builder.get_object('checkbutton4107p')
    checkbutton4108p = builder.get_object('checkbutton4108p')
    checkbutton4109p = builder.get_object('checkbutton4109p')
    checkbutton4110p = builder.get_object('checkbutton4110p')
    checkbutton4111p = builder.get_object('checkbutton4111p')
    checkbutton4112p = builder.get_object('checkbutton4112p')
    checkbutton4113p = builder.get_object('checkbutton4113p')
    checkbutton4114p = builder.get_object('checkbutton4114p')
    checkbutton4115p = builder.get_object('checkbutton4115p')
    checkbutton4116p = builder.get_object('checkbutton4116p')
    checkbutton4117p = builder.get_object('checkbutton4117p')
    checkbutton4118p = builder.get_object('checkbutton4118p')
    checkbutton4119p = builder.get_object('checkbutton4119p')
    checkbutton4120p = builder.get_object('checkbutton4120p')
    checkbutton4121p = builder.get_object('checkbutton4121p')
    checkbutton4122p = builder.get_object('checkbutton4122p')
    checkbutton4123p = builder.get_object('checkbutton4123p')
    checkbutton4124p = builder.get_object('checkbutton4124p')
    button4101p = builder.get_object('button4101p')
    button4102p = builder.get_object('button4102p')
    combobox4101p = builder.get_object('combobox4101p')
    combobox4102p = builder.get_object('combobox4102p')

    # ********************** Define object functions for Storage tab customizations popover Common GUI Objects **********************
    def on_button4101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_storage_func()
        Config.config_save_func()
        storage_tab_customization_popover_disconnect_signals_func()
        storage_tab_popover_set_gui()
        storage_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Storage tab customizations popover View Tab **********************
    def on_button4102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_storage_row_sort_column_order_func()
        storage_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        storage_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Storage tab customizations popover Add/Remove Columns Tab **********************
    def on_checkbutton4101p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4102p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4103p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4104p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4105p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4106p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4107p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4108p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4109p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4110p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4111p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4112p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4113p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4114p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4115p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4116p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4117p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4118p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4119p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4120p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4121p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4122p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4123p_toggled(widget):
        storage_add_remove_columns_function()
    def on_checkbutton4124p_toggled(widget):
        storage_add_remove_columns_function()

    # ********************** Define object functions for Storage tab customizations popover Precision/Data Tab **********************
    def on_combobox4101p_changed(widget):
        Config.storage_disk_usage_data_precision = Config.number_precision_list[combobox4101p.get_active()][2]
        Config.config_save_func()

    def on_combobox4102p_changed(widget):
        Config.storage_disk_usage_data_unit = Config.data_unit_list[combobox4102p.get_active()][2]
        Config.config_save_func()

    # ********************** Connect signals to GUI objects for Storage tab customizations popover Common GUI Objects **********************
    button4101p.connect("clicked", on_button4101p_clicked)
    button4102p.connect("clicked", on_button4102p_clicked)


    # ********************** Popover settings for Storage tab **********************
    popover4101p.set_relative_to(Storage.button4101)
    popover4101p.set_position(1)


    # ********************** Define function for connecting Storage tab customizations popover GUI signals **********************
    def storage_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Storage tab customizations popover Add/Remove Columns Tab **********************
        checkbutton4101p.connect("toggled", on_checkbutton4101p_toggled)
        checkbutton4102p.connect("toggled", on_checkbutton4102p_toggled)
        checkbutton4103p.connect("toggled", on_checkbutton4103p_toggled)
        checkbutton4104p.connect("toggled", on_checkbutton4104p_toggled)
        checkbutton4105p.connect("toggled", on_checkbutton4105p_toggled)
        checkbutton4106p.connect("toggled", on_checkbutton4106p_toggled)
        checkbutton4107p.connect("toggled", on_checkbutton4107p_toggled)
        checkbutton4108p.connect("toggled", on_checkbutton4108p_toggled)
        checkbutton4109p.connect("toggled", on_checkbutton4109p_toggled)
        checkbutton4110p.connect("toggled", on_checkbutton4110p_toggled)
        checkbutton4111p.connect("toggled", on_checkbutton4111p_toggled)
        checkbutton4112p.connect("toggled", on_checkbutton4112p_toggled)
        checkbutton4113p.connect("toggled", on_checkbutton4113p_toggled)
        checkbutton4114p.connect("toggled", on_checkbutton4114p_toggled)
        checkbutton4115p.connect("toggled", on_checkbutton4115p_toggled)
        checkbutton4116p.connect("toggled", on_checkbutton4116p_toggled)
        checkbutton4117p.connect("toggled", on_checkbutton4117p_toggled)
        checkbutton4118p.connect("toggled", on_checkbutton4118p_toggled)
        checkbutton4119p.connect("toggled", on_checkbutton4119p_toggled)
        checkbutton4120p.connect("toggled", on_checkbutton4120p_toggled)
        checkbutton4121p.connect("toggled", on_checkbutton4121p_toggled)
        checkbutton4122p.connect("toggled", on_checkbutton4122p_toggled)
        checkbutton4123p.connect("toggled", on_checkbutton4123p_toggled)
        checkbutton4124p.connect("toggled", on_checkbutton4124p_toggled)
        # ********************** Connect signals to GUI objects for Storage tab customizations popover Precision/Data Units Tab **********************
        combobox4101p.connect("changed", on_combobox4101p_changed)
        combobox4102p.connect("changed", on_combobox4102p_changed)


    # ********************** Define function for disconnecting Storage tab customizations popover GUI signals **********************
    def storage_tab_customization_popover_disconnect_signals_func():
        # ********************** Disconnect signals of GUI objects for Storage tab customizations popover Add/Remove Columns Tab **********************
        checkbutton4101p.disconnect_by_func(on_checkbutton4101p_toggled)
        checkbutton4102p.disconnect_by_func(on_checkbutton4102p_toggled)
        checkbutton4103p.disconnect_by_func(on_checkbutton4103p_toggled)
        checkbutton4104p.disconnect_by_func(on_checkbutton4104p_toggled)
        checkbutton4105p.disconnect_by_func(on_checkbutton4105p_toggled)
        checkbutton4106p.disconnect_by_func(on_checkbutton4106p_toggled)
        checkbutton4107p.disconnect_by_func(on_checkbutton4107p_toggled)
        checkbutton4108p.disconnect_by_func(on_checkbutton4108p_toggled)
        checkbutton4109p.disconnect_by_func(on_checkbutton4109p_toggled)
        checkbutton4110p.disconnect_by_func(on_checkbutton4110p_toggled)
        checkbutton4111p.disconnect_by_func(on_checkbutton4111p_toggled)
        checkbutton4112p.disconnect_by_func(on_checkbutton4112p_toggled)
        checkbutton4113p.disconnect_by_func(on_checkbutton4113p_toggled)
        checkbutton4114p.disconnect_by_func(on_checkbutton4114p_toggled)
        checkbutton4115p.disconnect_by_func(on_checkbutton4115p_toggled)
        checkbutton4116p.disconnect_by_func(on_checkbutton4116p_toggled)
        checkbutton4117p.disconnect_by_func(on_checkbutton4117p_toggled)
        checkbutton4118p.disconnect_by_func(on_checkbutton4118p_toggled)
        checkbutton4119p.disconnect_by_func(on_checkbutton4119p_toggled)
        checkbutton4120p.disconnect_by_func(on_checkbutton4120p_toggled)
        checkbutton4121p.disconnect_by_func(on_checkbutton4121p_toggled)
        checkbutton4122p.disconnect_by_func(on_checkbutton4122p_toggled)
        checkbutton4123p.disconnect_by_func(on_checkbutton4123p_toggled)
        checkbutton4124p.disconnect_by_func(on_checkbutton4124p_toggled)
        # ********************** Disconnect signals of GUI objects for Storage tab customizations popover Precision/Data Units Tab **********************
        combobox4101p.disconnect_by_func(on_combobox4101p_changed)
        combobox4102p.disconnect_by_func(on_combobox4102p_changed)


    # ********************** Popover settings for Storage tab customizations **********************
    storage_tab_popover_set_gui()
    storage_tab_customization_popover_connect_signals_func()


# ********************** Set Storage tab customizations popover menu GUI object data/selections appropriate for settings **********************
def storage_tab_popover_set_gui():
    # Set Storage tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.storage_treeview_columns_shown:
        checkbutton4101p.set_active(True)
    if 0 not in Config.storage_treeview_columns_shown:
        checkbutton4101p.set_active(False)
    if 1 in Config.storage_treeview_columns_shown:
        checkbutton4102p.set_active(True)
    if 1 not in Config.storage_treeview_columns_shown:
        checkbutton4102p.set_active(False)
    if 2 in Config.storage_treeview_columns_shown:
        checkbutton4103p.set_active(True)
    if 2 not in Config.storage_treeview_columns_shown:
        checkbutton4103p.set_active(False)
    if 3 in Config.storage_treeview_columns_shown:
        checkbutton4104p.set_active(True)
    if 3 not in Config.storage_treeview_columns_shown:
        checkbutton4104p.set_active(False)
    if 4 in Config.storage_treeview_columns_shown:
        checkbutton4105p.set_active(True)
    if 4 not in Config.storage_treeview_columns_shown:
        checkbutton4105p.set_active(False)
    if 5 in Config.storage_treeview_columns_shown:
        checkbutton4106p.set_active(True)
    if 5 not in Config.storage_treeview_columns_shown:
        checkbutton4106p.set_active(False)
    if 6 in Config.storage_treeview_columns_shown:
        checkbutton4107p.set_active(True)
    if 6 not in Config.storage_treeview_columns_shown:
        checkbutton4107p.set_active(False)
    if 7 in Config.storage_treeview_columns_shown:
        checkbutton4108p.set_active(True)
    if 7 not in Config.storage_treeview_columns_shown:
        checkbutton4108p.set_active(False)
    if 8 in Config.storage_treeview_columns_shown:
        checkbutton4109p.set_active(True)
    if 8 not in Config.storage_treeview_columns_shown:
        checkbutton4109p.set_active(False)
    if 9 in Config.storage_treeview_columns_shown:
        checkbutton4110p.set_active(True)
    if 9 not in Config.storage_treeview_columns_shown:
        checkbutton4110p.set_active(False)
    if 10 in Config.storage_treeview_columns_shown:
        checkbutton4111p.set_active(True)
    if 10 not in Config.storage_treeview_columns_shown:
        checkbutton4111p.set_active(False)
    if 11 in Config.storage_treeview_columns_shown:
        checkbutton4112p.set_active(True)
    if 11 not in Config.storage_treeview_columns_shown:
        checkbutton4112p.set_active(False)
    if 12 in Config.storage_treeview_columns_shown:
        checkbutton4113p.set_active(True)
    if 12 not in Config.storage_treeview_columns_shown:
        checkbutton4113p.set_active(False)
    if 13 in Config.storage_treeview_columns_shown:
        checkbutton4114p.set_active(True)
    if 13 not in Config.storage_treeview_columns_shown:
        checkbutton4114p.set_active(False)
    if 14 in Config.storage_treeview_columns_shown:
        checkbutton4115p.set_active(True)
    if 14 not in Config.storage_treeview_columns_shown:
        checkbutton4115p.set_active(False)
    if 15 in Config.storage_treeview_columns_shown:
        checkbutton4116p.set_active(True)
    if 15 not in Config.storage_treeview_columns_shown:
        checkbutton4116p.set_active(False)
    if 16 in Config.storage_treeview_columns_shown:
        checkbutton4117p.set_active(True)
    if 16 not in Config.storage_treeview_columns_shown:
        checkbutton4117p.set_active(False)
    if 17 in Config.storage_treeview_columns_shown:
        checkbutton4118p.set_active(True)
    if 17 not in Config.storage_treeview_columns_shown:
        checkbutton4118p.set_active(False)
    if 18 in Config.storage_treeview_columns_shown:
        checkbutton4119p.set_active(True)
    if 18 not in Config.storage_treeview_columns_shown:
        checkbutton4119p.set_active(False)
    if 19 in Config.storage_treeview_columns_shown:
        checkbutton4120p.set_active(True)
    if 19 not in Config.storage_treeview_columns_shown:
        checkbutton4120p.set_active(False)
    if 20 in Config.storage_treeview_columns_shown:
        checkbutton4121p.set_active(True)
    if 20 not in Config.storage_treeview_columns_shown:
        checkbutton4121p.set_active(False)
    if 21 in Config.storage_treeview_columns_shown:
        checkbutton4122p.set_active(True)
    if 21 not in Config.storage_treeview_columns_shown:
        checkbutton4122p.set_active(False)
    if 22 in Config.storage_treeview_columns_shown:
        checkbutton4123p.set_active(True)
    if 22 not in Config.storage_treeview_columns_shown:
        checkbutton4123p.set_active(False)
    if 23 in Config.storage_treeview_columns_shown:
        checkbutton4124p.set_active(True)
    if 23 not in Config.storage_treeview_columns_shown:
        checkbutton4124p.set_active(False)
    # Set Storage tab customizations popover menu Precision/Data Units tab GUI object data/selections appropriate for settings
    # Add Disk usage data precision into combobox
    if "liststore4101p" not in globals():                                                     # Check if "liststore4101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
        global liststore4101p
        liststore4101p = Gtk.ListStore()
        liststore4101p.set_column_types([str, int])
        combobox4101p.set_model(liststore4101p)
        renderer_text = Gtk.CellRendererText()
        combobox4101p.pack_start(renderer_text, True)
        combobox4101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore4101p.append([data[1], data[2]])
    combobox4101p.set_active(Config.storage_disk_usage_data_precision)
    # Add Disk usage data unit data into combobox
    if "liststore4102p" not in globals():
        global liststore4102p
        liststore4102p = Gtk.ListStore()
        liststore4102p.set_column_types([str, int])
        combobox4102p.set_model(liststore4102p)
        renderer_text = Gtk.CellRendererText()
        combobox4102p.pack_start(renderer_text, True)
        combobox4102p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore4102p.append([data[1], data[2]])
    for data_list in Config.data_unit_list:
        if data_list[2] == Config.storage_disk_usage_data_unit:      
            combobox4102p.set_active(data_list[0])


# ----------------------------------- Storage - Storage Add/Remove Columns Function (adds/removes storage treeview columns) -----------------------------------
def storage_add_remove_columns_function():

    Config.storage_treeview_columns_shown = []
    if checkbutton4101p.get_active() is True:
        Config.storage_treeview_columns_shown.append(0)
    if checkbutton4102p.get_active() is True:
        Config.storage_treeview_columns_shown.append(1)
    if checkbutton4103p.get_active() is True:
        Config.storage_treeview_columns_shown.append(2)
    if checkbutton4104p.get_active() is True:
        Config.storage_treeview_columns_shown.append(3)
    if checkbutton4105p.get_active() is True:
        Config.storage_treeview_columns_shown.append(4)
    if checkbutton4106p.get_active() is True:
        Config.storage_treeview_columns_shown.append(5)
    if checkbutton4107p.get_active() is True:
        Config.storage_treeview_columns_shown.append(6)
    if checkbutton4108p.get_active() is True:
        Config.storage_treeview_columns_shown.append(7)
    if checkbutton4109p.get_active() is True:
        Config.storage_treeview_columns_shown.append(8)
    if checkbutton4110p.get_active() is True:
        Config.storage_treeview_columns_shown.append(9)
    if checkbutton4111p.get_active() is True:
        Config.storage_treeview_columns_shown.append(10)
    if checkbutton4112p.get_active() is True:
        Config.storage_treeview_columns_shown.append(11)
    if checkbutton4113p.get_active() is True:
        Config.storage_treeview_columns_shown.append(12)
    if checkbutton4114p.get_active() is True:
        Config.storage_treeview_columns_shown.append(13)
    if checkbutton4115p.get_active() is True:
        Config.storage_treeview_columns_shown.append(14)
    if checkbutton4116p.get_active() is True:
        Config.storage_treeview_columns_shown.append(15)
    if checkbutton4117p.get_active() is True:
        Config.storage_treeview_columns_shown.append(16)
    if checkbutton4118p.get_active() is True:
        Config.storage_treeview_columns_shown.append(17)
    if checkbutton4119p.get_active() is True:
        Config.storage_treeview_columns_shown.append(18)
    if checkbutton4120p.get_active() is True:
        Config.storage_treeview_columns_shown.append(19)
    if checkbutton4121p.get_active() is True:
        Config.storage_treeview_columns_shown.append(20)
    if checkbutton4122p.get_active() is True:
        Config.storage_treeview_columns_shown.append(21)
    if checkbutton4123p.get_active() is True:
        Config.storage_treeview_columns_shown.append(22)
    if checkbutton4124p.get_active() is True:
        Config.storage_treeview_columns_shown.append(23)
    Config.config_save_func()
