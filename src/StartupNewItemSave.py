#!/usr/bin/env python3

import sys

# Get variables from bash
system_or_current_user_autostart_directory = sys.argv[1]
new_startup_application_file_name = sys.argv[2]
new_startup_application_name = sys.argv[3]
new_startup_application_comment = sys.argv[4]
new_startup_application_command = sys.argv[5]
new_startup_application_icon = sys.argv[6]
new_startup_application_startup_notify = sys.argv[7]
new_startup_application_terminal = sys.argv[8]


# Save ".desktop" file in order to add new startup item
with open(system_or_current_user_autostart_directory + new_startup_application_name + ".desktop", "w") as writer:
    writer.write("[Desktop Entry]" + "\n")
    writer.write("Type=Application" + "\n")
    writer.write("Name=" + new_startup_application_name + "\n")
    if new_startup_application_comment != "":
        writer.write("Comment=" + new_startup_application_comment + "\n")
    writer.write("Exec=" + new_startup_application_command + "\n")
    if new_startup_application_icon != "":
        writer.write("Icon=" + new_startup_application_icon + "\n")
    if new_startup_application_startup_notify == "True":
        writer.write("StartupNotify=true" + "\n")
    if new_startup_application_startup_notify == "False":
        writer.write("StartupNotify=false" + "\n")
    if new_startup_application_terminal == "True":
        writer.write("Terminal=true" + "\n")
    if new_startup_application_terminal == "False":
        writer.write("Terminal=false" + "\n")
