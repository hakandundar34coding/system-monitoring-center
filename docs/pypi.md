# Installing from PyPI

### Installation:
For installing from PyPI as a Python package:
- Option-1) Installing for current user account: `pip install system-monitoring-center`
- Option-2) Installing for system-wide: `sudo pip install system-monitoring-center`
    (This method can be used for preventing source code modifications.)
- First run:
    - Run the application by using `system-monitoring-center` command.
    - The application will prepare shortcut and GUI images automatically.
    - If command is not found, restart the system and run the command again.
    - If images are not shown on the GUI, run `touch ~/.local/share/*` or restart the system.

### Updating:
- Run one of these commands to update the application:
    - If the application is installed for current user account: `pip install --upgrade system-monitoring-center`
    - If the application is installed for system-wide: `sudo pip install --upgrade system-monitoring-center`

