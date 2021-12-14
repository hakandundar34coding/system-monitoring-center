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
    from . import Storage, MainGUI


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

    global builder, window4101w2
    global entry4101w2, label4101w2, label4102w2, button4101w2, button4102w2


    # Storage Rename window GUI objects - get
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/ui/StorageRenameWindow.ui")

    window4101w2 = builder.get_object('window4101w2')
    entry4101w2 = builder.get_object('entry4101w2')
    label4101w2 = builder.get_object('label4101w2')
    label4102w2 = builder.get_object('label4102w2')
    button4101w2 = builder.get_object('button4101w2')
    button4102w2 = builder.get_object('button4102w2')


    # Storage Rename window GUI functions
    def on_window4101w2_delete_event(widget, event):
        window4101w2.hide()
        return True

    def on_window4101w2_show(widget):
        global disk_name
        disk_name = Storage.selected_storage_kernel_name
        label4101w2.set_text("    " + disk_name)
        disk_label = ""                                                                       # Initial value of "disk_label" variable. This value will be used if disk label could not be detected.
        try:
            disk_label_list = os.listdir("/dev/disk/by-label/")
            for label in disk_label_list:
                if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == disk_name:
                    disk_label = bytes(label, "utf-8").decode("unicode_escape")               # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
        except FileNotFoundError:
            pass
        entry4101w2.set_text(disk_label)
        entry4101w2.set_can_focus(True)                                                       # Set flag to be able to enable grabing focus to be ready for typing directly without clicking on it. Otherwise, entry has to be clicked on it for typing in it.
        entry4101w2.grab_focus()                                                              # Enable grabing focus to be ready for typing directly without clicking on it. Otherwise, entry has to be clicked on it for typing in it.

    def on_entry4101w2_changed(widget):
        label4102w2.set_text(" ")                                                             # Reset warning information (it is shown if disk file system label is tried to be renamed after disk is removed) label after entry text is changed.
        label4102w2.modify_fg(Gtk.StateFlags.NORMAL, None)                                    # Reset warning information (it is shown if disk file system label is tried to be renamed after disk is removed) label color after entry text is changed.

    def on_entry4101w2_activate(widget):
        on_button4102w2_clicked(button4102w2)                                                 # Run "on_button4102w2_clicked" function if "Enter" keyboard button is pressed when entry is focused.

    def on_button4101w2_clicked(widget):                                                      # "Cancel" button
        window4101w2.hide()

    def on_button4102w2_clicked(widget):                                                      # "Apply" button
        # Get disk filesystem for defining the program to be used for renaming. Different programs are used for renaming different filesystems.
        disk_for_file_system = "/dev/" + disk_name
        disk_file_system = (subprocess.check_output(["lsblk", disk_for_file_system, "-no", "FSTYPE"], shell=False)).decode().strip().lower()    # Get disk file system for determining which application will be used for renaming operation. Different applications (commands) are used for renaming disks with different file systems.
        if disk_file_system == "":
            disk_file_system = "-"
        # Get new label from entry.
        new_label = entry4101w2.get_text()
        # Rename or delete labels of the disks. Some filesystems require different methods for deleting filesystem labels. Using "" for deleting the label does not work for them.
        try:
            if disk_file_system == "ntfs":
                if new_label != "" or new_label == "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "ntfslabel", disk_for_file_system, new_label], stderr=subprocess.STDOUT, shell=False)).decode()    # "pkexec" is used for running application as root by using polkit authentication window. "pkexec" is used with "sudo" because some applications such as "ntfslabel" do not work without "sudo" is used.
            elif disk_file_system == "ext2" or disk_file_system == "ext3" or disk_file_system == "ext4":
                if new_label != "" or new_label == "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "e2label", disk_for_file_system, new_label], stderr=subprocess.STDOUT, shell=False)).decode()
            elif disk_file_system == "btrfs":
                action_output = (subprocess.check_output(["pkexec", "sudo", "btrfs", "filesystem", "label", disk_for_file_system, new_label], stderr=subprocess.STDOUT, shell=False)).decode()    # Possibly, same command works for setting new label and deleting it. Additional information for deleting/resetting filsystem label was not found in the man page.
            elif disk_file_system == "mkswap":
                action_output = (subprocess.check_output(["pkexec", "sudo", "mkswap", "-L", new_label, disk_for_file_system], stderr=subprocess.STDOUT, shell=False)).decode()    # For renaming labels of "swap" disks.     # Possibly, same command works for setting new label and deleting it. Additional information for deleting/resetting filsystem label was not found in the man page.
            elif disk_file_system == "exfat":
                if new_label != "" or new_label == "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "exfatlabel", disk_for_file_system, new_label], stderr=subprocess.STDOUT, shell=False)).decode()
            elif disk_file_system == "fat" or disk_file_system == "vfat":
                if new_label == "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "fatlabel", disk_for_file_system, "-r"], stderr=subprocess.STDOUT, shell=False)).decode()
                if new_label != "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "fatlabel", disk_for_file_system, new_label], stderr=subprocess.STDOUT, shell=False)).decode()
            elif disk_file_system == "xfs":
                if new_label == "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "xfs_admin", "-L", "--", new_label, disk_for_file_system], stderr=subprocess.STDOUT, shell=False)).decode()    # For details, see: "https://man7.org/linux/man-pages/man8/xfs_admin.8.html".
                if new_label != "":
                    action_output = (subprocess.check_output(["pkexec", "sudo", "xfs_admin", "-L", new_label, disk_for_file_system], stderr=subprocess.STDOUT, shell=False)).decode()
            elif disk_file_system == "reiserfs":
                action_output = (subprocess.check_output(["pkexec", "sudo", "reiserfstune", "-l", new_label, disk_for_file_system], stderr=subprocess.STDOUT, shell=False)).decode()    # Possibly, same command works for setting new label and deleting it. Additional information for deleting/resetting filsystem label was not found in the man page.
            elif disk_file_system == "jfs":
                action_output = (subprocess.check_output(["pkexec", "sudo", "jfs_tune", "-L", new_label, disk_for_file_system], stderr=subprocess.STDOUT, shell=False)).decode()    # Possibly, same command works for setting new label and deleting it. Additional information for deleting/resetting filsystem label was not found in the man page.
            else:
                storage_rename_action_warning_dialog(_tr("Renaming disks with this file system is not supported.") + "\n\n    " + "File System: " + disk_file_system)
                window4101w2.hide()
                return
            if action_output != "":
                storage_rename_action_warning_dialog(action_output)
        except subprocess.CalledProcessError as e:
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
            if e.output.decode("utf-8").strip() != "":
                storage_rename_action_warning_dialog(e.output.decode("utf-8").strip())        # Convert bytes to string by using ".decode("utf-8")".
        window4101w2.hide()



    # Storage Rename window GUI functions - connect
    window4101w2.connect("delete-event", on_window4101w2_delete_event)
    window4101w2.connect("show", on_window4101w2_show)
    entry4101w2.connect("changed", on_entry4101w2_changed)
    entry4101w2.connect("activate", on_entry4101w2_activate)
    button4101w2.connect("clicked", on_button4101w2_clicked)
    button4102w2.connect("clicked", on_button4102w2_clicked)


# ----------------------------------- Storage - Storage Rename Action Warning Dialog Function (shows a warning dialog when an output text is obtained during disk renaming actions) -----------------------------------
def storage_rename_action_warning_dialog(dialog_text):

    warning_dialog4101w2 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Information"), )
    warning_dialog4101w2.format_secondary_text(dialog_text)
    global warning_dialog4101w2_response
    warning_dialog4101w2_response = warning_dialog4101w2.run()
    warning_dialog4101w2.destroy()
