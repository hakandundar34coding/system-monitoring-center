#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, Gdk, GLib
import os
import subprocess
from threading import Thread

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Gpu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuTab.ui")

        # Get GUI objects
        self.grid1501 = builder.get_object('grid1501')
        self.drawingarea1501 = builder.get_object('drawingarea1501')
        self.button1501 = builder.get_object('button1501')
        self.label1501 = builder.get_object('label1501')
        self.label1502 = builder.get_object('label1502')
        self.label1503 = builder.get_object('label1503')
        self.label1504 = builder.get_object('label1504')
        self.label1505 = builder.get_object('label1505')
        self.label1506 = builder.get_object('label1506')
        self.label1507 = builder.get_object('label1507')
        self.label1508 = builder.get_object('label1508')
        self.label1509 = builder.get_object('label1509')
        self.label1510 = builder.get_object('label1510')
        self.label1511 = builder.get_object('label1511')
        self.label1512 = builder.get_object('label1512')

        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-radius: 8px 8px 8px 8px;}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        self.viewport1501 = builder.get_object('viewport1501')
        self.viewport1501.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.viewport1502 = builder.get_object('viewport1502')
        self.viewport1502.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        self.separator1501 = builder.get_object('separator1501')
        self.separator1501.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1502 = builder.get_object('separator1502')
        self.separator1502.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1503 = builder.get_object('separator1503')
        self.separator1503.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1504 = builder.get_object('separator1504')
        self.separator1504.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_line_charts_draw_func = Performance.performance_line_charts_draw_func
        self.performance_line_charts_enter_notify_event_func = Performance.performance_line_charts_enter_notify_event_func
        self.performance_line_charts_leave_notify_event_func = Performance.performance_line_charts_leave_notify_event_func
        self.performance_line_charts_motion_notify_event_func = Performance.performance_line_charts_motion_notify_event_func

        # Connect GUI signals
        self.button1501.connect("clicked", self.on_button1501_clicked)
        self.drawingarea1501.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea1501.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea1501.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea1501.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)

        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea1501.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)

        # "0" value of "initial_already_run" variable means that initial function is not run before or tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1501_clicked(self, widget):

        # Open customizations menu
        from GpuMenu import GpuMenu
        GpuMenu.popover1501p.set_relative_to(widget)
        GpuMenu.popover1501p.set_position(1)
        GpuMenu.popover1501p.popup()


    # ----------------------------------- GPU - Initial Function -----------------------------------
    def gpu_initial_func(self):

        # Define initial values
        self.chart_data_history = Config.chart_data_history
        self.gpu_load_list = [0] * self.chart_data_history
        # Currently highest monitor refresh rate is 360. 365 is used in order to get GPU load for AMD GPUs precisely.
        self.amd_gpu_load_list = [0] * 365


        # Get information.
        self.gpu_get_gpu_list_and_boot_vga_func()
        self.gpu_set_selected_gpu_func()
        if_default_gpu = self.gpu_default_gpu_func()
        gpu_device_model_name = self.gpu_device_model_name_vendor_id_func()
        gpu_driver_name = self.gpu_driver_name_func()


        # Set GPU tab label texts by using information get
        self.label1501.set_text(gpu_device_model_name)
        self.label1502.set_text(f'{self.gpu_list[self.selected_gpu_number]}')
        self.label1507.set_text(if_default_gpu)
        self.label1510.set_text(gpu_driver_name)

        self.initial_already_run = 1


    # ----------------------------------- GPU - Get GPU Data Function -----------------------------------
    def gpu_loop_func(self):

        # Run "gpu_initial_func" if "initial_already_run variable is "0" which means all settings of the application is reset and initial function has be be run in order to avoid errors. This check is required only for GPU tab (not required for other Performance tab sub-tabs).
        if self.initial_already_run == 0:
            self.gpu_initial_func()

        # Get information.
        current_resolution, current_refresh_rate = self.gpu_resolution_refresh_rate_func()
        gpu_pci_address = self.gpu_pci_address_func()
        gpu_load, gpu_memory, gpu_current_frequency, gpu_min_max_frequency, gpu_temperature, gpu_power = self.gpu_load_memory_frequency_power_func(gpu_pci_address)

        gpu_load = gpu_load.split()[0]
        if gpu_load == "-":
            self.gpu_load_list.append(0)
            gpu_load = "-"
        else:
            self.gpu_load_list.append(float(gpu_load))
            gpu_load = f'{gpu_load} %'
        del self.gpu_load_list[0]

        try:
            gpu_temperature = float(gpu_temperature)
            gpu_temperature = f'{gpu_temperature:.0f} °C'
        except ValueError:
            pass

        self.drawingarea1501.queue_draw()

        # Run "main_gui_device_selection_list_func" if selected device list is changed since the last loop.
        gpu_list = self.gpu_list
        try:                                                                                      
            if self.gpu_list_prev != gpu_list:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
        except AttributeError:
            from MainGUI import MainGUI
            MainGUI.main_gui_device_selection_list_func()
        self.gpu_list_prev = gpu_list


        # Set and update GPU tab label texts by using information get
        self.label1503.set_text(gpu_load)
        self.label1504.set_text(gpu_memory)
        self.label1505.set_text(gpu_current_frequency)
        self.label1506.set_text(gpu_min_max_frequency)
        self.label1508.set_text(gpu_power)
        self.label1509.set_text(gpu_temperature)
        self.label1511.set_text(current_refresh_rate)
        self.label1512.set_text(f'{current_resolution}')


    # ----------------------- Get GPU list -----------------------
    def gpu_get_gpu_list_and_boot_vga_func(self):

        self.gpu_list = []
        self.gpu_device_path_list = []
        self.gpu_device_sub_path_list = []
        self.default_gpu = ""

        # Get GPU list from "/sys/class/drm/" directory which is used by x86_64 desktop systems.
        if os.path.isdir("/dev/dri/") == True:

            for file in os.listdir("/sys/class/drm/"):
                if "-" not in file and file.split("-")[0].rstrip("0123456789") == "card":
                    self.gpu_list.append(file)
                    self.gpu_device_path_list.append("/sys/class/drm/" + file + "/")
                    self.gpu_device_sub_path_list.append("/device/")

                    # Get if default GPU information.
                    try:
                        with open("/sys/class/drm/" + file + "/device/" + "boot_vga") as reader:
                            if reader.read().strip() == "1":
                                self.default_gpu = file
                    except (FileNotFoundError, NotADirectoryError) as me:
                        pass

        # Try to get GPU list from "/sys/devices/" folder which is used by some ARM systems with NVIDIA GPU.
        for file in os.listdir("/sys/devices/"):

            if file.split(".")[0] == "gpu":
                self.gpu_list.append(file)
                self.gpu_device_path_list.append("/sys/devices/" + file + "/")
                self.gpu_device_sub_path_list.append("/")

                # Get if default GPU information
                try:
                    with open("/sys/devices/" + file + "/" + "boot_vga") as reader:
                        if reader.read().strip() == "1":
                            self.default_gpu = file
                except (FileNotFoundError, NotADirectoryError) as me:
                    pass


    # ----------------------- Get default GPU -----------------------
    def gpu_set_selected_gpu_func(self):

        # "" is predefined gpu name before release of the software. This statement is used in order to avoid error, if no gpu selection is made since first run of the software.
        if Config.selected_gpu == "":
            if self.default_gpu != "":
                set_selected_gpu = self.default_gpu
            if self.default_gpu == "":
                set_selected_gpu = self.gpu_list[0]
        if Config.selected_gpu in self.gpu_list:
            set_selected_gpu = Config.selected_gpu
        else:
            if self.default_gpu != "":
                set_selected_gpu = self.default_gpu
            if self.default_gpu == "":
                set_selected_gpu = self.gpu_list[0]
        self.selected_gpu_number = self.gpu_list.index(set_selected_gpu)


    # ----------------------- Get if default GPU -----------------------
    def gpu_default_gpu_func(self):

        # Set default GPU if there is only 1 GPU on the system and these is not "boot_vga" file (on some systems such as ARM devices) which means default_gpu = "".
        if len(self.gpu_list) == 1:
            if_default_gpu = _tr("Yes")
        else:
            if self.gpu_list[self.selected_gpu_number] == self.default_gpu:
                if_default_gpu = _tr("Yes")
            else:
                if_default_gpu = _tr("No")

        return if_default_gpu


    # ----------------------- Get GPU driver name -----------------------
    def gpu_driver_name_func(self):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Read device driver name by reading "uevent" file.
        with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
            uevent_output_lines = reader.read().strip().split("\n")

        gpu_driver_name = "-"
        for line in uevent_output_lines:
            if line.startswith("DRIVER="):
                gpu_driver_name = line.split("=")[-1]
                break

        return gpu_driver_name


    # ----------------------- Get GPU device model name and vendor name -----------------------
    def gpu_device_model_name_vendor_id_func(self):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Read device vendor and model ids by reading "modalias" file.
        with open(gpu_device_path + gpu_device_sub_path + "modalias") as reader:
            modalias_output = reader.read().strip()

        # Determine device subtype.
        device_subtype, device_alias = modalias_output.split(":", 1)
        device_vendor_name, device_model_name, self.device_vendor_id, device_model_id = Performance.performance_get_device_vendor_model_func(modalias_output)
        if device_vendor_name == "Unknown":
            device_vendor_name = "[" + _tr("Unknown") + "]"
        if device_model_name == "Unknown":
            device_model_name = "[" + _tr("Unknown") + "]"
        gpu_device_model_name = f'{device_vendor_name} - {device_model_name}'

        return gpu_device_model_name


    # ----------------------- Get GPU PCI address which will be used for detecting the selected GPU for processing GPU performance information -----------------------
    def gpu_pci_address_func(self):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Read device driver name by reading "uevent" file.
        with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
            uevent_output_lines = reader.read().strip().split("\n")

        # ARM GPUs does not have PCI address.
        gpu_pci_address = "-"
        for line in uevent_output_lines:
            if line.startswith("PCI_SLOT_NAME="):
                gpu_pci_address = line.split("=")[-1]
                break

        return gpu_pci_address


    # ----------------------- Get GPU load, memory, frequencies, power -----------------------
    def gpu_load_memory_frequency_power_func(self, gpu_pci_address):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Define initial values. These values will be used if they can not be detected.
        gpu_load = "-"
        gpu_memory_used = "-"
        gpu_memory_capacity = "-"
        gpu_temperature = "-"
        gpu_current_frequency = "-"
        gpu_min_frequency = "-"
        gpu_max_frequency = "-"
        gpu_min_max_frequency = "-"
        gpu_power = "-"


        # If selected GPU vendor is Intel.
        if self.device_vendor_id == "v00008086":

            # Get GPU min frequency.
            try:
                with open(gpu_device_path + "gt_min_freq_mhz") as reader:
                    gpu_min_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_min_frequency = "-"

            if gpu_min_frequency != "-":
                gpu_min_frequency = f'{gpu_min_frequency} MHz'

            # Get GPU max frequency.
            try:
                with open(gpu_device_path + "gt_max_freq_mhz") as reader:
                    gpu_max_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_max_frequency = "-"

            if gpu_max_frequency != "-":
                gpu_max_frequency = f'{gpu_max_frequency} MHz'

            # Get GPU current frequency by reading "gt_cur_freq_mhz" file. This file may not be reliable because is contains a constant value on some systems. Actual value can be get by using "intel_gpu_top" tool by using root privileges.
            try:
                with open(gpu_device_path + "gt_cur_freq_mhz") as reader:
                    gpu_current_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_current_frequency = "-"

            if gpu_current_frequency != "-":
                gpu_current_frequency = f'{gpu_current_frequency} MHz'


        # If selected GPU vendor is AMD.
        if self.device_vendor_id in ["v00001022", "v00001002"]:

            # For more information about files under "/sys/class/drm/card[NUMBER]/device/" and their content for AMD GPUs: https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html and https://wiki.archlinux.org/title/AMDGPU.

            # Get GPU current, min, max frequencies (engine frequencies). This file contains all available frequencies of the GPU. There is no separate frequency information in files for video clock frequency for AMD GPUs.
            gpu_frequency_file_output = "-"
            try:
                with open(gpu_device_path + "device/pp_dpm_sclk") as reader:
                    gpu_frequency_file_output = reader.read().strip().split("\n")
            except FileNotFoundError:
                gpu_current_frequency = "-"
                gpu_max_frequency = "-"

            if gpu_frequency_file_output != "-":
                for line in gpu_frequency_file_output:
                    if "*" in line:
                        gpu_current_frequency = line.split(":")[1].rstrip("*").strip()
                        # Add a space character between value and unit. "Mhz" is used in the relevant file instead of "MHz".
                        if "Mhz" in gpu_current_frequency:
                            gpu_current_frequency = gpu_current_frequency.split("Mhz")[0] + " MHz"
                        break
                gpu_min_frequency = gpu_frequency_file_output[0].split(":")[1].strip()
                # Add a space character between value and unit.
                if "Mhz" in gpu_min_frequency:
                    gpu_min_frequency = gpu_min_frequency.split("Mhz")[0] + " MHz"
                gpu_max_frequency = gpu_frequency_file_output[-1].split(":")[1].strip()
                # Add a space character between value and unit.
                if "Mhz" in gpu_max_frequency:
                    gpu_max_frequency = gpu_max_frequency.split("Mhz")[0] + " MHz"

            # Get GPU load average. There is no "%" character in "gpu_busy_percent" file. This file contains GPU load for a very small time.
            try:
                self.gpu_load_amd_func()
                gpu_load = f'{(sum(self.amd_gpu_load_list) / len(self.amd_gpu_load_list)):.0f} %'
            except Exception:
                gpu_load = "-"

            # Get GPU used memory (data in this file is in Bytes). There is also "mem_info_vis_vram_used" file for visible memory (can be shown on the "lspci" command) and "mem_info_gtt_used" file for reserved memory from system memory. gtt+vram=total video memory. Probably "mem_busy_percent" is for memory controller load.
            try:
                with open(gpu_device_path + "device/mem_info_vram_used") as reader:
                    gpu_memory_used = reader.read().strip()
            except FileNotFoundError:
                gpu_memory_used = "-"

            if gpu_memory_used != "-":
                gpu_memory_used = f'{(int(gpu_memory_used) / 1024 / 1024):.0f} MiB'

            # Get GPU memory capacity (data in this file is in Bytes).
            try:
                with open(gpu_device_path + "device/mem_info_vram_total") as reader:
                    gpu_memory_capacity = reader.read().strip()
            except FileNotFoundError:
                gpu_memory_capacity = "-"

            if gpu_memory_capacity != "-":
                gpu_memory_capacity = f'{(int(gpu_memory_capacity) / 1024 / 1024):.0f} MiB'

            # Get GPU temperature.
            try:
                gpu_sensor_list = os.listdir(gpu_device_path + "device/hwmon/")
                for sensor in gpu_sensor_list:
                    if os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/temp1_input") == True:
                        with open(gpu_device_path + "device/hwmon/" + sensor + "/temp1_input") as reader:
                            gpu_temperature = reader.read().strip()
                        gpu_temperature = f'{(int(gpu_temperature) / 1000):.0f} °C'
                        break
            except (FileNotFoundError, NotADirectoryError, OSError) as me:
                gpu_temperature = "-"

            # Get GPU power usage.
            try:
                gpu_sensor_list = os.listdir(gpu_device_path + "device/hwmon/")
                for sensor in gpu_sensor_list:
                    if os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_input") == True:
                        with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_input") as reader:
                            gpu_power = reader.read().strip()
                        # Value in this file is in microwatts.
                        gpu_power = f'{(int(gpu_power) / 1000000):.2f} W'
                    elif os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_average") == True:
                        with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_average") as reader:
                            gpu_power = reader.read().strip()
                        gpu_power = f'{(int(gpu_power) / 1000000):.2f} W'
                    else:
                        gpu_power = "-"
            except (FileNotFoundError, NotADirectoryError, OSError) as me:
                gpu_power = "-"


        # If selected GPU vendor is Broadcom (for RB-Pi ARM devices).
        if self.device_vendor_id in ["Brcm"]:

            # Get GPU memory capacity. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
            try:
                gpu_memory_capacity = (subprocess.check_output(["vcgencmd", "get_mem", "gpu"], shell=False)).decode().strip().split("=")[1]
            except Exception:
                gpu_memory_capacity = "-"

            # Get GPU current frequency. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
            try:
                gpu_current_frequency = (subprocess.check_output(["vcgencmd", "measure_clock", "core"], shell=False)).decode().strip().split("=")[1]
                gpu_current_frequency = f'{float(gpu_current_frequency)/1000000:.0f} MHz'
            except Exception:
                gpu_current_frequency = "-"


        # If selected GPU vendor is NVIDIA and selected GPU is used on a PCI used system.
        if self.device_vendor_id == "v000010DE" and gpu_device_path.startswith("/sys/class/drm/") == True:

            # Try to get GPU usage information in a separate thread in order to prevent this function from blocking the main thread and GUI for a very small time which stops the GUI for a very small time.
            gpu_tool_output = "-"
            Thread(target=self.gpu_load_nvidia_func, daemon=True).start()

            try:
                gpu_tool_output = self.gpu_tool_output
            # Prevent error if thread is not finished before using the output variable "gpu_tool_output".
            except AttributeError:
                pass

            # Get values from command output if there was no error when running the command.
            if gpu_tool_output != "-":

                # Get line number of the selected GPU by using its PCI address.
                for i, line in enumerate(gpu_tool_output):
                    if gpu_pci_address in line or gpu_pci_address.upper() in line:
                        gpu_info_line_no = i
                        break

                gpu_tool_output_for_selected_gpu = gpu_tool_output[gpu_info_line_no].split(",")

                gpu_load = gpu_tool_output_for_selected_gpu[3].strip()
                gpu_memory_capacity = gpu_tool_output_for_selected_gpu[5].strip()
                gpu_memory_used = gpu_tool_output_for_selected_gpu[7].strip()
                gpu_temperature = gpu_tool_output_for_selected_gpu[8].strip()
                gpu_current_frequency = gpu_tool_output_for_selected_gpu[9].strip()
                gpu_max_frequency = gpu_tool_output_for_selected_gpu[10].strip()
                gpu_power = gpu_tool_output_for_selected_gpu[11].strip()

                if gpu_load in ["[Not Supported]", "[N/A]"]:
                    gpu_load = "-"
                if gpu_memory_used in ["[Not Supported]", "[N/A]"]:
                    gpu_memory_used = "-"
                if gpu_memory_capacity in ["[Not Supported]", "[N/A]"]:
                    gpu_memory_capacity = "-"
                if gpu_temperature in ["[Not Supported]", "[N/A]"]:
                    gpu_temperature = "-"
                if gpu_current_frequency in ["[Not Supported]", "[N/A]"]:
                    gpu_current_frequency = "-"
                if gpu_max_frequency in ["[Not Supported]", "[N/A]"]:
                    gpu_max_frequency = "-"
                if gpu_power in ["[Not Supported]", "[N/A]"]:
                    gpu_power = "-"

            try:
                gpu_temperature = float(gpu_temperature)
                gpu_temperature = f'{gpu_temperature:.0f} °C'
            except ValueError:
                pass


        # If selected GPU vendor is NVIDIA and selected GPU is used on an ARM system.
        if self.device_vendor_id in ["v000010DE", "Nvidia"] and gpu_device_path.startswith("/sys/devices/") == True:

            # Get GPU frequency folders list. NVIDIA Tegra GPU files are listed in "/sys/devices/gpu.0/devfreq/57000000.gpu/" folder.
            gpu_frequency_files_list = os.listdir(gpu_device_path + "devfreq/")
            gpu_frequency_folders_list = []
            for file in gpu_frequency_files_list:
                if file.endswith(".gpu") and os.path.isdir(gpu_device_path + "devfreq/" + file) == True:
                    gpu_frequency_folders_list.append(gpu_device_path + "devfreq/" + file + "/")
            gpu_frequency_folder = gpu_frequency_folders_list[0]

            # Get GPU min frequency.
            try:
                with open(gpu_frequency_folder + "min_freq") as reader:
                    gpu_min_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_min_frequency = "-"

            if gpu_min_frequency != "-":
                gpu_min_frequency = f'{(float(gpu_min_frequency) / 1000000):.0f}'

            # Get GPU max frequency.
            try:
                with open(gpu_frequency_folder + "max_freq") as reader:
                    gpu_max_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_max_frequency = "-"

            if gpu_max_frequency != "-":
                gpu_max_frequency = f'{(float(gpu_max_frequency) / 1000000):.0f} MHz'

            # Get GPU current frequency.
            try:
                with open(gpu_frequency_folder + "cur_freq") as reader:
                    gpu_current_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_current_frequency = "-"

            if gpu_current_frequency != "-":
                gpu_current_frequency = f'{(float(gpu_current_frequency) / 1000000):.0f} MHz'

            # Get GPU load.
            try:
                with open(gpu_device_path + "load") as reader:
                    gpu_load = reader.read().strip()
            except FileNotFoundError:
                gpu_load = "-"

            if gpu_load != "-":
                gpu_load = f'{(float(gpu_load) / 10):.0f} %'


        gpu_memory = f'{gpu_memory_used} / {gpu_memory_capacity}'
        gpu_min_max_frequency = f'{gpu_min_frequency} - {gpu_max_frequency}'

        return gpu_load, gpu_memory, gpu_current_frequency, gpu_min_max_frequency, gpu_temperature, gpu_power


    # ----------------------- Get GPU load average for NVIDIA (PCI) GPUs -----------------------
    def gpu_load_nvidia_func(self):

        # Define command for getting GPU usage information.
        gpu_tool_command = ["nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,power.draw", "--format=csv"]

        # Try to get GPU usage information.
        try:
            self.gpu_tool_output = (subprocess.check_output(gpu_tool_command, shell=False)).decode().strip().split("\n")
        # Prevent errors because nvidia-smi may not be installed on some devices (such as N.Switch with NVIDIA Tegra GPU).
        except FileNotFoundError:
            pass


    # ----------------------- Get GPU load average for AMD GPUs -----------------------
    def gpu_load_amd_func(self, *args):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.gpu_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.gpu_glib_source = GLib.timeout_source_new(1000 / 365)

        # Read file to get GPU load information. This information is calculated for a very small time (screen refresh rate or content (game, etc.) refresh rate?) and directly plotting this data gives spikes.
        with open(gpu_device_path + "device/gpu_busy_percent") as reader:
            gpu_load = reader.read().strip()

        # Add GPU load data into a list in order to calculate average of the list.
        self.amd_gpu_load_list.append(float(gpu_load))
        del self.amd_gpu_load_list[0]

        # Prevent running the function again if tab is GPU switched off.
        if Config.current_main_tab != 0 or Config.performance_tab_current_sub_tab != 4:
            return

        self.gpu_glib_source.set_callback(self.gpu_load_amd_func)
        # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
        self.gpu_glib_source.attach(GLib.MainContext.default())


    # ----------------------- Get screen resolution and refresh rate -----------------------
    def gpu_resolution_refresh_rate_func(self):

        # Get current screen.
        current_screen = Gdk.Screen.get_default()

        # Get current screen resolution.
        try:
            xrandr_output = (subprocess.check_output(["xrandr"], shell=False)).decode().strip()
            xrandr_output_lines = xrandr_output.split("\n")
            if "Screen 1:" not in xrandr_output:
                for line in xrandr_output_lines:
                    if "Screen 0:" in line:
                        current_resolution = ''.join(line.split("current")[1].split(",")[0].strip().split(" "))
        except Exception:
            xrandr_output = "-"
            current_resolution = "-"
        if current_resolution == "-":
            current_resolution = str(current_screen.get_width()) + "x" + str(current_screen.get_height())

        # Get current refresh rate
        try:
            current_monitor_number = current_screen.get_monitor_at_window(current_screen.get_active_window())
            current_display = Gdk.Display.get_default()
            current_refresh_rate = current_display.get_monitor(current_monitor_number).get_refresh_rate()
            current_refresh_rate = int(current_refresh_rate) / 1000
        except Exception:
            current_refresh_rate = "Unknown"

        # If refresh rate is not get or it is smaller than 30 (incorrect values such as 1, 2.14 are get on some systems such as RB-Pi devices), get it by using xrandr (if there is only one monitor connected).
        if current_refresh_rate == "Unknown" or current_refresh_rate < 30:
            try:
                if xrandr_output == "-":
                    xrandr_output = (subprocess.check_output(["xrandr"], shell=False)).decode().strip()
                    xrandr_output_lines = xrandr_output.split("\n")
                number_of_monitors = xrandr_output.count(" connected")
                if number_of_monitors == 1:
                    for line in xrandr_output_lines:
                        if "*" in line:
                            line_split = line.split()
                            for string_in_line in line_split:
                                if "*" in string_in_line:
                                    current_refresh_rate = float(string_in_line.strip().rstrip("*+"))
                                    break
            except Exception:
                pass

        if current_refresh_rate != "Unknown":
            current_refresh_rate = f'{current_refresh_rate:.2f} Hz'
        else:
            current_refresh_rate = f'[{_tr("Unknown")}]'

        return current_resolution, current_refresh_rate


# Generate object
Gpu = Gpu()

