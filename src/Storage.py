#!/usr/bin/env python3

# ----------------------------------- Storage - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_import_func():

    global Gtk, Gdk, GLib, GObject, Thread, subprocess, os, datetime

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, GObject
    from threading import Thread
    import subprocess
    import os
    from datetime import datetime


    global Config, MainGUI
    import Config, MainGUI


    # Import gettext module for defining translation texts which will be recognized by gettext application. These lines of code are enough to define this variable if another values are defined in another module (MainGUI) before importing this module.
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    from locale import gettext as _tr


# ----------------------------------- Storage - Storage GUI Function (the code of this module in order to avoid running them during module import and defines "Storage" tab GUI objects and functions/signals) -----------------------------------
def storage_gui_func():

    global grid4101, treeview4101, searchentry4101, button4101
    global radiobutton4101, radiobutton4102, radiobutton4103, radiobutton4104, radiobutton4105, radiobutton4106, radiobutton4107
    global label4101


    # Storage tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageTab.ui")

    # Storage tab GUI objects - get
    grid4101 = builder.get_object('grid4101')
    treeview4101 = builder.get_object('treeview4101')
    searchentry4101 = builder.get_object('searchentry4101')
    button4101 = builder.get_object('button4101')
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
            storage_treeview_column_order_width_row_sorting_func()

    def on_searchentry4101_changed(widget):                                                   # Search entry change event (called when text in the search entry is changed)
        radiobutton4101.set_active(True)
        radiobutton4105.set_active(True)
        storage_treeview_filter_search_func()

    def on_button4101_clicked(widget):                                                        # "Storage Tab Customizations" button
        if 'StorageMenuCustomizations' not in globals():                                      # Check if "StorageMenuCustomizations" module is imported. Therefore it is not reimported on every right click operation.
            global StorageMenuCustomizations
            import StorageMenuCustomizations
            StorageMenuCustomizations.storage_menu_customizations_import_func()
            StorageMenuCustomizations.storage_menu_customizations_gui_func()
        StorageMenuCustomizations.popover4101p.popup()

    def on_radiobutton4101_toggled(widget):                                                   # "Show all disks/partitions" radiobutton
        if radiobutton4101.get_active() == True:
            searchentry4101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            storage_treeview_filter_show_all_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4102_toggled(widget):                                                   # "Show all non-removable disks/partitions" radiobutton
        if radiobutton4102.get_active() == True:
            searchentry4101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            storage_treeview_filter_show_all_func()
            storage_treeview_filter_non_removable_disks_only_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4103_toggled(widget):                                                   # "Show all removable disks/partitions" radiobutton
        if radiobutton4103.get_active() == True:
            searchentry4101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            storage_treeview_filter_show_all_func()
            storage_treeview_filter_removable_disks_only_func()
            radiobutton4105.set_active(True)

    def on_radiobutton4104_toggled(widget):                                                   # "Show all optical and virtual disks/partitions" radiobutton
        if radiobutton4104.get_active() == True:
            searchentry4101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            storage_treeview_filter_show_all_func()
            storage_treeview_filter_optical_virtual_disks_only_func()
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


    # ********************** Connect signals to GUI objects for Storage tab right click menu **********************
    treeview4101.connect("button-press-event", on_treeview4101_button_press_event)
    treeview4101.connect("button-release-event", on_treeview4101_button_release_event)
    searchentry4101.connect("changed", on_searchentry4101_changed)
    button4101.connect("clicked", on_button4101_clicked)
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

    try:                                                                                      # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview4101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview4101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is not None:
        global selected_storage_kernel_name
        selected_storage_kernel_name = disk_list[storage_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "storage_data_rows" list to use it getting name of the disk.
        if 'StorageMenuRightClick' not in globals():                                          # Check if "StorageMenuRightClick" module is imported. Therefore it is not reimported on every right click operation.
            global StorageMenuRightClick
            import StorageMenuRightClick
            StorageMenuRightClick.storage_menu_right_click_import_func()
            StorageMenuRightClick.storage_menu_right_click_gui_func()
        StorageMenuRightClick.storage_disk_parent_child_disk_mount_point_etc_func()
        StorageMenuRightClick.menu4101m.popup(None, None, None, None, event.button, event.time)


# ----------------------------------- Storage - Open Storage Details Window Function (gets double clicked storage kernel name and opens Storage Details window) -----------------------------------
def storage_open_storage_details_window_func(event):

    if event.type == Gdk.EventType._2BUTTON_PRESS:                                            # Check if double click is performed
        try:                                                                                  # "try-except" is used in order to prevent errors when double clicked on an empty area on the treeview.
            path, _, _, _ = treeview4101.get_path_at_pos(int(event.x), int(event.y))
        except TypeError:
            return
        model = treeview4101.get_model()
        treeiter = model.get_iter(path)
        if treeiter is not None:
            global selected_storage_kernel_name
            selected_storage_kernel_name = disk_list[storage_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "storage_data_rows" list to use it getting name of the disk.
            # Open Storage Details window
            if 'StorageDetails' not in globals():                                             # Check if "StorageDetails" module is imported. Therefore it is not reimported for every double click on any user on the treeview if "StorageDetails" name is in globals().
                global StorageDetails
                import StorageDetails
                StorageDetails.storage_details_import_func()
                StorageDetails.storage_details_gui_function()
            StorageDetails.window4101w.show()
            StorageDetails.storage_details_foreground_thread_run_func()


# ----------------------------------- Storage - Initial Function (contains initial code which defines some variables and gets data which is not wanted to be run in every loop) -----------------------------------
def storage_initial_func():

    # data list explanation:
    # storage_data_list = [
    #                     [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
    #                     .
    #                     .
    #                     ]
    global storage_data_list
    storage_data_list = [
                        [0, _tr('Disk Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                        [1, _tr('Parent Name'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [2, _tr('System Disk'), 1, 1, 1, [bool], ['CellRendererToggle'], ['active'], [0], [0.5], [False], ['no_cell_function']],
                        [3, _tr('Type'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [4, _tr('Transport Type'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [5, _tr('File System'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [6, _tr('Total Size'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                        [7, _tr('Free Space'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                        [8, _tr('Used Space'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                        [9, _tr('Used Space%'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage_percentage]],
                        [10, _tr('Vendor-Model'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [11, _tr('Label'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [12, _tr('Partition Label'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [13, _tr('Mount Point'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [14, _tr('Path'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                        [15, _tr('Revision'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [16, _tr('Serial Number'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [17, _tr('Mode'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [18, _tr('Removable'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [19, _tr('Rotational'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [20, _tr('Read-Only'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [21, _tr('UUID'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [22, _tr('Unique Storage Id.'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [23, _tr('Major:Minor Device #'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                        ]

    storage_define_data_unit_converter_variables_func()                                       # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global storage_data_rows_prev, storage_treeview_columns_shown_prev, storage_data_row_sorting_column_prev, storage_data_row_sorting_order_prev, storage_data_column_order_prev, storage_data_column_widths_prev
    global disk_order_name_time_list_prev, selected_disk_type
    storage_data_rows_prev = []
    disk_order_name_time_list_prev = []
    selected_disk_type = "all_disks"                                                          # For counting and filtering(by clicking radiobuttons or typing into search entry) disk types. "all_disk" is the initial value. This variable will be modified by "show only ... disks/partitions" radiobuttons on the "Storage" tab.
    storage_treeview_columns_shown_prev = []
    storage_data_row_sorting_column_prev = ""
    storage_data_row_sorting_order_prev = ""
    storage_data_column_order_prev = []
    storage_data_column_widths_prev = []

    global disk_sector_size
    disk_sector_size = 512                                                                    # Disk data values from "/sys/class/block/[DISK_NAME]/" are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).

    global storage_image_ssd_hdd, storage_image_removable, storage_image_optical, storage_image_partition
    storage_image_ssd_hdd = "system-monitoring-center-disk-hdd-symbolic"
    storage_image_removable = "system-monitoring-center-disk-removable-symbolic"
    storage_image_optical = "system-monitoring-center-disk-optical-symbolic"
    storage_image_partition = "system-monitoring-center-disk-partition-symbolic"

    global filter_column
    filter_column = storage_data_list[0][2] - 1                                               # Search filter is "Process Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.


# ----------------------------------- Storage - Get Storage Data Function (gets storage data, adds into treeview and updates it) -----------------------------------
def storage_loop_func():

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview4101

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global storage_disk_usage_data_precision, storage_disk_usage_data_unit
    storage_disk_usage_data_precision = Config.storage_disk_usage_data_precision
    storage_disk_usage_data_unit = Config.storage_disk_usage_data_unit

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global storage_treeview_columns_shown
    global storage_treeview_columns_shown_prev, storage_data_row_sorting_column_prev, storage_data_row_sorting_order_prev, storage_data_column_order_prev, storage_data_column_widths_prev
    storage_treeview_columns_shown = Config.storage_treeview_columns_shown
    storage_data_row_sorting_column = Config.storage_data_row_sorting_column
    storage_data_row_sorting_order = Config.storage_data_row_sorting_order
    storage_data_column_order = Config.storage_data_column_order
    storage_data_column_widths = Config.storage_data_column_widths

    # Define global variables and empty lists for the current loop
    global storage_data_rows, storage_data_rows_prev, disk_list, parent_disk_list, disk_order_name_time_list, disk_order_name_time_list_prev, disk_type_list
    storage_data_rows = []
    parent_disk_list = []                                                                     # For tracking child/parent disk relationship for appending disk data rows into treeview as tree structure.
    disk_order_name_time_list = []                                                            # For tracking new/removed disk data rows.
    disk_type_list = []                                                                       # For counting and filtering(by clicking radiobuttons or typing into search entry) disk types

    # Get all disks (disks and partitions) including physical, optical and virtual disks
    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().split("\n")[2:-1]                               # Get without first 2 lines (header line and an empty line).
    disk_list = []
    for line in proc_partitions_lines:
        disk_list.append(line.split()[3])                                                     # Get disk list.    
    # Get disk path, mount point, file system and mode information
    with open("/proc/mounts") as reader:
        proc_mounts_lines = reader.read().strip().split("\n")
    # Get swap disk information
    with open("/proc/swaps") as reader:
        proc_swaps_lines = reader.read().split("\n")[1:-1]                                    # Get without first line (header line).
    swap_disk_list = []
    for line in proc_swaps_lines:
        swap_disk_list.append(line.split()[0].split("/")[-1])
    # Get disk device path
    disk_device_path_list = os.listdir("/dev/disk/by-path/")                                  # Some disks (such as zram0, zram1, etc. swap partitions) may not be present in "/dev/disk/by-path/" path.
    disk_device_path_disk_list = []
    for disk_device_path in disk_device_path_list:
        disk_device_path_disk_list.append(os.path.realpath("/dev/disk/by-path/" + disk_device_path).split("/")[-1])    # "os.readlink()" does not work with "/dev/disk/[folder_name]/[file_name]" files. "os.path.realpath()" is used for getting path.
    # "disk_order" variable is appended into "disk_order_name_time_list" list of multiple elemented sub-list which is used for tracing removed/appended disks to keep storage/disk list up to date. "disk_order" variable is used for sorting disks after "set()" method is used in order to get list differences.
    disk_order = 0                                                                            # Initial value of the "disk_order" variable. It starts from "1" and increases "1" for each disk.

    # Get and append per disk data
    for disk in disk_list:
        with open("/sys/class/block/" + disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")
        disk_order = disk_order + 1
        disk_connected_time = datetime.fromtimestamp(os.path.getmtime("/sys/class/block/" + disk + "/uevent")).strftime("%H:%M:%S %d.%m.%Y")
        disk_order_name_time_list.append([disk_order, disk + " - " + disk_connected_time])    # This data is used for tracking removed/appended disk/storage information
        # Get disk symbol which also will be used for detecting disk type (will be used for disk filtering)
        for line in sys_class_block_disk_uevent_lines:
            if "DEVTYPE" in line:
                disk_type = _tr(line.split("=")[1].capitalize())
                break
        disk_symbol = storage_image_ssd_hdd                                                   # Initial value of "disk_symbol" variable. This value will be used if disk type could not be detected. The same value is also used for non-USB and non-optical drives.
        if disk_type == _tr("Disk"):
            if "loop" in disk or "sr" in disk:                                                # Optical symbol is used as disk symbol if disk type is "disk (not partition)" and disk is a virtual disk or physical optical disk.
                disk_symbol = storage_image_optical
            elif disk not in disk_device_path_disk_list:                                      # This condition is used before checking "'-usb-' in disk_device_path_list" in order to avoid errors because of the "elif "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:" condition. Because some disks (such as zram0, zram1, etc.) may not present in "/dev/disk/by-path/" path and in "disk_device_path_disk_list" list.
                disk_symbol = storage_image_ssd_hdd
            elif "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
                disk_symbol = storage_image_removable
            else:
                disk_symbol = storage_image_ssd_hdd
        if disk_type == _tr("Partition"):                                                     # Same symbol image is used for all disk partitions.
            disk_symbol = storage_image_partition
        disk_type_list.append(disk_symbol)                                                    # Append disk type
        # Get disk parent name
        disk_parent_name = "-"                                                                # Initial value of "disk_parent_name" variable. This value will be used if disk has no parent disk or disk parent name could not be detected.
        if disk_type == _tr("Partition"):
            for check_disk_dir in disk_list:
                if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + disk) == True:
                    disk_parent_name = check_disk_dir
        parent_disk_list.append(disk_parent_name)
        # Get disk mount point which will be used for getting disk free, used spaces, used space percentage and also will be shown on the treeview as "disk mount point" information depending on user preferences.
        disk_mount_point = _tr("[Not mounted]")                                               # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
        for line in proc_mounts_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == disk:
                disk_mount_point = bytes(line_split[1], "utf-8").decode("unicode_escape")     # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
        # Append disk symbol and disk name
        storage_data_row = [True, disk_symbol, disk]                                          # Storage data row visibility data (True/False) is always appended into the list. True is an initial value and it is modified later.
        # Append disk parent name
        if 1 in storage_treeview_columns_shown:
            storage_data_row.append(disk_parent_name)
        # Get if disk is system disk information
        if 2 in storage_treeview_columns_shown:
            disk_system_disk = False                                                          # Initial value of "disk_system_disk" variable. This value will be used if disk mount point is not "/".
            for line in proc_mounts_lines:
                line_split = line.split()
                if line_split[0].split("/")[-1] == disk and line_split[1] == "/":
                    disk_system_disk = True
                    break
            storage_data_row.append(disk_system_disk)
        # Append disk type
        if 3 in storage_treeview_columns_shown:
            storage_data_row.append(disk_type)
        # Get disk transport type
        if 4 in storage_treeview_columns_shown:
            disk_transport_type = "-"                                                         # Initial value of "disk_transport_type" variable. This value will be used if disk transport type could not be detected.
            if disk in disk_device_path_disk_list:
                if "-ata-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
                    disk_transport_type = "SATA"
                if "-usb-" in disk_device_path_list[disk_device_path_disk_list.index(disk)]:
                    disk_transport_type = "USB"
            storage_data_row.append(disk_transport_type)
        # Get disk file system
        if 5 in storage_treeview_columns_shown:
            disk_file_system = "-"                                                            # Initial value of "disk_file_system" variable. This value will be used if disk file system could not be detected.
            for line in proc_mounts_lines:
                line_split = line.split()
                if line_split[0].split("/")[-1] == disk:
                    disk_file_system = line_split[2]
            if disk_file_system  == "fuseblk":                                                # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
                try:
                    disk_for_file_system = "/dev/" + disk
                    disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
                except:
                    pass
            if disk in swap_disk_list:
                disk_file_system = _tr("[SWAP]")
            storage_data_row.append(disk_file_system)
        # Get disk total size
        if 6 in storage_treeview_columns_shown:
            with open("/sys/class/block/" + disk + "/size") as reader:
                disk_total_size = int(reader.read()) * disk_sector_size
            storage_data_row.append(disk_total_size)
        # Get disk free space
        if 7 in storage_treeview_columns_shown:
            if disk_mount_point != _tr("[Not mounted]"):
                statvfs_disk_usage_values = os.statvfs(disk_mount_point)
                fragment_size = statvfs_disk_usage_values.f_frsize
                disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
            else:
                disk_available = -9999                                                        # "-9999" value is used as "disk_available" value if disk is not mounted. Code will recognize this value and show "[Not mounted]" information in this situation. This negative integer value is used instead of string value because this data colmn of the treestore is an integer typed column.
            storage_data_row.append(disk_available)
        # Get disk used space
        if 8 in storage_treeview_columns_shown:
            if disk_mount_point != _tr("[Not mounted]"):
                statvfs_disk_usage_values = os.statvfs(disk_mount_point)
                fragment_size = statvfs_disk_usage_values.f_frsize
                disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
                disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
                disk_used = disk_size - disk_free
            else:
                disk_used = -9999                                                             # "-9999" value is used as "disk_used" value if disk is not mounted. Code will recognize this value and show "[Not mounted]" information in this situation. This negative integer value is used instead of string value because this data colmn of the treestore is an integer typed column.
            storage_data_row.append(disk_used)
        # Get disk used space percentage
        if 9 in storage_treeview_columns_shown:
            if disk_mount_point != _tr("[Not mounted]"):
                statvfs_disk_usage_values = os.statvfs(disk_mount_point)
                fragment_size = statvfs_disk_usage_values.f_frsize
                disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
                # disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
                disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
                disk_used = disk_size - disk_free
                disk_usage_percent = disk_used / disk_size * 100                              # Gives same result with "lsblk" command (mass storage values)
                # disk_usage_percent = disk_used / (disk_available + disk_used) * 100         # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values (same with "df" command output values). This is real usage percent.
            else:
                disk_usage_percent = -9999                                                    # "-9999" value is used as "disk_usage_percent" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation. This negative integer value is used instead of string value because this data colmn of the treestore is an integer typed column.
            storage_data_row.append(disk_usage_percent)
        # Get disk vendor and model
        if 10 in storage_treeview_columns_shown:
            disk_vendor_model = "-"                                                           # Initial value of "disk_vendor_model" variable. This value will be used if disk vendor and model could not be detected. The same value is also used for disk partitions.
            if disk_type == _tr("Disk"):
                try:
                    with open("/sys/class/block/" + disk + "/device/vendor") as reader:
                        disk_vendor = reader.read().strip()
                    with open("/sys/class/block/" + disk + "/device/model") as reader:
                        disk_model = reader.read().strip()
                    disk_vendor_model = disk_vendor + " - " +  disk_model
                except:
                    disk_vendor_model = "-"
            storage_data_row.append(disk_vendor_model)
        # Get disk label
        if 11 in storage_treeview_columns_shown:
            disk_label = "-"                                                                  # Initial value of "disk_label" variable. This value will be used if disk label could not be detected.
            try:
                disk_label_list = os.listdir("/dev/disk/by-label/")
                for label in disk_label_list:
                    if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == disk:
                        disk_label = bytes(label, "utf-8").decode("unicode_escape")           # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
            except FileNotFoundError:
                pass
            storage_data_row.append(disk_label)
        # Get disk partition label
        if 12 in storage_treeview_columns_shown:
            disk_partition_label = "-"                                                        # Initial value of "disk_partition_label" variable. This value will be used if disk partition label could not be detected.
            try:
                disk_partition_label_list = os.listdir("/dev/disk/by-partlabel/")
                for label in disk_partition_label_list:
                    if os.path.realpath("/dev/disk/by-partlabel/" + label).split("/")[-1] == disk:
                        disk_partition_label = label
            except FileNotFoundError:
                pass
            storage_data_row.append(disk_partition_label)
        # Append disk mount point
        if 13 in storage_treeview_columns_shown:
            storage_data_row.append(disk_mount_point)
        # Get disk path
        if 14 in storage_treeview_columns_shown:
            disk_path = "-"                                                                   # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
            if os.path.exists("/dev/" + disk) == True:
                disk_path = "/dev/" + disk
            storage_data_row.append(disk_path)
        # Get disk revision
        if 15 in storage_treeview_columns_shown:
            disk_revision = "-"                                                               # Initial value of "disk_revision" variable. This value will be used if disk revision could not be detected. Disk partitions do not have disk revision.
            if disk_type == _tr("Disk"):
                try:
                    with open("/sys/class/block/" + disk + "/device/rev") as reader:
                        disk_revision = reader.read().strip()
                except:
                    pass
            storage_data_row.append(disk_revision)
        # Get disk serial number
        if 16 in storage_treeview_columns_shown:
            disk_serial_number = "-"                                                          # Initial value of "disk_serial_number" variable. This value will be used if disk serial number could not be detected.
            if disk_type == _tr("Disk"):
                disk_id_list = os.listdir("/dev/disk/by-id/")
                for id in disk_id_list:
                    if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == disk and ("/dev/disk/by-id/" + id).startswith("wwn-") == False:
                        disk_serial_number = id.split("-")[-1]
                        if "part" in disk_serial_number:
                            disk_serial_number = id.split("-")[-2]
            storage_data_row.append(disk_serial_number)
        # Get disk mode (rw, ro, etc.)
        if 17 in storage_treeview_columns_shown:
            disk_mode = "-"                                                                   # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
            if disk_type == _tr("Disk"):
                for line in proc_mounts_lines:
                    line_split = line.split()
                    if line_split[0].split("/")[-1] == disk:
                        disk_mode = line_split[3]
            storage_data_row.append(disk_mode)
        # Get disk removable information
        if 18 in storage_treeview_columns_shown:
            disk_removable = "-"                                                              # Initial value of "disk_removable" variable. This value will be used if disk removable information could not be detected (if disk is a partition).
            if disk_type == _tr("Disk"):
                with open("/sys/class/block/" + disk + "/removable") as reader:
                    disk_removable_as_number = reader.read().strip()
                if disk_removable_as_number == "1":
                    disk_removable = _tr("Yes")
                if disk_removable_as_number == "0":
                    disk_removable = _tr("No")
            storage_data_row.append(disk_removable)
        # Get disk rotational information
        if 19 in storage_treeview_columns_shown:
            disk_rotational = "-"                                                             # Initial value of "disk_rotational" variable. This value will be used if disk rotational information could not be detected (if disk is a partition).
            if disk_type == _tr("Disk"):
                with open("/sys/class/block/" + disk + "/queue/rotational") as reader:
                    disk_rotational_as_number = reader.read().strip()
                if disk_rotational_as_number == "1":
                    disk_rotational = _tr("Yes")
                if disk_rotational_as_number == "0":
                    disk_rotational = _tr("No")
            storage_data_row.append(disk_rotational)
        # Get disk read-only information
        if 20 in storage_treeview_columns_shown:
            disk_read_only = "-"                                                              # Initial value of "disk_read_only" variable. This value will be used if disk read-only information could not be detected (if disk is a partition).
            if disk_type == _tr("Disk"):
                with open("/sys/class/block/" + disk + "/ro") as reader:
                    disk_read_only_as_number = reader.read().strip()
                if disk_read_only_as_number == "1":
                    disk_read_only = _tr("Yes")
                if disk_read_only_as_number == "0":
                    disk_read_only = _tr("No")
            storage_data_row.append(disk_read_only)
        # Get disk UUID
        if 21 in storage_treeview_columns_shown:
            disk_uuid = "-"                                                                   # Initial value of "disk_uuid" variable. This value will be used if disk disk_uuid could not be detected (for example: if an optical drive has no disk).
            try:
                disk_uuid_list = os.listdir("/dev/disk/by-uuid/")
                for uuid in disk_uuid_list:
                    if os.path.realpath("/dev/disk/by-uuid/" + uuid).split("/")[-1] == disk:
                        disk_uuid = uuid
            except FileNotFoundError:
                pass
            storage_data_row.append(disk_uuid)
        # Get disk unique storage id
        if 22 in storage_treeview_columns_shown:
            disk_unique_storage_id = "-"                                                      # Initial value of "disk_read_only" variable. This value will be used if disk read-only information could not be detected (if disk is a virtual disk).
            try:
                disk_id_list = os.listdir("/dev/disk/by-id/")
                for id in disk_id_list:
                    if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == disk and id.startswith("wwn-") == True:
                        disk_unique_storage_id = id.split("wwn-")[1]
            except FileNotFoundError:
                pass
            storage_data_row.append(disk_unique_storage_id)
        # Get disk major:minor device number
        if 23 in storage_treeview_columns_shown:
            disk_maj_min_number = "-"                                                         # Initial value of "disk_maj_min_number" variable. This value will be used if disk major:minor device number could not be detected.
            for line in sys_class_block_disk_uevent_lines:
                if "MAJOR=" in line:
                    disk_major_number = line.split("=")[1]
                if "MINOR=" in line:
                    disk_minor_number = line.split("=")[1]
                    disk_maj_min_number = disk_major_number + ":" + disk_minor_number
                    break
            storage_data_row.append(disk_maj_min_number)
        # Append all data of the storage data into a list which will be appended into a treestore for showing the data on a treeview.
        storage_data_rows.append(storage_data_row)

    # Add/Remove treeview columns appropriate for user preferences
    treeview4101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if storage_treeview_columns_shown != storage_treeview_columns_shown_prev:                 # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview4101.get_columns():                                             # Remove all columns in the treeview.
            treeview4101.remove_column(column)
        for i, column in enumerate(storage_treeview_columns_shown):
            if storage_data_list[column][0] in storage_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + storage_data_list[column][2]
            storage_treeview_column = Gtk.TreeViewColumn(storage_data_list[column][1])        # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(storage_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                if cell_renderer_type == "CellRendererToggle":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererToggle()
                cell_renderer.set_alignment(storage_data_list[column][9][i], 0.5)             # Vertical alignment is set 0.5 in order to leave it as unchanged.
                storage_treeview_column.pack_start(cell_renderer, storage_data_list[column][10][i])    # Set if column will allocate unused space
                storage_treeview_column.add_attribute(cell_renderer, storage_data_list[column][7][i], cumulative_internal_data_id)
                if storage_data_list[column][11][i] != "no_cell_function":
                    storage_treeview_column.set_cell_data_func(cell_renderer, storage_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            storage_treeview_column.set_sizing(2)                                             # Set column sizing (2 = auto sizing which is required for "treeview4101.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            storage_treeview_column.set_sort_column_id(cumulative_sort_column_id)             # Be careful with lists contain same element more than one.
            storage_treeview_column.set_resizable(True)                                       # Set columns resizable by the user when column title button edge handles are dragged.
            storage_treeview_column.set_reorderable(True)                                     # Set columns reorderable by the user when column title buttons are dragged.
            storage_treeview_column.set_min_width(40)                                         # Set minimum column widths as "40 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            storage_treeview_column.connect("clicked", on_column_title_clicked)               # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview4101.append_column(storage_treeview_column)                               # Append column into treeview

        # Get column data types for appending storage data into treestore
        storage_data_column_types = []
        for column in sorted(storage_treeview_columns_shown):
            internal_column_count = len(storage_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                storage_data_column_types.append(storage_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore4101                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore4101 = Gtk.TreeStore()
        treestore4101.set_column_types(storage_data_column_types)                             # Set column types of the columns which will be appended into treestore
        treemodelfilter4101 = treestore4101.filter_new()
        treemodelfilter4101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort4101 = Gtk.TreeModelSort(treemodelfilter4101)
        treeview4101.set_model(treemodelsort4101)
        disk_order_name_time_list_prev = []                                                   # Redefine (clear) "disk_order_name_time_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    treeview4101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if storage_treeview_columns_shown_prev != storage_treeview_columns_shown or storage_data_column_order_prev != storage_data_column_order:
        storage_treeview_columns = treeview4101.get_columns()                                 # Get shown columns on the treeview in order to use this data for reordering the columns.
        storage_treeview_columns_modified = treeview4101.get_columns()
        treeview_column_titles = []
        for column in storage_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for order in reversed(sorted(storage_data_column_order)):                             # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if storage_data_column_order.index(order) <= len(storage_treeview_columns) - 1 and storage_data_column_order.index(order) in storage_treeview_columns_shown:
                column_number_to_move = storage_data_column_order.index(order)
                column_title_to_move = storage_data_list[column_number_to_move][1]
                column_to_move = storage_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                column_title_to_move = column_to_move.get_title()
                for data in storage_data_list:
                    if data[1] == column_title_to_move:
                        treeview4101.move_column_after(column_to_move, None)                  # Column is moved at the beginning of the treeview if "None" is used.

    # Sort storage rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if storage_treeview_columns_shown_prev != storage_treeview_columns_shown or storage_data_row_sorting_column_prev != storage_data_row_sorting_column or storage_data_row_sorting_order != storage_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        storage_treeview_columns = treeview4101.get_columns()                                 # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in storage_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if storage_data_row_sorting_column in storage_treeview_columns_shown:
                for data in storage_data_list:
                    if data[0] == storage_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if storage_data_row_sorting_column not in storage_treeview_columns_shown:
                column_title_for_sorting = storage_data_list[0][1]
            column_for_sorting = storage_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if storage_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if storage_treeview_columns_shown_prev != storage_treeview_columns_shown or storage_data_column_widths_prev != storage_data_column_widths:
        storage_treeview_columns = treeview4101.get_columns()
        treeview_column_titles = []
        for column in storage_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, storage_data in enumerate(storage_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == storage_data[1]:
                   column_width = storage_data_column_widths[i]
                   storage_treeview_columns[j].set_fixed_width(column_width)                  # Set column width in pixels. Fixed width is unset if value is "-1".

    # Get new/deleted(ended) storage for updating treestore/treeview
    disk_order_name_time_list_prev_set = set(tuple(i) for i in disk_order_name_time_list_prev)    # "set(a_list)" could not be used here because this list is a list of sub-lists. 
    disk_order_name_time_list_set = set(tuple(i) for i in disk_order_name_time_list)          # "set(a_list)" could not be used here because this list is a list of sub-lists. 
    deleted_storage = sorted(list(disk_order_name_time_list_prev_set - disk_order_name_time_list_set))
    new_storage = sorted(list(disk_order_name_time_list_set - disk_order_name_time_list_prev_set))
    existing_storage = sorted(list(disk_order_name_time_list_set.intersection(disk_order_name_time_list_prev_set)))
    updated_existing_proc_index = [[disk_order_name_time_list.index(list(i)), disk_order_name_time_list_prev.index(list(i))] for i in existing_storage]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    storage_data_rows_row_length = len(storage_data_rows[0])
    # Append/Remove/Update storage data into treestore
    treeview4101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global storage_search_text, filter_column
    if len(piter_list) > 0:
        for i, j in updated_existing_proc_index:
            if storage_data_rows[i] != storage_data_rows_prev[j]:
                for k in range(1, storage_data_rows_row_length):                              # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                    if storage_data_rows_prev[j][k] != storage_data_rows[i][k]:
                        treestore4101.set_value(piter_list[j], k, storage_data_rows[i][k])
    if len(deleted_storage) > 0:
        for storage in reversed(sorted(list(deleted_storage))):
            treestore4101.remove(piter_list[disk_order_name_time_list_prev.index(list(storage))])
            piter_list.remove(piter_list[disk_order_name_time_list_prev.index(list(storage))])
    if len(new_storage) > 0:
        for storage in new_storage:
            # /// Start /// This block of code is used for determining if the newly added disk/storage will be shown on the treeview (user search actions and/or search customizations and/or "Show only ... disks/partitions" preference affect disk/storage visibility).
            if radiobutton4102.get_active() == True and disk_type_list[disk_order_name_time_list.index(list(storage))] != selected_disk_type:    # Hide disk (set the visibility value as "False") if "Show all non-removable disks/partitions" option is selected on the GUI and disk type is not same with the selection.
                storage_data_rows[disk_order_name_time_list.index(list(storage))][0] = False
            if radiobutton4103.get_active() == True and disk_type_list[disk_order_name_time_list.index(list(storage))] != selected_disk_type:    # Hide disk (set the visibility value as "False") if "Show all removable disks/partitions" option is selected on the GUI and disk type is not same with the selection.
                storage_data_rows[disk_order_name_time_list.index(list(storage))][0] = False
            if radiobutton4104.get_active() == True and disk_type_list[disk_order_name_time_list.index(list(storage))] != selected_disk_type:    # Hide disk (set the visibility value as "False") if "Show all optical and virtual disks/partitions" option is selected on the GUI and disk type is not same with the selection.
                storage_data_rows[disk_order_name_time_list.index(list(storage))][0] = False
            if searchentry4101.get_text() != "":
                storage_search_text = searchentry4101.get_text()
                storage_data_text_in_model = storage_data_rows[disk_order_name_time_list.index(list(storage))][filter_column]
                if storage_search_text not in str(storage_data_text_in_model).lower():        # Hide disk (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the disk data.
                   storage_data_rows[disk_order_name_time_list.index(list(storage))][0] = False
            if disk_type_list[disk_order_name_time_list.index(list(storage))] == storage_image_partition:
                storage_data_rows[disk_order_name_time_list.index(list(storage))][0] = True   # Make visible child disks (partitions). Otherwise stay hidden because "storage_image_partition" does not match with " != selected_disk_type" control which is made when new disk/storage is connected to system.
            # \\\ End \\\ This block of code is used for determining if the newly added disk will be shown on the treeview (user search actions and/or search customizations and/or "SShow all non-removable/removable/optical-virtual disks/partitions" preference affect disk visibility).
            if parent_disk_list[disk_order_name_time_list.index(list(storage))] == "-":       # Disk parent disk name was set as "0" if it has no parent disk. Disk is set as tree root disk if it has no parent disk name. Treeview tree indentation is first level for the tree root disk.
                piter_list.append(treestore4101.append(None, storage_data_rows[disk_order_name_time_list.index(list(storage))]))
            if parent_disk_list[disk_order_name_time_list.index(list(storage))] != "-":
                piter_list.append(treestore4101.append(piter_list[disk_list.index(parent_disk_list[disk_order_name_time_list.index(list(storage))])], storage_data_rows[disk_order_name_time_list.index(list(storage))]))
#             new_storage_path = treestore4101.get_path(piter_list[-1])
#             model = treeview4101.get_model()
#             path = model.convert_child_path_to_path(new_storage_path)
#             treeview4101.expand_row(path, True)
            treeview4101.expand_all()                                                         # New appended row and its children are shown as collapsed on the treeview. All rows are expanded by this code. Only appended row should be expanded and there need to be a working code to do this.
    treeview4101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    if disk_order_name_time_list_prev == []:                                                  # Expand all treeview rows (if treeview items are in tree structured, not list) if this is the first loop of the Storage tab. It expands treeview rows (and children) in all loops if this control is not made. "First loop" control is made by checking if disk_order_name_time_list_prev is empty.
        treeview4101.expand_all()

    disk_order_name_time_list_prev = disk_order_name_time_list                                # For using values in the next loop
    storage_data_rows_prev = storage_data_rows
    storage_treeview_columns_shown_prev = storage_treeview_columns_shown
    storage_data_row_sorting_column_prev = storage_data_row_sorting_column
    storage_data_row_sorting_order_prev = storage_data_row_sorting_order
    storage_data_column_order_prev = storage_data_column_order
    storage_data_column_widths_prev = storage_data_column_widths

    # Get number of partitions and number of all disks/storage/partitions and show these information on the GUI label
    disks_count = disk_type_list.count(storage_image_partition)
    number_of_all_disks_partitions = len(disk_type_list)
    label4101.set_text(_tr("Total: ") + str(number_of_all_disks_partitions) + _tr(" disks/partitions (") + str(disks_count) + _tr(" disks, ") + str(number_of_all_disks_partitions-disks_count) + _tr(" partitions)"))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.


# ----------------------------------- Storage - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_disk_usage(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data == -9999:
        cell.set_property('text', _tr("[Not mounted]"))
    if cell_data != -9999:
        cell.set_property('text', f'{storage_data_unit_converter_func(cell_data, storage_disk_usage_data_unit, storage_disk_usage_data_precision)}')

def cell_data_function_disk_usage_percentage(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data == -9999:
        cell.set_property('text', _tr("[Not mounted]"))
    if cell_data != -9999:
        cell.set_property('text', f'{cell_data:.1f}%')


# ----------------------------------- Storage Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def storage_initial_thread_func():

    GLib.idle_add(storage_initial_func)


# ----------------------------------- Storage Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def storage_loop_thread_func(*args):                                                          # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton4.get_active() == True:
        global storage_glib_source, update_interval                                           # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            storage_glib_source.destroy()                                                     # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        storage_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(storage_loop_func)
        storage_glib_source.set_callback(storage_loop_thread_func)
        storage_glib_source.attach(GLib.MainContext.default())                                # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- Storage Thread Run Function (starts execution of the threads) -----------------------------------
def storage_thread_run_func():

    if "storage_data_rows" not in globals():                                                  # To be able to run initial thread for only one time
        storage_initial_thread = Thread(target=storage_initial_thread_func, daemon=True)
        storage_initial_thread.start()
        storage_initial_thread.join()
    storage_loop_thread = Thread(target=storage_loop_thread_func, daemon=True)
    storage_loop_thread.start()


# ----------------------------------- Storage - Treeview Filter Show All Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def storage_treeview_filter_show_all_func():

    for piter in piter_list:
        treestore4101.set_value(piter, 0, True)
    treeview4101.expand_all()


# ----------------------------------- Storage - Treeview Filter Non-Removable Disks Only Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def storage_treeview_filter_non_removable_disks_only_func():

    global selected_disk_type
    selected_disk_type = storage_image_ssd_hdd
    for piter in piter_list:
        if disk_type_list[piter_list.index(piter)] != selected_disk_type:
            treestore4101.set_value(piter, 0, False)
        if disk_type_list[piter_list.index(piter)] == storage_image_partition:
            treestore4101.set_value(piter, 0, True)
    treeview4101.expand_all()


# ----------------------------------- Storage - Treeview Filter Removable Disks Only Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def storage_treeview_filter_removable_disks_only_func():

    global selected_disk_type
    selected_disk_type = storage_image_removable
    for piter in piter_list:
        if disk_type_list[piter_list.index(piter)] != selected_disk_type:
            treestore4101.set_value(piter, 0, False)
        if disk_type_list[piter_list.index(piter)] == storage_image_partition:
            treestore4101.set_value(piter, 0, True)
    treeview4101.expand_all()


# ----------------------------------- Storage - Treeview Filter Optical/Virtual Disks Only Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def storage_treeview_filter_optical_virtual_disks_only_func():

    global selected_disk_type
    selected_disk_type = storage_image_optical
    for piter in piter_list:
        if disk_type_list[piter_list.index(piter)] != selected_disk_type:
            treestore4101.set_value(piter, 0, False)
        if disk_type_list[piter_list.index(piter)] == storage_image_partition:
            treestore4101.set_value(piter, 0, True)
    treeview4101.expand_all()


# ----------------------------------- Storage - Treeview Filter Search Function (updates treeview shown rows when text typed into entry) -----------------------------------
def storage_treeview_filter_search_func():

    global filter_column
    storage_search_text = searchentry4101.get_text().lower()
    # Set visible/hidden storage/disk
    for piter in piter_list:
        treestore4101.set_value(piter, 0, False)
        storage_data_text_in_model = treestore4101.get_value(piter, filter_column)
        if storage_search_text in str(storage_data_text_in_model).lower():
            treestore4101.set_value(piter, 0, True)
        if treestore4101.get_value(piter, 0) == True:                                         # Make parent disk visible if one of its children is visible.
            piter_parent = treestore4101.iter_parent(piter)
            while piter_parent != None:
                treestore4101.set_value(piter_parent, 0, True)
                piter_parent = treestore4101.iter_parent(piter_parent)

    treeview4101.expand_all()                                                                 # Expand all treeview rows (if tree view is preferred) after filtering is applied (after any text is typed into search entry).


# ----------------------------------- Storage - Column Title Clicked Function (gets treeview column number (id) and row sorting order by being triggered by Gtk signals) -----------------------------------
def on_column_title_clicked(widget):

    storage_data_row_sorting_column_title = widget.get_title()                                # Get column title which will be used for getting column number
    for data in storage_data_list:
        if data[1] == storage_data_row_sorting_column_title:
            Config.storage_data_row_sorting_column = data[0]                                  # Get column number
    Config.storage_data_row_sorting_order = int(widget.get_sort_order())                      # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Storage - Treeview Column Order-Width Row Sorting Function (gets treeview column order/widths and row sorting) -----------------------------------
def storage_treeview_column_order_width_row_sorting_func():
    # Columns in the treeview are get one by one and appended into "storage_data_column_order". "storage_data_column_widths" list elements are modified for widths of every columns in the treeview. Length of these list are always same even if columns are removed, appended and column widths are changed. Only values of the elements (element indexes are always same with "storage_data") are changed if column order/widths are changed.
    storage_treeview_columns = treeview4101.get_columns()
    treeview_column_titles = []
    for column in storage_treeview_columns:
        treeview_column_titles.append(column.get_title())
    for i, storage_data in enumerate(storage_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == storage_data[1]:
                Config.storage_data_column_order[i] = j
                Config.storage_data_column_widths[i] = storage_treeview_columns[j].get_width()
                break
    Config.config_save_func()


# ----------------------------------- Storage - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def storage_define_data_unit_converter_variables_func():

    global data_unit_list

    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently.

    # Unit Name    Abbreviation    bytes   
    # byte         B               1
    # kilobyte     KB              1024
    # megabyte     MB              1.04858E+06
    # gigabyte     GB              1.07374E+09
    # terabyte     TB              1.09951E+12
    # petabyte     PB              1.12590E+15
    # exabyte      EB              1.15292E+18

    # Unit Name    Abbreviation    bytes    
    # bit          b               8
    # kilobit      Kb              8192
    # megabit      Mb              8,38861E+06
    # gigabit      Gb              8,58993E+09
    # terabit      Tb              8,79609E+12
    # petabit      Pb              9,00720E+15
    # exabit       Eb              9,22337E+18

    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Storage - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def storage_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit in [0, 8]:                                                                        # "if unit in [0, 8]:" is about %25 faster than "if unit == 0 or unit == 8:".
        unit_counter = unit + 1
        while data > 1024:
            unit_counter = unit_counter + 1
            data = data/1024
        unit = data_unit_list[unit_counter][2]
        if data == 0:
            precision = 0
        return f'{data:.{precision}f} {unit}'

    data = data / data_unit_list[unit][1]
    unit = data_unit_list[unit][2]
    if data == 0:
        precision = 0
    return f'{data:.{precision}f} {unit}'
