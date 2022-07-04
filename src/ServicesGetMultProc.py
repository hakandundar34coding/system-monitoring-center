#!/usr/bin/env python3

# ----------------------- Get number of CPU cores to be used at the same time for getting service data -----------------------
def services_number_of_cpu_cores_used_func(number_of_logical_cores):

    # 1 or 2 CPU cores are not used in order to avoid reducing performance of other processes or the system.
    # Using more than 5 CPU cores does not improve performance noticeably on a 4 physical (8 logical) core system.
    if number_of_logical_cores == 3:
        number_of_cpu_cores_used = 2
    if number_of_logical_cores in [4, 5, 6, 7]:
        number_of_cpu_cores_used = number_of_logical_cores - 2
    if number_of_logical_cores > 7:
        number_of_cpu_cores_used = 5

    return number_of_cpu_cores_used


# ----------------------- Split service list into [number_of_cpu_cores_used] lists for using them to get service data by using multiprocessing -----------------------
def services_unit_files_command_split_func(number_of_cpu_cores_used, unit_files_command):

    # Get service list and unit file command parameters.
    service_list = unit_files_command[3:]
    unit_files_command = unit_files_command[:3]

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


# ----------------------- Get service data by using multiprocessing -----------------------
def get_service_data_func(queue1, i, unit_files_command_split):

    try:
        systemctl_show_command_lines_split = (subprocess.check_output(unit_files_command_split, shell=False)).decode().strip().split("\n\n")
    # Prevent errors if "systemd" is not used on the system.
    except Exception:
        pass

    # Put the service data (and process number) into queue in order to get it, reorder and merge them by using the main process. It is a FIFO queue and data can be get in the same order which they are put into the queue.
    # Nested "[}" required for putting the data as a list.
    queue1.put([[i, systemctl_show_command_lines_split]])


# ----------------------- Run the reuqired functions and start processes to get the service data by using multiprocessing -----------------------
def start_processes_func(number_of_logical_cores, unit_files_command):

    # Import modules in this function because entire module is run separately by the all processes if multiprocessing is used.
    global subprocess
    import subprocess
    import multiprocessing

    # Get the required data.
    number_of_cpu_cores_used = services_number_of_cpu_cores_used_func(number_of_logical_cores)
    unit_files_command_split = services_unit_files_command_split_func(number_of_cpu_cores_used, unit_files_command)

    # Define a queue for getting the data from the processes.
    queue1 = multiprocessing.Queue()

    # Generate processes and their argments (queue, process number for reordering the output, command per process).
    process_list = [multiprocessing.Process(target=get_service_data_func, args=(queue1, i, unit_files_command_split[i]), daemon=True) for i in range(number_of_cpu_cores_used)]

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

