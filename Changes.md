# System Monitoring Center

### v2.0.2 (21.11.2022)
  * Fix: Resetting all settings when GPU tab is opened
  * Fix: Window size when when default tab is changed
  * Fix: Hiding Services tab if systemd is not used
  * Several code simplifications

### v2.0.1 (20.11.2022)
  * Fix: Application crash after changing remembering last tabs

### v2.0.0 (20.11.2022)
  * New: GTK4 GUI toolkit is used instead of GTK3
  * New: Design changes for main/tab customization/right click menus
  * New: Light/Dark GUI option
  * New: Monitor resolution and refresh rate for multiple monitors
  * Fix: Several GTK3 bugs are removed by switching to GTK4
  * Several code simplifications
  * Several improvements (code, GUI, translations, etc.)

### v1.33.0 (07.11.2022)
  * Improved: CPU usage of user processes for Flatpak
  * Improved: Process shared memory support for Flatpak
  * Improved: Physical RAM of some ARM devices for Flatpak
  * Improvements for lower CPU usage (Processes tab)
  * Improvements for lower CPU usage (Process details)
  * Fix: Disk information for Flatpak
  * Minor improvements (GUI, translations, etc.)

### v1.32.0 (04.11.2022)
  * Simplified main menu
  * Replaced several GUI images with built-in GTK images
  * Fix: Getting disk/process information for old distributions
  * Minor improvements (GUI, translations, etc.)

### v1.31.0 (03.11.2022)
  * Improved: Process details window support for Flatpak
  * Improved: Process right click menu for Flatpak
  * Changed: Process details windows count limit: 8 (Flatpak: 3)
  * Updated: German translations
  * Removed: Parent/child process list (Process details window)
  * Fix: GUI images for Flatpak
  * Minor improvements (GUI, translations, etc.)

### v1.30.1 (29.10.2022)
  * Fix: Application shortcut generation

### v1.30.0 (29.10.2022)
  * Improved: Processes tab information support for Flatpak
  * Improved: Disk usage data support for Flatpak
  * Improved: User information support for Flatpak
  * Improved: SSID name support for Flatpak
  * Improved: Display manager info. support for Flatpak
  * Fix: Closing user account details window if deleted
  * Fix: Detection of dark system theme for Flatpak
  * Minor improvements (start speed, code etc.)

### v1.29.0
  * New: Support for Flatpak packaging
  * Changed: Single project branch for all packaging types
  * Minor code improvements

### v1.28.0
  * New: Option for language selection
  * New: Chinese (Simplified) translations
  * Minor improvements (GUI, translations, etc.)

### v1.27.0
  * New: German translations
  * Fix: File read errors for C locale
  * Minor improvements (GUI, translations, etc.)

### v1.26.1
  * Minor improvements (code, translations, etc.)

### v1.26.0
  * New: Support for multiple process details windows
  * New: Persian translations
  * Fix: GPU usage for AMD GPUs
  * Minor improvements (GUI, translations, etc.)

### v1.25.0
  * New: CPU, RAM, Disk graphs on process details window
  * Fix: Repeating functions multiple times (User,Service details)
  * Minor improvements (GUI, translations, etc.)

### v1.24.0
  * New: European Portuguese translations
  * Changed process details window behavior when process is ended
  * Fix: Getting services on older distributions (Services tab)
  * Minor improvements (GUI, translations, etc.)

### v1.23.0
  * Improved start speed of Services tab on several systems
  * Improved information show speed on some systems (System tab)
  * Improvements for preventing GUI blocking (GPU tab)
  * Improvements for thread safety (MainGUI)
  * Minor improvements (GUI, translations, etc.)

### v1.22.0
  * Changed main menu button location and appearance
  * Hide Services tab if systemd is not used
  * Fix: Updating search results after list changes on some tabs
  * Fix: Getting IP addresses on some distributions
  * Fix: Using dark theme on some newer desktop environments
  * Minor improvements (GUI, translations, etc.)

### v1.21.0
  * Removed: Unused translations
  * Fix: Incorrect column ordering (Processes,Users,Services tabs)
  * Fix: Screen resolution for modified screen scale factors
  * Minor improvements (GUI, etc.)

### v1.20.0
  * New: Keyboard shortcuts for Processes tab actions
  * New: Hungarian translations
  * Removed: Startup tab
  * Updated: Polish translations
  * Fix: RAM hardware details window is not shown
  * Fix: Copying some translations during installation
  * Minor improvements (GUI, translations, etc.)

### v1.19.0
  * New: Summary tab for showing performance summary
  * Updated translations for Czech language
  * Fix: GPU PCI address upper-lower case problem
  * Minor improvements

### v1.18.0
  * New: Option for hiding loop, ramdisk, zram disks (Disk tab)
  * New: Translations for Russian language
  * Fix: Disk read/write speed drawing/graph errors (Disk tab)
  * Minor improvements (GUI, translations, etc.)

### v1.17.0
  * New: Frequency and memory information of Broadcom (ARM) GPUs
  * Updated translations for Brazilian Portuguese
  * Fix: L1d-L1i cache memory order of CPU cores (CPU tab)
  * Minor improvements (GUI, translations, etc.)

### v1.16.0
  * New: Updated GUI design (CPU, RAM, Disk, Network, GPU tabs)
  * New: Highlighting selected device graph between other devices
  * New: Option for showing disk/network speed as powers of 1000
  * Simplified several customization menus
  * Fix: Graph scaling (Disk and Network tabs)
  * Minor improvements (GUI, performance, etc.)

### v1.15.0
  * New: Unified tab and device selector (Performance tab)
  * Replaced disk read/write time with read/write data (Disk tab)
  * Peak RAM usage is reduced (about 10 MiB)
  * Updated translations for Polish and Turkish languages
  * Fix: System disk information on Disk Details window
  * Minor improvements for start speed of the application
  * Minor improvements (GUI, performance, etc.)

### v1.14.0
  * Removed: Images on several menus for a simpler GUI
  * Removed: Filtering buttons on several tabs for a simpler GUI
  * Fix: Right click menu position for some multp. monitor setups
  * Minor improvements for reducing RAM usage of the application
  * Minor improvements for reducing start speed of the application
  * Improvements for showing GUI images after installation
  * Several improvements (GUI, translations, etc.)

### v1.13.0
  * New: Plot memory/disk/network usage/speed of all devices
  * New: Option for process command line column (Processes tab)
  * New: Check for updates (from PyPI) option
  * Removed: Floating Summary window
  * Fix: Temperature and GPU usage for AMD GPUs
  * Fix: Several chart plotting problems
  * Minor improvements (GUI, performance, etc.)

### v1.12.1
  * Fix: Prevent app.crash if system locale problem is found
  * Fix: GPU load, temperature, power for some GPUs (GPU tab)
  * Fix: GPU frequency text for AMD GPUs (GPU tab)
  * Fix: GPU usage information for some ARM devices
  * Fix: Power sensor units (Sensors tab)

### v1.12.0
  * New: GPU load, memory, frequency, power, etc. (GPU tab)
  * New: Support for power sensors
  * Removed: mesa-utils (glx-utils) dependency
  * Improved: Show RAM capacity if physical RAM is not detected
  * Improved: Show Arch Linux image version for OS version
  * Fix: GUI rendering problems after GPU tab is switched on
  * Fix: Detecting disk mount points for some ARM devices
  * Fix: Windowing system for Arch Linux if env.var. is not set
  * Minor improvements

### v1.11.0
  * New: Interactive charts (CPU, RAM, Disk, Network, GPU tabs)
  * Fix: Application start if desktop file is modified
  * Fix: Dashed line text for some fonts

### v1.10.2
  * v1.10.0, v1.10.1 are not published (fixes for packaging, etc.)
  * Improved: Getting ARM CPU model names
  * Improved: Device vendor-model detection
  * Fix: Detect window manager of GNOME DE
  * Fix: Disk model name on QEMU virtual machines
  * Fix: Error on systems with no systemd (Services tab)
  * Fix: Scr. refresh rate on some systems with Wayland win.s.

### v1.9.1
  * Fix: System integration (shortcut, images) for some cases

### v1.9.0
  * Update: project structure for Python packaging type
  * Improved: CPU model names for ARM CPUs
  * Add hardware database files
  * Minor improvements

### v1.8.0
  * New: Plot CPU usage history per-core
  * New: Gradient colors below line (CPU, RAM, GPU charts)
  * Updated pt_BR translation
  * Code updates for OOP (Several modules)
  * Improved: Detection of computer model on ARM devices
  * Replaced pci.ids dependency with hwdata
  * Fix: getting services on some ARM devices
  * Fix: USB network card vendor-model information
  * Fix: Disk mount point for disks with multiple mount points
  * Fix: GPU vendor-model names for ARM systems
  * Fix: network card names for virtual network interfaces
  * Fix: Showing some NICs (usb0) without device-vendor IDs
  * Minor improvements and other bug fixes

### v1.7.0
  * Code updates for OOP (menus, Performance, Settings)
  * Improved performance for tab switches
  * Improved FPS counter accuracy
  * Fix: Resetting some fields for switched off tabs
  * Fix: Showing error messages of startup item commands
  * Fix: Closing color chooser dialogs on some systems
  * Fix: Speed data conversions for bits/sec and orders
  * Minor improvements

### v1.6.0
  * New: Czech language translation
  * New: Polish language translation (initial)
  * Fix: application instance controls
  * Removed: python3-opengl dependency
  * Minor improvements

### v1.5.0
  * New: Brazilian Portuguese (pt_BR) translation
  * Removed deleted translation lines
  * Minor improvements

### v1.4.0
  * Rewrite Startup tab code (improved reliability)
  * Add: dependency (python3-gi-cairo)
  * Minor improvements for process names > 15 characters
  * Several minor improvements

### v1.3.0
  * New: remember window size option (Settings)
  * Simplifications for the GUI (several tabs)
  * Improved: saving/reading configuration file
  * Removed code for reading/writing read-only settings
  * Fix: resetting CPU usage graph type (avg./per core)
  * Fix: Enabling/Disabling service (Services tab)
  * Minor impovements and bug fixes

### v1.2.2
  * Swap Details window is reloaded automatically
  * Fix: Showing menu/details window for some processes
  * Fix: wrong default_main_tab values
  * Fix: disk vendor-model information (Disk Details)
  * Update some if controls of main_tab and sub_tab for optimizing
  * Minor changes for OS name and version information
  * Minor improvements (GUI, translations, etc.)
  * Optimize screenshots using png optimization tools

### v1.2.1
  * Fix: disk vendor-model information (Disk Details)
  * Fix: disk read/write speed (Process Details window)
  * Minor improvements (Users tab)
  * Minor improvements (GUI, translation, etc)
  * Minor improvements

### v1.2.0
  * Removed Storage tab and moved Disk details to Disk tab
  * Removed Environment Variables tab and GUI design changes
  * Fix: disk vendor-model information on VMs (Disk tab)
  * Fix: selecting hardware automatically (CPU,Disk,Network tabs
  * Minor improvements for GUI and System tab
  * Translation improvements
  * Minor improvements

### v1.1.0
  * Support for ARM devices
  * Minor improvements for application start speed
  * Bug fix and minor improvements (CPU tab)
  * Various improvements (bug fixes, performance, GUI, etc.

### v1.0.0
  * Various improvements (bug fixes, performance, GUI, etc.

### v0.3.2-beta1
  * Improvements for ARM device support
  * Fix: highligthing processes of clicked windows
  * Updated used RAM calculation method
  * Minor improvements for application start speed
  * Performance improvements (CPU tab)
  * Minor improvements

### v0.3.1-beta1
  * Fix: GPU model name matching problem (GPU tab)
  * Improvements for Flatpak packaging
  * Improvement: restarting the application with root privileges
  * Minor improvements

### v0.3.0-beta2
  * New: Support for voltage,current and more temp./fan sensors
  * Minor performance improvements for several tabs
  * Fix: sensor name (Sensors tab)
  * Updated package dependencies
  * Minor improvements

### v0.2.0-beta1
  * New: limited support for ARM CPUs (CPU tab)
  * New: limited support for ARM CPUs (System tab)
  * Improvements for detection of startup applications behavior
  * Fix: FPS graph problems for screens with high refresh rate (>100 Hz)
  * Fix: Disk vendor name for NVMe SSDs
  * Minor improvements for reducing CPU load (CPU tab)
  * Improvements for getting Gnome DE version (System tab)
  * Minor improvements

### v0.1.21-beta19
  * Improvements for getting Gnome DE version
  * Improvements for packaging scripts
  * Improvements for opening default terminal application
  * Fixed a bug for NVMe SSDs (Disk tab)
  * Minor improvements

### v0.1.21-beta18
  * Security improvements for command running operations (GPU tab)
  * Fixed a bug for GPU vendor-device information (GPU tab)
  * Application category change: Settings category is removed
  * Added new capability: Resetting all settings with new release
  * Improvements for detecting system disk (Disk tab)
  * Improvements for deleting environment variable
  * Performance improvements for getting RPM package count
  * Fixed a bug for running terminal application (Main menu)
  * Minor GUI improvements

### v0.1.21-beta17
  * New: End User Session action is added (Users tab)
  * Visual improvements for Sensors and RAM tabs
  * Improvements for debian packaging and GUI
  * Several improvements (RPM packaging, dependencies, etc.)
  * Several improvements (Sytsem tab DE support and other)
  * Various improvements (GUI, Readme file, etc.)
  * Minor improvements

### v0.1.21-beta16
  * Fixed a bug for RAM hardware information window

### v0.1.21-beta15
  * Minor improvements and bug fixes

### v0.1.21-beta14
  * New: RAM hardware information can be viewed (RAM tab)
  * New: Swap memory details can be viewed (RAM tab)
  * Improvements for Floating Summary window
  * Minor GUI improvements
  * Minor improvements

### v0.1.21-beta13
  * Fix a bug for RAM tab


### v0.1.21-beta12
  * Improvements for Startup tab right click menu
  * Improvements for GUI and translations
  * Various minor improvements
  * Bug fixes for Environment Variables tab
  * Several improvements

### v0.1.21-beta11
  * Several improvements (functionality, bug fixes, etc)

### v0.1.21-beta10
  * Several improvements (functionality, GUI design, bug fixes, etc)

### v0.1.21-beta9
  * Several improvements (performance, security, bug fixes, etc)

### v0.1.21-beta8
  * Improvements for error handling and dialogs (Startup tab)
  * Removed unused dialogs
  * Minor code comment changes
  * Added information of number of Python packages (System tab)
  * fix: dynamic updating of CPU core count and max frequency
  * Reduced data update latency on tab switch (Process Details window)
  * fix: search bug for services (Services tab)
  * Various minor improvements (settings, GUI, etc.)
  * Several changes for easier maintenance
  * Fixed Processes tab right click menu bugs
  * Improvements for performance summary on the headerbar

### v0.1.21-beta7
  * Minor updates for function repeating mechanism
  * Automatic data units are set for Floating Summary window
  * Minor internal and GUI improvements
  * Processes tab customizations menu simplifications
  * Reduced CPU load while application start and tab switch

### v0.1.21-beta6
  * Update README.md
  * Minor GUI improvements
  * Removed Run Application window which needs more detailed work
  * Updated translation files

### v0.1.21-beta5
  * Remove search customization features for simplicity

### v0.1.21-beta4
  * Added support for viewing Arch Linux and pacman packages information
  * Minor design changes on GUI icons
  * Update README.md

### v0.1.21-beta3
  * About %50 performance improvement for services data loading
  * Various bug fixes and minor improvements

### v0.1.21-beta2
  * Fixed bugs for double/right clicking on empty areas of the lists on several tabs
  * Improvements for Debian packaging

### v0.1.21-beta1
  * Improved tab switch performance

### v0.1.20-beta
  * Removed unused code

### v0.1.19-beta
  * Added support for showing Network and GPU device vendor and model information on RPM-based systems
  * Added support for showing number of installed RPM packages on RPM-based systems (System tab)
  * Fixed a bug for showing number of installed Flatpak packages
  * Minor performance improvements on Disk and System tab
  * Minor changes on application icon

### v0.1.18-beta
  * Fixed bugs for default tabs on application start
  * Fixed a bug for resetting selected disk (Disk tab)

### v0.1.17-beta
  * Application start speed is improved
  * Tab switch performance is improved
  * RAM usage of the application is decreased in most situations
  * Improved response times of the application window after window focus changes
  * CPU usage is decreased for several tabs
  * Minor viusal changes on application icon
  * Selected hardware can be reset on relevant tab (CPU, Disk, etc.)
  * Fixed a bug which causes running multiple instances of same threads after repetitive tab switches

### v0.1.16-beta
  * Application start speed is improved
  * Improved response times of the application window after window focus changes
  * Minor improvements for reducing CPU usage on several tabs
  * Added information of number of installed Flatpak packages (System tab)
  * Default value of average CPU usage precision is changed to "0" to increase readability
  * Minor GUI improvements

### v0.1.15-beta
  * Application start speed is improved
  * Tab switch performance is improved
  * Fixed a bug for showing process cmdline on Process Details window
  * Minor GUI improvements

### v0.1.14-beta
  * Fixed a bug which causes displaying wrong process icons (Processes tab)
  * Minor performance improvements on System tab
  * Minor translation updates

### v0.1.13-beta
  * Start speed of the application is increased
  * RAM usage of the application is decreased in most situations
  * Icon images are recolored as "bebebeff" color instead of black (this does not affect icon appearances on the GUI)
  * Fixed a bug for trying to open Service Details window without waiting the services to be loaded and listed

### v0.1.12-beta
  * Fixed a bug for showing right click menu on Services tab
  * Minor GUI improvements (CPU and GPU tabs)

### v0.1.11-beta
  * Window manager information is added to the System tab
  * Added support for listing startup applications on systems with LXQt and LXDE desktop environments
  * Added support for showing desktop environment versions of MATE and LXQt desktop environments (System tab)
  * Changed right click menu popup code for quicker menu popups
  * Removed open right click menu buttons on several tabs for a simpler GUI
  * Fixed a bug for some process names longer than 15 characters (Processes tab)
  * Fixed a bug for "Started" information on User Details window
  * Fixed bugs for untranslated texts on several tabs/windows
  * Various bug fixes
  * Minor GUI improvements

### v0.1.10-beta
  * OS kernel version information is available on the GUI
  * Fixed a bug for showing CPU architecture on some systems
  * For getting CPU architecture, removed dependency of lscpu command (CPU tab)
  * Minor improvements for CPU usage on CPU tab and System tab
  * Various bug fixes
  * Minor GUI improvements (added tooltips for several objects on System tab, etc.)

### v0.1.9-beta
  * User details can be viewed on a separate window (Users tab)
  * Child processes of a process can be viewed on Process Details window (Processes tab)
  * Fixed a bug for viewing storage details on systems if there is no disks with label since system installation.
  * Various bug fixes
  * Minor GUI improvements

### v0.1.8-beta
  * Improvements for listing environment/shell variables correctly
  * Add/Edit/Delete/Copy right click menu functions are added (Environment Variables tab)
  * Now double clicking on process/storage/service rows opens details window on relevant tab
  * Fixed bugs which cause error when application is run with root privileges (Startup tab)
  * Fixed a bug for showing signal strength (link value) of the WI-FI network (Network tab)
  * Various bug fixes
  * Minor GUI improvements

### v0.1.7-beta
  * Fixed bugs which cause incorrect startup item "Enabled/Disabled" behavior (Startup tab)
  * Minor GUI improvements (GUI object tooltip changes/updates)

### v0.1.6-beta
  * Added support for listing startup items on systems with GNOME-Classic, Ubuntu-GNOME desktop environments (Startup tab).
  * Added "Run Now" and "Reset To System Values" items on the right click menu on Startup tab.
  * Fixed bugs which cause incorrect startup item "Enabled/Disabled" information (Startup tab)
  * Various bug fixes
  * Minor GUI improvements

### v0.1.5-beta
  * Added support for listing startup items on systems with Cinnamon, Mate, Kde desktop environments (Startup tab).
  * Improvements for listing processes with names longer than 15 characters (Processes tab)
  * Various bug fixes
  * Minor performance improvements on Startup tab
  * Minor GUI improvements
  * Error handling improvements

### v0.1.4-beta
  * Added support for detection of Wayland windowing system (System tab)
  * Added support for detection of Cinnamon, Mate, Kde Plasma desktop environments (System tab)
  * Fixed a bug which causes error when an application window is tried to be defined on systems run Wayland (Processes tab)
  * Fixed a bug which causes error while detecting current monitor on systems run Wayland (System tab)
  * Fixed a bug which causes error while getting information of "Based on" on Debian OS (System tab)
  * Various bug fixes
  * Minor performance improvements on System tab
  * Error handling improvements
  * Removed unused code

### v0.1.3-beta
  * Performance improvements for more smooth tab switches
  * Minor performance improvements for application start speed
  * Implementations of functions for General Settings window
  * Fixed bugs which cause incorrect chart scaling on Disk and Network tabs.
  * Various bug fixes
  * Error handling improvements
  * Removed unused code

### v0.1.2-beta
  * Implementations of functions for General Settings window
  * Removed unnecessary commandline functions which are used for getting hardware information.
  * 0 Byte values are shown as 0 B instead of 0.00 B.
  * Menus longer than size of the main window are redesigned because they were trimmed on some systems.
  * Various bug fixes
  * Error handling improvements
  * Minor translation updates
  * Some code changes for easier code readability
  * Removed unused code

### v0.1.1-beta
  * Changed default settings for more user friendly view.
  * Changed some GTK GUI object properties which were deprecated.
  * Various bug fixes
  * Minor translation updates

### v0.1.0-beta
  * Initial commit

