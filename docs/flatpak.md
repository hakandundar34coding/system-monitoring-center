# Installing from Flatpak

### Installation:
For installing from GUI:
- Install the application by using Flatpak Application Center or Gnome Software Center.
For installing from command line:
- Option-1) Installing for system-wide: `flatpak install flathub io.github.hakandundar34coding.system-monitoring-center`
    (This method can be used for preventing source code modifications.)
- Option-2) Installing for current user account: `flatpak install --user flathub io.github.hakandundar34coding.system-monitoring-center`

### Updating:
- Run this command to update the application: `flatpak update io.github.hakandundar34coding.system-monitoring-center`

### Notes For Flatpak Support:
- Flatpak version of the application uses some permissions (like not sandboxed) to access performance/system information of the host OS.

