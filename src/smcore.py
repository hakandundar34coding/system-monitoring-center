#!/usr/bin/env python3


#####################################################################################################
#                                        Common functions                                           #
#####################################################################################################

def environment_type():
    """
    Detect environment type (Flatpak, Python package or native).
    This information will be used for accessing host OS commands if the application is run in Flatpak environment.
    """

    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_user_homedir = os.environ.get('HOME')
    application_flatpak_id = os.getenv('FLATPAK_ID')

    if application_flatpak_id != None:
        _environment_type = "flatpak"

    elif current_dir.startswith("/usr/local/lib/python") == True or current_dir.startswith(current_user_homedir + "/.local/lib/python") == True:
        _environment_type = "python_package"

    else:
        _environment_type = "native"

    return _environment_type


def systemd_used():
    """
    Get information of if 'systemd' is init system of the system.
    """

    _environment_type = environment_type()

    _systemd_used = "-"

    try:
        if _environment_type == "flatpak":
            import subprocess
            process_name = (subprocess.check_output(["flatpak-spawn", "--host", "cat", "/proc/1/comm"], shell=False)).decode().strip()
        else:
            with open("/proc/1/comm") as reader:
                process_name = reader.read().strip()
    except Exception:
        pass


    if process_name == "systemd":
        _systemd_used = "Yes"
    else:
        _systemd_used = "No"

    return _systemd_used


def device_vendor_model(modalias_output):
    """
    Get device vendor and model information.
    """

    _environment_type = environment_type()

    # Define "udev" hardware database file directory.
    udev_hardware_database_dir = "/usr/lib/udev/hwdb.d/"
    # Some older Linux distributions use "/lib/" instead of "/usr/lib/" but they are merged under "/usr/lib/" in newer versions.
    if os.path.isdir(udev_hardware_database_dir) == False:
        udev_hardware_database_dir = "/lib/udev/hwdb.d/"
    if _environment_type == "flatpak":
        udev_hardware_database_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../etc/udev/hwdb.d/"

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
    # modalias_output = "of:NgpuT<NULL>Cnvidia,tegra210-gm20bCnvidia,gm20b"    # NVIDIA Tegra GPU on N.Switch device
    # modalias_output = "of:NgpuT(null)Cbrcm,bcm2835-vc4"
    # modalias_output = "scsi:t-0x05"
    # modalias_output = "scsi:t-0x00"

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

        # Get search texts by using device IDs.
        search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        # Read database file for PCI devices.
        with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
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

        # Get search texts by using device IDs.
        search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        # Read database file for VIRTIO devices.
        with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
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
        with open(udev_hardware_database_dir + "20-usb-vendor-model.hwdb", encoding="utf-8") as reader:
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
        with open(udev_hardware_database_dir + "20-sdio-vendor-model.hwdb", encoding="utf-8") as reader:
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


#####################################################################################################
#                                          CPU functions                                            #
#####################################################################################################

def cpu_times():
    """
    Get CPU times all cores (first value) and per-core.
    "/proc/stat" file contains online logical CPU core names (without regarding CPU sockets) and CPU times.
    """

    with open("/proc/stat") as reader:
        proc_stat_lines = reader.read().split("intr", 1)[0].strip().split("\n")

    _cpu_times = {}
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
        _cpu_times[cpu_core] = cpu_stats(cpu_time_all, cpu_time_load, user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice)

    return _cpu_times


def logical_core_count():
    """
    Get number of online logical cores.
    """

    # First try a faster way: using "SC_NPROCESSORS_ONLN" variable.
    try:
        number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")
    except ValueError:
        number_of_logical_cores = None

    # As a second try, count by reading from "/proc/cpuinfo" file.
    if number_of_logical_cores == None:
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    return number_of_logical_cores


def cpu_core_frequency(core='all', freq='all', unit='GHz'):
    """
    Get current, minimum and maximum frequencies of the CPU core.
    """

    # Get online logical CPU core list
    if core == 'all':
        core_list = [core for core in logical_core_count()]
    else:
        core_list = [core]

    cpu_core_frequency = []
    for core in core_list:
        if freq == 'all':
            current_frequency = cpu_core_current_frequency(core)
            min_frequency, max_frequency = cpu_core_min_max_frequency(core)
        elif freq == 'current':
            current_frequency = cpu_core_current_frequency(core)
            min_frequency, max_frequency = None, None
        elif freq == 'min_max':
            current_frequency = None
            min_frequency, max_frequency = cpu_core_min_max_frequency(core)

        current_frequency = cpu_core_frequency_unit(current_frequency, unit)
        min_frequency = cpu_core_frequency_unit(min_frequency, unit)
        max_frequency = cpu_core_frequency_unit(max_frequency, unit)

        cpu_core_frequency.append(core_freq(current_frequency, min_frequency, max_frequency))

    return cpu_core_frequency


def cpu_core_current_frequency(core):
    """
    Get current frequency of the CPU core.
    Value in 'scaling_cur_freq' file is in KHz unit.
    Values in '/proc/cpuinfo' file are in MHz unit.
    """

    # "/sys/devices/system/cpu/cpu[NUMBER]/cpufreq" is used instead of "/sys/devices/system/cpu/cpufreq/policy[NUMBER]".
    # Because CPU core current frequencies may be same for all cores on RB_Pi devices and
    # "scaling_cur_freq" file may be available for only 0th core of the relevant CPU group (little cores , big cores).
    try:
        with open("/sys/devices/system/cpu/cpu" + core + "/cpufreq/scaling_cur_freq") as reader:
            current_frequency = float(reader.read().strip())
    # CPU core current frequency may not be found in "/sys/..." folders on virtual machines.
    except FileNotFoundError:
        current_frequency = None

    # Get current frequency value by reading "/proc/cpuinfo" file.
    if current_frequency == None:
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
        proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(core.split("cpu")[1])].split("\n")
        for line in proc_cpuinfo_all_cores_lines:
            if line.startswith("cpu MHz"):
                current_frequency = float(line.split(":")[1].strip()) * 1000
                break

    return current_frequency


def cpu_core_min_max_frequency(core):
    """
    Get minimum and maximum frequencies of the CPU core.
    Values in 'scaling_min_freq' and 'scaling_max_freq' files are in KHz unit.
    """

    try:
        with open("/sys/devices/system/cpu/cpu" + core + "/cpufreq/scaling_min_freq") as reader:
            min_frequency = float(reader.read().strip())
        with open("/sys/devices/system/cpu/cpu" + core + "/cpufreq/scaling_max_freq") as reader:
            max_frequency = float(reader.read().strip())
    except FileNotFoundError:
        min_frequency = None
        max_frequency = None

    return min_frequency, max_frequency


def cpu_core_frequency_unit(frequency, unit):
    """
    Convert CPU core frequency values.
    """

    if frequency == None:
        return None

    if unit == "Hz":
        frequency = frequency * 1000

    elif unit == "KHz":
        pass

    elif unit == "MHz":
        frequency = frequency / 1000

    elif unit == "GHz":
        frequency = frequency / 1000000

    return frequency


def cpu_core_cache(core='all'):
    """
    Get L1i, L1d, L2, L3 cache memory values of the selected CPU core.
    """

    # Get online logical CPU core list
    if core == 'all':
        core_list = [core for core in logical_core_count()]
    else:
        core_list = [core]

    cpu_core_cache = []
    for core in core_list:

        # Get l1d cache
        try:
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index0/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index0/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index0/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Data":
                l1d_cache = cache_size
        except FileNotFoundError:
            l1d_cache = None

        # Get li cache
        try:
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index1/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index1/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index1/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Instruction":
                l1i_cache = cache_size
        except FileNotFoundError:
            l1i_cache = None

        # Get l2 cache
        try:
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index2/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index2/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "2":
                l2_cache = cache_size
        except FileNotFoundError:
            l2_cache = None

        # Get l3 cache
        try:
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index3/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/cpu" + core + "/cache/index3/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "3":
                l3_cache = cache_size
        except FileNotFoundError:
            l3_cache = None

        cpu_core_cache.append(core_cache(l1d_cache, l1i_cache, l2_cache, l3_cache))

    return cpu_core_cache


def processes_threads():
    """
    Get number of threads and number of processes.
    """

    _environment_type = environment_type()

    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host", "ps", "--no-headers", "-eo", "thcount"]
        ps_output_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        number_of_processes = len(ps_output_lines)
        number_of_threads = 0
        for line in ps_output_lines:
            number_of_threads = number_of_threads + int(line.strip())

    else:
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]

        thread_count_list = []
        for pid in pid_list:
            try:
                with open("/proc/" + pid + "/status") as reader:
                    proc_status_output = reader.read()
            # Skip to the next loop without "FileNotFoundError" error when a process is ended after process list is get.
            except (FileNotFoundError, ProcessLookupError) as me:
                continue
            # Append number of threads of the process
            thread_count_list.append(int(proc_status_output.split("\nThreads:", 1)[1].split("\n", 1)[0].strip()))

        number_of_processes = len(thread_count_list)
        number_of_threads = sum(thread_count_list)

    number_of_processes_threads = procs_threads(number_of_processes, number_of_threads)

    return number_of_processes_threads


def cpu_architecture():
    """
    Get CPU architecture.
    """

    architecture = platform.processor()
    if architecture == "":
        architecture = platform.machine()
        if architecture == "":
            architecture = "-"

    return architecture


def system_up_time():
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


def cpu_model_name(core='0'):
    """
    Get model name for the CPU core.
    """

    core = int(core)

    with open("/proc/cpuinfo") as reader:
        proc_cpuinfo_output = reader.read()
    proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")

    # Get number of physical cores, number_of_cpu_sockets, cpu_models for "x86_64" architecture.
    # Physical and logical cores and model name per core information are tracked easily on this platform.
    if "physical id" in proc_cpuinfo_output:
        cpu_models = []
        for line in proc_cpuinfo_output_lines:
            if line.startswith("model name"):
                cpu_models.append(line.split(":")[1].strip())
        cpu_model = cpu_models[core]

    # Get number of physical cores, number_of_cpu_sockets, cpu_models for "ARM" architecture.
    # Physical and logical cores and model name per core information are not tracked easily on this platform.
    # Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
    else:
        cpu_models = []

        cpu_implementer_list = []
        cpu_architecture_list = []
        cpu_part_list = []

        # Get register values to get required information.
        for line in proc_cpuinfo_output_lines:
            # Get vendor
            if line.startswith("CPU implementer"):
                cpu_implementer_list.append(line.split(":")[-1].strip())
            # Get architecture
            elif line.startswith("CPU architecture"):
                cpu_architecture_list.append(line.split(":")[-1].strip())
            # Get core model (for example: Cortex-A57)
            elif line.startswith("CPU part"):
                cpu_part_list.append(line.split(":")[-1].strip())

        # Redefine "core" in order to get information of the selected CPU core.
        number_of_logical_cores = logical_core_count()
        if len(cpu_implementer_list) == number_of_logical_cores:
            pass
        # There may be only one instance of register values even if CPU has multiple cores.
        else:
            core = 0

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
        search_text1 = cpu_implementer_list[core].split("0x", 1)[-1]
        search_text2 = "\t" + cpu_part_list[core].split("0x", 1)[-1]
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
            cpu_architecture = arm_architecture_dict[cpu_architecture_list[core]]
        except KeyError:
            cpu_architecture = "-"
        cpu_model = f'{cpu_implementer} {cpu_part} ({cpu_architecture})'
        # Get CPU model information by using "/proc/cpuinfo" file if CPU implementer or CPU part is not detected.
        if cpu_implementer == "-" or cpu_part == "-":
            cpu_model = "-"
            for line in proc_cpuinfo_output_lines:
                if line.startswith("model name"):
                    cpu_model = line.split(":")[-1].strip()
            if cpu_model == "-":
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("Processor"):
                        cpu_model = line.split(":")[-1].strip()
            if cpu_model == "-":
                cpu_model = "[" + _tr("Unknown") + "]"

    return cpu_model


def physical_core_socket_count():
    """
    Get number of physical cores, number of cpu sockets.
    """

    with open("/proc/cpuinfo") as reader:
        proc_cpuinfo_output = reader.read()
    proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")

    # Get number of physical cores, number_of_cpu_sockets, cpu_models for "x86_64" architecture.
    # Physical and logical cores and model name per core information are tracked easily on this platform.
    if "physical id" in proc_cpuinfo_output:
        number_of_physical_cores = 0
        physical_id = 0
        physical_id_prev = 0
        for line in proc_cpuinfo_output_lines:
            if line.startswith("physical id"):
                physical_id_prev = physical_id
                physical_id = line.split(":")[1].strip()
            if physical_id != physical_id_prev and line.startswith("cpu cores"):
                number_of_physical_cores = number_of_physical_cores + int(line.split(":")[1].strip())
        number_of_cpu_sockets = int(physical_id) + 1

    # Get number of physical cores, number_of_cpu_sockets, cpu_models for "ARM" architecture.
    # Physical and logical cores and model name per core information are not tracked easily on this platform.
    # Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
    else:
        number_of_physical_cores = logical_core_count()
        number_of_cpu_sockets = 1

    physical_cores_sockets = phy_cores_sockets(number_of_physical_cores, number_of_cpu_sockets)

    return physical_cores_sockets


#####################################################################################################
#                                         Memory functions                                          #
#####################################################################################################

def memory_info():
    """
    Get memory (RAM and swap) values.
    Values in '/proc/meminfo' file are in KiB unit.
    """

    with open("/proc/meminfo") as reader:
        proc_meminfo_output = reader.read()

    # Get memory (RAM)
    ram_total = int(proc_meminfo_output.split("MemTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_free = int(proc_meminfo_output.split("\nMemFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_available = int(proc_meminfo_output.split("\nMemAvailable:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    ram_used = ram_total - ram_available
    ram_used_percent = ram_used / ram_total * 100

    # Get memory (swap)
    swap_total = int(proc_meminfo_output.split("\nSwapTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    swap_free = int(proc_meminfo_output.split("\nSwapFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
    # Calculate values if swap memory exists.
    if swap_free != 0:
        swap_used = swap_total - swap_free
        swap_used_percent = swap_used / swap_total * 100
    # Set values as "0" if swap memory does not exist.
    else:
        swap_used = 0
        swap_used_percent = 0

    _memory_info = memory_stats(ram_total, ram_free, ram_available, ram_used, ram_used_percent, swap_total, swap_free, swap_used, swap_used_percent)

    return _memory_info


def physical_ram():
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
            # The value get by "vcgencmd get_config total_mem" command is in MiB unit.
            total_physical_ram = float(total_physical_ram) * 1024 * 1024
        except Exception:
            total_physical_ram = "-"

    return total_physical_ram


#####################################################################################################
#                                          Disk functions                                           #
#####################################################################################################

def disk_io():
    """
    Get disk read bytes, write bytes, read count, write count, read time, write time.
    '/proc/partitions' contains current disk list.
    '/proc/diskstats' contains all disks and disk io information since system start.
    """

    # Get disk list
    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().strip().split("\n")[2:]

    disk_list = []
    for line in proc_partitions_lines:
        disk_list.append(line.split()[3].strip())

    # Get disk IO information
    with open("/proc/diskstats") as reader:
        proc_diskstats_lines = reader.read().strip().split("\n")

    _disk_io = {}
    for line in proc_diskstats_lines:
        line_split = line.split()
        disk_name = line_split[2]
        if disk_name not in disk_list:
            continue
        read_bytes = int(line_split[5]) * disk_sector_size
        write_bytes = int(line_split[9]) * disk_sector_size
        read_count = int(line_split[4])
        write_count = int(line_split[8])
        read_time = int(line_split[7])
        write_time = int(line_split[11])
        _disk_io[disk_name] = disk_stats(read_bytes, write_bytes, read_count, write_count, read_time, write_time)

    return _disk_io


def disk_list():
    """
    Get disk list.
    """

    with open("/proc/partitions") as reader:
        proc_partitions_lines = reader.read().strip().split("\n")[2:]

    _disk_list = []
    for line in proc_partitions_lines:
        _disk_list.append(line.split()[3].strip())

    return _disk_list


def disk_type(disk):
    """
    Get disk type (disk or partition).
    """

    with open("/sys/class/block/" + disk + "/uevent") as reader:
        sys_class_block_disk_uevent_lines = reader.read().split("\n")

    for line in sys_class_block_disk_uevent_lines:
        if "DEVTYPE" in line:
            _disk_type = line.split("=")[1]
            break

    return _disk_type


def disk_parent_name(disk):
    """
    Get disk parent name.
    """

    _disk_type = disk_type(disk)
    _disk_list = disk_list()

    _disk_parent_name = "-"
    if _disk_type == "partition":
        for check_disk_dir in _disk_list:
            if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + disk) == True:
                _disk_parent_name = check_disk_dir

    return _disk_parent_name


def file_system_info(disk='all'):
    """
    Get file system information (file systems, capacities, used, free, used percentages and mount points) of all disks.
    """

    _environment_type = environment_type()

    if disk == 'all':
        _disk_list = disk_list()
    else:
        _disk_list = [disk]

    # Get file system information of the mounted disks by using "df" command.
    command_list = ["df", "--output=source,fstype,size,used,avail,pcent,target"]
    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    df_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

    # Remove command output title line
    del df_output_lines[0]

    # Get mounted disk list
    mounted_disk_list = []
    for line in df_output_lines:
        disk_name = line.split()[0]
        mounted_disk_list.append(disk_name.split("/dev/")[-1])

    # Get file system information of the mounted and unmounted disks.
    _file_system_info = []
    for disk in _disk_list:
        if disk in mounted_disk_list:
            index = mounted_disk_list.index(disk)
            disk_file_system = df_output_lines[index].split()[1]
            disk_capacity = int(df_output_lines[index].split()[2]) * 1024
            disk_used = int(df_output_lines[index].split()[3]) * 1024
            disk_free = int(df_output_lines[index].split()[4]) * 1024
            disk_used_percentage = int(df_output_lines[index].split()[5].strip("%"))
            disk_mount_point = df_output_lines[index].split("% ", 1)[-1]
        else:
            disk_file_system = "[" + "Not mounted" + "]"
            disk_capacity = "[" + "Not mounted" + "]"
            disk_used = "[" + "Not mounted" + "]"
            disk_free = "[" + "Not mounted" + "]"
            disk_used_percentage = 0
            disk_mount_point = "[" + "Not mounted" + "]"
        _file_system_info.append(fs_info(disk, disk_file_system, disk_capacity, disk_used, disk_free, disk_used_percentage, disk_mount_point))

    return _file_system_info


def file_system(disk):
    """
    Get disk file system if it is detected as 'fuseblk' before (this happens for USB drives).
    Because "/proc/mounts" file contains file system information as in user space. To be able to get the
    actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
    """

    _environment_type = environment_type()

    disk_path = "/dev/" + disk

    command_list = ["lsblk", "-no", "FSTYPE", disk_path]
    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    try:
        lsblk_output_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        if len(lsblk_output_lines) > 1:
            _file_system = "[" + "Not mounted" + "]"
        else:
            _file_system = lsblk_output_lines[0]
    except Exception:
        _file_system = "fuseblk"

    return _file_system


def disk_read_write_data_func(disk):
    """
    Get disk read data and disk written data.
    """

    _disk_list = disk_list()

    disk_read_data = Performance.disk_read_data[_disk_list.index(disk)]
    disk_write_data = Performance.disk_write_data[_disk_list.index(disk)]

    return disk_read_data, disk_write_data


def disk_capacity_mass_storage(disk):
    """
    Get disk capacity (mass storage).
    This value is bigger than disk capacity (file system) value.
    """

    with open("/sys/class/block/" + disk + "/size") as reader:
        _disk_capacity_mass_storage = int(reader.read()) * disk_sector_size

    return _disk_capacity_mass_storage


def disk_label(disk):
    """
    Get disk label (file system).
    """

    _disk_label = "-"
    try:
        disk_label_list = os.listdir("/dev/disk/by-label/")
        for label in disk_label_list:
            if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == disk:
                # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                _disk_label = bytes(label, "utf-8").decode("unicode_escape")
    except FileNotFoundError:
        pass

    return _disk_label


def disk_vendor_model(disk):
    """
    Get disk vendor and model.
    """

    _disk_type = disk_type(disk)
    _disk_parent_name = disk_parent_name(disk)

    # Get parent disk name for getting disk vendor and model.
    if _disk_type == "disk":
        disk_or_parent_disk_name = disk
    elif _disk_type == "partition":
        disk_or_parent_disk_name = _disk_parent_name

    # Get disk vendor and model.
    device_vendor_name = "-"
    device_model_name = "-"

    # Get disk vendor and model if disk is a NVMe SSD.
    # These disks do not have "modalias" or "model" files under "/sys/class/block/[DISK]/device" directory.
    try:
        with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/modalias") as reader:
            modalias_output = reader.read().strip()
        device_vendor_name, device_model_name, _, _ = device_vendor_model(modalias_output)
    except (FileNotFoundError, NotADirectoryError) as me:
        pass

    # Get disk vendor and model if disk is a SCSI, IDE or virtio device (on QEMU virtual machines).
    try:
        with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/modalias") as reader:
            modalias_output = reader.read().strip()
        device_vendor_name, device_model_name, _, _ = device_vendor_model(modalias_output)
    except (FileNotFoundError, NotADirectoryError) as me:
        pass

    # Get disk vendor and model if disk is a SCSI or IDE disk.
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

    # Set device vendor model if it is not get so far.
    if device_vendor_name == "Unknown":
        device_vendor_name = "[" + "Unknown" + "]"
    if device_model_name == "Unknown":
        device_model_name = "[" + "Unknown" + "]"

    _disk_vendor_model = f'{device_vendor_name} - {device_model_name}'

    # Get disk vendor and model if disk is loop device.
    if disk.startswith("loop"):
        _disk_vendor_model = "[Loop Device]"

    # Get disk vendor and model if disk is a swap disk.
    if disk.startswith("zram"):
        _disk_vendor_model = "[" + "Swap" + "]"

    # Get disk vendor and model if disk is a ramdisk.
    if disk.startswith("ram"):
        _disk_vendor_model = "[Ramdisk]"

    # Get disk vendor and model if disk is a device mapper.
    if disk.startswith("dm-"):
        _disk_vendor_model = "[Device Mapper]"

    # Get disk vendor and model if disk is a memory card.
    if disk.startswith("mmcblk"):
        # Read database file for MMC disk register values.
        # For more info about CIDs: https://www.kernel.org/doc/Documentation/mmc/mmc-dev-attrs.txt
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
        _disk_vendor_model = f'{disk_vendor} - {disk_model} ({disk_card_type} Card, Class {disk_card_speed_class})'

    return _disk_vendor_model


#####################################################################################################
#                                        Network functions                                          #
#####################################################################################################

def network_io():
    """
    Get network card download bytes, upload bytes, download packets, upload packets.
    """

    # Get network card list
    network_card_list = []
    with open("/proc/net/dev") as reader:
        proc_net_dev_lines = reader.read().strip().split("\n")[2:]

    # Get network card IO information
    _network_io = {}
    for line in proc_net_dev_lines:
        line_split = line.split()
        network_card = line_split[0].split(":")[0]
        download_bytes = int(line_split[1])
        upload_bytes = int(line_split[9])
        download_packets = int(line_split[2])
        upload_packets = int(line_split[10])
        _network_io[network_card] = net_card_stats(download_bytes, upload_bytes, download_packets, upload_packets)

    return _network_io


def connection_type(network_card):
    """
    Get connection type on the network card.
    """

    if network_card.startswith("en"):
        _connection_type = "Ethernet"
    elif network_card.startswith("wl"):
        _connection_type = "Wi-Fi"
    else:
        _connection_type = "-"

    return _connection_type


def mac_address(network_card):
    """
    Get network card MAC address.
    """

    try:
        with open("/sys/class/net/" + network_card + "/address") as reader:
            _mac_address = reader.read().strip().upper()
    # Some network interfaces (such as virtual network interfaces) may not have a MAC address.
    except FileNotFoundError:
        _mac_address = "-"

    return _mac_address


def ipv4_ipv6_address(network_card):
    """
    Get IPv4 and IPv6 addresses on the network card.
    """

    try:
        ip_output = (subprocess.check_output(["ip", "a", "show", network_card], shell=False)).decode()
    # "ip" program is in "/sbin/" on some systems (such as Slackware based distributions).
    except FileNotFoundError:
        ip_output = (subprocess.check_output(["/sbin/ip", "a", "show", network_card], shell=False)).decode()

    ip_output_lines = ip_output.strip().split("\n")
    network_address_ipv4 = "-"
    network_address_ipv6 = "-"
    for line in ip_output_lines:
        if "inet " in line:
            network_address_ipv4 = line.split()[1].split("/")[0]
        if "inet6 " in line:
            network_address_ipv6 = line.split()[1].split("/")[0]

    _ipv4_ipv6_address = ipv4_ipv6(network_address_ipv4, network_address_ipv6)

    return _ipv4_ipv6_address


def network_card_vendor_model(network_card):
    """
    Get network card vendor and model.
    """

    device_vendor_name = "-"
    device_model_name = "-"

    # Get device vendor and model names if it is not a virtual device.
    if os.path.isdir("/sys/devices/virtual/net/" + network_card) == False:
        # Check if there is a "modalias" file. Some network interfaces (such as usb0, usb1, etc.) may not have this file.
        if os.path.isfile("/sys/class/net/" + network_card + "/device/modalias") == True:
            # Read device vendor and model ids by reading "modalias" file.
            with open("/sys/class/net/" + network_card + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = device_vendor_model(modalias_output)
            if device_vendor_name == "Unknown":
                device_vendor_name = "[" + "Unknown" + "]"
            if device_model_name == "Unknown":
                device_model_name = "[" + "Unknown" + "]"
        _network_card_vendor_model = f'{device_vendor_name} - {device_model_name}'

    # Get device vendor and model names if it is a virtual device.
    else:
        # lo (Loopback Device) is a system device and it is not a physical device. It could not be found in "pci.ids" file.
        if network_card == "lo":
            _network_card_vendor_model = "Loopback Device"
        else:
            _network_card_vendor_model = "[" + "Virtual Network Interface" + "]"

    return _network_card_vendor_model


def network_card_connected(network_card):
    """
    Get connected information for the network card.
    """

    with open("/sys/class/net/" + network_card + "/operstate") as reader:
        network_info = reader.read().strip()

    if network_info == "up":
        _network_card_connected = "Yes"
    elif network_info == "down":
        _network_card_connected = "No"
    elif network_info == "unknown":
        _network_card_connected = "[" + "Unknown" + "]"
    else:
        _network_card_connected = network_info

    return _network_card_connected


def network_ssid(network_card):
    """
    Get network name (SSID).
    """

    _environment_type = environment_type()

    command_list = ["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"]
    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    try:                                                                                      
        nmcli_output_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
    # Avoid errors because Network Manager (which is required for running "nmcli" command) may not be installed on all systems (very rare).
    except (FileNotFoundError, subprocess.CalledProcessError) as me:
        _network_ssid = "[" + "Unknown" + "]"

    # Check if "nmcli_output_lines" value is get.
    if "nmcli_output_lines" in locals():
        for line in nmcli_output_lines:
            line_splitted = line.split(":")
            if network_card == line_splitted[0]:
                _network_ssid = line_splitted[1].strip()
                break

    # "_network_ssid" value is get as "" if network card is not connected a Wi-Fi network.
    if _network_ssid == "":
        _network_ssid = "-"

    return _network_ssid


def link_quality(network_card):
    """
    Get network signal strength (link value).
    """

    _network_card_connected = network_card_connected(network_card)

    _link_quality = "-"
    # Translated value have to be used by using gettext constant. Not "Yes".
    if network_card.startswith("wl") == True and _network_card_connected == "Yes":
        with open("/proc/net/wireless") as reader:
            proc_net_wireless_output_lines = reader.read().strip().split("\n")
        for line in proc_net_wireless_output_lines:
            line_splitted = line.split()
            if network_card == line_splitted[0].split(":")[0]:
                # "split(".")" is used in order to remove "." at the end of the signal value.
                _link_quality = line_splitted[2].split(".")[0]
                if _link_quality != "-":
                    _link_quality = f'{_link_quality} (link)'
                break

    return _link_quality


#####################################################################################################
#                                          GPU functions                                            #
#####################################################################################################

def gpu_list():
    """
    Get GPU list.
    """

    _gpu_list = []

    # Get GPU list from "/sys/class/drm/" directory which is used by x86_64 desktop systems.
    if os.path.isdir("/dev/dri/") == True:

        for file in os.listdir("/sys/class/drm/"):
            if "-" not in file and file.split("-")[0].rstrip("0123456789") == "card":
                _gpu_list.append(file)

    # Get GPU list from "/sys/devices/" folder which is used by some ARM systems with NVIDIA GPU.
    for file in os.listdir("/sys/devices/"):

        if file.split(".")[0] == "gpu":
            _gpu_list.append(file)

    return _gpu_list


def gpu_device_paths(gpu):
    """
    Get device path and device sub-path of the GPU.
    """

    if os.path.isdir("/sys/class/drm/" + gpu + "/"):
        gpu_device_path = "/sys/class/drm/" + gpu + "/"
        gpu_device_sub_path = "/device/"
    else:
        if os.path.isdir("/sys/devices/" + file + "/"):
            gpu_device_path = "/sys/devices/" + file + "/"
            gpu_device_sub_path = "/"
        else:
            gpu_device_path = "-"
            gpu_device_sub_path = "-"

    return gpu_device_path, gpu_device_sub_path


def boot_vga():
    """
    Get GPU list.
    """

    _gpu_list = gpu_list()

    _boot_vga = "-"

    for _gpu in _gpu_list:
        try:
            with open("/sys/class/drm/" + _gpu + "/device/" + "boot_vga") as reader:
                if reader.read().strip() == "1":
                    _boot_vga = _gpu
        except (FileNotFoundError, NotADirectoryError) as me:
            pass

    # Get "boot_vga" information from "/sys/devices/" folder which is used by some ARM systems with NVIDIA GPU.
    if _boot_vga == "-":
        for _gpu in _gpu_list:
            try:
                with open("/sys/devices/" + _gpu + "/" + "boot_vga") as reader:
                    if reader.read().strip() == "1":
                        _boot_vga = _gpu
            except (FileNotFoundError, NotADirectoryError) as me:
                pass

    return _boot_vga


def gpu_driver(gpu):
    """
    Get GPU driver name.
    """

    _gpu_driver = "-"
    gpu_device_path, gpu_device_sub_path = gpu_device_paths(gpu)

    # Read device driver name by reading "uevent" file.
    try:
        with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
            uevent_output_lines = reader.read().strip().split("\n")
    except Exception:
        uevent_output_lines = "-"

    if uevent_output_lines != "-":
        for line in uevent_output_lines:
            if line.startswith("DRIVER="):
                _gpu_driver = line.split("=")[-1].strip()
                break

    return _gpu_driver


def gpu_pci_address(gpu):
    """
    Get GPU PCI address which will be used for detecting the selected GPU for processing GPU performance information.
    """

    gpu_device_path, gpu_device_sub_path = gpu_device_paths(gpu)

    # Read device driver name by reading "uevent" file.
    with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
        uevent_output_lines = reader.read().strip().split("\n")

    # ARM GPUs does not have PCI address.
    _gpu_pci_address = "-"
    for line in uevent_output_lines:
        if line.startswith("PCI_SLOT_NAME="):
            _gpu_pci_address = line.split("=")[-1]
            break

    return _gpu_pci_address


def resolution_refresh_rate():
    """
    Get current resolution and refresh rate of the monitor(s).
    """

    try:
        import gi
        gi.require_version('Gdk', '4.0')
        from gi.repository import Gdk
        monitor_list = Gdk.Display().get_default().get_monitors()
    except Exception:
        monitor_list = "-"
        resolution = "-"
        refresh_rate = "-"

    _resolution_refresh_rate = []
    if monitor_list != "-":
        for monitor in monitor_list:
            monitor_rectangle = monitor.get_geometry()
            monitor_width = monitor_rectangle.width
            monitor_height = monitor_rectangle.height
            resolution = str(monitor_width) + "x" + str(monitor_height)
            # Milli-Hertz is converted to Hertz
            refresh_rate = float(monitor.get_refresh_rate() / 1000)
            refresh_rate = f'{refresh_rate:.2f} Hz'
            _resolution_refresh_rate.append(monitor_info(resolution, refresh_rate))
    else:
        _resolution_refresh_rate = [monitor_info(resolution, refresh_rate)]

    return _resolution_refresh_rate


def gpu_vendor_model(gpu):
    """
    Get GPU device model name and vendor name.
    """

    gpu_device_path, gpu_device_sub_path = gpu_device_paths(gpu)

    # Read device vendor and model ids by reading "modalias" file.
    with open(gpu_device_path + gpu_device_sub_path + "modalias") as reader:
        modalias_output = reader.read().strip()

    # Determine device subtype.
    device_subtype, device_alias = modalias_output.split(":", 1)
    device_vendor_name, device_model_name, device_vendor_id, device_model_id = device_vendor_model(modalias_output)

    if device_vendor_name == "Unknown":
        device_vendor_name = "[" + _tr("Unknown") + "]"
    if device_model_name == "Unknown":
        device_model_name = "[" + _tr("Unknown") + "]"

    _gpu_vendor_model = dev_vendor_model(device_vendor_name, device_model_name, device_vendor_id, device_model_id )

    return _gpu_vendor_model


def gpu_statistics(gpu):
    """
    Get GPU load, memory, frequencies, power.
    """

    _environment_type = environment_type()
    gpu_device_path, gpu_device_sub_path = gpu_device_paths(gpu)
    _gpu_pci_address = gpu_pci_address(gpu)
    _gpu_vendor_model = gpu_vendor_model(gpu)
    device_vendor_id = _gpu_vendor_model.vendor_id

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
    if device_vendor_id == "v00008086":

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
    if device_vendor_id in ["v00001022", "v00001002"]:

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
            gpu_load_amd_func()
            gpu_load = f'{(sum(amd_gpu_load_list) / len(amd_gpu_load_list)):.0f} %'
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
    if device_vendor_id in ["Brcm"]:

        # Get GPU memory capacity. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
        try:
            command_list = ["vcgencmd", "get_mem", "gpu"]
            if _environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            gpu_memory_capacity = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
        except Exception:
            gpu_memory_capacity = "-"

        # Get GPU current frequency. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
        try:
            command_list = ["vcgencmd", "measure_clock", "core"]
            if _environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            gpu_current_frequency = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
            gpu_current_frequency = f'{float(gpu_current_frequency)/1000000:.0f} MHz'
        except Exception:
            gpu_current_frequency = "-"


    # If selected GPU vendor is NVIDIA and selected GPU is used on a PCI used system.
    if device_vendor_id == "v000010DE" and gpu_device_path.startswith("/sys/class/drm/") == True:

        # Try to get GPU usage information in a separate thread in order to prevent this function from blocking the main thread and GUI for a very small time which stops the GUI for a very small time.
        gpu_tool_output = "-"
        Thread(target=gpu_load_nvidia_func, daemon=True).start()

        try:
            gpu_tool_output = gpu_tool_output
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
    if device_vendor_id in ["v000010DE", "Nvidia"] and gpu_device_path.startswith("/sys/devices/") == True:

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

    _gpu_statistics = gpu_stats(gpu_load, gpu_memory, gpu_current_frequency, gpu_min_max_frequency, gpu_temperature, gpu_power)

    return _gpu_statistics


def gpu_load_nvidia_func():
    """
    Get GPU load average for NVIDIA (PCI) GPUs.
    """

    # Define command for getting GPU usage information.
    command_list = ["nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,power.draw", "--format=csv"]
    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    # Get GPU usage information.
    try:
        gpu_tool_output = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
    # Prevent errors because nvidia-smi may not be installed on some devices (such as N.Switch with NVIDIA Tegra GPU).
    except FileNotFoundError:
        pass


def gpu_load_amd_func(*args):
    """
    Get GPU load average for AMD GPUs.
    """

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
    if Config.current_main_tab != 0 or Config.performance_tab_current_sub_tab != 5:
        return

    self.gpu_glib_source.set_callback(gpu_load_amd_func)
    # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
    self.gpu_glib_source.attach(GLib.MainContext.default())


#####################################################################################################
#                                        System functions                                           #
#####################################################################################################

def os_name_version():
    """
    Get OS name, version, version code name and OS based on information.
    """

    _environment_type = environment_type()

    if _environment_type == "flatpak":
        with open("/var/run/host/etc/os-release") as reader:
            os_release_output_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/os-release") as reader:
            os_release_output_lines = reader.read().strip().split("\n")

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
        if _environment_type == "flatpak":
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

    _os_name_version = os_info(os_name, os_version, os_based_on)

    return _os_name_version


def os_family():
    """
    Get OS family.
    """

    _os_family = platform.system()

    if _os_family == "":
        _os_family = "-"

    return _os_family


def kernel_information():
    """
    Get kernel release (base version of kernel) and kernel version (package version of kernel).
    """

    # Get kernel release (base version of kernel)
    kernel_release = platform.release()
    if kernel_release == "":
        kernel_release = "-"

    # Get kernel version (package version of kernel)
    kernel_version = platform.version()
    if kernel_version == "":
        kernel_version = "-"

    _kernel_information = kernel_info(kernel_release, kernel_version)

    return _kernel_information


def computer_information():
    """
    Get computer vendor, model and chassis type
    '/sys/devices/virtual/dmi' is used for UEFI/ACPI systems and this directory is not found on ARM systems.
    """

    # Get computer vendor
    try:
        with open("/sys/devices/virtual/dmi/id/sys_vendor") as reader:
            computer_vendor = reader.read().strip()
    except FileNotFoundError:
        computer_vendor = "-"

    # Get computer model
    try:
        with open("/sys/devices/virtual/dmi/id/product_name") as reader:
            computer_model = reader.read().strip()
    except FileNotFoundError:
        # Try to get computer model for ARM systems.
        try:
            # "/proc/device-tree/model" is a symlink to "/sys/firmware/devicetree/base/model" and using it is safer.
            # For details: https://github.com/torvalds/linux/blob/v5.9/Documentation/ABI/testing/sysfs-firmware-ofw
            with open("/proc/device-tree/model") as reader:
                computer_model = reader.read().strip()
        except FileNotFoundError:
            computer_model = "-"

    # Get computer chassis
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

    _computer_information = computer_info(computer_vendor, computer_model, computer_chassis_type)

    return _computer_information


def host_name():
    """
    Get host name.
    """

    with open("/proc/sys/kernel/hostname") as reader:
        _host_name = reader.read().strip()

    return _host_name


def monitor_count():
    """
    Get number of monitors.
    """

    try:
        monitor_list = Gdk.Display().get_default().get_monitors()
        _monitor_count = len(monitor_list)
    except Exception:
        _monitor_count = "-"

    return _monitor_count


def flatpak_package_count():
    """
    Get number of installed Flatpak packages (and runtimes).
    """

    _environment_type = environment_type()

    _flatpak_package_count = "-"

    command_list = ["flatpak", "list"]
    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list

    try:
        flatpak_packages_available = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        # Differentiate empty line count
        _flatpak_package_count = len(flatpak_packages_available) - flatpak_packages_available.count("")
    except (FileNotFoundError, subprocess.CalledProcessError) as me:
        _flatpak_package_count = "-"

    return _flatpak_package_count


def apt_rpm_pacman_package_count():
    """
    Get number of installed APT, RPM or pacman packages.
    """

    _environment_type = environment_type()

    # Initial value of the variables.
    apt_packages_available = "-"
    rpm_packages_available = "-"
    pacman_packages_available = "-"
    _apt_rpm_pacman_package_count = "-"

    # Get number of APT (deb) packages if available.
    try:
        command_list = ["dpkg", "-s", "python3"]
        if _environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        # Check if "python3" is installed in order to determine package type of the system.
        apt_packages_available = (subprocess.check_output(command_list, shell=False)).decode().strip()
        if "Package: python3" in apt_packages_available:
            command_list = ["dpkg", "--list"]
            if _environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            number_of_installed_apt_packages = (subprocess.check_output(command_list, shell=False)).decode().strip().count("\nii  ")
            _apt_rpm_pacman_package_count = f'{number_of_installed_apt_packages} (APT)'
    # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system.
    # It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
    except (FileNotFoundError, subprocess.CalledProcessError) as me:
        apt_packages_available = "-"

    # Get number of RPM packages if available.
    if apt_packages_available == "-":
        try:
            command_list = ["rpm", "-q", "python3"]
            if _environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            rpm_packages_available = (subprocess.check_output(command_list, shell=False)).decode().strip()
            if rpm_packages_available.startswith("python3-3."):
                command_list = ["rpm", "-qa"]
                if _environment_type == "flatpak":
                    command_list = ["flatpak-spawn", "--host"] + command_list
                number_of_installed_rpm_packages = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
                # Differentiate empty line count
                number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")
                _apt_rpm_pacman_package_count = f'{number_of_installed_rpm_packages} (RPM)'
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            rpm_packages_available = "-"

    # Get number of pacman (Arch Linux) packages if available.
    if apt_packages_available == "-" and rpm_packages_available == "-":
        try:
            command_list = ["pacman", "-Q", "python3"]
            if _environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            pacman_packages_available = (subprocess.check_output(command_list, shell=False)).decode().strip()
            if pacman_packages_available.startswith("python 3."):
                command_list = ["pacman", "-Qq"]
                if _environment_type == "flatpak":
                    command_list = ["flatpak-spawn", "--host"] + command_list
                number_of_installed_pacman_packages = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
                # Differentiate empty line count
                number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")
                _apt_rpm_pacman_package_count = f'{number_of_installed_pacman_packages} (pacman)'
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            pacman_packages_available = "-"

    return _apt_rpm_pacman_package_count


def python_gtk_version():
    """
    Get current Python version and GTK version.
    """

    # Get current Python version (Python which is running this code)
    python_version = platform.python_version()

    # Get GTK version which is used for this application.
    try:
        gtk_version = f'{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}'
    except Exception:
        gtk_version = "-"

    _python_gtk_version = package_version(python_version, gtk_version)

    return _python_gtk_version


def desktop_components():
    """
    Get current desktop environment, windowing system, window manager, display manager.
    """

    _environment_type = environment_type()

    # Get current username
    # Get user name that gets root privileges.
    # Otherwise, username is get as "root" when root access is get.
    current_user_name = os.environ.get('SUDO_USER')
    # Get username in the following way if current application has not been run by root privileges.
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
                                      "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome", "muffin"]
    # First values are process names of the display managers, second values
    # are names of the display managers.
    supported_display_managers_dict = {"lightdm":"lightdm", "gdm":"gdm", "gdm3":"gdm3", "sddm":"sddm", "xdm":"xdm", "lxdm-binary":"lxdm"}                                                       

    # Try to detect windowing system, window manager, current desktop 
    # environment and current display manager by reading process names and
    # other details.
    command_list = ["ps", "--no-headers", "-eo", "comm,user"]
    if _environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    ps_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

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
    current_desktop_environment_version = desktop_environment_version(current_desktop_environment)

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

    _desktop_components = desktop_comp(current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager)

    return _desktop_components


def desktop_environment_version(current_desktop_environment):
    """
    Get current desktop environment version.
    """

    _environment_type = environment_type()

    desktop_environment_version_command_dict = {
                                                "XFCE":["xfce4-panel", "--version"],
                                                "GNOME":["gnome-shell", "--version"],
                                                "zorin:GNOME":["gnome-shell", "--version"],
                                                "ubuntu:GNOME":["gnome-shell", "--version"],
                                                "X-Cinnamon":["cinnamon", "--version"],
                                                "CINNAMON":["cinnamon", "--version"],
                                                "MATE":["mate-about", "--version"],
                                                "KDE":["plasmashell", "--version"],
                                                "LXQt":["lxqt-about", "--version"],
                                                "Budgie":["budgie-desktop", "--version"],
                                                "Budgie:GNOME":["budgie-desktop", "--version"]
                                                }

    current_desktop_environment_version = "-"

    if current_desktop_environment in desktop_environment_version_command_dict:
        command_list = desktop_environment_version_command_dict[current_desktop_environment]
        if _environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        try:
            desktop_environment_version_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        except Exception:
            desktop_environment_version_output = "-"
    else:
        desktop_environment_version_output = "-"

    if current_desktop_environment == "XFCE":
        for line in desktop_environment_version_output.split("\n"):
            if "xfce4-panel" in line:
                current_desktop_environment_version = line.split(" ")[1]

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




"""time1=time.time()
#cpu_core_frequency = cpu_core_frequency(core="0", freq='current', unit="MHz")
a = cpu_times()
print(time.time()-time1)

print(a)"""

