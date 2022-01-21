#!/usr/bin/env python3

# ----------------------------------- Performance - Import Function -----------------------------------
def performance_import_func():

    global GLib, os

    import gi
    from gi.repository import GLib
    import os


    global Config
    import Config


# ----------------------------------- Performance - Set Selected CPU Core Function -----------------------------------
def performance_set_selected_cpu_core_func():

    # Set selected CPU core
    first_core = logical_core_list[0]
    global selected_cpu_core, selected_cpu_core_number
    if Config.selected_cpu_core in logical_core_list:
        selected_cpu_core = Config.selected_cpu_core
    if Config.selected_cpu_core not in logical_core_list:
        selected_cpu_core = first_core
    selected_cpu_core_number = logical_core_list_system_ordered.index(selected_cpu_core)


# ----------------------------------- Performance - Set Selected Disk Function -----------------------------------
def performance_set_selected_disk_func():

    # Set selected disk
    with open("/proc/mounts") as reader:
        proc_mounts_output_lines = reader.read().strip().split("\n")
    system_disk_list = []
    for line in proc_mounts_output_lines:
        line_split = line.split(" ", 2)
        if line_split[1].strip() == "/":
            disk = line_split[0].strip().split("/")[-1]
            if disk in disk_list:
                system_disk_list.append(disk)
                break
    if system_disk_list == []:                                                                # The code below this statement is used because system disk may not be detected by checking if mount point is "/" on some systems such as some ARM devices. "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
        with open("/proc/cmdline") as reader:
            proc_cmdline = reader.read()
        if "root=UUID=" in proc_cmdline:
            disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
            system_disk_list.append(os.path.realpath("/dev/disk/by-uuid/" + disk_uuid_partuuid).split("/")[-1].strip())
        if "root=PARTUUID=" in proc_cmdline:
            disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
            system_disk_list.append(os.path.realpath("/dev/disk/by-partuuid/" + disk_uuid_partuuid).split("/")[-1].strip())
    global selected_disk_number
    if Config.selected_disk in disk_list:
        selected_disk = Config.selected_disk
    if Config.selected_disk not in disk_list:
        if system_disk_list != []:
            selected_disk = system_disk_list[0]
        if system_disk_list == []:
            selected_disk = disk_list[0]
    selected_disk_number = disk_list_system_ordered.index(selected_disk)


# ----------------------------------- Performance - Set Selected Network Card Function -----------------------------------
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


# ----------------------------------- Performance - Background Initial Function -----------------------------------
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

    # Reset selected hardware if "remember_last_selected_hardware" prefrence is disabled by the user.
    if Config.remember_last_selected_hardware == 0:
        Config.selected_cpu_core = ""
        Config.selected_disk = ""
        Config.selected_network_card = ""
        Config.selected_gpu = ""

# ----------------------------------- Performance - Background Function (gets basic CPU, RAM, disk and network usage data in the background in order to assure uninterrupted data for charts) -----------------------------------
def performance_background_loop_func():

    global update_interval                                                                    # This value will be used multiple times and it is get from another module and defined as a global variable in this function in order to achieve lower CPU consumption.

    # Get logical_core_list, number_of_logical_cores
    global logical_core_list_system_ordered, logical_core_list, number_of_logical_cores       # "logical_core_list" list contains online CPU core numbers and ordering changes when online/offline CPU core changes are made. Last online-made core is listed as the last core.
    global cpu_time_all, cpu_time_load
    global cpu_time_all_prev, cpu_time_load_prev                                              # Make global previously defined variables, therefore Python could acces these variables faster (it directly searchs in globals()).
    logical_core_list_system_ordered = []                                                     # "logical_core_list_system_ordered" contains online CPU core numbers in the order of "/proc/stats" file content which is in "ascending" online core number order.
    with open("/proc/stat") as reader:                                                        # "/proc/stat" file contains online logical CPU core numbers (all cores without regarding CPU sockets, physical/logical cores) and CPU times since system boot.
        proc_stat_lines = reader.read().split("intr", 1)[0].strip().split("\n")[1:]           # Trimmed unneeded information in the file
    for line in proc_stat_lines:
        logical_core_list_system_ordered.append(line.split(" ", 1)[0])                        # Add CPU core names into a temporary list in ascending core number order. This list will be used with logical_core_list in order to track last online-made CPU core. This operations are performed in order to track CPU usage per core continuously even if CPU cores made online/offline.
    number_of_logical_cores = len(logical_core_list_system_ordered)
    logical_core_list_prev = logical_core_list[:]                                             # Get copy of the list. Otherwise, lists will be linked.
    for i, cpu_core in enumerate(logical_core_list_system_ordered):                           # Track the changes if CPU core is made online/offline
        if cpu_core not in logical_core_list:                                                 # Add new core number into logical_core_list if CPU core is made online. Also CPU time data related to online-made the core is appended into lists.
            logical_core_list.append(cpu_core)
            cpu_time = proc_stat_lines[i].split()
            cpu_time_all_prev.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))
            cpu_time_load_prev.append(cpu_time_all_prev[-1] - int(cpu_time[4]) - int(cpu_time[5]))
    for cpu_core in logical_core_list[:]:                                                     # Remove core number from logical_core_list if it is made offline. Also CPU time data related to offline-made the core is removed from lists.
        if cpu_core not in logical_core_list_system_ordered:
            del cpu_time_all_prev[logical_core_list.index(cpu_core)]
            del cpu_time_load_prev[logical_core_list.index(cpu_core)]
            logical_core_list.remove(cpu_core)
    if logical_core_list_prev != logical_core_list:
        performance_set_selected_cpu_core_func()
    # Get cpu_usage_percent_per_core, cpu_usage_percent_ave
    global cpu_usage_percent_per_core, cpu_usage_percent_ave
    cpu_time_all = []
    cpu_time_load = []
    cpu_usage_percent_per_core = []
    for i, cpu_core in enumerate(logical_core_list):                                          # Get CPU core times calculate CPU usage values and append usage values into lists in the core number order listed in logical_core_list.
        cpu_time = proc_stat_lines[logical_core_list_system_ordered.index(cpu_core)].split()
        cpu_time_all.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))    # All time since boot for the cpu core
        cpu_time_load.append(cpu_time_all[-1] - int(cpu_time[4]) - int(cpu_time[5]))          # Time elapsed during core processing for the core
        if cpu_time_all[-1] - cpu_time_all_prev[i] == 0:
            cpu_time_all[-1] = cpu_time_all[-1] + 1                                           # Append 1 CPU time (a negligible value) in order to avoid zeor division error in the first loop after application start or in the first loop of newly online-made CPU core. It is corrected in the next loop.
        cpu_usage_percent_per_core.append((cpu_time_load[-1] - cpu_time_load_prev[i]) / (cpu_time_all[-1] - cpu_time_all_prev[i]) * 100)    # Calculate CPU usage precent for the core (load time difference / all time difference *100). Time difference is calculated as "value in this loop - value from previous loop". CPU times difference interval should be higher than 0.1 seconds in order to achieve an accurate CPU usage percent value. For many systems CPU ticks 100 times in a second and this value could be get by using "os.sysconf("SC_CLK_TCK")". If measurement is made in a lower time interval, "0" CPU usage could be get.
    cpu_usage_percent_ave.append(sum(cpu_usage_percent_per_core) / number_of_logical_cores)   # Calculate average CPU usage for all logical cores (summation of CPU usage per core / number of logical cores)
    del cpu_usage_percent_ave[0]                                                              # Delete the first CPU usage percent value from the list in order to keep list lenght same. Because a new value is appended in every loop. This list is used for CPU usage percent graphic.        
    cpu_time_all_prev = list(cpu_time_all)                                                    # Use the values as "previous" data. This data will be used in the next loop for calculating time difference.
    cpu_time_load_prev = list(cpu_time_load)

    # Get ram_usage_percent
    global ram_usage_percent
    global ram_total, ram_free, ram_available, ram_used
    with open("/proc/meminfo") as reader:
        memory_info = reader.read()
    ram_total = int(memory_info.split("MemTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_free = int(memory_info.split("\nMemFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_available = int(memory_info.split("\nMemAvailable:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_used = ram_total - ram_available
    ram_usage_percent.append(ram_used / ram_total * 100)
    del ram_usage_percent[0]

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
            proc_diskstats_lines_filtered.append(line)                                        # Disk information of some disks (such a loop devices) exist in "/proc/diskstats" file even if these dvice are unmounted. "proc_diskstats_lines_filtered" list is used in order to use disk list without these remaining information.
    disk_list_prev = disk_list[:]
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
    for disk in reversed(disk_list[:]):
        if disk not in disk_list_system_ordered:
            del disk_read_data_prev[disk_list.index(disk)]
            del disk_write_data_prev[disk_list.index(disk)]
            del disk_read_speed[disk_list.index(disk)]
            del disk_write_speed[disk_list.index(disk)]
            disk_list.remove(disk)
    if disk_list_prev != disk_list:
        performance_set_selected_disk_func()
    # Get disk_read_speed, disk_write_speed
    disk_read_data = []
    disk_write_data = []
    for i, disk in enumerate(disk_list):
        disk_data = proc_diskstats_lines_filtered[disk_list_system_ordered.index(disk)].split()
        disk_read_data.append(int(disk_data[5]) * disk_sector_size)
        disk_write_data.append(int(disk_data[9]) * disk_sector_size)
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
        network_card_list_system_ordered.append(line.split(":", 1)[0].strip())
    network_card_list_prev = network_card_list[:]
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
    for network_card in reversed(network_card_list[:]):
        if network_card not in network_card_list_system_ordered:
            del network_receive_bytes_prev[network_card_list.index(network_card)]
            del network_send_bytes_prev[network_card_list.index(network_card)]
            del network_receive_speed[network_card_list.index(network_card)]
            del network_send_speed[network_card_list.index(network_card)]
            network_card_list.remove(network_card)
    if network_card_list_prev != network_card_list:
        performance_set_selected_network_card_func()
    # Get network_receive_speed, network_send_speed
    network_receive_bytes = []
    network_send_bytes = []
    for i, network_card in enumerate(network_card_list):
        network_data = proc_net_dev_lines[network_card_list_system_ordered.index(network_card)].split()
        network_receive_bytes.append(int(network_data[1]))
        network_send_bytes.append(int(network_data[9]))
        network_receive_speed[i].append((network_receive_bytes[-1] - network_receive_bytes_prev[i]) / update_interval)
        network_send_speed[i].append((network_send_bytes[-1] - network_send_bytes_prev[i]) / update_interval)
        del network_receive_speed[i][0]
        del network_send_speed[i][0]
    network_receive_bytes_prev = list(network_receive_bytes)
    network_send_bytes_prev = list(network_send_bytes)


# ----------------------------------- Performance - Background Run Function -----------------------------------
def performance_background_run_func():

    if 'update_interval' not in globals():
        global update_interval
        performance_background_initial_func()                                                 # Function is run directly without using "GLib.idle_add([function_name])" in order to avoid errors which are given if another threads (such as threads in CPU module) run before this function is finished.
    update_interval = Config.update_interval
    performance_background_loop_func()
    GLib.timeout_add(update_interval * 1000, performance_background_run_func)
