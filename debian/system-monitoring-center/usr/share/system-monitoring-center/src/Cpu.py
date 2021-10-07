#!/usr/bin/env python3

# ----------------------------------- CPU - CPU Tab GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def cpu_import_func():

    global Gtk, GLib, Thread, os, platform

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os
    import platform


    global Config, MainGUI, Performance, CpuGUI
    import Config, MainGUI, Performance, CpuGUI


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


# ----------------------------------- CPU - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def cpu_initial_func():

    number_of_logical_cores = Performance.number_of_logical_cores
    logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
    selected_cpu_core_number = Performance.selected_cpu_core_number
    selected_cpu_core = Performance.selected_cpu_core

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
    cpu_architecture = platform.processor()
    if cpu_architecture == "":
        cpu_architecture = platform.machine()
        if cpu_architecture == "":
            cpu_architecture = "-"

    # Set CPU tab label texts by using information get
    show_cpu_usage_per_core = Config.show_cpu_usage_per_core
    if show_cpu_usage_per_core == 0:
        CpuGUI.label1113.set_text(_tr("CPU Usage % (Average):"))
    if show_cpu_usage_per_core == 1:
        CpuGUI.label1113.set_text(_tr("CPU Usage % (Per Core):"))
    CpuGUI.label1101.set_text(cpu_model_names[selected_cpu_core_number])
#         CpuGUI.label1102.set_text(f'Selected CPU Core: {selected_cpu_core}')
    CpuGUI.label1102.set_text(_tr("Selected CPU Core: ") + selected_cpu_core)
    if isinstance(cpu_max_frequency_all_cores[selected_cpu_core_number], str) is False:
        CpuGUI.label1105.set_text(f'{cpu_min_frequency_all_cores[selected_cpu_core_number]:.0f} - {cpu_max_frequency_all_cores[selected_cpu_core_number]:.0f} MHz')
    if isinstance(cpu_max_frequency_all_cores[selected_cpu_core_number], str) is True:
        CpuGUI.label1105.set_text(f'{cpu_min_frequency_all_cores[selected_cpu_core_number]} - {cpu_max_frequency_all_cores[selected_cpu_core_number]}')
    CpuGUI.label1106.set_text(f'{number_of_cpu_sockets}')
    CpuGUI.label1107.set_text(f'{number_of_physical_cores} - {number_of_logical_cores}')
    CpuGUI.label1108.set_text(cpu_architecture)
    CpuGUI.label1109.set_text(f'{cpu_l1i_cache_values[selected_cpu_core_number]} - {cpu_l1d_cache_values[selected_cpu_core_number]}')
    CpuGUI.label1110.set_text(f'{cpu_l2_cache_values[selected_cpu_core_number]} - {cpu_l3_cache_values[selected_cpu_core_number]}')


# ----------------------------------- CPU - Get CPU Data Function (gets CPU data, shows on the labels on the GUI) -----------------------------------
def cpu_loop_func():

    logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
    cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
    selected_cpu_core_number = Performance.selected_cpu_core_number

    CpuGUI.drawingarea1101.queue_draw()

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
    pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
    for pid in pid_list:
        try:                                                                                  # try-except is used in order to pass the loop without application error if a "FileNotFoundError" error is encountered when process is ended after process list is get.
            with open("/proc/" + pid + "/status") as reader:
                proc_status_output = reader.read()
                thread_count_list.append(int(proc_status_output.split("\nThreads:")[1].split("\n")[0].strip()))    # Append number of threads of the process
        except (FileNotFoundError, ProcessLookupError) as me:
            pass
    number_of_total_processes = len(thread_count_list)
    number_of_total_threads = sum(thread_count_list)

    # Set and update CPU tab label texts by using information get
    CpuGUI.label1111.set_text(f'{number_of_total_processes} - {number_of_total_threads}')
    CpuGUI.label1112.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
    CpuGUI.label1103.set_text(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
    CpuGUI.label1104.set_text(f'{cpu_current_frequency_all_cores[int(selected_cpu_core_number)]:.0f} MHz')


# ----------------------------------- CPU Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def cpu_initial_thread_func():

    GLib.idle_add(cpu_initial_func)


# ----------------------------------- CPU Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def cpu_loop_thread_func(dummy_variable):                                                     # "dummy_variable" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

#     GLib.idle_add(cpu_loop_func)
#     if MainGUI.radiobutton1001.get_active() == True:
#         global update_interval
#         update_interval = Config.update_interval
#         GLib.timeout_add(update_interval * 1000, cpu_loop_thread_func)

    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1001.get_active() == True:
        global cpu_glib_source, update_interval                                               # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            cpu_glib_source.destroy()                                                         # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        cpu_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(cpu_loop_func)
        cpu_glib_source.set_callback(cpu_loop_thread_func)
        cpu_glib_source.attach(GLib.MainContext.default())                                    # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- CPU Thread Run Function (starts execution of the threads) -----------------------------------
def cpu_thread_run_func():

    if "update_interval" not in globals():                                                    # To be able to run initial thread for only one time
        cpu_initial_thread = Thread(target=cpu_initial_thread_func, daemon=True)
        cpu_initial_thread.start()
        cpu_initial_thread.join()
    cpu_loop_thread = Thread(target=cpu_loop_thread_func(None), daemon=True)                  # "None" is an arbitrary value which is required for using "GLib.timeout_source_new()".
    cpu_loop_thread.start()
