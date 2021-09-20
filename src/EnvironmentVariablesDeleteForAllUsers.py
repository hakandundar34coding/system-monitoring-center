#!/usr/bin/env python3

import sys

# Get variables from bash
variable_to_delete = sys.argv[1]
variable_to_delete_value = sys.argv[2]


# ----------------------------------- Environment Variables - Add Environment Variable For All Users Function (contains code for adding environment variable for all users which require root privileges for writing into files in the "/etc/..." directory) -----------------------------------
def environment_variables_add_environment_variable_for_all_users():
    with open("/etc/environment") as reader:
        etc_environment_lines = reader.read().strip().split("\n")                             # ".strip()" is used in order to prevent adding "\n" per function run (this new line is appended when data is written into file).
    with open("/etc/environment", "w") as writer:
        for line_write in etc_environment_lines:
            if line_write.startswith(variable_to_delete + "=") == False:                      # Write exiting lines into the file.
                writer.write(line_write + "\n")

environment_variables_add_environment_variable_for_all_users()
