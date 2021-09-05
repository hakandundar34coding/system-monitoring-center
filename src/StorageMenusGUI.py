#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, MainGUI, Storage, StorageGUI, StorageDetails, StorageDetailsGUI, StorageRenameGUI
    import Config, MainGUI, Storage, StorageGUI, StorageDetails, StorageDetailsGUI, StorageRenameGUI


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


# ----------------------------------- Storage - Storage Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Storage" tab menu/popover GUI objects and functions/signals) -----------------------------------
def storage_menus_gui_func():

    # Define builder and get all objects (Storage tab right click menu, Storage tab customizations popover, Storage tab search customizations popover) from GUI file.
    builder4101m = Gtk.Builder()
    builder4101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageMenus.glade")


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Processes tab right click menu
    # ********************** Define object names for Storage tab right click menu **********************
    global menu4101m
    global menuitem4101m, menuitem4102m, menuitem4103m, menuitem4104m, menuitem4106m, menuitem4107m, menuitem4108m

    # ********************** Get object names for Storage tab right click menu **********************
    menu4101m = builder4101m.get_object('menu4101m')
    menuitem4101m = builder4101m.get_object('menuitem4101m')
    menuitem4102m = builder4101m.get_object('menuitem4102m')
    menuitem4103m = builder4101m.get_object('menuitem4103m')
    menuitem4104m = builder4101m.get_object('menuitem4104m')
    menuitem4106m = builder4101m.get_object('menuitem4106m')
    menuitem4107m = builder4101m.get_object('menuitem4107m')
    menuitem4108m = builder4101m.get_object('menuitem4108m')

    # ********************** Define object functions for Storage tab right click menu **********************
    def on_menu4101m_show(widget):
        pass

    def on_menuitem4101m_activate(widget):                                                    # "Browse" item on the right click menu
        disk_name = StorageGUI.selected_storage_kernel_name
        with open("/proc/mounts") as reader:                                                  # Read "/proc/mounts" file in order to get disk mount point.
            proc_mounts_lines = reader.read().strip().split("\n")
        disk_mount_point = "[Not mounted]"                                                    # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
        for line in proc_mounts_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == disk_name:
                disk_mount_point = bytes(line_split[1], "utf-8").decode("unicode_escape")     # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
        if disk_mount_point != "[Not mounted]":
            os.system('xdg-open "%s"' % disk_mount_point)
        if disk_mount_point == "[Not mounted]":
            storage_disk_not_mounted_error_dialog()

    def on_menuitem4102m_activate(widget):                                                    # "Mount" item on the right click menu
        disk_name = StorageGUI.selected_storage_kernel_name
        # Get all disks (disks and partitions) including physical, optical and virtual disks
        with open("/proc/partitions") as reader:
            proc_partitions_lines = reader.read().split("\n")[2:-1]                           # Get without first 2 lines (header line and an empty line).
        disk_list = []
        for line in proc_partitions_lines:
            disk_list.append(line.split()[3])
        # Get disk mount points which will be used for passing mounting operation if disk is already mounted.
        with open("/proc/mounts") as reader:
            proc_mounts_lines = reader.read().strip().split("\n")
        # Get Right clicked disk and its child disks (if it has child disks)
        disk_and_child_disks_list = [disk_name]
        for disk in disk_list:
            if os.path.isdir("/sys/class/block/" + disk_name + "/" + disk) == True:
                disk_and_child_disks_list.append(disk)
        # Try mounting right clicked disk and its child disks (if it has child disks)
        for disk in disk_and_child_disks_list:
            disk_mount_point = "[Not mounted]"                                                # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
            for line in proc_mounts_lines:
                line_split = line.split()
                if line_split[0].split("/")[-1] == disk:
                    disk_mount_point = line_split[1]
            if disk_mount_point != "[Not mounted]":                                           # Skip to next loop (skip this disk) if disk is already mounted.
                continue
            disk_path = "-"                                                                   # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
            if os.path.exists("/dev/" + disk) == True:
                disk_path = "/dev/" + disk
            if disk_path != "-":             
                try:
                    (subprocess.check_output("udisksctl mount -b " + disk_path, shell=True).strip()).decode()
                except subprocess.CalledProcessError:                                         # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                    pass

    def on_menuitem4103m_activate(widget):                                                    # "Unmount" item on the right click menu
        disk_name = StorageGUI.selected_storage_kernel_name
        # Get all disks (disks and partitions) including physical, optical and virtual disks
        with open("/proc/partitions") as reader:
            proc_partitions_lines = reader.read().split("\n")[2:-1]                           # Get without first 2 lines (header line and an empty line).
        disk_list = []
        for line in proc_partitions_lines:
            disk_list.append(line.split()[3])
        # Get disk mount points which will be used for passing mounting operation if disk is already unmounted.
        with open("/proc/mounts") as reader:
            proc_mounts_lines = reader.read().strip().split("\n")
        # Get Right clicked disk and its child disks (if it has child disks)
        disk_and_child_disks_list = [disk_name]
        for disk in disk_list:
            if os.path.isdir("/sys/class/block/" + disk_name + "/" + disk) == True:
                disk_and_child_disks_list.append(disk)
        # Try mounting right clicked disk and its child disks (if it has child disks)
        for disk in disk_and_child_disks_list:
            disk_mount_point = "[Not mounted]"                                                # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
            for line in proc_mounts_lines:
                line_split = line.split()
                if line_split[0].split("/")[-1] == disk:
                    disk_mount_point = line_split[1]
            if disk_mount_point == "[Not mounted]":                                           # Skip to next loop (skip this disk) if disk is already unmounted.
                continue
            disk_path = "-"                                                                   # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
            if os.path.exists("/dev/" + disk) == True:
                disk_path = "/dev/" + disk
            if disk_path != "-":             
                try:
                    (subprocess.check_output("udisksctl unmount -b " + disk_path, shell=True).strip()).decode()
                except subprocess.CalledProcessError:                                         # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                    pass

    def on_menuitem4104m_activate(widget):                                                    # "Remove" item on the right click menu
        on_menuitem4103m_activate(menuitem4103m)
        disk_name = StorageGUI.selected_storage_kernel_name
        disk_path = "-"                                                                       # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
        if os.path.exists("/dev/" + disk_name) == True:
            disk_path = "/dev/" + disk_name
        if disk_path != "-":
            if "loop" in disk_name:                                                           # "Remove" operation ("delete loop" operation for optical disks) for loop (virtual disk) devices.
                (subprocess.check_output("udisksctl loop-delete -b " + disk_path, shell=True).strip()).decode()
                return
            if "sr" in disk_name:                                                             # "Remove" operation ("eject" operation for optical disk disks) for optical disk drives.
                (subprocess.check_output("eject " + disk_name, shell=True).strip()).decode()
                return
            if "loop" not in disk_name or "sr" not in disk_name:                              # "Remove" operation ("power off" operation) for non-virtual (loop devices) disks and non-optical disk drives. This operations method is used for USB disks, external HDDs/SSDs, etc.
                (subprocess.check_output("udisksctl power-off -b " + disk_path, shell=True).strip()).decode()

    def on_menuitem4106m_activate(widget):                                                    # "Copy Mount Point" item on the right click menu
        disk_name = StorageGUI.selected_storage_kernel_name
        with open("/proc/mounts") as reader:                                                  # Read "/proc/mounts" file in order to get disk mount point.
            proc_mounts_lines = reader.read().strip().split("\n")
        disk_mount_point = "[Not mounted]"                                                    # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
        for line in proc_mounts_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == disk_name:
                disk_mount_point = line_split[1].replace("\\040", " ")                        # Replace ""\\040"" whitespace character with " " if it exists.
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(disk_mount_point, -1)
        clipboard.store()                                                                     # Stores copied text in the clipboard. Therefore text stays in the clipboard after application has quit.

    def on_menuitem4107m_activate(widget):                                                    # "Rename Label" item on the right click menu
        disk_name = StorageGUI.selected_storage_kernel_name
        StorageRenameGUI.window4101w2.show()

    def on_menuitem4108m_activate(widget):                                                    # "Details" item on the right click menu
        StorageDetailsGUI.storage_details_gui_function()
        StorageDetailsGUI.window4101w.show()
        StorageDetails.storage_details_foreground_thread_run_func()

    # ********************** Connect signals to GUI objects for Storage tab right click menu **********************
    menu4101m.connect("show", on_menu4101m_show)
    menuitem4101m.connect("activate", on_menuitem4101m_activate)
    menuitem4102m.connect("activate", on_menuitem4102m_activate)
    menuitem4103m.connect("activate", on_menuitem4103m_activate)
    menuitem4104m.connect("activate", on_menuitem4104m_activate)
    menuitem4106m.connect("activate", on_menuitem4106m_activate)
    menuitem4107m.connect("activate", on_menuitem4107m_activate)
    menuitem4108m.connect("activate", on_menuitem4108m_activate)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Storage tab customizations popover
    # ********************** Define object names for Storage tab customizations popover **********************
    global popover4101p
    global checkbutton4101p, checkbutton4102p, checkbutton4103p, checkbutton4104p, checkbutton4105p, checkbutton4106p
    global checkbutton4107p, checkbutton4108p, checkbutton4109p, checkbutton4110p, checkbutton4111p, checkbutton4112p
    global checkbutton4113p, checkbutton4114p, checkbutton4115p, checkbutton4116p, checkbutton4117p, checkbutton4118p
    global checkbutton4119p, checkbutton4120p, checkbutton4121p, checkbutton4122p, checkbutton4123p, checkbutton4124p
    global button4101p, button4102p
    global combobox4101p, combobox4102p

    # ********************** Get object names for Storage tab customizations popover **********************
    popover4101p = builder4101m.get_object('popover4101p')
    checkbutton4101p = builder4101m.get_object('checkbutton4101p')
    checkbutton4102p = builder4101m.get_object('checkbutton4102p')
    checkbutton4103p = builder4101m.get_object('checkbutton4103p')
    checkbutton4104p = builder4101m.get_object('checkbutton4104p')
    checkbutton4105p = builder4101m.get_object('checkbutton4105p')
    checkbutton4106p = builder4101m.get_object('checkbutton4106p')
    checkbutton4107p = builder4101m.get_object('checkbutton4107p')
    checkbutton4108p = builder4101m.get_object('checkbutton4108p')
    checkbutton4109p = builder4101m.get_object('checkbutton4109p')
    checkbutton4110p = builder4101m.get_object('checkbutton4110p')
    checkbutton4111p = builder4101m.get_object('checkbutton4111p')
    checkbutton4112p = builder4101m.get_object('checkbutton4112p')
    checkbutton4113p = builder4101m.get_object('checkbutton4113p')
    checkbutton4114p = builder4101m.get_object('checkbutton4114p')
    checkbutton4115p = builder4101m.get_object('checkbutton4115p')
    checkbutton4116p = builder4101m.get_object('checkbutton4116p')
    checkbutton4117p = builder4101m.get_object('checkbutton4117p')
    checkbutton4118p = builder4101m.get_object('checkbutton4118p')
    checkbutton4119p = builder4101m.get_object('checkbutton4119p')
    checkbutton4120p = builder4101m.get_object('checkbutton4120p')
    checkbutton4121p = builder4101m.get_object('checkbutton4121p')
    checkbutton4122p = builder4101m.get_object('checkbutton4122p')
    checkbutton4123p = builder4101m.get_object('checkbutton4123p')
    checkbutton4124p = builder4101m.get_object('checkbutton4124p')
    button4101p = builder4101m.get_object('button4101p')
    button4102p = builder4101m.get_object('button4102p')
    combobox4101p = builder4101m.get_object('combobox4101p')
    combobox4102p = builder4101m.get_object('combobox4102p')

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
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Storage tab search customizations popover
    # ********************** Define object names for Storage tab search customizations popover **********************
    global popover4101p2
    global radiobutton4101p2, radiobutton4102p2, radiobutton4103p2, radiobutton4104p2, radiobutton4105p2, radiobutton4106p2
    global radiobutton4107p2, radiobutton4108p2
    global checkbutton4101p2, checkbutton4102p2, checkbutton4103p2, checkbutton4104p2

    # ********************** Get object names for Storage tab search customizations popover **********************
    popover4101p2 = builder4101m.get_object('popover4101p2')
    radiobutton4101p2 = builder4101m.get_object('radiobutton4101p2')
    radiobutton4102p2 = builder4101m.get_object('radiobutton4102p2')
    radiobutton4103p2 = builder4101m.get_object('radiobutton4103p2')
    radiobutton4104p2 = builder4101m.get_object('radiobutton4104p2')
    radiobutton4105p2 = builder4101m.get_object('radiobutton4105p2')
    radiobutton4106p2 = builder4101m.get_object('radiobutton4106p2')
    radiobutton4107p2 = builder4101m.get_object('radiobutton4107p2')
    radiobutton4108p2 = builder4101m.get_object('radiobutton4108p2')
    checkbutton4101p2 = builder4101m.get_object('checkbutton4101p2')
    checkbutton4102p2 = builder4101m.get_object('checkbutton4102p2')
    checkbutton4103p2 = builder4101m.get_object('checkbutton4103p2')
    checkbutton4104p2 = builder4101m.get_object('checkbutton4104p2')

    # ********************** Define object functions for Storage tab search customizations popover **********************
    def on_radiobutton4101p2_toggled(widget):
        if radiobutton4101p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4102p2_toggled(widget):
        if radiobutton4102p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4103p2_toggled(widget):
        if radiobutton4103p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4104p2_toggled(widget):
        if radiobutton4104p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4105p2_toggled(widget):
        if radiobutton4105p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4106p2_toggled(widget):
        if radiobutton4106p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4105p2_toggled(widget):
        if radiobutton4105p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4106p2_toggled(widget):
        if radiobutton4106p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4107p2_toggled(widget):
        if radiobutton4107p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_radiobutton4108p2_toggled(widget):
        if radiobutton4108p2.get_active() == True:
            Storage.storage_treeview_filter_search_func()

    def on_checkbutton4101p2_toggled(widget):
        storage_popovers_checkbutton_behavior_func(checkbutton4101p2)

    def on_checkbutton4102p2_toggled(widget):
        storage_popovers_checkbutton_behavior_func( checkbutton4102p2)

    def on_checkbutton4103p2_toggled(widget):
        storage_popovers_checkbutton_behavior_func(checkbutton4103p2)

    def on_checkbutton4104p2_toggled(widget):
        storage_popovers_checkbutton_behavior_func(checkbutton4104p2)

    # ********************** Connect signals to GUI objects for Storage tab search customizations popover **********************
    radiobutton4101p2.connect("toggled", on_radiobutton4101p2_toggled)
    radiobutton4102p2.connect("toggled", on_radiobutton4102p2_toggled)
    radiobutton4103p2.connect("toggled", on_radiobutton4103p2_toggled)
    radiobutton4104p2.connect("toggled", on_radiobutton4104p2_toggled)
    radiobutton4105p2.connect("toggled", on_radiobutton4105p2_toggled)
    radiobutton4106p2.connect("toggled", on_radiobutton4106p2_toggled)
    radiobutton4107p2.connect("toggled", on_radiobutton4107p2_toggled)
    radiobutton4108p2.connect("toggled", on_radiobutton4108p2_toggled)
    global checkbutton4101p2_handler_id, checkbutton4102p2_handler_id, checkbutton4103p2_handler_id, checkbutton4104p2_handler_id
    checkbutton4101p2_handler_id = checkbutton4101p2.connect("toggled", on_checkbutton4101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton4102p2_handler_id = checkbutton4102p2.connect("toggled", on_checkbutton4102p2_toggled)
    checkbutton4103p2_handler_id = checkbutton4103p2.connect("toggled", on_checkbutton4103p2_toggled)
    checkbutton4104p2_handler_id = checkbutton4104p2.connect("toggled", on_checkbutton4104p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Storage tab **********************
    popover4101p.set_relative_to(StorageGUI.button4101)
    popover4101p.set_position(1)
    # ********************** Popover settings for Storage tab search customizations **********************
    popover4101p2.set_relative_to(StorageGUI.button4103)
    popover4101p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



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
    if "liststore4101p" not in globals():                                                 # Check if "liststore4101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
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


# ----------------------------------- Storage - Storage Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def storage_popovers_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton4101p2, checkbutton4102p2, checkbutton4103p2, checkbutton4104p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton4101p2.handler_block(checkbutton4101p2_handler_id) as p1, checkbutton4102p2.handler_block(checkbutton4102p2_handler_id) as p2, checkbutton4103p2.handler_block(checkbutton4103p2_handler_id) as p3, checkbutton4104p2.handler_block(checkbutton4104p2_handler_id) as p4:
        if caller_checkbutton != select_all_checkbutton and caller_checkbutton.get_active() == False:
            if True not in checkbutton_active_state_list:
                caller_checkbutton.set_active(True)
                checkbutton_active_state_list[sub_checkbutton_list.index(caller_checkbutton)] = True
        if caller_checkbutton != select_all_checkbutton and False not in checkbutton_active_state_list:
            select_all_checkbutton.set_active(True)
            select_all_checkbutton.set_inconsistent(False)
        if caller_checkbutton != select_all_checkbutton and False in checkbutton_active_state_list:
            select_all_checkbutton.set_active(False)
            select_all_checkbutton.set_inconsistent(True)
        if select_all_checkbutton.get_active() == True:
            select_all_checkbutton.set_inconsistent(False)
            for i, checkbutton in enumerate(sub_checkbutton_list):
                checkbutton.set_active(True)
                checkbutton_active_state_list[i] = True
        if select_all_checkbutton.get_active() == False:
            if False not in checkbutton_active_state_list:
                select_all_checkbutton.set_active(True)

    if StorageGUI.searchentry4101.get_text() != "":                                         # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the "show all ... disks" radiobuttons above the treeview.
        Storage.storage_treeview_filter_search_func()


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


# ----------------------------------- Storage - Storage Disk Not Mounted Error Dialog Function (shows an error dialog when a disk with no mount point is tried to be browsed) -----------------------------------
def storage_disk_not_mounted_error_dialog():

    error_dialog4101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Disk Is Not Mounted"), )
    error_dialog4101.format_secondary_text(_tr("The disk you have tried to browse is not mounted.\n Disk have to be mounted before browsing.\n Note: Some disks such as swap disks do not have mount points."))
    error_dialog4101.run()
    error_dialog4101.destroy()

# ----------------------------------- Storage - Storage Disk Has No Mountable File System Error Dialog Function (shows an error dialog when a disk with no mountable file system is tried to be mounted/unmounted) -----------------------------------
def storage_disk_has_no_mountable_file_system_error_dialog():

    error_dialog4102 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Disk Has No Mountable File System"), )
    error_dialog4102.format_secondary_text(_tr("The disk you have tried to mount or unmount has no mountable file system.\n\n Note: Some disks such as parent disks, swap disks do not have mountable file systems."))
    error_dialog4102.run()
    error_dialog4102.destroy()
