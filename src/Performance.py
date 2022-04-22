#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os
import cairo

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

        # Define initial values for RAM usage percent
        self.ram_usage_percent = [0] * self.chart_data_history

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


    # ----------------------------------- Performance - Background Function (gets basic CPU, RAM, disk and network usage data in the background in order to assure uninterrupted data for charts) -----------------------------------
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
                # Disk information of some disks (such a loop devices) exist in "/proc/diskstats" file even if these dvice are unmounted. "proc_diskstats_lines_filtered" list is used in order to use disk list without these remaining information.
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
        disk_read_data = []
        disk_write_data = []
        for i, disk in enumerate(self.disk_list):
            disk_data = proc_diskstats_lines_filtered[self.disk_list_system_ordered.index(disk)].split()
            disk_read_data.append(int(disk_data[5]) * self.disk_sector_size)
            disk_write_data.append(int(disk_data[9]) * self.disk_sector_size)
            self.disk_read_speed[i].append((disk_read_data[-1] - self.disk_read_data_prev[i]) / update_interval)
            self.disk_write_speed[i].append((disk_write_data[-1] - self.disk_write_data_prev[i]) / update_interval)
            del self.disk_read_speed[i][0]
            del self.disk_write_speed[i][0]
        self.disk_read_data_prev = list(disk_read_data)
        self.disk_write_data_prev = list(disk_write_data)

        # Get network card list
        network_card_list_system_ordered = []
        with open("/proc/net/dev") as reader:
            proc_net_dev_lines = reader.read().strip().split("\n")[2:]
        for line in proc_net_dev_lines:
            network_card_list_system_ordered.append(line.split(":", 1)[0].strip())
        network_card_list_prev = self.network_card_list[:]
        for i, network_card in enumerate(network_card_list_system_ordered):
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
            if network_card not in network_card_list_system_ordered:
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
            network_data = proc_net_dev_lines[network_card_list_system_ordered.index(network_card)].split()
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


    # ----------------------- Called for drawing performance data as line chart -----------------------
    def performance_line_charts_draw_func(self, widget, ctx):

        # Check if drawing will be for CPU tab.
        performance_tab_current_sub_tab = Config.performance_tab_current_sub_tab
        if performance_tab_current_sub_tab == 0:

            # Get performance data to be drawn.
            performance_data1 = self.cpu_usage_percent_ave

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Check if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices.
            if Config.show_cpu_usage_per_core == 0:
                draw_per_device = 0
            else:
                draw_per_device = 1

            # Check which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Check if drawing will be for RAM tab.
        elif performance_tab_current_sub_tab == 1:

            # Get performance data to be drawn.
            performance_data1 = self.ram_usage_percent

            # Get chart colors.
            chart_line_color = Config.chart_line_color_ram_swap_percent

            # Check if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices.
            draw_per_device = 0

            # Check which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100

        # Check if drawing will be for Disk tab.
        elif performance_tab_current_sub_tab == 2:

            # Get performance data to be drawn.
            performance_data1 = self.disk_read_speed[self.selected_disk_number]
            performance_data2 = self.disk_write_speed[self.selected_disk_number]

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Check if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices.
            draw_per_device = 0

            # Check which performance data will be drawn.
            if Config.plot_disk_read_speed == 1:
                draw_performance_data1 = 1
            else:
                draw_performance_data1 = 0

            if Config.plot_disk_write_speed == 1:
                draw_performance_data2 = 1
            else:
                draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit = 1.1 * ((max(max(performance_data1), max(performance_data2))) + 0.0000001)
            if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                chart_y_limit = 1.1 * (max(performance_data1) + 0.0000001)
            if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                chart_y_limit = 1.1 * (max(performance_data2) + 0.0000001)

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            from Disk import Disk
            data_unit_for_chart_y_limit = 0
            if Config.performance_disk_speed_data_unit >= 8:
                data_unit_for_chart_y_limit = 8
            try:
                chart_y_limit_str = f'{Disk.performance_data_unit_converter_func(chart_y_limit, data_unit_for_chart_y_limit, 0)}/s'
            # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
            except AttributeError:
                return
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_split[0])))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            Disk.label1313.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            chart_y_limit = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for Network tab.
        elif performance_tab_current_sub_tab == 3:

            # Get performance data to be drawn.
            performance_data1 = self.network_receive_speed[self.selected_network_card_number]
            performance_data2 = self.network_send_speed[self.selected_network_card_number]

            # Get chart colors.
            chart_line_color = Config.chart_line_color_network_speed_data

            # Check if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices.
            draw_per_device = 0

            # Check which performance data will be drawn.
            if Config.plot_network_download_speed == 1:
                draw_performance_data1 = 1
            else:
                draw_performance_data1 = 0

            if Config.plot_network_upload_speed == 1:
                draw_performance_data2 = 1
            else:
                draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit = 1.1 * ((max(max(performance_data1), max(performance_data2))) + 0.0000001)
            if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                chart_y_limit = 1.1 * (max(performance_data1) + 0.0000001)
            if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                chart_y_limit = 1.1 * (max(performance_data2) + 0.0000001)

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            from Network import Network
            data_unit_for_chart_y_limit = 0
            if Config.performance_network_speed_data_unit >= 8:
                data_unit_for_chart_y_limit = 8
            try:
                chart_y_limit_str = f'{Network.performance_data_unit_converter_func(chart_y_limit, data_unit_for_chart_y_limit, 0)}/s'
            # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
            except AttributeError:
                return
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_split[0])))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            Network.label1413.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            chart_y_limit = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for GPU tab.
        elif performance_tab_current_sub_tab == 4:

            # Get performance data to be drawn.
            from Gpu import Gpu
            try:
                performance_data1 = Gpu.gpu_load_list
            # Handle errors because chart signals are connected before running relevant performance thread (in the GPU module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            except AttributeError:
                return

            # Get chart colors.
            chart_line_color = Config.chart_line_color_fps

            # Check if drawing will be for the current device (CPU core, disk, network card, etc.) or all devices.
            draw_per_device = 0

            # Check which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Draw "average CPU usage" if preferred.
        if draw_per_device == 0:

            # Get chart data history.
            chart_data_history = Config.chart_data_history
            chart_x_axis = list(range(0, chart_data_history))

            # Get chart background color.
            chart_background_color = Config.chart_background_color_all_charts

            # Get drawingarea size.
            chart_width = Gtk.Widget.get_allocated_width(widget)
            chart_height = Gtk.Widget.get_allocated_height(widget)

            # Draw and fill chart background.
            ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
            ctx.rectangle(0, 0, chart_width, chart_height)
            ctx.fill()

            # Draw horizontal and vertical gridlines.
            ctx.set_line_width(1)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
            for i in range(3):
                ctx.move_to(0, chart_height/4*(i+1))
                ctx.rel_line_to(chart_width, 0)
            for i in range(4):
                ctx.move_to(chart_width/5*(i+1), 0)
                ctx.rel_line_to(0, chart_height)
            ctx.stroke()

            # Draw outer border of the chart.
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            ctx.rectangle(0, 0, chart_width, chart_height)
            ctx.stroke()

            if draw_performance_data1 == 1:

                # Draw performance data.
                ctx.move_to(0, chart_height)
                ctx.rel_move_to(0, -chart_height*performance_data1[0]/chart_y_limit)
                for i in range(chart_data_history - 1):
                    delta_x = (chart_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width * chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height*performance_data1[i+1]/chart_y_limit) - (chart_height*performance_data1[i]/chart_y_limit)
                    ctx.rel_line_to(delta_x, -delta_y)
                ctx.stroke_preserve()

                # Set line color (full transparent in order to prevent drawing bolder lines due to overlapping), close the drawn line to fill inside area of it and copy the performance line path to use it for highlighting.
                ctx.set_source_rgba(0, 0, 0, 0)
                ctx.rel_line_to(0, chart_height*performance_data1[-1]/chart_y_limit)
                ctx.rel_line_to(-(chart_width), 0)
                ctx.close_path()
                performance_data1_line_path = ctx.copy_path()
                ctx.stroke()

                # Use previously copied performance line path and fill the closed area (area below the performance data line).
                ctx.append_path(performance_data1_line_path)  
                gradient_pattern = cairo.LinearGradient(0, 0, 0, chart_height)
                gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
                gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
                ctx.set_source(gradient_pattern)
                ctx.fill()

            if draw_performance_data2 == 1:

                # Set color and line dash style for this performance data line.
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.set_dash([5, 3])

                # Draw performance data.
                ctx.move_to(0, chart_height)
                ctx.rel_move_to(0, -chart_height*performance_data2[0]/chart_y_limit)
                for i in range(chart_data_history - 1):
                    delta_x = (chart_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width * chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height*performance_data2[i+1]/chart_y_limit) - (chart_height*performance_data2[i]/chart_y_limit)
                    ctx.rel_line_to(delta_x, -delta_y)
                ctx.stroke_preserve()

                # Set line color (full transparent in order to prevent drawing bolder lines due to overlapping), close the drawn line to fill inside area of it and copy the performance line path to use it for highlighting.
                ctx.set_source_rgba(0, 0, 0, 0)
                ctx.rel_line_to(0, chart_height*performance_data2[-1]/chart_y_limit)
                ctx.rel_line_to(-(chart_width), 0)
                ctx.close_path()
                performance_data2_line_path = ctx.copy_path()
                ctx.stroke()

                # Set line style as solid line.
                ctx.set_dash([])

            # Check if chart line will be highlighted.
            if self.chart_line_highlight == 1:

                # Set antialiasing level as "BEST" in order to avoid low quality chart line because of the highlight effect (more than one line will be overlayed for this appearance).
                ctx.set_antialias(cairo.Antialias.BEST)

                # Set line joining style as "LINE_JOIN_ROUND" in order to avoid spikes at the line joints due to high antialiasing level.
                ctx.set_line_join(cairo.LINE_JOIN_ROUND)

                # Use previously copied performance line path(s).
                if draw_performance_data1 == 1:
                    ctx.append_path(performance_data1_line_path)

                    # Set line features and append the path (draw it).
                    ctx.set_line_width(2.5)
                    ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                    ctx.stroke_preserve()

                    # Set line features (white and semi-transparent color in order to overlay with the previous line and generate highlight effect) and append the path (draw it).
                    ctx.set_line_width(2.5)
                    ctx.set_source_rgba(1, 1, 1, 0.3)
                    ctx.stroke()

                if draw_performance_data2 == 1:
                    ctx.append_path(performance_data2_line_path)

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

                # Check if chart point(s) will be highlighted.
                chart_point_highlight = self.chart_point_highlight
                if chart_point_highlight != -1:

                    # Set color for the point to be highlighted.
                    ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])

                    # Get location of the point(s) to be highlighted.
                    loc_x = chart_width * chart_x_axis[chart_point_highlight]/(chart_data_history-1)
                    loc_y_list =[]
                    if draw_performance_data1 == 1:
                        loc_y1 = chart_height - (chart_height*performance_data1[chart_point_highlight]/chart_y_limit)
                        loc_y_list.append(loc_y1)
                    if draw_performance_data2 == 1:
                        loc_y2 = chart_height - (chart_height*performance_data2[chart_point_highlight]/chart_y_limit)
                        loc_y_list.append(loc_y2)

                    # Draw a big point and fill it.
                    for loc_y in loc_y_list:
                        ctx.arc(loc_x, loc_y, 5, 0, 2*3.14)
                        ctx.fill()

                    # Set font size and text for showing performance data of the highlighted point and get its location data in order to use it for showing a centered box under the text.
                    ctx.set_font_size(13)
                    performance_data_at_point_text_list =[]
                    if draw_performance_data1 == 1:
                        if performance_tab_current_sub_tab == 0:
                            performance_data1_at_point_text = f'{performance_data1[chart_point_highlight]:.{Config.performance_cpu_usage_percent_precision}f} %'
                        elif performance_tab_current_sub_tab == 1:
                            performance_data1_at_point_text = f'{performance_data1[chart_point_highlight]:.{Config.performance_ram_swap_data_precision}f} %'
                        elif performance_tab_current_sub_tab == 2:
                            performance_data1_at_point_text = f'{Disk.performance_data_unit_converter_func(performance_data1[chart_point_highlight], data_unit_for_chart_y_limit, 0)}/s'
                        elif performance_tab_current_sub_tab == 3:
                            performance_data1_at_point_text = f'{Network.performance_data_unit_converter_func(performance_data1[chart_point_highlight], data_unit_for_chart_y_limit, 0)}/s'
                        elif performance_tab_current_sub_tab == 4:
                            performance_data1_at_point_text = f'{performance_data1[chart_point_highlight]:.0f} %'
                        # Add "-" before the text if there are 2 performance data lines.
                        if len(loc_y_list) == 2:
                            performance_data1_at_point_text = f'-  {performance_data1_at_point_text}'
                        performance_data_at_point_text_list.append(performance_data1_at_point_text)

                    if draw_performance_data2 == 1:
                        if performance_tab_current_sub_tab == 0:
                            performance_data2_at_point_text = f'- -{performance_data2[chart_point_highlight]:.{Config.performance_cpu_usage_percent_precision}f} %'
                        elif performance_tab_current_sub_tab == 1:
                            performance_data2_at_point_text = f'- -{performance_data2[chart_point_highlight]:.{Config.performance_ram_swap_data_precision}f} %'
                        elif performance_tab_current_sub_tab == 2:
                            performance_data2_at_point_text = f'- -{Disk.performance_data_unit_converter_func(performance_data2[chart_point_highlight], data_unit_for_chart_y_limit, 0)}/s'
                        elif performance_tab_current_sub_tab == 3:
                            performance_data2_at_point_text = f'- -{Network.performance_data_unit_converter_func(performance_data2[chart_point_highlight], data_unit_for_chart_y_limit, 0)}/s'
                        elif performance_tab_current_sub_tab == 4:
                            performance_data2_at_point_text = f'- -{performance_data2[chart_point_highlight]:.0f} %'
                        performance_data_at_point_text_list.append(performance_data2_at_point_text)

                    performance_data_at_point_text = '  |  '.join(performance_data_at_point_text_list)

                    text_extends = ctx.text_extents(performance_data_at_point_text)
                    text_start_x = text_extends.width / 2
                    text_start_y = text_extends.height / 2
                    text_border_margin = 10
                    origin_for_text =  chart_height*0.35

                    # Calculate correction value for x location of the text, box under the text and line between box and highligthed data point(s) in order to prevent them going out of the visible area (drawingara) when mouse is close to beginning/end of the drawingarea.
                    box_under_text_location_correction = 0
                    box_under_text_start = loc_x-text_start_x-text_border_margin
                    box_under_text_end = loc_x+text_start_x+text_border_margin
                    if box_under_text_start < 0:
                        box_under_text_location_correction = -1 * box_under_text_start
                    if box_under_text_end > chart_width:
                        box_under_text_location_correction = chart_width - box_under_text_end

                    # Set grey color for the box under the text and draw the box.
                    ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
                    ctx.rectangle(box_under_text_start+box_under_text_location_correction,origin_for_text-text_start_y-text_border_margin, text_extends.width+2*text_border_margin, text_extends.height+2*text_border_margin)
                    ctx.fill()

                    # Set color for the text and show the text.
                    ctx.set_line_width(1)
                    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.7)
                    ctx.move_to(loc_x-text_start_x+box_under_text_location_correction,origin_for_text+text_start_y)
                    ctx.show_text(performance_data_at_point_text)

                    # Draw a line between the highlighted point and the box under the text.
                    ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
                    for loc_y in loc_y_list:
                        ctx.move_to(loc_x, loc_y-10)
                        ctx.line_to(box_under_text_start+box_under_text_location_correction, origin_for_text+text_start_y+15)
                        ctx.rel_line_to(text_extends.width+2*text_border_margin, 0)
                        ctx.stroke()

        # Draw "per-core CPU usage" if preferred.
        else:

            # Get chart data history.
            chart_data_history = Config.chart_data_history
            chart_x_axis = list(range(0, chart_data_history))

            # Get performance data to be drawn.
            logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
            number_of_logical_cores = Performance.number_of_logical_cores
            cpu_usage_percent_per_core1 = Performance.cpu_usage_percent_per_core

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent
            chart_background_color = Config.chart_background_color_all_charts

            # Get drawingarea size.
            chart_width = Gtk.Widget.get_allocated_width(widget)
            chart_height = Gtk.Widget.get_allocated_height(widget)

            from math import sqrt, ceil
            # Get number of horizontal and vertical charts (per-core).
            for i in range(1, 1000):
                if number_of_logical_cores % i == 0:
                    number_of_horizontal_charts = i
                    number_of_vertical_charts = number_of_logical_cores // i
                    if number_of_horizontal_charts >= number_of_vertical_charts:
                        if number_of_horizontal_charts > 2 * number_of_vertical_charts:
                            number_of_horizontal_charts = number_of_vertical_charts = ceil(sqrt(number_of_logical_cores))
                        break

            # Get chart index list for horizontal and vertical charts.
            chart_index_list = []
            for i in range(number_of_vertical_charts):
                for j in range(number_of_horizontal_charts):
                    chart_index_list.append([j, i])

            # Spacing 3 from left and right.
            chart_width_per_core = (chart_width / number_of_horizontal_charts) - 6
            # Spacing 3 from top and bottom.
            chart_height_per_core = (chart_height / number_of_vertical_charts) - 6

            # Draw charts per-core.
            for j, cpu_core in enumerate(logical_core_list_system_ordered):

                # Get performance data for the current core.
                cpu_usage_percent_per_core = cpu_usage_percent_per_core1[j]

                # Draw and fill chart background.
                ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
                ctx.rectangle(0, 0, chart_width_per_core, chart_height_per_core)
                ctx.fill()

                # Draw horizontal and vertical gridlines.
                ctx.set_line_width(1)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
                for i in range(3):
                    ctx.move_to((chart_width_per_core+6)*chart_index_list[j][0], chart_index_list[j][1]*(chart_height_per_core+6) + chart_height_per_core/4*(i+1))
                    ctx.rel_line_to(chart_width_per_core, 0)
                for i in range(4):
                    ctx.move_to((chart_width_per_core+6)*chart_index_list[j][0] + chart_width_per_core/5*(i+1), (chart_height_per_core+6)*chart_index_list[j][1])
                    ctx.rel_line_to(0, chart_height_per_core)
                ctx.stroke()

                # Draw outer border of the chart.
                ctx.set_line_width(1)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.rectangle(chart_index_list[j][0]*(chart_width_per_core+6), chart_index_list[j][1]*(chart_height_per_core+6), chart_width_per_core, chart_height_per_core)
                ctx.stroke()

                # Draw performance data.
                ctx.move_to((chart_width_per_core+6)*chart_index_list[j][0], (chart_height_per_core)+(chart_height_per_core+6)*chart_index_list[j][1])
                ctx.rel_move_to(0, -chart_height_per_core*cpu_usage_percent_per_core[0]/100)
                for i in range(len(chart_x_axis) - 1):
                    delta_x = (chart_width_per_core * chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width_per_core * chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height_per_core*cpu_usage_percent_per_core[i+1]/100) - (chart_height_per_core*cpu_usage_percent_per_core[i]/100)
                    ctx.rel_line_to(delta_x, -delta_y)

                # Change line color before drawing lines for closing the drawn line in order to revent drawing bolder lines due to overlapping.
                ctx.stroke_preserve()
                ctx.set_source_rgba(0, 0, 0, 0)

                # Close the drawn line to fill inside area of it.
                ctx.rel_line_to(0, chart_height_per_core*cpu_usage_percent_per_core[-1]/100)
                ctx.rel_line_to(-(chart_width_per_core), 0)
                ctx.close_path()

                # Fill the closed area.
                ctx.stroke_preserve()
                gradient_pattern = cairo.LinearGradient(0, (chart_height_per_core+6)*chart_index_list[j][1], 0, (chart_height_per_core)+(chart_height_per_core+6)*chart_index_list[j][1])
                gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
                gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
                ctx.set_source(gradient_pattern)
                ctx.fill()

                # Draw core number per chart.
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.move_to(chart_index_list[j][0]*(chart_width_per_core+6)+4, chart_index_list[j][1]*(chart_height_per_core+6)+12)
                ctx.show_text(f'{cpu_core.split("cpu")[-1]}')


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

        # Get chart data history.
        chart_data_history = Config.chart_data_history

        # Get drawingarea size.
        chart_width = Gtk.Widget.get_allocated_width(widget)

        # Get mouse position on the x coordinate on the drawingarea.
        mouse_position_x = event.x

        # Calculate the length between chart data points.
        data_point_width = chart_width / (chart_data_history - 1)

        # Calculate number of data points from start (left) to the mouse cursor position and fraction after the last (first data point before the mouse cursor) data point.
        data_point_count_until_mouse_cursor = mouse_position_x / data_point_width
        data_point_count_int = int(data_point_count_until_mouse_cursor)
        fraction = data_point_count_until_mouse_cursor - data_point_count_int

        # Determine the data point to be highlighted when mouse cursor is between two data points.
        if fraction > 0.5:
            self.chart_point_highlight = data_point_count_int + 1
        # if fraction <= 0.5:
        else:
            self.chart_point_highlight = data_point_count_int

        # Update the chart in order to show visual changes.
        widget.queue_draw()


    # ----------------------- Called for drawing performance data as bar chart -----------------------
    def performance_bar_charts_draw_func(self, widget, ctx):

        # Check if drawing will be for RAM tab.
        performance_tab_current_sub_tab = Config.performance_tab_current_sub_tab
        if performance_tab_current_sub_tab == 1:

            # Get performance data to be drawn.
            from Ram import Ram
            try:
                performance_data1 = Ram.swap_percent
            # "swap_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
            except AttributeError:
                return

            # Get chart colors.
            chart_line_color = Config.chart_line_color_ram_swap_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Check if drawing will be for Disk tab.
        if performance_tab_current_sub_tab == 2:

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
            chart_line_color = Config.chart_line_color_ram_swap_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Get chart background color.
        chart_background_color = Config.chart_background_color_all_charts

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

        # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]

        # Unit Name    Abbreviation    bytes   
        # byte         B               1
        # kilobyte     KB              1024
        # megabyte     MB              1.04858E+06
        # gigabyte     GB              1.07374E+09
        # terabyte     TB              1.09951E+12
        # petabyte     PB              1.12590E+15
        # exabyte      EB              1.15292E+18

        # Unit Name    Abbreviation    bits    
        # bit          b               1
        # kilobit      Kb              1024
        # megabit      Mb              1.04858E+06
        # gigabit      Gb              1.07374E+09
        # terabit      Tb              1.09951E+12
        # petabit      Pb              1.12590E+15
        # exabit       Eb              1.15292E+18

        # 1 byte = 8 bits

        self.data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                              [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                              [8, 0, "Auto-bit"], [9, 8, "b"], [10, 1024, "Kib"], [11, 1.04858E+06, "Mib"], [12, 1.07374E+09, "Gib"],
                              [13, 1.09951E+12, "Tib"], [14, 1.12590E+15, "Pib"], [15, 1.15292E+18, "Eib"]]


    # ----------------------- Called for converting data units and setting value precision (called from several modules) -----------------------
    def performance_data_unit_converter_func(self, data, unit, precision):

        data_unit_list = self.data_unit_list
        if isinstance(data, str) == True:
            return data

        if unit >= 8:
            data = data * 8

        if unit in [0, 8]:
            unit_counter = unit + 1
            while data > 1024:
                unit_counter = unit_counter + 1
                data = data/1024
            unit = data_unit_list[unit_counter][2]
            if data == 0:
                precision = 0
            return f'{data:.{precision}f} {unit}'

        data = data / data_unit_list[unit][1]
        unit = data_unit_list[unit][2]
        if data == 0:
            precision = 0
        return f'{data:.{precision}f} {unit}'


# Generate object
Performance = Performance()

