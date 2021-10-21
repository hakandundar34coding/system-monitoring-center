#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Right Click Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_menu_right_click_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global MainGUI, Storage
    import MainGUI, Storage


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


# ----------------------------------- Storage - Storage Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Storage" tab menu/popover GUI objects and functions/signals) -----------------------------------
def storage_menu_right_click_gui_func():

    # Define builder and get all objects (Storage tab right click menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageMenuRightClick.ui")

    # ********************** Define object names for Storage tab right click menu **********************
    global menu4101m
    global menuitem4101m, menuitem4102m, menuitem4103m, menuitem4104m, menuitem4106m, menuitem4107m, menuitem4108m

    # ********************** Get object names for Storage tab right click menu **********************
    menu4101m = builder.get_object('menu4101m')
    menuitem4101m = builder.get_object('menuitem4101m')
    menuitem4102m = builder.get_object('menuitem4102m')
    menuitem4103m = builder.get_object('menuitem4103m')
    menuitem4104m = builder.get_object('menuitem4104m')
    menuitem4106m = builder.get_object('menuitem4106m')
    menuitem4107m = builder.get_object('menuitem4107m')
    menuitem4108m = builder.get_object('menuitem4108m')

    # ********************** Define object functions for Storage tab right click menu **********************
    def on_menuitem4101m_activate(widget):                                                    # "Browse" item on the right click menu
        disk_name = Storage.selected_storage_kernel_name
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
        storage_disk_child_disk_mount_point_etc_func()
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
                    remove_output = (subprocess.check_output(["udisksctl", "mount", "-b", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
                except subprocess.CalledProcessError as e:                                    # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                    storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())      # Convert bytes to string by using ".decode("utf-8")".

    def on_menuitem4103m_activate(widget):                                                    # "Unmount" item on the right click menu
        storage_disk_child_disk_mount_point_etc_func()
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
                    remove_output = (subprocess.check_output(["udisksctl", "unmount", "-b", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
                except subprocess.CalledProcessError as e:                                    # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                    storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())      # Convert bytes to string by using ".decode("utf-8")".

    def on_menuitem4104m_activate(widget):                                                    # "Remove" item on the right click menu
        on_menuitem4103m_activate(menuitem4103m)                                              # Unmount device before removing it.
        disk_name = Storage.selected_storage_kernel_name
        disk_path = "-"                                                                       # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
        if os.path.exists("/dev/" + disk_name) == True:
            disk_path = "/dev/" + disk_name
        if disk_path != "-":
            if "loop" in disk_name and os.path.isdir("/sys/class/block/" + disk_name + "/loop/") == True:    # "Remove" operation ("delete loop" operation for optical disks) for loop (virtual disk) devices (also if they are not partition).
                try:
                    remove_output = (subprocess.check_output(["udisksctl", "loop-delete", "-b", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
                except subprocess.CalledProcessError as e:
                    storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())      # Convert bytes to string by using ".decode("utf-8")".
                return
            if "sr" in disk_name:                                                             # "Remove" operation ("eject" operation for optical disk disks) for optical disk drives.
                try:
                    remove_output = (subprocess.check_output(["eject", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
                except subprocess.CalledProcessError as e:
                    storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())
                return
            if "loop" not in disk_name and "sr" not in disk_name:                             # "Remove" operation ("power off" operation) for non-virtual (loop devices) disks and non-optical disk drives. This operations method is used for USB disks, external HDDs/SSDs, etc.
                try:
                    remove_output = (subprocess.check_output(["udisksctl", "power-off", "-b", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
                except subprocess.CalledProcessError as e:
                    storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())
                return

    def on_menuitem4106m_activate(widget):                                                    # "Copy Mount Point" item on the right click menu
        disk_name = Storage.selected_storage_kernel_name
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
        disk_name = Storage.selected_storage_kernel_name
        if 'StorageRenameGUI' not in globals():                                               # Check if "StorageRenameGUI" module is imported. Therefore it is not reimported for every click on "Rename Label" menu item if "StorageRenameGUI" name is in globals().
            global StorageRenameGUI
            import StorageRenameGUI
            StorageRenameGUI.storage_rename_import_func()
            StorageRenameGUI.storage_rename_gui_func()
        StorageRenameGUI.window4101w2.show()

    def on_menuitem4108m_activate(widget):                                                    # "Details" item on the right click menu
        if 'StorageDetails' not in globals():                                                 # Check if "StorageDetails" module is imported. Therefore it is not reimported for double click on "Details" menu item on the right click menu if "StorageDetails" name is in globals().
            global StorageDetails
            import StorageDetails
            StorageDetails.storage_details_import_func()
            StorageDetails.storage_details_gui_function()
        StorageDetails.window4101w.show()
        StorageDetails.storage_details_foreground_thread_run_func()

    # ********************** Connect signals to GUI objects for Storage tab right click menu **********************
    menuitem4101m.connect("activate", on_menuitem4101m_activate)
    menuitem4102m.connect("activate", on_menuitem4102m_activate)
    menuitem4103m.connect("activate", on_menuitem4103m_activate)
    menuitem4104m.connect("activate", on_menuitem4104m_activate)
    menuitem4106m.connect("activate", on_menuitem4106m_activate)
    menuitem4107m.connect("activate", on_menuitem4107m_activate)
    menuitem4108m.connect("activate", on_menuitem4108m_activate)


# ----------------------------------- Storage - Storage Disk, Child Disk, Mount Point, etc Function (gets several disk information) -----------------------------------
def storage_disk_child_disk_mount_point_etc_func():

    disk_name = Storage.selected_storage_kernel_name
    # Get all disks (disks and partitions) including physical, optical and virtual disks
    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().split("\n")[2:-1]                               # Get without first 2 lines (header line and an empty line).
    global disk_list
    disk_list = []
    for line in proc_partitions_lines:
        disk_list.append(line.split()[3])
    # Get disk mount points which will be used for passing mounting operation if disk is already mounted.
    global proc_mounts_lines
    with open("/proc/mounts") as reader:
        proc_mounts_lines = reader.read().strip().split("\n")
    # Get Right clicked disk and its child disks (if it has child disks)
    global disk_and_child_disks_list
    disk_and_child_disks_list = [disk_name]
    for disk in disk_list:
        if os.path.isdir("/sys/class/block/" + disk_name + "/" + disk) == True:
            disk_and_child_disks_list.append(disk)


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


# ----------------------------------- Storage - Storage Disk Action Warning Dialog Function (shows a warning dialog when an output text is obtained during disk actions (mount, unmount, remove, etc.)) -----------------------------------
def storage_disk_action_warning_dialog(dialog_text):

    warning_dialog4101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Information"), )
    warning_dialog4101.format_secondary_text(dialog_text)
    global warning_dialog4101_response
    warning_dialog4101_response = warning_dialog4101.run()
    warning_dialog4101.destroy()
