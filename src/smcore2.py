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

