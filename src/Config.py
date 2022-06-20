#!/usr/bin/env python3

# Import modules
import os


# Define class
class Config:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Define configration file and directory
        self.current_user_homedir = os.environ.get('HOME')
        self.config_folder_path = self.current_user_homedir + "/.config/system-monitoring-center/"
        self.config_file_path = self.config_folder_path + "config.txt"

        # Define read-only values
        # number_precision_list data info: [[ordering number, used in the code to get data, data unit, precision number], ...]
        self.number_precision_list = [[0, '0', 0], [1, '0.0', 1], [2, '0,00', 2], [3, '0,000', 3]]

        # Read settings
        self.config_read_func()


    # ----------------------- Called for reading settings (when the application is started) from the configration file -----------------------
    def config_read_func(self):

        # Define variables to read config data
        # This value is used for resetting all settings. There is no relationship between this value and application version.
        # This integer value is increased "1" in the new application release if resetting is wanted by the developer.
        # Code reads this value from the config file and compares with the value in the code.
        # All settings are reset if integer value of this value is bigger than the value in the config file.
        # There is no action if integer value of this value is smaller than the value in the config file.
        self.reset_all_settings_with_new_release_value = 4
        self.config_variables = []
        self.config_values = []

        # Read the config file
        try:
            with open(self.config_file_path) as reader:
                config_lines = reader.read().split("\n")
        except Exception:
            # Generate config folder if it does not exist.
            if os.path.exists(self.config_folder_path) == False:
                os.makedirs(self.config_folder_path)
            # Read/reset default config data and save to file
            self.config_default_reset_all_func()
            self.config_save_func()
            return

        # Add config names and values into separate lists
        for line in config_lines:
            if " = " in line:
                line_split = line.split(" = ")
                self.config_variables.append(line_split[0])
                self.config_values.append(line_split[1])

        # Read/reset default config data before getting values from the lists which is read from file because some new settings may be added and they may not be present in the config file.
        # Default values are read and modified by the user defined values if they are available.
        self.config_default_reset_all_func()

        # Get config data from the lists which is read from file
        try:
            self.config_get_values_func()
        except Exception:
            pass

        # Reset user config data if relevant setting is changed by the developer
        if self.reset_all_settings_with_new_release < self.reset_all_settings_with_new_release_value:
            self.config_default_reset_all_func()
            self.config_save_func()


    # ----------------------- Called for default all settings -----------------------
    def config_default_reset_all_func(self):

        self.config_default_general_general_func()
        self.config_default_performance_cpu_func()
        self.config_default_performance_memory_func()
        self.config_default_performance_disk_func()
        self.config_default_performance_network_func()
        self.config_default_performance_gpu_func()
        self.config_default_performance_sensors_func()
        self.config_default_processes_func()
        self.config_default_users_func()
        self.config_default_services_func()


    # ----------------------- Called for default general settings -----------------------
    def config_default_general_general_func(self):

        self.reset_all_settings_with_new_release = self.reset_all_settings_with_new_release_value 
        self.update_interval = 0.75
        self.chart_data_history = 150
        self.default_main_tab = 0
        self.performance_tab_default_sub_tab = 0
        self.performance_summary_on_the_headerbar = 1
        self.remember_last_opened_tabs_on_application_start = 0
        self.remember_last_selected_hardware = 0
        self.remember_window_size = [0, 0, 0, 0]
        self.check_for_updates_automatically = 0


    # ----------------------- Called for default CPU Tab settings -----------------------
    def config_default_performance_cpu_func(self):
        
        self.chart_line_color_cpu_percent = [0.29, 0.78, 0.0, 1.0]
        self.show_cpu_usage_per_core = 0
        self.performance_cpu_usage_percent_precision = 0
        self.selected_cpu_core = ""


    # ----------------------- Called for default Memory Tab settings -----------------------
    def config_default_performance_memory_func(self):

        self.chart_line_color_memory_percent = [0.27, 0.49, 1.0, 1.0]
        self.show_memory_usage_per_memory = 0
        self.performance_memory_data_precision = 1
        self.performance_memory_data_unit = 0


    # ----------------------- Called for default Disk Tab settings -----------------------
    def config_default_performance_disk_func(self):

        self.chart_line_color_disk_speed_usage = [1.0, 0.44, 0.17, 1.0]
        self.show_disk_usage_per_disk = 0
        self.performance_disk_data_precision = 1
        self.performance_disk_data_unit = 0
        self.performance_disk_speed_bit = 0
        self.plot_disk_read_speed = 1
        self.plot_disk_write_speed = 1
        self.hide_loop_ramdisk_zram_disks = 1
        self.selected_disk = ""


    # ----------------------- Called for default Network Tab settings -----------------------
    def config_default_performance_network_func(self):

        self.chart_line_color_network_speed_data = [0.56, 0.30, 0.78, 1.0]
        self.show_network_usage_per_network_card = 0
        self.performance_network_data_precision = 1
        self.performance_network_data_unit = 0
        self.performance_network_speed_bit = 0
        self.plot_network_download_speed = 1
        self.plot_network_upload_speed = 1
        self.selected_network_card = ""

    # ----------------------- Called for default GPU Tab settings -----------------------
    def config_default_performance_gpu_func(self):

        self.chart_line_color_fps = [1.0, 0.09, 0.09, 1.0]
        self.selected_gpu = ""


    # ----------------------- Called for default Sensors Tab Row Sort Column Order Width settings -----------------------
    def config_default_performance_sensors_func(self):

        self.sensors_treeview_columns_shown = [0, 1, 2, 3, 4]
        self.sensors_data_row_sorting_column = 0
        self.sensors_data_row_sorting_order = 0
        self.sensors_data_column_order = [0, 1, 2, 3, 4]
        self.sensors_data_column_widths = [-1, -1, -1, -1, -1]


    # ----------------------- Called for default Processes Tab settings -----------------------
    def config_default_processes_func(self):

        self.show_processes_of_all_users = 1
        self.show_processes_as_tree = 0
        self.show_tree_lines = 0
        self.processes_cpu_precision = 0
        self.processes_memory_data_precision = 1
        self.processes_memory_data_unit = 0
        self.processes_disk_data_precision = 1
        self.processes_disk_data_unit = 0
        self.processes_disk_speed_bit = 0
        self.warn_before_stopping_processes = 1
        self.processes_treeview_columns_shown = [0, 1, 2, 4, 5, 10, 11]
        self.processes_data_row_sorting_column = 0
        self.processes_data_row_sorting_order = 0
        self.processes_data_column_order = [0, 1, 2, -1, 3, 4, -1, -1, -1, -1, 5, 6, -1, -1, -1, -1, -1, -1, -1]
        self.processes_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]


    # ----------------------- Called for default Users Tab settings -----------------------
    def config_default_users_func(self):

        self.users_cpu_precision = 0
        self.users_treeview_columns_shown = [0, 2, 3, 5, 6, 7, 10]
        self.users_data_row_sorting_column = 0
        self.users_data_row_sorting_order = 0
        self.users_data_column_order = [0, -1, 1, 2, -1, 3, 4, 5, -1, -1, 6]
        self.users_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]


    # ----------------------- Called for default Services Tab settings -----------------------
    def config_default_services_func(self):

        self.services_memory_data_precision = 1
        self.services_memory_data_unit = 0
        self.services_treeview_columns_shown = [0, 1, 2, 3, 4, 5, 6, 7]
        self.services_data_row_sorting_column = 0
        self.services_data_row_sorting_order = 0
        self.services_data_column_order = [0, 1, 2, 3, 4, 5, 6, 7]
        self.services_data_column_widths = [-1, -1, -1, -1, -1, -1, -1, -1]


    # ----------------------- Called for reading settings from the configration file -----------------------
    def config_get_values_func(self):

        config_variables = self.config_variables
        config_values = self.config_values

        self.reset_all_settings_with_new_release = int(config_values[config_variables.index("reset_all_settings_with_new_release")])
        self.update_interval = float(config_values[config_variables.index("update_interval")])
        self.chart_data_history = int(config_values[config_variables.index("chart_data_history")])
        self.default_main_tab = int(config_values[config_variables.index("default_main_tab")])
        self.performance_tab_default_sub_tab = int(config_values[config_variables.index("performance_tab_default_sub_tab")])
        self.performance_summary_on_the_headerbar = int(config_values[config_variables.index("performance_summary_on_the_headerbar")])
        self.remember_last_opened_tabs_on_application_start = int(config_values[config_variables.index("remember_last_opened_tabs_on_application_start")])
        self.remember_last_selected_hardware = int(config_values[config_variables.index("remember_last_selected_hardware")])
        self.remember_window_size = [int(value) for value in config_values[config_variables.index("remember_window_size")].strip("[]").split(", ")]
        self.check_for_updates_automatically = int(config_values[config_variables.index("check_for_updates_automatically")])

        self.chart_line_color_cpu_percent = [float(value) for value in config_values[config_variables.index("chart_line_color_cpu_percent")].strip("[]").split(", ")]
        self.show_cpu_usage_per_core = int(config_values[config_variables.index("show_cpu_usage_per_core")])
        self.performance_cpu_usage_percent_precision = int(config_values[config_variables.index("performance_cpu_usage_percent_precision")])
        self.selected_cpu_core = config_values[config_variables.index("selected_cpu_core")]

        self.chart_line_color_memory_percent = [float(value) for value in config_values[config_variables.index("chart_line_color_memory_percent")].strip("[]").split(", ")]
        self.show_memory_usage_per_memory = int(config_values[config_variables.index("show_memory_usage_per_memory")])
        self.performance_memory_data_precision = int(config_values[config_variables.index("performance_memory_data_precision")])
        self.performance_memory_data_unit = int(config_values[config_variables.index("performance_memory_data_unit")])

        self.chart_line_color_disk_speed_usage = [float(value) for value in config_values[config_variables.index("chart_line_color_disk_speed_usage")].strip("[]").split(", ")]
        self.show_disk_usage_per_disk = int(config_values[config_variables.index("show_disk_usage_per_disk")])
        self.performance_disk_data_precision = int(config_values[config_variables.index("performance_disk_data_precision")])
        self.performance_disk_data_unit = int(config_values[config_variables.index("performance_disk_data_unit")])
        self.performance_disk_speed_bit = int(config_values[config_variables.index("performance_disk_speed_bit")])
        self.plot_disk_read_speed = int(config_values[config_variables.index("plot_disk_read_speed")])
        self.plot_disk_write_speed = int(config_values[config_variables.index("plot_disk_write_speed")])
        self.selected_disk = config_values[config_variables.index("selected_disk")]
        if "hide_loop_ramdisk_zram_disks" in config_variables:
            self.hide_loop_ramdisk_zram_disks = int(config_values[config_variables.index("hide_loop_ramdisk_zram_disks")])
        else:
            pass

        self.chart_line_color_network_speed_data = [float(value) for value in config_values[config_variables.index("chart_line_color_network_speed_data")].strip("[]").split(", ")]
        self.show_network_usage_per_network_card = int(config_values[config_variables.index("show_network_usage_per_network_card")])
        self.performance_network_data_precision = int(config_values[config_variables.index("performance_network_data_precision")])
        self.performance_network_data_unit = int(config_values[config_variables.index("performance_network_data_unit")])
        self.performance_network_speed_bit = int(config_values[config_variables.index("performance_network_speed_bit")])
        self.plot_network_download_speed = int(config_values[config_variables.index("plot_network_download_speed")])
        self.plot_network_upload_speed = int(config_values[config_variables.index("plot_network_upload_speed")])
        self.selected_network_card = config_values[config_variables.index("selected_network_card")]

        self.chart_line_color_fps = [float(value) for value in config_values[config_variables.index("chart_line_color_fps")].strip("[]").split(", ")]
        self.selected_gpu = config_values[config_variables.index("selected_gpu")]

        self.show_processes_of_all_users = int(config_values[config_variables.index("show_processes_of_all_users")])
        self.show_processes_as_tree = int(config_values[config_variables.index("show_processes_as_tree")])
        self.show_tree_lines = int(config_values[config_variables.index("show_tree_lines")])
        self.processes_cpu_precision = int(config_values[config_variables.index("processes_cpu_precision")])
        self.processes_memory_data_precision = int(config_values[config_variables.index("processes_memory_data_precision")])
        self.processes_memory_data_unit = int(config_values[config_variables.index("processes_memory_data_unit")])
        self.processes_disk_data_precision = int(config_values[config_variables.index("processes_disk_data_precision")])
        self.processes_disk_data_unit = int(config_values[config_variables.index("processes_disk_data_unit")])
        self.processes_disk_speed_bit = int(config_values[config_variables.index("processes_disk_speed_bit")])
        self.warn_before_stopping_processes = int(config_values[config_variables.index("warn_before_stopping_processes")])
        self.processes_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("processes_treeview_columns_shown")].strip("[]").split(", ")]
        self.processes_data_row_sorting_column = int(config_values[config_variables.index("processes_data_row_sorting_column")])
        self.processes_data_row_sorting_order = int(config_values[config_variables.index("processes_data_row_sorting_order")])
        self.processes_data_column_order = [int(value) for value in config_values[config_variables.index("processes_data_column_order")].strip("[]").split(", ")]
        self.processes_data_column_widths = [int(value) for value in config_values[config_variables.index("processes_data_column_widths")].strip("[]").split(", ")]

        self.users_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("users_treeview_columns_shown")].strip("[]").split(", ")]
        self.users_data_row_sorting_column = int(config_values[config_variables.index("users_data_row_sorting_column")])
        self.users_data_row_sorting_order = int(config_values[config_variables.index("users_data_row_sorting_order")])
        self.users_data_column_order = [int(value) for value in config_values[config_variables.index("users_data_column_order")].strip("[]").split(", ")]
        self.users_data_column_widths = [int(value) for value in config_values[config_variables.index("users_data_column_widths")].strip("[]").split(", ")]

        self.services_treeview_columns_shown = [int(value) for value in config_values[config_variables.index("services_treeview_columns_shown")].strip("[]").split(", ")]
        self.services_data_row_sorting_column = int(config_values[config_variables.index("services_data_row_sorting_column")])
        self.services_data_row_sorting_order = int(config_values[config_variables.index("services_data_row_sorting_order")])
        self.services_data_column_order = [int(value) for value in config_values[config_variables.index("services_data_column_order")].strip("[]").split(", ")]
        self.services_data_column_widths = [int(value) for value in config_values[config_variables.index("services_data_column_widths")].strip("[]").split(", ")]

        # Adding a new setting
        #     if "new_setting" in config_variables:
        #         self.new_setting = int(config_values[config_variables.index("new_setting")])
        #     else:
        #         pass


    # ----------------------- Called for writing settings into the configration file -----------------------
    def config_save_func(self):

        config_write_text = ""
        config_write_text = config_write_text + "[General - General]" + "\n"
        config_write_text = config_write_text + "reset_all_settings_with_new_release = " + str(self.reset_all_settings_with_new_release) + "\n"
        config_write_text = config_write_text + "update_interval = " + str(self.update_interval) + "\n"
        config_write_text = config_write_text + "chart_data_history = " + str(self.chart_data_history) + "\n"
        config_write_text = config_write_text + "default_main_tab = " + str(self.default_main_tab) + "\n"
        config_write_text = config_write_text + "performance_tab_default_sub_tab = " + str(self.performance_tab_default_sub_tab) + "\n"
        config_write_text = config_write_text + "performance_summary_on_the_headerbar = " + str(self.performance_summary_on_the_headerbar) + "\n"
        config_write_text = config_write_text + "remember_last_opened_tabs_on_application_start = " + str(self.remember_last_opened_tabs_on_application_start) + "\n"
        config_write_text = config_write_text + "remember_last_selected_hardware = " + str(self.remember_last_selected_hardware) + "\n"
        config_write_text = config_write_text + "remember_window_size = " + str(self.remember_window_size) + "\n"
        config_write_text = config_write_text + "check_for_updates_automatically = " + str(self.check_for_updates_automatically) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Performance Tab - CPU]" + "\n"
        config_write_text = config_write_text + "chart_line_color_cpu_percent = " + str(self.chart_line_color_cpu_percent) + "\n"
        config_write_text = config_write_text + "show_cpu_usage_per_core = " + str(self.show_cpu_usage_per_core) + "\n"
        config_write_text = config_write_text + "performance_cpu_usage_percent_precision = " + str(self.performance_cpu_usage_percent_precision) + "\n"
        config_write_text = config_write_text + "selected_cpu_core = " + str(self.selected_cpu_core) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Performance Tab - Memory]" + "\n"
        config_write_text = config_write_text + "chart_line_color_memory_percent = " + str(self.chart_line_color_memory_percent) + "\n"
        config_write_text = config_write_text + "show_memory_usage_per_memory = " + str(self.show_memory_usage_per_memory) + "\n"
        config_write_text = config_write_text + "performance_memory_data_precision = " + str(self.performance_memory_data_precision) + "\n"
        config_write_text = config_write_text + "performance_memory_data_unit = " + str(self.performance_memory_data_unit) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Performance Tab - Disk]" + "\n"
        config_write_text = config_write_text + "chart_line_color_disk_speed_usage = " + str(self.chart_line_color_disk_speed_usage) + "\n"
        config_write_text = config_write_text + "show_disk_usage_per_disk = " + str(self.show_disk_usage_per_disk) + "\n"
        config_write_text = config_write_text + "performance_disk_data_precision = " + str(self.performance_disk_data_precision) + "\n"
        config_write_text = config_write_text + "performance_disk_data_unit = " + str(self.performance_disk_data_unit) + "\n"
        config_write_text = config_write_text + "performance_disk_speed_bit = " + str(self.performance_disk_speed_bit) + "\n"
        config_write_text = config_write_text + "plot_disk_read_speed = " + str(self.plot_disk_read_speed) + "\n"
        config_write_text = config_write_text + "plot_disk_write_speed = " + str(self.plot_disk_write_speed) + "\n"
        config_write_text = config_write_text + "selected_disk = " + str(self.selected_disk) + "\n"
        config_write_text = config_write_text + "hide_loop_ramdisk_zram_disks = " + str(self.hide_loop_ramdisk_zram_disks) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Performance Tab - Network]" + "\n"
        config_write_text = config_write_text + "chart_line_color_network_speed_data = " + str(self.chart_line_color_network_speed_data) + "\n"
        config_write_text = config_write_text + "show_network_usage_per_network_card = " + str(self.show_network_usage_per_network_card) + "\n"
        config_write_text = config_write_text + "performance_network_data_precision = " + str(self.performance_network_data_precision) + "\n"
        config_write_text = config_write_text + "performance_network_data_unit = " + str(self.performance_network_data_unit) + "\n"
        config_write_text = config_write_text + "performance_network_speed_bit = " + str(self.performance_network_speed_bit) + "\n"
        config_write_text = config_write_text + "plot_network_download_speed = " + str(self.plot_network_download_speed) + "\n"
        config_write_text = config_write_text + "plot_network_upload_speed = " + str(self.plot_network_upload_speed) + "\n"
        config_write_text = config_write_text + "selected_network_card = " + str(self.selected_network_card) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Performance Tab - GPU]" + "\n"
        config_write_text = config_write_text + "chart_line_color_fps = " + str(self.chart_line_color_fps) + "\n"
        config_write_text = config_write_text + "selected_gpu = " + str(self.selected_gpu) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Processes Tab]" + "\n"
        config_write_text = config_write_text + "show_processes_of_all_users = " + str(self.show_processes_of_all_users) + "\n"
        config_write_text = config_write_text + "show_processes_as_tree = " + str(self.show_processes_as_tree) + "\n"
        config_write_text = config_write_text + "show_tree_lines = " + str(self.show_tree_lines) + "\n"
        config_write_text = config_write_text + "processes_cpu_precision = " + str(self.processes_cpu_precision) + "\n"
        config_write_text = config_write_text + "processes_memory_data_precision = " + str(self.processes_memory_data_precision) + "\n"
        config_write_text = config_write_text + "processes_memory_data_unit = " + str(self.processes_memory_data_unit) + "\n"
        config_write_text = config_write_text + "processes_disk_data_precision = " + str(self.processes_disk_data_precision) + "\n"
        config_write_text = config_write_text + "processes_disk_data_unit = " + str(self.processes_disk_data_unit) + "\n"
        config_write_text = config_write_text + "processes_disk_speed_bit = " + str(self.processes_disk_speed_bit) + "\n"
        config_write_text = config_write_text + "warn_before_stopping_processes = " + str(self.warn_before_stopping_processes) + "\n"
        config_write_text = config_write_text + "processes_treeview_columns_shown = " + str(self.processes_treeview_columns_shown) + "\n"
        config_write_text = config_write_text + "processes_data_row_sorting_column = " + str(self.processes_data_row_sorting_column) + "\n"
        config_write_text = config_write_text + "processes_data_row_sorting_order = " + str(self.processes_data_row_sorting_order) + "\n"
        config_write_text = config_write_text + "processes_data_column_order = " + str(self.processes_data_column_order) + "\n"
        config_write_text = config_write_text + "processes_data_column_widths = " + str(self.processes_data_column_widths) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Users Tab]" + "\n"
        config_write_text = config_write_text + "users_treeview_columns_shown = " + str(self.users_treeview_columns_shown) + "\n"
        config_write_text = config_write_text + "users_data_row_sorting_column = " + str(self.users_data_row_sorting_column) + "\n"
        config_write_text = config_write_text + "users_data_row_sorting_order = " + str(self.users_data_row_sorting_order) + "\n"
        config_write_text = config_write_text + "users_data_column_order = " + str(self.users_data_column_order) + "\n"
        config_write_text = config_write_text + "users_data_column_widths = " + str(self.users_data_column_widths) + "\n"
        config_write_text = config_write_text + "\n"

        config_write_text = config_write_text + "[Services Tab]" + "\n"
        config_write_text = config_write_text + "services_treeview_columns_shown = " + str(self.services_treeview_columns_shown) + "\n"
        config_write_text = config_write_text + "services_data_row_sorting_column = " + str(self.services_data_row_sorting_column) + "\n"
        config_write_text = config_write_text + "services_data_row_sorting_order = " + str(self.services_data_row_sorting_order) + "\n"
        config_write_text = config_write_text + "services_data_column_order = " + str(self.services_data_column_order) + "\n"
        config_write_text = config_write_text + "services_data_column_widths = " + str(self.services_data_column_widths) + "\n"
        config_write_text = config_write_text + "\n"

        # Adding a new setting
        #     config_write_text = config_write_text + "new_setting = " + str(self.new_value) + "\n"

        with open(self.config_file_path, "w") as writer:
            writer.write(config_write_text)


# Generate object
Config = Config()

