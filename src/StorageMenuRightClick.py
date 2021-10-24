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
        storage_disk_parent_child_disk_mount_point_etc_func()
        if disk_mount_point != _tr("[Not mounted]"):
            (subprocess.check_output(["xdg-open", disk_mount_point], shell=False)).decode()
        if disk_mount_point == _tr("[Not mounted]"):
            storage_disk_not_mounted_error_dialog()

    def on_menuitem4102m_activate(widget):                                                    # "Mount" item on the right click menu
        storage_disk_parent_child_disk_mount_point_etc_func()
        global disk_mount_point, disk_path
        if disk_mount_point != _tr("[Not mounted]"):
            storage_disk_action_warning_dialog(_tr("Disk is already mounted."))
            return
        if disk_mount_point == _tr("[Not mounted]"):
            try:
                remove_output = (subprocess.check_output(["udisksctl", "mount", "-b", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
            except subprocess.CalledProcessError as e:                                        # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())          # Convert bytes to string by using ".decode("utf-8")".

    def on_menuitem4103m_activate(widget):                                                    # "Unmount" item on the right click menu
        storage_disk_parent_child_disk_mount_point_etc_func()
        global disk_mount_point, disk_path
        if disk_mount_point == _tr("[Not mounted]"):
            storage_disk_action_warning_dialog(_tr("Disk is already unmounted."))
            return
        if disk_mount_point != _tr("[Not mounted]"):
            try:
                remove_output = (subprocess.check_output(["udisksctl", "unmount", "-b", disk_path], stderr=subprocess.STDOUT, shell=False)).decode().strip()
            except subprocess.CalledProcessError as e:                                        # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())          # Convert bytes to string by using ".decode("utf-8")".

    def on_menuitem4104m_activate(widget):                                                    # "Remove" item on the right click menu
        storage_disk_parent_child_disk_mount_point_etc_func()
        # Unmount child disks of the right clicked disk
        global disk_name
        if disk_file_system != "-":
            child_disk_list.append(disk_name)
        for disk in child_disk_list:
            disk_mount_point_local = _tr("[Not mounted]")                                     # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
            for line in proc_mounts_lines:
                line_split = line.split()
                if line_split[0].split("/")[-1] == disk:
                    disk_mount_point_local = bytes(line_split[1], "utf-8").decode("unicode_escape")    # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                    break
            if disk_mount_point_local != _tr("[Not mounted]"):                                # Check if disk is mounted.
                if os.path.exists("/dev/" + disk) == True:
                    disk_path_local = "/dev/" + disk
                else:
                    return
                try:
                    remove_output = (subprocess.check_output(["udisksctl", "unmount", "-b", disk_path_local], stderr=subprocess.STDOUT, shell=False)).decode().strip()    # Unmount disk
                except subprocess.CalledProcessError as e:                                    # Some disks do not have a mountable file system. A warning (Object /org/freedesktop/UDisks2/block_devices/[DISK_NAME] is not a mountable filesystem.) is given by "udisksctl" application for these disks.
                    storage_disk_action_warning_dialog(e.output.decode("utf-8").strip())      # Convert bytes to string by using ".decode("utf-8")".
        # Remove the right clicked disk
        global disk_path
        if disk_path != "-":                                                                  # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
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
        storage_disk_parent_child_disk_mount_point_etc_func()
        global disk_mount_point
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
def storage_disk_parent_child_disk_mount_point_etc_func():

    global disk_name
    disk_name = Storage.selected_storage_kernel_name
    # Get all disks (disks and partitions) including physical, optical and virtual disks
    global disk_list
    disk_list = Storage.disk_list
    # Get disk mount points which will be used for passing mounting operation if disk is already mounted.
    global proc_mounts_lines, disk_mount_point
    with open("/proc/mounts") as reader:
        proc_mounts_lines = reader.read().strip().split("\n")
    disk_mount_point = _tr("[Not mounted]")                                                   # Initial value of "disk_mount_point" variable. This value will be used if disk mount point could not be detected.
    for line in proc_mounts_lines:
        line_split = line.split()
        if line_split[0].split("/")[-1] == disk_name:
            disk_mount_point = bytes(line_split[1], "utf-8").decode("unicode_escape")         # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
    # Get disk type to use for getting parent disk name
    with open("/sys/class/block/" + disk_name + "/uevent") as reader:
        sys_class_block_disk_uevent_lines = reader.read().split("\n")
    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            disk_type = _tr(line.split("=")[1].capitalize())
            break
    # Get parent disk name of the right clicked disk
    global disk_parent_name
    disk_parent_name = "-"                                                                    # Initial value of "disk_parent_name" variable. This value will be used if disk has no parent disk or disk parent name could not be detected.
    if disk_type == _tr("Partition"):
        for disk in disk_list:
            if os.path.isdir("/sys/class/block/" + disk + "/" + disk_name) == True:
                disk_parent_name = disk
    # Get child disks of the right clicked disk
    global child_disk_list
    child_disk_list = []
    for disk in disk_list:
        if os.path.isdir("/sys/class/block/" + disk_name + "/" + disk) == True:
            child_disk_list.append(disk)
    # Get disk path
    global disk_path
    disk_path = "-"                                                                           # Initial value of "disk_path" variable. This value will be used if disk path could not be detected.
    if os.path.exists("/dev/" + disk_name) == True:
        disk_path = "/dev/" + disk_name
    # Get disk file system
    global disk_file_system
    disk_file_system = (subprocess.check_output(["lsblk", disk_path, "-no", "FSTYPE"], shell=False)).decode().split("\n")[0].strip().lower()    # ".split("\n")[0]" is used in order to get correct line if file system of a parent disk is tried to get. Else, it will give parent and child disk filsystems in different lines.
    if disk_file_system == "":
        disk_file_system = "-"
    # Set right click menu items sensitive or insensitive for preventing errorenous user actions. For example, mounting parent disks or removing partitions are prevented.
    if (disk_file_system != "-" and disk_parent_name != "-" and child_disk_list == []) or (disk_file_system != "-" and disk_parent_name == "-" and child_disk_list == []):    # Checking only "disk_file_system" is not adequate for determining if disk has a mountable filesystem. For example, disk may be a parent loop disk and it is not mountable even if it gives "iso9660 as filesystem.
        menuitem4101m.set_sensitive(True)
        menuitem4102m.set_sensitive(True)
        menuitem4103m.set_sensitive(True)
    else:
        menuitem4101m.set_sensitive(False)
        menuitem4102m.set_sensitive(False)
        menuitem4103m.set_sensitive(False)

    if disk_parent_name == "-":
        menuitem4104m.set_sensitive(True)
    if disk_parent_name != "-":
        menuitem4104m.set_sensitive(False)


# ----------------------------------- Storage - Storage Disk Not Mounted Error Dialog Function (shows an error dialog when a disk with no mount point is tried to be browsed) -----------------------------------
def storage_disk_not_mounted_error_dialog():

    error_dialog4101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Disk Is Not Mounted"), )
    error_dialog4101.format_secondary_text(_tr("The disk you have tried to browse is not mounted.") +
                                           "\n" +
                                           _tr("Disk have to be mounted before browsing.") +
                                           "\n\n" + _tr("Note: Some disks such as parent disks or swap disks do not have mount points."))
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
