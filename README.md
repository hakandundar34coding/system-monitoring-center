# System Monitoring Center

<p align="center">
    <img src="https://github.com/hakandundar34coding/system-monitoring-center/blob/master/icons/hicolor/scalable/apps/system-monitoring-center.svg" width="100">
</p>


<p align="center">
    <strong>
        Multi-featured system monitor
    </strong>
</p>


<p align="center">
    <a href="https://github.com/hakandundar34coding/system-monitoring-center/tags">
        <img alt="Platform (GNU/Linux)" src="https://img.shields.io/badge/platform-GNU/Linux-blue.svg"/>
    </a>
    <a href="https://github.com/hakandundar34coding/system-monitoring-center/tags">
        <img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/v/tag/hakandundar34coding/system-monitoring-center?sort=semver">
    </a>
    <a href="https://github.com/hakandundar34coding/system-monitoring-center/tags">
        <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/hakandundar34coding/system-monitoring-center/total">
    </a>
    <a href="https://pypi.org/project/system-monitoring-center/">
        <img src="https://static.pepy.tech/personalized-badge/system-monitoring-center?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads"/>
    </a>
    <a href="https://flathub.org/apps/details/io.github.hakandundar34coding.system-monitoring-center">
        <img alt="Flathub" src="https://img.shields.io/flathub/downloads/io.github.hakandundar34coding.system-monitoring-center">
    </a>
    <a href="https://github.com/hakandundar34coding/system-monitoring-center/blob/master/Changes.md">
        <img src="https://img.shields.io/badge/View-Changelog-b37840">
    </a>
</p>


<p align="center">
    <a href="https://github.com/hakandundar34coding/system-monitoring-center/tags">
        <img src="https://img.shields.io/badge/Code-Python3-52a381">
    </a>
    <a href="https://github.com/hakandundar34coding/system-monitoring-center/tags">
        <img src="https://img.shields.io/badge/GUI-GTK4-52a381">
    </a>
</p>


<p align="center">
    <strong>
        Translations:
    </strong>
    Czech | German | English | Français | Hungarian | Persian | Polish | Portuguese (Brazilian) | Portuguese (Portugal) | Russian | Spanish | Turkish | <a href="docs/translations.md">Notes for translators</a>
</p>


<p align="center">
    <a href='https://pypi.org/project/system-monitoring-center'>
        <img width='240' alt='Download from PyPI' src='https://github.com/hakandundar34coding/system-monitoring-center/raw/master/docs/download_image_pypi.svg'/>
    </a>
    <a href='https://flathub.org/apps/details/io.github.hakandundar34coding.system-monitoring-center'>
        <img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.svg'/>
    </a>
    <a href='https://apps.pardus.org.tr/app/system-monitoring-center'>
        <img width='240' alt='Install From Pardus Software Center' src='https://github.com/hakandundar34coding/system-monitoring-center/raw/master/docs/download_image_pardus.svg'/>
    </a>
    <a href='https://github.com/Botspot/pi-apps'>
        <img width='240' alt='Install From Pi-Apps' src='https://github.com/Botspot/pi-apps/blob/master/icons/badge.png?raw=true'/>
    </a>
</p>


<p align="center">
    <a href="https://repology.org/project/system-monitoring-center/versions">
        <img src="https://repology.org/badge/vertical-allrepos/system-monitoring-center.svg" alt="Packaging status">
    </a>
</p>
<p align="center">
    <a href="https://flathub.org/apps/details/io.github.hakandundar34coding.system-monitoring-center">
        <img alt="Flathub" src="https://img.shields.io/flathub/v/io.github.hakandundar34coding.system-monitoring-center">
    </a>
    <a href="https://pypi.org/project/system-monitoring-center/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/system-monitoring-center">
    </a>
    <a href="https://github.com/Botspot/pi-apps">
        <img src="https://img.shields.io/badge/dynamic/json?color=blue&label=Pi-Apps&query=%24..%5B%3F%28%40.Name%3D%3D%22System%20Monitoring%20Center%22%29%5D.Version&url=https%3A%2F%2Fraw.githubusercontent.com%2FBotspot%2Fpi-apps-analytics%2Fmain%2Fpackage_data.json" alt="Pi-Apps Packaging Status">
    </a>
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
- Optimized for low CPU usage and fast start
- Supports ARM architecture
- Free and open source


### Installation:
- There are several options for using System Monitoring Center:
    - Installing from PyPI as a Python package ([Details](docs/pypi.md)).
    - Installing from Flatpak ([Details](docs/flatpak.md)).
    - Installing from several application stores (Pardus Application Center, Pi-Apps Store).
    - Installing from repositories of distributions (currently a few distributions).
    - Running from source code (in ```src/``` folder, run: ```python3 ./Main.py```).
<strong>
    - Note: System Monitoring Center v2.x.x is only available for Flatpak and ArchLinux (AUR).
</strong>


### Dependencies:
- Dependency [list](docs/dependencies.md).


### Screenshots:

![System Monitoring Center](screenshots/summary_tab_dark_system_theme.png)

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
- Non-Flatpak versions of the application has higher performance (start speed, CPU, RAM usage).
- GTK4 (used for SMC v2) uses about 2x RAM when compared to GTK3 (used for SMC v1).

