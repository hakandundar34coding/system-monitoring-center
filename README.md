# System Monitoring Center

Multi-featured system monitor.


<p align="center">
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="Platform (GNU/Linux)" src="https://img.shields.io/badge/platform-GNU/Linux-blue.svg"/></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/hakandundar34coding/system-monitoring-center"></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/hakandundar34coding/system-monitoring-center/total"></a>
<a href="https://pypi.org/project/system-monitoring-center/"><img src="https://static.pepy.tech/personalized-badge/system-monitoring-center?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads"/></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/blob/master/Changes.md"><img src="https://img.shields.io/badge/View-Changelog-b37840"></a>
</p>


### Features:
- Detailed system performance and usage usage monitoring/managing features:
    - Monitoring CPU, RAM, Disk, Network, GPU hardware/usage information
    - Monitoring and managing processes and services (systemd)
    - Monitoring users, sensors and general system information
- Supports PolicyKit. No need to run the application with "sudo"
- Hardware selection options (selecting CPU cores, disks, network cards, GPUs)
- Plotting performance data of multiple devices at the same time
- Interactive charts for querying performance data on any point
- Option for showing processes as tree or list
- Language support:
    - Brazilian Portuguese, Czech, English, European Portuguese, German, Hungarian, Persian, Polish, Russian, Turkish
- Optimized for low CPU usage and fast start
- Shows notification if update is available on PyPI (disabled by default)
- Supports ARM architecture
- Adapts to system theme
- Free and open source


### Installation:
- System Monitoring Center is installable from PyPI as a Python package.
- Option-1) Installing for current user account: `pip install system-monitoring-center`
- Option-2) Installing for system-wide: `sudo pip install system-monitoring-center`
    (This method can be used for preventing source code modifications.)
- First run:
    - Run the application by using `system-monitoring-center` command.
    - The application will prepare shortcut and GUI images automatically.
    - If command is not found, restart the system and run the command again.
    - If images are not shown on the GUI, run `touch ~/.local/share/*` or restart the system.


<a href="https://repology.org/project/system-monitoring-center/versions">
    <img src="https://repology.org/badge/vertical-allrepos/system-monitoring-center.svg" alt="Packaging status"></a>


### Dependencies:
- These dependencies are already installed on many systems: 
    - `bash, dmidecode, iproute2, python3 (>=3.6), python3-cairo, python3-gi, python3-gi-cairo, udev, util-linux`
- Following dependencies may be required on some systems:
    - `libcairo2-dev` (for systems with .deb packages)
    - `polkit` (for Arch Linux)
- Optional dependencies:
    - `x11-xserver-utils` or `xorg-xrandr` (for more accurate screen resolution and refresh rate detection)
    - `vcgencmd` (for physical RAM size, GPU frequency and video memory information on Raspberry Pi devices)


### Updating:
- Run one of these commands to update the application:
    - If the application is installed for current user account: `pip install --upgrade system-monitoring-center`
    - If the application is installed for system-wide: `sudo pip install --upgrade system-monitoring-center`


### Screenshots:
![System Monitoring Center](screenshots/cpu_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/cpu_tab_white_system_theme.png)

![System Monitoring Center](screenshots/cpu_tab_per_core_dark_system_theme.png)

![System Monitoring Center](screenshots/network_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/gpu_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/sensors_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/processes_list_view_dark_system_theme.png)

![System Monitoring Center](screenshots/services_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/system_tab_dark_system_theme.png)


### Notes:
- GPU usage information availability depends on vendor/driver.
- GPU load is not tracked if GPU tab is switched off (for lower CPU usage).
- Virtual machines may not provide CPU min-max frequencies, sensors and RAM hardware information.
