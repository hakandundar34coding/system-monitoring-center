# Uninstalling Python (PyPI) package of the application

### Uninstallation:
For uninstalling Python (PyPI) package:
- Uninstalling for current user account: `pip uninstall system-monitoring-center`
- Uninstalling for system-wide: `sudo pip uninstall system-monitoring-center`
- Removing files for system integration:
  - Delete `io.github.hakandundar34coding.system-monitoring-center.desktop` file in `/home/[USERNAME]/.local/share/applications/`
  - Delete `system-monitoring-center.svg` in `/home/[USERNAME]/.local/share/icons/hicolor/scalable/apps/`
  - Delete `.svg` files that start with `system-monitoring-center-` in `/home/[USERNAME]/.local/share/icons/hicolor/scalable/actions/`

Commands for deleting files:

```
rm /home/$USER/.local/share/applications/io.github.hakandundar34coding.system-monitoring-center.desktop
rm /home/$USER/.local/share/applications/com.github.hakand34.system-monitoring-center.desktop
rm /home/$USER/.local/share/icons/hicolor/scalable/apps/system-monitoring-center.svg
rm /home/$USER/.local/share/icons/hicolor/scalable/actions/system-monitoring-center-*
```
