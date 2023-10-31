import os
import subprocess
import sys
import platform
import time
from datetime import datetime
import threading


# ***********************************************************************************************
#                                           Constants
# ***********************************************************************************************

# For many systems CPU ticks 100 times in a second.
# Wall clock time is get if CPU times are multiplied with this value.
number_of_clock_ticks = os.sysconf("SC_CLK_TCK")

# Memory page size is used for converting memory page values into byte values.
# It depends on architecture (also sometimes depends on machine model).
# Default value is 4096 Bytes (4 KiB) for most processors.
memory_page_size = os.sysconf("SC_PAGE_SIZE")

# Disk data from '/proc/diskstats' is multiplied by 512 in order to find values in the form of byte.
# Disk sector size for all disk devices could be found in '/sys/block/[disk device name such as sda]/queue/hw_sector_size'.
# Linux uses 512 value for all disks without regarding device real block size.
# source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121)
disk_sector_size = 512

# GPU Transfer rate (link speed) units are GT/s.
gpu_pci_express_version_dict = {"2.5": "PCI-Express 1.0",
                                "5.0": "PCI-Express 2.0",
                                "8.0": "PCI-Express 3.0",
                                "16.0": "PCI-Express 4.0",
                                "32.0": "PCI-Express 5.0",
                                "64.0": "PCI-Express 6.0",
                                "128.0": "PCI-Express 7.0"}

# The content of the file is updated about 50-60 times in a second. 
# 120 is used in order to get GPU load for AMD GPUs precisely.
amd_gpu_load_read_frequency = 1 / 120
amd_gpu_load_list = [0]

# This list is used in order to show full status of the process.
# For more information, see: "https://man7.org/linux/man-pages/man5/proc.5.html".
process_status_dict = {"R": "Running", "S": "Sleeping", "D": "Waiting", "I": "Idle",
                       "Z": "Zombie", "T": "Stopped", "t": "Tracing Stop", "X": "Dead",
                       "K": "Wakekill", "P": "Parked", "x": "Dead", "W": "Waking"}

supported_sensor_attributes = ["temp", "fan", "in", "curr", "power"]

# Define values for converting data units and set value precision.
"""
      ISO UNITs (as powers of 1000)        -             IEC UNITs (as powers of 1024)
Unit Name    Abbreviation     bytes        -       Unit Name    Abbreviation    bytes   
byte         B                1            -       byte         B               1
kilobyte     KB               1000         -       kibibyte     KiB             1024
megabyte     MB               1000^2       -       mebibyte     MiB             1024^2
gigabyte     GB               1000^3       -       gibibyte     GiB             1024^3
terabyte     TB               1000^4       -       tebibyte     TiB             1024^4
petabyte     PB               1000^5       -       pebibyte     PiB             1024^5

Unit Name    Abbreviation     bits         -       Unit Name    Abbreviation    bits    
bit          b                1            -       bit          b               1
kilobit      Kb               1000         -       kibibit      Kib             1024
megabit      Mb               1000^2       -       mebibit      Mib             1024^2
gigabit      Gb               1000^3       -       gibibit      Gib             1024^3
terabit      Tb               1000^4       -       tebibit      Tib             1024^4
petabit      Pb               1000^5       -       pebibit      Pib             1024^5

1 byte = 8 bits
"""
# Data unit options: 0: Bytes (ISO), 1: Bytes (IEC), 2: bits (ISO), 3: bits (IEC).
data_unit_list = [[0, "B", "B", "b", "b"], [1, "KiB", "KB", "Kib", "Kb"], [2, "MiB", "MB", "Mib", "Mb"],
                  [3, "GiB", "GB", "Gib", "Gb"], [4, "TiB", "TB", "Tib", "Tb"], [5, "PiB", "PB", "Pib", "Pb"]]

# For more information about computer chassis types, see: "https://www.dmtf.org/standards/SMBIOS"
# "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                               10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                               17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                               22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC", 25: "Multi-system chassis", 26: "Compact PCI", 27: "Advanced TCA",
                               28: "Blade", 29: "Blade Enclosure", 30: "Tablet", 31: "Convertible", 32: "Detachable", 33: "IoT Gateway", 34: "Embedded PC",
                               35: "Mini PC", 36: "Stick PC"}

# First values are process names of the DEs, second values are names of
# the DEs. Cinnamon dektop environment accepts both "X-Cinnamon" and
# "CINNAMON" names in the .desktop files.
supported_desktop_environments_dict = {"xfce4-session":"XFCE", "gnome-session-b":"GNOME", "cinnamon-session":"X-Cinnamon",
                                       "mate-session":"MATE", "plasmashell":"KDE", "lxqt-session":"LXQt", "lxsession":"LXDE",
                                       "budgie-panel":"Budgie", "dde-desktop":"Deepin"}

supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "budgie-wm", "openbox", "metacity", 
                                  "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome", "muffin"]
# First values are process names of the display managers, second values
# are names of the display managers.
supported_display_managers_dict = {"lightdm":"lightdm", "gdm":"gdm", "gdm3":"gdm3", "sddm":"sddm", "xdm":"xdm", "lxdm-binary":"lxdm"}                                                       

desktop_environment_version_command_dict = {"XFCE":["xfce4-panel", "--version"],
                                            "GNOME":["gnome-shell", "--version"],
                                            "zorin:GNOME":["gnome-shell", "--version"],
                                            "ubuntu:GNOME":["gnome-shell", "--version"],
                                            "X-Cinnamon":["cinnamon", "--version"],
                                            "CINNAMON":["cinnamon", "--version"],
                                            "MATE":["mate-about", "--version"],
                                            "KDE":["plasmashell", "--version"],
                                            "LXQt":["lxqt-about", "--version"],
                                            "Budgie":["budgie-desktop", "--version"],
                                            "Budgie:GNOME":["budgie-desktop", "--version"]}


# ***********************************************************************************************
#                                           Common
# ***********************************************************************************************

def _tr(text_for_translation):
    """
    This function is used for preventing errors if "set_translation_func" is not run.
    Text is not translated if this function is used.
    """

    return text_for_translation


def set_translation_func(translation_func):
    """
    Set "locale" translation function for translation text in function outputs.
    """

    global _tr
    _tr = translation_func


def get_environment_type():
    """
    Detect environment type (Flatpak or native).
    It will be used for accessing host OS commands if the application is run in Flatpak environment.
    """

    application_flatpak_id = os.getenv('FLATPAK_ID')

    if application_flatpak_id != None:
        environment_type = "flatpak"
    else:
        environment_type = "native"

    return environment_type


def get_init_system():
    """
    Get init system of the OS. Currently it is detected as "systemd" or "other".
    """

    try:
        if get_environment_type() == "flatpak":
            process_name = (subprocess.check_output(["flatpak-spawn", "--host", "cat", "/proc/1/comm"], shell=False)).decode().strip()
        else:
            with open("/proc/1/comm") as reader:
                process_name = reader.read().strip()
    except Exception:
        process_name = "-"

    if process_name == "systemd":
        init_system = "systemd"
    else:
        init_system = "other"

    return init_system


def get_number_of_logical_cores():
    """
    Get number of online logical cores.
    """

    try:
        # First try a faster way: using "SC_NPROCESSORS_ONLN" variable.
        number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")
    except ValueError:
        # As a second try, count by reading from "/proc/cpuinfo" file.
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    return number_of_logical_cores


def get_number_of_all_logical_cores():
    """
    Get number of all (online + offline) logical cores.
    """

    try:
        number_of_all_logical_cores = os.sysconf('SC_NPROCESSORS_CONF')
    except ValueError:
        number_of_all_logical_cores = "-"

    return number_of_all_logical_cores


def get_system_boot_time():
    """
    Get system boot time.
    """

    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")

    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())

    return system_boot_time


def get_number_of_processes():
    """
    Get number of processes.
    """

    if get_environment_type() == "flatpak":
        ls_proc_list = (subprocess.run(["flatpak-spawn", "--host", "ls", "/proc/"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split()
        processes_number_text = f'{len([filename for filename in ls_proc_list if filename.isdigit()])}'
    else:
        processes_number_text = f'{len([filename for filename in os.listdir("/proc/") if filename.isdigit()])}'

    return processes_number_text


def get_parsed_kernel_data_list(data_list):
    """
    Get Linux kernel data list after parsing it.
    For example: CPU core list may be get as "0", "0-4", "4,5", "0-3,7".
    They are get as list. For example: "0-3,7" > [0, 1, 2, 3, 7].
    """

    parsed_list = []
    data_list = data_list.split(",")
    for data_sub_list in data_list:
        if "-" in data_sub_list:
            list_range_start, list_range_end = data_sub_list.split("-")
            data_sub_list_processed = list(range(int(list_range_start), int(list_range_end)+1))
            parsed_list.extend(data_sub_list_processed)
        else:
            parsed_list.append(int(data_sub_list))

    return parsed_list


def get_device_vendor_model(modalias_output):
    """
    Get device vendor and model information.
    Hardware database of "udev" is used if "hwdata" database is not found. "hwdata" database is updated frequently.
    If hardware database of "hwdata" is found:
      - It is used for PCI, virtio and USB devices.
      - Hardware database of "udev" is used for SDIO devices. This database is copied into "database" folder of the application.
    """

    environment_type = get_environment_type()

    # Define hardware database file directories.
    udev_database = "no"
    pci_usb_hardware_database_dir = "/usr/share/hwdata/"
    if environment_type == "flatpak":
        pci_usb_hardware_database_dir = "/app/share/hwdata/"
    sdio_hardware_database_dir = os.path.dirname(os.path.realpath(__file__)) + "/../database/"

    # Define hardware database file directories for "udev" if "hwdata" is not installed.
    if os.path.isdir(pci_usb_hardware_database_dir) == False:
        udev_database = "yes"
        # Define "udev" hardware database file directory.
        udev_hardware_database_dir = "/usr/lib/udev/hwdb.d/"
        # Some older Linux distributions use "/lib/" instead of "/usr/lib/" but they are merged under "/usr/lib/" in newer versions.
        if os.path.isdir(udev_hardware_database_dir) == False:
            udev_hardware_database_dir = "/lib/udev/hwdb.d/"
        if environment_type == "flatpak":
            udev_hardware_database_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../etc/udev/hwdb.d/"

    """# Example modalias file contents for testing.
    modalias_output_list = [
    "usb:v0B95p1790d0100dcFFdscFFdp00icFFiscFFip00in00",
    "virtio:d00000001v00001AF4",
    "sdio:c00v02D0d4324",
    "pci:v000010DEd00000DF4sv00001043sd00001642bc03sc00i00",
    "pci:v0000168Cd0000002Bsv00001A3Bsd00002C37bc02sc80i00",
    "pci:v000010ECd00008168sv00001043sd000016D5bc02sc00i00",
    "pci:v00008086d00000116sv00001043sd00001642bc03sc00i00",
    "pci:v00001B85d00006018sv00001B85sd00006018bc01sc08i02",
    "pci:v0000144Dd0000A808sv0000144Dsd0000A801bc01sc08i02",
    "of:NgpuT<NULL>Cnvidia,tegra210-gm20bCnvidia,gm20b",
    "of:NgpuT(null)Cbrcm,bcm2835-vc4",
    "scsi:t-0x05",
    "scsi:t-0x00"]"""

    # Determine device subtype.
    device_subtype, device_alias = modalias_output.split(":", 1)

    # Get device vendor, model if device subtype is PCI.
    if device_subtype == "pci":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 8 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("d")
        last_index = first_index + 8 + 1
        device_model_id = device_alias[first_index:last_index]

        if udev_database == "no":
            # Get search texts
            search_text1 = "\n" + device_vendor_id[5:].lower() + "  "
            search_text2 = "\n\t" + device_model_id[5:].lower() + "  "

            # Read database file
            with open(pci_usb_hardware_database_dir + "pci.ids", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Get search texts
            search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file
            with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is virtio.
    elif device_subtype == "virtio":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 8 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("d")
        last_index = first_index + 8 + 1
        device_model_id = device_alias[first_index:last_index]
        # 1040 is added to device ID of virtio devices. 
        # For details: https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01.html
        device_model_id = "d0000" + str(int(device_model_id.strip("d")) + 1040)

        if udev_database == "no":
            # Get search texts
            search_text1 = "\n" + device_vendor_id[5:].lower() + "  "
            search_text2 = "\n\t" + device_model_id[5:].lower() + "  "

            # Read database file
            with open(pci_usb_hardware_database_dir + "pci.ids", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Get search texts
            search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file
            with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is USB.
    elif device_subtype == "usb":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 4 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("p")
        last_index = first_index + 4 + 1
        device_model_id = device_alias[first_index:last_index]

        if udev_database == "no":
            # Get search texts
            search_text1 = "\n" + device_vendor_id[1:].lower() + "  "
            search_text2 = "\n\t" + device_model_id[1:].lower() + "  "

            # Read database file
            with open(pci_usb_hardware_database_dir + "usb.ids", encoding="utf-8", errors="ignore") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Get search texts
            search_text1 = "usb:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "usb:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file
            with open(udev_hardware_database_dir + "20-usb-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is SDIO.
    elif device_subtype == "sdio":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 4 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("d")
        last_index = first_index + 4 + 1
        device_model_id = device_alias[first_index:last_index]

        # Get search texts
        search_text1 = "sdio:" + "c*" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "sdio:" + "c*" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        if udev_database == "no":
            # Read database file
            with open(sdio_hardware_database_dir + "/20-sdio-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Read database file
            with open(udev_hardware_database_dir + "20-sdio-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is of.
    elif device_subtype == "of":

        device_vendor_name = device_vendor_id = device_alias.split("C", 1)[-1].split("C", 1)[0].split(",")[0].title()
        device_model_name = device_model_id = device_alias.split("C", 1)[-1].split("C", 1)[0].split(",")[1].title()

    # Get device vendor, model if device subtype is SCSI or IDE.
    elif device_subtype in ["scsi", "ide"]:

        device_vendor_name = device_vendor_id = "[scsi_or_ide_disk]"
        device_model_name = device_model_id = "[scsi_or_ide_disk]"

    # Set device vendor, model if device subtype is not known so far.
    else:
        device_vendor_name = device_vendor_id = "Unknown"
        device_model_name = device_model_id = "Unknown"

    return device_vendor_name, device_model_name, device_vendor_id, device_model_id


def get_processes_information(process_list=[], processes_of_user="all", hide_kernel_threads=0, cpu_usage_divide_by_cores="yes", detail_level="medium", processes_data_dict_prev={}, system_boot_time=0, username_uid_dict={}):
    """
    Get process information of all/specified processes.
    """

    global number_of_clock_ticks, memory_page_size, process_status_dict

    # Get usernames and UIDs
    if username_uid_dict == {}:
        username_uid_dict = get_username_uid_dict()

    # Get current username which will be used for determining processes from only this user or other users.
    current_user_name = os.environ.get('USER')

    # Redefine core count division number if "Divide CPU usage by core count" option is disabled.
    if cpu_usage_divide_by_cores == "yes":
        core_count_division_number = get_number_of_logical_cores()
    else:
        core_count_division_number = 1

    # Get system boot time
    if system_boot_time == 0:
        system_boot_time = get_system_boot_time()

    # Read information from procfs files. "/proc/[PID]/smaps" file is not read for all processes. Because reading and
    # processing "/proc/[PID]/smaps" file data for all processes (about 250 processes) requires nearly 1 second on a 4 core CPU (i7-2630QM).
    cat_output_split, global_time, global_cpu_time_all = read_process_information(process_list, detail_level)

    # Define lists for getting process information from command output.
    processes_data_dict = {}
    if processes_data_dict_prev != {}:
        pid_list_prev = processes_data_dict_prev["pid_list"]
        ppid_list_prev = processes_data_dict_prev["ppid_list"]
        process_cpu_times_prev = processes_data_dict_prev["process_cpu_times"]
        disk_read_write_data_prev = processes_data_dict_prev["disk_read_write_data"]
        global_cpu_time_all_prev = processes_data_dict_prev["global_cpu_time_all"]
        global_time_prev = processes_data_dict_prev["global_time"]
    else:
        pid_list_prev = []
        ppid_list_prev = []
        process_cpu_times_prev = {}
        disk_read_write_data_prev = {}
    pid_list = []
    ppid_list = []
    username_list = []
    cmdline_list = []
    process_cpu_times = {}
    disk_read_write_data = {}

    # Get process information from command output.
    cat_output_split_iter = iter(cat_output_split)
    for process_data_stat_statm_status in cat_output_split_iter:
        # Also get second part of the data of the current process.
        if detail_level == "medium":
            process_data_io_cmdline = next(cat_output_split_iter)
        # Also get second and third part of the data of the current process.
        elif detail_level == "high":
            process_data_io_cmdline = next(cat_output_split_iter)
            process_data_smaps = next(cat_output_split_iter)

        # Get process information from "/proc/[PID]/stat" file
        # Skip to next loop if one of the stat, statm, status files is not read.
        try:
            stat_file, statm_file, status_file = process_data_stat_statm_status.split("\n", 2)
        except ValueError:
            continue
        if status_file.startswith("Name:") == False or "" in (stat_file, statm_file, status_file):
            continue
        stat_file_split = stat_file.split()

        # Get PID
        try:
            pid = int(stat_file_split[0])
        except IndexError:
            break

        ppid = int(stat_file_split[-49])
        status = process_status_dict[stat_file_split[-50]]
        # Get process CPU time in user mode (utime + stime)
        cpu_time_user = int(stat_file_split[-39])
        cpu_time_kernel = int(stat_file_split[-38])
        cpu_time = cpu_time_user + cpu_time_kernel
        # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_rss = int(stat_file_split[-29]) * memory_page_size
        # Get process VMS (virtual memory size) memory (this value is in bytes unit).
        memory_vms = int(stat_file_split[-30])
        # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting to wall clock time)
        start_time = (int(stat_file_split[-31]) / number_of_clock_ticks) + system_boot_time
        nice = int(stat_file_split[-34])
        number_of_threads = int(stat_file_split[-33])

        # Get process information from "/proc/[PID]/status" file
        name = status_file.split("Name:\t", 1)[1].split("\n", 1)[0]
        # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
        uid = int(status_file.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0])
        # There are 4 values in the Gid line and first one (real GID) is get from this file.
        gid = int(status_file.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0])

        # Get username
        try:
            username = username_uid_dict[uid]
        except KeyError:
            username = str(uid)

        # Skip to next process information if process information of current user is wanted
        # or kernel threads are not wanted.
        if (ppid == 2 and hide_kernel_threads == 1) or (username != current_user_name and processes_of_user == "current"):
            continue

        # Get process information from "/proc/[PID]/statm" file
        statm_file_split = statm_file.split()
        # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_shared = int(statm_file_split[2]) * memory_page_size
        # Get memory
        memory = memory_rss - memory_shared

        # Get process information from "/proc/[PID]/io" and "/proc/[PID]/cmdline" files
        if detail_level == "medium" or detail_level == "high":
            if process_data_io_cmdline.startswith("rchar") == True:
                try:
                    io_cmdline_files_split = process_data_io_cmdline.split("\n", 7)
                    cmdline_file = io_cmdline_files_split[-1]
                except ValueError:
                    io_cmdline_files_split = process_data_io_cmdline.split("\n")
                    cmdline_file = ""
                read_data = int(io_cmdline_files_split[4].split(":")[1])
                written_data = int(io_cmdline_files_split[5].split(":")[1])
            else:
                read_data = 0
                written_data = 0
                cmdline_file = process_data_io_cmdline
                io_cmdline_files_split = "-"

            # "cmdline" content may contain "\x00". They are replaced with " ". Otherwise, file content may be get as "".
            command_line = cmdline_file.replace("\x00", " ")
            if command_line == "":
                command_line = f'[{name}]'

        # Get process information from "/proc/[PID]/smaps" file and other files that are processed previously.
        if detail_level == "high":
            # Get process USS (unique set size) memory and swap memory and convert them to bytes
            process_data_smaps_split = process_data_smaps.split("\n")
            private_clean = 0
            private_dirty = 0
            memory_swap = 0
            for line in process_data_smaps_split:
                if "Private_Clean:" in line:
                    private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
                elif "Private_Dirty:" in line:
                    private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
                elif line.startswith("Swap:"):
                    memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
            memory_uss = (private_clean + private_dirty) * 1024
            memory_swap = memory_swap * 1024

            # Get other CPU time information (children_user, children_kernel, io_wait)
            cpu_time_children_user = int(stat_file_split[-37])
            cpu_time_children_kernel = int(stat_file_split[-36])
            cpu_time_io_wait = int(stat_file_split[-11])

            # Get numbers of CPU cores that process is run on.
            cpu_numbers = int(stat_file_split[-14])

            # Get UIDs (real, effective, saved)
            uids = status_file.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t")
            uid_real, uid_effective, uid_saved = int(uids[0]), int(uids[1]), int(uids[2])

            # Get GIDs (real, effective, saved)
            gids = status_file.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t")
            gid_real, gid_effective, gid_saved = int(gids[0]), int(gids[1]), int(gids[2])

            # Get number of context switches (voluntary and nonvoluntary)
            ctx_switches_voluntary = int(status_file.split("\nvoluntary_ctxt_switches:\t", 1)[1].split("\n", 1)[0])
            ctx_switches_nonvoluntary = int(status_file.split("\nnonvoluntary_ctxt_switches:\t", 1)[1].split("\n", 1)[0])

            # Get read count and write count
            if io_cmdline_files_split != "-":
                read_count = int(io_cmdline_files_split[2].split(":")[1])
                write_count = int(io_cmdline_files_split[3].split(":")[1])
            else:
                read_count = 0
                write_count = 0

            # Get CPU affinity
            cpu_affinity = status_file.split("\nCpus_allowed_list:\t", 1)[1].split("\n", 1)[0]

        # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters
        # (it is counted as 15). "/proc/[PID]/cmdline" file is read and it is split by the last "/" character 
        # (not all process cmdlines have this) in order to obtain full process name.
        if detail_level == "medium" or detail_level == "high":
            process_name_from_status = name
            if len(name) == 15:
                name = command_line.split("/")[-1].split(" ")[0]
                if name.startswith(process_name_from_status) == False:
                    name = command_line.split(" ")[0].split("/")[-1]
                    if name.startswith(process_name_from_status) == False:
                        name = process_name_from_status

        # Get CPU usage by using CPU times
        process_cpu_time = cpu_time
        process_cpu_times[pid] = process_cpu_time
        try:
            process_cpu_time_prev = process_cpu_times_prev[pid]
        except KeyError:
            # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
            process_cpu_time_prev = process_cpu_time
            # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
            global_cpu_time_all_prev = global_cpu_time_all - 1
        cpu_usage = (process_cpu_time - process_cpu_time_prev) / (global_cpu_time_all - global_cpu_time_all_prev) * 100 / core_count_division_number

        # Get disk read speed and disk write speed
        if detail_level == "medium" or detail_level == "high":
            disk_read_write_data[pid] = (read_data, written_data)
            try:
                read_data_prev, written_data_prev = disk_read_write_data_prev[pid]
                update_interval = global_time - global_time_prev
            except (KeyError, NameError) as e:
                # Make read_data_prev and written_data_prev equal to read_data for giving "0" disk read/write speed values
                # if this is first loop of the process
                read_data_prev = read_data
                written_data_prev = written_data
                update_interval = 1
            read_speed = (read_data - read_data_prev) / update_interval
            write_speed = (written_data - written_data_prev) / update_interval

        pid_list.append(pid)
        ppid_list.append(ppid)
        if detail_level == "medium" or detail_level == "high":
            cmdline_list.append(command_line)
        username_list.append(username)

        # Add process data to a sub-dictionary
        if detail_level == "low":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                }
        elif detail_level == "medium":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "read_data" : read_data,
                                "written_data" : written_data,
                                "read_speed" : read_speed,
                                "write_speed" : write_speed,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                "command_line" : command_line
                                }
        elif detail_level == "high":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "memory_uss" : memory_uss,
                                "memory_swap" : memory_swap,
                                "read_data" : read_data,
                                "written_data" : written_data,
                                "read_speed" : read_speed,
                                "write_speed" : write_speed,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                "command_line" : command_line,
                                "memory_uss": memory_uss,
                                "memory_swap": memory_swap,
                                "cpu_time_user": cpu_time_user,
                                "cpu_time_kernel": cpu_time_kernel,
                                "cpu_time_children_user": cpu_time_children_user,
                                "cpu_time_children_kernel": cpu_time_children_kernel,
                                "cpu_time_io_wait": cpu_time_io_wait,
                                "cpu_numbers": cpu_numbers,
                                "uid_real" : uid_real,
                                "uid_effective" : uid_effective,
                                "uid_saved" : uid_saved,
                                "gid_real" : gid_real,
                                "gid_effective" : gid_effective,
                                "gid_saved" : gid_saved,
                                "ctx_switches_voluntary": ctx_switches_voluntary,
                                "ctx_switches_nonvoluntary": ctx_switches_nonvoluntary,
                                "read_count": read_count,
                                "write_count": write_count,
                                "cpu_affinity": cpu_affinity
                                }

        # Add process sub-dictionary to dictionary
        processes_data_dict[pid] = process_data_dict

    # Add process related lists and variables for returning them for using them (for using some them as previous data in the next loop).
    processes_data_dict["pid_list"] = pid_list
    processes_data_dict["ppid_list"] = ppid_list
    processes_data_dict["username_list"] = username_list
    processes_data_dict["cmdline_list"] = cmdline_list
    processes_data_dict["process_cpu_times"] = process_cpu_times
    processes_data_dict["disk_read_write_data"] = disk_read_write_data
    processes_data_dict["global_cpu_time_all"] = global_cpu_time_all
    processes_data_dict["global_time"] = global_time

    return processes_data_dict


def read_process_information(process_list, detail_level="medium"):
    """
    Read information from procfs files.
    """

    # Get environment type
    environment_type = get_environment_type()

    # Get process PIDs
    if process_list == []:
        command_list = ["ls", "/proc/"]
        if environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        pid_list = []
        for pid in ls_output.split():
            if pid.isdigit() == True:
                pid_list.append(pid)
        pid_list = sorted(pid_list, key=int)
    else:
        pid_list = process_list

    # Get process information from procfs files. "/proc/version" file content is used as separator text.
    command_list = ["env", "LANG=C", "cat"]
    command_list.append('/proc/version')
    if environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    if detail_level == "low":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version'
                                ))
    elif detail_level == "medium":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version',
                                f'/proc/{pid}/io',
                                f'/proc/{pid}/cmdline',
                                '/proc/version'
                                ))
    elif detail_level == "high":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version',
                                f'/proc/{pid}/io',
                                f'/proc/{pid}/cmdline',
                                '/proc/version',
                                f'/proc/{pid}/smaps',
                                '/proc/version'
                                ))
    # Get time just before "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_before = time.time()
    #cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)).stdout.strip()
    cat_output = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    # Get time just after "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_after = time.time()
    # Calculate average values of "global_time" and "global_cpu_time_all".
    global_time = (time_before + time_after) / 2
    global_cpu_time_all = global_time * number_of_clock_ticks
    try:
        cat_output = cat_output.decode().strip()
    # Prevent errors if "cmdline" file contains characters that can not be decoded.
    except UnicodeDecodeError:
        cat_output = cat_output.decode("utf-8", "ignore").strip()

    # Get separator text
    separator_text = cat_output.split("\n", 1)[0]

    cat_output_split = cat_output.split(separator_text + "\n")
    # Delete first empty element
    del cat_output_split[0]

    return cat_output_split, global_time, global_cpu_time_all


def data_unit_converter(data_type, data_type_option, data, unit, precision):
    """
    Convert data units and set value precision (called from several modules).
    """

    global data_unit_list
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


# ***********************************************************************************************
#                                           Performance
# ***********************************************************************************************

def get_cpu_times():
    """
    Get CPU times for all cores (first value).
    '/proc/stat' file contains online logical CPU core names (without regarding CPU sockets) and CPU times (unit is jiffies).
    """

    # Read CPU times and remove first line (summation for all cores)
    with open("/proc/stat") as reader:
        proc_stat_lines = reader.read().split("intr", 1)[0].strip().split("\n")[1:]

    # Get CPU times
    cpu_times = {}
    for line in proc_stat_lines:
        line_split = line.split()
        cpu_core = line_split[0]
        user = int(line_split[1])
        nice = int(line_split[2])
        system = int(line_split[3])
        idle = int(line_split[4])
        iowait = int(line_split[5])
        irq = int(line_split[6])
        softirq = int(line_split[7])
        steal = int(line_split[8])
        guest = int(line_split[9])
        guest_nice = int(line_split[10])
        cpu_time_all = user + nice + system + idle + iowait + irq + softirq + steal + guest
        cpu_time_load = cpu_time_all - idle - iowait
        cpu_times[cpu_core] = {"load": cpu_time_load, "all": cpu_time_all}

    return cpu_times


def get_memory_info():
    """
    Get memory (RAM and swap) values.
    Values in '/proc/meminfo' file are in KiB unit.
    """

    # Read memory information
    with open("/proc/meminfo") as reader:
        proc_meminfo_output = reader.read()

    # Get memory (RAM) information
    ram_total = int(proc_meminfo_output.split("MemTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_free = int(proc_meminfo_output.split("\nMemFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_available = int(proc_meminfo_output.split("\nMemAvailable:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_cached = int(proc_meminfo_output.split("\nCached:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_used = ram_total - ram_available
    ram_used_percent = ram_used / ram_total * 100

    # Get memory (swap) information
    swap_total = int(proc_meminfo_output.split("\nSwapTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    swap_free = int(proc_meminfo_output.split("\nSwapFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    swap_cached = int(proc_meminfo_output.split("\nSwapCached:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    # Calculate values if swap memory exists.
    if swap_free != 0:
        swap_used = swap_total - swap_free
        swap_used_percent = swap_used / swap_total * 100
    # Set values as "0" if swap memory does not exist.
    else:
        swap_used = 0
        swap_used_percent = 0

    memory_info = {"ram_total": ram_total, "ram_free": ram_free, "ram_available": ram_available, "ram_cached": ram_cached,
                   "ram_used": ram_used, "ram_used_percent": ram_used_percent, "swap_total": swap_total,
                   "swap_free": swap_free, "swap_used": swap_used, "swap_used_percent": swap_used_percent,
                   "swap_cached": swap_cached}

    return memory_info


def get_disk_io():
    """
    Get disk read bytes and write bytes.
    '/proc/partitions' contains current disk list.
    '/proc/diskstats' contains all disks and disk io information since system start.
    """

    # Get disk list
    # Read disk information and remove first 2 lines (header information and spaces)
    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().strip().split("\n")[2:]

    # Get disk list
    _disk_list = []
    for line in proc_partitions_lines:
        _disk_list.append(line.split()[3].strip())

    # Read disk IO information
    with open("/proc/diskstats") as reader:
        proc_diskstats_lines = reader.read().strip().split("\n")

    # Get disk IO information
    disk_io = {}
    for line in proc_diskstats_lines:
        line_split = line.split()
        disk_name = line_split[2]
        if disk_name not in _disk_list:
            continue
        read_bytes = int(line_split[5]) * disk_sector_size
        write_bytes = int(line_split[9]) * disk_sector_size
        disk_io[disk_name] = {"read_bytes": read_bytes, "write_bytes": write_bytes}

    return disk_io


def get_network_io():
    """
    Get network card download bytes, upload bytes.
    """

    # Read network card IO information
    network_card_list = []
    with open("/proc/net/dev") as reader:
        proc_net_dev_lines = reader.read().strip().split("\n")[2:]

    # Get network card IO information
    network_io = {}
    for line in proc_net_dev_lines:
        line_split = line.split()
        network_card = line_split[0].split(":")[0]
        download_bytes = int(line_split[1])
        upload_bytes = int(line_split[9])
        network_io[network_card] = {"download_bytes": download_bytes, "upload_bytes": upload_bytes}

    return network_io


def get_cpu_memory_disk_network_usages(chart_data_history, system_performance_data_dict_prev={}):
    """
    Get system-wide CPU usage percentages per-core CPU usage percentage average, memory-RAM, memory-swap,
    disk read speed, disk write speed, network download speed, network upload speed.
    """

    # Define lists for getting performance information
    system_performance_data_dict = {}
    if system_performance_data_dict_prev != {}:

        # Define previous and initial values for CPU usage percentage
        logical_core_list_prev = system_performance_data_dict_prev["logical_core_list"]
        cpu_times_prev = system_performance_data_dict_prev["cpu_times"]
        cpu_usage_percent_per_core = system_performance_data_dict_prev["cpu_usage_percent_per_core"]
        cpu_usage_percent_ave = system_performance_data_dict_prev["cpu_usage_percent_ave"]
        cpu_usage_percent_ave = system_performance_data_dict_prev["cpu_usage_percent_ave"]

        # Define previous and initial values for RAM usage percentage and swap usage percentage
        ram_usage_percent = system_performance_data_dict_prev["ram_usage_percent"]
        swap_usage_percent = system_performance_data_dict_prev["swap_usage_percent"]

        # Define previous and initial values for disk read speed and write speed
        disk_list_prev = system_performance_data_dict_prev["disk_list"]
        disk_io_prev = system_performance_data_dict_prev["disk_io"]
        disk_read_speed = system_performance_data_dict_prev["disk_read_speed"]
        disk_write_speed = system_performance_data_dict_prev["disk_write_speed"]

        # Define previous and initial values for network receive speed and network send speed
        network_card_list_prev = system_performance_data_dict_prev["network_card_list"]
        network_io_prev = system_performance_data_dict_prev["network_io"]
        network_receive_speed = system_performance_data_dict_prev["network_receive_speed"]
        network_send_speed = system_performance_data_dict_prev["network_send_speed"]

        # Define previous value for time
        get_time_prev = system_performance_data_dict_prev["get_time"]

    else:

        # Define previous and initial values for CPU usage percentage
        logical_core_list_prev = []
        cpu_times_prev = {}
        cpu_usage_percent_per_core = {}
        cpu_usage_percent_ave = {}
        cpu_usage_percent_ave = [0] * chart_data_history

        # Define previous and initial values for RAM usage percentage and swap usage percentage
        ram_usage_percent = [0] * chart_data_history
        swap_usage_percent = [0] * chart_data_history

        # Define previous and initial values for disk read speed and write speed
        disk_list_prev = []
        disk_io_prev = {}
        disk_read_speed = {}
        disk_write_speed = {}

        # Define previous and initial values for network receive speed and network send speed
        network_card_list_prev = []
        network_io_prev = {}
        network_receive_speed = {}
        network_send_speed = {}

        # Define previous value for time
        get_time_prev = time.time()

    # Get CPU usage percentage per-core
    cpu_times = get_cpu_times()
    logical_core_list = list(cpu_times.keys())
    for core in logical_core_list:
        if core not in logical_core_list_prev:
            cpu_usage_percent_per_core[core] = [0] * chart_data_history
        else:
            cpu_time_load_difference = cpu_times[core]["load"] - cpu_times_prev[core]["load"]
            cpu_time_all_difference = cpu_times[core]["all"] - cpu_times_prev[core]["all"]
            # Prevent errors if there is no time change for the core
            if cpu_time_all_difference == 0:
                _cpu_usage_percent_core = 0
            else:
                _cpu_usage_percent_core = cpu_time_load_difference / cpu_time_all_difference * 100
            cpu_usage_percent_per_core[core].append(_cpu_usage_percent_core)
            del cpu_usage_percent_per_core[core][0]
    for core in logical_core_list_prev:
        if core not in logical_core_list:
            cpu_usage_percent_per_core[core] = [0] * chart_data_history
    # Get average CPU usage percentage
    _cpu_usage_percent_ave = 0
    for core in logical_core_list:
        _cpu_usage_percent_ave = _cpu_usage_percent_ave + cpu_usage_percent_per_core[core][-1]
    number_of_logical_cores = len(logical_core_list)
    cpu_usage_percent_ave.append(_cpu_usage_percent_ave / number_of_logical_cores)
    del cpu_usage_percent_ave[0]
    # Set selected CPU core
    if logical_core_list_prev != logical_core_list:
        system_performance_data_dict["logical_core_list_changed"] = "yes"
    else:
        system_performance_data_dict["logical_core_list_changed"] = "no"

    system_performance_data_dict["logical_core_list"] = logical_core_list
    system_performance_data_dict["cpu_times"] = cpu_times
    system_performance_data_dict["cpu_usage_percent_per_core"] = cpu_usage_percent_per_core
    system_performance_data_dict["cpu_usage_percent_ave"] = cpu_usage_percent_ave

    # Get RAM usage percentage
    memory_info = get_memory_info()
    ram_used_percent = memory_info["ram_used_percent"]
    ram_usage_percent.append(ram_used_percent)
    del ram_usage_percent[0]
    # Get swap usage percentage
    swap_used_percent = memory_info["swap_used_percent"]
    swap_usage_percent.append(swap_used_percent)
    del swap_usage_percent[0]

    system_performance_data_dict["ram_usage_percent"] = ram_usage_percent
    system_performance_data_dict["swap_usage_percent"] = swap_usage_percent

    # Get time for calculating disk and network speeds
    get_time = time.time()

    system_performance_data_dict["get_time"] = get_time

    # Get disk read speed and write speed
    disk_io = get_disk_io()
    disk_list = list(disk_io.keys())
    for disk in disk_list:
        if disk not in disk_list_prev:
            disk_read_speed[disk] = [0] * chart_data_history
            disk_write_speed[disk] = [0] * chart_data_history
        else:
            disk_read_speed_difference = disk_io[disk]["read_bytes"] - disk_io_prev[disk]["read_bytes"]
            disk_write_speed_difference = disk_io[disk]["write_bytes"] - disk_io_prev[disk]["write_bytes"]
            _disk_read_speed = disk_read_speed_difference / (get_time - get_time_prev)
            _disk_write_speed = disk_write_speed_difference / (get_time - get_time_prev)
            disk_read_speed[disk].append(_disk_read_speed)
            del disk_read_speed[disk][0]
            disk_write_speed[disk].append(_disk_write_speed)
            del disk_write_speed[disk][0]
    for disk in disk_list_prev:
        if disk not in disk_list:
            disk_read_speed[disk] = [0] * chart_data_history
            disk_write_speed[disk] = [0] * chart_data_history
    # Set selected disk
    if disk_list_prev != disk_list:
        system_performance_data_dict["disk_list_changed"] = "yes"
    else:
        system_performance_data_dict["disk_list_changed"] = "no"

    system_performance_data_dict["disk_list"] = disk_list
    system_performance_data_dict["disk_io"] = disk_io
    system_performance_data_dict["disk_read_speed"] = disk_read_speed
    system_performance_data_dict["disk_write_speed"] = disk_write_speed

    # Get network download speed and upload speed
    network_io = get_network_io()
    network_card_list = list(network_io.keys())
    for network_card in network_card_list:
        if network_card not in network_card_list_prev:
            network_receive_speed[network_card] = [0] * chart_data_history
            network_send_speed[network_card] = [0] * chart_data_history
        else:
            network_receive_speed_difference = network_io[network_card]["download_bytes"] - network_io_prev[network_card]["download_bytes"]
            network_send_speed_difference = network_io[network_card]["upload_bytes"] - network_io_prev[network_card]["upload_bytes"]
            _network_receive_speed = network_receive_speed_difference / (get_time - get_time_prev)
            _network_send_speed = network_send_speed_difference / (get_time - get_time_prev)
            network_receive_speed[network_card].append(_network_receive_speed)
            del network_receive_speed[network_card][0]
            network_send_speed[network_card].append(_network_send_speed)
            del network_send_speed[network_card][0]
    for network_card in network_card_list_prev:
        if network_card not in network_card_list:
            network_receive_speed[network_card] = [0] * chart_data_history
            network_send_speed[network_card] = [0] * chart_data_history
    # Set selected network card
    if network_card_list_prev != network_card_list:
        system_performance_data_dict["network_card_list_changed"] = "yes"
    else:
        system_performance_data_dict["network_card_list_changed"] = "no"

    system_performance_data_dict["network_card_list"] = network_card_list
    system_performance_data_dict["network_io"] = network_io
    system_performance_data_dict["network_receive_speed"] = network_receive_speed
    system_performance_data_dict["network_send_speed"] = network_send_speed

    return system_performance_data_dict


def set_selected_cpu_core(config_selected_cpu_core, logical_core_list):
    """
    Set selected CPU core.
    """

    if config_selected_cpu_core in logical_core_list:
        selected_cpu_core = config_selected_cpu_core
    else:
        first_core = logical_core_list[0]
        selected_cpu_core = first_core

    return selected_cpu_core


def set_selected_disk(config_selected_disk, disk_list):
    """
    Set selected disk.
    """

    # Set selected disk
    with open("/proc/mounts") as reader:
        proc_mounts_output = reader.read().strip()
    # Get "/proc/mounts" file content if there are encrypted disks and environment type is Flatpak.
    # Because, information line for the encrypted disk may not contain mountpoint as "/" in this case.
    # Additionally, there may be more lines that contain encrypted disk name in this file.
    if "/dev/mapper/" in proc_mounts_output:
        if get_environment_type() == "flatpak":
            proc_mounts_output = (subprocess.check_output(["flatpak-spawn", "--host", "cat", "/proc/mounts"], shell=False)).decode().strip()
    proc_mounts_output_lines = proc_mounts_output.split("\n")
    system_disk_list = []
    for line in proc_mounts_output_lines:
        line_split = line.split(" ", 2)
        if line_split[1].strip() == "/":
            disk_full_name = line_split[0]
            # While disk mountpoint is "/", disk full name may be "tmpfs" if there are encrypted disks and environment type is Flatpak.
            if disk_full_name == "tmpfs":
                continue
            disk = disk_full_name.strip().split("/")[-1]
            # Get disk "/proc/partitions" name if it is an encrypted disk.
            if disk_full_name.startswith("/dev/mapper/") == True:
                encrypted_disk_name = disk_full_name.split("/dev/mapper/")[-1]
                if os.path.isdir("/dev/mapper/" + encrypted_disk_name) != True:
                    disk_real_path = os.path.realpath("/dev/mapper/" + encrypted_disk_name)
                    disk_proc_name = disk_real_path.split("/")[-1]
                    disk = disk_proc_name
            # "/dev/root" disk is not listed in "/proc/partitions" file.
            if disk in disk_list:
                system_disk_list.append(disk)
                break
    # Detect system disk by checking if mount point is "/" on some systems such as some ARM devices.
    # "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
    if system_disk_list == []:
        with open("/proc/cmdline") as reader:
            proc_cmdline = reader.read()
        if "root=UUID=" in proc_cmdline:
            disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
            system_disk_list.append(os.path.realpath(f'/dev/disk/by-uuid/{disk_uuid_partuuid}').split("/")[-1].strip())
        elif "root=PARTUUID=" in proc_cmdline:
            disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
            system_disk_list.append(os.path.realpath(f'/dev/disk/by-partuuid/{disk_uuid_partuuid}').split("/")[-1].strip())

    if config_selected_disk in disk_list:
        selected_disk = config_selected_disk
    else:
        if system_disk_list != []:
            selected_disk = system_disk_list[0]
        else:
            selected_disk = disk_list[0]
            # Try to not to set selected disk a loop, ram, zram disk in order to avoid errors
            # if "hide_loop_ramdisk_zram_disks" option is enabled and performance data of all disks are plotted
            # at the same time. loop device may be the first disk on some systems if they are run without installation.
            for disk in disk_list:
                if disk.startswith("loop") == False and disk.startswith("ram") == False and disk.startswith("zram") == False:
                    selected_disk = disk
                    break

    return selected_disk, system_disk_list


def set_selected_network_card(config_selected_network_card, network_card_list):
    """
    Set selected network card.
    """

    # Set selected network card
    connected_network_card_list = []
    for network_card in network_card_list:
        with open(f'/sys/class/net/{network_card}/operstate') as reader:
            sys_class_net_output = reader.read().strip()
        if sys_class_net_output == "up":
            connected_network_card_list.append(network_card)

    # Avoid errors if there is no any network card that connected.
    if connected_network_card_list != []:
        selected_network_card = connected_network_card_list[0]
    else:
        selected_network_card = network_card_list[0]
    # "" is predefined network card name before release of the software. This statement is used
    # in order to avoid error, if no network card selection is made since first run of the software.
    if config_selected_network_card == "":
        selected_network_card = selected_network_card
    if config_selected_network_card in network_card_list:
        selected_network_card = config_selected_network_card
    else:
        selected_network_card = selected_network_card

    return selected_network_card, connected_network_card_list


# ***********************************************************************************************
#                                           CPU
# ***********************************************************************************************

def get_cpu_core_min_max_frequency(selected_cpu_core):
    """
    Get minimum and maximum frequencies of the CPU core.
    """

    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_max_freq") as reader:
            cpu_core_max_frequency = float(reader.read().strip()) / 1000000
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_min_freq") as reader:
            cpu_core_min_frequency = float(reader.read().strip()) / 1000000
    except FileNotFoundError:
        cpu_core_max_frequency = "-"
        cpu_core_min_frequency = "-"

    return cpu_core_min_frequency, cpu_core_max_frequency


def get_cpu_core_l1_l2_l3_cache(selected_cpu_core):
    """
    Get L1i, L1d, L2, L3 cache memory values of the CPU core.
    """

    # Get l1d cache
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/type") as reader:
            cache_type = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "1" and cache_type == "Data":
            cpu_core_l1d_cache = int(cache_size.strip("K"))
    except FileNotFoundError:
        cpu_core_l1d_cache = "-"

    # Get li cache
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/type") as reader:
            cache_type = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "1" and cache_type == "Instruction":
            cpu_core_l1i_cache = int(cache_size.strip("K"))
    except FileNotFoundError:
        cpu_core_l1i_cache = "-"

    # Get l2 cache
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "2":
            cpu_core_l2_cache = int(cache_size.strip("K"))
    except FileNotFoundError:
        cpu_core_l2_cache = "-"

    # Get l3 cache
    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/size") as reader:
            cache_size = reader.read().strip()
        if cache_level == "3":
            cpu_core_l3_cache = int(cache_size.strip("K"))
    except FileNotFoundError:
        cpu_core_l3_cache = "-"

    if cpu_core_l1d_cache != "-":
        cpu_core_l1d_cache = convert_cpu_cache_data_unit(cpu_core_l1d_cache)
    if cpu_core_l1i_cache != "-":
        cpu_core_l1i_cache = convert_cpu_cache_data_unit(cpu_core_l1i_cache)
    if cpu_core_l2_cache != "-":
        cpu_core_l2_cache = convert_cpu_cache_data_unit(cpu_core_l2_cache)
    if cpu_core_l3_cache != "-":
        cpu_core_l3_cache = convert_cpu_cache_data_unit(cpu_core_l3_cache)

    return cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache


def get_cpu_socket_l1_l2_l3_cache(selected_cpu_core):
    """
    Get L1i, L1d, L2, L3 cache memory values of the CPU socket of the selected CPU core.
    """

    # Get CPU core - CPU socket dictionary.
    with open("/proc/cpuinfo") as reader:
        proc_cpuinfo = reader.read()

    # Get CPU core - CPU socket dictionary for x86_64 architecture.
    if "physical id" in proc_cpuinfo:
        proc_cpuinfo_core_line_blocks = proc_cpuinfo.split("\n\n")

        cpu_core_socket_dict = {}
        for core_line_block in proc_cpuinfo_core_line_blocks:
            core_line_block_lines = core_line_block.split("\n")
            for line in core_line_block_lines:
                if line.startswith("processor\t:") == True:
                    cpu_core_number = line.split(":")[-1].strip()
                if line.startswith("physical id\t:") == True:
                    cpu_socket_number = line.split(":")[-1].strip()
            cpu_core_socket_dict[cpu_core_number] = cpu_socket_number

        # Get CPU cores of CPU socket that contains selected CPU core.
        selected_cpu_core_socket = cpu_core_socket_dict[selected_cpu_core.strip("cpu")]
        selected_cpu_core_socket_core_list = []
        for cpu_core in sorted(list(cpu_core_socket_dict.keys())):
            if cpu_core_socket_dict[cpu_core] == selected_cpu_core_socket:
                selected_cpu_core_socket_core_list.append("cpu" + cpu_core)

    # Get CPU core - CPU socket dictionary for ARM architecture.
    else:
        number_of_logical_cores = get_number_of_logical_cores()
        selected_cpu_core_socket_core_list = []
        for core_number in list(range(number_of_logical_cores)):
            selected_cpu_core_socket_core_list.append("cpu" + str(core_number))

    # Get CPU core cache values
    socket_cores_cache_dict = {}
    cache_index_list = ["0", "1", "2", "3"]
    for cpu_core in selected_cpu_core_socket_core_list:
        core_caches_dict = {}
        for cache_index in cache_index_list:
            core_cache_dict = get_core_cache_dict(cpu_core, cache_index)
            cache_level = core_cache_dict["cache_level"]
            core_caches_dict[cache_level] = dict(core_cache_dict)
        socket_cores_cache_dict[cpu_core] = core_caches_dict


    cpu_socket_l1d_cache = get_cpu_socket_specific_cache(socket_cores_cache_dict, "L1d")
    cpu_socket_l1i_cache = get_cpu_socket_specific_cache(socket_cores_cache_dict, "L1i")
    cpu_socket_l2_cache = get_cpu_socket_specific_cache(socket_cores_cache_dict, "L2")
    cpu_socket_l3_cache = get_cpu_socket_specific_cache(socket_cores_cache_dict, "L3")

    return cpu_socket_l1d_cache, cpu_socket_l1i_cache, cpu_socket_l2_cache, cpu_socket_l3_cache


def get_core_cache_dict(cpu_core, cache_index):
    """
    Get cache size, type, and level of the CPU core.
    """

    try:
        with open("/sys/devices/system/cpu/" + cpu_core + "/cache/index" + cache_index + "/level") as reader:
            cache_level = reader.read().strip()
        with open("/sys/devices/system/cpu/" + cpu_core + "/cache/index" + cache_index + "/type") as reader:
            cache_type = reader.read().strip()
        with open("/sys/devices/system/cpu/" + cpu_core + "/cache/index" + cache_index + "/size") as reader:
            cache_size = reader.read().strip()
        with open("/sys/devices/system/cpu/" + cpu_core + "/cache/index" + cache_index + "/shared_cpu_list") as reader:
            cache_shared_cpu_list = reader.read().strip()
    except FileNotFoundError:
        cache_level = "-"
        cache_type = "-"
        cache_size = "-"
        cache_shared_cpu_list = "-"

    if cache_level == "1" and cache_type == "Data":
        cache_level = "L1d"
    elif cache_level == "1" and cache_type == "Instruction":
        cache_level = "L1i"
    elif cache_level == "2":
        cache_level = "L2"
    elif cache_level == "3":
        cache_level = "L3"

    if cache_shared_cpu_list != "-":
        cache_shared_cpu_list = get_parsed_kernel_data_list(cache_shared_cpu_list)

    core_cache_dict = {
                       "cache_level" : cache_level,
                       "cache_type" : cache_type,
                       "cache_size" : cache_size,
                       "cache_shared_cpu_list" : cache_shared_cpu_list
                       }

    return core_cache_dict


def get_cpu_socket_specific_cache(socket_cores_cache_dict, specified_cache_type):
    """
    Get total cache of CPU socket.
    """

    cache_size_cumulative = 0
    cache_shared_cpu_list_all = []
    selected_cpu_core_socket_core_list = sorted(list(socket_cores_cache_dict.keys()))
    for cpu_core in selected_cpu_core_socket_core_list:
        if cpu_core in cache_shared_cpu_list_all:
            continue
        core_caches_dict = socket_cores_cache_dict[cpu_core]
        for cache_type in core_caches_dict:
            core_cache_dict = core_caches_dict[cache_type]
            if cache_type == specified_cache_type:
                cache_size = core_cache_dict["cache_size"]
                cache_size_cumulative = cache_size_cumulative + int(cache_size.strip("K"))
                cache_shared_cpu_list = core_cache_dict["cache_shared_cpu_list"]
                for shared_cpu_core in cache_shared_cpu_list:
                    cache_shared_cpu_list_all.append("cpu" + str(shared_cpu_core))
    #cache_size_cumulative = str(cache_size_cumulative) + "K"
    cache_size_cumulative = convert_cpu_cache_data_unit(cache_size_cumulative)

    return cache_size_cumulative


def convert_cpu_cache_data_unit(cache_size):

    for data_unit in ["KiB", "MiB", "GiB"]:
        if cache_size < 1024:
            break
        cache_size = cache_size / 1024

    cache_size_str = str(cache_size)
    if "." in cache_size_str and cache_size_str.split(".")[-1] != "0":
        cache_size = f'{cache_size:.1f}'
    else:
        cache_size = f'{cache_size:.0f}'

    cache_size = str(cache_size) + " " + data_unit

    return cache_size


def get_cpu_architecture():
    """
    Get CPU architecture.
    """

    cpu_architecture = platform.processor()
    if cpu_architecture == "":
        cpu_architecture = platform.machine()
        if cpu_architecture == "":
            cpu_architecture = "-"

    return cpu_architecture


def get_cpu_core_current_frequency(selected_cpu_core):
    """
    Get current frequency of the CPU core.
    '/sys/devices/system/cpu/cpu[NUMBER]/cpufreq' is used instead of '/sys/devices/system/cpu/cpufreq/policy[NUMBER]'.
    Because CPU core current frequencies may be same for all cores on RB-Pi devices and "scaling_cur_freq" file may be available
    for only 0th core of the relevant CPU group (little cores , big cores).
    """

    cpu_core_current_frequency = "-"

    try:
        with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_cur_freq") as reader:
            cpu_core_current_frequency = float(reader.read().strip()) / 1000000
    # CPU core current frequency may not be available in "/sys/devices/system/cpu/cpufreq/policy..." folders on virtual machines (x86_64).
    # Get it by reading "/proc/cpuinfo" file.
    except FileNotFoundError:
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
        proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(selected_cpu_core.split("cpu")[1])].split("\n")
        for line in proc_cpuinfo_all_cores_lines:
            if line.startswith("cpu MHz"):
                cpu_core_current_frequency = float(line.split(":")[1].strip()) / 1000
                break

    return cpu_core_current_frequency


def get_number_of_physical_cores_sockets_cpu_name(selected_cpu_core, number_of_logical_cores):
    """
    Get number of physical cores, number of cpu sockets, cpu_model_names.
    """

    cpu_times = get_cpu_times()
    cpu_core_number = list(cpu_times.keys()).index(selected_cpu_core)

    with open("/proc/cpuinfo") as reader:
        proc_cpuinfo_output = reader.read()
    proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")

    # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "x86_64" architecture.
    # Physical and logical cores and model name per core information are tracked easily on this platform.
    if "physical id" in proc_cpuinfo_output:
        cpu_model_names = []
        number_of_physical_cores = 0
        physical_id = 0
        physical_id_prev = 0
        for line in proc_cpuinfo_output_lines:
            if line.startswith("physical id"):
                physical_id_prev = physical_id
                physical_id = line.split(":")[1].strip()
            if physical_id != physical_id_prev and line.startswith("cpu cores"):
                number_of_physical_cores = number_of_physical_cores + int(line.split(":")[1].strip())
            if line.startswith("model name"):
                cpu_model_names.append(line.split(":")[1].strip())
        number_of_cpu_sockets = int(physical_id) + 1
        cpu_model_name = cpu_model_names[cpu_core_number]

    # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture.
    # Physical and logical cores and model name per core information are not tracked easily on this platform.
    # Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
    else:
        cpu_model_names = []
        number_of_physical_cores = number_of_logical_cores
        number_of_cpu_sockets = 1

        cpu_implementer_list = []
        cpu_architecture_list = []
        cpu_part_list = []

        # Get register values to get required information.
        for line in proc_cpuinfo_output_lines:
            # "CPU implementer" is used for getting vendor.
            if line.startswith("CPU implementer"):
                cpu_implementer_list.append(line.split(":")[-1].strip())
            # "CPU architecture" is used for getting architecture.
            elif line.startswith("CPU architecture"):
                cpu_architecture_list.append(line.split(":")[-1].strip())
            # "CPU part" is used for getting core model such as Cortex-A57.
            elif line.startswith("CPU part"):
                cpu_part_list.append(line.split(":")[-1].strip())

        # Redefine "cpu_core_number" in order to get information of the CPU core.
        if len(cpu_implementer_list) == number_of_logical_cores:
            pass
        # There may be only one instance of register values even if CPU has multiple cores.
        else:
            cpu_core_number = 0

        # Get CPU model information by using register values.
        cpu_implementer = "-"
        cpu_architecture = "-"
        cpu_part = "-"
        # Read database file for ARM CPU register values.
        with open(os.path.dirname(os.path.realpath(__file__)) + "/../database/arm.ids") as reader:
            ids_file_output = reader.read().strip()
        # Define ARM architecture dictionary.
        arm_architecture_dict = {"5TE": "ARMv5", "6TEJ": "ARMv6", "7": "ARMv7", "8": "ARMv8"}
        # Get device vendor, model names from device ID file content.
        search_text1 = cpu_implementer_list[cpu_core_number].split("0x", 1)[-1]
        search_text2 = "\t" + cpu_part_list[cpu_core_number].split("0x", 1)[-1]
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            cpu_implementer = rest_of_the_ids_file_output.split("\n", 1)[0].strip()
            if search_text2 in ids_file_output:
                cpu_part = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0].strip()
            else:
                cpu_part = "-"
        else:
            cpu_implementer = "-"
            cpu_part = "-"
        try:
            cpu_architecture = arm_architecture_dict[cpu_architecture_list[cpu_core_number]]
        except KeyError:
            cpu_architecture = "-"
        cpu_model_name = f'{cpu_implementer} {cpu_part} ({cpu_architecture})'
        # Get CPU model information by using "/proc/cpuinfo" file if CPU implementer or CPU part is not detected.
        if cpu_implementer == "-" or cpu_part == "-":
            cpu_model_name = "-"
            for line in proc_cpuinfo_output_lines:
                if line.startswith("model name"):
                    cpu_model_name = line.split(":")[-1].strip()
            if cpu_model_name == "-":
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("Processor"):
                        cpu_model_name = line.split(":")[-1].strip()
            if cpu_model_name == "-":
                cpu_model_name = "[" + _tr("Unknown") + "]"

    return number_of_physical_cores, number_of_cpu_sockets, cpu_model_name


def get_processes_threads():
    """
    Get number of threads and number of processes.
    """

    if get_environment_type() == "flatpak":
        number_of_total_processes, number_of_total_threads = get_processes_threads_ps()
        if number_of_total_processes == 0 or number_of_total_threads == 0:
            number_of_total_processes, number_of_total_threads = get_processes_threads_ls_cat()

    else:
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]

        thread_count_list = []
        for pid in pid_list:
            try:
                with open("/proc/" + pid + "/status") as reader:
                    proc_status_output = reader.read()
            # Skip to the next loop without application error if a "FileNotFoundError" error is encountered
            # when process is ended after process list is get.
            except (FileNotFoundError, ProcessLookupError) as me:
                continue
            # Append number of threads of the process
            thread_count_list.append(int(proc_status_output.split("\nThreads:", 1)[1].split("\n", 1)[0].strip()))

        number_of_total_processes = len(thread_count_list)
        number_of_total_threads = sum(thread_count_list)

    return number_of_total_processes, number_of_total_threads


def get_processes_threads_ps():
    """
    Get number of threads and number of processes by using "ps" command.
    "procps" package is required for running this command and it may not be installed on all systems.
    """

    command_list = ["flatpak-spawn", "--host", "ps", "-eo", "thcount"]
    ps_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")
    # Delete header line
    del ps_output_lines[0]
    number_of_total_processes = len(ps_output_lines)
    number_of_total_threads = 0
    for line in ps_output_lines:
        number_of_total_threads = number_of_total_threads + int(line.strip())

    return number_of_total_processes, number_of_total_threads


def get_processes_threads_ls_cat():
    """
    Get number of threads and number of processes by using "ls" and "cat" commands.
    """

    # Get PID list
    command_list = ["ls", "/proc/"]
    command_list = ["flatpak-spawn", "--host"] + command_list
    ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
    pid_list = []
    for pid in ls_output.split():
        if pid.isdigit() == True:
            pid_list.append(pid)
    pid_list = sorted(pid_list, key=int)

    # Get process information from procfs files.
    command_list = ["env", "LANG=C", "cat"]
    command_list = ["flatpak-spawn", "--host"] + command_list
    for pid in pid_list:
        command_list.append(f'/proc/{pid}/stat')
    cat_output_lines = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip().split("\n")
    # Delete empty lines of ended processes
    if "" in cat_output_lines:
        cat_output_lines.remove("")

    # Get process and thread count
    number_of_total_processes = len(cat_output_lines)
    number_of_total_threads = 0
    for line in cat_output_lines:
        number_of_total_threads = number_of_total_threads + int(line.split(" ")[-33])

    return number_of_total_processes, number_of_total_threads


def get_system_up_time():
    """
    Get system up time.
    """

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

    system_up_time = f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}'

    return system_up_time


# ***********************************************************************************************
#                                           Memory
# ***********************************************************************************************

def get_physical_ram():
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
    Physical RAM size may be get 1 GiB less than hardware capacity on systems with integrated AMD GPUs.
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
        if get_environment_type() == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        try:
            total_physical_ram = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
            # Convert MiB value to bytes
            total_physical_ram = float(total_physical_ram) * 1024 * 1024
        except Exception:
            total_physical_ram = "-"

    return total_physical_ram


def get_ram_hardware_info():
    """
    Get RAM hardware information by using "dmidecode" command.
    """

    # Initial value of the variable
    memory_ram_hardware_info = ""

    # "sudo" has to be used for using "pkexec" to run "dmidecode" with root privileges.
    command_list = ["pkexec", "sudo", "dmidecode", "-t", "16,17"]
    if get_environment_type() == "flatpak":
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


def get_swap_details_info(performance_memory_data_precision=1, performance_memory_data_unit=0):
    """
    Get swap memory details information by reading "/proc/swaps" file.
    """

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
        swap_size = f'{data_unit_converter("data", "none", swap_size, performance_memory_data_unit, performance_memory_data_precision)}'
        swap_used = int(line_split[3].strip()) * 1024
        swap_used = f'{data_unit_converter("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}'
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

    return memory_swap_details_info


# ***********************************************************************************************
#                                           Disk
# ***********************************************************************************************

def get_disk_type(selected_disk):
    """
    Get disk type (Disk or Partition).
    """

    with open("/sys/class/block/" + selected_disk + "/uevent") as reader:
        sys_class_block_disk_uevent_lines = reader.read().split("\n")

    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            disk_type = _tr(line.split("=")[1].capitalize())
            break

    return disk_type


def get_disk_parent_name(selected_disk, disk_type, disk_list):
    """
    Get disk parent name.
    """

    disk_parent_name = "-"
    if disk_type == _tr("Partition"):
        for check_disk_dir in disk_list:
            if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk) == True:
                disk_parent_name = check_disk_dir

    return disk_parent_name


def get_disk_device_model_name(selected_disk, disk_type, disk_parent_name):
    """
    Get disk vendor and model.
    """

    if disk_type == _tr("Disk"):
        disk_or_parent_disk_name = selected_disk
    if disk_type == _tr("Partition"):
        disk_or_parent_disk_name = disk_parent_name

    # Get disk vendor and model.
    device_vendor_name = "-"
    device_model_name = "-"
    disk_device_model_name = "-"

    # Get device vendor model if this is a NVMe SSD.
    # These disks do not have "modalias" or "vendor" files under "/sys/class/block/" + selected_disk + "/device" directory.
    if os.path.isdir("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/") == True:
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = get_device_vendor_model(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass

        if "-" not in [device_vendor_name, device_model_name] or "Unknown" not in [device_vendor_name, device_model_name]:
            disk_device_model_name = f'{device_vendor_name} - {device_model_name}'

        # Get device vendor-model if this is a NVMe SSD and vendor or model is not found in hardware database.
        if "-" in [device_vendor_name, device_model_name] or "Unknown" in [device_vendor_name, device_model_name]:
            device_vendor_name = "-"
            device_model_name = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                    device_model_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                pass

            if device_model_name != "-":
                disk_device_model_name = device_model_name
            else:
                device_vendor_name = "[" + _tr("Unknown") + "]"
                device_model_name = "[" + _tr("Unknown") + "]"
                disk_device_model_name = f'{device_vendor_name} - {device_model_name}'

    # Get device vendor model if this is a SCSI, IDE or virtio device (on QEMU virtual machines).
    if os.path.isdir("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/") == False:
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = get_device_vendor_model(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass

        # Get device vendor model if this is a SCSI or IDE disk.
        if device_vendor_name == "[scsi_or_ide_disk]":
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/vendor") as reader:
                    device_vendor_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                device_vendor_name = "Unknown"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                    device_model_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                device_model_name = "Unknown"

        if device_vendor_name == "Unknown":
            device_vendor_name = "[" + _tr("Unknown") + "]"
        if device_model_name == "Unknown":
            device_model_name = "[" + _tr("Unknown") + "]"
        disk_device_model_name = f'{device_vendor_name} - {device_model_name}'

    # Get disk vendor and model if disk is loop device or swap disk.
    if selected_disk.startswith("loop"):
        disk_device_model_name = "[Loop Device]"
    if selected_disk.startswith("zram"):
        disk_device_model_name = "[" + "zram" + "]"
        # zram disks may be used as swap disk, disk for temporary files (/tmp), etc.
        # Check if disk name is in "/proc/swaps" file in order to determine if it is used as swap disk.
        with open("/proc/swaps") as reader:
            proc_swaps_lines = reader.read().split("\n")
        # Delete header indormation which is get from "/proc/swaps" file.
        del proc_swaps_lines[0]
        for line in proc_swaps_lines:
            if line.split()[0].split("/")[-1] == selected_disk:
                disk_device_model_name = "[" + "zram - " + _tr("Swap").upper() + "]"
                break
    if selected_disk.startswith("ram"):
        disk_device_model_name = "[Ramdisk]"
    if selected_disk.startswith("dm-"):
        disk_device_model_name = "[Device Mapper]"
    if selected_disk.startswith("mmcblk"):
        # Read database file for MMC disk register values. For more info about CIDs: https://www.kernel.org/doc/Documentation/mmc/mmc-dev-attrs.txt
        with open(os.path.dirname(os.path.realpath(__file__)) + "/../database/sdcard.ids") as reader:
            ids_file_output = reader.read().strip()
        # Get device vendor, model names from device ID file content.
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/manfid") as reader:
                disk_vendor_manfid = reader.read().strip()
            search_text1 = "MANFID " + disk_vendor_manfid.split("0x", 1)[-1]
            if search_text1 in ids_file_output:
                disk_vendor = ids_file_output.split(search_text1, 1)[1].split("\n", 1)[0].strip()
            else:
                disk_vendor = "-"
        except Exception:
            disk_vendor = "-"
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/name") as reader:
                disk_name = reader.read().strip()
            disk_model = disk_name
        except FileNotFoundError:
            disk_model = "-"
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/type") as reader:
                disk_card_type = reader.read().strip()
        except FileNotFoundError:
            disk_card_type = "-"
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/speed_class") as reader:
                disk_card_speed_class = reader.read().strip()
        except FileNotFoundError:
            disk_card_speed_class = "-"
        disk_device_model_name = f'{disk_vendor} - {disk_model} ({disk_card_type} Card, Class {disk_card_speed_class})'

    return disk_device_model_name


def get_disk_file_system_information(disk_list):
    """
    Get file system information (file systems, capacities, used, free, used percentages and mount points) of all disks.
    """

    # Get file system information of the mounted disks by using "df" command.
    # Online drives are excluded from "df" command output for avoiding long command runs and GUI blockings.
    # Currently, "fuse.onedriver" filesystems (generated by Onedriver application) are excluded.
    # More filesystems can be excluded by using the parameter multiple times (comma-separated filesystems
    # for excluding are not supported by "df").
    command_list = ["df", "--exclude-type=fuse.onedriver", "--output=source,fstype,size,used,avail,pcent,target"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    df_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

    # Remove command output title line. Only disk information will be left.
    del df_output_lines[0]

    # Get mounted disk list.
    mounted_disk_list = []
    for line in df_output_lines:
        disk_name = line.split()[0]
        mounted_disk_list.append(disk_name.split("/dev/")[-1])

    encrypted_disk_filesystem_information_dict = get_encrypted_disk_information(df_output_lines)
    encrypted_disk_list = list(encrypted_disk_filesystem_information_dict.keys())

    # Get file system information of the mounted and unmounted disks.
    disk_filesystem_information_list = []
    for disk in disk_list:
        if disk in mounted_disk_list:
            index = mounted_disk_list.index(disk)
            disk_file_system = df_output_lines[index].split()[1]
            disk_capacity = int(df_output_lines[index].split()[2]) * 1024
            disk_used = int(df_output_lines[index].split()[3]) * 1024
            disk_free = int(df_output_lines[index].split()[4]) * 1024
            disk_used_percentage = int(df_output_lines[index].split()[5].strip("%"))
            disk_mount_point = df_output_lines[index].split("% ", 1)[-1]
            encrypted_disk_name = ""
        elif disk in encrypted_disk_list:
            disk_file_system = encrypted_disk_filesystem_information_dict[disk]["disk_file_system"]
            disk_capacity = encrypted_disk_filesystem_information_dict[disk]["disk_capacity"]
            disk_used = encrypted_disk_filesystem_information_dict[disk]["disk_used"]
            disk_free = encrypted_disk_filesystem_information_dict[disk]["disk_free"]
            disk_used_percentage = encrypted_disk_filesystem_information_dict[disk]["disk_used_percentage"]
            disk_mount_point = encrypted_disk_filesystem_information_dict[disk]["disk_mount_point"]
            encrypted_disk_name = encrypted_disk_filesystem_information_dict[disk]["encrypted_disk_name"]
        else:
            disk_file_system = "[" + _tr("Not mounted") + "]"
            disk_capacity = "[" + _tr("Not mounted") + "]"
            disk_used = "[" + _tr("Not mounted") + "]"
            disk_free = "[" + _tr("Not mounted") + "]"
            disk_used_percentage = 0
            disk_mount_point = "[" + _tr("Not mounted") + "]"
            encrypted_disk_name = ""
        disk_filesystem_information_list.append([disk, disk_file_system, disk_capacity, disk_used, disk_free, disk_used_percentage, disk_mount_point, encrypted_disk_name])

    return disk_filesystem_information_list


def get_encrypted_disk_information(df_output_lines):
    """
    Check if the selected disk is encrypted and get its file system information.
    """

    encrypted_disk_filesystem_information_dict = {}

    for line in df_output_lines:
        encrypted_disk_information = {}
        disk_name = line.split()[0]
        if disk_name.startswith("/dev/mapper/") == False:
            continue
        else:
            encrypted_disk_name = disk_name.split("/dev/mapper/")[-1]
            disk_file_system = line.split()[1]
            disk_capacity = int(line.split()[2]) * 1024
            disk_used = int(line.split()[3]) * 1024
            disk_free = int(line.split()[4]) * 1024
            disk_used_percentage = int(line.split()[5].strip("%"))
            disk_mount_point = line.split("% ", 1)[-1]
            encrypted_disk_information["encrypted_disk_name"] = encrypted_disk_name
            encrypted_disk_information["disk_file_system"] = disk_file_system
            encrypted_disk_information["disk_capacity"] = disk_capacity
            encrypted_disk_information["disk_used"] = disk_used
            encrypted_disk_information["disk_free"] = disk_free
            encrypted_disk_information["disk_used_percentage"] = disk_used_percentage
            encrypted_disk_information["disk_mount_point"] = disk_mount_point
            # Get disk file in "/dev/mapper"
            dev_mapper_disks = os.listdir("/dev/mapper/")
            if encrypted_disk_name in dev_mapper_disks:
                if os.path.isdir("/dev/mapper/" + encrypted_disk_name) != True:
                    disk_real_path = os.path.realpath("/dev/mapper/" + encrypted_disk_name)
                    disk_proc_name = disk_real_path.split("/")[-1]
                    encrypted_disk_filesystem_information_dict[disk_proc_name] = encrypted_disk_information

    return encrypted_disk_filesystem_information_dict


def get_disk_file_system_capacity_used_free_used_percent_mount_point(disk_filesystem_information_list, disk_list, selected_disk):
    """
    Get file file systems, capacities, used, free, used percentages and mount points of all disks.
    """

    disk_index = disk_list.index(selected_disk)
    disk_file_system = disk_filesystem_information_list[disk_index][1]
    disk_capacity = disk_filesystem_information_list[disk_index][2]
    disk_used = disk_filesystem_information_list[disk_index][3]
    disk_free = disk_filesystem_information_list[disk_index][4]
    disk_usage_percentage = disk_filesystem_information_list[disk_index][5]
    disk_mount_point = disk_filesystem_information_list[disk_index][6]
    encrypted_disk_name = disk_filesystem_information_list[disk_index][7]

    return disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point, encrypted_disk_name


def get_disk_file_system_fuseblk(selected_disk):
    """
    Get disk file system if it is detected as 'fuseblk'.
    """

    # Try to get actual file system by using "lsblk" tool if file system
    # has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts"
    # file contains file system information as in user space. To be able to get the
    # actual file system, root access is needed for reading from some files or 
    # "lsblk" tool could be used.
    disk_for_file_system = "/dev/" + selected_disk
    command_list = ["lsblk", "-no", "FSTYPE", disk_for_file_system]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    try:
        disk_file_system = (subprocess.check_output(command_list, shell=False)).decode().strip()
    except Exception:
        disk_file_system = "fuseblk"

    return disk_file_system


def get_disk_if_system_disk(selected_disk, system_disk_list):
    """
    Get if system disk information.
    """

    if selected_disk in system_disk_list:
        if_system_disk = _tr("Yes")
    else:
        if_system_disk = _tr("No")

    return if_system_disk


def get_disk_read_write_data(selected_disk):
    """
    Get disk read data and disk write data.
    """

    disk_io = get_disk_io()

    disk_read_data = disk_io[selected_disk]["read_bytes"]
    disk_write_data = disk_io[selected_disk]["write_bytes"]

    return disk_read_data, disk_write_data


def get_disk_capacity_mass_storage(selected_disk):
    """
    Get disk capacity (mass storage).
    """

    with open("/sys/class/block/" + selected_disk + "/size") as reader:
        disk_capacity_mass_storage = int(reader.read()) * disk_sector_size

    return disk_capacity_mass_storage


def get_disk_label(selected_disk):
    """
    Get disk label.
    """

    disk_label = "-"
    try:
        disk_label_list = os.listdir("/dev/disk/by-label/")
        for label in disk_label_list:
            if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == selected_disk:
                # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                disk_label = bytes(label, "utf-8").decode("unicode_escape")
    except FileNotFoundError:
        pass

    return disk_label


# ***********************************************************************************************
#                                           Network
# ***********************************************************************************************

def get_network_card_device_model_name(selected_network_card):
    """
    Get network card vendor and model.
    """

    # Get device vendor and model names
    device_vendor_name = "-"
    device_model_name = "-"
    # Get device vendor and model names if it is not a virtual device.
    if os.path.isdir("/sys/devices/virtual/net/" + selected_network_card) == False:
        # Check if there is a "modalias" file. Some network interfaces (such as usb0, usb1, etc.) may not have this file.
        if os.path.isfile("/sys/class/net/" + selected_network_card + "/device/modalias") == True:
            # Read device vendor and model ids by reading "modalias" file.
            with open("/sys/class/net/" + selected_network_card + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = get_device_vendor_model(modalias_output)
            if device_vendor_name == "Unknown":
                device_vendor_name = "[" + _tr("Unknown") + "]"
            if device_model_name == "Unknown":
                device_model_name = "[" + _tr("Unknown") + "]"
        network_card_device_model_name = f'{device_vendor_name} - {device_model_name}'

    # Get device vendor and model names if it is a virtual device.
    else:
        # lo (Loopback Device) is a system device and it is not a physical device.
        if selected_network_card == "lo":
            network_card_device_model_name = "[" + "Loopback Device" + "]"
        else:
            network_card_device_model_name = "[" + _tr("Virtual Network Interface") + "]"

    return network_card_device_model_name


def get_connection_type(selected_network_card):
    """
    Get connection type on the selected network card.
    """

    if selected_network_card.startswith("en"):
        connection_type = _tr("Ethernet")
    elif selected_network_card.startswith("wl"):
        connection_type = _tr("Wi-Fi")
    else:
        connection_type = "-"

    return connection_type


def get_mac_address(selected_network_card):
    """
    Get network card MAC address.
    """

    try:
        with open("/sys/class/net/" + selected_network_card + "/address") as reader:
            network_card_mac_address = reader.read().strip().upper()
    # Some network interfaces (such as some of the virtual network interfaces) may not have a MAC address.
    except FileNotFoundError:
        network_card_mac_address = "-"

    return network_card_mac_address


def get_ipv4_ipv6_address(selected_network_card):
    """
    Get IPv4 and IPv6 addresses on the selected network card.
    """

    try:
        ip_output = (subprocess.check_output(["ip", "a", "show", selected_network_card], shell=False)).decode()
    # "ip" program is in "/sbin/" on some systems (such as Slackware based distributions).
    except FileNotFoundError:
        ip_output = (subprocess.check_output(["/sbin/ip", "a", "show", selected_network_card], shell=False)).decode()
    ip_output_lines = ip_output.strip().split("\n")

    network_address_ipv4 = "-"
    network_address_ipv6 = "-"

    for line in ip_output_lines:
        if "inet " in line:
            network_address_ipv4 = line.split()[1].split("/")[0]
        if "inet6 " in line:
            network_address_ipv6 = line.split()[1].split("/")[0]

    return network_address_ipv4, network_address_ipv6


def get_network_download_upload_data(selected_network_card):
    """
    Get network card download data and upload data.
    """

    network_io = get_network_io()

    network_receive_bytes = network_io[selected_network_card]["download_bytes"]
    network_send_bytes = network_io[selected_network_card]["upload_bytes"]

    return network_send_bytes, network_receive_bytes


def get_network_card_connected(selected_network_card):
    """
    Get connected information for the selected network card.
    """

    with open("/sys/class/net/" + selected_network_card + "/operstate") as reader:
        network_info = reader.read().strip()

    if network_info == "up":
        network_card_connected = _tr("Yes")
    elif network_info == "down":
        network_card_connected = _tr("No")
    elif network_info == "unknown":
        network_card_connected = "[" + _tr("Unknown") + "]"
    else:
        network_card_connected = network_info

    return network_card_connected


def get_network_ssid(selected_network_card):
    """
    Get network name (SSID).
    """

    command_list = ["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    try:
        nmcli_output_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
    # Avoid errors because Network Manager (required "nmcli" command) may not be installed (very rare).
    except (FileNotFoundError, subprocess.CalledProcessError) as me:
        nmcli_output_lines = "-"
        network_ssid = "[" + _tr("Unknown") + "]"

    # Check if "nmcli_output_lines" value is get.
    if nmcli_output_lines != "-":
        for line in nmcli_output_lines:
            line_splitted = line.split(":")
            if selected_network_card == line_splitted[0]:
                network_ssid = line_splitted[1].strip()
                break

    # "network_ssid" value is get as "" if selected network card is not connected a Wi-Fi network.
    if network_ssid == "":
        network_ssid = "-"

    return network_ssid


def get_network_link_quality(selected_network_card, network_card_connected):
    """
    Get network link quality.
    """

    network_link_quality = "-"
    # Translated value have to be used by using gettext constant. Not "Yes".
    if selected_network_card.startswith("wl") == True and network_card_connected == _tr("Yes"):
        with open("/proc/net/wireless") as reader:
            proc_net_wireless_output_lines = reader.read().strip().split("\n")
        for line in proc_net_wireless_output_lines:
            line_splitted = line.split()
            if selected_network_card == line_splitted[0].split(":")[0]:
                # Remove "." at the end of the signal value.
                network_link_quality = line_splitted[2].split(".")[0]
                if network_link_quality != "-":
                    network_link_quality = f'{network_link_quality} (link)'
                break

    return network_link_quality


# ***********************************************************************************************
#                                           GPU
# ***********************************************************************************************

def get_gpu_list_and_boot_vga():
    """
    Get GPU list.
    """

    gpu_list = []
    gpu_device_path_list = []
    gpu_device_sub_path_list = []
    default_gpu = ""

    # Get GPU list from "/sys/class/drm/" directory which is used by x86_64 desktop systems.
    if os.path.isdir("/dev/dri/") == True:

        for file in os.listdir("/sys/class/drm/"):
            if "-" not in file and file.split("-")[0].rstrip("0123456789") == "card":
                gpu_list.append(file)
                gpu_device_path_list.append("/sys/class/drm/" + file + "/")
                gpu_device_sub_path_list.append("/device/")

                # Get if default GPU information.
                try:
                    with open("/sys/class/drm/" + file + "/device/" + "boot_vga") as reader:
                        if reader.read().strip() == "1":
                            default_gpu = file
                except (FileNotFoundError, NotADirectoryError) as me:
                    pass

    # Try to get GPU list from "/sys/devices/" folder which is used by some ARM systems with NVIDIA GPU.
    for file in os.listdir("/sys/devices/"):

        if file.split(".")[0] == "gpu":
            gpu_list.append(file)
            gpu_device_path_list.append("/sys/devices/" + file + "/")
            gpu_device_sub_path_list.append("/")

            # Get if default GPU information
            try:
                with open("/sys/devices/" + file + "/" + "boot_vga") as reader:
                    if reader.read().strip() == "1":
                        default_gpu = file
            except (FileNotFoundError, NotADirectoryError) as me:
                pass

    return gpu_list, gpu_device_path_list, gpu_device_sub_path_list, default_gpu


def gpu_set_selected_gpu(selected_gpu, gpu_list, default_gpu):
    """
    Get default GPU.
    """

    # "" is predefined gpu name before release of the software. This statement is used in order to avoid error, if no gpu selection is made since first run of the software.
    if selected_gpu == "":
        if default_gpu != "":
            set_selected_gpu = default_gpu
        if default_gpu == "":
            set_selected_gpu = gpu_list[0]
    if selected_gpu in gpu_list:
        set_selected_gpu = selected_gpu
    else:
        if default_gpu != "":
            set_selected_gpu = default_gpu
        if default_gpu == "":
            set_selected_gpu = gpu_list[0]
    selected_gpu_number = gpu_list.index(set_selected_gpu)
    selected_gpu = set_selected_gpu

    return selected_gpu_number, selected_gpu


def get_default_gpu(selected_gpu_number, gpu_list, default_gpu):
    """
    Get if default GPU.
    """

    # Set default GPU if there is only 1 GPU on the system and
    # there is not "boot_vga" file (such as ARM devices) which means default_gpu = "".
    if len(gpu_list) == 1:
        if_default_gpu = _tr("Yes")
    else:
        if gpu_list[selected_gpu_number] == default_gpu:
            if_default_gpu = _tr("Yes")
        else:
            if_default_gpu = _tr("No")

    return if_default_gpu


def get_driver_name(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list):
    """
    Get GPU driver name.
    """

    selected_gpu = gpu_list[selected_gpu_number]
    gpu_device_path = gpu_device_path_list[selected_gpu_number]
    gpu_device_sub_path = gpu_device_sub_path_list[selected_gpu_number]

    # Read device driver name by reading "uevent" file.
    with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
        uevent_output_lines = reader.read().strip().split("\n")

    gpu_driver_name = "-"
    for line in uevent_output_lines:
        if line.startswith("DRIVER="):
            gpu_driver_name = line.split("=")[-1]
            break

    return gpu_driver_name


def get_resolution_refresh_rate():
    """
    Get current resolution and refresh rate of the monitor(s).
    """

    resolution_list = []
    refresh_rate_list = []

    try:
        import gi
        gi.require_version('Gdk', '4.0')
        from gi.repository import Gdk
        monitor_list = Gdk.Display().get_default().get_monitors()
    except Exception:
        current_resolution = "-"
        current_refresh_rate = "-"
        return current_resolution, current_refresh_rate

    for monitor in monitor_list:
        monitor_rectangle = monitor.get_geometry()
        monitor_width = monitor_rectangle.width
        monitor_height = monitor_rectangle.height
        resolution_list.append(str(monitor_width) + "x" + str(monitor_height))
        # Milli-Hertz is converted to Hertz
        refresh_rate = float(monitor.get_refresh_rate() / 1000)
        refresh_rate_list.append(f'{refresh_rate:.2f} Hz')

    current_resolution = ', '.join(resolution_list)
    current_refresh_rate = ', '.join(refresh_rate_list)

    return current_resolution, current_refresh_rate


def monitor_resolution_refresh_rate_multiple_text(current_resolution, current_refresh_rate):
    """
    Generate a multiline text for resolutions and refresh rates of multiple monitors.
    """

    current_resolution_list = current_resolution.split(", ")
    current_refresh_rate_list = current_refresh_rate.split(", ")

    resolution_refresh_rate_text = ""
    for i, resolution in enumerate(current_resolution_list):
        resolution_refresh_rate_text = resolution_refresh_rate_text + resolution + " @" + current_refresh_rate_list[i]
        if i != len(current_resolution_list) - 1:
            resolution_refresh_rate_text = resolution_refresh_rate_text + ", "

    return resolution_refresh_rate_text


def get_device_model_name_vendor_id(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list):
    """
    Get GPU device model name and vendor name.
    """

    selected_gpu = gpu_list[selected_gpu_number]
    gpu_device_path = gpu_device_path_list[selected_gpu_number]
    gpu_device_sub_path = gpu_device_sub_path_list[selected_gpu_number]

    # Read device vendor and model ids by reading "modalias" file.
    with open(gpu_device_path + gpu_device_sub_path + "modalias") as reader:
        modalias_output = reader.read().strip()

    # Determine device subtype.
    device_subtype, device_alias = modalias_output.split(":", 1)
    device_vendor_name, device_model_name, device_vendor_id, device_model_id = get_device_vendor_model(modalias_output)
    if device_vendor_name == "Unknown":
        device_vendor_name = "[" + _tr("Unknown") + "]"
    if device_model_name == "Unknown":
        device_model_name = "[" + _tr("Unknown") + "]"
    gpu_device_model_name = f'{device_vendor_name} - {device_model_name}'

    return gpu_device_model_name, device_vendor_id


def get_gpu_pci_address(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list):
    """
    Get GPU PCI address which will be used for detecting the selected GPU for processing GPU performance information.
    """

    selected_gpu = gpu_list[selected_gpu_number]
    gpu_device_path = gpu_device_path_list[selected_gpu_number]
    gpu_device_sub_path = gpu_device_sub_path_list[selected_gpu_number]

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


def get_gpu_load_memory_frequency_power(gpu_pci_address, device_vendor_id, selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list):
    """
    Get GPU load, memory, frequencies, power.
    """

    gpu_device_path = gpu_device_path_list[selected_gpu_number]

    # If selected GPU vendor is Intel
    if device_vendor_id in ["v00008086"]:
        gpu_load_memory_frequency_power_dict = get_gpu_load_memory_frequency_power_intel(gpu_device_path)

    # If selected GPU vendor is AMD
    elif device_vendor_id in ["v00001022", "v00001002"]:
        gpu_load_memory_frequency_power_dict = get_gpu_load_memory_frequency_power_amd(gpu_device_path)

        # Get GPU load average. There is no "%" character in "gpu_busy_percent" file. This file contains GPU load for a very small time.
        global event
        try:
            event.set()
        except (NameError, UnboundLocalError, AttributeError):
            pass
        event = threading.Event()
        amd_gpu_load_thread = threading.Thread(target=gpu_load_amd_func, args=(gpu_device_path, event))
        amd_gpu_load_thread.daemon = True
        amd_gpu_load_thread.name = "amd_gpu_load_thread"
        try:
            amd_gpu_load_thread.start()
            gpu_load = f'{(sum(amd_gpu_load_list) / len(amd_gpu_load_list)):.0f} %'
        except Exception:
            gpu_load = "-"

        """# Update the GPU load value. Because it is not get in "get_gpu_load_memory_frequency_power_amd" function.
        gpu_load_memory_frequency_power_dict["gpu_load"] = gpu_load

        # Get encoder/decoder engine load of AMD GPU by using "amdgpu_top" tool.
        threading.Thread(target=gpu_encoder_decoder_load_amd_func, daemon=True).start()

        global gpu_tool_output_amdgpu_top
        try:
            check_value = gpu_tool_output_amdgpu_top
        except NameError:
            gpu_tool_output_amdgpu_top = "-"

        # Update encoder/decoder engine load values. Because they are not get in "get_gpu_load_memory_frequency_power_amd" function.
        gpu_load_memory_frequency_power_dict = process_gpu_tool_output_amdgpu_top(gpu_pci_address, gpu_tool_output_amdgpu_top, gpu_load_memory_frequency_power_dict)
        """

    # If selected GPU vendor is Broadcom (for RB-Pi ARM devices).
    elif device_vendor_id in ["Brcm"]:
        gpu_load_memory_frequency_power_dict = get_gpu_load_memory_frequency_power_broadcom_arm()

    # If selected GPU vendor is NVIDIA and selected GPU is used on a PCI used system.
    elif device_vendor_id == "v000010DE" and gpu_device_path.startswith("/sys/class/drm/") == True:
        # Try to get GPU usage information in a separate thread in order to prevent this function from blocking
        # the main thread and GUI for a very small time which stops the GUI for a very small time.
        threading.Thread(target=gpu_load_nvidia_func, daemon=True).start()

        global gpu_tool_output_nvidia_smi, nvidia_smi_encoder_decoder
        try:
            check_value = gpu_tool_output_nvidia_smi
        except NameError:
            gpu_tool_output_nvidia_smi = "-"
            nvidia_smi_encoder_decoder = 1

        gpu_load_memory_frequency_power_dict = process_gpu_tool_output_nvidia(gpu_pci_address, gpu_tool_output_nvidia_smi, nvidia_smi_encoder_decoder)

    # If selected GPU vendor is NVIDIA and selected GPU is used on an ARM system.
    elif device_vendor_id in ["v000010DE", "Nvidia"] and gpu_device_path.startswith("/sys/devices/") == True:
        gpu_load_memory_frequency_power_dict = get_gpu_load_memory_frequency_power_nvidia_arm(gpu_device_path)

    else:
        gpu_load_memory_frequency_power_dict = {
                                                "gpu_load" : "-",
                                                "gpu_encoder_load": "-",
                                                "gpu_decoder_load": "-",
                                                "gpu_memory_used" : "-",
                                                "gpu_memory_capacity" : "-",
                                                "gpu_current_frequency" : "-",
                                                "gpu_min_frequency" : "-",
                                                "gpu_max_frequency" : "-",
                                                "gpu_memory_current_frequency" : "-",
                                                "gpu_memory_min_frequency" : "-",
                                                "gpu_memory_max_frequency" : "-",
                                                "gpu_temperature" : "-",
                                                "gpu_power_current" : "-",
                                                "gpu_power_max" : "-",
                                                "gpu_driver_version" : "-"
                                                }

    return gpu_load_memory_frequency_power_dict


def get_gpu_load_memory_frequency_power_intel(gpu_device_path):
    """
    Get GPU load, video memory, GPU frequency, power usage if GPU vendor is Intel.
    """

    # Define initial values
    gpu_load = "-"
    gpu_encoder_load = "-"
    gpu_decoder_load = "-"
    gpu_memory_used = "-"
    gpu_memory_capacity = "-"
    gpu_current_frequency = "-"
    gpu_min_frequency = "-"
    gpu_max_frequency = "-"
    gpu_memory_current_frequency = "-"
    gpu_memory_min_frequency = "-"
    gpu_memory_max_frequency = "-"
    gpu_temperature = "-"
    gpu_power_current = "-"
    gpu_power_max = "-"
    gpu_driver_version = "-"

    # Get GPU min frequency
    try:
        with open(gpu_device_path + "gt_min_freq_mhz") as reader:
            gpu_min_frequency = reader.read().strip()
    except FileNotFoundError:
        gpu_min_frequency = "-"

    if gpu_min_frequency != "-":
        gpu_min_frequency = f'{gpu_min_frequency} MHz'

    # Get GPU max frequency
    try:
        with open(gpu_device_path + "gt_max_freq_mhz") as reader:
            gpu_max_frequency = reader.read().strip()
    except FileNotFoundError:
        gpu_max_frequency = "-"

    if gpu_max_frequency != "-":
        gpu_max_frequency = f'{gpu_max_frequency} MHz'

    # Get GPU current frequency by reading "gt_cur_freq_mhz" file. This file may not be reliable because it
    # contains a constant value on some systems. Actual value can be get by using "intel_gpu_top" tool by using root privileges.
    try:
        with open(gpu_device_path + "gt_cur_freq_mhz") as reader:
            gpu_current_frequency = reader.read().strip()
    except FileNotFoundError:
        gpu_current_frequency = "-"

    if gpu_current_frequency != "-":
        gpu_current_frequency = f'{gpu_current_frequency} MHz'

    gpu_load_memory_frequency_power_dict = {
                                            "gpu_load" : gpu_load,
                                            "gpu_encoder_load": gpu_encoder_load,
                                            "gpu_decoder_load": gpu_decoder_load,
                                            "gpu_memory_used" : gpu_memory_used,
                                            "gpu_memory_capacity" : gpu_memory_capacity,
                                            "gpu_current_frequency" : gpu_current_frequency,
                                            "gpu_min_frequency" : gpu_min_frequency,
                                            "gpu_max_frequency" : gpu_max_frequency,
                                            "gpu_memory_current_frequency" : gpu_memory_current_frequency,
                                            "gpu_memory_min_frequency" : gpu_memory_min_frequency,
                                            "gpu_memory_max_frequency" : gpu_memory_max_frequency,
                                            "gpu_temperature" : gpu_temperature,
                                            "gpu_power_current" : gpu_power_current,
                                            "gpu_power_max" : gpu_power_max,
                                            "gpu_driver_version" : gpu_driver_version
                                            }

    return gpu_load_memory_frequency_power_dict


def get_gpu_load_memory_frequency_power_broadcom_arm():
    """
    Get GPU load, video memory, GPU frequency, power usage if GPU vendor is Broadcom (for RB-Pi ARM devices).
    GPU memory capacity and GPU current frequency information are get by using "vcgencmd" tool and
    it is not installed on the systems by default.
    """

    # Define initial values
    gpu_load = "-"
    gpu_encoder_load = "-"
    gpu_decoder_load = "-"
    gpu_memory_used = "-"
    gpu_memory_capacity = "-"
    gpu_current_frequency = "-"
    gpu_min_frequency = "-"
    gpu_max_frequency = "-"
    gpu_memory_current_frequency = "-"
    gpu_memory_min_frequency = "-"
    gpu_memory_max_frequency = "-"
    gpu_temperature = "-"
    gpu_power_current = "-"
    gpu_power_max = "-"
    gpu_driver_version = "-"

    # Get GPU memory capacity
    command_list = ["vcgencmd", "get_mem", "gpu"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    try:
        gpu_memory_capacity = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
    except Exception:
        gpu_memory_capacity = "-"

    # Get GPU current frequency
    command_list = ["vcgencmd", "measure_clock", "core"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    try:
        gpu_current_frequency = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
        gpu_current_frequency = f'{float(gpu_current_frequency)/1000000:.0f} MHz'
    except Exception:
        gpu_current_frequency = "-"

    gpu_load_memory_frequency_power_dict = {
                                            "gpu_load" : gpu_load,
                                            "gpu_encoder_load": gpu_encoder_load,
                                            "gpu_decoder_load": gpu_decoder_load,
                                            "gpu_memory_used" : gpu_memory_used,
                                            "gpu_memory_capacity" : gpu_memory_capacity,
                                            "gpu_current_frequency" : gpu_current_frequency,
                                            "gpu_min_frequency" : gpu_min_frequency,
                                            "gpu_max_frequency" : gpu_max_frequency,
                                            "gpu_memory_current_frequency" : gpu_memory_current_frequency,
                                            "gpu_memory_min_frequency" : gpu_memory_min_frequency,
                                            "gpu_memory_max_frequency" : gpu_memory_max_frequency,
                                            "gpu_temperature" : gpu_temperature,
                                            "gpu_power_current" : gpu_power_current,
                                            "gpu_power_max" : gpu_power_max,
                                            "gpu_driver_version" : gpu_driver_version
                                            }

    return gpu_load_memory_frequency_power_dict


def get_gpu_load_memory_frequency_power_nvidia_arm(gpu_device_path):
    """
    Get GPU load, video memory, GPU frequency, power usage if GPU vendor is NVIDIA and
    it is used on an ARM system (NVIDIA Tegra GPUs).
    """

    # Define initial values
    gpu_load = "-"
    gpu_encoder_load = "-"
    gpu_decoder_load = "-"
    gpu_memory_used = "-"
    gpu_memory_capacity = "-"
    gpu_current_frequency = "-"
    gpu_min_frequency = "-"
    gpu_max_frequency = "-"
    gpu_memory_current_frequency = "-"
    gpu_memory_min_frequency = "-"
    gpu_memory_max_frequency = "-"
    gpu_temperature = "-"
    gpu_power_current = "-"
    gpu_power_max = "-"
    gpu_driver_version = "-"

    # Get GPU frequency folders list. NVIDIA Tegra GPU files are listed in "/sys/devices/gpu.0/devfreq/57000000.gpu/" folder.
    gpu_frequency_files_list = os.listdir(gpu_device_path + "devfreq/")
    gpu_frequency_folders_list = []
    for file in gpu_frequency_files_list:
        if file.endswith(".gpu") and os.path.isdir(gpu_device_path + "devfreq/" + file) == True:
            gpu_frequency_folders_list.append(gpu_device_path + "devfreq/" + file + "/")
    gpu_frequency_folder = gpu_frequency_folders_list[0]

    # Get GPU min frequency
    try:
        with open(gpu_frequency_folder + "min_freq") as reader:
            gpu_min_frequency = reader.read().strip()
    except FileNotFoundError:
        gpu_min_frequency = "-"

    if gpu_min_frequency != "-":
        gpu_min_frequency = f'{(float(gpu_min_frequency) / 1000000):.0f}'

    # Get GPU max frequency
    try:
        with open(gpu_frequency_folder + "max_freq") as reader:
            gpu_max_frequency = reader.read().strip()
    except FileNotFoundError:
        gpu_max_frequency = "-"

    if gpu_max_frequency != "-":
        gpu_max_frequency = f'{(float(gpu_max_frequency) / 1000000):.0f} MHz'

    # Get GPU current frequency
    try:
        with open(gpu_frequency_folder + "cur_freq") as reader:
            gpu_current_frequency = reader.read().strip()
    except FileNotFoundError:
        gpu_current_frequency = "-"

    if gpu_current_frequency != "-":
        gpu_current_frequency = f'{(float(gpu_current_frequency) / 1000000):.0f} MHz'

    # Get GPU load
    try:
        with open(gpu_device_path + "load") as reader:
            gpu_load = reader.read().strip()
    except FileNotFoundError:
        gpu_load = "-"

    if gpu_load != "-":
        gpu_load = f'{(float(gpu_load) / 10):.0f} %'

    gpu_load_memory_frequency_power_dict = {
                                            "gpu_load" : gpu_load,
                                            "gpu_encoder_load": gpu_encoder_load,
                                            "gpu_decoder_load": gpu_decoder_load,
                                            "gpu_memory_used" : gpu_memory_used,
                                            "gpu_memory_capacity" : gpu_memory_capacity,
                                            "gpu_current_frequency" : gpu_current_frequency,
                                            "gpu_min_frequency" : gpu_min_frequency,
                                            "gpu_max_frequency" : gpu_max_frequency,
                                            "gpu_memory_current_frequency" : gpu_memory_current_frequency,
                                            "gpu_memory_min_frequency" : gpu_memory_min_frequency,
                                            "gpu_memory_max_frequency" : gpu_memory_max_frequency,
                                            "gpu_temperature" : gpu_temperature,
                                            "gpu_power_current" : gpu_power_current,
                                            "gpu_power_max" : gpu_power_max,
                                            "gpu_driver_version" : gpu_driver_version
                                            }

    return gpu_load_memory_frequency_power_dict


def get_gpu_load_memory_frequency_power_amd(gpu_device_path):
    """
    Get GPU load, video memory, GPU frequency, power usage if GPU vendor is AMD.
    """

    # Define initial values
    gpu_load = "-"
    gpu_encoder_load = "-"
    gpu_decoder_load = "-"
    gpu_memory_used = "-"
    gpu_memory_capacity = "-"
    gpu_current_frequency = "-"
    gpu_min_frequency = "-"
    gpu_max_frequency = "-"
    gpu_memory_current_frequency = "-"
    gpu_memory_min_frequency = "-"
    gpu_memory_max_frequency = "-"
    gpu_temperature = "-"
    gpu_power_current = "-"
    gpu_power_max = "-"
    gpu_driver_version = "-"

    # For more information about files under "/sys/class/drm/card[NUMBER]/device/" and their content
    # for AMD GPUs: https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html and https://wiki.archlinux.org/title/AMDGPU

    # Get GPU current, min, max frequencies (engine frequencies). This file contains all available
    # frequencies of the GPU. There is no separate frequency information in files for video clock frequency for AMD GPUs.
    gpu_frequency_file_output = "-"
    try:
        with open(gpu_device_path + "device/pp_dpm_sclk") as reader:
            gpu_frequency_file_output = reader.read().strip().split("\n")
    except FileNotFoundError:
        gpu_current_frequency = "-"
        gpu_max_frequency = "-"
        gpu_min_frequency = "-"

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

    # Get GPU used memory (data in this file is in Bytes). There is also "mem_info_vis_vram_used" file
    # for visible memory (can be shown on the "lspci" command) and "mem_info_gtt_used" file for reserved memory
    # from system memory. gtt+vram=total video memory. Probably "mem_busy_percent" is for memory controller load.
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

    # Get GPU temperature
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

    # Get GPU current power usage
    try:
        gpu_sensor_list = os.listdir(gpu_device_path + "device/hwmon/")
        for sensor in gpu_sensor_list:
            if os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_input") == True:
                with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_input") as reader:
                    gpu_power_current = reader.read().strip()
                # Value in this file is in microwatts.
                gpu_power_current = f'{(int(gpu_power_current) / 1000000):.2f} W'
            elif os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_average") == True:
                with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_average") as reader:
                    gpu_power_current = reader.read().strip()
                gpu_power_current = f'{(int(gpu_power_current) / 1000000):.2f} W'
            else:
                gpu_power_current = "-"
    except (FileNotFoundError, NotADirectoryError, OSError) as me:
        gpu_power_current = "-"

    # Get GPU max power usage
    try:
        gpu_sensor_list = os.listdir(gpu_device_path + "device/hwmon/")
        for sensor in gpu_sensor_list:
            if os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_cap") == True:
                # "power1_cap" file contains selected power cap value. It may be editable.
                # "power1_cap_max" file contains max supported power cap value.
                with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_cap") as reader:
                    gpu_power_max = reader.read().strip()
                # Value in this file is in microwatts.
                gpu_power_max = f'{(int(gpu_power_max) / 1000000):.2f} W'
            else:
                gpu_power_max = "-"
    except (FileNotFoundError, NotADirectoryError, OSError) as me:
        gpu_power_max = "-"

    # Get GPU memory current, min, max frequencies
    gpu_memory_current_frequency, gpu_memory_min_frequency, gpu_memory_max_frequency = get_gpu_memory_current_min_max_frequency_amd_gpu(gpu_device_path)

    gpu_load_memory_frequency_power_dict = {
                                            "gpu_load" : gpu_load,
                                            "gpu_encoder_load": gpu_encoder_load,
                                            "gpu_decoder_load": gpu_decoder_load,
                                            "gpu_memory_used" : gpu_memory_used,
                                            "gpu_memory_capacity" : gpu_memory_capacity,
                                            "gpu_current_frequency" : gpu_current_frequency,
                                            "gpu_min_frequency" : gpu_min_frequency,
                                            "gpu_max_frequency" : gpu_max_frequency,
                                            "gpu_memory_current_frequency" : gpu_memory_current_frequency,
                                            "gpu_memory_min_frequency" : gpu_memory_min_frequency,
                                            "gpu_memory_max_frequency" : gpu_memory_max_frequency,
                                            "gpu_temperature" : gpu_temperature,
                                            "gpu_power_current" : gpu_power_current,
                                            "gpu_power_max" : gpu_power_max,
                                            "gpu_driver_version" : gpu_driver_version
                                            }

    return gpu_load_memory_frequency_power_dict


def gpu_load_amd_func(gpu_device_path, event):
    """
    Get GPU load average for AMD GPUs.
    """

    while True:

        if event.is_set():
            break

        # Read file to get GPU load information. This information is calculated for a very small
        # time (screen refresh rate or content (game, etc.) refresh rate?) and directly plotting this data gives spikes.
        try:
            with open(gpu_device_path + "device/gpu_busy_percent") as reader:
                gpu_load = reader.read().strip()
        except Exception:
            gpu_load = 0

        # Add GPU load data into a list in order to calculate average of the list.
        global amd_gpu_load_list
        amd_gpu_load_list.append(float(gpu_load))
        del amd_gpu_load_list[0]

        time.sleep(amd_gpu_load_read_frequency)


def gpu_encoder_decoder_load_amd_func():
    """
    Get video encoder/decoder engine loads of AMD GPUs by using "amdgpu_top" tool.
    This is a 3rd party tool. GPU, video engine loads, etc. are get as intermittent data
    if this tool is run repeatedly by using its single loop mode.
    This tool uses its update interval for calculating these loads.
    """

    command_list = ["amdgpu_top", "-J", "-s", "100ms", "-n", "1"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    global gpu_tool_output_amdgpu_top
    try:
        gpu_tool_output_amdgpu_top = (subprocess.check_output(command_list, shell=False)).decode().strip()
        import json
        gpu_tool_output_amdgpu_top = json.loads(gpu_tool_output_amdgpu_top)
    # Prevent errors because "amdgpu_top" may not be installed on systems.
    except Exception:
        pass


def process_gpu_tool_output_amdgpu_top(gpu_pci_address, gpu_tool_output_amdgpu_top, gpu_load_memory_frequency_power_dict):
    """
    Get values from command output if there was no error when running the command.
    """

    # Define initial values
    gpu_encoder_load = "-"
    gpu_decoder_load = "-"

    not_supported_text = ["[Not Supported]", "[N/A]", "null", "Null", "NULL", "None"]

    if gpu_tool_output_amdgpu_top != "-":
        all_gpus_information = gpu_tool_output_amdgpu_top["devices"]
        for gpu_information in all_gpus_information:
            if gpu_pci_address != gpu_information["Info"]["PCI"]:
                continue
            try:
                media_engine_load = gpu_information["gpu_activity"]["MediaEngine"]
                #media_engine_load_unit = media_engine_load["unit"]
                media_engine_load_value = float(media_engine_load["value"])
            except KeyError:
                pass

            if media_engine_load_value == 65535 or media_engine_load_value in not_supported_text:
                pass
            else:
                gpu_encoder_load = f'{float(media_engine_load_value):.0f} %'
                gpu_decoder_load = "-9999 %"

    # A single video engine load is get for some AMD GPUs.
    # Because AMD GPUs have a single engine (VCN)4 for video encoding and decoding after 2022.
    # In this case, video engine load value is tracked by "gpu_encoder_load" variable.
    # "gpu_decoder_load" variable ise set as "-9999 %". Code using this function may recognize that
    # there is a single video engine load value.
    gpu_load_memory_frequency_power_dict["gpu_encoder_load"] = gpu_encoder_load
    gpu_load_memory_frequency_power_dict["gpu_decoder_load"] = gpu_decoder_load

    return gpu_load_memory_frequency_power_dict



def get_process_gpu_information():

    gpu_process_information_dict = {}

    # Get encoder/decoder engine load of AMD GPU by using "amdgpu_top" tool.
    threading.Thread(target=gpu_process_information_amd_func, daemon=True).start()

    global gpu_tool_process_output_amdgpu_top
    try:
        check_value = gpu_tool_process_output_amdgpu_top
    except NameError:
        gpu_tool_process_output_amdgpu_top = "-"

    # Update encoder/decoder engine load values. Because they are not get in "get_gpu_load_memory_frequency_power_amd" function.
    gpu_process_information_dict = process_gpu_tool_process_output_amdgpu_top(gpu_tool_process_output_amdgpu_top, gpu_process_information_dict)


def gpu_process_information_amd_func():

    command_list = ["amdgpu_top", "-J", "-s", "100ms", "-n", "1"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    global gpu_tool_process_output_amdgpu_top
    try:
        gpu_tool_process_output_amdgpu_top = (subprocess.check_output(command_list, shell=False)).decode().strip()
        import json
        gpu_tool_process_output_amdgpu_top = json.loads(gpu_tool_process_output_amdgpu_top)
    # Prevent errors because "amdgpu_top" may not be installed on systems.
    except Exception:
        pass


def process_gpu_tool_process_output_amdgpu_top(gpu_tool_process_output_amdgpu_top, gpu_process_information_dict):
    """
    Get values from command output if there was no error when running the command.
    """

    not_supported_text = ["[Not Supported]", "[N/A]", "null", "Null", "NULL", "None", 65535]

    if gpu_tool_process_output_amdgpu_top != "-":
        all_gpus_information = gpu_tool_process_output_amdgpu_top["devices"]
        for gpu_information in all_gpus_information:
            all_processes_gpu_information = gpu_information["fdinfo"]
            for pid in all_processes_gpu_information:
                process_gpu_information = all_processes_gpu_information[pid]["usage"]
                try:
                    gpu_load_information = process_gpu_information["GFX"]
                    #gpu_load_unit = gpu_load_information["unit"]
                    gpu_usage = float(gpu_load_information["value"])
                    gpu_memory_information = process_gpu_information["VRAM"]
                    gpu_memory_unit = gpu_memory_information["unit"]
                    gpu_memory = float(gpu_memory_information["value"]) 
                    gpu_memory = get_memory_bytes_from_string(f'{gpu_memory} {gpu_memory_unit}')
                except KeyError:
                    pass

                if gpu_usage in not_supported_text:
                    gpu_usage = 0
                if gpu_memory in not_supported_text:
                    gpu_memory = 0

                pid = int(pid)
                if pid not in gpu_process_information_dict:
                    gpu_process_information_dict[pid] = {"gpu_usage": gpu_usage, "gpu_memory": gpu_memory}
                else:
                    gpu_process_information_dict[pid]["gpu_usage"] = gpu_process_information_dict[pid]["gpu_usage"] + gpu_usage
                    gpu_process_information_dict[pid]["gpu_memory"] = gpu_process_information_dict[pid]["gpu_memory"] + gpu_memory

    return gpu_process_information_dict



def gpu_load_nvidia_func():
    """
    Get GPU load average for NVIDIA (PCI) GPUs.
    """

    command_list = ["nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,utilization.encoder,utilization.decoder,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,clocks.current.memory,clocks.max.memory,power.draw,power.limit,enforced.power.limit", "--format=csv"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    global gpu_tool_output_nvidia_smi, nvidia_smi_encoder_decoder
    try:
        nvidia_smi_encoder_decoder = 1
        gpu_tool_output_nvidia_smi = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
    # Prevent errors because "nvidia-smi" may not be installed on some devices (such as N.Switch with NVIDIA Tegra GPU).
    except Exception:
        nvidia_smi_encoder_decoder = 0
        command_list = ["nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,clocks.current.memory,clocks.max.memory,power.draw,power.limit,enforced.power.limit", "--format=csv"]
        if get_environment_type() == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        try:
            gpu_tool_output_nvidia_smi = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        # Prevent errors because "nvidia-smi" may not be installed on some devices (such as N.Switch with NVIDIA Tegra GPU).
        except Exception:
            pass


def process_gpu_tool_output_nvidia(gpu_pci_address, gpu_tool_output_nvidia_smi, nvidia_smi_encoder_decoder):
    """
    Get values from command output if there was no error when running the command.
    """

    # Define initial values
    gpu_load = "-"
    gpu_encoder_load = "-"
    gpu_decoder_load = "-"
    gpu_memory_used = "-"
    gpu_memory_capacity = "-"
    gpu_current_frequency = "-"
    gpu_min_frequency = "-"
    gpu_max_frequency = "-"
    gpu_memory_current_frequency = "-"
    gpu_memory_min_frequency = "-"
    gpu_memory_max_frequency = "-"
    gpu_temperature = "-"
    gpu_power_current = "-"
    gpu_power_max = "-"
    gpu_driver_version = "-"

    gpu_enforced_power_limit = "-"

    if gpu_tool_output_nvidia_smi != "-":

        # Get line number of the selected GPU by using its PCI address.
        for i, line in enumerate(gpu_tool_output_nvidia_smi):
            if gpu_pci_address in line or gpu_pci_address.upper() in line:
                gpu_info_line_no = i
                break

        gpu_tool_output_for_selected_gpu = gpu_tool_output_nvidia_smi[gpu_info_line_no].split(",")

        if len(gpu_tool_output_for_selected_gpu) == 18:
            gpu_driver_version = gpu_tool_output_for_selected_gpu[2].strip()
            gpu_load = gpu_tool_output_for_selected_gpu[3].strip()
            gpu_encoder_load = gpu_tool_output_for_selected_gpu[5].strip()
            gpu_decoder_load = gpu_tool_output_for_selected_gpu[6].strip()
            gpu_memory_capacity = gpu_tool_output_for_selected_gpu[7].strip()
            gpu_memory_used = gpu_tool_output_for_selected_gpu[9].strip()
            gpu_temperature = gpu_tool_output_for_selected_gpu[10].strip()
            gpu_current_frequency = gpu_tool_output_for_selected_gpu[11].strip()
            gpu_max_frequency = gpu_tool_output_for_selected_gpu[12].strip()
            gpu_memory_current_frequency = gpu_tool_output_for_selected_gpu[13].strip()
            gpu_memory_max_frequency = gpu_tool_output_for_selected_gpu[14].strip()
            gpu_power_current = gpu_tool_output_for_selected_gpu[15].strip()
            gpu_power_max = gpu_tool_output_for_selected_gpu[16].strip()
            gpu_enforced_power_limit = gpu_tool_output_for_selected_gpu[17].strip()
        if len(gpu_tool_output_for_selected_gpu) == 16:
            gpu_driver_version = gpu_tool_output_for_selected_gpu[2].strip()
            gpu_load = gpu_tool_output_for_selected_gpu[3].strip()
            gpu_memory_capacity = gpu_tool_output_for_selected_gpu[5].strip()
            gpu_memory_used = gpu_tool_output_for_selected_gpu[7].strip()
            gpu_temperature = gpu_tool_output_for_selected_gpu[8].strip()
            gpu_current_frequency = gpu_tool_output_for_selected_gpu[9].strip()
            gpu_max_frequency = gpu_tool_output_for_selected_gpu[10].strip()
            gpu_memory_current_frequency = gpu_tool_output_for_selected_gpu[11].strip()
            gpu_memory_max_frequency = gpu_tool_output_for_selected_gpu[12].strip()
            gpu_power_current = gpu_tool_output_for_selected_gpu[13].strip()
            gpu_power_max = gpu_tool_output_for_selected_gpu[14].strip()
            gpu_enforced_power_limit = gpu_tool_output_for_selected_gpu[15].strip()

        not_supported_text = ["[Not Supported]", "[N/A]"]

        if gpu_driver_version in not_supported_text:
            gpu_driver_version = "-"
        if gpu_load in not_supported_text:
            gpu_load = "-"
        if gpu_encoder_load in not_supported_text:
            gpu_encoder_load = "-"
        if gpu_decoder_load in not_supported_text:
            gpu_decoder_load = "-"
        if gpu_memory_capacity in not_supported_text:
            gpu_memory_capacity = "-"
        if gpu_memory_used in not_supported_text:
            gpu_memory_used = "-"
        if gpu_temperature in not_supported_text:
            gpu_temperature = "-"
        if gpu_current_frequency in not_supported_text:
            gpu_current_frequency = "-"
        if gpu_max_frequency in not_supported_text:
            gpu_max_frequency = "-"
        if gpu_memory_current_frequency in not_supported_text:
            gpu_memory_current_frequency = "-"
        if gpu_memory_min_frequency in not_supported_text:
            gpu_memory_min_frequency = "-"
        if gpu_memory_max_frequency in not_supported_text:
            gpu_memory_max_frequency = "-"
        if gpu_power_current in not_supported_text:
            gpu_power_current = "-"
        if gpu_power_max in not_supported_text:
            gpu_power_max = "-"
        if gpu_enforced_power_limit in not_supported_text:
            gpu_enforced_power_limit = "-"

    try:
        gpu_temperature = float(gpu_temperature)
        gpu_temperature = f'{gpu_temperature:.0f} °C'
    except ValueError:
        pass

    # Use enforced power limit value if power max value is not get.
    if gpu_power_max == "-":
        gpu_power_max = gpu_enforced_power_limit

    gpu_load_memory_frequency_power_dict = {
                                            "gpu_load" : gpu_load,
                                            "gpu_encoder_load": gpu_encoder_load,
                                            "gpu_decoder_load": gpu_decoder_load,
                                            "gpu_memory_used" : gpu_memory_used,
                                            "gpu_memory_capacity" : gpu_memory_capacity,
                                            "gpu_current_frequency" : gpu_current_frequency,
                                            "gpu_min_frequency" : gpu_min_frequency,
                                            "gpu_max_frequency" : gpu_max_frequency,
                                            "gpu_memory_current_frequency" : gpu_memory_current_frequency,
                                            "gpu_memory_min_frequency" : gpu_memory_min_frequency,
                                            "gpu_memory_max_frequency" : gpu_memory_max_frequency,
                                            "gpu_temperature" : gpu_temperature,
                                            "gpu_power_current" : gpu_power_current,
                                            "gpu_power_max" : gpu_power_max,
                                            "gpu_driver_version" : gpu_driver_version
                                            }

    return gpu_load_memory_frequency_power_dict


def get_gpu_memory_usage_percentage(gpu_memory_used, gpu_memory_capacity):
    """
    Get GPU memory usage percentage.
    """

    if gpu_memory_used == "-" or gpu_memory_capacity == "-":
        gpu_memory_usage_percentage = 0

    else:
        gpu_memory_used_bytes = get_memory_bytes_from_string(gpu_memory_used)
        gpu_memory_capacity_bytes = get_memory_bytes_from_string(gpu_memory_capacity)
        gpu_memory_usage_percentage = gpu_memory_used_bytes / gpu_memory_capacity_bytes * 100

    return gpu_memory_usage_percentage


def get_memory_bytes_from_string(memory_string):
    """
    Get memory value in bytes unit by processing string value. Example: 5 MiB.
    """

    memory_number, memory_unit = memory_string.split(" ", 1)

    if memory_unit in ["KB", "KiB", "kb", "kib"]:
        memory_divisor = 1024
    elif memory_unit in ["MB", "MiB", "mb", "mib"]:
        memory_divisor = 1024 * 1024
    elif memory_unit in ["GB", "GiB", "gb", "gib"]:
        memory_divisor = 1024 * 1024 * 1024
    elif memory_unit in ["TB", "TiB", "tb", "tib"]:
        memory_divisor = 1024 * 1024 * 1024 * 1024

    memory_bytes = float(memory_number) * memory_divisor
    memory_bytes = round(memory_bytes)

    return memory_bytes


def get_gpu_memory_current_min_max_frequency_amd_gpu(gpu_device_path):
    """
    Get current, minimum and maximum memory frequencies of AMD GPUs.
    """

    # For more information about files under "/sys/class/drm/card[NUMBER]/device/" and their content
    # for AMD GPUs: https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html and https://wiki.archlinux.org/title/AMDGPU

    # Get GPU current, min, max frequencies (memory frequencies). This file contains all available
    # frequencies of the GPU memory.
    gpu_memory_frequency_file_output = "-"
    try:
        with open(gpu_device_path + "device/pp_dpm_mclk") as reader:
            gpu_memory_frequency_file_output = reader.read().strip().split("\n")
    except FileNotFoundError:
        gpu_memory_current_frequency = "-"
        gpu_memory_max_frequency = "-"
        gpu_memory_min_frequency = "-"

    if gpu_memory_frequency_file_output != "-":
        for line in gpu_memory_frequency_file_output:
            if "*" in line:
                gpu_memory_current_frequency = line.split(":")[1].rstrip("*").strip()
                # Add a space character between value and unit. "Mhz" is used in the relevant file instead of "MHz".
                if "Mhz" in gpu_memory_current_frequency:
                    gpu_memory_current_frequency = gpu_memory_current_frequency.split("Mhz")[0] + " MHz"
                break
        gpu_memory_min_frequency = gpu_memory_frequency_file_output[0].split(":")[1].strip()
        # Add a space character between value and unit.
        if "Mhz" in gpu_memory_min_frequency:
            gpu_memory_min_frequency = gpu_memory_min_frequency.split("Mhz")[0] + " MHz"
        gpu_memory_max_frequency = gpu_memory_frequency_file_output[-1].split(":")[1].strip()
        # Add a space character between value and unit.
        if "Mhz" in gpu_memory_max_frequency:
            gpu_memory_max_frequency = gpu_memory_max_frequency.split("Mhz")[0] + " MHz"

    return gpu_memory_current_frequency, gpu_memory_min_frequency, gpu_memory_max_frequency


def get_gpu_current_link_speed(gpu_device_path):

    try:
        with open(gpu_device_path + "device/current_link_speed") as reader:
            current_link_speed = reader.read().strip()
    except Exception:
        current_link_speed = "-"

    current_link_speed = process_gpu_link_speed(current_link_speed)

    return current_link_speed


def get_gpu_max_link_speed(gpu_device_path):

    try:
        with open(gpu_device_path + "device/max_link_speed") as reader:
            max_link_speed = reader.read().strip()
    except Exception:
        max_link_speed = "-"

    max_link_speed = process_gpu_link_speed(max_link_speed)

    return max_link_speed


def process_gpu_link_speed(gpu_link_speed):

    if gpu_link_speed in ["Unknown", "unknown", ""]:
        gpu_link_speed = "-"

    if gpu_link_speed.endswith("PCIe") == True:
        gpu_link_speed = gpu_link_speed.rstrip(" PCIe")

    return gpu_link_speed


def get_gpu_current_link_width(gpu_device_path):

    try:
        with open(gpu_device_path + "device/current_link_width") as reader:
            current_link_width = reader.read().strip()
    except Exception:
        current_link_width = "-"

    return current_link_width


def get_gpu_max_link_width(gpu_device_path):

    try:
        with open(gpu_device_path + "device/max_link_width") as reader:
            max_link_width = reader.read().strip()
    except Exception:
        max_link_width = "-"

    return max_link_width


def get_gpu_pci_express_version(gpu_device_path):

    max_link_speed = get_gpu_max_link_speed(gpu_device_path)
    if max_link_speed != "-":
        max_link_speed_split = max_link_speed.split(" ")
        max_link_speed_number = max_link_speed_split[0]
        max_link_speed_unit = max_link_speed_split[1]
    else:
        max_link_speed_unit = "-"

    if max_link_speed_unit in ["GT/s", "GT/S", "gt/s"]:
        gpu_pci_express_version = gpu_pci_express_version_dict[max_link_speed_number]
    else:
        gpu_pci_express_version = "-"

    return gpu_pci_express_version


def get_gpu_interface(gpu_device_path):

    gpu_pci_express_version = get_gpu_pci_express_version(gpu_device_path)
    max_link_width = get_gpu_max_link_width(gpu_device_path)

    if gpu_pci_express_version != "-":
        if max_link_width != "-":
            gpu_interface = gpu_pci_express_version + " x" + max_link_width
        else:
            gpu_interface = gpu_pci_express_version
    else:
        gpu_interface = "-"

    return gpu_interface


def get_gpu_connections(gpu_device_path, selected_gpu):
    """
    Get GPU display connections.
    """

    try:
        file_list = os.listdir(gpu_device_path)
    except Exception:
        file_list = "-"

    # Get connection name if file starts with GPU name and it is a folder.
    if file_list != "-":
        gpu_connections_list = []
        for file_name in file_list:
            if file_name.startswith(selected_gpu + "-") == True:
                if os.path.isdir(gpu_device_path + file_name) == True:
                    connection_name = file_name.split("-", 1)[-1]
                    gpu_connections_list.append(connection_name)
        gpu_connections = ', '.join(gpu_connections_list)
    else:
        gpu_connections = "-"

    return gpu_connections


# ***********************************************************************************************
#                                           Sensors
# ***********************************************************************************************

def get_sensors_information(temperature_unit="celsius"):
    """
    Get sensor information.
    """

    # Get sensor group names. In some sensor directories there are a name file and multiple label files.
    # For example, name: "coretemp", label: "Core 0", "Core 1", ... For easier grouping and understanding
    # name is used as "Sensor Group" name and labels are used as "Sensor" names.
    sensors_data_dict = {}
    sensor_count = 0
    sensor_unique_id_list = []
    sensor_groups = sorted(os.listdir("/sys/class/hwmon/"))
    sensor_group_names = []
    for sensor_group in sensor_groups:
        files_in_sensor_group = os.listdir("/sys/class/hwmon/" + sensor_group)
        for attribute in supported_sensor_attributes:
            sensor_number = 0
            # Continue loop until code breaks it when next sensor data is not available in the folder.
            while True:
                string_sensor_number = str(sensor_number)
                # Some sensor groups have both label and input files. Some sensor groups have only label or only input files.
                # Some sensor groups do not have label or input files, but they have name files. Data of sensor groups
                # with only name files are not get because they do not have sensor values.
                if (attribute + string_sensor_number + "_label" not in files_in_sensor_group) and (attribute + string_sensor_number + "_input" not in files_in_sensor_group):
                    # Number in sensor names may start from 0 or 1. Skipped to next loop if number is 0.
                    if sensor_number == 0:
                        sensor_number = sensor_number + 1
                        continue
                    # Number in sensor names may start from 0 or 1. Loop is broken if number is bigger than 1.
                    if sensor_number > 0:
                        break

                # Get device name
                with open("/sys/class/hwmon/" + sensor_group + "/name") as reader:
                    sensor_group_name = reader.read().strip()
                if attribute == "temp":
                    sensor_type = "temperature"
                elif attribute == "fan":
                    sensor_type = "fan"
                elif attribute in ["in", "curr", "power"]:
                    sensor_type = "voltage_current_power"

                # Get device detailed name
                device_path = os.readlink("/sys/class/hwmon/" + sensor_group)
                device_detailed_name = device_path.split("/")[-2]
                if device_detailed_name.startswith("hwmon") == True:
                    device_detailed_name = device_path.split("/")[-3]
                    if device_detailed_name.startswith("hwmon") == True:
                        device_detailed_name = "-"
                if device_detailed_name != "-" and device_detailed_name.startswith("0000:") == False:
                    sensor_group_name = device_detailed_name + " ( " + sensor_group_name + " )"

                # Get sensor name
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_label") as reader:
                        sensor_name = reader.read().strip()
                except OSError:
                    sensor_name = "-"

                # Get sensor current value
                try:
                    # Units of data in this file are millidegree Celsius for temperature sensors, RPM for fan sensors,
                    # millivolt for voltage sensors and milliamper for current sensors.
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_input") as reader:
                        current_value = int(reader.read().strip())
                    if attribute == "temp":
                        if temperature_unit == "celsius":
                            # Convert millidegree Celsius to degree Celsius
                            current_value = f'{(current_value / 1000):.0f} °C'
                        elif temperature_unit == "fahrenheit":
                            current_value = f'{((current_value / 1000)*9/5)+32:.0f} °F'
                    if attribute == "fan":
                        current_value = f'{current_value} RPM'
                    if attribute == "in":
                        # Convert millivolt to Volt
                        current_value = f'{(current_value / 1000):.3f} V'
                    if attribute == "curr":
                        # Convert milliamper to Amper
                        current_value = f'{(current_value / 1000):.3f} A'
                    if attribute == "power":
                        # Convert microwatt to Watt
                        current_value = f'{(current_value / 1000000):.3f} W'
                except OSError:
                    current_value = "-"

                # Get sensor high value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_max") as reader:
                        max_value = int(reader.read().strip())
                    if attribute == "temp":
                        if temperature_unit == "celsius":
                            max_value = f'{(max_value / 1000):.0f} °C'
                        elif temperature_unit == "fahrenheit":
                            max_value = f'{((max_value / 1000)*9/5)+32:.0f} °F'
                    if attribute == "fan":
                        max_value = f'{max_value} RPM'
                    if attribute == "in":
                        max_value = f'{(max_value / 1000):.3f} V'
                    if attribute == "curr":
                        max_value = f'{(max_value / 1000):.3f} A'
                    if attribute == "power":
                        max_value = f'{(max_value / 1000000):.3f} W'
                except OSError:
                    max_value = "-"

                # Get sensor critical value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_crit") as reader:
                        critical_value = int(reader.read().strip())
                    if attribute == "temp":
                        if temperature_unit == "celsius":
                            critical_value = f'{(critical_value / 1000):.0f} °C'
                        elif temperature_unit == "fahrenheit":
                            critical_value = f'{((critical_value / 1000)*9/5)+32:.0f} °F'
                    if attribute == "fan":
                        critical_value = f'{critical_value} RPM'
                    if attribute == "in":
                        critical_value = f'{(critical_value / 1000):.3f} V'
                    if attribute == "curr":
                        critical_value = f'{(critical_value / 1000):.3f} A'
                    if attribute == "power":
                        critical_value = f'{(critical_value / 1000000):.3f} W'
                except OSError:
                    critical_value = "-"

                # Add sensor data to a sub-dictionary
                sensor_data_dict = {
                                    "sensor_type": sensor_type,
                                    "sensor_group_name" : sensor_group_name,
                                    "sensor_name" : sensor_name,
                                    "current_value" : current_value,
                                    "max_value" : max_value,
                                    "critical_value" : critical_value
                                    }

                # Increase sensor number by "1" in order to use this value for getting next file names of the sensor.
                sensor_number = sensor_number + 1

                sensor_count = sensor_count + 1
                sensor_unique_id = "sensor_" + str(sensor_count)

                sensor_unique_id_list.append(sensor_unique_id)

                # Add sensor sub-dictionary to dictionary
                sensors_data_dict[sensor_unique_id] = sensor_data_dict

    # Add sensor related lists and variables
    sensors_data_dict["sensor_unique_id_list"] = sensor_unique_id_list

    return sensors_data_dict


# ***********************************************************************************************
#                                           Processes
# ***********************************************************************************************

def get_fd_task_ls_output(process_pid):
    """
    Get fd and stat folder list outputs.
    """

    # Generate command for getting file outputs
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host", "ls"]
    else:
        command_list = ["ls"]
    command_list.append(f'/proc/{process_pid}/fd/')
    command_list.append(f'/proc/{process_pid}/task/')

    ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()

    # Get output of procfs folders
    if "/fd/" in ls_output and "/task/" in ls_output:
        fd_ls_output, task_ls_output = ls_output.split("\n\n")
    elif "/fd/" in ls_output and "/task/" not in ls_output:
        fd_ls_output = ls_output
        task_ls_output = "-"
    elif "/fd/" not in ls_output and "/task/" in ls_output:
        fd_ls_output = "-"
        task_ls_output = ls_output
    else:
        fd_ls_output = "-"
        task_ls_output = "-"

    return fd_ls_output, task_ls_output


def get_process_tids(task_ls_output):
    """
    Get thread IDs (TIDs) of the process.
    """

    task_ls_output_lines = task_ls_output.split("\n")
    process_threads = [filename for filename in task_ls_output_lines if filename.isdigit()]
    process_threads = sorted(process_threads, key=int)

    return process_threads


def get_process_exe_cwd_open_files(process_pid, fd_ls_output):
    """
    Get process cwd and open files.
    """

    command_list = ["readlink"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    # "/proc/self" folder will be used for splitting the "readlink" command output
    command_list.append("/proc/self")

    # Get process exe path
    process_exe_path = f'/proc/{process_pid}/exe'
    command_list.append(process_exe_path)

    # Append command for splitting command output
    command_list.append("/proc/self")

    # Get process cwd path
    process_cwd_path = f'/proc/{process_pid}/cwd'
    command_list.append(process_cwd_path)

    # Append command for splitting command output
    command_list.append("/proc/self")

    # Get process fd path list
    fd_ls_output_lines = fd_ls_output.split("\n")
    process_fds = [filename for filename in fd_ls_output_lines if filename.isdigit()]
    process_fds = sorted(process_fds, key=int)

    process_fd_paths = []
    for fd in process_fds:
        process_fd_paths.append(f'/proc/{process_pid}/fd/' + fd)

    if process_fd_paths == []:
        process_fd_paths = "-"

    # Append command list for process open files
    if process_fd_paths != "-":
        for path in process_fd_paths:
            command_list.append(path)

    # Get "readlink" command output
    readlink_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()
    readlink_output_lines = readlink_output.split("\n")

    # Split the "readlink" command output
    split_text = readlink_output_lines[0].strip()
    readlink_output_split = readlink_output.split(split_text)
    del readlink_output_split[0]

    # Get process exe
    process_exe = readlink_output_split[0].strip()
    if process_exe == "":
        process_exe = "-"

    # Get process cwd
    process_cwd = readlink_output_split[1].strip()
    if process_cwd == "":
        process_cwd = "-"

    # Get process open files list
    process_open_files = []
    readlink_output_split = readlink_output_split[2].strip().split("\n")
    for file in readlink_output_split:
        file_strip = file.strip()
        # Prevent adding lines which are not files
        if file_strip.count("/") > 1:
            process_open_files.append(file_strip)

    if process_open_files == []:
        process_open_files = "-"

    return process_exe, process_cwd, process_open_files


def get_username_uid_dict():
    """
    Get usernames and UIDs.
    """

    environment_type = get_environment_type()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    username_uid_dict = {}
    for line in etc_passwd_lines:
        line_splitted = line.split(":", 3)
        username_uid_dict[int(line_splitted[2])] = line_splitted[0]

    return username_uid_dict


def get_application_name_image_dict():
    """
    Get application names and images. Process name will be searched in "application_image_dict" list.
    """

    application_image_dict = {}

    # Get ".desktop" file names
    application_file_list = [file for file in os.listdir("/usr/share/applications/") if file.endswith(".desktop")]

    # Get application name and image information
    for application in application_file_list:

        # "encoding="utf-8"" is used for preventing "UnicodeDecodeError" errors during reading the file content if "C" locale is used.
        try:
            with open("/usr/share/applications/" + application, encoding="utf-8") as reader:
                application_file_content = reader.read()
        except (PermissionError, FileNotFoundError) as e:
            continue

        # Do not include application name or icon name if any of them is not found in the .desktop file.
        if "Exec=" not in application_file_content or "Icon=" not in application_file_content:
            continue

        # Get application exec data
        application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0].split("/")[-1].split(" ")[0]
        # Splitting operation above may give "sh" as application name and this may cause confusion between "sh" process
        # and splitted application exec (for example: sh -c "gdebi-gtk %f"sh -c "gdebi-gtk %f").
        # This statement is used to avoid from this confusion.
        if application_exec == "sh":
            application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0]

        # Get application image name data
        application_image = application_file_content.split("Icon=", 1)[1].split("\n", 1)[0]

        """# Get "desktop_application/application" information
        if "NoDisplay=" in application_file_content:
            desktop_application_value = application_file_content.split("NoDisplay=", 1)[1].split("\n", 1)[0]
            if desktop_application_value == "true":
                application_type = "application"
            if desktop_application_value == "false":
                application_type = "desktop_application"
        else:
            application_type = "desktop_application"
        """

        application_image_dict[application_exec] = application_image

    return application_image_dict


def get_process_priority(process_pid):
    """
    Get process priority (nice).
    """

    process_stat_file = "/proc/" + str(process_pid) + "/stat"
    command_list = ["cat", process_stat_file]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()

    # Process may be ended just after pid_list is generated. "cat" command output is get as "" in this situation.
    if cat_output != "":
        selected_process_nice = int(cat_output.split()[-34])
    else:
        selected_process_nice = "-"

    return selected_process_nice


def change_process_priority(process_list, priority_option):
    """
    Change priority (nice) of process.
    """

    process_pid_list_str = []
    for process_pid in process_list:
        process_pid_list_str.append(str(process_pid))

    if priority_option == "priority_very_high":
        priority_command = ["renice", "-n", "-20", "-p"]
        priority_command_pkexec = ["pkexec", "renice", "-n", "-20", "-p"]
    elif priority_option == "priority_high":
        priority_command = ["renice", "-n", "-10", "-p"]
        priority_command_pkexec = ["pkexec", "renice", "-n", "-10", "-p"]
    elif priority_option == "priority_normal":
        priority_command = ["renice", "-n", "0", "-p"]
        priority_command_pkexec = ["pkexec", "renice", "-n", "0", "-p"]
    elif priority_option == "priority_low":
        priority_command = ["renice", "-n", "10", "-p"]
        priority_command_pkexec = ["pkexec", "renice", "-n", "10", "-p"]
    elif priority_option == "priority_very_low":
        priority_command = ["renice", "-n", "19", "-p"]
        priority_command_pkexec = ["pkexec", "renice", "-n", "19", "-p"]
    else:
        process_priority = priority_option
        priority_command = ["renice", "-n", process_priority, "-p"]
        priority_command_pkexec = ["pkexec", "renice", "-n", process_priority, "-p"]

    priority_command = priority_command + process_pid_list_str
    priority_command_pkexec = priority_command_pkexec + process_pid_list_str

    if get_environment_type() == "flatpak":
        priority_command = ["flatpak-spawn", "--host"] + priority_command
        priority_command_pkexec = ["flatpak-spawn", "--host"] + priority_command_pkexec

    # Try to change priority of the process.
    try:
        (subprocess.check_output(priority_command, stderr=subprocess.STDOUT, shell=False)).decode()
        # Stop running the function if process priority is changed without root privileges.
        return
    except subprocess.CalledProcessError:
        # Try to change priority of the process if root privileges are required.
        try:
            (subprocess.check_output(priority_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
        except subprocess.CalledProcessError:
            return


def get_process_cpu_affinity(process_pid):
    """
    Get process CPU affinity.
    """

    command_list = ["taskset", "-pc", process_pid]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    taskset_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()

    # Process may be ended just after pid_list is generated. "cat" command output is get as "" in this situation.
    if taskset_output.startswith("taskset: ") == True:
        selected_process_cpu_affinity = "-"
    else:
        selected_process_cpu_affinity = []
        selected_process_cpu_affinity_list = taskset_output.split(": ")[-1]
        selected_process_cpu_affinity_list = selected_process_cpu_affinity_list.split(",")
        for cpu_affinity_sub_list in selected_process_cpu_affinity_list:
            if "-" in cpu_affinity_sub_list:
                cpu_affinity_range_start, cpu_affinity_range_end = cpu_affinity_sub_list.split("-")
                cpu_affinity_sub_list_processed = list(range(int(cpu_affinity_range_start), int(cpu_affinity_range_end)+1))
                selected_process_cpu_affinity.extend(cpu_affinity_sub_list_processed)
            else:
                selected_process_cpu_affinity.append(int(cpu_affinity_sub_list))

    return selected_process_cpu_affinity


def set_process_cpu_affinity(process_list, cpu_core_list):
    """
    Set CPU affinity of process.
    """

    process_pid_list_str = []
    for process_pid in process_list:
        process_pid_list_str.append(str(process_pid))


    cpu_core_list_str = []
    for cpu_core in cpu_core_list:
        cpu_core_list_str.append(str(cpu_core))
    cpu_core_list_str_joined = ','.join(cpu_core_list_str)

    for pid in process_pid_list_str:
        command_list = ["taskset", "-pc", cpu_core_list_str_joined, pid]
        command_list_pkexec = ["pkexec", "taskset", "-pc", cpu_core_list_str_joined, pid]

        if get_environment_type() == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
            command_list_pkexec = ["flatpak-spawn", "--host"] + command_list_pkexec

        # Try to change priority of the process.
        try:
            (subprocess.check_output(command_list, stderr=subprocess.STDOUT, shell=False)).decode()
            # Stop running the function if process priority is changed without root privileges.
            return
        except subprocess.CalledProcessError:
            # Try to change priority of the process if root privileges are required.
            try:
                (subprocess.check_output(command_list_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                return


def manage_process(process_list, manage_option):
    """
    Manage (pause, continue, end, end immediately) processes.
    """

    process_pid_list_str = []
    for process_pid in process_list:
        process_pid_list_str.append(str(process_pid))

    if manage_option == "pause_process":
        process_command = ["kill", "-19"]
        process_command_pkexec = ["pkexec", "kill", "-19"]

    elif manage_option == "continue_process":
        process_command = ["kill", "-18"]
        process_command_pkexec = ["pkexec", "kill", "-18"]

    elif manage_option == "end_process":
        process_command = ["kill", "-15"]
        process_command_pkexec = ["pkexec", "kill", "-15"]

    elif manage_option == "end_process_immediately":
        process_command = ["kill", "-9"]
        process_command_pkexec = ["pkexec", "kill", "-9"]

    process_command = process_command + process_pid_list_str
    process_command_pkexec = process_command_pkexec + process_pid_list_str

    if get_environment_type() == "flatpak":
        process_command = ["flatpak-spawn", "--host"] + process_command
        process_command_pkexec = ["flatpak-spawn", "--host"] + process_command_pkexec

    # Try to end the process without using root privileges.
    try:
        (subprocess.check_output(process_command, stderr=subprocess.STDOUT, shell=False)).decode()
    except subprocess.CalledProcessError:
        # End the process if root privileges are given.
        try:
            (subprocess.check_output(process_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
        # Prevent errors if wrong password is used or polkit dialog is closed by user.
        except subprocess.CalledProcessError:
            pass


# ***********************************************************************************************
#                                           Users
# ***********************************************************************************************

def get_etc_passwd_dict():
    """
    Get username, UID, user full name, user termninal information from "/etc/passwd" file.
    """

    environment_type = get_environment_type()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    etc_passwd_dict = {}
    for line in etc_passwd_lines:
        line_split = line.split(":", 6)
        uid = int(line_split[2])
        etc_passwd_sub_dict = {
                               "username" : line_split[0],
                               "gid" : int(line_split[3]),
                               "full_name" : line_split[4],
                               "home_dir" : line_split[5],
                               "terminal" : line_split[6]
                               }
        etc_passwd_dict[uid] = etc_passwd_sub_dict

    return etc_passwd_dict


def get_etc_group_dict():
    """
    Get user group name, GID information from "/etc/group" file.
    """

    environment_type = get_environment_type()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/group") as reader:
            etc_group_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/group") as reader:
            etc_group_lines = reader.read().strip().split("\n")

    etc_group_dict = {}
    for line in etc_group_lines:
        line_split = line.split(":", 3)
        gid = int(line_split[2])
        etc_group_sub_dict = {
                             "user_group_name" : line_split[0]
                             }
        etc_group_dict[gid] = etc_group_sub_dict

    return etc_group_dict


def get_users_information(users_data_dict_prev={}, system_boot_time=0, username_uid_dict={}):
    """
    Get user information of all/specified users.
    """

    process_list = []
    processes_of_user = "all"
    hide_kernel_threads = 0
    cpu_usage_divide_by_cores = "yes"
    detail_level = "low"

    # Define lists for getting user information from command output.
    users_data_dict = {}
    if users_data_dict_prev != {}:
        uid_list_prev = users_data_dict_prev["uid_list"]
        processes_data_dict_prev = users_data_dict_prev["processes_data_dict_prev"]
        pid_list_prev = processes_data_dict_prev["pid_list"]
        ppid_list_prev = processes_data_dict_prev["ppid_list"]
        process_cpu_times_prev = processes_data_dict_prev["process_cpu_times"]
        disk_read_write_data_prev = processes_data_dict_prev["disk_read_write_data"]
        global_cpu_time_all_prev = processes_data_dict_prev["global_cpu_time_all"]
        global_time_prev = processes_data_dict_prev["global_time"]
    else:
        uid_list_prev = []
        processes_data_dict_prev = {}
        pid_list_prev = []
        ppid_list_prev = []
        process_cpu_times_prev = {}
        disk_read_write_data_prev = {}
    uid_list = []
    human_user_uid_list = []
    pid_list = []
    ppid_list = []
    username_list = []
    cmdline_list = []
    process_cpu_times = {}
    disk_read_write_data = {}

    # Get process information fo getting logged in, CPU usage percentage, log in time and process count information.
    processes_data_dict = get_processes_information(process_list, processes_of_user, hide_kernel_threads, cpu_usage_divide_by_cores, detail_level, processes_data_dict_prev, system_boot_time, username_uid_dict)
    processes_data_dict_prev = dict(processes_data_dict)

    # Get user and user group information of all users
    etc_passwd_dict = get_etc_passwd_dict()
    etc_group_dict = get_etc_group_dict()

    # Get logged in users list
    logged_in_users_list = processes_data_dict["username_list"]

    # Get UIDs, CPU usage percentages and start times of all processes
    user_process_cpu_usage_start_time_dict = {}
    for pid in processes_data_dict["pid_list"]:
        process_data_dict = processes_data_dict[pid]
        uid = process_data_dict["uid"]
        uid_list.append(uid)
        user_process_cpu_usage_start_time_sub_dict = {
                                                     "uid" : uid,
                                                     "cpu_usage" : process_data_dict["cpu_usage"],
                                                     "start_time" : process_data_dict["start_time"]
                                                     }
        user_process_cpu_usage_start_time_dict[pid] = user_process_cpu_usage_start_time_sub_dict

    # Get user information for all human users
    for uid in etc_passwd_dict.keys():
        etc_passwd_sub_dict = etc_passwd_dict[uid]
        # Get information for only human users
        if uid >= 1000 and uid != 65534:
            human_user_uid_list.append(uid)
            username = etc_passwd_sub_dict["username"]
            if uid in uid_list:
                logged_in = True
            else:
                logged_in = False
            gid = etc_passwd_sub_dict["gid"]
            group_name = etc_group_dict[gid]["user_group_name"]
            full_name = etc_passwd_sub_dict["full_name"]
            home_dir = etc_passwd_sub_dict["home_dir"]
            terminal = etc_passwd_sub_dict["terminal"]

            # Get user processes
            cpu_usage_list = []
            start_time_list = []
            for pid in user_process_cpu_usage_start_time_dict:
                user_process_cpu_usage_start_time_sub_dict = user_process_cpu_usage_start_time_dict[pid]
                user_uid = user_process_cpu_usage_start_time_sub_dict["uid"]
                if user_uid == uid:
                    cpu_usage_list.append(user_process_cpu_usage_start_time_sub_dict["cpu_usage"])
                    start_time_list.append(user_process_cpu_usage_start_time_sub_dict["start_time"])
            if cpu_usage_list == []:
                total_cpu_usage = 0
            else:
                total_cpu_usage = sum(cpu_usage_list)
            if start_time_list == []:
                log_in_time = 0
            else:
                log_in_time = min(start_time_list)
            process_count = len(cpu_usage_list)

            # Add user data to a sub-dictionary
            user_data_dict = {
                             "username" : username,
                             "gid" : gid,
                             "group_name" : group_name,
                             "full_name" : full_name,
                             "logged_in" : logged_in,
                             "home_dir" : home_dir,
                             "terminal" : terminal,
                             "total_cpu_usage" : total_cpu_usage,
                             "log_in_time" : log_in_time,
                             "process_count" : process_count
                             }

            # Add user sub-dictionary to dictionary
            users_data_dict[uid] = user_data_dict

    # Add user related lists and variables for returning them for using them (for using some them as previous data in the next loop).
    users_data_dict["uid_list"] = uid_list
    users_data_dict["human_user_uid_list"] = human_user_uid_list
    users_data_dict["processes_data_dict_prev"] = processes_data_dict_prev

    return users_data_dict


# ***********************************************************************************************
#                                           Services
# ***********************************************************************************************

def get_services_information():
    """
    Get systemd services information.
    Service files (Unit files) are in the "/etc/systemd/system/" and "/usr/lib/systemd/system/autovt@.service" directories.
    But the first directory contains links to the service files in the second directory. Thus, service files get from the second directory.
    There is no "/usr/lib/systemd/system/" on some ARM systems (and also on older distributions) and "/lib/systemd/system/" is used
    in this case. On newer distributions "/usr/lib/systemd/system/" is a symlink to "/lib/systemd/system/".
    On ARM systems, also "/usr/lib/systemd/system/" folder may be used after installling some applications. In this situation
    this folder will be a real path. There may be user services in "/home/[USERNAME]/.config/systemd/user/" folder.
    Service list information is get by using multiprocessing. systemd may not support this for providing service information.
    This shortened time for getting service information and did not printed errors and did not give incorrect service information during tests.
    """

    environment_type = get_environment_type()

    services_data_dict = {}
    service_unit_file_list_usr_lib_systemd = []
    service_unit_file_list_lib_systemd = []
    if environment_type == "flatpak":
        if os.path.isdir("/var/run/host/usr/lib/systemd/system/") == True:
            service_unit_files_dir = "/var/run/host/usr/lib/systemd/system/"
            service_unit_file_list_usr_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]
        # There is no access to "/run" folder of the host OS in Flatpak environment.
        if (subprocess.check_output(["flatpak-spawn", "--host", "realpath", "/lib/systemd/system/"], shell=False)).decode().strip() + "/" == "/lib/systemd/system/":
            service_unit_files_dir = "/lib/systemd/system/"
            service_unit_file_list_lib_systemd_scratch = (subprocess.check_output(["flatpak-spawn", "--host", "ls", service_unit_files_dir], shell=False)).decode().strip().split()
            service_unit_file_list_lib_systemd = []
            for file in service_unit_file_list_lib_systemd_scratch:
                if file.endswith(".service") == True:
                    service_unit_file_list_lib_systemd.append(file)
    else:
        if os.path.isdir("/usr/lib/systemd/system/") == True:
            service_unit_files_dir = "/usr/lib/systemd/system/"
            service_unit_file_list_usr_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]
        if os.path.realpath("/lib/systemd/system/") + "/" == "/lib/systemd/system/":
            service_unit_files_dir = "/lib/systemd/system/"
            service_unit_file_list_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]

    # Get user services
    current_user_name = os.environ.get('USER')
    service_unit_files_dir_user = "/home/" + current_user_name + "/.config/systemd/user/"
    try:
        service_unit_file_list_user = [filename for filename in os.listdir(service_unit_files_dir_user) if filename.endswith(".service")]
    except Exception:
        service_unit_file_list_user = []

    # Merge service file lists from different folders.
    service_unit_file_list = service_unit_file_list_usr_lib_systemd + service_unit_file_list_lib_systemd + service_unit_file_list_user

    # Remove duplicated service names
    service_unit_file_list = sorted(list(set(service_unit_file_list)))

    try:
        if environment_type == "flatpak":
            # There is no access to "/run" folder of the host OS in Flatpak environment.
            service_files_from_run_systemd_list = (subprocess.check_output(["flatpak-spawn", "--host", "ls", "/run/systemd/units/"], shell=False)).decode().strip().split()
        else:
            service_files_from_run_systemd_list = [filename.split("invocation:", 1)[-1] for filename in os.listdir("/run/systemd/units/")]    # "/run/systemd/units/" directory contains loaded and non-dead services.
    except FileNotFoundError:
        service_files_from_run_systemd_list = []

    if environment_type == "flatpak":
        service_unit_files_dir_scratch = service_unit_files_dir.split("/var/run/host")[-1]
        service_unit_file_real_path_list = (subprocess.check_output(["flatpak-spawn", "--host", "ls", "-l", service_unit_files_dir_scratch], shell=False)).decode().strip().split("\n")
        for service_file in service_unit_file_real_path_list:
            if " -> " in service_file and "/dev/null" not in service_file:
                file = service_file.split(" -> ")[0].split()[-1].strip()
                if file in service_unit_file_list:
                    service_unit_file_list.remove(file)
    else:
        for file in service_unit_file_list[:]:                                                # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
            if os.path.islink(service_unit_files_dir + file) == True and os.path.realpath(service_unit_files_dir + file) != "/dev/null":    # Some service files are link to other ".service" files in the same directory. These links are removed from the list. Not all link files are removed. Link files with "/dev/null" are kept in the list.
                service_unit_file_list.remove(file)

    # Get all service names (joining service names from "systemctl list-unit-files ..." and "systemctl list-units ..."). Some services are run multiple times. For example there is one instance of "user@.service" from ""systemctl list-unit-files ..." command but there are two loaded services (user@1000.service and user@1001.service) per logged in user. There are several examples for this situation. "user@.service" is removed from list, "user@1000.service" and "user@1001.service" appended into list for getting information for all services correctly.
    service_list = []
    for service_unit_file in service_unit_file_list:
        if "@" not in service_unit_file:
            service_list.append(service_unit_file)
            continue
        else:
            service_unit_file_split = service_unit_file.split("@")[0]
            for service_loaded in service_files_from_run_systemd_list:
                if "@" in service_loaded:
                    service_loaded = service_loaded.split("invocation:")[-1]
                    if service_unit_file_split == service_loaded.split("@")[0]:
                        service_list.append(service_loaded)
                        continue
    service_list = sorted(service_list)

    # Generate "unit_files_command_parameter_list". This list will be used for constructing commandline for getting
    # service data per service file.
    # "LoadState" is always get for filtering service, etc. Also it prevents errors if every columns other than 
    # service names are preferred not to be shown. It gives errors if no property is specified with
    # "systemctl show [service_name] --property=" command.
    unit_files_command_parameter_list = ["LoadState", "UnitFileState", "MainPID", "ActiveState", "SubState", "MemoryCurrent", "Description"]
    unit_files_command_parameter_list = ",".join(unit_files_command_parameter_list)           # Join strings with "," between them.
    # Construct command for getting service information for all services
    if environment_type == "flatpak":
        unit_files_command = ["flatpak-spawn", "--host", "systemctl", "show", "--property=" + unit_files_command_parameter_list]
    else:
        unit_files_command = ["systemctl", "show", "--property=" + unit_files_command_parameter_list]
    for service in service_list:
        unit_files_command.append(service)

    # Get number of online logical CPU cores (this operation is repeated in every loop because 
    # number of online CPU cores may be changed by user and this may cause wrong calculation of
    # CPU usage percentage data of the processes even if this is a very rare situation.)
    number_of_logical_cores = get_number_of_logical_cores()

    # Get services bu using single process (instead of multiprocessing) if the system has 1 or 2 CPU cores.
    if number_of_logical_cores < 3:
        # Get service data per service file in one attempt in order to obtain lower CPU usage.
        # Because information from all service files will be get by one commandline operation and will be parsed later.
        try:
            systemctl_show_command_lines = (subprocess.check_output(unit_files_command, shell=False)).decode().strip().split("\n\n")
        # Prevent errors if "systemd" is not used on the system.
        except Exception:
            return
    # Get services bu using multiple processes (multiprocessing) if the system has more than 2 CPU cores.
    else:
        systemctl_show_command_lines = start_processes_func(number_of_logical_cores, unit_files_command)

    # Get service information by processing command output
    for i, service_name in enumerate(service_list):
        systemctl_show_command_lines_split = systemctl_show_command_lines[i]
        # Get service "loaded/not loaded" status
        load_state = "-"
        load_state = _tr(systemctl_show_command_lines_split.split("LoadState=", 1)[1].split("\n", 1)[0].capitalize())
        # Get service unit file state
        unit_file_state = _tr(systemctl_show_command_lines_split.split("UnitFileState=", 1)[1].split("\n", 1)[0].capitalize())
        # Get service main PID
        main_pid = int(systemctl_show_command_lines_split.split("MainPID=", 1)[1].split("\n", 1)[0].capitalize())
        # Get service active state
        active_state = _tr(systemctl_show_command_lines_split.split("ActiveState=", 1)[1].split("\n", 1)[0].capitalize())
        # Get service substate
        sub_state = _tr(systemctl_show_command_lines_split.split("SubState=", 1)[1].split("\n", 1)[0].capitalize())
        # Get service current memory
        memory_current = systemctl_show_command_lines_split.split("MemoryCurrent=", 1)[1].split("\n", 1)[0].capitalize()
        # "-1" value is used as "memory_current" value if memory value is get as "[not set]".
        # Code will recognize this value and show "-" information in this situation.
        if memory_current.startswith("["):
            memory_current = -1
        else:
            memory_current = int(memory_current)
        # Get service description
        description = systemctl_show_command_lines_split.split("Description=", 1)[1].split("\n", 1)[0].capitalize()

        # Add service data to a sub-dictionary
        service_data_dict = {
                             "load_state" : load_state,
                             "unit_file_state" : unit_file_state,
                             "main_pid" : main_pid,
                             "active_state" : active_state,
                             "sub_state" : sub_state,
                             "memory_current" : memory_current,
                             "description" : description
                             }

        # Add service sub-dictionary to dictionary
        services_data_dict[service_name] = service_data_dict

    # Add service related lists and variables
    services_data_dict["service_list"] = service_list

    return services_data_dict


def get_core_count_for_getting_services(number_of_logical_cores):
    """
    Get number of CPU cores to be used at the same time for getting service data.
    """

    # 1 or 2 CPU cores are not used in order to avoid reducing performance of other processes or the system.
    # Using more than 5 CPU cores does not improve performance noticeably on a 4 physical (8 logical) core system.
    if number_of_logical_cores == 3:
        number_of_cpu_cores_used = 2
    if number_of_logical_cores in [4, 5, 6, 7]:
        number_of_cpu_cores_used = number_of_logical_cores - 2
    if number_of_logical_cores > 7:
        number_of_cpu_cores_used = 5

    return number_of_cpu_cores_used


def split_unit_files_command_output(number_of_cpu_cores_used, unit_files_command):
    """
    Split service list into [number_of_cpu_cores_used] lists for using them to get service data by using multiprocessing.
    """

    # Get service list and unit file command parameters. "+1" for list slice index, "+2" for 2 elements after "systemctl" parameter to obtain index of element which starts with "--property=".
    index_to_split_list = unit_files_command.index("systemctl") + 1 + 2
    service_list = unit_files_command[index_to_split_list:]
    unit_files_command = unit_files_command[:index_to_split_list]

    # Get number of services per process.
    number_of_services_per_process = len(service_list) // number_of_cpu_cores_used
    remaining_services = len(service_list) % number_of_cpu_cores_used

    # Split service list per process.
    service_list_split = []
    for i in range(number_of_cpu_cores_used):
        service_list_split.append(service_list[i*number_of_services_per_process:(i+1)*number_of_services_per_process])

    # Add the remaining services into the last list.
    if remaining_services != 0:
        for service in service_list[-remaining_services:]:
            service_list_split[-1].append(service)

    # Also add the command parameters to the beginning of the all service lists to use them as commands.
    unit_files_command_split = []
    for service_list_data in service_list_split:
        unit_files_command_scratch = list(unit_files_command)
        for service in service_list_data:
            unit_files_command_scratch.append(service)
        unit_files_command_split.append(unit_files_command_scratch)

    return unit_files_command_split


def get_service_data(queue1, i, unit_files_command_split):
    """
    Get service data by using multiprocessing.
    """

    try:
        systemctl_show_command_lines_split = (subprocess.check_output(unit_files_command_split, shell=False)).decode().strip().split("\n\n")
    # Prevent errors if "systemd" is not used on the system.
    except Exception:
        pass

    # Put the service data (and process number) into queue in order to get it, reorder and merge them by using the main process. It is a FIFO queue and data can be get in the same order which they are put into the queue.
    # Nested "[}" required for putting the data as a list.
    queue1.put([[i, systemctl_show_command_lines_split]])


def start_processes_func(number_of_logical_cores, unit_files_command):
    """
    Run the required functions and start processes to get the service data by using multiprocessing.
    """

    # Import modules in this function because entire module is run separately by the all processes if multiprocessing is used.
    import multiprocessing

    # Get the required data.
    number_of_cpu_cores_used = get_core_count_for_getting_services(number_of_logical_cores)
    unit_files_command_split = split_unit_files_command_output(number_of_cpu_cores_used, unit_files_command)

    # Define a queue for getting the data from the processes.
    queue1 = multiprocessing.Queue()

    # Generate processes and their argments (queue, process number for reordering the output, command per process).
    process_list = [multiprocessing.Process(target=get_service_data, args=(queue1, i, unit_files_command_split[i]), daemon=True) for i in range(number_of_cpu_cores_used)]

    # Start the processes.
    for process in process_list:
        process.start()

    # Wait for processes to finish.
    for process in process_list:
        process.join()

    # Get all the data in the queue (until it is empty).
    queue_data_list = []
    while queue1.empty() == False:
        queue_data_list = queue_data_list + queue1.get()

    # Reorder the data by using the process numbers. Because processes may not be finish the works in the start order.
    queue_data_list = sorted(queue_data_list)

    # Merge the process data and obtain a single list.
    systemctl_show_command_lines = []
    for data1 in queue_data_list:
        for service in data1[1]:
            systemctl_show_command_lines.append(service)

    return systemctl_show_command_lines


def get_service_detailed_information(service_name):
    """
    Get detailed information of the specified service.
    """

    service_detailed_info_dict = {}

    system_boot_time = get_system_boot_time()

    # Get all information of the service
    command_list = ["systemctl", "show", service_name]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    systemctl_show_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")

    # Initial values of the variables. These values will be used if they could not be detected.
    service_type = "-"
    main_pid = "-"
    exec_main_start_times_stamp_monotonic = "-"
    exec_main_exit_times_stamp_monotonic ="-"
    memory_current = "-"
    requires = "-"
    conflicts = "-"
    after = "-"
    before = "-"
    triggered_by = "-"
    documentation = "-"
    description = "-"
    active_state = "-"
    load_state = "-"
    sub_state = "-"
    fragment_path = "-"
    unit_file_state = "-"
    unit_file_preset = "-"

    for line in systemctl_show_lines:
        if "Type=" in line:
            service_type = _tr(line.split("=", 1)[1].capitalize())
            # Skip to next loop if searched line ("Type=") is found in order to avoid redundant line search.
            continue
        if "MainPID=" in line:
            main_pid = line.split("=", 1)[1]
            continue
        if "ExecMainStartTimestampMonotonic=" in line:
            line_split = line.split("=", 1)[1]
            if line_split != "0":
                # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain
                # time in seconds and appended to system boot time for getting service start time.
                # Because time data is get as "elapsed time after system boot" from the file.
                exec_main_start_times_stamp_monotonic = int(line.split("=")[1])/1000000 + system_boot_time
                exec_main_start_times_stamp_monotonic = datetime.fromtimestamp(exec_main_start_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
            if line_split == "0":
                exec_main_start_times_stamp_monotonic = "-"
            continue
        if "ExecMainExitTimestampMonotonic=" in line:
            line_split = line.split("=", 1)[1]
            if line_split != "0":
                exec_main_exit_times_stamp_monotonic = int(line.split("=")[1])/1000000 + system_boot_time
                exec_main_exit_times_stamp_monotonic = datetime.fromtimestamp(exec_main_exit_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
            if line_split == "0":
                exec_main_exit_times_stamp_monotonic = "-"
            continue
        if "MemoryCurrent=" in line:
            memory_current = line.split("=", 1)[1]
            try:
                memory_current = int(memory_current)
            except Exception:
                memory_current = -1
            continue
        if "Requires=" in line:
            requires = sorted(line.split("=", 1)[1].split())
            continue
        if "Conflicts=" in line:
            conflicts = sorted(line.split("=", 1)[1].split())
            continue
        if "After=" in line:
            after = sorted(line.split("=", 1)[1].split())
            continue
        if "Before=" in line:
            before = sorted(line.split("=", 1)[1].split())
            continue
        if "TriggeredBy=" in line:
            triggered_by = line.split("=", 1)[1]
            continue
        if "Documentation=" in line:
            documentation = line.split("=", 1)[1].split()
            # Convert string into multi-line string if there are more than one documentation information.
            documentation_scratch = []
            for documentation in documentation:
                documentation_scratch.append(documentation.strip('"'))
            documentation = documentation_scratch
            continue
        if "Description=" in line:
            description = line.split("=", 1)[1]
            continue
        if "ActiveState=" in line:
            active_state = _tr(line.split("=", 1)[1].capitalize())
            continue
        if "LoadState=" in line:
            load_state = _tr(line.split("=", 1)[1].capitalize())
            continue
        if "SubState=" in line:
            sub_state = _tr(line.split("=", 1)[1].capitalize())
            continue
        if "FragmentPath=" in line:
            fragment_path = line.split("=", 1)[1]
            continue
        if "UnitFileState=" in line:
            unit_file_state = _tr(line.split("=", 1)[1].capitalize())
            continue
        if "UnitFilePreset=" in line:
            unit_file_preset = _tr(line.split("=", 1)[1].capitalize())
            continue

    # Add service data to a dictionary
    service_detailed_info_dict = {
                                  "service_name" : service_name,
                                  "service_type" : service_type,
                                  "main_pid" : main_pid,
                                  "exec_main_start_times_stamp_monotonic" : exec_main_start_times_stamp_monotonic,
                                  "exec_main_exit_times_stamp_monotonic" : exec_main_exit_times_stamp_monotonic,
                                  "memory_current" : memory_current,
                                  "requires" : requires,
                                  "conflicts" : conflicts,
                                  "after" : after,
                                  "before" : before,
                                  "triggered_by" : triggered_by,
                                  "documentation" : documentation,
                                  "description" : description,
                                  "active_state" : active_state,
                                  "load_state" : load_state,
                                  "sub_state" : sub_state,
                                  "fragment_path" : fragment_path,
                                  "unit_file_state" : unit_file_state,
                                  "unit_file_preset" : unit_file_preset
                                  }

    return service_detailed_info_dict


def get_service_mask_state(service_name):
    """
    Get service mask state (masked/unmasked).
    """

    command_list = ["systemctl", "show", service_name, "--property=UnitFileState"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    service_mask_status = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]

    return service_mask_status


def manage_service(service_name, action_name):
    """
    Start, stop, restart, enable, disable, mask (hide), unmask services.
    """

    command_list = ["systemctl", action_name, service_name]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    # Run command and get output if there are errors.
    try:
        systemctl_run = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #systemctl_output = systemctl_run.stdout.decode().strip()
        systemctl_error = systemctl_run.stderr.decode().strip()
    except Exception:
        systemctl_error = "-"

    return systemctl_error


# ***********************************************************************************************
#                                           System
# ***********************************************************************************************

def get_os_name_version_codename_based_on():
    """
    Get OS name, version, version code name and OS based on information.
    """

    # Read "/etc/os-release" file for getting OS name, version and based on information.
    if get_environment_type() == "flatpak":
        try:
            with open("/var/run/host/etc/os-release") as reader:
                os_release_output = reader.read()
        except FileNotFoundError:
            # Read "os-release" file on NixOS.
            # It is not read by using "/var/run/host/etc/os-release" path even though there is a link of this file.
            with open("/var/run/host/etc/static/os-release") as reader:
                os_release_output = reader.read()
    else:
        with open("/etc/os-release") as reader:
            os_release_output = reader.read()

    os_release_output_lines = os_release_output.strip().split("\n")

    os_name = "-"
    os_based_on = "-"
    os_version = "-"
    build_id = "-"

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
        if line.startswith("BUILD_ID="):
            build_id = line.split("BUILD_ID=")[1].strip(' "').title()
            continue

    # Some Arch Linux based distributions may have "BUILD_ID" instead of "VERSION". For example: Endeavour OS.
    if os_version == "-":
        os_version = build_id

    # Append Debian version to the based on information if OS is based on Debian.
    if os_based_on == "Debian":
        debian_version = "-"
        if get_environment_type() == "flatpak":
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


def get_os_family():
    """
    Get OS family.
    """

    os_family = platform.system()
    if os_family == "":
        os_family = "-"

    return os_family


def get_kernel_release():
    """
    Get kernel release (base version of kernel)
    """

    kernel_release = platform.release()
    if kernel_release == "":
        kernel_release = "-"

    return kernel_release


def get_kernel_version():
    """
    Get kernel version (package version of kernel).
    """

    kernel_version = platform.version()
    if kernel_version == "":
        kernel_version = "-"

    return kernel_version


def get_computer_vendor_model_chassis_type():
    """
    Get computer vendor, model and chassis type.
    """

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

    computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]

    # Add "Virtual Machine" information if chasssis type is detected as "Other" and 
    # computer vendor is one of the known virtual machine vendors.
    if computer_chassis_type == "Other":
        if computer_vendor in ["QEMU", "innotek GmbH", "VMware, Inc."]:
            computer_chassis_type = computer_chassis_type + " (" + _tr("Virtual Machine") + ")"

    return computer_vendor, computer_model, computer_chassis_type


def get_host_name():
    """
    Get host name.
    """

    with open("/proc/sys/kernel/hostname") as reader:
        host_name = reader.read().strip()

    return host_name


def get_number_of_monitors():
    """
    Get number of monitors.
    """

    number_of_monitors = "-"
    try:
        import gi
        gi.require_version('Gdk', '4.0')
        from gi.repository import Gdk
        monitor_list = Gdk.Display().get_default().get_monitors()
        number_of_monitors = len(monitor_list)
    except Exception:
        pass

    return number_of_monitors


def get_current_python_version():
    """
    Get current Python version (Python which is running this code).
    """

    current_python_version = platform.python_version()

    return current_python_version


def get_current_gtk_version():
    """
    Get Gtk version which is used for this application.
    """

    import gi
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk

    current_gtk_version = f'{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}'

    return current_gtk_version


def get_installed_system_packages():
    """
    Get number of installed APT, RPM or pacman packages.
    """

    environment_type = get_environment_type()

    # Initial value of the variables.
    apt_packages_available = "-"
    rpm_packages_available = "-"
    pacman_packages_available = "-"
    apk_packages_available = "-"
    portage_packages_available = "-"
    system_packages_count = "-"

    # Get number of APT (deb) packages if available.
    try:
        # Check if "python3" is installed in order to determine package type of the system.
        if environment_type == "flatpak":
            apt_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "dpkg", "-s", "python3"], shell=False)).decode().strip()
        else:
            apt_packages_available = (subprocess.check_output(["dpkg", "-s", "python3"], shell=False)).decode().strip()
        if "Package: python3" in apt_packages_available:
            if environment_type == "flatpak":
                number_of_installed_apt_packages = (subprocess.check_output(["flatpak-spawn", "--host", "dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
            else:
                number_of_installed_apt_packages = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
            system_packages_count = f'{number_of_installed_apt_packages} (APT)'
    # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system. It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        apt_packages_available = "-"

    # Get number of RPM packages if available.
    if apt_packages_available == "-":
        try:
            if environment_type == "flatpak":
                rpm_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "rpm", "-q", "python3"], shell=False)).decode().strip()
            else:
                rpm_packages_available = (subprocess.check_output(["rpm", "-q", "python3"], shell=False)).decode().strip()
            if rpm_packages_available.startswith("python3-3."):
                if environment_type == "flatpak":
                    number_of_installed_rpm_packages = (subprocess.check_output(["flatpak-spawn", "--host", "rpm", "-qa"], shell=False)).decode().strip().split("\n")
                else:
                    number_of_installed_rpm_packages = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
                # Differentiate empty line count
                number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")
                system_packages_count = f'{number_of_installed_rpm_packages} (RPM)'
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            rpm_packages_available = "-"

    # Get number of pacman (Arch Linux) packages if available.
    if apt_packages_available == "-" and rpm_packages_available == "-":
        try:
            if environment_type == "flatpak":
                pacman_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "pacman", "-Q", "python3"], shell=False)).decode().strip()
            else:
                pacman_packages_available = (subprocess.check_output(["pacman", "-Q", "python3"], shell=False)).decode().strip()
            if pacman_packages_available.startswith("python 3."):
                if environment_type == "flatpak":
                    number_of_installed_pacman_packages = (subprocess.check_output(["flatpak-spawn", "--host", "pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                else:
                    number_of_installed_pacman_packages = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                # Differentiate empty line count
                number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")
                system_packages_count = f'{number_of_installed_pacman_packages} (pacman)'
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            pacman_packages_available = "-"

    # Get number of APK (Alpine Linux) packages if available.
    if apt_packages_available == "-" and rpm_packages_available == "-" and pacman_packages_available == "-":
        try:
            if environment_type == "flatpak":
                apk_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "apk", "list", "--installed", "python3"], shell=False)).decode().strip()
            else:
                apk_packages_available = (subprocess.check_output(["apk", "list", "--installed", "python3"], shell=False)).decode().strip()
            if apk_packages_available.startswith("python3-3."):
                if environment_type == "flatpak":
                    number_of_installed_apk_packages = (subprocess.check_output(["flatpak-spawn", "--host", "apk", "info"], shell=False)).decode().strip().split("\n")
                else:
                    number_of_installed_apk_packages = (subprocess.check_output(["apk", "info"], shell=False)).decode().strip().split("\n")
                # Differentiate empty line count
                number_of_installed_apk_packages = len(number_of_installed_apk_packages) - number_of_installed_apk_packages.count("")
                system_packages_count = f'{number_of_installed_apk_packages} (APK)'
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            apk_packages_available = "-"

    # Get number of Portage (Gentoo distribution) packages if available.
    if apt_packages_available == "-" and rpm_packages_available == "-" and pacman_packages_available == "-" and apk_packages_available == "-":
        try:
            # Python3 is in core system, no need to check if it is available.
            if environment_type == "flatpak":
                qlist_output = (subprocess.check_output(["flatpak-spawn", "--host", "qlist", "-Iv"], shell=False))
            else:
                qlist_output = (subprocess.check_output(["qlist", "-Iv"], shell=False))
            installed_portage_packages = qlist_output.decode().strip().split("\n")
            number_of_installed_portage_packages = len(installed_portage_packages)
            system_packages_count = f'{number_of_installed_portage_packages} (Portage)'
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            portage_packages_available = "-"

    return system_packages_count


def get_installed_flatpak_packages():
    """
    Get number of installed Flatpak packages (and runtimes).
    """

    flatpak_packages_count = "-"

    command_list = ["flatpak", "list"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    try:
        flatpak_packages_available = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        # Differentiate empty line count
        flatpak_packages_count = len(flatpak_packages_available) - flatpak_packages_available.count("")
    except (FileNotFoundError, subprocess.CalledProcessError) as me:
        flatpak_packages_count = "-"

    return flatpak_packages_count


def get_desktop_environment_and_version_windowing_system_window_manager_display_manager():
    """
    Get current desktop environment, windowing_system, window_manager, current_display_manager.
    """

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

    # Try to detect windowing system, window manager, current desktop 
    # environment and current display manager by reading process names and
    # other details.
    command_list = ["ps", "-eo", "comm,user"]
    if get_environment_type() == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    ps_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")
    # Delete header line
    del ps_output_lines[0]

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
    current_desktop_environment_version = get_desktop_environment_version(current_desktop_environment)

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
            if current_desktop_environment_version.split(".")[0] in ["3", "40", "41", "42", "43", "44", "45"]:
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


def get_desktop_environment_version(current_desktop_environment):
    """
    Get current desktop environment version.
    """

    current_desktop_environment_version = "-"

    if current_desktop_environment in desktop_environment_version_command_dict:
        command_list = desktop_environment_version_command_dict[current_desktop_environment]
        if get_environment_type() == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        try:
            desktop_environment_version_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        except Exception:
            desktop_environment_version_output = "-"
    else:
        desktop_environment_version_output = "-"

    if current_desktop_environment == "XFCE":
        # Example output: "xfce4-panel 4.18.2 (Xfce 4.18)"
        for line in desktop_environment_version_output.split("\n"):
            if line.startswith("xfce4-panel "):
                current_desktop_environment_version = line.split(" ")[-1].strip("()")
                break

    if current_desktop_environment in ["GNOME", "zorin:GNOME", "ubuntu:GNOME"]:
        for line in desktop_environment_version_output.split("\n"):
            if "GNOME Shell" in line:
                current_desktop_environment_version = line.split(" ")[-1]

    if current_desktop_environment in ["X-Cinnamon", "CINNAMON"]:
        current_desktop_environment_version = desktop_environment_version_output.split(" ")[-1]

    if current_desktop_environment == "MATE":
        current_desktop_environment_version = desktop_environment_version_output.split(" ")[-1]

    if current_desktop_environment == "KDE":
        current_desktop_environment_version = desktop_environment_version_output

    if current_desktop_environment == "LXQt":
        for line in desktop_environment_version_output:
            if "liblxqt" in line:
                current_desktop_environment_version = line.split()[1].strip()

    if current_desktop_environment in ["Budgie", "Budgie:GNOME"]:
        current_desktop_environment_version = desktop_environment_version_output.split("\n")[0].strip().split(" ")[-1]

    return current_desktop_environment_version

