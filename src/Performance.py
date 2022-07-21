#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os
import cairo
from math import sqrt, ceil, sin, cos

from locale import gettext as _tr

from Config import Config


# Define class
class Performance:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Set chart performance data line and point highligting off. "chart_line_highlight" takes 0/1 values for highlighting or not. "chart_point_highlight" takes data point index or "-1" for not highlighting.
        self.chart_line_highlight = 0
        self.chart_point_highlight = -1


    # ----------------------------------- Performance - Set Selected CPU Core Function -----------------------------------
    def performance_set_selected_cpu_core_func(self):

        # Set selected CPU core
        first_core = self.logical_core_list[0]
        if Config.selected_cpu_core in self.logical_core_list:
            selected_cpu_core = Config.selected_cpu_core
        else:
            selected_cpu_core = first_core
        self.selected_cpu_core_number = self.logical_core_list_system_ordered.index(selected_cpu_core)

        # Definition to access to this variable from other modules.
        self.selected_cpu_core = selected_cpu_core


    # ----------------------------------- Performance - Set Selected Disk Function -----------------------------------
    def performance_set_selected_disk_func(self):

        # Set selected disk
        with open("/proc/mounts") as reader:
            proc_mounts_output_lines = reader.read().strip().split("\n")
        system_disk_list = []
        for line in proc_mounts_output_lines:
            line_split = line.split(" ", 2)
            if line_split[1].strip() == "/":
                disk = line_split[0].strip().split("/")[-1]
                # "/dev/root" disk is not listed in "/proc/partitions" file.
                if disk in self.disk_list:
                    system_disk_list.append(disk)
                    break
        # Detect system disk by checking if mount point is "/" on some systems such as some ARM devices. "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
        if system_disk_list == []:
            with open("/proc/cmdline") as reader:
                proc_cmdline = reader.read()
            if "root=UUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk_list.append(os.path.realpath(f'/dev/disk/by-uuid/{disk_uuid_partuuid}').split("/")[-1].strip())
            if "root=PARTUUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk_list.append(os.path.realpath(f'/dev/disk/by-partuuid/{disk_uuid_partuuid}').split("/")[-1].strip())

        if Config.selected_disk in self.disk_list:
            selected_disk = Config.selected_disk
        else:
            if system_disk_list != []:
                selected_disk = system_disk_list[0]
            else:
                selected_disk = self.disk_list[0]
                # Try to not to set selected disk a loop, ram, zram disk in order to avoid errors if "hide_loop_ramdisk_zram_disks" option is enabled and performance data of all disks are plotted at the same time. loop device may be the first disk on some systems if they are run without installation.
                for disk in self.disk_list:
                    if disk.startswith("loop") == False and disk.startswith("ram") == False and disk.startswith("zram") == False:
                        selected_disk = disk
                        break

        self.system_disk_list = system_disk_list
        self.selected_disk_number = self.disk_list_system_ordered.index(selected_disk)


    # ----------------------------------- Performance - Set Selected Network Card Function -----------------------------------
    def performance_set_selected_network_card_func(self):

        # Set selected network card
        connected_network_card_list = []
        for network_card in self.network_card_list:
            with open(f'/sys/class/net/{network_card}/operstate') as reader:
                sys_class_net_output = reader.read().strip()
            if sys_class_net_output == "up":
                connected_network_card_list.append(network_card)
        # Avoid errors if there is no any network card that connected.
        if connected_network_card_list != []:
            selected_network_card = connected_network_card_list[0]
        else:
            selected_network_card = self.network_card_list[0]
        # "" is predefined network card name before release of the software. This statement is used in order to avoid error, if no network card selection is made since first run of the software.
        if Config.selected_network_card == "":
            selected_network_card_number = self.network_card_list.index(selected_network_card)
        if Config.selected_network_card in self.network_card_list:
            selected_network_card_number = self.network_card_list.index(Config.selected_network_card)
        else:
            selected_network_card_number = self.network_card_list.index(selected_network_card)

        # Definition to access to this variable from other modules.
        self.selected_network_card_number = selected_network_card_number


    # ----------------------------------- Performance - Background Initial Function -----------------------------------
    def performance_background_initial_func(self):

        self.chart_data_history = Config.chart_data_history

        # Define initial values for CPU usage percent
        self.logical_core_list = []
        self.cpu_time_all_prev = []
        self.cpu_time_load_prev = []
        self.cpu_usage_percent_per_core = []
        self.cpu_usage_percent_ave = [0] * self.chart_data_history

        # Define initial values for RAM usage percent and swap usage percent
        self.ram_usage_percent = [0] * self.chart_data_history
        self.swap_usage_percent = [0] * self.chart_data_history

        # Define initial values for disk read speed and write speed
        # Disk data from /proc/diskstats are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).
        self.disk_sector_size = 512
        self.disk_list = []
        self.disk_read_data_prev = []
        self.disk_write_data_prev = []
        self.disk_read_speed = []
        self.disk_write_speed = []

        # Define initial values for network receive speed and network send speed
        self.network_card_list = []
        self.network_receive_bytes_prev = []
        self.network_send_bytes_prev =[]
        self.network_receive_speed = []
        self.network_send_speed = []

        # Reset selected hardware if "remember_last_selected_hardware" prefrence is disabled by the user.
        if Config.remember_last_selected_hardware == 0:
            Config.selected_cpu_core = ""
            Config.selected_disk = ""
            Config.selected_network_card = ""
            Config.selected_gpu = ""


    # ----------------------------------- Performance - Background Function (gets basic CPU, memory, disk and network usage data in the background in order to assure uninterrupted data for charts) -----------------------------------
    def performance_background_loop_func(self):

        # Definition for lower CPU usage because this variable is used multiple times in this function.
        update_interval = Config.update_interval

        # Get CPU core list
        self.logical_core_list_system_ordered = []                                            # "logical_core_list_system_ordered" contains online CPU core numbers in the order of "/proc/stats" file content which is in "ascending" online core number order.
        with open("/proc/stat") as reader:                                                    # "/proc/stat" file contains online logical CPU core numbers (all cores without regarding CPU sockets, physical/logical cores) and CPU times since system boot.
            proc_stat_lines = reader.read().split("intr", 1)[0].strip().split("\n")[1:]       # Trimmed unneeded information in the file
        for line in proc_stat_lines:
            self.logical_core_list_system_ordered.append(line.split(" ", 1)[0])               # Add CPU core names into a temporary list in ascending core number order. This list will be used with logical_core_list in order to track last online-made CPU core. This operations are performed in order to track CPU usage per core continuously even if CPU cores made online/offline.
        self.number_of_logical_cores = len(self.logical_core_list_system_ordered)             # "logical_core_list" list contains online CPU core numbers and ordering changes when online/offline CPU core changes are made. Last online-made core is listed as the last core.
        logical_core_list_prev = self.logical_core_list[:]                                    # Get copy of the list. Otherwise, lists will be linked.
        for i, cpu_core in enumerate(self.logical_core_list_system_ordered):                  # Track the changes if CPU core is made online/offline
            if cpu_core not in self.logical_core_list:                                        # Add new core number into logical_core_list if CPU core is made online. Also CPU time data related to online-made the core is appended into lists.
                self.logical_core_list.append(cpu_core)
                cpu_time = proc_stat_lines[i].split()
                self.cpu_time_all_prev.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))
                self.cpu_time_load_prev.append(self.cpu_time_all_prev[-1] - int(cpu_time[4]) - int(cpu_time[5]))
                self.cpu_usage_percent_per_core.append([0] * self.chart_data_history)
        for cpu_core in self.logical_core_list[:]:                                            # Remove core number from logical_core_list if it is made offline. Also CPU time data related to offline-made the core is removed from lists.
            if cpu_core not in self.logical_core_list_system_ordered:
                cpu_core_index_to_remove = self.logical_core_list.index(cpu_core)
                del self.cpu_time_all_prev[cpu_core_index_to_remove]
                del self.cpu_time_load_prev[cpu_core_index_to_remove]
                del self.cpu_usage_percent_per_core[cpu_core_index_to_remove]
                self.logical_core_list.remove(cpu_core)
        if logical_core_list_prev != self.logical_core_list:
            self.performance_set_selected_cpu_core_func()
        # Get cpu_usage_percent_per_core, cpu_usage_percent_ave
        cpu_time_all = []
        cpu_time_load = []
        for i, cpu_core in enumerate(self.logical_core_list):                                 # Get CPU core times calculate CPU usage values and append usage values into lists in the core number order listed in logical_core_list.
            cpu_time = proc_stat_lines[self.logical_core_list_system_ordered.index(cpu_core)].split()
            cpu_time_all.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))    # All time since boot for the cpu core
            cpu_time_load.append(cpu_time_all[-1] - int(cpu_time[4]) - int(cpu_time[5]))      # Time elapsed during core processing for the core
            if cpu_time_all[-1] - self.cpu_time_all_prev[i] == 0:
                cpu_time_all[-1] = cpu_time_all[-1] + 1                                       # Append 1 CPU time (a negligible value) in order to avoid zeor division error in the first loop after application start or in the first loop of newly online-made CPU core. It is corrected in the next loop.
            self.cpu_usage_percent_per_core[i].append((cpu_time_load[-1] - self.cpu_time_load_prev[i]) / (cpu_time_all[-1] - self.cpu_time_all_prev[i]) * 100)
            del self.cpu_usage_percent_per_core[i][0]
        cpu_usage_average = []
        for cpu_usage_per_core in self.cpu_usage_percent_per_core:
            cpu_usage_average.append(cpu_usage_per_core[-1])
        self.cpu_usage_percent_ave.append(sum(cpu_usage_average) / self.number_of_logical_cores)    # Calculate average CPU usage for all logical cores (summation of CPU usage per core / number of logical cores)
        del self.cpu_usage_percent_ave[0]                                                     # Delete the first CPU usage percent value from the list in order to keep list lenght same. Because a new value is appended in every loop. This list is used for CPU usage percent graphic.        
        self.cpu_time_all_prev = list(cpu_time_all)                                           # Use the values as "previous" data. This data will be used in the next loop for calculating time difference.
        self.cpu_time_load_prev = list(cpu_time_load)

        # Get ram_usage_percent
        with open("/proc/meminfo") as reader:
            memory_info = reader.read()
        self.ram_total = int(memory_info.split("MemTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.ram_free = int(memory_info.split("\nMemFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.ram_available = int(memory_info.split("\nMemAvailable:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.ram_used = self.ram_total - self.ram_available
        self.ram_usage_percent.append(self.ram_used / self.ram_total * 100)
        del self.ram_usage_percent[0]
        # Get swap_usage_percent
        self.swap_total = int(memory_info.split("\nSwapTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.swap_free = int(memory_info.split("\nSwapFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        # Calculate values if swap memory exists.
        if self.swap_free != 0:
            self.swap_used = self.swap_total - self.swap_free
            self.swap_usage_percent.append(self.swap_used / self.swap_total * 100)
        # Set values as "0" if swap memory does not exist.
        else:
            self.swap_used = 0
            self.swap_usage_percent.append(0)
        del self.swap_usage_percent[0]

        # Get disk_list
        self.disk_list_system_ordered = []
        proc_diskstats_lines_filtered = []
        with open("/proc/partitions") as reader:
            proc_partitions_lines = reader.read().strip().split("\n")[2:]
        for line in proc_partitions_lines:
            self.disk_list_system_ordered.append(line.split()[3].strip())
        with open("/proc/diskstats") as reader:
            proc_diskstats_lines = reader.read().strip().split("\n")
        for line in proc_diskstats_lines:
            if line.split()[2] in self.disk_list_system_ordered:
                # Disk information of some disks (such a loop devices) exist in "/proc/diskstats" file even if these devices are unmounted. "proc_diskstats_lines_filtered" list is used in order to use disk list without these remaining information.
                proc_diskstats_lines_filtered.append(line)
        disk_list_prev = self.disk_list[:]
        for i, disk in enumerate(self.disk_list_system_ordered):
            if disk not in self.disk_list:
                self.disk_list.append(disk)
                disk_data = proc_diskstats_lines[i].split()
                disk_read_data = int(disk_data[5]) * self.disk_sector_size
                disk_write_data = int(disk_data[9]) * self.disk_sector_size
                self.disk_read_data_prev.append(disk_read_data)
                self.disk_write_data_prev.append(disk_write_data)
                self.disk_read_speed.append([0] * self.chart_data_history)
                self.disk_write_speed.append([0] * self.chart_data_history)
        for disk in reversed(self.disk_list[:]):
            if disk not in self.disk_list_system_ordered:
                disk_index_to_remove = self.disk_list.index(disk)
                del self.disk_read_data_prev[disk_index_to_remove]
                del self.disk_write_data_prev[disk_index_to_remove]
                del self.disk_read_speed[disk_index_to_remove]
                del self.disk_write_speed[disk_index_to_remove]
                self.disk_list.remove(disk)
        if disk_list_prev != self.disk_list:
            self.performance_set_selected_disk_func()
        # Get disk_read_speed, disk_write_speed
        self.disk_read_data = []
        self.disk_write_data = []
        for i, disk in enumerate(self.disk_list):
            disk_data = proc_diskstats_lines_filtered[self.disk_list_system_ordered.index(disk)].split()
            self.disk_read_data.append(int(disk_data[5]) * self.disk_sector_size)
            self.disk_write_data.append(int(disk_data[9]) * self.disk_sector_size)
            self.disk_read_speed[i].append((self.disk_read_data[-1] - self.disk_read_data_prev[i]) / update_interval)
            self.disk_write_speed[i].append((self.disk_write_data[-1] - self.disk_write_data_prev[i]) / update_interval)
            del self.disk_read_speed[i][0]
            del self.disk_write_speed[i][0]
        self.disk_read_data_prev = list(self.disk_read_data)
        self.disk_write_data_prev = list(self.disk_write_data)

        # Get network card list
        self.network_card_list_system_ordered = []
        with open("/proc/net/dev") as reader:
            proc_net_dev_lines = reader.read().strip().split("\n")[2:]
        for line in proc_net_dev_lines:
            self.network_card_list_system_ordered.append(line.split(":", 1)[0].strip())
        network_card_list_prev = self.network_card_list[:]
        for i, network_card in enumerate(self.network_card_list_system_ordered):
            if network_card not in self.network_card_list:
                self.network_card_list.append(network_card)
                network_data = proc_net_dev_lines[i].split()
                self.network_receive_bytes = int(network_data[1])
                self.network_send_bytes = int(network_data[9])
                self.network_receive_bytes_prev.append(self.network_receive_bytes)
                self.network_send_bytes_prev.append(self.network_send_bytes)
                self.network_receive_speed.append([0] * self.chart_data_history)
                self.network_send_speed.append([0] * self.chart_data_history)
        for network_card in reversed(self.network_card_list[:]):
            if network_card not in self.network_card_list_system_ordered:
                network_card_index_to_remove = self.network_card_list.index(network_card)
                del self.network_receive_bytes_prev[network_card_index_to_remove]
                del self.network_send_bytes_prev[network_card_index_to_remove]
                del self.network_receive_speed[network_card_index_to_remove]
                del self.network_send_speed[network_card_index_to_remove]
                self.network_card_list.remove(network_card)
        if network_card_list_prev != self.network_card_list:
            self.performance_set_selected_network_card_func()
        # Get network_receive_speed, network_send_speed
        self.network_receive_bytes = []
        self.network_send_bytes = []
        for i, network_card in enumerate(self.network_card_list):
            network_data = proc_net_dev_lines[self.network_card_list_system_ordered.index(network_card)].split()
            self.network_receive_bytes.append(int(network_data[1]))
            self.network_send_bytes.append(int(network_data[9]))
            self.network_receive_speed[i].append((self.network_receive_bytes[-1] - self.network_receive_bytes_prev[i]) / update_interval)
            self.network_send_speed[i].append((self.network_send_bytes[-1] - self.network_send_bytes_prev[i]) / update_interval)
            del self.network_receive_speed[i][0]
            del self.network_send_speed[i][0]
        self.network_receive_bytes_prev = list(self.network_receive_bytes)
        self.network_send_bytes_prev = list(self.network_send_bytes)


    # ----------------------- Called for getting device vendor and model information -----------------------
    def performance_get_device_vendor_model_func(self, modalias_output):

        # Define "udev" hardware database file directory.
        udev_hardware_database_dir = "/usr/lib/udev/hwdb.d/"
        # Some older Linux distributions use "/lib/" instead of "/usr/lib/" but they are merged under "/usr/lib/" in newer versions.
        if os.path.isdir(udev_hardware_database_dir) == False:
            udev_hardware_database_dir = "/lib/udev/hwdb.d/"

        # Example modalias file contents for testing.
        # modalias_output = "usb:v0B95p1790d0100dcFFdscFFdp00icFFiscFFip00in00"
        # modalias_output = "virtio:d00000001v00001AF4"
        # modalias_output = "sdio:c00v02D0d4324"
        # modalias_output = "pci:v000010DEd00000DF4sv00001043sd00001642bc03sc00i00"
        # modalias_output = "pci:v0000168Cd0000002Bsv00001A3Bsd00002C37bc02sc80i00"
        # modalias_output = "pci:v000010ECd00008168sv00001043sd000016D5bc02sc00i00"
        # modalias_output = "pci:v00008086d00000116sv00001043sd00001642bc03sc00i00"
        # modalias_output = "pci:v00001B85d00006018sv00001B85sd00006018bc01sc08i02"
        # modalias_output = "pci:v0000144Dd0000A808sv0000144Dsd0000A801bc01sc08i02"
        # modalias_output = "of:NgpuT<NULL>Cnvidia,tegra210-gm20bCnvidia,gm20b"
        # modalias_output = "of:NgpuT(null)Cbrcm,bcm2835-vc4"
        # modalias_output = "scsi:t-0x05"
        # modalias_output = "scsi:t-0x00"

        # Determine device subtype.
        device_subtype, device_alias = modalias_output.split(":", 1)

        # Get device vendor, model if device subtype is PCI.
        if device_subtype == "pci":

            # Example pci device modalias: "pci:v000010DEd00000DF4sv00001043sd00001642bc03sc00i00".

            # Get device IDs from modalias file content.
            first_index = device_alias.find("v")
            last_index = first_index + 8 + 1
            device_vendor_id = device_alias[first_index:last_index]
            first_index = device_alias.find("d")
            last_index = first_index + 8 + 1
            device_model_id = device_alias[first_index:last_index]

            # Get search texts by using device IDs.
            search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file for PCI devices.
            with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb") as reader:
                ids_file_output = reader.read()

            # Get device vendor, model names from device ID file content.
            if search_text1 in ids_file_output:
                rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
                device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
                if search_text2 in ids_file_output:
                    device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
                else:
                    device_model_name = "Unknown"
            else:
                device_vendor_name = "Unknown"
                device_model_name = "Unknown"

        # Get device vendor, model if device subtype is virtio.
        elif device_subtype == "virtio":

            # Example virtio device modalias: "virtio:d00000001v00001AF4".

            # Get device IDs from modalias file content.
            first_index = device_alias.find("v")
            last_index = first_index + 8 + 1
            device_vendor_id = device_alias[first_index:last_index]
            first_index = device_alias.find("d")
            last_index = first_index + 8 + 1
            device_model_id = device_alias[first_index:last_index]
            # 1040 is added to device ID of virtio devices. For details: https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01.html
            device_model_id = "d0000" + str(int(device_model_id.strip("d")) + 1040)

            # Get search texts by using device IDs.
            search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file for VIRTIO devices.
            with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb") as reader:
                ids_file_output = reader.read()

            # Get device vendor, model names from device ID file content.
            if search_text1 in ids_file_output:
                rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
                device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
                if search_text2 in ids_file_output:
                    device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
                else:
                    device_model_name = "Unknown"
            else:
                device_vendor_name = "Unknown"
                device_model_name = "Unknown"

        # Get device vendor, model if device subtype is USB.
        elif device_subtype == "usb":

            # Example usb device modalias: "usb:v0B95p1790d0100dcFFdscFFdp00icFFiscFFip00in00".

            # Get device IDs from modalias file content.
            first_index = device_alias.find("v")
            last_index = first_index + 4 + 1
            device_vendor_id = device_alias[first_index:last_index]
            first_index = device_alias.find("p")
            last_index = first_index + 4 + 1
            device_model_id = device_alias[first_index:last_index]

            # Get search texts by using device IDs.
            search_text1 = "usb:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "usb:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file for USB devices.
            with open(udev_hardware_database_dir + "20-usb-vendor-model.hwdb") as reader:
                ids_file_output = reader.read()

            # Get device vendor, model names from device ID file content.
            if search_text1 in ids_file_output:
                rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
                device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
                if search_text2 in ids_file_output:
                    device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
                else:
                    device_model_name = "Unknown"
            else:
                device_vendor_name = "Unknown"
                device_model_name = "Unknown"

        # Get device vendor, model if device subtype is SDIO.
        elif device_subtype == "sdio":

            # Example sdio device modalias: "sdio:c00v02D0d4324".

            # Get device IDs from modalias file content.
            first_index = device_alias.find("v")
            last_index = first_index + 4 + 1
            device_vendor_id = device_alias[first_index:last_index]
            first_index = device_alias.find("d")
            last_index = first_index + 4 + 1
            device_model_id = device_alias[first_index:last_index]

            # Get search texts by using device IDs.
            search_text1 = "sdio:" + "c*" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "sdio:" + "c*" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file for SDIO devices.
            with open(udev_hardware_database_dir + "20-sdio-vendor-model.hwdb") as reader:
                ids_file_output = reader.read()

            # Get device vendor, model names from device ID file content.
            if search_text1 in ids_file_output:
                rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
                device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
                if search_text2 in ids_file_output:
                    device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
                else:
                    device_model_name = "Unknown"
            else:
                device_vendor_name = "Unknown"
                device_model_name = "Unknown"

        # Get device vendor, model if device subtype is of.
        elif device_subtype == "of":

            # Example sdio device modalias (NVIDIA Tegra GPU on N.Switch device: "of:NgpuT<NULL>Cnvidia,tegra210-gm20bCnvidia,gm20b".

            device_vendor_name = device_vendor_id = device_alias.split("C", 1)[-1].split("C", 1)[0].split(",")[0].title()
            device_model_name = device_model_id = device_alias.split("C", 1)[-1].split("C", 1)[0].split(",")[1].title()

        # Get device vendor, model if device subtype is SCSI or IDE.
        elif device_subtype in ["scsi", "ide"]:

            # Example SCSI device modalias: "scsi:t-0x00".

            device_vendor_name = device_vendor_id = "[scsi_or_ide_disk]"
            device_model_name = device_model_id = "[scsi_or_ide_disk]"

        # Set device vendor, model if device subtype is not known so far.
        else:
            device_vendor_name = device_vendor_id = "Unknown"
            device_model_name = device_model_id = "Unknown"

        return device_vendor_name, device_model_name, device_vendor_id, device_model_id



    # ----------------------- Called for drawing performance summary data -----------------------
    def performance_summary_chart_draw_func(self, widget, ctx):

        # Get chart colors of performance tab sub-tab charts.
        chart_line_color_cpu_percent = Config.chart_line_color_cpu_percent
        chart_line_color_memory_percent = Config.chart_line_color_memory_percent
        chart_line_color_disk_speed_usage = Config.chart_line_color_disk_speed_usage
        chart_line_color_network_speed_data = Config.chart_line_color_network_speed_data

        # Get performance data and set text format.
        performance_cpu_usage_percent_precision = 0
        cpu_usage_text = f'{self.cpu_usage_percent_ave[-1]:.{performance_cpu_usage_percent_precision}f}'
        performance_memory_data_precision = 0
        ram_usage_text = f'{self.ram_usage_percent[-1]:.{performance_memory_data_precision}f}'
        processes_number_text = f'{len([filename for filename in os.listdir("/proc/") if filename.isdigit()])}'
        swap_usage_text = f'{self.swap_usage_percent[-1]:.0f}%'
        selected_disk_number = self.selected_disk_number
        performance_disk_data_precision = 1
        performance_disk_data_unit = Config.performance_disk_data_unit
        performance_disk_speed_bit = Config.performance_disk_speed_bit
        disk_read_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, self.disk_read_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s'
        disk_write_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, self.disk_write_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s'
        selected_network_card_number = self.selected_network_card_number
        performance_network_data_precision = 1
        performance_network_data_unit = Config.performance_network_data_unit
        performance_network_speed_bit = Config.performance_network_speed_bit
        network_download_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, self.network_receive_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s'
        network_upload_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, self.network_send_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s'


        # Set antialiasing level as "BEST" in order to avoid low quality chart line because of the highlight effect (more than one line will be overlayed for this appearance).
        ctx.set_antialias(cairo.Antialias.BEST)

        # Set line joining style as "LINE_JOIN_ROUND" in order to avoid spikes at the line joints due to high antialiasing level.
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # Define pi number
        pi_number = 3.14159

        # Get drawingarea size.
        chart_width = Gtk.Widget.get_allocated_width(widget)
        chart_height = Gtk.Widget.get_allocated_height(widget)

        # Get biggest outer frame size. Aspect ratio of this frame is fixed in order to avoid changing aspect ratio of the drawn objects when window size is changed.
        if chart_width > chart_height * 1.384:
            frame_width = chart_height * 1.384
            frame_height = chart_height
        else:
            frame_width = chart_width
            frame_height = chart_width / 1.384


        # Define dimensions, locations, etc. to use them for scalable graphics.
        gauge_outer_radius = frame_height * 0.43
        gauge_circular_center_x = chart_width / 2 - gauge_outer_radius * 0.48
        gauge_inner_radius = gauge_outer_radius * 0.57
        background_upper_lower_band_height = chart_height * 0.1
        background_upper_lower_band_vertex = chart_height * 0.15
        background_upper_lower_band_vertex_width = gauge_outer_radius * 2.26
        shadow_radius = gauge_outer_radius * 0.8
        shadow_center_loc_y = frame_height * 0.485
        gauge_indicator_line_major_thickness = gauge_outer_radius * 0.02
        gauge_indicator_line_minor_thickness = gauge_outer_radius * 0.01
        gauge_indicator_line_major_length = gauge_outer_radius * 0.04
        gauge_indicator_line_minor_length = gauge_outer_radius * 0.026
        gauge_indicator_line_major_move = gauge_outer_radius * 0.053
        gauge_indicator_line_minor_move = gauge_outer_radius * 0.063
        gauge_indicator_text_radius = gauge_outer_radius * 0.73
        gauge_indicator_text_correction = gauge_outer_radius * 0.047
        gauge_indicator_text_move = gauge_outer_radius * 0.027
        gauge_indicator_text_size = gauge_outer_radius * 0.091
        gauge_indicator_text_size_smaller = gauge_indicator_text_size * 0.78
        gauge_cpu_ram_label_text_move = gauge_outer_radius * 0.266
        gauge_cpu_ram_label_text_margin = gauge_outer_radius * 0.07
        gauge_cpu_ram_usage_text_size = gauge_outer_radius * 0.25
        gauge_cpu_ram_usage_text_shadow_move = gauge_outer_radius * 0.014
        gauge_cpu_ram_usage_text_move = gauge_outer_radius * 0.026
        gauge_percentage_label_text_below_cpu_ram_move = gauge_outer_radius * 0.074
        gauge_percentage_label_text_below_cpu_ram_size = gauge_outer_radius * 0.08
        gauge_processes_swap_label_text_size = gauge_indicator_text_size * 0.88
        gauge_processes_swap_label_text_move = gauge_outer_radius * 0.22
        gauge_processes_swap_usage_text_size = gauge_cpu_ram_usage_text_size * 0.45
        gauge_processes_swap_usage_text_move = gauge_outer_radius * 0.34
        gauge_processes_swap_usage_text_shadow_move = gauge_cpu_ram_usage_text_shadow_move * 0.5
        gauge_separator_line_vertical_center_length = gauge_outer_radius * 0.94
        gauge_separator_line_vertical_upper_start = gauge_outer_radius * 0.83
        gauge_separator_line_vertical_upper_length = gauge_outer_radius * 0.23
        gauge_separator_line_vertical_lower_start = gauge_outer_radius * 0.6
        gauge_separator_line_vertical_lower_length = gauge_outer_radius * 0.23
        gauge_right_outer_radius = gauge_outer_radius * 1.05
        gauge_right_move = gauge_outer_radius * 0.938
        gauge_right_upper_lower_edge_thickness = gauge_outer_radius * 0.07
        gauge_right_upper_lower_edge_move_horizontal = gauge_right_outer_radius * 0.027
        gauge_separator_line_horizontal_start = gauge_outer_radius * 0.23
        gauge_separator_line_horizontal_length = gauge_outer_radius * 0.6
        gauge_disk_network_label_text_size = gauge_indicator_text_size * 0.88
        gauge_disk_read_speed_label_text_move_x = gauge_outer_radius * 0.09
        gauge_disk_read_speed_label_text_move_y = gauge_outer_radius * 0.5
        gauge_disk_write_speed_label_text_move_x = gauge_outer_radius * 0.21
        gauge_disk_write_speed_label_text_move_y = gauge_outer_radius * 0.2
        gauge_network_download_speed_label_text_move_x = gauge_outer_radius * 0.21
        gauge_network_download_speed_label_text_move_y = gauge_outer_radius * 0.15
        gauge_network_upload_speed_label_text_move_x = gauge_outer_radius * 0.09
        gauge_network_upload_speed_label_text_move_y = gauge_outer_radius * 0.43
        gauge_disk_network_usage_text_size = gauge_cpu_ram_usage_text_size * 0.4
        gauge_disk_network_usage_text_shadow_move = gauge_outer_radius * 0.009
        gauge_disk_network_usage_text_move_y = gauge_outer_radius * 0.11


        # Save current (default) transformations (translation, rotation, scale, color, line thickness, etc.) to restore back.
        ctx.save()

        # Draw and fill chart background.
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.set_source_rgba(44/255, 60/255, 73/255, 1.0)
        ctx.fill()


        # Draw background upper band.
        ctx.move_to(0, 0)
        ctx.rel_line_to(0, (chart_height - frame_height) / 2)
        ctx.rel_line_to(0, background_upper_lower_band_height)
        ctx.rel_line_to((chart_width - frame_width) / 2, 0)
        ctx.rel_line_to(background_upper_lower_band_vertex_width / 2, background_upper_lower_band_vertex - background_upper_lower_band_height)
        ctx.rel_line_to(background_upper_lower_band_vertex_width / 2, -(background_upper_lower_band_vertex - background_upper_lower_band_height))
        ctx.rel_line_to(frame_width - background_upper_lower_band_vertex_width, 0)
        ctx.rel_line_to((chart_width - frame_width) / 2, 0)
        ctx.rel_line_to(0, -background_upper_lower_band_height)
        ctx.rel_line_to(0, -(chart_height - frame_height) / 2)
        ctx.rel_line_to(-chart_width, 0)
        ctx.close_path()
        background_upper_lower_band_path = ctx.copy_path()
        gradient_pattern = cairo.LinearGradient(0, (chart_height - frame_height) / 2 + background_upper_lower_band_height * 0.66, 0, (chart_height - frame_height) / 2 + background_upper_lower_band_vertex)
        gradient_pattern.add_color_stop_rgba(0, 80/255, 107/255, 137/255, 1)
        gradient_pattern.add_color_stop_rgba(0.10, 85/255, 117/255, 147/255, 1)
        gradient_pattern.add_color_stop_rgba(0.55, 110/255, 187/255, 197/255, 1)
        gradient_pattern.add_color_stop_rgba(0.70, 149/255, 236/255, 251/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 179/255, 236/255, 240/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()

        # Flip (scale), rotate and translate the copied background upper band and draw background lower band.
        ctx.scale(-1, 1)
        ctx.translate(0, chart_height)
        ctx.rotate(180*pi_number/180)
        ctx.append_path(background_upper_lower_band_path)
        ctx.set_source(gradient_pattern)
        ctx.fill()

        # Restore current (default) transformations (translation, rotation, scale, etc.)
        ctx.restore()


        # Translate, rotate and scale coordinate system and draw shadow of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, (chart_height / 2) + shadow_center_loc_y)
        ctx.scale(1, 0.25)
        ctx.arc(0, 0, shadow_radius, 2*pi_number*0.5, 0)
        gradient_pattern = cairo.LinearGradient(0, -shadow_radius/2, 0, 0)
        gradient_pattern.add_color_stop_rgba(0, 50/255, 50/255, 50/255, 0.55)
        gradient_pattern.add_color_stop_rgba(1, 50/255, 50/255, 50/255, 0)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        # Restore default transformations.
        ctx.restore()


        # Draw rectangle part of the background of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90+40)*pi_number/180
        ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
        angle1 = (90-40)*pi_number/180
        ctx.line_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -2*gauge_right_outer_radius*cos(angle1))
        ctx.set_source_rgba(34/255, 52/255, 71/255, 1)
        ctx.fill()
        ctx.restore()


        # Draw circular (partial) part of the background and edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = -40*pi_number/180
        end_angle = 40*pi_number/180

        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        # Draw upper edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90+40)*pi_number/180
        # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
        ctx.move_to(gauge_right_outer_radius*sin(angle1)-gauge_right_upper_lower_edge_move_horizontal, gauge_right_outer_radius*cos(angle1))
        ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)+gauge_right_outer_radius, 0, gauge_right_outer_radius*cos(angle1))
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw lower edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90-40)*pi_number/180
        # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
        ctx.move_to(gauge_right_outer_radius*sin(angle1)-gauge_right_upper_lower_edge_move_horizontal, gauge_right_outer_radius*cos(angle1))
        ctx.rel_move_to(0, -gauge_right_outer_radius*0.07)
        ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)-gauge_right_outer_radius, 0, gauge_right_outer_radius*cos(angle1))
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw fillet on the connection point of the upper right corner of the right gauge for continuous gauge edge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = -90*pi_number/180
        end_angle = -55*pi_number/180
        angle1 = (90-40)*pi_number/180
        ctx.translate(gauge_right_outer_radius*sin(angle1), -gauge_right_outer_radius*cos(angle1))
        ctx.translate(-gauge_right_outer_radius*0.03, gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius*0.07)
        scale_value = 1-0.93
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba((0.93 - 0.93) / scale_value, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba((0.94 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.95 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba((0.98 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.99 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius*0.07, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        # Draw fillet on the connection point of the lower right corner of the right gauge for continuous gauge edge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = 55*pi_number/180
        end_angle = 90*pi_number/180
        angle1 = (90+40)*pi_number/180
        ctx.translate(gauge_right_outer_radius*sin(angle1), -gauge_right_outer_radius*cos(angle1))
        ctx.translate(-gauge_right_outer_radius*0.03, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius*0.07)
        scale_value = 1-0.93
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba((0.93 - 0.93) / scale_value, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba((0.94 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.95 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba((0.98 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.99 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius*0.07, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)

        # Draw white reflection on upper right area of the circular edge of the right gauge.
        for i in range(2):
            start_angle = (305+15)*pi_number/180
            end_angle = (305+25+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_right_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_right_outer_radius*0.992, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_right_outer_radius*0.992, 0, 0, gauge_right_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection on upper area of the upper edge of the right gauge.
        for i in range(2):
            angle1 = (90+40)*pi_number/180
            # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
            ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
            ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
            ctx.rel_line_to(-gauge_right_outer_radius, 0)
            ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
            gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)*0.98, 0, gauge_right_outer_radius*cos(angle1))
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection on lower area of the lower edge of the right gauge.
        for i in range(2):
            angle1 = (90-40)*pi_number/180
            # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
            ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
            ctx.rel_move_to(0, -gauge_right_outer_radius*0.07)
            ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
            ctx.rel_line_to(-gauge_right_outer_radius, 0)
            ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
            gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)*0.98, 0, gauge_right_outer_radius*cos(angle1))
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        ctx.restore()


        # Draw shadow on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + 0, chart_height / 2)
        start_angle = -40*pi_number/180
        end_angle = 40*pi_number/180

        gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius, 0, 0, gauge_right_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 0/255, 0/255, 0/255, 0)
        gradient_pattern.add_color_stop_rgba(0, 0/255, 0/255, 0/255, 0.5)
        gradient_pattern.add_color_stop_rgba(1, 0/255, 0/255, 0/255, 0)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius, start_angle, end_angle)
        ctx.rel_line_to(-gauge_right_outer_radius, -gauge_outer_radius*0.067)
        ctx.rel_line_to(0, -gauge_right_outer_radius-gauge_outer_radius*0.333)
        ctx.fill()
        ctx.restore()


        # Draw horizontal separator line on the center of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        ctx.move_to(gauge_separator_line_horizontal_start, 0)
        ctx.rel_line_to(gauge_separator_line_horizontal_length, 0)
        ctx.set_line_width(1.5)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()
        ctx.restore()


        # Draw circular (partial) line on the left of the disk read/write labels on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        start_angle = -31*pi_number/180
        end_angle = -4*pi_number/180

        ctx.set_line_width(1.5)
        ctx.set_source_rgba(chart_line_color_disk_speed_usage[0], chart_line_color_disk_speed_usage[1], chart_line_color_disk_speed_usage[2], chart_line_color_disk_speed_usage[3])
        ctx.arc(0, 0, gauge_outer_radius * 1.07, start_angle, end_angle)
        ctx.stroke()
        ctx.restore()


        # Draw circular (partial) line on the left of the network download/upload labels on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        start_angle = 4*pi_number/180
        end_angle = 31*pi_number/180

        ctx.set_line_width(1.5)
        ctx.set_source_rgba(chart_line_color_network_speed_data[0], chart_line_color_network_speed_data[1], chart_line_color_network_speed_data[2], chart_line_color_network_speed_data[3])
        ctx.arc(0, 0, gauge_outer_radius * 1.07, start_angle, end_angle)
        ctx.stroke()
        ctx.restore()


        # Draw background and outer circle of the circular gauge.
        ctx.arc(gauge_circular_center_x, chart_height / 2, gauge_outer_radius, 0, 2*pi_number)
        gradient_pattern = cairo.RadialGradient(gauge_circular_center_x, chart_height / 2, 0, gauge_circular_center_x, chart_height / 2, gauge_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.86, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.88, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.90, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.96, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()


        # Draw background and inner circle of the circular gauge.
        ctx.arc(gauge_circular_center_x, chart_height / 2, gauge_inner_radius, 0, 2*pi_number)
        gradient_pattern = cairo.RadialGradient(gauge_circular_center_x, chart_height / 2, 0, gauge_circular_center_x, chart_height / 2, gauge_inner_radius)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.96, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()


        # Rotate the coordinate system and draw reflection on the background of the inner circle.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.rotate(-45*pi_number/180)
        ctx.arc(0, 0, gauge_inner_radius*0.94, 0, 2*pi_number)
        gradient_pattern = cairo.LinearGradient(0, -gauge_inner_radius*0.94/2, 0, gauge_inner_radius*0.94/2)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.5, 72/255, 88/255, 107/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 32/255, 41/255, 49/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Save translations.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)

        # Draw white reflection (on 180 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (180-40-i)*pi_number/180
            end_angle = (180+40+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 305 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (305-20-i)*pi_number/180
            end_angle = (305+20+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 45 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (45-20-i)*pi_number/180
            end_angle = (45+20+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 270 degree) on the inner circle of the circular gauge.
        for i in range(3):
            start_angle = (270-35-i)*pi_number/180
            end_angle = (270+35+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_inner_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_inner_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius*0.98, 0, 0, gauge_inner_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 90 degree) on the inner circle of the circular gauge.
        for i in range(3):
            start_angle = (90-25-i)*pi_number/180
            end_angle = (90+25+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_inner_radius*0.96, end_angle, start_angle)
            ctx.arc(0, 0, gauge_inner_radius*0.94, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius*0.94, 0, 0, gauge_inner_radius*0.96)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Restore translations.
        ctx.restore()


        # Draw percentage indicator lines on the left side.
        for i, angle in enumerate([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
            ctx.save()
            ctx.translate(gauge_circular_center_x, chart_height / 2)
            ctx.rotate(((i*15)+15)*pi_number/180)

            if angle % 20 == 0:
                ctx.rectangle(-gauge_indicator_line_major_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_major_move, gauge_indicator_line_major_thickness, gauge_indicator_line_major_length)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            else:
                ctx.rectangle(-gauge_indicator_line_minor_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_minor_move, gauge_indicator_line_minor_thickness, gauge_indicator_line_minor_length)
                ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
            ctx.fill()

            ctx.restore()

            # Draw percentage numbers on the left side if angle value is power of 20 ("gauge_indicator_text_correction" is a correction number for aligning the texts).
            if angle % 20 == 0:
                ctx.save()
                ctx.translate((gauge_circular_center_x)-gauge_indicator_text_correction, (chart_height / 2)+gauge_indicator_text_correction)
                angle1 = -((i*15)+15)*pi_number/180
                ctx.move_to((gauge_indicator_text_radius-gauge_indicator_text_move)*sin(angle1), (gauge_indicator_text_radius-gauge_indicator_text_move)*cos(angle1))
                ctx.set_font_size(gauge_indicator_text_size)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                ctx.show_text(f'{angle}')
                ctx.restore()

        # Draw percentage indicator lines on the right side.
        for i, angle in enumerate([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
            ctx.save()
            ctx.translate(gauge_circular_center_x, chart_height / 2)
            ctx.rotate(-((i*15)+15)*pi_number/180)

            if angle % 20 == 0:
                ctx.rectangle(-gauge_indicator_line_major_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_major_move, gauge_indicator_line_major_thickness, gauge_indicator_line_major_length)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            else:
                ctx.rectangle(-gauge_indicator_line_minor_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_minor_move, gauge_indicator_line_minor_thickness, gauge_indicator_line_minor_length)
                ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
            ctx.fill()

            ctx.restore()

            # Draw percentage numbers on the right side if angle value is power of 20 ("gauge_indicator_text_correction" is a correction number for aligning the texts).
            if angle % 20 == 0:
                ctx.save()
                ctx.translate((gauge_circular_center_x)-gauge_indicator_text_correction, (chart_height / 2)+gauge_indicator_text_correction)
                angle1 = ((i*15)+15)*pi_number/180
                ctx.move_to((gauge_indicator_text_radius-gauge_indicator_text_move)*sin(angle1), (gauge_indicator_text_radius-gauge_indicator_text_move)*cos(angle1))
                ctx.set_font_size(gauge_indicator_text_size)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                ctx.show_text(f'{angle}')
                ctx.restore()


        # Draw vertical separator line on the center of the inner circle of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.move_to(0, -gauge_separator_line_vertical_center_length / 2)
        ctx.rel_line_to(0, gauge_separator_line_vertical_center_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()

        # Draw vertical separator line on the center of the outer circle of the circular gauge (upper side).
        ctx.move_to(0, -gauge_separator_line_vertical_upper_start)
        ctx.rel_line_to(0, gauge_separator_line_vertical_upper_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()

        # Draw vertical separator line on the center of the outer circle of the circular gauge (lower side).
        ctx.move_to(0, gauge_separator_line_vertical_lower_start)
        ctx.rel_line_to(0, gauge_separator_line_vertical_lower_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()


        # Draw "CPU" label on the upper-left side of the inner circle of the circular gauge.
        cpu_text = _tr("CPU")
        ctx.set_font_size(gauge_indicator_text_size)
        text_extends = ctx.text_extents(cpu_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(cpu_text)

        # Draw "RAM" label on the upper-right side of the inner circle of the circular gauge.
        ram_text = _tr("RAM")
        ctx.set_font_size(gauge_indicator_text_size)
        text_extends = ctx.text_extents(ram_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(ram_text)

        # Draw "Processes" label on the lower-left side of the inner circle of the circular gauge.
        processes_text = _tr("Processes")
        ctx.set_font_size(gauge_processes_swap_label_text_size)
        if len(processes_text) > 9:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        text_extends = ctx.text_extents(processes_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(processes_text)

        # Draw "Swap" label on the upper-right side of the inner circle of the circular gauge.
        ram_text = _tr("Swap")
        ctx.set_font_size(gauge_processes_swap_label_text_size)
        if len(ram_text) > 9:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        text_extends = ctx.text_extents(ram_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(ram_text)


        # Draw "%" labels below the CPU and RAM percentages on the inner circle of the circular gauge.
        percentage_text = "%"
        ctx.set_font_size(gauge_percentage_label_text_below_cpu_ram_size)
        text_extends = ctx.text_extents(percentage_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_percentage_label_text_below_cpu_ram_move)
        ctx.set_source_rgba(180/255, 180/255, 180/255, 1.0)
        ctx.show_text(percentage_text)
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_percentage_label_text_below_cpu_ram_move)
        ctx.set_source_rgba(180/255, 180/255, 180/255, 1.0)
        ctx.show_text(percentage_text)


        # Draw lowest layer of the shadow of the CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        text_extends = ctx.text_extents(cpu_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move + 2 * gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(cpu_usage_text)

        # Draw shadow of the CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move + gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(cpu_usage_text)

        # Draw CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(cpu_usage_text)

        # Draw lowest layer of the shadow of the RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        text_extends = ctx.text_extents(ram_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move + 2 * gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(ram_usage_text)

        # Draw shadow of the RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move + gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(ram_usage_text)

        # Draw RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(ram_usage_text)

        # Draw lowest layer of the shadow of the Processes label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        text_extends = ctx.text_extents(processes_number_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move + 2 * gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(processes_number_text)

        # Draw shadow of the Processes label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move + gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(processes_number_text)

        # Draw Processes label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(processes_number_text)

        # Draw lowest layer of the shadow of the Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        text_extends = ctx.text_extents(swap_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move + 2 * gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(swap_usage_text)

        # Draw shadow of the Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move + gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(swap_usage_text)

        # Draw Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(swap_usage_text)

        # Reset translating.
        ctx.restore()
        ctx.move_to(0, 0)
        ctx.stroke()


        # Draw CPU usage indicator.
        cpu_usage_angle = self.cpu_usage_percent_ave[-1] / 10
        start_angle = ((0*15)+105)*pi_number/180
        end_angle = ((cpu_usage_angle*15)+105)*pi_number/180

        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.arc_negative(0, 0, gauge_outer_radius*0.86, end_angle, start_angle)
        ctx.arc(0, 0, gauge_inner_radius, start_angle, end_angle)
        gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius, 0, 0, gauge_outer_radius*0.86)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 0)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 0.5)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 1)
        gradient_pattern.add_color_stop_rgba(1, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw RAM usage indicator.
        ram_usage_angle = self.ram_usage_percent[-1] / 10
        end_angle = (75-(0*15))*pi_number/180
        start_angle = (75-(ram_usage_angle*15))*pi_number/180

        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.arc_negative(0, 0, gauge_outer_radius*0.86, end_angle, start_angle)
        ctx.arc(0, 0, gauge_inner_radius, start_angle, end_angle)
        gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius, 0, 0, gauge_outer_radius*0.86)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 0)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 0.5)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 1)
        gradient_pattern.add_color_stop_rgba(1, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw "Read Speed" label on the upper-left side of the inner circle of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        read_speed_text = _tr("Read Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(read_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(read_speed_text)

        # Draw "Write Speed" label on the upper-left side of the inner circle of the circular gauge.
        write_speed_text = _tr("Write Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(write_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(write_speed_text)

        # Draw "Download Speed" label on the upper-left side of the inner circle of the circular gauge.
        download_speed_text = _tr("Download Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(download_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(download_speed_text)

        # Draw "Upload Speed" label on the upper-left side of the inner circle of the circular gauge.
        upload_speed_text = _tr("Upload Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(upload_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(upload_speed_text)


        # Draw lowest layer of the shadow of the Disk Read Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(disk_read_speed_text)

        # Draw shadow of the Disk Read Speed label on the right gauge.
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_read_speed_text)

        # Draw Disk Read Speed label on the right gauge.
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_read_speed_text)

        # Draw lowest layer of the shadow of the Disk Write Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(disk_write_speed_text)

        # Draw shadow of the Disk Write Speed label on the right gauge.
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_write_speed_text)

        # Draw Disk Write Speed label on the right gauge.
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_write_speed_text)

        # Draw lowest layer of the shadow of the Network Download Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(network_download_speed_text)

        # Draw shadow of the Network Download Speed label on the right gauge.
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_download_speed_text)

        # Draw Network Download Speed label on the right gauge.
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_download_speed_text)

        # Draw lowest layer of the shadow of the Network Upload Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(network_upload_speed_text)

        # Draw shadow of the Network Upload Speed label on the right gauge.
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_upload_speed_text)

        # Draw Network Upload Speed label on the right gauge.
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_upload_speed_text)

        ctx.restore()


    # ----------------------- Called for drawing performance data as line chart -----------------------
    def performance_line_charts_draw_func(self, widget, ctx):

        # Get widget ID in order to detect GUI module (CPU, Memory, etc. tabs, process detail window, etc.) for drawing details.
        widget_id = Gtk.Buildable.get_name(widget)

        # Check if drawing will be for CPU tab.
        if widget_id == "drawingarea1101":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            if Config.show_cpu_usage_per_core == 0:
                draw_per_device = 0
                performance_data1 = [self.cpu_usage_percent_ave]
                device_name_list = [""]
                selected_device_number = None
            else:
                draw_per_device = 1
                performance_data1 = self.cpu_usage_percent_per_core
                device_name_list = self.logical_core_list_system_ordered
                selected_device_number = self.selected_cpu_core_number

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_list = []
            for device_name in device_name_list:
                chart_y_limit_list.append(100)

        # Check if drawing will be for Memory tab.
        elif widget_id == "drawingarea1201":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            if Config.show_memory_usage_per_memory == 0:
                draw_per_device = 0
                performance_data1 = [self.ram_usage_percent]
                device_name_list = [""]
                selected_device_number = None
            else:
                draw_per_device = 1
                performance_data1 = [self.ram_usage_percent, self.swap_usage_percent]
                device_name_list = [_tr("RAM"), _tr("Swap Memory")]
                selected_device_number = None

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_list = []
            for device_name in device_name_list:
                chart_y_limit_list.append(100)

        # Check if drawing will be for Disk tab.
        elif widget_id == "drawingarea1301":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            if Config.show_disk_usage_per_disk == 0:
                draw_per_device = 0
                performance_data1 = [self.disk_read_speed[self.selected_disk_number]]
                performance_data2 = [self.disk_write_speed[self.selected_disk_number]]
                device_name_list = [""]
                selected_device_number = None
            else:
                draw_per_device = 1
                performance_data1 = list(self.disk_read_speed)
                performance_data2 = list(self.disk_write_speed)
                device_name_list = list(self.disk_list_system_ordered)
                # Remove the device from the list if "hide_loop_ramdisk_zram_disks" option is enabled.
                if Config.hide_loop_ramdisk_zram_disks == 1:
                    for device in self.disk_list_system_ordered:
                        if device.startswith("loop") == True or device.startswith("ram") == True or device.startswith("zram") == True:
                            device_index = device_name_list.index(device)
                            del device_name_list[device_index]
                            del performance_data1[device_index]
                            del performance_data2[device_index]
                # "selected_device_number" for Disk tab is get in a different way. Because device list may be changed if "hide_loop_ramdisk_zram_disks" option is enabled.
                selected_device_number = device_name_list.index(self.disk_list_system_ordered[self.selected_disk_number])

            # Get which performance data will be drawn.
            if Config.plot_disk_read_speed == 1:
                draw_performance_data1 = 1
            else:
                draw_performance_data1 = 0

            if Config.plot_disk_write_speed == 1:
                draw_performance_data2 = 1
            else:
                draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_list = []
            for i, device_name in enumerate(device_name_list):
                chart_y_limit = 1.1 * ((max(max(performance_data1[i]), max(performance_data2[i]))) + 0.0000001)
                if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                    chart_y_limit = 1.1 * (max(performance_data1[i]) + 0.0000001)
                if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                    chart_y_limit = 1.1 * (max(performance_data2[i]) + 0.0000001)
                chart_y_limit_list.append(chart_y_limit)

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            from Disk import Disk
            performance_disk_data_precision = Config.performance_disk_data_precision
            performance_disk_data_unit = Config.performance_disk_data_unit
            performance_disk_speed_bit = Config.performance_disk_speed_bit
            # Get biggest chart_y_limit value in the chart_y_limit_list to show it on a label if all performance data is drawn for all devices.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit = chart_y_limit_list[selected_device_number]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(chart_y_limit_list)
            try:
                chart_y_limit_str = f'{Disk.performance_data_unit_converter_func("speed", performance_disk_speed_bit, chart_y_limit, performance_disk_data_unit, performance_disk_data_precision)}/s'
            # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
            except AttributeError:
                return
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            Disk.label1313.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_list if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit_list[selected_device_number] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update chart_y_limit_list if single chart (device) is drawn.
            else:
                chart_y_limit_list[chart_y_limit_list.index(chart_y_limit)] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for Network tab.
        elif widget_id == "drawingarea1401":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_network_speed_data

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            if Config.show_network_usage_per_network_card == 0:
                draw_per_device = 0
                performance_data1 = [self.network_receive_speed[self.selected_network_card_number]]
                performance_data2 = [self.network_send_speed[self.selected_network_card_number]]
                device_name_list = [""]
                selected_device_number = None
            else:
                draw_per_device = 1
                performance_data1 = self.network_receive_speed
                performance_data2 = self.network_send_speed
                device_name_list = self.network_card_list_system_ordered
                selected_device_number = self.selected_network_card_number

            # Get which performance data will be drawn.
            if Config.plot_network_download_speed == 1:
                draw_performance_data1 = 1
            else:
                draw_performance_data1 = 0

            if Config.plot_network_upload_speed == 1:
                draw_performance_data2 = 1
            else:
                draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_list = []
            for i, device_name in enumerate(device_name_list):
                chart_y_limit = 1.1 * ((max(max(performance_data1[i]), max(performance_data2[i]))) + 0.0000001)
                if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                    chart_y_limit = 1.1 * (max(performance_data1[i]) + 0.0000001)
                if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                    chart_y_limit = 1.1 * (max(performance_data2[i]) + 0.0000001)
                chart_y_limit_list.append(chart_y_limit)

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            from Network import Network
            performance_network_data_precision = Config.performance_network_data_precision
            performance_network_data_unit = Config.performance_network_data_unit
            performance_network_speed_bit = Config.performance_network_speed_bit
            # Get biggest chart_y_limit value in the chart_y_limit_list to show it on a label if all performance data is drawn for all devices.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit = chart_y_limit_list[selected_device_number]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(chart_y_limit_list)
            try:
                chart_y_limit_str = f'{Network.performance_data_unit_converter_func("speed", performance_network_speed_bit, chart_y_limit, performance_network_data_unit, performance_network_data_precision)}/s'
            # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
            except AttributeError:
                return
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            Network.label1413.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_list if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit_list[selected_device_number] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update chart_y_limit_list if single chart (device) is drawn.
            else:
                chart_y_limit_list[chart_y_limit_list.index(chart_y_limit)] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for GPU tab.
        elif widget_id == "drawingarea1501":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_fps

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            draw_per_device = 0
            from Gpu import Gpu
            try:
                performance_data1 = [Gpu.gpu_load_list]
            # Handle errors because chart signals are connected before running relevant performance thread (in the GPU module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            except AttributeError:
                return
            device_name_list = [""]
            selected_device_number = None

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_list = []
            for device_name in device_name_list:
                chart_y_limit_list.append(100)

        # Check if drawing will be for Process Details window CPU tab.
        elif widget_id == "drawingarea2101w":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            draw_per_device = 0
            from ProcessesDetails import ProcessesDetails
            if ProcessesDetails.drawingarea2101w == widget:
                pass
            performance_data1 = [ProcessesDetails.process_cpu_usage_list]
            device_name_list = [""]
            selected_device_number = None

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_list = []
            for device_name in device_name_list:
                chart_y_limit_list.append(100)

        # Check if drawing will be for Process Details window Memory tab.
        elif widget_id == "drawingarea2102w":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            draw_per_device = 0
            from ProcessesDetails import ProcessesDetails
            if ProcessesDetails.drawingarea2101w == widget:
                pass
            performance_data1 = [ProcessesDetails.process_ram_usage_list]
            device_name_list = [""]
            selected_device_number = None

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            """# Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_list = []
            for device_name in device_name_list:
                chart_y_limit_list.append(100)"""

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_list = []
            for i, device_name in enumerate(device_name_list):
                #chart_y_limit = 1.1 * ((max(max(performance_data1[i]), max(performance_data2[i]))) + 0.0000001)
                #if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                chart_y_limit = 1.1 * (max(performance_data1[i]) + 0.0000001)
                #if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                #    chart_y_limit = 1.1 * (max(performance_data2[i]) + 0.0000001)
                chart_y_limit_list.append(chart_y_limit)

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            #from Disk import Disk
            processes_memory_data_precision = Config.processes_memory_data_precision
            processes_memory_data_unit = Config.processes_memory_data_unit
            # Get biggest chart_y_limit value in the chart_y_limit_list to show it on a label if all performance data is drawn for all devices.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit = chart_y_limit_list[selected_device_number]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(chart_y_limit_list)
            try:
                chart_y_limit_str = f'{ProcessesDetails.performance_data_unit_converter_func("data", "none", chart_y_limit, processes_memory_data_unit, processes_memory_data_precision)}'
            # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
            except AttributeError:
                return
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            ProcessesDetails.label2139w.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_list if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit_list[selected_device_number] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update chart_y_limit_list if single chart (device) is drawn.
            else:
                chart_y_limit_list[chart_y_limit_list.index(chart_y_limit)] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for Process Details window Disk tab.
        elif widget_id == "drawingarea2103w":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Get if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices, get performance data to be drawn and device list.
            draw_per_device = 0
            from ProcessesDetails import ProcessesDetails
            if ProcessesDetails.drawingarea2101w == widget:
                pass
            performance_data1 = [ProcessesDetails.process_disk_read_speed_list]
            performance_data2 = [ProcessesDetails.process_disk_write_speed_list]
            device_name_list = [""]
            selected_device_number = None

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 1

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_list = []
            for i, device_name in enumerate(device_name_list):
                chart_y_limit = 1.1 * ((max(max(performance_data1[i]), max(performance_data2[i]))) + 0.0000001)
                if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                    chart_y_limit = 1.1 * (max(performance_data1[i]) + 0.0000001)
                if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                    chart_y_limit = 1.1 * (max(performance_data2[i]) + 0.0000001)
                chart_y_limit_list.append(chart_y_limit)

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            #from Disk import Disk
            processes_disk_data_precision = Config.processes_disk_data_precision
            processes_disk_data_unit = Config.processes_disk_data_unit
            processes_disk_speed_bit = Config.processes_disk_speed_bit
            # Get biggest chart_y_limit value in the chart_y_limit_list to show it on a label if all performance data is drawn for all devices.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit = chart_y_limit_list[selected_device_number]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(chart_y_limit_list)
            try:
                chart_y_limit_str = f'{ProcessesDetails.performance_data_unit_converter_func("speed", processes_disk_speed_bit, chart_y_limit, processes_disk_data_unit, processes_disk_data_precision)}/s'
            # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
            except AttributeError:
                return
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            ProcessesDetails.label2140w.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_list if multiple charts (devices) are drawn.
            if selected_device_number != None:
                chart_y_limit_list[selected_device_number] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update chart_y_limit_list if single chart (device) is drawn.
            else:
                chart_y_limit_list[chart_y_limit_list.index(chart_y_limit)] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)


        # Start drawing the performance data.
        # Get chart data history.
        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        # Get chart background color.
        chart_background_color = [0.0, 0.0, 0.0, 0.0]

        # Get drawingarea size.
        chart_width = Gtk.Widget.get_allocated_width(widget)
        chart_height = Gtk.Widget.get_allocated_height(widget)

        # Get number of charts.
        number_of_charts = len(device_name_list)

        # Get number of horizontal and vertical charts (per-device).
        for i in range(1, 1000):
            if number_of_charts % i == 0:
                number_of_horizontal_charts = i
                number_of_vertical_charts = number_of_charts // i
                if number_of_horizontal_charts >= number_of_vertical_charts:
                    if number_of_horizontal_charts > 2 * number_of_vertical_charts:
                        number_of_horizontal_charts = number_of_vertical_charts = ceil(sqrt(number_of_charts))
                    break

        # Get chart index list for horizontal and vertical charts. This data will be used for tiling charts.
        chart_index_list = []
        for i in range(number_of_vertical_charts):
            for j in range(number_of_horizontal_charts):
                chart_index_list.append([j, i])

        # Correction for some number of charts (devices) to avoid using empty last chart row.
        if len(chart_index_list) - number_of_horizontal_charts > number_of_charts:
            number_of_vertical_charts = number_of_vertical_charts - 1
            chart_index_list = chart_index_list[:-number_of_horizontal_charts]

        # Set chart border spacing value.
        if number_of_charts == 1:
            chart_spacing = 0
        else:
            chart_spacing = 6
        chart_spacing_half = chart_spacing / 2

        # Get chart width and height per-device.
        chart_width_per_device = chart_width / number_of_horizontal_charts
        chart_height_per_device = chart_height / number_of_vertical_charts

        # Get chart width and height per-device.
        chart_width_per_device_wo_borders = (chart_width / number_of_horizontal_charts) - chart_spacing
        chart_height_per_device_wo_borders = (chart_height / number_of_vertical_charts) - chart_spacing

        # Set antialiasing level as "BEST" in order to avoid low quality chart line because of the highlight effect (more than one line will be overlayed for this appearance).
        ctx.set_antialias(cairo.Antialias.BEST)

        # Set line joining style as "LINE_JOIN_ROUND" in order to avoid spikes at the line joints due to high antialiasing level.
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # Performance data line paths will be used for highlighting the line.
        performance_data1_line_path_list = []
        performance_data2_line_path_list = []

        # Draw charts per-device.
        for j, device_name in enumerate(device_name_list):

            # Draw and fill chart background.
            ctx.rectangle((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half, (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half, chart_width_per_device, chart_height_per_device)
            ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
            ctx.fill()

            # Draw horizontal and vertical gridlines.
            for i in range(3):
                ctx.move_to((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half, (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half + chart_height_per_device/4*(i+1))
                ctx.rel_line_to(chart_width_per_device-chart_spacing, 0)
            for i in range(4):
                ctx.move_to(chart_width_per_device/5*(i+1), 0)
                ctx.move_to((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half + chart_width_per_device/5*(i+1), (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half)
                ctx.rel_line_to(0, chart_height_per_device-chart_spacing)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
            ctx.set_line_width(1)
            ctx.stroke()

            # Draw outer border of the chart.
            ctx.rectangle((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half, (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half, chart_width_per_device-chart_spacing, chart_height_per_device-chart_spacing)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            # Draw outer border of the selected device by using thicker line if all devices are plotted.
            if selected_device_number == j:
                ctx.set_line_width(2)
                ctx.stroke()
            else:
                ctx.set_line_width(1)
                ctx.stroke()
            # Set the line thickness as 1 again in oder to avoid using thick line for the next drawings.
            ctx.set_line_width(1)

            if draw_performance_data1 == 1:

                performance_data1_current = performance_data1[j]

                # Draw performance data.
                ctx.move_to((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half, chart_height_per_device+(chart_height_per_device*chart_index_list[j][1])-chart_spacing_half)
                ctx.rel_move_to(0, -chart_height_per_device_wo_borders*performance_data1_current[0]/chart_y_limit_list[j])
                for i in range(chart_data_history - 1):
                    delta_x = (chart_width_per_device_wo_borders*chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width_per_device_wo_borders*chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height_per_device_wo_borders*performance_data1_current[i+1]/chart_y_limit_list[j]) - (chart_height_per_device_wo_borders*performance_data1_current[i]/chart_y_limit_list[j])
                    ctx.rel_line_to(delta_x, -delta_y)
                ctx.stroke_preserve()

                # Set line color (full transparent in order to prevent drawing bolder lines due to overlapping), close the drawn line to fill inside area of it and copy the performance line path to use it for highlighting.
                ctx.rel_line_to(0, chart_height_per_device_wo_borders*performance_data1_current[-1]/chart_y_limit_list[j])
                ctx.rel_line_to(-(chart_width_per_device_wo_borders), 0)
                ctx.close_path()
                performance_data1_line_path_list.append(ctx.copy_path())
                ctx.set_source_rgba(0, 0, 0, 0)
                ctx.stroke()

                # Use previously copied performance line path and fill the closed area (area below the performance data line).
                ctx.append_path(performance_data1_line_path_list[-1])  
                gradient_pattern = cairo.LinearGradient(0, (chart_height_per_device*chart_index_list[j][1])-chart_spacing_half, 0, (chart_height_per_device*chart_index_list[j][1])-chart_spacing_half+chart_height_per_device_wo_borders)
                gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
                gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
                ctx.set_source(gradient_pattern)
                ctx.fill()

            if draw_performance_data2 == 1:

                performance_data2_current = performance_data2[j]

                # Set color and line dash style for this performance data line.
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.set_dash([5, 3])

                # Draw performance data.
                ctx.move_to((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half, chart_height_per_device+(chart_height_per_device*chart_index_list[j][1])-chart_spacing_half)
                ctx.rel_move_to(0, -chart_height_per_device_wo_borders*performance_data2_current[0]/chart_y_limit_list[j])
                for i in range(chart_data_history - 1):
                    delta_x = (chart_width_per_device_wo_borders*chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width_per_device_wo_borders*chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height_per_device_wo_borders*performance_data2_current[i+1]/chart_y_limit_list[j]) - (chart_height_per_device_wo_borders*performance_data2_current[i]/chart_y_limit_list[j])
                    ctx.rel_line_to(delta_x, -delta_y)
                ctx.stroke_preserve()

                # Set line color (full transparent in order to prevent drawing bolder lines due to overlapping), close the drawn line to fill inside area of it and copy the performance line path to use it for highlighting.
                ctx.rel_line_to(0, chart_height_per_device_wo_borders*performance_data2_current[-1]/chart_y_limit_list[j])
                ctx.rel_line_to(-(chart_width_per_device_wo_borders), 0)
                ctx.close_path()
                performance_data2_line_path_list.append(ctx.copy_path())
                ctx.set_source_rgba(0, 0, 0, 0)
                ctx.stroke()

                # Set line style as solid line.
                ctx.set_dash([])

            # Draw core number per chart.
            ctx.move_to((chart_width_per_device*chart_index_list[j][0])+chart_spacing_half+3, (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half+12)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            ctx.show_text(f'{device_name}')


        # Check if chart line will be highlighted.
        if self.chart_line_highlight == 1:

            # Define local variables for maouse position for lower CPU usage.
            try:
                mouse_position_x = self.mouse_position_x
                mouse_position_y = self.mouse_position_y
            # It gives error at the beginning of the mouse move on the chart.
            except AttributeError:
                return

            # Get the chart which mouse cursor in moved on.
            chart_number_to_highlight = -1
            for j in range(number_of_charts):
                if mouse_position_x > (chart_width_per_device*chart_index_list[j][0])+chart_spacing_half and mouse_position_x < (chart_width_per_device*chart_index_list[j][0])+chart_spacing_half+chart_width_per_device_wo_borders:
                    if mouse_position_y > (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half and mouse_position_y < (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half+chart_height_per_device_wo_borders:
                        chart_number_to_highlight = j
                        break

            # Prevent errors if mouse cursor on the empty area (chart spacing) between charts (if multiple charts are drawn).
            if chart_number_to_highlight == -1:
                return

            # Use previously copied performance line path(s).
            if draw_performance_data1 == 1:
                ctx.append_path(performance_data1_line_path_list[chart_number_to_highlight])

                # Set line features and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.stroke_preserve()

                # Set line features (white and semi-transparent color in order to overlay with the previous line and generate highlight effect) and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(1, 1, 1, 0.3)
                ctx.stroke()

            if draw_performance_data2 == 1:
                ctx.append_path(performance_data2_line_path_list[chart_number_to_highlight])

                # Set line style as solid line for this performance data line.
                ctx.set_dash([5, 3])

                # Set line features and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.stroke_preserve()

                # Set line features (white and semi-transparent color in order to overlay with the previous line and generate highlight effect) and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(1, 1, 1, 0.3)
                ctx.stroke()

                # Set line style as solid line.
                ctx.set_dash([])


            # Highlight chart point(s).
            # Calculate the length between chart data points.
            data_point_width = chart_width_per_device_wo_borders / (chart_data_history - 1)

            # Calculate number of data points from start (left) to the mouse cursor position and fraction after the last (first data point before the mouse cursor) data point.
            total_length_of_left_charts = (chart_width_per_device*chart_index_list[chart_number_to_highlight][0])+chart_spacing_half
            total_length_of_upper_charts = (chart_height_per_device*chart_index_list[chart_number_to_highlight][1])+chart_spacing_half
            mouse_position_x_current_chart = mouse_position_x-total_length_of_left_charts
            data_point_count_until_mouse_cursor = mouse_position_x_current_chart / data_point_width
            data_point_count_int = int(data_point_count_until_mouse_cursor)
            fraction = data_point_count_until_mouse_cursor - data_point_count_int

            # Determine the data point to be highlighted when mouse cursor is between two data points.
            if fraction > 0.5:
                chart_point_highlight = data_point_count_int + 1
            # if fraction <= 0.5:
            else:
                chart_point_highlight = data_point_count_int

            # Get location of the point(s) to be highlighted.
            loc_x = total_length_of_left_charts + chart_width_per_device_wo_borders * chart_x_axis[chart_point_highlight]/(chart_data_history-1)
            loc_y_list =[]
            if draw_performance_data1 == 1:
                loc_y1 = total_length_of_upper_charts + chart_height_per_device_wo_borders - (chart_height_per_device_wo_borders*performance_data1[chart_number_to_highlight][chart_point_highlight]/chart_y_limit_list[chart_number_to_highlight])
                loc_y_list.append(loc_y1)
            if draw_performance_data2 == 1:
                loc_y2 = total_length_of_upper_charts + chart_height_per_device_wo_borders - (chart_height_per_device_wo_borders*performance_data2[chart_number_to_highlight][chart_point_highlight]/chart_y_limit_list[chart_number_to_highlight])
                loc_y_list.append(loc_y2)

            # Draw a big point and fill it.
            # Set color for the point to be highlighted.
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            for loc_y in loc_y_list:
                ctx.arc(loc_x, loc_y, 5, 0, 2*3.14)
                ctx.fill()

            # Set font size and text for showing performance data of the highlighted point and get its location data in order to use it for showing a centered box under the text.
            ctx.set_font_size(13)
            performance_data_at_point_text_list =[]
            if draw_performance_data1 == 1:
                if widget_id == "drawingarea1101":
                    performance_data1_at_point_text = f'{performance_data1[chart_number_to_highlight][chart_point_highlight]:.{Config.performance_cpu_usage_percent_precision}f} %'
                elif widget_id == "drawingarea1201":
                    performance_data1_at_point_text = f'{performance_data1[chart_number_to_highlight][chart_point_highlight]:.{Config.performance_memory_data_precision}f} %'
                elif widget_id == "drawingarea1301":
                    performance_data1_at_point_text = f'{Disk.performance_data_unit_converter_func("speed", performance_disk_speed_bit, performance_data1[chart_number_to_highlight][chart_point_highlight], performance_disk_data_unit, performance_disk_data_precision)}/s'
                elif widget_id == "drawingarea1401":
                    performance_data1_at_point_text = f'{Network.performance_data_unit_converter_func("speed", performance_network_speed_bit, performance_data1[chart_number_to_highlight][chart_point_highlight], performance_network_data_unit, performance_network_data_precision)}/s'
                elif widget_id == "drawingarea1501":
                    performance_data1_at_point_text = f'{performance_data1[chart_number_to_highlight][chart_point_highlight]:.0f} %'
                elif widget_id == "drawingarea2101w":
                    performance_data1_at_point_text = f'{performance_data1[chart_number_to_highlight][chart_point_highlight]:.{Config.processes_cpu_precision}f} %'
                elif widget_id == "drawingarea2102w":
                    performance_data1_at_point_text = f'{ProcessesDetails.performance_data_unit_converter_func("data", "none", performance_data1[chart_number_to_highlight][chart_point_highlight], processes_memory_data_unit, processes_memory_data_precision)}'
                elif widget_id == "drawingarea2103w":
                    performance_data1_at_point_text = f'{ProcessesDetails.performance_data_unit_converter_func("speed", processes_disk_speed_bit, performance_data1[chart_number_to_highlight][chart_point_highlight], processes_disk_data_unit, processes_disk_data_precision)}/s'
                # Add "-" before the text if there are 2 performance data lines.
                if len(loc_y_list) == 2:
                    performance_data1_at_point_text = f'-  {performance_data1_at_point_text}'
                performance_data_at_point_text_list.append(performance_data1_at_point_text)

            if draw_performance_data2 == 1:
                if widget_id == "drawingarea1101":
                    performance_data2_at_point_text = f'- -{performance_data2[chart_number_to_highlight][chart_point_highlight]:.{Config.performance_cpu_usage_percent_precision}f} %'
                elif widget_id == "drawingarea1201":
                    performance_data2_at_point_text = f'- -{performance_data2[chart_number_to_highlight][chart_point_highlight]:.{Config.performance_memory_swap_data_precision}f} %'
                elif widget_id == "drawingarea1301":
                    performance_data2_at_point_text = f'- -{Disk.performance_data_unit_converter_func("speed", performance_disk_speed_bit, performance_data2[chart_number_to_highlight][chart_point_highlight], performance_disk_data_unit, performance_disk_data_precision)}/s'
                elif widget_id == "drawingarea1401":
                    performance_data2_at_point_text = f'- -{Network.performance_data_unit_converter_func("speed", performance_network_speed_bit, performance_data2[chart_number_to_highlight][chart_point_highlight], performance_network_data_unit, performance_network_data_precision)}/s'
                elif widget_id == "drawingarea1501":
                    performance_data2_at_point_text = f'- -{performance_data2[chart_number_to_highlight][chart_point_highlight]:.0f} %'
                elif widget_id == "drawingarea2103w":
                    performance_data2_at_point_text = f'- -{ProcessesDetails.performance_data_unit_converter_func("speed", processes_disk_speed_bit, performance_data2[chart_number_to_highlight][chart_point_highlight], processes_disk_data_unit, processes_disk_data_precision)}/s'
                performance_data_at_point_text_list.append(performance_data2_at_point_text)

            performance_data_at_point_text = '  |  '.join(performance_data_at_point_text_list)

            text_extends = ctx.text_extents(performance_data_at_point_text)
            text_start_x = text_extends.width / 2
            text_start_y = text_extends.height / 2
            text_border_margin = 10
            origin_for_text =  (chart_height_per_device*chart_index_list[j][1])+chart_spacing_half + chart_height_per_device_wo_borders*0.35

            # Calculate correction value for x location of the text, box under the text and line between box and highligthed data point(s) in order to prevent them going out of the visible area (drawingara) when mouse is close to beginning/end of the drawingarea.
            box_under_text_location_correction = 0
            box_under_text_start = loc_x-text_start_x-text_border_margin
            box_under_text_end = loc_x+text_start_x+text_border_margin
            if box_under_text_start < 0 + chart_spacing_half:
                box_under_text_location_correction = -1 * box_under_text_start + chart_spacing_half
            if box_under_text_end > chart_width - chart_spacing_half:
                box_under_text_location_correction = chart_width - chart_spacing_half - box_under_text_end

            # Set grey color for the box under the text and draw the box.
            ctx.rectangle(box_under_text_start+box_under_text_location_correction,origin_for_text-text_start_y-text_border_margin, text_extends.width+2*text_border_margin, text_extends.height+2*text_border_margin)
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
            ctx.fill()

            # Set color for the text and show the text.
            ctx.move_to(loc_x-text_start_x+box_under_text_location_correction,origin_for_text+text_start_y)
            ctx.set_line_width(1)
            ctx.set_source_rgba(1.0, 1.0, 1.0, 0.7)
            ctx.show_text(performance_data_at_point_text)

            # Draw a line between the highlighted point and the box under the text.
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
            for loc_y in loc_y_list:
                ctx.move_to(loc_x, loc_y-5)
                ctx.line_to(box_under_text_start+box_under_text_location_correction, origin_for_text+text_start_y+15)
                ctx.rel_line_to(text_extends.width+2*text_border_margin, 0)
                ctx.stroke()


    # ----------------------- Highlight performance chart line if mouse is moved onto the drawingarea -----------------------
    def performance_line_charts_enter_notify_event_func(self, widget, event):

        self.chart_line_highlight = 1
        widget.queue_draw()


    # ----------------------- Revert highlighted performance chart line if mouse is moved out of the drawingarea -----------------------
    def performance_line_charts_leave_notify_event_func(self, widget, event):

        self.chart_line_highlight = 0
        widget.queue_draw()


    # ----------------------- Highlight performance chart point and show performance data text if mouse is moved on the drawingarea -----------------------
    def performance_line_charts_motion_notify_event_func(self, widget, event):

        # Get mouse position on the x coordinate on the drawingarea.
        self.mouse_position_x = event.x
        self.mouse_position_y = event.y

        # Update the chart in order to show visual changes.
        widget.queue_draw()


    # ----------------------- Called for drawing performance data as bar chart -----------------------
    def performance_bar_charts_draw_func(self, widget, ctx):

        # Check if drawing will be for Memory tab.
        performance_tab_current_sub_tab = Config.performance_tab_current_sub_tab
        if performance_tab_current_sub_tab == 2:

            # Get performance data to be drawn.
            from Memory import Memory
            try:
                performance_data1 = Memory.swap_usage_percent[-1]
            # "swap_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
            except AttributeError:
                return

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Check if drawing will be for Disk tab.
        if performance_tab_current_sub_tab == 3:

            # Get performance data to be drawn.
            from Disk import Disk
            try:
                performance_data1 = Disk.disk_usage_percent
            # "disk_usage_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
            except AttributeError:
                return

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100

        # Check if widget is the drawingarea on the headerbar for CPU usage and overwrite previous values (values which get during tab checks).
        from PerformanceSummaryHeaderbar import PerformanceSummaryHeaderbar
        if widget == PerformanceSummaryHeaderbar.drawingarea101:

            # Get performance data to be drawn.
            performance_data1 = self.cpu_usage_percent_ave[-1]

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100

        # Check if widget is the drawingarea on the headerbar for RAM usage and overwrite previous values (values which get during tab checks).
        if widget == PerformanceSummaryHeaderbar.drawingarea102:

            # Get performance data to be drawn.
            performance_data1 = self.ram_usage_percent[-1]

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Get chart background color.
        chart_background_color = [0.0, 0.0, 0.0, 0.0]

        # Get drawingarea size.
        chart_width = Gtk.Widget.get_allocated_width(widget)
        chart_height = Gtk.Widget.get_allocated_height(widget)

        # Draw and fill chart background.
        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.fill()

        # Draw outer border of the chart.
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.6 * chart_line_color[3])
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.stroke()

        # Draw performance data.
        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3])
        ctx.rectangle(0, 0, chart_width*performance_data1/chart_y_limit, chart_height)
        ctx.fill()


    # ----------------------- Called for defining values for converting data units and setting value precision (called from several modules) -----------------------
    def performance_define_data_unit_converter_variables_func(self):

        #       ISO UNITs (as powers of 1000)        -             IEC UNITs (as powers of 1024)
        # Unit Name    Abbreviation     bytes        -       Unit Name    Abbreviation    bytes   
        # byte         B                1            -       byte         B               1
        # kilobyte     KB               1000         -       kibibyte     KiB             1024
        # megabyte     MB               1000^2       -       mebibyte     MiB             1024^2
        # gigabyte     GB               1000^3       -       gibibyte     GiB             1024^3
        # terabyte     TB               1000^4       -       tebibyte     TiB             1024^4
        # petabyte     PB               1000^5       -       pebibyte     PiB             1024^5

        # Unit Name    Abbreviation     bits         -       Unit Name    Abbreviation    bits    
        # bit          b                1            -       bit          b               1
        # kilobit      Kb               1000         -       kibibit      Kib             1024
        # megabit      Mb               1000^2       -       mebibit      Mib             1024^2
        # gigabit      Gb               1000^3       -       gibibit      Gib             1024^3
        # terabit      Tb               1000^4       -       tebibit      Tib             1024^4
        # petabit      Pb               1000^5       -       pebibit      Pib             1024^5

        # 1 byte = 8 bits

        self.data_unit_list = [[0, "B", "B", "b", "b"], [1, "KiB", "KB", "Kib", "Kb"], [2, "MiB", "MB", "Mib", "Mb"],
                              [3, "GiB", "GB", "Gib", "Gb"], [4, "TiB", "TB", "Tib", "Tb"], [5, "PiB", "PB", "Pib", "Pb"]]

        # Data unit options: 0: Bytes (ISO), 1: Bytes (IEC), 2: bits (ISO), 3: bits (IEC).


    # ----------------------- Called for converting data units and setting value precision (called from several modules) -----------------------
    def performance_data_unit_converter_func(self, data_type, data_type_option, data, unit, precision):

        data_unit_list = self.data_unit_list
        if isinstance(data, str) == True:
            return data

        if unit == 0:
            power_of_value = 1024
            unit_text_index = 1

        if unit == 1:
            power_of_value = 1000
            unit_text_index = 2

        if data_type == "speed":
            if data_type_option == 1:
                data = data * 8
                unit_text_index = unit_text_index + 2

        unit_counter = 0
        while data >= power_of_value:
            unit_counter = unit_counter + 1
            data = data/power_of_value
        unit = data_unit_list[unit_counter][unit_text_index]

        if data == 0:
            precision = 0

        return f'{data:.{precision}f} {unit}'


# Generate object
Performance = Performance()

