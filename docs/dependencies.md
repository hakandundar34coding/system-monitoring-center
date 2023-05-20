# Dependencies

There is no need to install these dependencies for installing the application from Flatpak.
For other installation types:

- For System Monitoring Center v2.x.x:
    - `dmidecode, gir1.2-adw-1, gir1.2-glib-2.0, gir1.2-gtk-4.0, gir1.2-pango-1.0, hwdata, iproute2, python3 (>=3.6), python3-cairo, python3-gi, python3-gi-cairo, util-linux (>=2.31)`

- For System Monitoring Center v1.x.x:
    - `dmidecode, hwdata, iproute2, python3 (>=3.6), python3-cairo, python3-gi, python3-gi-cairo, util-linux (>=2.31)`

- Following dependencies may be required on some systems:
    - `libcairo2-dev` (for systems with .deb packages)
    - `polkit` (for Arch Linux)
- Optional dependencies:
    - `x11-xserver-utils` or `xorg-xrandr` (for more accurate screen resolution and refresh rate detection of System Monitoring Center v1.x.x)
    - `vcgencmd` (for physical RAM size, GPU frequency and video memory information on Raspberry Pi devices)

