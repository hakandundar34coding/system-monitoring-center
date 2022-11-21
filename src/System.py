#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GLib, Pango

import subprocess
import os
import platform
import threading

from locale import gettext as _tr

from Config import Config
from MainWindow import MainWindow


class System:

    def __init__(self):

        # System tab GUI
        self.system_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def system_tab_gui(self):
        """
        Generate System tab GUI.
        """

        # System tab grid
        self.system_tab_grid = Gtk.Grid()
        self.system_tab_grid.set_row_spacing(10)
        self.system_tab_grid.set_margin_top(2)
        self.system_tab_grid.set_margin_bottom(2)
        self.system_tab_grid.set_margin_start(2)
        self.system_tab_grid.set_margin_end(2)

        # Bold and 2x label atributes
        self.attribute_list_bold_2x = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold_2x.insert(attribute)
        attribute = Pango.attr_scale_new(2.0)
        self.attribute_list_bold_2x.insert(attribute)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Tab name, device name labels and menu button
        self.system_gui_label_grid()

        # Performance information labels
        self.system_gui_performance_info_grid()

        # Connect signals
        self.system_gui_signals()


    def system_gui_label_grid(self):
        """
        Generate tab name, os name-version, computer vendor-model labels and refresh button.
        """

        # Tab name label grid
        tab_name_label_grid = Gtk.Grid()
        self.system_tab_grid.attach(tab_name_label_grid, 0, 0, 1, 1)

        # Tab name label
        tab_name_label = Gtk.Label()
        tab_name_label.set_halign(Gtk.Align.START)
        tab_name_label.set_margin_end(60)
        tab_name_label.set_attributes(self.attribute_list_bold_2x)
        tab_name_label.set_label(_tr("System"))
        tab_name_label_grid.attach(tab_name_label, 0, 0, 1, 2)

        # OS name-version label
        self.os_name_version_label = Gtk.Label()
        self.os_name_version_label.set_halign(Gtk.Align.START)
        self.os_name_version_label.set_selectable(True)
        self.os_name_version_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.os_name_version_label.set_attributes(self.attribute_list_bold)
        self.os_name_version_label.set_label("--")
        self.os_name_version_label.set_tooltip_text(_tr("Operating System (OS)"))
        tab_name_label_grid.attach(self.os_name_version_label, 1, 0, 1, 1)

        # Computer vendor-model label
        self.computer_vendor_model_label = Gtk.Label()
        self.computer_vendor_model_label.set_halign(Gtk.Align.START)
        self.computer_vendor_model_label.set_selectable(True)
        self.computer_vendor_model_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.computer_vendor_model_label.set_label("--")
        self.computer_vendor_model_label.set_tooltip_text(_tr("Computer"))
        tab_name_label_grid.attach(self.computer_vendor_model_label, 1, 1, 1, 1)

        # Tab refresh menu button
        self.refresh_button = Gtk.Button()
        self.refresh_button.set_tooltip_text(_tr("Refresh the data on this tab"))
        self.refresh_button.set_hexpand(True)
        self.refresh_button.set_halign(Gtk.Align.END)
        self.refresh_button.set_valign(Gtk.Align.CENTER)
        self.refresh_button.set_icon_name("view-refresh-symbolic")
        tab_name_label_grid.attach(self.refresh_button, 2, 0, 1, 2)


    def system_gui_performance_info_grid(self):
        """
        Generate performance information labels.
        """

        # Add viewports for showing borders around some the performance data.
        css = b"grid {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_grid = Gtk.CssProvider()
        style_provider_grid.load_from_data(css)

        # Performance information labels grid
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        performance_info_grid.set_margin_top(5)
        performance_info_grid.get_style_context().add_provider(style_provider_grid, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.system_tab_grid.attach(performance_info_grid, 0, 1, 1, 1)

        # Performance information labels inner grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(12)
        grid.set_row_spacing(10)
        grid.set_margin_top(6)
        grid.set_margin_bottom(6)
        grid.set_margin_start(6)
        grid.set_margin_end(6)
        performance_info_grid.attach(grid, 0, 0, 1, 1)

        # Performance information labels
        # Title label (Operating System (OS))
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Operating System (OS)"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 2, 1)

        label = Gtk.Label()
        label.set_label(_tr("Name") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)

        # Information label (Name for OS)
        self.system_os_name_label = Gtk.Label()
        self.system_os_name_label.set_selectable(True)
        self.system_os_name_label.set_attributes(self.attribute_list_bold)
        self.system_os_name_label.set_label("--")
        self.system_os_name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_os_name_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_os_name_label, 1, 1, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Version - Code Name") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)

        # Information label (Version - Code Name)
        self.system_version_codename_label = Gtk.Label()
        self.system_version_codename_label.set_selectable(True)
        self.system_version_codename_label.set_attributes(self.attribute_list_bold)
        self.system_version_codename_label.set_label("--")
        self.system_version_codename_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_version_codename_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_version_codename_label, 1, 2, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("OS Family") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)

        # Information label (OS Family)
        self.system_os_family_label = Gtk.Label()
        self.system_os_family_label.set_selectable(True)
        self.system_os_family_label.set_attributes(self.attribute_list_bold)
        self.system_os_family_label.set_label("--")
        self.system_os_family_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_os_family_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_os_family_label, 1, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Based On") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)

        # Information label (Based On)
        self.system_based_on_label = Gtk.Label()
        self.system_based_on_label.set_selectable(True)
        self.system_based_on_label.set_attributes(self.attribute_list_bold)
        self.system_based_on_label.set_label("--")
        self.system_based_on_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_based_on_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_based_on_label, 1, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Kernel Release") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 5, 1, 1)

        # Information label (Kernel Release)
        self.system_kernel_release_label = Gtk.Label()
        self.system_kernel_release_label.set_selectable(True)
        self.system_kernel_release_label.set_attributes(self.attribute_list_bold)
        self.system_kernel_release_label.set_label("--")
        self.system_kernel_release_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_kernel_release_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_kernel_release_label, 1, 5, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Kernel Version") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 6, 1, 1)

        # Information label (Kernel Version)
        self.system_kernel_version_label = Gtk.Label()
        self.system_kernel_version_label.set_selectable(True)
        self.system_kernel_version_label.set_attributes(self.attribute_list_bold)
        self.system_kernel_version_label.set_label("--")
        self.system_kernel_version_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_kernel_version_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_kernel_version_label, 1, 6, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        separator.set_valign(Gtk.Align.CENTER)
        grid.attach(separator, 0, 7, 4, 1)

        # Title label (Operating System (OS))
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Graphical User Interface (GUI)"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 8, 2, 1)

        label = Gtk.Label()
        label.set_label(_tr("Desktop Environment") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 9, 1, 1)

        # Information label (Desktop Environment)
        self.system_desktop_environment_label = Gtk.Label()
        self.system_desktop_environment_label.set_selectable(True)
        self.system_desktop_environment_label.set_attributes(self.attribute_list_bold)
        self.system_desktop_environment_label.set_label("--")
        self.system_desktop_environment_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_desktop_environment_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_desktop_environment_label, 1, 9, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Windowing System") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 10, 1, 1)

        # Information label (Windowing System)
        self.system_windowing_system_label = Gtk.Label()
        self.system_windowing_system_label.set_selectable(True)
        self.system_windowing_system_label.set_attributes(self.attribute_list_bold)
        self.system_windowing_system_label.set_label("--")
        self.system_windowing_system_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_windowing_system_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_windowing_system_label, 1, 10, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Window Manager") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 11, 1, 1)

        # Information label (Window Manager)
        self.system_window_manager_label = Gtk.Label()
        self.system_window_manager_label.set_selectable(True)
        self.system_window_manager_label.set_attributes(self.attribute_list_bold)
        self.system_window_manager_label.set_label("--")
        self.system_window_manager_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_window_manager_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_window_manager_label, 1, 11, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Display Manager") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 12, 1, 1)

        # Information label (Display Manager)
        self.system_display_manager_label = Gtk.Label()
        self.system_display_manager_label.set_selectable(True)
        self.system_display_manager_label.set_attributes(self.attribute_list_bold)
        self.system_display_manager_label.set_label("--")
        self.system_display_manager_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_display_manager_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_display_manager_label, 1, 12, 1, 1)

        # Title label (Computer)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Computer"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 0, 2, 1)

        label = Gtk.Label()
        label.set_label(_tr("Vendor") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 1, 1, 1)

        # Information label (Vendor)
        self.system_vendor_label = Gtk.Label()
        self.system_vendor_label.set_selectable(True)
        self.system_vendor_label.set_attributes(self.attribute_list_bold)
        self.system_vendor_label.set_label("--")
        self.system_vendor_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_vendor_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_vendor_label, 3, 1, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Model") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 2, 1, 1)

        # Information label (Model)
        self.system_model_label = Gtk.Label()
        self.system_model_label.set_selectable(True)
        self.system_model_label.set_attributes(self.attribute_list_bold)
        self.system_model_label.set_label("--")
        self.system_model_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_model_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_model_label, 3, 2, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Computer Type") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 3, 1, 1)

        # Information label (Computer Type)
        self.system_computer_type_label = Gtk.Label()
        self.system_computer_type_label.set_selectable(True)
        self.system_computer_type_label.set_attributes(self.attribute_list_bold)
        self.system_computer_type_label.set_label("--")
        self.system_computer_type_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_computer_type_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_computer_type_label, 3, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Name") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 4, 1, 1)

        # Information label (Name for computer)
        self.system_computer_name_label = Gtk.Label()
        self.system_computer_name_label.set_selectable(True)
        self.system_computer_name_label.set_attributes(self.attribute_list_bold)
        self.system_computer_name_label.set_label("--")
        self.system_computer_name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_computer_name_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_computer_name_label, 3, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Architecture") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 5, 1, 1)

        # Information label (Architecture)
        self.system_architecture_label = Gtk.Label()
        self.system_architecture_label.set_selectable(True)
        self.system_architecture_label.set_attributes(self.attribute_list_bold)
        self.system_architecture_label.set_label("--")
        self.system_architecture_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_architecture_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_architecture_label, 3, 5, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Number Of Monitors") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 6, 1, 1)

        # Information label (Number Of Monitors)
        self.system_number_of_monitors_label = Gtk.Label()
        self.system_number_of_monitors_label.set_selectable(True)
        self.system_number_of_monitors_label.set_attributes(self.attribute_list_bold)
        self.system_number_of_monitors_label.set_label("--")
        self.system_number_of_monitors_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_number_of_monitors_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_number_of_monitors_label, 3, 6, 1, 1)

        # There is a separator between rows 6 and 7.

        # Title label (Packages)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Packages"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 8, 2, 1)

        label = Gtk.Label()
        label.set_label(_tr("System") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 9, 1, 1)

        grid_system_packages = Gtk.Grid()
        grid_system_packages.set_column_spacing(2)
        grid.attach(grid_system_packages, 3, 9, 1, 1)

        # Information label (System)
        self.system_system_label = Gtk.Label()
        self.system_system_label.set_selectable(True)
        self.system_system_label.set_attributes(self.attribute_list_bold)
        self.system_system_label.set_label("--")
        self.system_system_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_system_label.set_halign(Gtk.Align.START)
        grid_system_packages.attach(self.system_system_label, 0, 0, 1, 1)

        # Information spinner (System)
        self.system_spinner_system = Gtk.Spinner()
        self.system_spinner_system.start()
        grid_system_packages.attach(self.system_spinner_system, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Flatpak") + ":")
        label.set_tooltip_text(_tr("Number of installed Flatpak applications and runtimes"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 10, 1, 1)

        # Information label (Flatpak)
        self.system_flatpak_label = Gtk.Label()
        self.system_flatpak_label.set_selectable(True)
        self.system_flatpak_label.set_attributes(self.attribute_list_bold)
        self.system_flatpak_label.set_label("--")
        self.system_flatpak_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_flatpak_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_flatpak_label, 3, 10, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("GTK Version") + ":")
        label.set_tooltip_text(_tr("Version for the currently running software"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 11, 1, 1)

        # Information label (GTK Version)
        self.system_gtk_version_label = Gtk.Label()
        self.system_gtk_version_label.set_selectable(True)
        self.system_gtk_version_label.set_attributes(self.attribute_list_bold)
        self.system_gtk_version_label.set_label("--")
        self.system_gtk_version_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_gtk_version_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_gtk_version_label, 3, 11, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Python Version") + ":")
        label.set_tooltip_text(_tr("Version for the currently running software"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 2, 12, 1, 1)

        # Information label (Python Version)
        self.system_python_version_label = Gtk.Label()
        self.system_python_version_label.set_selectable(True)
        self.system_python_version_label.set_attributes(self.attribute_list_bold)
        self.system_python_version_label.set_label("--")
        self.system_python_version_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.system_python_version_label.set_halign(Gtk.Align.START)
        grid.attach(self.system_python_version_label, 3, 12, 1, 1)


    def system_gui_signals(self):
        """
        Connect GUI signals.
        """

        self.refresh_button.connect("clicked", self.on_refresh_button_clicked)


    def on_refresh_button_clicked(self, widget):
        """
        Refresh data on the tab.
        """

        # Start spinner animation and show it before running the function for getting information.
        self.system_spinner_system.start()
        self.system_spinner_system.show()
        GLib.idle_add(self.system_initial_func)


    # ----------------------- System - Initial Function -----------------------
    def system_initial_func(self):

        # Get information.
        os_name, os_version, os_based_on = self.system_os_name_version_codename_based_on_func()
        os_family = self.system_os_family_func()
        kernel_release, kernel_version = self.system_kernel_release_kernel_version_func()
        cpu_architecture = self.system_cpu_architecture_func()
        computer_vendor, computer_model, computer_chassis_type = self.system_computer_vendor_model_chassis_type_func()
        host_name = self.system_host_name_func()
        number_of_monitors = self.system_number_of_monitors_func()
        number_of_installed_flatpak_packages = self.system_installed_flatpak_packages_func()
        current_python_version, current_gtk_version = self.system_current_python_version_gtk_version_func()
        current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager = self.system_desktop_environment_and_version_windowing_system_window_manager_display_manager_func()
        # Run this function in a separate thread because it may take a long time (2-3 seconds) to get the information on some systems (such as rpm based systems) and it blocks the GUI during this process if a separate thread is not used.
        threading.Thread(target=self.system_installed_apt_rpm_pacman_packages_func, daemon=True).start()


        # Set label texts to show information
        self.os_name_version_label.set_label(f'{os_name} - {os_version}')
        self.computer_vendor_model_label.set_label(f'{computer_vendor} - {computer_model}')
        self.system_os_name_label.set_label(os_name)
        self.system_version_codename_label.set_label(os_version)
        self.system_os_family_label.set_label(os_family)
        self.system_based_on_label.set_label(os_based_on)
        self.system_kernel_release_label.set_label(kernel_release)
        self.system_kernel_version_label.set_label(kernel_version)
        self.system_desktop_environment_label.set_label(f'{current_desktop_environment} ({current_desktop_environment_version})')
        self.system_windowing_system_label.set_label(windowing_system)
        self.system_window_manager_label.set_label(window_manager)
        self.system_display_manager_label.set_label(current_display_manager)
        self.system_vendor_label.set_label(computer_vendor)
        self.system_model_label.set_label(computer_model)
        self.system_computer_type_label.set_label(computer_chassis_type)
        self.system_computer_name_label.set_label(host_name)
        self.system_architecture_label.set_label(cpu_architecture)
        self.system_number_of_monitors_label.set_label(f'{number_of_monitors}')
        #self.system_system_label.set_label(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')
        self.system_flatpak_label.set_label(f'{number_of_installed_flatpak_packages}')
        self.system_gtk_version_label.set_label(current_gtk_version)
        self.system_python_version_label.set_label(f'{current_python_version}')

        self.initial_already_run = 1


    # ----------------------- Set spinner properties and show "number_of_installed_apt_or_rpm_or_pacman_packages" information on the label -----------------------
    def system_set_number_of_installed_apt_or_rpm_or_pacman_packages_label_func(self, number_of_installed_apt_or_rpm_or_pacman_packages):

        # Stop spinner animation and hide it after running the function for getting information.
        self.system_spinner_system.stop()
        self.system_spinner_system.hide()
        self.system_system_label.set_label(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')


    # ----------------------- Get OS name, version, version code name and OS based on information -----------------------
    def system_os_name_version_codename_based_on_func(self):

        # Initial value of "os_name" variable. This value will be used if "os_name" could not be detected.
        os_name = "-"
        os_based_on = "-"
        os_version = "-"

        # Read "/etc/os-release" file for getting OS name, version and based on information.
        if Config.environment_type == "flatpak":
            with open("/var/run/host/etc/os-release") as reader:
                os_release_output_lines = reader.read().strip().split("\n")
        else:
            with open("/etc/os-release") as reader:
                os_release_output_lines = reader.read().strip().split("\n")

        # Get OS name, version and based on information.
        for line in os_release_output_lines:
            if line.startswith("NAME="):
                os_name = line.split("NAME=")[1].strip(' "')
                continue
            if line.startswith("VERSION="):
                os_version = line.split("VERSION=")[1].strip(' "')
                continue
            if line.startswith("ID_LIKE="):
                os_based_on = line.split("ID_LIKE=")[1].strip(' "').title()
                continue

        # Append Debian version to the based on information if OS is based on Debian.
        if os_based_on == "Debian":
            debian_version = "-"
            if Config.environment_type == "flatpak":
                with open("/var/run/host/etc/debian_version") as reader:
                    debian_version = reader.read().strip()
            else:
                with open("/etc/debian_version") as reader:
                    debian_version = reader.read().strip()
            os_based_on = os_based_on + " (" + debian_version + ")"

        # Append Ubuntu version to the based on information if OS is based on Ubuntu.
        if os_based_on == "Ubuntu":
            ubuntu_version = "-"
            for line in os_release_output_lines:
                if line.startswith("UBUNTU_CODENAME="):
                    ubuntu_version = line.split("UBUNTU_CODENAME=")[1].strip(' "')
                    break
            os_based_on = os_based_on + " (" + ubuntu_version + ")"

        # Get Image version and use it as OS version for ArchLinux.
        if os_name.lower() == "arch linux":
            for line in os_release_output_lines:
                if line.startswith("IMAGE_VERSION="):
                    os_version = "Image Version: " + line.split("IMAGE_VERSION=")[1].strip(' "')
                    break

        return os_name, os_version, os_based_on


    # ----------------------- Get OS family -----------------------
    def system_os_family_func(self):

        # Get os family
        os_family = platform.system()
        if os_family == "":
            os_family = "-"

        return os_family


    # ----------------------- Get kernel release (base version of kernel) and kernel version (package version of kernel) -----------------------
    def system_kernel_release_kernel_version_func(self):

        # Get kernel release (base version of kernel)
        kernel_release = platform.release()
        if kernel_release == "":
            kernel_release = "-"

        # Get kernel version (package version of kernel)
        kernel_version = platform.version()
        if kernel_version == "":
            kernel_version = "-"

        return kernel_release, kernel_version


    # ----------------------- Get CPU architecture -----------------------
    def system_cpu_architecture_func(self):

        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"

        return cpu_architecture


    # ----------------------- Get computer vendor, model and chassis type -----------------------
    def system_computer_vendor_model_chassis_type_func(self):

        # Get computer vendor ("/sys/devices/virtual/dmi" is used for UEFI/ACPI systems and not found on ARM systems)
        #, model, chassis information (These informations may not be available on some systems such as ARM CPU used motherboards).
        try:
            with open("/sys/devices/virtual/dmi/id/sys_vendor") as reader:
                computer_vendor = reader.read().strip()
        except FileNotFoundError:
            computer_vendor = "-"

        # Get computer model ("/sys/devices/virtual/dmi" is used for UEFI/ACPI systems and not found on ARM systems)
        try:
            with open("/sys/devices/virtual/dmi/id/product_name") as reader:
                computer_model = reader.read().strip()
        except FileNotFoundError:
            # Try to get computer model for ARM systems.
            try:
                # "/proc/device-tree/model" is a symlink to "/sys/firmware/devicetree/base/model" and using it is safer. For details: https://github.com/torvalds/linux/blob/v5.9/Documentation/ABI/testing/sysfs-firmware-ofw
                with open("/proc/device-tree/model") as reader:
                    computer_model = reader.read().strip()
            except FileNotFoundError:
                computer_model = "-"

        # Get computer chassis ("/sys/devices/virtual/dmi" is used for UEFI/ACPI systems and not found on ARM systems)
        try:
            with open("/sys/devices/virtual/dmi/id/chassis_type") as reader:
                computer_chassis_type_value = reader.read().strip()
        except FileNotFoundError:
            computer_chassis_type_value = 2

        # For more information about computer chassis types, see: "https://www.dmtf.org/standards/SMBIOS"
        # "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
        computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                                       10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                                       17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                                       22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC", 25: "Multi-system chassis", 26: "Compact PCI", 27: "Advanced TCA",
                                       28: "Blade", 29: "Blade Enclosure", 30: "Tablet", 31: "Convertible", 32: "Detachable", 33: "IoT Gateway", 34: "Embedded PC",
                                       35: "Mini PC", 36: "Stick PC"}
        computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]

        return computer_vendor, computer_model, computer_chassis_type


    # ----------------------- Get host name -----------------------
    def system_host_name_func(self):

        with open("/proc/sys/kernel/hostname") as reader:
            host_name = reader.read().strip()

        return host_name


    # ----------------------- Get number of monitors -----------------------
    def system_number_of_monitors_func(self):

        try:
            monitor_list = Gdk.Display().get_default().get_monitors()
            number_of_monitors = len(monitor_list)
        except Exception:
            number_of_monitors = "-"

        return number_of_monitors


    # ----------------------- Get number of installed Flatpak packages (and runtimes) -----------------------
    def system_installed_flatpak_packages_func(self):

        number_of_installed_flatpak_packages = "-"

        try:
            if Config.environment_type == "flatpak":
                flatpak_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "flatpak", "list"], shell=False)).decode().strip().split("\n")
            else:
                flatpak_packages_available = (subprocess.check_output(["flatpak", "list"], shell=False)).decode().strip().split("\n")
            # Differentiate empty line count
            number_of_installed_flatpak_packages = len(flatpak_packages_available) - flatpak_packages_available.count("")
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            number_of_installed_flatpak_packages = "-"

        return number_of_installed_flatpak_packages


    # ----------------------- Get current Python version and GTK version -----------------------
    def system_current_python_version_gtk_version_func(self):

        # Get current Python version (Python which is running this code)
        current_python_version = platform.python_version()

        # Get Gtk version which is used for this application.
        current_gtk_version = f'{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}'

        return current_python_version, current_gtk_version


    # ----------------------- Get number of installed APT, RPM or pacman packages -----------------------
    def system_installed_apt_rpm_pacman_packages_func(self):

        # Initial value of the variables.
        apt_packages_available = "-"
        rpm_packages_available = "-"
        pacman_packages_available = "-"
        number_of_installed_apt_or_rpm_or_pacman_packages = "-"

        # Get number of APT (deb) packages if available.
        try:
            # Check if "python3" is installed in order to determine package type of the system.
            if Config.environment_type == "flatpak":
                apt_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "dpkg", "-s", "python3"], shell=False)).decode().strip()
            else:
                apt_packages_available = (subprocess.check_output(["dpkg", "-s", "python3"], shell=False)).decode().strip()
            if "Package: python3" in apt_packages_available:
                if Config.environment_type == "flatpak":
                    number_of_installed_apt_packages = (subprocess.check_output(["flatpak-spawn", "--host", "dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
                else:
                    number_of_installed_apt_packages = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
                number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_apt_packages} (APT)'
        # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system. It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            apt_packages_available = "-"

        # Get number of RPM packages if available.
        if apt_packages_available == "-":
            try:
                if Config.environment_type == "flatpak":
                    rpm_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "rpm", "-q", "python3"], shell=False)).decode().strip()
                else:
                    rpm_packages_available = (subprocess.check_output(["rpm", "-q", "python3"], shell=False)).decode().strip()
                if rpm_packages_available.startswith("python3-3."):
                    if Config.environment_type == "flatpak":
                        number_of_installed_rpm_packages = (subprocess.check_output(["flatpak-spawn", "--host", "rpm", "-qa"], shell=False)).decode().strip().split("\n")
                    else:
                        number_of_installed_rpm_packages = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
                    # Differentiate empty line count
                    number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")
                    number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_rpm_packages} (RPM)'
            except (FileNotFoundError, subprocess.CalledProcessError) as me:
                rpm_packages_available = "-"

        # Get number of pacman (Arch Linux) packages if available.
        if apt_packages_available == "-" and rpm_packages_available == "-":
            try:
                if Config.environment_type == "flatpak":
                    pacman_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "pacman", "-Q", "python3"], shell=False)).decode().strip()
                else:
                    pacman_packages_available = (subprocess.check_output(["pacman", "-Q", "python3"], shell=False)).decode().strip()
                if pacman_packages_available.startswith("python 3."):
                    if Config.environment_type == "flatpak":
                        number_of_installed_pacman_packages = (subprocess.check_output(["flatpak-spawn", "--host", "pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                    else:
                        number_of_installed_pacman_packages = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                    # Differentiate empty line count
                    number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")
                    number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_pacman_packages} (pacman)'
            except (FileNotFoundError, subprocess.CalledProcessError) as me:
                pacman_packages_available = "-"

        # Show the information on the label by using "GLib.idle_add" in order to avoid problems (bugs, data corruption, etc.) because of threading (GTK is not thread-safe).
        GLib.idle_add(self.system_set_number_of_installed_apt_or_rpm_or_pacman_packages_label_func, number_of_installed_apt_or_rpm_or_pacman_packages)

        return number_of_installed_apt_or_rpm_or_pacman_packages


    # ----------------------- Get current desktop environment, windowing_system, window_manager, current_display_manager -----------------------
    def system_desktop_environment_and_version_windowing_system_window_manager_display_manager_func(self):

        # Get current username
        # Get user name that gets root privileges.
        # Othervise, username is get as "root" when root access is get.
        current_user_name = os.environ.get('SUDO_USER')
        # Get username in the following way if current application has not
        # been run by root privileges.
        if current_user_name is None:
            current_user_name = os.environ.get('USER')

        # Try to get windowing system. This value may be get as "None" if the
        # application is run with root privileges. This value will be get by
        # reading information of processes if it is get as "None".
        windowing_system = os.environ.get('XDG_SESSION_TYPE')
        # "windowing_system" is get as "None" if application is run with root privileges.
        if windowing_system != None:
            windowing_system = windowing_system.capitalize()

        # Try to get current desktop environment. This value may be get as
        # "None" if the application is run with root privileges. This value
        # will be get by reading information of processes if it is get as "None".
        # This command may give Gnome DE based DEs as "[DE_name]:GNOME".
        # For example, "Budgie:GNOME" value is get on Budgie DE.
        current_desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP')
        if current_desktop_environment == None:
            # Define initial value of "desktop environment".
            current_desktop_environment = "-"

        # Define initial value of "windowing_system".
        if windowing_system == None:
            windowing_system = "-"

        # Define initial value of "window_manager".
        window_manager = "-"

        # Define initial value of "current_display_manager".
        current_display_manager = "-"

        # First values are process names of the DEs, second values are names of
        # the DEs. Cinnamon dektop environment accepts both "X-Cinnamon" and
        # "CINNAMON" names in the .desktop files.
        supported_desktop_environments_dict = {"xfce4-session":"XFCE", "gnome-session-b":"GNOME", "cinnamon-session":"X-Cinnamon",
                                               "mate-session":"MATE", "plasmashell":"KDE", "lxqt-session":"LXQt", "lxsession":"LXDE",
                                               "budgie-panel":"Budgie", "dde-desktop":"Deepin"}
        supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "budgie-wm", "openbox", "metacity", 
                                          "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome"]
        # First values are process names of the display managers, second values
        # are names of the display managers.
        supported_display_managers_dict = {"lightdm":"lightdm", "gdm":"gdm", "gdm3":"gdm3", "sddm":"sddm", "xdm":"xdm", "lxdm-binary":"lxdm"}                                                       

        # Try to detect windowing system, window manager, current desktop 
        # environment and current display manager by reading process names and
        # other details.
        if Config.environment_type == "flatpak":
            ps_output_lines = (subprocess.check_output(["flatpak-spawn", "--host", "ps", "--no-headers", "-eo", "comm,user"], shell=False)).decode().strip().split("\n")
        else:
            ps_output_lines = (subprocess.check_output(["ps", "--no-headers", "-eo", "comm,user"], shell=False)).decode().strip().split("\n")

        process_name_list = []
        username_list = []

        for line in ps_output_lines:
            line_split = line.split()
            process_name_list.append(line_split[0])
            username_list.append(line_split[1])

        # Get current desktop environment information
        # "current_desktop_environment == "GNOME"" check is performed in order to
        # detect if current DE is "Budgie DE". Because "budgie-panel" process is child
        # process of "gnome-session-b" process.
        for process_name in process_name_list:
            if current_desktop_environment == "-" or current_desktop_environment == "GNOME":
                if process_name in supported_desktop_environments_dict:
                    process_username = username_list[process_name_list.index(process_name)]
                    if process_username == current_user_name:
                        current_desktop_environment = supported_desktop_environments_dict[process_name]
                        break

        # Get current desktop environment version
        current_desktop_environment_version = self.system_desktop_environment_version_func(current_desktop_environment)

        # Get windowing system information.
        # Windowing system may be get as "tty" (which is for non-graphical system) when
        # "os.environ.get('XDG_SESSION_TYPE')" is used on Arch Linux if environment
        # variables are not set after installing a windowing system.
        for process_name in process_name_list:
            if windowing_system in ["-", "Tty"]:
                process_name = process_name.lower()
                if process_name == "xorg":
                    windowing_system = "X11"
                    break
                if process_name == "xwayland":
                    windowing_system = "Wayland"
                    break

        # Get window manager information
        for process_name in process_name_list:
            if window_manager == "-":
                if process_name.lower() in supported_window_managers_list:
                    process_username = username_list[process_name_list.index(process_name)]
                    if process_username == current_user_name:
                        window_manager = process_name.lower()
                        break

        # Get window manager for GNOME DE (GNOME DE uses mutter window manager and
        # it not detected because it has no separate package or process.).
        if window_manager == "-":
            if current_desktop_environment.upper() == "GNOME":
                if current_desktop_environment_version.split(".")[0] in ["3", "40", "41", "42", "43"]:
                    window_manager = "mutter"

        # Get current display manager information
        for process_name in process_name_list:
            if current_display_manager == "-":
                if process_name in supported_display_managers_dict:
                    process_username = username_list[process_name_list.index(process_name)]
                    # Display manager processes are owned by root user.
                    if process_username == "root":
                        current_display_manager = supported_display_managers_dict[process_name]
                        break

        return current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager


    # ----------------------- Get current desktop environment version -----------------------
    def system_desktop_environment_version_func(self, current_desktop_environment):

        # Set initial value of the "current_desktop_environment_version".
        current_desktop_environment_version = "-"

        if current_desktop_environment == "XFCE":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version_lines = (subprocess.check_output(["flatpak-spawn", "--host", "xfce4-panel", "--version"], shell=False)).decode().strip().split("\n")
                else:
                    current_desktop_environment_version_lines = (subprocess.check_output(["xfce4-panel", "--version"], shell=False)).decode().strip().split("\n")
                for line in current_desktop_environment_version_lines:
                    if "xfce4-panel" in line:
                        current_desktop_environment_version = line.split(" ")[1]
            except FileNotFoundError:
                pass

        if current_desktop_environment == "GNOME" or current_desktop_environment == "zorin:GNOME" or current_desktop_environment == "ubuntu:GNOME":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version_lines = (subprocess.check_output(["flatpak-spawn", "--host", "gnome-shell", "--version"], shell=False)).decode().strip().split("\n")
                else:
                    current_desktop_environment_version_lines = (subprocess.check_output(["gnome-shell", "--version"], shell=False)).decode().strip().split("\n")
                for line in current_desktop_environment_version_lines:
                    if "GNOME Shell" in line:
                        current_desktop_environment_version = line.split(" ")[-1]
            except FileNotFoundError:
                pass

        if current_desktop_environment == "X-Cinnamon" or current_desktop_environment == "CINNAMON":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version = (subprocess.check_output(["flatpak-spawn", "--host", "cinnamon", "--version"], shell=False)).decode().strip().split(" ")[-1]
                else:
                    current_desktop_environment_version = (subprocess.check_output(["cinnamon", "--version"], shell=False)).decode().strip().split(" ")[-1]
            except FileNotFoundError:
                pass

        if current_desktop_environment == "MATE":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version = (subprocess.check_output(["flatpak-spawn", "--host", "mate-about", "--version"], shell=False)).decode().strip().split(" ")[-1]
                else:
                    current_desktop_environment_version = (subprocess.check_output(["mate-about", "--version"], shell=False)).decode().strip().split(" ")[-1]
            except FileNotFoundError:
                pass

        if current_desktop_environment == "KDE":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version = (subprocess.check_output(["flatpak-spawn", "--host", "plasmashell", "--version"], shell=False)).decode().strip()
                else:
                    current_desktop_environment_version = (subprocess.check_output(["plasmashell", "--version"], shell=False)).decode().strip()
            except FileNotFoundError:
                pass

        if current_desktop_environment == "LXQt":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version_lines = (subprocess.check_output(["flatpak-spawn", "--host", "lxqt-about", "--version"], shell=False)).decode().strip()
                else:
                    current_desktop_environment_version_lines = (subprocess.check_output(["lxqt-about", "--version"], shell=False)).decode().strip()
                for line in current_desktop_environment_version_lines:
                    if "liblxqt" in line:
                        current_desktop_environment_version = line.split()[1].strip()
            except FileNotFoundError:
                pass

        if current_desktop_environment == "Budgie" or current_desktop_environment == "Budgie:GNOME":
            try:
                if Config.environment_type == "flatpak":
                    current_desktop_environment_version = (subprocess.check_output(["flatpak-spawn", "--host", "budgie-desktop", "--version"], shell=False)).decode().strip().split("\n")[0].strip().split(" ")[-1]
                else:
                    current_desktop_environment_version = (subprocess.check_output(["budgie-desktop", "--version"], shell=False)).decode().strip().split("\n")[0].strip().split(" ")[-1]
            except FileNotFoundError:
                pass

        return current_desktop_environment_version


System = System()

