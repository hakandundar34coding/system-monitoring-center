#!/usr/bin/env python3

# ----------------------------------- Storage - Storage Rename Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def storage_rename_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Storage, MainGUI
    import Storage, MainGUI


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


# ----------------------------------- Storage - Storage Rename Window GUI Function (the code of this module in order to avoid running them during module import and defines "Storage" tab GUI objects and functions/signals) -----------------------------------
def storage_rename_gui_func():

    global builder4101w2, window4101w2
    global entry4101w2, label4101w2, label4102w2, button4101w2, button4102w2


    # Storage Rename window GUI objects - get
    builder4101w2 = Gtk.Builder()
    builder4101w2.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StorageRenameWindow.ui")

    window4101w2 = builder4101w2.get_object('window4101w2')
    entry4101w2 = builder4101w2.get_object('entry4101w2')
    label4101w2 = builder4101w2.get_object('label4101w2')
    label4102w2 = builder4101w2.get_object('label4102w2')
    button4101w2 = builder4101w2.get_object('button4101w2')
    button4102w2 = builder4101w2.get_object('button4102w2')


    # Storage Rename window GUI functions
    def on_window4101w2_delete_event(widget, event):
        window4101w2.hide()
        return True

    def on_window4101w2_show(widget):
        global disk_name
        disk_name = Storage.selected_storage_kernel_name
        label4101w2.set_text(disk_name)
        disk_label = ""                                                                       # Initial value of "disk_label" variable. This value will be used if disk label could not be detected.
        try:
            disk_label_list = os.listdir("/dev/disk/by-label/")
            for label in disk_label_list:
                if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == disk_name:
                    disk_label = bytes(label, "utf-8").decode("unicode_escape")               # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
        except FileNotFoundError:
            pass
        entry4101w2.set_text(disk_label)

    def on_entry4101w2_changed(widget):
        label4102w2.set_text(" ")                                                             # Reset warning information (it is shown if disk file system label is tried to be renamed after disk is removed) label after entry text is changed.
        label4102w2.modify_fg(Gtk.StateFlags.NORMAL, None)                                    # Reset warning information (it is shown if disk file system label is tried to be renamed after disk is removed) label color after entry text is changed.

    def on_button4101w2_clicked(widget):                                                      # "Cancel" button
        window4101w2.hide()

    def on_button4102w2_clicked(widget):                                                      # "Apply" button
        new_label = entry4101w2.get_text()
        if new_label == "":
            new_label = '""'                                                                  # Not string can not be used for deleting labels because of the its applications. "" have to be used in the commandline for deleting labels. '""' value is used for deleting labels of the file systems if no text is get from the entry.
        try:
            disk_filesystem = (subprocess.check_output("lsblk /dev/" + disk_name + " -no FSTYPE", shell=True).strip()).decode().lower()    # Get disk file system for determining which application will be used for renaming operation. Different applications (commands) are used for renaming disks with different file systems.
            if disk_filesystem == "ntfs":
                os.system("pkexec sudo ntfslabel /dev/" + disk_name + " " + new_label)        # "pkexec" is used for running application as root by using polkit authentication window. "pkexec" is used with "sudo" because some applications such as "ntfslabel" do not work without "sudo" is used.
            if disk_filesystem == "ex2" or disk_filesystem == "ex3" or disk_filesystem == "ex4":
                os.system("pkexec sudo e2label /dev/" + disk_name + " " + new_label)
            if disk_filesystem == "mkswap":
                os.system("pkexec sudo mkswap -L " + new_label + " /dev/" + disk_name)        # For renaming labels of "swap"disks
            if disk_filesystem == "exfat":
                os.system("pkexec sudo exfatlabel /dev/" + disk_name + " " + new_label)
            if disk_filesystem == "fat" or disk_filesystem == "vfat":
                os.system("pkexec sudo fatlabel /dev/" + disk_name + " " + new_label)
        except subprocess.CalledProcessError:
            # Get all disks (disks and partitions) including physical, optical and virtual disks for checking if disk is not removed.
            with open("/proc/partitions") as reader:
                proc_partitions_lines = reader.read().split("\n")[2:-1]                       # Get without first 2 lines (header line and an empty line).
            disk_list = []
            for line in proc_partitions_lines:
                disk_list.append(line.split()[3])
            if disk_name not in disk_list:                                                    # Perform following actions if disk is removed.
                label4102w2.set_text(_tr("Disk has been removed and file system could not be renamed."))    # Show warning information if disk file system label is tried to be renamed after disk is removed.
                label4102w2.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))          # Change color of warning information text to "red" if disk file system label is tried to be renamed after disk is removed.
                return                                                                        # For preventing code from closing the window.
        window4101w2.hide()



    # Storage Rename window GUI functions - connect
    window4101w2.connect("delete-event", on_window4101w2_delete_event)
    window4101w2.connect("show", on_window4101w2_show)
    entry4101w2.connect("changed", on_entry4101w2_changed)
    button4101w2.connect("clicked", on_button4101w2_clicked)
    button4102w2.connect("clicked", on_button4102w2_clicked)
