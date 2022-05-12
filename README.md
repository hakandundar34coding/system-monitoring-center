# System Monitoring Center

GTK3 and Python 3 based, system performance and usage monitoring tool.


<p align="center">
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="Platform (GNU/Linux)" src="https://img.shields.io/badge/platform-GNU/Linux-blue.svg"/></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/hakandundar34coding/system-monitoring-center"></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/system-monitoring-center"></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="Download System Monitoring Center" src="https://img.shields.io/sourceforge/dt/system-monitoring-center.svg" ></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/tags"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/hakandundar34coding/system-monitoring-center/total"></a>
<a href="https://pypi.org/project/system-monitoring-center/"><img src="https://img.shields.io/badge/Visit-PyPI%20Page-b37840"/></a>
<a href="https://github.com/hakandundar34coding/system-monitoring-center/blob/master/Changes.md"><img src="https://img.shields.io/badge/View-Changelog-b37840"></a>
</p>


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


### Dependencies:
- These dependencies are already installed on many systems: `bash, dmidecode, iproute2, python3 (>=3.6), python3-cairo, python3-gi, python3-gi-cairo, udev, util-linux`
- Following dependencies may be required on some systems: for systems with .deb packages: `libcairo2-dev`, for Arch Linux: `polkit`


### Updating:
- Run one of these commands to update the application:
    - If the application is installed for current user account: `pip install --upgrade system-monitoring-center`
    - If the application is installed for system-wide: `sudo pip install --upgrade system-monitoring-center`


<a href="https://repology.org/project/system-monitoring-center/versions">
    <img src="https://repology.org/badge/vertical-allrepos/system-monitoring-center.svg" alt="Packaging status"></a>


### Features:
- Detailed system performance and usage usage monitoring/managing features:
    - Monitoring CPU, RAM, Disk, Network, GPU hardware information/performance/usage
    - Monitoring and managing processes, startup applications and services (systemd)
    - Monitoring users, sensors and general system information
- Supports PolicyKit. No need to run the application with "sudo"
- Hardware selection options (selecting  different CPU cores, disks, network cards, GPUs)
- Plotting performance data of multiple devices at the same time
- Interactive charts for querying performance data on any point
- Option for showing processes as tree or list
- Language support:
    - Brazilian Portuguese, Czech, English, Polish, Turkish
    - More languages will be added if translations are provided by contributors
- Optimized for low CPU usage and fast start
- Shows notification if update is available on PyPI (disabled by default)
- Supports ARM architecture
- Adapts to system theme
- Free and open sourced


### Screenshots:
![System Monitoring Center](screenshots/cpu_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/cpu_tab_white_system_theme.png)

![System Monitoring Center](screenshots/cpu_tab_per_core_dark_system_theme.png)

![System Monitoring Center](screenshots/network_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/gpu_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/sensors_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/processes_list_view_dark_system_theme.png)

![System Monitoring Center](screenshots/startup_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/services_tab_dark_system_theme.png)

![System Monitoring Center](screenshots/system_tab_dark_system_theme.png)


### Notes:
- GPU usage information availability depends on vendor/driver.
- GPU load is not tracked if GPU tab is switched off (for lower CPU usage).
- Some virtual machines does not provide CPU min-max frequencies, sensors and RAM hardware information.
