#!/usr/bin/env python3

# ----------------------------------- Performance - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_import_func():

    global Gtk, GLib, Thread, subprocess, os, time

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import subprocess
    import os
    import time


    global Config, MainGUI, PerformanceGUI, ChartPlots
    import Config, MainGUI, PerformanceGUI, ChartPlots


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


import OpenGL
from OpenGL.GL import *                                                                       # This code could not be run in a module because of the "*". Need to be imported in a module when "GPU" tab is opened. Because importing this module consumes about 11 MiB of RAM.


# ----------------------------------- Performance - Set Selected CPU Core Function (defines CPU logical core to be viewed (hardware and performance data)) -----------------------------------
def performance_set_selected_cpu_core_func():

    # Set selected CPU core
    first_core = logical_core_list[0]
    global selected_cpu_core, selected_cpu_core_number
    if Config.selected_cpu_core in logical_core_list:
        selected_cpu_core = Config.selected_cpu_core
    if Config.selected_cpu_core not in logical_core_list:
        selected_cpu_core = first_core
    selected_cpu_core_number = logical_core_list_system_ordered.index(selected_cpu_core)


# ----------------------------------- Performance - Set Selected Disk Function (defines disk to be viewed (hardware and performance data)) -----------------------------------
def performance_set_selected_disk_func():

    # Set selected disk
    system_disk_list = []
    for disk in disk_list:
        with open("/proc/mounts") as reader:
            proc_mounts_output_lines = reader.read().strip().split("\n")
            for line in proc_mounts_output_lines:
                if line.split()[0].strip() == ("/dev/" + disk) and line.split()[1].strip() == "/":
                    system_disk_list.append(disk)
    global selected_disk_number
    if Config.selected_disk in disk_list:
        selected_disk_number = disk_list.index(Config.selected_disk)
    if Config.selected_disk not in disk_list:
        if system_disk_list != []:
            selected_disk = system_disk_list[0]
            selected_disk_number = disk_list.index(selected_disk)
        if system_disk_list == []:
            selected_disk_number = disk_list.index(disk_list[0])


# ----------------------------------- Performance - Set Selected Network Card Function (defines network card to be viewed (hardware and performance data)) -----------------------------------
def performance_set_selected_network_card_func():

    # Set selected network card
    connected_network_card_list = []
    for network_card in network_card_list:
        with open("/sys/class/net/" + network_card + "/operstate") as reader:
            sys_class_net_output = reader.read().strip()
            if sys_class_net_output == "up":
                connected_network_card_list.append(network_card)
    global selected_network_card_number
    if connected_network_card_list != []:                                                     # This if statement is used in order to avoid error if there is no any network card that connected.
        selected_network_card = connected_network_card_list[0]
    if connected_network_card_list == []:
        selected_network_card = network_card_list[0]
    if Config.selected_network_card == "":                                                    # "" is predefined network card name before release of the software. This statement is used in order to avoid error, if no network card selection is made since first run of the software.
        selected_network_card_number = network_card_list.index(selected_network_card)
    if Config.selected_network_card in network_card_list:
        selected_network_card_number = network_card_list.index(Config.selected_network_card)
    if Config.selected_network_card not in network_card_list:
        selected_network_card_number = network_card_list.index(selected_network_card)


# ----------------------------------- Performance - Set Selected GPU/Graphics Card Function (defines GPU/graphics card to be viewed (hardware and performance data)) -----------------------------------
def performance_get_gpu_list_and_set_selected_gpu_func():

    global gpu_list, gpu_number_list, default_gpu, gpu_device_model_name, gpu_vendor_id_list, gpu_device_id_list
    gpu_list = []
    gpu_number_list = []
    gpu_pci_info_list_unordered = []
    gpu_directory = []
    gpu_device_model_name = []
    gpu_vendor_id_list = []
    gpu_device_id_list = []
    files_in_dev_dri = os.listdir("/dev/dri/")
    for file in files_in_dev_dri:
        if file.startswith("card"):
            gpu_list.append(file)
            gpu_number_list.append(file.split("card")[1])
    files_in_dev_dri_by_path = os.listdir("/dev/dri/by-path/")
    for file in files_in_dev_dri_by_path:
        if file.endswith("card"):
            gpu_pci_info_list_unordered.append(file.split("-card")[0].split("pci-")[1])
    for gpu_number in gpu_number_list:
        for gpu_pci_info in gpu_pci_info_list_unordered:
            if os.path.isdir("/sys/devices/pci0000:00/" + gpu_pci_info + "/drm/card" + gpu_number) == True:
                gpu_directory.append("/sys/devices/pci0000:00/" + gpu_pci_info + "/")
                continue
            if os.path.isdir("/sys/devices/pci0000:00/" + gpu_pci_info + "/drm/card" + gpu_number) == False:
                files_in_sys_devices_pci = os.listdir("/sys/devices/pci0000:00/")
                for file in files_in_sys_devices_pci:
                    if os.path.isdir("/sys/devices/pci0000:00/" + file + "/" + gpu_pci_info + "/drm/card" + gpu_number):
                        gpu_directory.append("/sys/devices/pci0000:00/" + file + "/" + gpu_pci_info + "/")
                        continue
    for i, gpu_number in enumerate(gpu_number_list):
        with open(gpu_directory[i] + "/boot_vga") as reader:
            if reader.read().strip() == "1":
                default_gpu = gpu_list[i]
        with open(gpu_directory[i] + "/vendor") as reader:
            gpu_vendor_id = "\n" + reader.read().split("x")[1].strip() + "  "
        with open(gpu_directory[i] + "/device") as reader:
            gpu_device_id = "\n\t" + reader.read().split("x")[1].strip() + "  "
        with open("/usr/share/misc/pci.ids") as reader:
            pci_ids_output = reader.read()
            if gpu_vendor_id in pci_ids_output:
                rest_of_the_pci_ids_output = pci_ids_output.split(gpu_vendor_id)[1]
                gpu_vendor_name = rest_of_the_pci_ids_output.split("\n")[0].strip()
            if gpu_device_id in rest_of_the_pci_ids_output:
                rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(gpu_device_id)[1]
                gpu_device_name = rest_of_the_rest_of_the_pci_ids_output.split("\n")[0].strip()
        gpu_device_model_name.append(f'{gpu_vendor_name} {gpu_device_name}')
        gpu_vendor_id_list.append(gpu_vendor_id)                                              # This list will be used for matching with GPU information from "glxinfo" command.
        gpu_device_id_list.append(gpu_device_id)                                              # This list will be used for matching with GPU information from "glxinfo" command.

    # Set selected gpu/graphics card
    if Config.selected_gpu == "":                                                             # "" is predefined disk name before release of the software. This statement is used in order to avoid error, if no disk selection is made since first run of the software.
        set_selected_gpu = default_gpu
    if Config.selected_gpu in gpu_list:
        set_selected_gpu = Config.selected_gpu
    if Config.selected_gpu not in gpu_list:
        set_selected_gpu = default_gpu
    global selected_gpu_number
    selected_gpu_number = gpu_list.index(set_selected_gpu)


# ----------------------------------- Performance - Background Initial Function (defines initial arrays and values for performance background function) -----------------------------------
def performance_background_initial_func():

    # Define common initial values for performance data
    global chart_data_history
    chart_data_history = Config.chart_data_history                                            # This value will be used multiple times and it is get from another module and defined as a variable in this module in order to achieve lower CPU consumption.

    # Define initial values for CPU usage percent
    global logical_core_list, cpu_time_all_prev, cpu_time_load_prev, cpu_usage_percent_ave
    logical_core_list = []
    cpu_time_all_prev = []
    cpu_time_load_prev = []
    cpu_usage_percent_ave = [0] * chart_data_history

    # Define initial values for RAM usage percent
    global ram_usage_percent
    ram_usage_percent = [0] * chart_data_history

    # Define initial values for disk read speed and write speed
    global disk_sector_size
    disk_sector_size = 512                                                                    # Disk data from /proc/diskstats are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).
    global disk_list, disk_read_data_prev, disk_write_data_prev, disk_read_speed, disk_write_speed
    disk_list = []
    disk_read_data_prev = []
    disk_write_data_prev = []
    disk_read_speed = []
    disk_write_speed = []

    # Define initial values for network receive speed and network send speed
    global network_card_list, network_receive_bytes_prev, network_send_bytes_prev, network_receive_speed, network_send_speed
    network_card_list = []
    network_receive_bytes_prev = []
    network_send_bytes_prev =[]
    network_receive_speed = []
    network_send_speed = []

    # Define initial values for fps_count and frame_latency values
    global fps_count, frame_latency
    fps_count = [0] * Config.chart_data_history
    frame_latency = 0

    # Reset selected hardware if "remember_last_selected_hardware" prefrence is disabled by the user.
    if Config.remember_last_selected_hardware == 0:
        Config.selected_cpu_core = ""
        Config.selected_disk = ""
        Config.selected_network_card = ""
        Config.selected_gpu = ""

# ----------------------------------- Performance - Background Function (gets basic CPU, RAM, disk and network usage data in the background in order to assure uninterrupted data for charts) -----------------------------------
def performance_background_func():

    update_interval = Config.update_interval                                                  # This value will be used multiple times and it is get from another module and defined as a variable in this module in order to achieve lower CPU consumption.

    # Get logical_core_list, number_of_logical_cores
    global logical_core_list_system_ordered, logical_core_list, number_of_logical_cores       # "logical_core_list" list contains online CPU core numbers and ordering changes when online/offline CPU core changes are made. Last online-made core is listed as the last core.
    global cpu_time_all, cpu_time_load
    global cpu_time_all_prev, cpu_time_load_prev                                              # Make global previously defined variables, therefore Python could acces these variables faster (it directly searchs in globals()).
    logical_core_list_system_ordered = []                                                     # "logical_core_list_system_ordered" contains online CPU core numbers in the order of "/proc/stats" file content which is in "ascending" online core number order.
    with open("/proc/stat") as reader:                                                        # "/proc/stat" file contains online logical CPU core numbers (all cores without regarding CPU sockets, physical/logical cores) and CPU times since system boot. This file is not a real file (it is provided by using Virtual File System by the OS kernel) and it is not located on the storage.
        proc_stat_lines = reader.read().split("intr")[0].strip().split("\n")[1:]              # Trimmed unneeded information in the file
    for line in proc_stat_lines:
        line = line.split()
        logical_core_list_system_ordered.append(line[0].split("cpu")[1])                      # Add CPU core numbers into a temporary list in ascending core number order. This list will be used with logical_core_list in order to track last online-made CPU core. This operations are performed in order to track CPU usage per core continuously even if CPU cores made online/offline.
    number_of_logical_cores = len(logical_core_list_system_ordered)                           # Count number of online logical CPU cores.
    for i, cpu_core in enumerate(logical_core_list_system_ordered):                           # Track the changes if CPU core is made online/offline
        if cpu_core not in logical_core_list:                                                 # Add new core number into logical_core_list if CPU core is made online. Also CPU time data related to online-made the core is appended into lists.
            logical_core_list.append(cpu_core)
            cpu_time = proc_stat_lines[i].split()
            cpu_time_all_scratch = int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9])
            cpu_time_load_scratch = cpu_time_all_scratch - int(cpu_time[4]) - int(cpu_time[5])
            cpu_time_all_prev.append(cpu_time_all_scratch)
            cpu_time_load_prev.append(cpu_time_load_scratch)
            performance_set_selected_cpu_core_func()
            if "performance_background_first_loop_completed" in globals():
                performance_foreground_initial_func()
    for cpu_core in logical_core_list:                                                        # Remove core number from logical_core_list if it is made offline. Also CPU time data related to offline-made the core is removed from lists.
        if cpu_core not in logical_core_list_system_ordered:
            del cpu_time_all_prev[logical_core_list.index(cpu_core)]
            del cpu_time_load_prev[logical_core_list.index(cpu_core)]
            logical_core_list.remove(cpu_core)
            performance_set_selected_cpu_core_func()
            if "performance_background_first_loop_completed" in globals():
                performance_foreground_initial_func()
    # Get cpu_usage_percent_per_core, cpu_usage_percent_ave
    global cpu_usage_percent_per_core, cpu_usage_percent_ave
    cpu_time_all = []
    cpu_time_load = []
    cpu_usage_percent_per_core = []
    for i, cpu_core in enumerate(logical_core_list):                                          # Get CPU core times calculate CPU usage values and append usage values into lists in the core number order listed in logical_core_list.
        cpu_time = proc_stat_lines[logical_core_list_system_ordered.index(cpu_core)].split()
        cpu_time_all.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))    # All time since boot for the cpu core
        cpu_time_load.append(cpu_time_all[-1] - int(cpu_time[4]) - int(cpu_time[5]))                                                                                                                     # Time elapsed during core processing for the core
        if cpu_time_all[-1] - cpu_time_all_prev[i] == 0:
            cpu_time_all[-1] = cpu_time_all[-1] + 1                                           # Append 1 CPU time (a negligible value) in order to avoid zeor division error in the first loop after application start or in the first loop of newly online-made CPU core. It is corrected in the next loop.
        cpu_usage_percent_per_core.append((cpu_time_load[-1] - cpu_time_load_prev[i]) / (cpu_time_all[-1] - cpu_time_all_prev[i]) * 100)    # Calculate CPU usage precent for the core (load time difference / all time difference *100). Time difference is calculated as "value in this loop - value from previous loop". CPU times difference interval should be higher than 0.1 seconds in order to achieve an accurate CPU usage percent value. For many systems CPU ticks 100 times in a second and this value could be get by using "os.sysconf("SC_CLK_TCK")". If measurement is made in a lower time interval, "0" CPU usage could be get.
    cpu_usage_percent_ave.append(sum(cpu_usage_percent_per_core) / number_of_logical_cores)   # Calculate average CPU usage for all logical cores (summation of CPU usage per core / number of logical cores)
    del cpu_usage_percent_ave[0]                                                              # Delete the first CPU usage percent value from the list in order to keep list lenght same. Because a new value is appended in every loop. This list is used for CPU usage percent graphic.        
    cpu_time_all_prev = list(cpu_time_all)                                                    # Use the values as "previous" data. This data will be used in the next loop for calculating time difference.
    cpu_time_load_prev = list(cpu_time_load)                                                  # Use the values as "previous" data. This data will be used in the next loop for calculating time difference.

    # Get ram_usage_percent
    global ram_usage_percent
    global ram_total, ram_free, ram_available, ram_used
    with open("/proc/meminfo") as reader:                                                     # RAM usage information is get from /proc/meminfo VFS file.
        memory_info = reader.read().split("\n")
        for line in memory_info:
            if line.startswith("MemTotal:"):
                ram_total = int(line.split()[1]) * 1024                                       # Memory values in /proc/meminfo directory are in KibiBytes (KiB). Thet are multiplied with 1024 in order to convert them into bytes. There is some accuracy deviation during the convertion (only in bytes form, it is not valid for KiB, MiB, ...) but it is negligible.
            if line.startswith("MemFree:"):
               ram_free = int(line.split()[1]) * 1024
            if line.startswith("MemAvailable:"):
                ram_available = int(line.split()[1]) * 1024
            if line.startswith("Buffers:"):
                ram_buffers = int(line.split()[1]) * 1024
            if line.startswith("Cached:"):
                ram_cached = int(line.split()[1]) * 1024
        ram_used = ram_total - ram_free - ram_cached - ram_buffers                            # Used RAM value is calculated
        ram_usage_percent.append(ram_used / ram_total * 100)                                  # Used RAM percentage is calculated
        del ram_usage_percent[0]                                                              # Delete the first RAM usage percent value from the list in order to keep list lenght same. Because a new value is appended in every loop. This list is used for RAM usage percent graphic.

    # Get disk_list
    global disk_list_system_ordered, disk_list
    global disk_read_data, disk_write_data
    global disk_read_data_prev, disk_write_data_prev
    global disk_read_speed, disk_write_speed
    disk_list_system_ordered = []
    proc_diskstats_lines_filtered = []
    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().strip().split("\n")[2:]
    for line in proc_partitions_lines:
        disk_list_system_ordered.append(line.split()[3].strip())
    with open("/proc/diskstats") as reader:
        proc_diskstats_lines = reader.read().strip().split("\n")
        for line in proc_diskstats_lines:
            if line.split()[2] in disk_list_system_ordered:
                proc_diskstats_lines_filtered.append(line)                                    # Disk information of some disks (such a loop devices) exist in "/proc/diskstats" file even if these dvice are unmounted. "proc_diskstats_lines_filtered" list is used in order to use disk list without these remaining information.
    for i, disk in enumerate(disk_list_system_ordered):
        if disk not in disk_list:
            disk_list.append(disk)
            disk_data = proc_diskstats_lines[i].split()
            disk_read_data = int(disk_data[5]) * disk_sector_size
            disk_write_data = int(disk_data[9]) * disk_sector_size
            disk_read_data_prev.append(disk_read_data)
            disk_write_data_prev.append(disk_write_data)
            disk_read_speed.append([0] * chart_data_history)
            disk_write_speed.append([0] * chart_data_history)
            performance_set_selected_disk_func()
            if "performance_background_first_loop_completed" in globals():
                performance_foreground_initial_func()
    for disk in reversed(disk_list):
        if disk not in disk_list_system_ordered:
            del disk_read_data_prev[disk_list.index(disk)]
            del disk_write_data_prev[disk_list.index(disk)]
            del disk_read_speed[disk_list.index(disk)]
            del disk_write_speed[disk_list.index(disk)]
            disk_list.remove(disk)
            performance_set_selected_disk_func()
            if "performance_background_first_loop_completed" in globals():
                performance_foreground_initial_func()
    # Get disk_read_speed, disk_write_speed
    disk_read_data = []
    disk_write_data = []
    for i, disk in enumerate(disk_list):
        disk_data = proc_diskstats_lines_filtered[disk_list_system_ordered.index(disk)].split()
        disk_read_data.append(int(disk_data[5]) * disk_sector_size)
        disk_write_data.append(int(disk_data[9]) * disk_sector_size)
        if disk_read_data[-1] - disk_read_data_prev[i] == 0:
            pass
        disk_read_speed[i].append((disk_read_data[-1] - disk_read_data_prev[i]) / update_interval)
        disk_write_speed[i].append((disk_write_data[-1] - disk_write_data_prev[i]) / update_interval)
        del disk_read_speed[i][0]
        del disk_write_speed[i][0]
    disk_read_data_prev = list(disk_read_data)
    disk_write_data_prev = list(disk_write_data)

    # Get network card list
    global network_card_list_system_ordered, network_card_list
    global network_receive_bytes, network_send_bytes
    global network_receive_bytes_prev, network_send_bytes_prev
    global network_receive_speed, network_send_speed
    network_card_list_system_ordered = []
    with open("/proc/net/dev") as reader:
        proc_net_dev_lines = reader.read().strip().split("\n")[2:]
    for line in proc_net_dev_lines:
        network_card_list_system_ordered.append(line.split(":")[0].strip())
    for i, network_card in enumerate(network_card_list_system_ordered):
        if network_card not in network_card_list:
            network_card_list.append(network_card)
            network_data = proc_net_dev_lines[i].split()
            network_receive_bytes = int(network_data[1])
            network_send_bytes = int(network_data[9])
            network_receive_bytes_prev.append(network_receive_bytes)
            network_send_bytes_prev.append(network_send_bytes)
            network_receive_speed.append([0] * chart_data_history)
            network_send_speed.append([0] * chart_data_history)
            performance_set_selected_network_card_func()
            if "performance_background_first_loop_completed" in globals():
                performance_foreground_initial_func()
    for network_card in reversed(network_card_list):
        if network_card not in network_card_list_system_ordered:
            del network_receive_bytes_prev[network_card_list.index(network_card)]
            del network_send_bytes_prev[network_card_list.index(network_card)]
            del network_receive_speed[network_card_list.index(network_card)]
            del network_send_speed[network_card_list.index(network_card)]
            network_card_list.remove(network_card)
            performance_set_selected_network_card_func()
            if "performance_background_first_loop_completed" in globals():
                performance_foreground_initial_func()
    # Get network_receive_speed, network_send_speed
    network_receive_bytes = []
    network_send_bytes = []
    for i, network_card in enumerate(network_card_list):
        network_data = proc_net_dev_lines[network_card_list_system_ordered.index(network_card)].split()
        network_receive_bytes.append(int(network_data[1]))
        network_send_bytes.append(int(network_data[9]))
        if network_receive_bytes[-1] - network_receive_bytes_prev[i] == 0:
            pass
        network_receive_speed[i].append((network_receive_bytes[-1] - network_receive_bytes_prev[i]) / update_interval)
        network_send_speed[i].append((network_send_bytes[-1] - network_send_bytes_prev[i]) / update_interval)
        del network_receive_speed[i][0]
        del network_send_speed[i][0]
    network_receive_bytes_prev = list(network_receive_bytes)
    network_send_bytes_prev = list(network_send_bytes)

    global performance_background_first_loop_completed
    performance_background_first_loop_completed = 1

# ----------------------------------- Performance - Background Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def performance_background_initial_initial_func():

    GLib.idle_add(performance_background_initial_func)


# ----------------------------------- Performance Background Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def performance_background_loop_func():

    GLib.idle_add(performance_background_func)
    global update_interval
    update_interval = Config.update_interval
    GLib.timeout_add(update_interval * 1000, performance_background_loop_func)


# ----------------------------------- Performance Background Thread Run Function (starts execution of the threads) -----------------------------------
def performance_background_thread_run_func():

    global performance_background_initial_thread, performance_background_thread
    performance_background_initial_thread = Thread(target=performance_background_initial_initial_func, daemon=True)
    performance_background_initial_thread.start()
    performance_background_initial_thread.join()
    performance_background_thread = Thread(target=performance_background_loop_func, daemon=True)
    performance_background_thread.start()



# ----------------------------------- Performance - Foreground Initial Function (shows performance data (this data isnot updated continuously, it is updated if Peformance tab is switched off and on) on the GUI) -----------------------------------
def performance_foreground_initial_func():

    performance_define_data_unit_converter_variables_func()                                   # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    if PerformanceGUI.radiobutton1001.get_active() == True:                                   # Check if CPU tab is selected.
        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names
        cpu_model_names = []
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_lines = reader.read().split("\n")
            number_of_physical_cores = 0
            physical_id = 0
            physical_id_prev = 0
            for line in proc_cpuinfo_lines:
                if line.startswith("physical id"):
                    physical_id_prev = physical_id
                    physical_id = line.split(":")[1].strip()
                if physical_id != physical_id_prev and line.startswith("cpu cores"):
                    number_of_physical_cores = number_of_physical_cores + int(line.split(":")[1].strip())
                if line.startswith("model name"):
                    cpu_model_names.append(line.split(":")[1].strip())
            number_of_cpu_sockets = int(physical_id) + 1
        # Get maximum and minimum frequencies of all cores
        cpu_max_frequency_all_cores = []
        cpu_min_frequency_all_cores = []
        if os.path.isfile("/sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq") is True:
            for cpu_core in logical_core_list_system_ordered:
                with open("/sys/devices/system/cpu/cpufreq/policy" + cpu_core + "/scaling_max_freq") as reader:
                    cpu_max_frequency_all_cores.append(float(reader.read().strip()) / 1000)
                with open("/sys/devices/system/cpu/cpufreq/policy" + cpu_core + "/scaling_min_freq") as reader:
                    cpu_min_frequency_all_cores.append(float(reader.read().strip()) / 1000)
        else:
            cpu_max_frequency_all_cores = ["-"] * number_of_logical_cores
            cpu_min_frequency_all_cores = ["-"] * number_of_logical_cores
        # Get cache values of all cores
        cpu_l1d_cache_values = []
        cpu_l1i_cache_values = []
        cpu_l2_cache_values = []
        cpu_l3_cache_values = []
        for cpu_core in logical_core_list_system_ordered:
            if os.path.isfile("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index0/level") is True:    # Get l1d cache values
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index0/level") as reader:
                    cache_level = reader.read().strip()
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index0/type") as reader:
                    cache_type = reader.read().strip()
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index0/size") as reader:
                    cache_size = reader.read().strip()
                if cache_level == "1" and cache_type == "Data":
                    cpu_l1d_cache_values.append(cache_size)
            else:
                cpu_l1d_cache_values.append("-")
            if os.path.isfile("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index1/level") is True:    # Get li cache values
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index1/level") as reader:
                    cache_level = reader.read().strip()
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index1/type") as reader:
                    cache_type = reader.read().strip()
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index1/size") as reader:
                    cache_size = reader.read().strip()
                if cache_level == "1" and cache_type == "Instruction":
                    cpu_l1i_cache_values.append(cache_size)
            else:
                cpu_l1i_cache_values.append("-")
            if os.path.isfile("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index2/level") is True:    # Get l2 cache values
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index2/level") as reader:
                    cache_level = reader.read().strip()
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index2/size") as reader:
                    cache_size = reader.read().strip()
                if cache_level == "2":
                    cpu_l2_cache_values.append(cache_size)
            else:
                cpu_l2_cache_values.append("-")
            if os.path.isfile("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index3/level") is True:    # Get l3 cache values
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index3/level") as reader:
                    cache_level = reader.read().strip()
                with open("/sys/devices/system/cpu/cpu" + cpu_core + "/cache/index3/size") as reader:
                    cache_size = reader.read().strip()
                if cache_level == "3":
                    cpu_l3_cache_values.append(cache_size)
            else:
                cpu_l3_cache_values.append("-")
        # Get CPU architecture
        lscpu_output = (subprocess.check_output("lscpu", shell=True).strip()).decode().split("\n")
        for line in lscpu_output:
            if "Architecture:" in line:
                cpu_architecture = line.split(":")[1].strip()
        if 'cpu_architecture' not in dir():
            cpu_architecture = "-"

        # Set CPU tab label texts by using information get
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            PerformanceGUI.label1113.set_text(_tr("CPU Usage % (Average):"))
        if show_cpu_usage_per_core == 1:
            PerformanceGUI.label1113.set_text(_tr("CPU Usage % (Per Core):"))
        PerformanceGUI.label1101.set_text(cpu_model_names[selected_cpu_core_number])
#         PerformanceGUI.label1102.set_text(f'Selected CPU Core: {selected_cpu_core}')
        PerformanceGUI.label1102.set_text(_tr("Selected CPU Core: ") + selected_cpu_core)
        if isinstance(cpu_max_frequency_all_cores[selected_cpu_core_number], str) is False:
            PerformanceGUI.label1105.set_text(f'{cpu_min_frequency_all_cores[selected_cpu_core_number]:.0f} - {cpu_max_frequency_all_cores[selected_cpu_core_number]:.0f} MHz')
        if isinstance(cpu_max_frequency_all_cores[selected_cpu_core_number], str) is True:
            PerformanceGUI.label1105.set_text(f'{cpu_min_frequency_all_cores[selected_cpu_core_number]} - {cpu_max_frequency_all_cores[selected_cpu_core_number]}')
        PerformanceGUI.label1106.set_text(f'{number_of_cpu_sockets}')
        PerformanceGUI.label1107.set_text(f'{number_of_physical_cores} - {number_of_logical_cores}')
        PerformanceGUI.label1108.set_text(cpu_architecture)
        PerformanceGUI.label1109.set_text(f'{cpu_l1i_cache_values[selected_cpu_core_number]} - {cpu_l1d_cache_values[selected_cpu_core_number]}')
        PerformanceGUI.label1110.set_text(f'{cpu_l2_cache_values[selected_cpu_core_number]} - {cpu_l3_cache_values[selected_cpu_core_number]}')


    if PerformanceGUI.radiobutton1002.get_active() == True:                                   # Check if RAM tab is selected.
        performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
        performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit

        # Get total_physical_ram value (this value is very similar to RAM hardware size which is a bit different than ram_total value)
        with open("/sys/devices/system/memory/block_size_bytes") as reader:                   # "memory block size" is read from this file and size of the blocks depend on architecture (For more information see: https://www.kernel.org/doc/html/latest/admin-guide/mm/memory-hotplug.html).
            block_size = int(reader.read().strip(), 16)                                       # Value in this file is in hex form and it is converted into integer (byte)
        total_online_memory = 0
        total_offline_memory = 0
        files_in_sys_devices_system_memory = os.listdir("/sys/devices/system/memory/")        # Number of folders (of which name start with "memory") in this folder is multiplied with the integer value of "block_size_bytes" file content (hex value).
        for file in files_in_sys_devices_system_memory:
            if os.path.isdir("/sys/devices/system/memory/" + file) and file.startswith("memory"):
                with open("/sys/devices/system/memory/" + file + "/online") as reader:
                    if reader.read().strip() == "1":
                        total_online_memory = total_online_memory + block_size
                    if reader.read().strip() == "0":
                        total_offline_memory = total_offline_memory + block_size
        total_physical_ram = (total_online_memory + total_offline_memory)                     # Summation of total online and offline memories gives RAM hardware size. RAM harware size and total RAM value get from proc file system of by using "free" command are not same thing. Because some of the RAM may be reserved for harware and/or by the OS kernel.
        # Get ram_total and swap_total values
        with open("/proc/meminfo") as reader:
            proc_memory_info_output_lines = reader.read().split("\n")
            for line in proc_memory_info_output_lines:
                if "MemTotal:" in line:
                    ram_total = int(line.split()[1]) * 1024                                   # Values in this file are in "KiB" unit. These values are multiplied with 1024 in order to obtain byte (nearly) values.
                if "SwapTotal:" in line:
                    swap_total = int(line.split()[1]) * 1024

        # Set RAM tab label texts by using information get
#         PerformanceGUI.label1201.set_text(f'Total Physical RAM: {performance_data_unit_converter_func(total_physical_ram, 0, 1)}')
#         PerformanceGUI.label1202.set_text(f'Reserved Swap Memory: {performance_data_unit_converter_func(swap_total, 0, 1)}')
        PerformanceGUI.label1201.set_text(_tr("Total Physical RAM: ") + str(performance_data_unit_converter_func(total_physical_ram, 0, 1)))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.
        PerformanceGUI.label1202.set_text(_tr("Reserved Swap Memory: ") + str(performance_data_unit_converter_func(swap_total, 0, 1)))
        PerformanceGUI.label1205.set_text(performance_data_unit_converter_func(ram_total, performance_ram_swap_data_unit, performance_ram_swap_data_precision))


    if PerformanceGUI.radiobutton1003.get_active() == True:                                   # Check if Disk tab is selected.
        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            if os.path.isdir("/sys/class/block/" + disk_list[selected_disk_number]) == False:
                return
        except:
            return
        # Get disk_model_name, parent_disk, disk_mount_point
        performance_get_device_partition_model_name_mount_point_func()
        # Get disk_file_system
        with open("/proc/mounts") as reader:                                                  # Get file systems for mounted disks
            proc_mounts_output_lines = reader.read().strip().split("\n")
            for line in proc_mounts_output_lines:
                if line.split()[0].strip() == ("/dev/" + disk_list[selected_disk_number]):
                    disk_file_system = line.split()[2].strip()
                    break
                else:
                    disk_file_system = _tr("[Not mounted]")
        with open("/proc/swaps") as reader:                                                   # Show "[SWAP]" information for swap disks (if selected swap area is partition (not file))
            proc_swaps_output_lines = reader.read().strip().split("\n")
            swap_disk_list = []
            for line in proc_swaps_output_lines:
                if line.split()[1].strip() == "partition":
                    swap_disk_list.append(line.split()[0].strip().split("/")[-1])
        if len(swap_disk_list) > 0 and disk_list[selected_disk_number] in swap_disk_list:
            disk_file_system = _tr("[SWAP]")
        if disk_file_system  == "fuseblk":                                                    # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
            try:
                disk_file_system_from_lsblk = (subprocess.check_output("lsblk -no FSTYPE /dev/" + disk_list[selected_disk_number], shell=True).strip()).decode()
                disk_file_system = disk_file_system + " (" + disk_file_system_from_lsblk + ")"
            except:
                pass
        # Get if_system_disk
        if disk_mount_point == "/":
            if_system_disk = _tr("Yes")
        else:
            if_system_disk = _tr("No")

        # Set Disk tab label texts by using information get
        PerformanceGUI.label1301.set_text(disk_model_name)
        PerformanceGUI.label1302.set_text(f'{disk_list[selected_disk_number]} ({disk_device_or_partition})')
        PerformanceGUI.label1307.set_text(disk_file_system)
        PerformanceGUI.label1312.set_text(if_system_disk)


    if PerformanceGUI.radiobutton1004.get_active() == True:                                   # Check if Network tab is selected.
        # Get network_card_device_name
        network_card_vendor_name = "-"
        network_card_device_name = "-"
        if network_card_list[selected_network_card_number] != "lo":
            with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/device/vendor") as reader:   # Get network card vendor id
                network_card_vendor_id = "\n" + reader.read().split("x")[1].strip() + "  "
            with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/device/device") as reader:   # Get network card device id
                network_card_device_id = "\n\t" + reader.read().split("x")[1].strip() + "  "
            with open("/usr/share/misc/pci.ids") as reader:                                   # Find network card device model from "/usr/share/misc/pci.ids" file by using vendor id and device id.
                pci_ids_output = reader.read()
                if network_card_vendor_id in pci_ids_output:
                    rest_of_the_pci_ids_output = pci_ids_output.split(network_card_vendor_id)[1]
                    network_card_vendor_name = rest_of_the_pci_ids_output.split("\n")[0].strip()
                if network_card_device_id in rest_of_the_pci_ids_output:
                    rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(network_card_device_id)[1]
                    network_card_device_name = rest_of_the_rest_of_the_pci_ids_output.split("\n")[0].strip()
        network_card_device_model_name = f'{network_card_vendor_name} {network_card_device_name}'
        if network_card_list[selected_network_card_number] == "lo":                           # lo (Loopback Device) is a system device and it is not a physical device. Therefore it could not be found in "/usr/share/misc/pci.ids" file.
            network_card_device_model_name = "Loopback Device"
        # Get connection_type
        if "en" in network_card_list[selected_network_card_number]:
            connection_type = _tr("Ethernet")
        elif "wl" in network_card_list[selected_network_card_number]:
            connection_type = _tr("Wi-Fi")
        else:
            connection_type = "-"
        # Get network_card_mac_address
        with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/address") as reader:
            network_card_mac_address = reader.read().strip().upper()
        # Get network_address_ipv4, network_address_ipv6
        ip_output_lines = (subprocess.check_output("ip a show " + network_card_list[selected_network_card_number], shell=True).strip()).decode().split("\n")
        for line in ip_output_lines:
            if "inet " in line:
                network_address_ipv4 = line.split()[1].split("/")[0]
            if "inet6 " in line:
                network_address_ipv6 = line.split()[1].split("/")[0]
        if "network_address_ipv4" not in locals():
            network_address_ipv4 = "-"
        if "network_address_ipv6" not in locals():
            network_address_ipv6 = "-"

        # Set Network tab label texts by using information get
        PerformanceGUI.label1401.set_text(network_card_device_model_name)
        PerformanceGUI.label1402.set_text(network_card_list[selected_network_card_number])
        PerformanceGUI.label1407.set_text(connection_type)
        PerformanceGUI.label1410.set_text(network_address_ipv4)
        PerformanceGUI.label1411.set_text(network_address_ipv6)
        PerformanceGUI.label1412.set_text(network_card_mac_address)


    if PerformanceGUI.radiobutton1005.get_active() == True:                                   # Check if GPU tab is selected.

        # Measure FPS
        if "frame_list" not in globals():
            global glarea1501, frame_list
            glarea1501 = PerformanceGUI.glarea1501
            frame_list = []

            def on_glarea1501_realize(area):
                area.make_current()
                if (area.get_error() != None):
                  return

            def on_glarea1501_render(area, context):
                glClearColor(0.5, 0.5, 0.5, 1.0)
                glClear(GL_COLOR_BUFFER_BIT)
                glFlush()
                global frame_list
                frame_list.append(0)
                #PerformanceGUI.label1513.set_text(".")
                glarea1501.queue_draw()
                return True

            glarea1501.connect('realize', on_glarea1501_realize)
            glarea1501.connect('render', on_glarea1501_render)

        # Get gpu_device_name value
        performance_get_gpu_list_and_set_selected_gpu_func()                                  # Get gpu/graphics card list and set selected gpu
        # Get video_memory, if_unified_memory, direct_rendering, mesa_version, opengl_version values of the GPU which is preferred for running this application. "DRI_PRIME application-name" and "DRI_PRIME=1 application-name" could be used for running an application by using internal and external GPUs respectively.
        glxinfo_command_list = ["glxinfo -B", "DRI_PRIME=1 glxinfo -B"]
        for command in glxinfo_command_list:                                                  # "10" is large enough to try for all GPUs on an average computer.
            try:
                glxinfo_output_lines = (subprocess.check_output(command, shell=True).strip()).decode().split("\n")    # This command gives current GPU information. If application is run with "DRI_PRIME=1 application-name" this command gives external GPU information.
                for line in glxinfo_output_lines:
                    if line.strip().startswith("Vendor:"):
                        gpu_vendor_in_driver = line.split()[-1].strip("()").split("x")[1].strip()
                    if line.strip().startswith("Device:"):
                        gpu_device_in_driver = line.split()[-1].strip("()").split("x")[1].strip()
            except:
                gpu_vendor_in_driver = "-"
                gpu_device_in_driver = "-"
            if gpu_vendor_in_driver == gpu_vendor_id_list[selected_gpu_number].strip(" \n\t") and gpu_device_in_driver == gpu_device_id_list[selected_gpu_number].strip(" \n\t")[1:]:    # Check for matching GPU information from "sys/devices/pci0000:00/..." directory and from "glxinfo" command. "[1:]" is used for trimming "0" at the beginning of the device id which is get from "/sys/devices/..." directory.
                break
        try:
            for line in glxinfo_output_lines:
                if line.strip().startswith("OpenGL vendor string:"):
                    gpu_vendor_name_in_driver = line.split(":")[1].strip()
                if line.strip().startswith("OpenGL renderer string:"):
                    gpu_device_name_in_driver = line.split(":")[1].strip()
                if line.strip().startswith("Video memory:"):
                    video_memory = line.split(":")[1].strip()
                if line.strip().startswith("Unified memory:"):
                    if_unified_memory = line.split(":")[1].strip().capitalize()
                if line.strip().startswith("direct rendering:"):
                    direct_rendering = line.split(":")[1].strip()
                if line.strip().startswith("Version:"):
                    mesa_version = line.split(":")[1].strip()
                if line.strip().startswith("OpenGL version string:"):
                    opengl_version, display_driver = line.split(":")[1].strip().split(" ", 1)   # "split(" ", 1" is for splitting string by first space character
        except:
            gpu_vendor_name_in_driver = "-"
            gpu_device_name_in_driver = "-"
            video_memory = "-"
            if_unified_memory = "-"
            direct_rendering = "-"
            mesa_version = "-"
            opengl_version = "-"
            display_driver = "-"
        # Get if_default_gpu value
        if gpu_list[selected_gpu_number] == default_gpu:
            if_default_gpu = _tr("Yes")
        if gpu_list[selected_gpu_number] != default_gpu:
            if_default_gpu = _tr("No")

        # Set GPU tab label texts by using information get
        PerformanceGUI.label1501.set_text(gpu_device_model_name[selected_gpu_number])
        PerformanceGUI.label1502.set_text(f'{gpu_list[selected_gpu_number]} ({gpu_vendor_name_in_driver} {gpu_device_name_in_driver})')
        PerformanceGUI.label1507.set_text(if_default_gpu)
        PerformanceGUI.label1508.set_text(video_memory)
        PerformanceGUI.label1509.set_text(if_unified_memory)
        PerformanceGUI.label1510.set_text(direct_rendering)
        PerformanceGUI.label1511.set_text(display_driver)
        PerformanceGUI.label1512.set_text(opengl_version)


# ----------------------------------- Performance - Foreground Function (updates performance data on the GUI) -----------------------------------
def performance_foreground_func():

    # Update performance data on the headerbar
    if Config.performance_summary_on_the_headerbar == 1:                                      # Perform the following operations if "performance_summary_on_the_headerbar" preference is enabled by the user.
        ChartPlots.drawingarea101.queue_draw()
        ChartPlots.drawingarea102.queue_draw()
        MainGUI.label101.set_text(f'{performance_data_unit_converter_func((disk_read_speed[selected_disk_number][-1] + disk_write_speed[selected_disk_number][-1]), 0, 0)}/s')
        MainGUI.label102.set_text(f'{performance_data_unit_converter_func((network_receive_speed[selected_network_card_number][-1] + network_send_speed[selected_network_card_number][-1]), 0, 0)}/s')

    # Update CPU tab data on the GUI
    if PerformanceGUI.radiobutton1001.get_active() == True:                                   # Check if CPU tab is selected.
        ChartPlots.drawingarea1101.queue_draw()

        # Get system up time (sut) information
        with open("/proc/uptime") as reader:
            sut_read = float(reader.read().split(" ")[0].strip())
        sut_days = sut_read/60/60/24
        sut_days_int = int(sut_days)
        sut_hours = (sut_days -sut_days_int) * 24
        sut_hours_int = int(sut_hours)
        sut_minutes = (sut_hours - sut_hours_int) * 60
        sut_minutes_int = int(sut_minutes)
        sut_seconds = (sut_minutes - sut_minutes_int) * 60
        sut_seconds_int = int(sut_seconds)
        # Get current frequencies of all cores
        cpu_current_frequency_all_cores = []
        if os.path.isfile("/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq") is True:
            for cpu_core in logical_core_list_system_ordered:
                with open("/sys/devices/system/cpu/cpufreq/policy" + cpu_core + "/scaling_cur_freq") as reader:
                    cpu_current_frequency_all_cores.append(float(reader.read().strip()) / 1000)
        else:
            with open("/proc/cpuinfo") as reader:
                proc_cpuinfo_lines = reader.read().split("\n")
                for line in proc_cpuinfo_lines:
                    if line.startswith("cpu MHz"):
                        cpu_current_frequency_all_cores.append(float(line.split(":")[1].strip()))
        # Get number_of_total_threads and number_of_total_processes
        thread_count_list = []
        file_list = os.listdir("/proc/")                                                      # List all file in the "/proc/" directory
        for file in file_list:
            if file.isdigit():                                                                # Accept file name as process PID if file name is digit. Because there are also another files/folders in the "/proc/" directory.
                pid = file
                try:                                                                          # try-except is used in order to pass the loop without application error if a "FileNotFoundError" error is encountered when process is ended after process list is get.
                    with open("/proc/" + pid + "/status") as reader:
                        proc_status_output = reader.read()
                        thread_count_list.append(int(proc_status_output.split("\nThreads:")[1].split("\n")[0].strip()))    # Append number of threads of the process
                except FileNotFoundError:
                    pass
        number_of_total_processes = len(thread_count_list)
        number_of_total_threads = sum(thread_count_list)

        # Set and update CPU tab label texts by using information get
        PerformanceGUI.label1111.set_text(f'{number_of_total_processes} - {number_of_total_threads}')
        PerformanceGUI.label1112.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
        PerformanceGUI.label1103.set_text(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        PerformanceGUI.label1104.set_text(f'{cpu_current_frequency_all_cores[int(selected_cpu_core_number)]:.0f} MHz')


    # Update RAM tab data on the GUI
    if PerformanceGUI.radiobutton1002.get_active() == True:                                   # Check if RAM tab is selected.

        performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
        performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit
        global swap_percent

        ChartPlots.drawingarea1201.queue_draw()
        ChartPlots.drawingarea1202.queue_draw()

        # Get RAM usage values
        with open("/proc/meminfo") as reader:                                                 # Read total swap area and free swap area from /proc/meminfo file
            memory_info = reader.read().split("\n")
        for line in memory_info:
            if line.startswith("SwapTotal:"):
                swap_total = int(line.split()[1]) * 1024
            if line.startswith("SwapFree:"):
                swap_free = int(line.split()[1]) * 1024
        if swap_free != 0:                                                                    # Calculate values if swap memory exists.
            swap_used = swap_total - swap_free
            swap_percent = swap_used / swap_total * 100
        if swap_free == 0:                                                                    # Set values as "0" if swap memory does not exist.
            swap_used = 0
            swap_percent = 0

        # Set and update RAM tab label texts by using information get
        PerformanceGUI.label1203.set_text(f'{performance_data_unit_converter_func(ram_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)} ({ram_usage_percent[-1]:.0f} %)')
        PerformanceGUI.label1204.set_text(performance_data_unit_converter_func(ram_available, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
        PerformanceGUI.label1206.set_text(performance_data_unit_converter_func(ram_free, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
        PerformanceGUI.label1207.set_text(f'{swap_percent:.0f} %')
        PerformanceGUI.label1208.set_text(f'{performance_data_unit_converter_func(swap_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)}')
        PerformanceGUI.label1209.set_text(performance_data_unit_converter_func(swap_free, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
        PerformanceGUI.label1210.set_text(performance_data_unit_converter_func((swap_total), performance_ram_swap_data_unit, performance_ram_swap_data_precision))


    # Update Disk tab data on the GUI
    if PerformanceGUI.radiobutton1003.get_active() == True:                                   # Check if Disk tab is selected.

        performance_disk_speed_data_precision = Config.performance_disk_speed_data_precision
        performance_disk_usage_data_precision = Config.performance_disk_usage_data_precision
        performance_disk_speed_data_unit = Config.performance_disk_speed_data_unit
        performance_disk_usage_data_unit = Config.performance_disk_usage_data_unit

        ChartPlots.drawingarea1301.queue_draw()
        ChartPlots.drawingarea1302.queue_draw()

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            if os.path.isdir("/sys/class/block/" + disk_list[selected_disk_number]) == False:
                return
        except:
            return
        # Get disk_read_time, disk_write_time
        with open("/proc/diskstats") as reader:
            proc_diskstats_lines = reader.read().strip().split("\n")
            for line in proc_diskstats_lines:
                if line.split()[2].strip() == disk_list[selected_disk_number]:
                    disk_read_time = int(line.split()[6])
                    disk_write_time = int(line.split()[10])
        # Get disk_size, disk_available, disk_free, disk_used, disk_usage_percent
        performance_get_device_partition_model_name_mount_point_func()
        global disk_usage_percent
        if disk_mount_point != "":
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)                          # Values are calculated for filesystem size values (as df command does). lsblk command shows values of mass storage.
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_used = disk_size - disk_free
            #disk_usage_percent = disk_used / disk_size * 100                                 # Gives same result with "lsblk" command
            disk_usage_percent = disk_used / (disk_available + disk_used) * 100               # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values. This is real usage percent.
        if disk_mount_point == "":
            disk_size = _tr("[Not mounted]")
            disk_available = _tr("[Not mounted]")
            disk_free = _tr("[Not mounted]")
            disk_used = _tr("[Not mounted]")
            disk_usage_percent = 0

        # Set and update Disk tab label texts by using information get
        PerformanceGUI.label1303.set_text(f'{performance_data_unit_converter_func(disk_read_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
        PerformanceGUI.label1304.set_text(f'{performance_data_unit_converter_func(disk_write_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
        PerformanceGUI.label1305.set_text(f'{performance_time_unit_converter_func(disk_read_time)} ms')
        PerformanceGUI.label1306.set_text(f'{performance_time_unit_converter_func(disk_write_time)} ms')
        if disk_mount_point != "":
            PerformanceGUI.label1308.set_text(f'{disk_usage_percent:.0f} %')
        if disk_mount_point == "":
            PerformanceGUI.label1308.set_text("- %")
        PerformanceGUI.label1309.set_text(performance_data_unit_converter_func(disk_available, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
        PerformanceGUI.label1310.set_text(performance_data_unit_converter_func(disk_used, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
        PerformanceGUI.label1311.set_text(performance_data_unit_converter_func(disk_size, performance_disk_usage_data_unit, performance_disk_usage_data_precision))


    # Update Network tab data on the GUI
    if PerformanceGUI.radiobutton1004.get_active() == True:                                   # Check if Network tab is selected.

        performance_network_speed_data_precision = Config.performance_network_speed_data_precision
        performance_network_data_data_precision = Config.performance_network_data_data_precision
        performance_network_speed_data_unit = Config.performance_network_speed_data_unit
        performance_network_data_data_unit = Config.performance_network_data_data_unit

        ChartPlots.drawingarea1401.queue_draw()

        # Get network_card_connected
        with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/operstate") as reader:   # Get the information of if network card is connected by usng "/sys/class/net/" file.
            network_info = reader.read().strip()
            if network_info == "up":
                network_card_connected = _tr("Yes")
            elif network_info == "down":
                network_card_connected = _tr("No")
            elif network_info == "unknown":
                network_card_connected = _tr("Unknown")
            else:
                network_card_connected = network_info
        # Get network_ssid
        nmcli_output_lines = (subprocess.check_output("nmcli -get-values DEVICE,CONNECTION device status", shell=True).strip()).decode().split("\n")
        for line in nmcli_output_lines:
            line_splitted = line.split(":")
            if network_card_list[selected_network_card_number] == line_splitted[0]:
                network_ssid = line_splitted[1].strip()
                break
        if network_ssid == "":
            network_ssid = "-"
        # Get network_signal_strength
        network_signal_strength = ""
        if "wl" in network_card_list[selected_network_card_number] and network_card_connected == "Yes":
            with open("/proc/net/wireless") as reader:
                proc_net_wireless_output_lines = reader.read().strip().split("\n")
                for line in proc_net_wireless_output_lines:
                    line_splitted = line.split()
                    if network_card_list[selected_network_card_number] == line_splitted[0].split(":")[0]:
                        network_signal_strength = line_splitted[2].split(".")[0]              # "split(".")" is used in order to remove "." at the end of the signal value.
                        break
        if network_signal_strength == "":
            network_signal_strength = "-"

        # Set and update Network tab label texts by using information get
        PerformanceGUI.label1403.set_text(f'{performance_data_unit_converter_func(network_receive_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
        PerformanceGUI.label1404.set_text(f'{performance_data_unit_converter_func(network_send_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
        PerformanceGUI.label1405.set_text(performance_data_unit_converter_func(network_receive_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
        PerformanceGUI.label1406.set_text(performance_data_unit_converter_func(network_send_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
        PerformanceGUI.label1408.set_text(f'{network_card_connected} - {network_ssid}')
        PerformanceGUI.label1409.set_text(network_signal_strength)


    # Update GPU tab data on the GUI
    if PerformanceGUI.radiobutton1005.get_active() == True:                                   # Check if GPU tab is selected.

        global frame_list, fps_count, fps_count_list, frame_latency
        #glarea1501.queue_draw()
        fps = len(frame_list) / update_interval
        del fps_count[0]
        fps_count.append(fps)
        frame_latency = 1 / (fps + 0.0000001)
        frame_list = []

        ChartPlots.drawingarea1501.queue_draw()
        current_resolution_and_refresh_rate = (subprocess.check_output("xrandr | grep '*'", shell=True).strip()).decode().split('*')[0].split(' ')
        current_resolution_and_refresh_rate = [i for i in current_resolution_and_refresh_rate if i != '']


        # Set and update GPU tab label texts by using information get
        PerformanceGUI.label1503.set_text(f'{fps_count[-1]:.0f}')
        PerformanceGUI.label1504.set_text(f'{frame_latency:.2f} ms')
        PerformanceGUI.label1505.set_text(f'{current_resolution_and_refresh_rate[1]} Hz')
        PerformanceGUI.label1506.set_text(f'{current_resolution_and_refresh_rate[0]}')


# ----------------------------------- Performance - Foreground Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def performance_foreground_initial_initial_func():

    GLib.idle_add(performance_foreground_initial_func)


# ----------------------------------- Performance Foreground Loop Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def performance_foreground_loop_func():

    GLib.idle_add(performance_foreground_func)
    GLib.timeout_add(Config.update_interval * 1000, performance_foreground_loop_func)


# ----------------------------------- Performance Foreground Thread Run Function (starts execution of the threads) -----------------------------------
def performance_foreground_thread_run_func():

    global performance_foreground_initial_thread
    performance_foreground_initial_thread = Thread(target=performance_foreground_initial_initial_func, daemon=True)
    performance_foreground_initial_thread.start()
    performance_foreground_initial_thread.join()
    performance_foreground_thread = Thread(target=performance_foreground_loop_func, daemon=True)
    performance_foreground_thread.start()


# ----------------------------------- Performance - Get disk_model_name, parent_disk, disk_mount_point Values Function -----------------------------------
def performance_get_device_partition_model_name_mount_point_func():
    # Get disk_model_name, parent_disk, disk_mount_point values
    global disk_device_or_partition, disk_model_name, disk_mount_point
    # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
    try:
        if os.path.isdir("/sys/class/block/" + disk_list[selected_disk_number]) == False:
            return
    except:
        return
    if os.path.isdir("/sys/class/block/" + disk_list[selected_disk_number] + "/device"):      # Checking "DEVTYPE" information in "/sys/class/block/[DISKNAME]/uevent" causes getting wrong "parent-child disk" information for "loop" devices. Checking "/device" folder is a more secure way.
        disk_device_or_partition = _tr("disk")
        parent_disk = ""
        with open("/sys/class/block/" + disk_list[selected_disk_number] + "/device/model") as reader:
            disk_model_name = reader.read().strip()
    elif "loop" in disk_list[selected_disk_number]:
        disk_device_or_partition = _tr("disk")
        parent_disk = ""
        disk_model_name = "[Loop Device]"
    else:
        disk_device_or_partition = _tr("partition")
        parent_disk = disk_list[selected_disk_number].rstrip('0123456789')                    # Split string with numbers at the end of it.
        with open("/sys/class/block/" + parent_disk + "/device/model") as reader:
            disk_model_name = reader.read().strip()
    with open("/proc/mounts") as reader:
        proc_mounts_output_lines = reader.read().strip().split("\n")
        disk_mount_point = ""
        for line in proc_mounts_output_lines:
            if line.split()[0].strip() == ("/dev/" + disk_list[selected_disk_number]):
                disk_mount_point = line.split()[1].strip().replace("\\040", " ")              # Disk mount point is get with containing "\\040" characters if there are spaces in the name of the loop disk. ".replace("\\040", " ")" code is used in order to replace these characters with a space for avoidng errors.


# ----------------------------------- Performance - Define Time Unit Converter Variables Function (contains time unit variables) -----------------------------------
def performance_time_unit_converter_func(time):

    w_r_time_days = time / 24 / 60 / 60 / 1000
    w_r_time_days_int = int(w_r_time_days)
    w_r_time_hours = (w_r_time_days - w_r_time_days_int) * 24
    w_r_time_hours_int = int(w_r_time_hours)
    w_r_time_minutes = (w_r_time_hours - w_r_time_hours_int) * 60
    w_r_time_minutes_int = int(w_r_time_minutes)
    w_r_time_seconds = (w_r_time_minutes - w_r_time_minutes_int) * 60
    w_r_time_seconds_int = int(w_r_time_seconds)
    w_r_time_milliseconds = (w_r_time_seconds - w_r_time_seconds_int) * 1000
    w_r_time_milliseconds_int = int(w_r_time_milliseconds)
    
    if w_r_time_days_int != 0:
        return f'{w_r_time_days_int:02}:{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}.{w_r_time_seconds_int:02}:{w_r_time_milliseconds_int:03}'
    if w_r_time_days_int == 0:
        return f'{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}:{w_r_time_seconds_int:02}.{w_r_time_milliseconds_int:03}'


# ----------------------------------- Performance - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def performance_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain faster code run, because this function will be called very frequently.
    # For the details of the calculation, see "Data_unit_conversion.ods." document.
    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 1.04858E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Performance - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def performance_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit == 0 or unit == 8:
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
