import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow
import Common


class Memory:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.da_grid()

        self.information_grid()


    def tab_title_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Memory)
        label = Common.tab_title_label(_tr("Memory"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label()
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label()
        grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.tab_grid.attach(grid, 0, 1, 1, 1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(_tr("RAM Usage"), Gtk.Align.START)
        grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea (RAM/Memory usage)
        self.da_memory_usage = Common.drawingarea(Performance.performance_line_charts_draw, "da_memory_usage")
        grid.attach(self.da_memory_usage, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Common.performance_info_grid()
        performance_info_grid.set_row_homogeneous(False)
        performance_info_grid.set_row_spacing(6)
        self.tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Label - Title (RAM)
        label = Common.title_label(_tr("RAM"))
        performance_info_grid.attach(label, 0, 0, 1, 1)

        # Styled information widgets (Used and Available)
        # ScrolledWindow (Used and Available)
        scrolledwindow, self.ram_used_label, self.ram_available_label = Common.styled_information_scrolledwindow(_tr("Used"), None, _tr("Available"), None)
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Grid - Lower left information labels
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(2)
        grid.set_row_spacing(3)
        performance_info_grid.attach(grid, 0, 2, 1, 1)

        # Label (Capacity)
        label = Common.static_information_label(_tr("Capacity") + ":")
        grid.attach(label, 0, 0, 1, 1)
        # Label (Capacity)
        self.ram_capacity_label = Common.dynamic_information_label()
        grid.attach(self.ram_capacity_label, 1, 0, 1, 1)

        # Label (Free)
        label = Common.static_information_label(_tr("Free") + ":")
        grid.attach(label, 0, 1, 1, 1)
        # Label (Free)
        self.ram_free_label = Common.dynamic_information_label()
        grid.attach(self.ram_free_label, 1, 1, 1, 1)

        # Label (Hardware)
        label = Common.static_information_label(_tr("Hardware") + ":")
        grid.attach(label, 0, 2, 1, 1)
        # Label (Show...)
        self.ram_hardware_label = Common.clickable_label(_tr("Show..."), self.on_details_label_released)
        grid.attach(self.ram_hardware_label, 1, 2, 1, 1)

        # Label - Title (Swap Memory)
        label = Common.title_label(_tr("Swap Memory"))
        performance_info_grid.attach(label, 1, 0, 1, 1)

        # Styled information widgets (Used and Free)
        # ScrolledWindow (Used and Free)
        scrolledwindow, self.swap_used_label, self.swap_free_label = Common.styled_information_scrolledwindow(_tr("Used"), None, _tr("Free"), None)
        performance_info_grid.attach(scrolledwindow, 1, 1, 1, 1)

        # Grid (lower right information labels)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(2)
        grid.set_row_spacing(3)
        performance_info_grid.attach(grid, 1, 2, 1, 1)

        # Label (Used (swap percent))
        label = Common.static_information_label(_tr("Used") + ":")
        grid.attach(label, 0, 0, 1, 1)
        # Label and DrawingArea (Used (swap percent))
        grid_label_and_da = Gtk.Grid()
        grid_label_and_da.set_column_spacing(5)
        grid.attach(grid_label_and_da, 1, 0, 1, 1)
        # DrawingArea (Used (swap percent))
        self.da_swap_usage = Common.drawingarea(Performance.performance_bar_charts_draw, "da_swap_usage")
        self.da_swap_usage.set_vexpand(False)
        grid_label_and_da.attach(self.da_swap_usage, 0, 0, 1, 1)
        # Label (Used (swap percent))
        self.swap_used_percent_label = Common.dynamic_information_label()
        grid_label_and_da.attach(self.swap_used_percent_label, 1, 0, 1, 1)

        # Label (Capacity (swap))
        label = Common.static_information_label(_tr("Capacity") + ":")
        grid.attach(label, 0, 1, 1, 1)
        # Label (Capacity (swap))
        self.swap_capacity_label = Common.dynamic_information_label()
        grid.attach(self.swap_capacity_label, 1, 1, 1, 1)

        # Label (Details (swap))
        label = Common.static_information_label(_tr("Details") + ":")
        grid.attach(label, 0, 2, 1, 1)
        # Label (Show... (swap))
        self.swap_details_label = Common.clickable_label(_tr("Show..."), self.on_details_label_released)
        grid.attach(self.swap_details_label, 1, 2, 1, 1)


    def on_details_label_released(self, event, count, x, y):
        """
        Show RAM hardware window or swap details window.
        """

        widget = event.get_widget()

        # Show RAM hardware window
        if widget == self.ram_hardware_label:
            memory_ram_hardware_info = self.ram_hardware_info_get()
            try:
                self.ram_hardware_window.present()
            except AttributeError:
                # Avoid generating window multiple times on every button click.
                self.ram_hardware_window_gui()
                self.ram_hardware_window.present()
            self.ram_hardware_win_label.set_label(memory_ram_hardware_info)

        # Show swap details window
        if widget == self.swap_details_label:
            try:
                self.swap_details_window.present()
            except AttributeError:
                # Avoid generating window multiple times on every button click.
                self.swap_details_window_gui()
                self.swap_details_window.present()
            self.swap_details_info_get()
            self.swap_details_update()


    def ram_hardware_window_gui(self):
        """
        RAM hardware window GUI.
        """

        # Window
        self.ram_hardware_window = Gtk.Window()
        self.ram_hardware_window.set_default_size(400, 480)
        self.ram_hardware_window.set_title(_tr("Physical RAM"))
        self.ram_hardware_window.set_icon_name("system-monitoring-center")
        self.ram_hardware_window.set_transient_for(MainWindow.main_window)
        self.ram_hardware_window.set_modal(True)
        self.ram_hardware_window.set_hide_on_close(True)

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.ram_hardware_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid (Main)
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        viewport.set_child(main_grid)

        # Label
        self.ram_hardware_win_label = Gtk.Label()
        self.ram_hardware_win_label.set_halign(Gtk.Align.START)
        self.ram_hardware_win_label.set_valign(Gtk.Align.START)
        self.ram_hardware_win_label.set_selectable(True)
        self.ram_hardware_win_label.set_label("--")
        main_grid.attach(self.ram_hardware_win_label, 0, 0, 1, 1)


    def ram_hardware_info_get(self):
        """
        Get RAM hardware information by using "dmidecode" command.
        """

        # Initial value of the variable
        memory_ram_hardware_info = ""

        # "sudo" has to be used for using "pkexec" to run "dmidecode" with root privileges.
        command_list = ["pkexec", "sudo", "dmidecode", "-t", "16,17"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        try:
            dmidecode_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        except Exception:
            dmidecode_output = "-"
            memory_ram_hardware_info = "-"

        dmidecode_output_lines = dmidecode_output.split("\n")

        # Initial value of "maximum_capacity". This value will be used if value could not be get.
        maximum_capacity = "-"
        number_of_devices = "-"

        # Perform the following operations if "Physical Memory Array" is found in "dmidecode_output" output. This information may not be available on some systems.
        if "Physical Memory Array" in dmidecode_output:
            for line in dmidecode_output_lines:
                line = line.strip()
                if line.startswith("Maximum Capacity:"):
                    maximum_capacity = line.split(":")[1].strip()
                    continue
                if line.startswith("Number Of Devices:"):
                    number_of_devices = line.split(":")[1].strip()
                    continue
        memory_ram_hardware_info = memory_ram_hardware_info + _tr("Maximum Capacity") + " :    " + maximum_capacity
        memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Number Of Devices") + " :    " + number_of_devices + "\n"

        # Perform the following operations if "Memory Device" is found in "dmidecode_output" output. This information may not be available on some systems.
        if "Memory Device" in dmidecode_output:
            data_per_slot = dmidecode_output.split("Memory Device")
            # First element in this list is not information of memory device and it is deleted.
            del data_per_slot[0]
            for data in data_per_slot:
                data_lines = data.split("\n")
                memory_size = "-"
                memory_form_factor = "-"
                memory_locator = "-"
                memory_bank_locator = "-"
                memory_type = "-"
                memory_speed = "-"
                memory_manufacturer = "-"
                for line in data_lines:
                    line = line.strip()
                    if  line.startswith("Size:"):
                        memory_size = line.split(":")[1].strip()
                        continue
                    if line.startswith("Form Factor:"):
                        memory_form_factor = line.split(":")[1].strip()
                        continue
                    if line.startswith("Locator:"):
                        memory_locator = line.split(":")[1].strip()
                        continue
                    if line.startswith("Bank Locator:"):
                        memory_bank_locator = line.split(":")[1].strip()
                        continue
                    if line.startswith("Type:"):
                        memory_type = line.split(":")[1].strip()
                        continue
                    if line.startswith("Speed:"):
                        memory_speed = line.split(":")[1].strip()
                        continue
                    if line.startswith("Manufacturer:"):
                        memory_manufacturer = line.split(":")[1].strip()
                        continue
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Capacity") + " :    " + memory_size
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Type") + " :    " + memory_type
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Speed") + " :    " + memory_speed
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Locator") + " :    " + memory_locator
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator
                memory_ram_hardware_info = memory_ram_hardware_info + "\n"

        # Perform the following operations if "Memory Device" is not found in "dmidecode_output" output. This information may not be available on some systems.
        if "Memory Device" not in dmidecode_output:
            memory_size = "-"
            memory_form_factor = "-"
            memory_locator = "-"
            memory_bank_locator = "-"
            memory_type = "-"
            memory_speed = "-"
            memory_manufacturer = "-"

            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Capacity") + " :    " + memory_size
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Type") + " :    " + memory_type
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Speed") + " :    " + memory_speed
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Locator") + " :    " + memory_locator
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator

        return memory_ram_hardware_info


    def swap_details_window_gui(self):
        """
        Swap details window GUI.
        """

        # Window
        self.swap_details_window = Gtk.Window()
        self.swap_details_window.set_default_size(320, 280)
        self.swap_details_window.set_title(_tr("Swap Memory"))
        self.swap_details_window.set_icon_name("system-monitoring-center")
        self.swap_details_window.set_transient_for(MainWindow.main_window)
        self.swap_details_window.set_modal(True)
        self.swap_details_window.set_hide_on_close(True)

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.swap_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        viewport.set_child(main_grid)

        # Label
        self.swap_details_win_label = Gtk.Label()
        self.swap_details_win_label.set_halign(Gtk.Align.START)
        self.swap_details_win_label.set_valign(Gtk.Align.START)
        self.swap_details_win_label.set_selectable(True)
        self.swap_details_win_label.set_label("--")
        main_grid.attach(self.swap_details_win_label, 0, 0, 1, 1)


    def swap_details_info_get(self):
        """
        Get swap memory details information by reading "/proc/swaps" file.
        """

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        # List for language translation
        memory_swap_details_text_list = [_tr("Partition"), _tr("File")]

        # Set initial value of "memory_hardware_information_text".
        memory_swap_details_info = ""

        # Read "/proc/swaps" file for getting swap memory details.
        # Systems may have more than one swap partition/file and this information can be read from this file.
        with open("/proc/swaps") as reader:
            proc_swaps_lines = reader.read().split("\n")

        # Delete header indormation which is get from "/proc/swaps" file.
        del proc_swaps_lines[0]

        for line in proc_swaps_lines:
            if line == "":
                break
            swap_name = "-"
            swap_type = "-"
            swap_size = "-"
            swap_used = "-"
            swap_priority = "-"
            line_split = line.split()
            swap_name = line_split[0].strip()
            swap_type = line_split[1].strip().title()
            # Values in this file are in KiB. They are converted to Bytes.
            swap_size = int(line_split[2].strip()) * 1024
            swap_size = f'{Performance.performance_data_unit_converter_func("data", "none", swap_size, performance_memory_data_unit, performance_memory_data_precision)}'
            swap_used = int(line_split[3].strip()) * 1024
            swap_used = f'{Performance.performance_data_unit_converter_func("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}'
            swap_priority = line_split[4].strip()
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Name") + " :    " + swap_name
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Type") + " :    " + _tr(swap_type)
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Capacity") + " :    " + swap_size
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Used") + " :    " + swap_used
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Priority") + " :    " + swap_priority
            memory_swap_details_info = memory_swap_details_info + "\n"
            memory_swap_details_info = memory_swap_details_info + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"

        # In order to remove this string from the last line.
        memory_swap_details_info = memory_swap_details_info.strip("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

        # Remove empty lines.
        memory_swap_details_info = memory_swap_details_info.strip()

        if memory_swap_details_info.strip() == "":
            memory_swap_details_info = "-"

        self.swap_details_win_label.set_label(memory_swap_details_info)


    def swap_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        if self.swap_details_window.get_visible() == True:
            # Destroy GLib source for preventing it repeating the function.
            try:
                self.main_glib_source.destroy()
            # Prevent errors if this is first run of the function.
            except AttributeError:
                pass
            self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)
            self.swap_details_info_get()
            self.main_glib_source.set_callback(self.swap_details_update)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
            # A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    def memory_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        total_physical_ram = self.physical_ram()
        ram_total = self.ram_capacity()


        # Set Memory tab label texts by using information get
        if total_physical_ram != "-":
            self.device_vendor_model_label.set_text(_tr("Physical RAM") + ": " + str(Performance.performance_data_unit_converter_func("data", "none", total_physical_ram, 0, 1)))
        else:
            self.device_vendor_model_label.set_text(_tr("RAM") + " - " + _tr("Capacity") + ": " + str(Performance.performance_data_unit_converter_func("data", "none", ram_total, 0, 1)))

        self.initial_already_run = 1


    def memory_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        ram_used = Performance.ram_used
        ram_usage_percent = Performance.ram_usage_percent
        ram_available = Performance.ram_available
        ram_free = Performance.ram_free
        ram_total = Performance.ram_total

        self.swap_usage_percent = Performance.swap_usage_percent
        swap_used = Performance.swap_used
        swap_free = Performance.swap_free
        swap_total = Performance.swap_total

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        self.da_memory_usage.queue_draw()
        self.da_swap_usage.queue_draw()


        # Set and update Memory tab label texts by using information get
        self.device_kernel_name_label.set_text(_tr("Swap Memory") + ": " + str(Performance.performance_data_unit_converter_func("data", "none", swap_total, 0, 1)))
        self.ram_used_label.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", ram_used, performance_memory_data_unit, performance_memory_data_precision)}  ( {ram_usage_percent[-1]:.0f}% )')
        self.ram_available_label.set_text(Performance.performance_data_unit_converter_func("data", "none", ram_available, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_capacity_label.set_text(Performance.performance_data_unit_converter_func("data", "none", ram_total, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_free_label.set_text(Performance.performance_data_unit_converter_func("data", "none", ram_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_used_label.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}  ( {self.swap_usage_percent[-1]:.0f}% )')
        self.swap_used_percent_label.set_text(f'{self.swap_usage_percent[-1]:.0f}%')
        self.swap_free_label.set_text(Performance.performance_data_unit_converter_func("data", "none", swap_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_capacity_label.set_text(Performance.performance_data_unit_converter_func("data", "none", swap_total, performance_memory_data_unit, performance_memory_data_precision))


    def physical_ram(self):
        """
        Get physical ram value. Summation of total online and offline memories gives RAM hardware size.
        This value is very similar to RAM hardware size which is a bit different than ram_total value.
        RAM hardware size and total RAM value (get from proc file system by using "free" command) are not same thing.
        Because some of the RAM may be reserved for hardware and/or by the OS kernel.
        "block_size_bytes" file may not be present on some systems such as ARM CPU used systems.
        Physical RAM can not be detected on these systems. "vcgencmd" Python module can be used for physical RAM of RB-Pi devices.
        But this module is not installed on these systems by default.
        Currently kernel 5.10 does not have this feature but this feature will be included in the newer versions of the kernel.
        Size of the blocks (block_size_bytes) depend on architecture.
        For more information see: https://www.kernel.org/doc/html/latest/admin-guide/mm/memory-hotplug.html
        """

        # Get "memory block size" and convert hex value to integer (byte).
        try:
            with open("/sys/devices/system/memory/block_size_bytes") as reader:
                block_size = int(reader.read().strip(), 16)
        except FileNotFoundError:
            block_size = "-"

        # Get physical RAM value
        if block_size != "-":
            total_online_memory = 0
            total_offline_memory = 0
            # Folder (of which name start with "memory") in this folder is multiplied with memory block size.
            files_in_sys_devices_system_memory = os.listdir("/sys/devices/system/memory/")
            for file in files_in_sys_devices_system_memory:
                if os.path.isdir("/sys/devices/system/memory/" + file) and file.startswith("memory"):
                    with open("/sys/devices/system/memory/" + file + "/online") as reader:
                        memory_online_offline_value = reader.read().strip()
                    if memory_online_offline_value == "1":
                        total_online_memory = total_online_memory + block_size
                    if memory_online_offline_value == "0":
                        total_offline_memory = total_offline_memory + block_size
            total_physical_ram = (total_online_memory + total_offline_memory)

        # Try to get physical RAM for RB Pi devices.
        else:
            command_list = ["vcgencmd", "get_config", "total_mem"]
            _environment_type = environment_type()
            if _environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            try:
                total_physical_ram = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
                # Convert MiB value to bytes
                total_physical_ram = float(total_physical_ram) * 1024 * 1024
            except Exception:
                total_physical_ram = "-"

        return total_physical_ram


    def ram_capacity(self):
        """
        Get RAM capacity.
        """

        with open("/proc/meminfo") as reader:
            proc_memory_info_output_lines = reader.read().split("\n")

        for line in proc_memory_info_output_lines:
            if "MemTotal:" in line:
                # Convert KiB value to bytes
                ram_total = int(line.split()[1]) * 1024

        return ram_total


Memory = Memory()

