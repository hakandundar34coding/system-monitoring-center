#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('GLib', '2.0')
from gi.repository import GLib
import os

from Config import Config


# Define class
class Performance:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        pass


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

