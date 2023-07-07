def start_processes_func(number_of_logical_cores, unit_files_command):
    """
    Run the reuqired functions and start processes to get the service data by using multiprocessing.
    """

    # Import modules in this function because entire module is run separately by the all processes if multiprocessing is used.
    import multiprocessing
    from . import Libsysmon

    # Get the required data.
    number_of_cpu_cores_used = Libsysmon.get_core_count_for_getting_services(number_of_logical_cores)
    unit_files_command_split = Libsysmon.split_unit_files_command_output(number_of_cpu_cores_used, unit_files_command)

    # Define a queue for getting the data from the processes.
    queue1 = multiprocessing.Queue()

    # Generate processes and their argments (queue, process number for reordering the output, command per process).
    process_list = [multiprocessing.Process(target=Libsysmon.get_service_data, args=(queue1, i, unit_files_command_split[i]), daemon=True) for i in range(number_of_cpu_cores_used)]

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

