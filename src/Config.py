#! /usr/bin/python3

# ----------------------------------- Config - Config Import Function -----------------------------------
def config_import_func():

    global os
    import os


# ----------------------------------- Config - Config Read Function (reads settings from configration file) -----------------------------------
def config_read_func():

    # Define configration folder and file directory
    global config_file_path
    current_user_homedir = os.environ.get('HOME')
    config_folder_path = current_user_homedir + "/.config/system-monitoring-center/"
    config_file_path = config_folder_path + "config.txt"

    global number_precision_list, data_unit_list, data_speed_unit_list
    # number_precision_list data info: [[ordering number, used in the code to get data, data unit, precision number], ...]
    number_precision_list = [[0, '0', 0], [1, '0.0', 1], [2, '0,00', 2], [3, '0,000', 3]]
    # data_unit_list data info: [[ordering number, used in the code to get data, data unit, precision number], ...]
    data_unit_list = [[0, 'Auto', 0], [1, 'B', 1], [2, 'KiB', 2], [3, 'MiB', 3],
                     [4, 'GiB', 4], [5, 'TiB', 5], [6, 'PiB', 6], [7, 'EiB', 7]]
    # data_speed_unit_list data info: [[ordering number, used in the code to get data, data unit, precision number], ...]
    data_speed_unit_list = [[0, 'Auto-Byte', 0], [1, 'B/s', 1], [2, 'KiB/s', 2], [3, 'MiB/s', 3],
                           [4, 'GiB/s', 4], [5, 'TiB/s', 5], [6, 'PiB/s', 6], [7, 'EiB/s', 7],
                           [8, 'Auto-bit', 8], [9, 'b/s', 9], [10, 'Kib/s', 10], [11, 'Mib/s', 11],
                           [12, 'Gib/s', 12], [13, 'Tib/s', 13], [14, 'Pib/s', 14], [15, 'Eib/s', 15]]


    # Define variables to read config data
    global reset_all_settings_with_new_release_value                                      # This value is used for resetting all settings. This integer value is increased "1" in the new application release if resetting is wanted by the developer. Code reads this value from the config file and compares with the value in the code. All settings are reset if integer value of this value is bigger than the value in the config file. There is no action if integer value of this value is smaller than the value in the config file. There is no relationship between this value and application version.
    reset_all_settings_with_new_release_value = 2
    global config_variables, config_values
    config_variables = []
    config_values = []
    # Read config file
    try:
        with open(config_file_path) as reader:
            config_lines = reader.read().split("\n")
    except Exception:
        # Generate config folder
        if os.path.exists(config_folder_path) == False:
            os.makedirs(config_folder_path)
        # Read/reset default config data and save to file
        config_default_reset_all_func()
        config_save_func()
        return
    # Add config names and values into separate lists
    for line in config_lines:
        if " = " in line:
            line_split = line.split(" = ")
            config_variables.append(line_split[0])
            config_values.append(line_split[1])
    # Read/reset default config data before getting values from the lists which is read from file because some new settings may be added and they may not be present in the config file.
    # Default values are read and modified by the user defined values if they are available.
    config_default_reset_all_func()
    # Get config data from the lists which is read from file
    try:
        config_get_values_func()
    except Exception:
        pass
    # Reset user config data if relevant setting is changed by the developer
    if 'reset_all_settings_with_new_release' not in globals() or reset_all_settings_with_new_release < reset_all_settings_with_new_release_value:
        config_default_reset_all_func()
        config_save_func()


# ----------------------------------- Config - Config Default Reset All Function (Defines default settings by user demand or if there are any problems during reading config file and its content) -----------------------------------
def config_default_reset_all_func():
    config_default_general_general_func()
    config_default_general_floating_summary_func()
    config_default_performance_cpu_func()
    config_default_performance_ram_func()
    config_default_performance_disk_func()
    config_default_performance_network_func()
    config_default_performance_gpu_func()
    config_default_performance_sensors_row_column_func()
    config_default_processes_func()
    config_default_processes_row_sort_column_order_func()
    config_default_users_func()
    config_default_users_row_sort_column_order_func()
    config_default_startup_func()
    config_default_startup_row_sort_column_order_func()
    config_default_services_func()
    config_default_services_row_sort_column_order_func()

# ----------------------------------- Config - Config Default General Function -----------------------------------
def config_default_general_general_func():
    global reset_all_settings_with_new_release
    global update_interval, chart_data_history, default_main_tab, performance_tab_default_sub_tab
    global performance_summary_on_the_headerbar, remember_last_opened_tabs_on_application_start, chart_background_color_all_charts
    global remember_last_selected_hardware
    reset_all_settings_with_new_release = reset_all_settings_with_new_release_value 
    update_interval = 0.75
    chart_data_history = 150
    default_main_tab = 0
    performance_tab_default_sub_tab = 0
    performance_summary_on_the_headerbar = 1
    remember_last_opened_tabs_on_application_start = 0
    chart_background_color_all_charts = [0.0, 0.0, 0.0, 0.0]
    remember_last_selected_hardware = 0

# Adding a new setting
#     global new_setting
#     new_setting=1

# ----------------------------------- Config - Config Default Floating Summary Function -----------------------------------
def config_default_general_floating_summary_func():
    global show_floating_summary, floating_summary_window_transparency, floating_summary_data_shown
    show_floating_summary = 0
    floating_summary_window_transparency = 0.6
    floating_summary_data_shown = [0, 1]                                                      # floating_summary_data_shown all values = [0, 1, 2, 3, 4, 5, 6, 7] - [0: CPU, 1: RAM, 2: Disk Read+Write, 3: Disk Read, 4: Disk Write, 5: Network Receive+Send, 6: Network Receive, 7: Network Send]

# ----------------------------------- Config - Config Default Performance Tab-CPU Tab Function -----------------------------------
def config_default_performance_cpu_func():
    global chart_background_color_all_charts, chart_line_color_cpu_percent, show_cpu_usage_per_core, performance_cpu_usage_percent_precision, selected_cpu_core
    chart_background_color_all_charts = [0.0, 0.0, 0.0, 0.0]
    chart_line_color_cpu_percent = [0.29, 0.78, 0.0, 1.0]
    show_cpu_usage_per_core = 0
    performance_cpu_usage_percent_precision = 0
    selected_cpu_core = ""

# ----------------------------------- Config - Config Default Performance Tab-RAM Tab Function -----------------------------------
def config_default_performance_ram_func():
    global chart_background_color_all_charts, chart_line_color_ram_swap_percent, performance_ram_swap_data_precision, performance_ram_swap_data_unit
    chart_background_color_all_charts = [0.0, 0.0, 0.0, 0.0]
    chart_line_color_ram_swap_percent = [0.27, 0.49, 1.0, 1.0]
    performance_ram_swap_data_precision = 1
    performance_ram_swap_data_unit = 0

# ----------------------------------- Config - Config Default Performance Tab-Disk Tab Function -----------------------------------
def config_default_performance_disk_func():
    global chart_background_color_all_charts, chart_line_color_disk_speed_usage, performance_disk_speed_data_precision, performance_disk_usage_data_precision
    global performance_disk_speed_data_unit, performance_disk_usage_data_unit, plot_disk_read_speed, plot_disk_write_speed, selected_disk
    chart_background_color_all_charts = [0.0, 0.0, 0.0, 0.0]
    chart_line_color_disk_speed_usage = [1.0, 0.44, 0.17, 1.0]
    performance_disk_speed_data_precision = 1
    performance_disk_usage_data_precision = 1
    performance_disk_speed_data_unit = 0
    performance_disk_usage_data_unit = 0
    plot_disk_read_speed = 1
    plot_disk_write_speed = 1
    selected_disk = ""

# ----------------------------------- Config - Config Default Performance Tab-Network Tab Function -----------------------------------
def config_default_performance_network_func():
    global chart_background_color_all_charts, chart_line_color_network_speed_data, performance_network_speed_data_precision, performance_network_data_data_precision
    global performance_network_speed_data_unit, performance_network_data_data_unit, plot_network_download_speed, plot_network_upload_speed, selected_network_card
    chart_background_color_all_charts = [0.0, 0.0, 0.0, 0.0]
    chart_line_color_network_speed_data = [0.56, 0.30, 0.78, 1.0]
    performance_network_speed_data_precision = 1
    performance_network_data_data_precision = 2
    performance_network_speed_data_unit = 0
    performance_network_data_data_unit = 0
    plot_network_download_speed = 1
    plot_network_upload_speed = 1
    selected_network_card = ""

# ----------------------------------- Config - Config Default Performance Tab-GPU Tab Function -----------------------------------
def config_default_performance_gpu_func():
    global chart_background_color_all_charts, chart_line_color_fps, selected_gpu
    chart_background_color_all_charts = [0.0, 0.0, 0.0, 0.0]
    chart_line_color_fps = [1.0, 0.09, 0.09, 1.0]
    selected_gpu = ""

# ----------------------------------- Config - Config Default Performance Tab-Sensors Tab Row Sort Column Order Width Function -----------------------------------
def config_default_performance_sensors_row_column_func():
    global sensors_treeview_columns_shown, sensors_data_row_sorting_column, sensors_data_row_sorting_order, sensors_data_column_order, sensors_data_column_widths
    sensors_treeview_columns_shown = [0, 1, 2, 3, 4]
    sensors_data_row_sorting_column = 0
    sensors_data_row_sorting_order = 0
    sensors_data_column_order = [0, 1, 2, 3, 4]                                               # sensors_data_column_order all values = [0, 1, 2, 3]
    sensors_data_column_widths = [-1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Default Processes Tab Function -----------------------------------
def config_default_processes_func():
    global show_processes_of_all_users, show_processes_as_tree, show_tree_lines, processes_cpu_usage_percent_precision
    global processes_ram_swap_data_precision, processes_ram_swap_data_unit, processes_disk_speed_data_precision, processes_disk_usage_data_precision
    global processes_disk_speed_data_unit, processes_disk_usage_data_unit, warn_before_stopping_processes
    global processes_treeview_columns_shown, processes_data_row_sorting_column, processes_data_row_sorting_order, processes_data_column_order, processes_data_column_widths
    show_processes_of_all_users = 1
    show_processes_as_tree = 0
    show_tree_lines = 0
    processes_cpu_usage_percent_precision = 0
    processes_ram_swap_data_precision = 1
    processes_ram_swap_data_unit = 0
    processes_disk_speed_data_precision = 1
    processes_disk_usage_data_precision = 1
    processes_disk_speed_data_unit = 0
    processes_disk_usage_data_unit = 0
    warn_before_stopping_processes = 1
    processes_treeview_columns_shown = [0, 1, 2, 4, 5, 10, 11]                                # Processes data to be get, processed and shown. processes_treeview_columns_shown all values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    processes_data_row_sorting_column = 0                                                     # Column number for row sorting
    processes_data_row_sorting_order = 0
    processes_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    processes_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Default Processes Tab Row Sort Column Order Function -----------------------------------
def config_default_processes_row_sort_column_order_func():
    global processes_data_row_sorting_column, processes_data_row_sorting_order, processes_data_column_order, processes_data_column_widths
    processes_data_row_sorting_column = 0                                                     # Column number for row sorting
    processes_data_row_sorting_order = 0
    processes_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    processes_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Default Users Tab Function -----------------------------------
def config_default_users_func():
    global users_cpu_usage_percent_precision, users_ram_swap_data_precision, users_ram_swap_data_unit
    global users_treeview_columns_shown, users_data_row_sorting_column, users_data_row_sorting_order, users_data_column_order, users_data_column_widths
    users_cpu_usage_percent_precision = 0
    users_ram_swap_data_precision = 1
    users_ram_swap_data_unit = 0
    users_treeview_columns_shown = [0, 2, 3, 5, 7, 12, 13]                                    # users_treeview_columns_shown all values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    users_data_row_sorting_column = 0
    users_data_row_sorting_order = 0
    users_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    users_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Default Users Tab Row Sort Column Order Function -----------------------------------
def config_default_users_row_sort_column_order_func():
    global users_data_row_sorting_column, users_data_row_sorting_order, users_data_column_order, users_data_column_widths
    users_data_row_sorting_column = 0
    users_data_row_sorting_order = 0
    users_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    users_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Default Startup Tab Function -----------------------------------
def config_default_startup_func():
    global startup_treeview_columns_shown, startup_data_row_sorting_column, startup_data_row_sorting_order, startup_data_column_order, startup_data_column_widths
    startup_treeview_columns_shown = [0, 1, 2]                                                # startup_treeview_columns_shown all values = [0, 1, 2]
    startup_data_row_sorting_column = 0
    startup_data_row_sorting_order = 0
    startup_data_column_order = [0, 1, 2]
    startup_data_column_widths = [-1, -1, -1]

# ----------------------------------- Config - Config Default Startup Tab Row Sort Column Order Function -----------------------------------
def config_default_startup_row_sort_column_order_func():
    global startup_data_row_sorting_column, startup_data_row_sorting_order, startup_data_column_order, startup_data_column_widths
    startup_data_row_sorting_column = 0
    startup_data_row_sorting_order = 0
    startup_data_column_order = [0, 1, 2]
    startup_data_column_widths = [-1, -1, -1]

# ----------------------------------- Config - Config Default Services Tab Function -----------------------------------
def config_default_services_func():
    global services_ram_swap_data_precision, services_ram_swap_data_unit
    global services_treeview_columns_shown, services_data_row_sorting_column, services_data_row_sorting_order, services_data_column_order, services_data_column_widths
    services_ram_swap_data_precision = 1
    services_ram_swap_data_unit = 0
    services_treeview_columns_shown = [0, 1, 2, 3, 4, 5, 6, 7]                                # services_treeview_columns_shown all values = [0, 1, 2, 3, 4, 5, 6, 7]
    services_data_row_sorting_column = 0
    services_data_row_sorting_order = 0
    services_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7]
    services_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Default Services Tab Row Sort Column Order Function -----------------------------------
def config_default_services_row_sort_column_order_func():
    global services_data_row_sorting_column, services_data_row_sorting_order, services_data_column_order, services_data_column_widths
    services_data_row_sorting_column = 0
    services_data_row_sorting_order = 0
    services_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7]
    services_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1]

# ----------------------------------- Config - Config Read Function (reads settings from configration file) -----------------------------------
def config_get_values_func():
    global reset_all_settings_with_new_release
    global update_interval, chart_data_history, default_main_tab, performance_tab_default_sub_tab
    global performance_summary_on_the_headerbar, remember_last_opened_tabs_on_application_start, chart_background_color_all_charts
    global remember_last_selected_hardware

    global show_floating_summary, floating_summary_window_transparency, floating_summary_data_shown

    global chart_line_color_cpu_percent, show_cpu_usage_per_core, performance_cpu_usage_percent_precision, selected_cpu_core

    global chart_line_color_ram_swap_percent, performance_ram_swap_data_precision, performance_ram_swap_data_unit

    global chart_line_color_disk_speed_usage, performance_disk_speed_data_precision, performance_disk_usage_data_precision
    global performance_disk_speed_data_unit, performance_disk_usage_data_unit, plot_disk_read_speed, plot_disk_write_speed, selected_disk

    global chart_line_color_network_speed_data, performance_network_speed_data_precision, performance_network_data_data_precision
    global performance_network_speed_data_unit, performance_network_data_data_unit, plot_network_download_speed, plot_network_upload_speed, selected_network_card

    global chart_line_color_fps, selected_gpu

    global sensors_treeview_columns_shown, sensors_data_row_sorting_column, sensors_data_row_sorting_order, sensors_data_column_order, sensors_data_column_widths

    global show_processes_of_all_users, show_processes_as_tree, show_tree_lines, processes_cpu_usage_percent_precision
    global processes_ram_swap_data_precision, processes_ram_swap_data_unit, processes_disk_speed_data_precision, processes_disk_usage_data_precision
    global processes_disk_speed_data_unit, processes_disk_usage_data_unit, warn_before_stopping_processes
    global processes_treeview_columns_shown, processes_data_row_sorting_column, processes_data_row_sorting_order, processes_data_column_order, processes_data_column_widths

    global users_cpu_usage_percent_precision, users_ram_swap_data_precision, users_ram_swap_data_unit
    global users_treeview_columns_shown, users_data_row_sorting_column, users_data_row_sorting_order, users_data_column_order, users_data_column_widths

    global startup_treeview_columns_shown, startup_data_row_sorting_column, startup_data_row_sorting_order, startup_data_column_order, startup_data_column_widths

    global services_ram_swap_data_precision, services_ram_swap_data_unit
    global services_treeview_columns_shown, services_data_row_sorting_column, services_data_row_sorting_order, services_data_column_order, services_data_column_widths

    global config_variables, config_values

    reset_all_settings_with_new_release = int(config_values[config_variables.index("reset_all_settings_with_new_release")])
    update_interval = float(config_values[config_variables.index("update_interval")])
    chart_data_history = int(config_values[config_variables.index("chart_data_history")])
    default_main_tab = int(config_values[config_variables.index("default_main_tab")])
    performance_tab_default_sub_tab = int(config_values[config_variables.index("performance_tab_default_sub_tab")])
    performance_summary_on_the_headerbar = int(config_values[config_variables.index("performance_summary_on_the_headerbar")])
    remember_last_opened_tabs_on_application_start = int(config_values[config_variables.index("remember_last_opened_tabs_on_application_start")])
    chart_background_color_all_charts = [float(value) for value in config_values[config_variables.index("chart_background_color_all_charts")].strip("[]").split(", ")]
    remember_last_selected_hardware = int(config_values[config_variables.index("remember_last_selected_hardware")])

    show_floating_summary = int(config_values[config_variables.index("show_floating_summary")])
    floating_summary_window_transparency = float(config_values[config_variables.index("floating_summary_window_transparency")])
    floating_summary_data_shown = [int(value) for value in config_values[config_variables.index("floating_summary_data_shown")].strip("[]").split(", ")]

    chart_line_color_cpu_percent = [float(value) for value in config_values[config_variables.index("chart_line_color_cpu_percent")].strip("[]").split(", ")]
    show_cpu_usage_per_core = int(config_values[config_variables.index("show_cpu_usage_per_core")])
    performance_cpu_usage_percent_precision = int(config_values[config_variables.index("performance_cpu_usage_percent_precision")])
    selected_cpu_core = config_values[config_variables.index("selected_cpu_core")]

    chart_line_color_ram_swap_percent = [float(value) for value in config_values[config_variables.index("chart_line_color_ram_swap_percent")].strip("[]").split(", ")]
    performance_ram_swap_data_precision = int(config_values[config_variables.index("performance_ram_swap_data_precision")])
    performance_ram_swap_data_unit = int(config_values[config_variables.index("performance_ram_swap_data_unit")])

    chart_line_color_disk_speed_usage = [float(value) for value in config_values[config_variables.index("chart_line_color_disk_speed_usage")].strip("[]").split(", ")]
    performance_disk_speed_data_precision = int(config_values[config_variables.index("performance_disk_speed_data_precision")])
    performance_disk_usage_data_precision = int(config_values[config_variables.index("performance_disk_usage_data_precision")])
    performance_disk_speed_data_unit = int(config_values[config_variables.index("performance_disk_speed_data_unit")])
    performance_disk_usage_data_unit = int(config_values[config_variables.index("performance_disk_usage_data_unit")])
    plot_disk_read_speed = int(config_values[config_variables.index("plot_disk_read_speed")])
    plot_disk_write_speed = int(config_values[config_variables.index("plot_disk_write_speed")])
    selected_disk = config_values[config_variables.index("selected_disk")]

    chart_line_color_network_speed_data = [float(value) for value in config_values[config_variables.index("chart_line_color_network_speed_data")].strip("[]").split(", ")]
    performance_network_speed_data_precision = int(config_values[config_variables.index("performance_network_speed_data_precision")])
    performance_network_data_data_precision = int(config_values[config_variables.index("performance_network_data_data_precision")])
    performance_network_speed_data_unit = int(config_values[config_variables.index("performance_network_speed_data_unit")])
    performance_network_data_data_unit = int(config_values[config_variables.index("performance_network_data_data_unit")])
    plot_network_download_speed = int(config_values[config_variables.index("plot_network_download_speed")])
    plot_network_upload_speed = int(config_values[config_variables.index("plot_network_upload_speed")])
    selected_network_card = config_values[config_variables.index("selected_network_card")]

    chart_line_color_fps = [float(value) for value in config_values[config_variables.index("chart_line_color_fps")].strip("[]").split(", ")]
    selected_gpu = config_values[config_variables.index("selected_gpu")]

    sensors_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("sensors_treeview_columns_shown")].strip("[]").split(", ")]
    sensors_data_row_sorting_column = int(config_values[config_variables.index("sensors_data_row_sorting_column")])
    sensors_data_row_sorting_order = int(config_values[config_variables.index("sensors_data_row_sorting_order")])
    sensors_data_column_order = [int(value) for value in config_values[config_variables.index("sensors_data_column_order")].strip("[]").split(", ")]
    sensors_data_column_widths = [int(value) for value in config_values[config_variables.index("sensors_data_column_widths")].strip("[]").split(", ")]

    show_processes_of_all_users = int(config_values[config_variables.index("show_processes_of_all_users")])
    show_processes_as_tree = int(config_values[config_variables.index("show_processes_as_tree")])
    show_tree_lines = int(config_values[config_variables.index("show_tree_lines")])
    processes_cpu_usage_percent_precision = int(config_values[config_variables.index("processes_cpu_usage_percent_precision")])
    processes_ram_swap_data_precision = int(config_values[config_variables.index("processes_ram_swap_data_precision")])
    processes_ram_swap_data_unit = int(config_values[config_variables.index("processes_ram_swap_data_unit")])
    processes_disk_speed_data_precision = int(config_values[config_variables.index("processes_disk_speed_data_precision")])
    processes_disk_usage_data_precision = int(config_values[config_variables.index("processes_disk_usage_data_precision")])
    processes_disk_speed_data_unit = int(config_values[config_variables.index("processes_disk_speed_data_unit")])
    processes_disk_usage_data_unit = int(config_values[config_variables.index("processes_disk_usage_data_unit")])
    warn_before_stopping_processes = int(config_values[config_variables.index("warn_before_stopping_processes")])
    processes_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("processes_treeview_columns_shown")].strip("[]").split(", ")]
    processes_data_row_sorting_column = int(config_values[config_variables.index("processes_data_row_sorting_column")])
    processes_data_row_sorting_order = int(config_values[config_variables.index("processes_data_row_sorting_order")])
    processes_data_column_order = [int(value) for value in config_values[config_variables.index("processes_data_column_order")].strip("[]").split(", ")]
    processes_data_column_widths = [int(value) for value in config_values[config_variables.index("processes_data_column_widths")].strip("[]").split(", ")]

    users_cpu_usage_percent_precision = int(config_values[config_variables.index("users_cpu_usage_percent_precision")])
    users_ram_swap_data_precision = int(config_values[config_variables.index("users_ram_swap_data_precision")])
    users_ram_swap_data_unit = int(config_values[config_variables.index("users_ram_swap_data_unit")])
    users_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("users_treeview_columns_shown")].strip("[]").split(", ")]
    users_data_row_sorting_column = int(config_values[config_variables.index("users_data_row_sorting_column")])
    users_data_row_sorting_order = int(config_values[config_variables.index("users_data_row_sorting_order")])
    users_data_column_order = [int(value) for value in config_values[config_variables.index("users_data_column_order")].strip("[]").split(", ")]
    users_data_column_widths = [int(value) for value in config_values[config_variables.index("users_data_column_widths")].strip("[]").split(", ")]

    startup_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("startup_treeview_columns_shown")].strip("[]").split(", ")]
    startup_data_row_sorting_column = int(config_values[config_variables.index("startup_data_row_sorting_column")])
    startup_data_row_sorting_order = int(config_values[config_variables.index("startup_data_row_sorting_order")])
    startup_data_column_order = [int(value) for value in config_values[config_variables.index("startup_data_column_order")].strip("[]").split(", ")]
    startup_data_column_widths = [int(value) for value in config_values[config_variables.index("startup_data_column_widths")].strip("[]").split(", ")]

    services_ram_swap_data_precision = int(config_values[config_variables.index("services_ram_swap_data_precision")])
    services_ram_swap_data_unit = int(config_values[config_variables.index("services_ram_swap_data_unit")])
    services_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("services_treeview_columns_shown")].strip("[]").split(", ")]
    services_data_row_sorting_column = int(config_values[config_variables.index("services_data_row_sorting_column")])
    services_data_row_sorting_order = int(config_values[config_variables.index("services_data_row_sorting_order")])
    services_data_column_order = [int(value) for value in config_values[config_variables.index("services_data_column_order")].strip("[]").split(", ")]
    services_data_column_widths = [int(value) for value in config_values[config_variables.index("services_data_column_widths")].strip("[]").split(", ")]

# Adding a new setting
#     global new_setting
#     if "new_setting" in config_variables:
#         new_setting = int(config_values[config_variables.index("new_setting")])
#     else:
#         pass


# ----------------------------------- Config - Config Save Function (writes settings into configration file) -----------------------------------
def config_save_func():

    config_write_text = ""
    config_write_text = config_write_text + "[General - General]" + "\n"
    config_write_text = config_write_text + "reset_all_settings_with_new_release = " + str(reset_all_settings_with_new_release) + "\n"
    config_write_text = config_write_text + "update_interval = " + str(update_interval) + "\n"
    config_write_text = config_write_text + "chart_data_history = " + str(chart_data_history) + "\n"
    config_write_text = config_write_text + "default_main_tab = " + str(default_main_tab) + "\n"
    config_write_text = config_write_text + "performance_tab_default_sub_tab = " + str(performance_tab_default_sub_tab) + "\n"
    config_write_text = config_write_text + "performance_summary_on_the_headerbar = " + str(performance_summary_on_the_headerbar) + "\n"
    config_write_text = config_write_text + "remember_last_opened_tabs_on_application_start = " + str(remember_last_opened_tabs_on_application_start) + "\n"
    config_write_text = config_write_text + "chart_background_color_all_charts = " + str(chart_background_color_all_charts) + "\n"
    config_write_text = config_write_text + "remember_last_selected_hardware = " + str(remember_last_selected_hardware) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[General - Floating Summary]" + "\n"
    config_write_text = config_write_text + "show_floating_summary = " + str(show_floating_summary) + "\n"
    config_write_text = config_write_text + "floating_summary_window_transparency = " + str(floating_summary_window_transparency) + "\n"
    config_write_text = config_write_text + "floating_summary_data_shown = " + str(floating_summary_data_shown) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Performance Tab - CPU]" + "\n"
    config_write_text = config_write_text + "chart_line_color_cpu_percent = " + str(chart_line_color_cpu_percent) + "\n"
    config_write_text = config_write_text + "show_cpu_usage_per_core = " + str(show_cpu_usage_per_core) + "\n"
    config_write_text = config_write_text + "performance_cpu_usage_percent_precision = " + str(performance_cpu_usage_percent_precision) + "\n"
    config_write_text = config_write_text + "selected_cpu_core = " + str(selected_cpu_core) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Performance Tab - RAM]" + "\n"
    config_write_text = config_write_text + "chart_line_color_ram_swap_percent = " + str(chart_line_color_ram_swap_percent) + "\n"
    config_write_text = config_write_text + "performance_ram_swap_data_precision = " + str(performance_ram_swap_data_precision) + "\n"
    config_write_text = config_write_text + "performance_ram_swap_data_unit = " + str(performance_ram_swap_data_unit) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Performance Tab - Disk]" + "\n"
    config_write_text = config_write_text + "chart_line_color_disk_speed_usage = " + str(chart_line_color_disk_speed_usage) + "\n"
    config_write_text = config_write_text + "performance_disk_speed_data_precision = " + str(performance_disk_speed_data_precision) + "\n"
    config_write_text = config_write_text + "performance_disk_usage_data_precision = " + str(performance_disk_usage_data_precision) + "\n"
    config_write_text = config_write_text + "performance_disk_speed_data_unit = " + str(performance_disk_speed_data_unit) + "\n"
    config_write_text = config_write_text + "performance_disk_usage_data_unit = " + str(performance_disk_usage_data_unit) + "\n"
    config_write_text = config_write_text + "plot_disk_read_speed = " + str(plot_disk_read_speed) + "\n"
    config_write_text = config_write_text + "plot_disk_write_speed = " + str(plot_disk_write_speed) + "\n"
    config_write_text = config_write_text + "selected_disk = " + str(selected_disk) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Performance Tab - Network]" + "\n"
    config_write_text = config_write_text + "chart_line_color_network_speed_data = " + str(chart_line_color_network_speed_data) + "\n"
    config_write_text = config_write_text + "performance_network_speed_data_precision = " + str(performance_network_speed_data_precision) + "\n"
    config_write_text = config_write_text + "performance_network_data_data_precision = " + str(performance_network_data_data_precision) + "\n"
    config_write_text = config_write_text + "performance_network_speed_data_unit = " + str(performance_network_speed_data_unit) + "\n"
    config_write_text = config_write_text + "performance_network_data_data_unit = " + str(performance_network_data_data_unit) + "\n"
    config_write_text = config_write_text + "plot_network_download_speed = " + str(plot_network_download_speed) + "\n"
    config_write_text = config_write_text + "plot_network_upload_speed = " + str(plot_network_upload_speed) + "\n"
    config_write_text = config_write_text + "selected_network_card = " + str(selected_network_card) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Performance Tab - GPU]" + "\n"
    config_write_text = config_write_text + "chart_line_color_fps = " + str(chart_line_color_fps) + "\n"
    config_write_text = config_write_text + "selected_gpu = " + str(selected_gpu) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Performance Tab - Sensors]" + "\n"
    config_write_text = config_write_text + "sensors_treeview_columns_shown = " + str(sensors_treeview_columns_shown) + "\n"
    config_write_text = config_write_text + "sensors_data_row_sorting_column = " + str(sensors_data_row_sorting_column) + "\n"
    config_write_text = config_write_text + "sensors_data_row_sorting_order = " + str(sensors_data_row_sorting_order) + "\n"
    config_write_text = config_write_text + "sensors_data_column_order = " + str(sensors_data_column_order) + "\n"
    config_write_text = config_write_text + "sensors_data_column_widths = " + str(sensors_data_column_widths) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Processes Tab]" + "\n"
    config_write_text = config_write_text + "show_processes_of_all_users = " + str(show_processes_of_all_users) + "\n"
    config_write_text = config_write_text + "show_processes_as_tree = " + str(show_processes_as_tree) + "\n"
    config_write_text = config_write_text + "show_tree_lines = " + str(show_tree_lines) + "\n"
    config_write_text = config_write_text + "processes_cpu_usage_percent_precision = " + str(processes_cpu_usage_percent_precision) + "\n"
    config_write_text = config_write_text + "processes_ram_swap_data_precision = " + str(processes_ram_swap_data_precision) + "\n"
    config_write_text = config_write_text + "processes_ram_swap_data_unit = " + str(processes_ram_swap_data_unit) + "\n"
    config_write_text = config_write_text + "processes_disk_speed_data_precision = " + str(processes_disk_speed_data_precision) + "\n"
    config_write_text = config_write_text + "processes_disk_usage_data_precision = " + str(processes_disk_usage_data_precision) + "\n"
    config_write_text = config_write_text + "processes_disk_speed_data_unit = " + str(processes_disk_speed_data_unit) + "\n"
    config_write_text = config_write_text + "processes_disk_usage_data_unit = " + str(processes_disk_usage_data_unit) + "\n"
    config_write_text = config_write_text + "warn_before_stopping_processes = " + str(warn_before_stopping_processes) + "\n"
    config_write_text = config_write_text + "processes_treeview_columns_shown = " + str(processes_treeview_columns_shown) + "\n"
    config_write_text = config_write_text + "processes_data_row_sorting_column = " + str(processes_data_row_sorting_column) + "\n"
    config_write_text = config_write_text + "processes_data_row_sorting_order = " + str(processes_data_row_sorting_order) + "\n"
    config_write_text = config_write_text + "processes_data_column_order = " + str(processes_data_column_order) + "\n"
    config_write_text = config_write_text + "processes_data_column_widths = " + str(processes_data_column_widths) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Users Tab]" + "\n"
    config_write_text = config_write_text + "users_cpu_usage_percent_precision = " + str(users_cpu_usage_percent_precision) + "\n"
    config_write_text = config_write_text + "users_ram_swap_data_precision = " + str(users_ram_swap_data_precision) + "\n"
    config_write_text = config_write_text + "users_ram_swap_data_unit = " + str(users_ram_swap_data_unit) + "\n"
    config_write_text = config_write_text + "users_treeview_columns_shown = " + str(users_treeview_columns_shown) + "\n"
    config_write_text = config_write_text + "users_data_row_sorting_column = " + str(users_data_row_sorting_column) + "\n"
    config_write_text = config_write_text + "users_data_row_sorting_order = " + str(users_data_row_sorting_order) + "\n"
    config_write_text = config_write_text + "users_data_column_order = " + str(users_data_column_order) + "\n"
    config_write_text = config_write_text + "users_data_column_widths = " + str(users_data_column_widths) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Startup Tab]" + "\n"
    config_write_text = config_write_text + "startup_treeview_columns_shown = " + str(startup_treeview_columns_shown) + "\n"
    config_write_text = config_write_text + "startup_data_row_sorting_column = " + str(startup_data_row_sorting_column) + "\n"
    config_write_text = config_write_text + "startup_data_row_sorting_order = " + str(startup_data_row_sorting_order) + "\n"
    config_write_text = config_write_text + "startup_data_column_order = " + str(startup_data_column_order) + "\n"
    config_write_text = config_write_text + "startup_data_column_widths = " + str(startup_data_column_widths) + "\n"
    config_write_text = config_write_text + "\n"

    config_write_text = config_write_text + "[Services Tab]" + "\n"
    config_write_text = config_write_text + "services_ram_swap_data_precision = " + str(services_ram_swap_data_precision) + "\n"
    config_write_text = config_write_text + "services_ram_swap_data_unit = " + str(services_ram_swap_data_unit) + "\n"
    config_write_text = config_write_text + "services_treeview_columns_shown = " + str(services_treeview_columns_shown) + "\n"
    config_write_text = config_write_text + "services_data_row_sorting_column = " + str(services_data_row_sorting_column) + "\n"
    config_write_text = config_write_text + "services_data_row_sorting_order = " + str(services_data_row_sorting_order) + "\n"
    config_write_text = config_write_text + "services_data_column_order = " + str(services_data_column_order) + "\n"
    config_write_text = config_write_text + "services_data_column_widths = " + str(services_data_column_widths) + "\n"
    config_write_text = config_write_text + "\n"

# Adding a new setting
#     config_write_text = config_write_text + "new_setting = " + str("1") + "\n"

    with open(config_file_path, "w") as writer:
        writer.write(config_write_text)
