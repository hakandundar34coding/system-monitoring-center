import os
import cairo
from math import sqrt, ceil

from .Config import Config
from . import Libsysmon

_tr = Config._tr


class Performance:

    def __init__(self):

        # Define data unit conversion variables
        self.unit_converter_variables()

        # Set chart performance data line and point highligting off.
        # "chart_line_highlight" takes chart name or "" for highlighting or not.
        # "chart_point_highlight" takes data point index or "-1" for not highlighting.
        self.chart_line_highlight = ""
        self.chart_point_highlight = -1


    def performance_set_selected_cpu_core_func(self):
        self.selected_cpu_core = Libsysmon.set_selected_cpu_core(Config.selected_cpu_core, self.logical_core_list)

    def performance_set_selected_disk_func(self):
        self.selected_disk, self.system_disk_list = Libsysmon.set_selected_disk(Config.selected_cpu_core, self.disk_list)

    def performance_set_selected_network_card_func(self):
        self.selected_network_card = Libsysmon.set_selected_network_card(Config.selected_cpu_core, self.network_card_list)


    def performance_background_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.system_performance_data_dict_prev = {}

        # Reset selected hardware if "remember_last_selected_hardware" prefrence is disabled by the user.
        if Config.remember_last_selected_hardware == 0:
            Config.selected_cpu_core = ""
            Config.selected_disk = ""
            Config.selected_network_card = ""
            Config.selected_gpu = ""


    def performance_background_loop_func(self):
        """
        Get basic CPU, memory, disk and network usage data in the background in order to assure uninterrupted data for charts.
        """

        self.chart_data_history = Config.chart_data_history

        system_performance_data_dict = Libsysmon.get_cpu_memory_disk_network_usages(self.chart_data_history, self.system_performance_data_dict_prev)
        self.system_performance_data_dict_prev = dict(system_performance_data_dict)

        self.logical_core_list = system_performance_data_dict["logical_core_list"]
        self.cpu_usage_percent_per_core = system_performance_data_dict["cpu_usage_percent_per_core"]
        self.cpu_usage_percent_ave = system_performance_data_dict["cpu_usage_percent_ave"]

        self.ram_usage_percent = system_performance_data_dict["ram_usage_percent"]
        self.swap_usage_percent = system_performance_data_dict["swap_usage_percent"]

        self.disk_list = system_performance_data_dict["disk_list"]
        self.disk_read_speed = system_performance_data_dict["disk_read_speed"]
        self.disk_write_speed = system_performance_data_dict["disk_write_speed"]

        self.network_card_list = system_performance_data_dict["network_card_list"]
        self.network_receive_speed = system_performance_data_dict["network_receive_speed"]
        self.network_send_speed = system_performance_data_dict["network_send_speed"]

        if system_performance_data_dict["logical_core_list_changed"] == "yes":
            self.performance_set_selected_cpu_core_func()
        if system_performance_data_dict["disk_list_changed"] == "yes":
            self.performance_set_selected_disk_func()
        if system_performance_data_dict["network_card_list_changed"] == "yes":
            self.performance_set_selected_network_card_func()


    def performance_line_charts_draw(self, widget, ctx, width, height, widget_name):
        """
        Draw performance data as line chart.
        """

        # Check if drawing will be for CPU tab.
        if widget_name == "da_cpu_usage":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Get performance data and device list for current device or all devices.
            if Config.show_cpu_usage_per_core == 0:
                performance_data1 = {"average": self.cpu_usage_percent_ave}
                device_name_list = list(performance_data1.keys())
                selected_device = ""
            else:
                performance_data1 = self.cpu_usage_percent_per_core
                device_name_list = list(self.logical_core_list)
                selected_device = self.selected_cpu_core

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit_dict[device_name] = 100

        # Check if drawing will be for Memory tab.
        elif widget_name == "da_memory_usage":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get performance data and device list for current device or all devices.
            if Config.show_memory_usage_per_memory == 0:
                performance_data1 = {_tr("RAM"): self.ram_usage_percent}
                device_name_list = list(performance_data1.keys())
                selected_device = ""
            else:
                performance_data1 = {_tr("RAM"): self.ram_usage_percent, _tr("Swap"): self.swap_usage_percent}
                device_name_list = list(performance_data1.keys())
                selected_device = ""

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit_dict[device_name] = 100

        # Check if drawing will be for Disk tab.
        elif widget_name == "da_disk_speed":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Get performance data and device list for current device or all devices.
            if Config.show_disk_usage_per_disk == 0:
                performance_data1 = {self.selected_disk: self.disk_read_speed[self.selected_disk]}
                performance_data2 = {self.selected_disk: self.disk_write_speed[self.selected_disk]}
                device_name_list = list(performance_data1.keys())
                selected_device = ""
            else:
                performance_data1 = self.disk_read_speed
                performance_data2 = self.disk_write_speed
                device_name_list = list(self.disk_list)
                selected_device = self.selected_disk

            # Remove the device from the list if "hide_loop_ramdisk_zram_disks" option is enabled.
            if Config.show_disk_usage_per_disk == 1 and Config.hide_loop_ramdisk_zram_disks == 1:
                for device in device_name_list[:]:
                    if device.startswith("loop") == True or device.startswith("ram") == True or device.startswith("zram") == True:
                        device_name_list.remove(device)

            # Get which performance data will be drawn.
            if Config.plot_disk_read_speed == 1:
                draw_performance_data1 = 1
            else:
                draw_performance_data1 = 0

            if Config.plot_disk_write_speed == 1:
                draw_performance_data2 = 1
            else:
                draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when
            # performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit = 1.1 * ((max(max(performance_data1[device_name]), max(performance_data2[device_name]))) + 0.0000001)
                if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                    chart_y_limit = 1.1 * (max(performance_data1[device_name]) + 0.0000001)
                if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                    chart_y_limit = 1.1 * (max(performance_data2[device_name]) + 0.0000001)
                chart_y_limit_dict[device_name] = chart_y_limit

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            from .Disk import Disk
            performance_disk_data_precision = Config.performance_disk_data_precision
            performance_disk_data_unit = Config.performance_disk_data_unit
            performance_disk_speed_bit = Config.performance_disk_speed_bit
            # Get biggest chart_y_limit value in the "chart_y_limit_dict" to show it on a label.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit = chart_y_limit_dict[selected_device]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(list(chart_y_limit_dict.values()))
            chart_y_limit_str = f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, chart_y_limit, performance_disk_data_unit, performance_disk_data_precision)}/s'
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account.
            # For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            Disk.da_upper_right_label.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update "chart_y_limit_dict" if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit_dict[selected_device] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update "chart_y_limit_dict" if single chart (device) is drawn.
            else:
                chart_y_limit_dict[list(chart_y_limit_dict.keys())[0]] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for Network tab.
        elif widget_name == "da_network_speed":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_network_speed_data

            # Get performance data and device list for current device or all devices.
            if Config.show_network_usage_per_network_card == 0:
                performance_data1 = {self.selected_network_card: self.network_receive_speed[self.selected_network_card]}
                performance_data2 = {self.selected_network_card: self.network_send_speed[self.selected_network_card]}
                device_name_list = list(performance_data1.keys())
                selected_device = ""
            else:
                performance_data1 = self.network_receive_speed
                performance_data2 = self.network_send_speed
                device_name_list = list(self.network_card_list)
                selected_device = self.selected_network_card

            # Get which performance data will be drawn.
            if Config.plot_network_download_speed == 1:
                draw_performance_data1 = 1
            else:
                draw_performance_data1 = 0

            if Config.plot_network_upload_speed == 1:
                draw_performance_data2 = 1
            else:
                draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when
            # performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit = 1.1 * ((max(max(performance_data1[device_name]), max(performance_data2[device_name]))) + 0.0000001)
                if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                    chart_y_limit = 1.1 * (max(performance_data1[device_name]) + 0.0000001)
                if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                    chart_y_limit = 1.1 * (max(performance_data2[device_name]) + 0.0000001)
                chart_y_limit_dict[device_name] = chart_y_limit

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            from .Network import Network
            performance_network_data_precision = Config.performance_network_data_precision
            performance_network_data_unit = Config.performance_network_data_unit
            performance_network_speed_bit = Config.performance_network_speed_bit
            # Get biggest chart_y_limit value in the "chart_y_limit_dict" to show it on a label.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit = chart_y_limit_dict[selected_device]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(list(chart_y_limit_dict.values()))
            chart_y_limit_str = f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, chart_y_limit, performance_network_data_unit, performance_network_data_precision)}/s'
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account.
            # For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            Network.da_upper_right_label.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_dict if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit_dict[selected_device] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update "chart_y_limit_dict" if single chart (device) is drawn.
            else:
                chart_y_limit_dict[list(chart_y_limit_dict.keys())[0]] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for GPU tab.
        elif widget_name == "da_gpu_usage":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_fps

            # Get performance data and device list for current device or all devices.
            from .Gpu import Gpu
            try:
                performance_data1 = {Gpu.selected_gpu: Gpu.gpu_load_list}
            # Handle errors because chart signals are connected before running relevant performance thread (in the GPU module)
            # to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            except AttributeError:
                return
            device_name_list = list(performance_data1.keys())
            selected_device = ""

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit_dict[device_name] = 100

        # Check if drawing will be for Process Details window CPU tab.
        elif widget_name == "processes_details_da_cpu_usage":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Get performance data and device list for current device or all devices.
            from . import ProcessesDetails
            # There may be more than one instance of object (per process). Search for the current one by checking the widget.
            for process_object in ProcessesDetails.processes_details_object_list:
                if process_object.processes_details_da_cpu_usage == widget:
                    current_process_object = process_object
            performance_data1 = {"process_cpu_usage": current_process_object.process_cpu_usage_list}
            device_name_list = list(performance_data1.keys())
            selected_device = ""

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Get chart y limit values in order to show maximum values of the charts as 100.
            if Config.processes_cpu_divide_by_core == 0:
                chart_y_limit_for_cpu_core = self.number_of_logical_cores * 100
            else:
                chart_y_limit_for_cpu_core = 100
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit_dict[device_name] = chart_y_limit_for_cpu_core

            # Get chart y limit value in order to show maximum value of the chart as 100% or CPU core count x 100%.
            if selected_device != "":
                chart_y_limit = chart_y_limit_dict[selected_device]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(list(chart_y_limit_dict.values()))
            chart_y_limit_str = f'{chart_y_limit_for_cpu_core}%'
            chart_y_limit_split = chart_y_limit_str
            current_process_object.drawingarea_cpu_limit_label.set_text(chart_y_limit_split)

        # Check if drawing will be for Process Details window Memory tab.
        elif widget_name == "processes_details_da_memory_usage":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get performance data and device list for current device or all devices.
            from . import ProcessesDetails
            # There may be more than one instance of object (per process). Search for the current one by checking the widget.
            for process_object in ProcessesDetails.processes_details_object_list:
                if process_object.processes_details_da_memory_usage == widget:
                    current_process_object = process_object
            performance_data1 = {"process_ram_usage": current_process_object.process_ram_usage_list}
            device_name_list = list(performance_data1.keys())
            selected_device = ""

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 0

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit = 1.1 * (max(performance_data1[device_name]) + 0.0000001)
                chart_y_limit_dict[device_name] = chart_y_limit

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            processes_memory_data_precision = Config.processes_memory_data_precision
            processes_memory_data_unit = Config.processes_memory_data_unit
            # Get biggest chart_y_limit value in the "chart_y_limit_dict" to show it on a label.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit = chart_y_limit_dict[selected_device]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(list(chart_y_limit_dict.values()))
            chart_y_limit_str = f'{self.performance_data_unit_converter_func("data", "none", chart_y_limit, processes_memory_data_unit, processes_memory_data_precision)}'
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account.
            # For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            current_process_object.drawingarea_memory_limit_label.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_dict if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit_dict[selected_device] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update "chart_y_limit_dict" if single chart (device) is drawn.
            else:
                chart_y_limit_dict[list(chart_y_limit_dict.keys())[0]] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)

        # Check if drawing will be for Process Details window Disk tab.
        elif widget_name == "processes_details_da_disk_speed":

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Get performance data and device list for current device or all devices.
            from . import ProcessesDetails
            # There may be more than one instance of object (per process). Search for the current one by checking the widget.
            for process_object in ProcessesDetails.processes_details_object_list:
                if process_object.processes_details_da_disk_speed == widget:
                    current_process_object = process_object
            performance_data1 = {"process_disk_speed": current_process_object.process_disk_read_speed_list}
            performance_data2 = {"process_disk_speed": current_process_object.process_disk_write_speed_list}
            device_name_list = list(performance_data1.keys())
            selected_device = ""

            # Get which performance data will be drawn.
            draw_performance_data1 = 1
            draw_performance_data2 = 1

            # Maximum performance data value is multiplied by 1.1 in order to scale chart when
            # performance data is increased or decreased for preventing the line being out of the chart border.
            chart_y_limit_dict = {}
            for device_name in device_name_list:
                chart_y_limit = 1.1 * ((max(max(performance_data1[device_name]), max(performance_data2[device_name]))) + 0.0000001)
                if draw_performance_data1 == 1 and draw_performance_data2 == 0:
                    chart_y_limit = 1.1 * (max(performance_data1[device_name]) + 0.0000001)
                if draw_performance_data1 == 0 and draw_performance_data2 == 1:
                    chart_y_limit = 1.1 * (max(performance_data2[device_name]) + 0.0000001)
                chart_y_limit_dict[device_name] = chart_y_limit

            # Get chart y limit value in order to show maximum value of the chart as multiples of 1, 10, 100.
            processes_disk_data_precision = Config.processes_disk_data_precision
            processes_disk_data_unit = Config.processes_disk_data_unit
            processes_disk_speed_bit = Config.processes_disk_speed_bit
            # Get biggest chart_y_limit value in the "chart_y_limit_dict" to show it on a label.
            # Get chart_y_limit value if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit = chart_y_limit_dict[selected_device]
            # Get chart_y_limit value if single chart (device) is drawn.
            else:
                chart_y_limit = max(list(chart_y_limit_dict.values()))
            chart_y_limit_str = f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, chart_y_limit, processes_disk_data_unit, processes_disk_data_precision)}/s'
            chart_y_limit_split = chart_y_limit_str.split(" ")
            chart_y_limit_float = float(chart_y_limit_split[0])
            number_of_digits = len(str(int(chart_y_limit_float)))
            multiple = 10 ** (number_of_digits - 1)
            # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
            number_to_get_next_multiple = chart_y_limit_float + (multiple - 0.0001)
            next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
            current_process_object.drawingarea_disk_limit_label.set_text(f'{next_multiple} {chart_y_limit_split[1]}')
            # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
            # Update chart_y_limit_dict if multiple charts (devices) are drawn.
            if selected_device != "":
                chart_y_limit_dict[selected_device] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)
            # Update "chart_y_limit_dict" if single chart (device) is drawn.
            else:
                chart_y_limit_dict[list(chart_y_limit_dict.keys())[0]] = (chart_y_limit * next_multiple / (chart_y_limit_float + 0.0000001) + 0.0000001)


        # Start drawing the performance data.
        # Get chart data history.
        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        # Get chart background color.
        chart_background_color = [0.0, 0.0, 0.0, 0.0]

        # Get drawingarea size.
        chart_width = width
        chart_height = height

        # Get number of charts.
        number_of_charts = len(device_name_list)

        # Get number of horizontal and vertical charts (per-device).
        for i in range(1, 1000):
            if number_of_charts % i == 0:
                number_of_horizontal_charts = i
                number_of_vertical_charts = number_of_charts // i
                if number_of_horizontal_charts >= number_of_vertical_charts:
                    if number_of_horizontal_charts > 2 * number_of_vertical_charts:
                        number_of_horizontal_charts = number_of_vertical_charts = ceil(sqrt(number_of_charts))
                    break

        # Get chart index list for horizontal and vertical charts. This data will be used for tiling charts.
        chart_index_dict = {}
        horizontal_counter = 0
        vertical_counter = 0
        for device_name in device_name_list:
            chart_index_dict[device_name] = [horizontal_counter, vertical_counter]
            if horizontal_counter == number_of_horizontal_charts - 1:
                horizontal_counter = -1
                vertical_counter = vertical_counter + 1
            horizontal_counter = horizontal_counter + 1
        # Set "number_of_vertical_charts" value as "vertical_counter" value of the last chart.
        number_of_vertical_charts = list(chart_index_dict.values())[-1][1] + 1

        # Set chart border spacing value.
        if number_of_charts == 1:
            chart_spacing = 0
        else:
            chart_spacing = 6
        chart_spacing_half = chart_spacing / 2

        # Get chart width and height per-device.
        chart_width_per_device = chart_width / number_of_horizontal_charts
        chart_height_per_device = chart_height / number_of_vertical_charts

        # Get chart width and height per-device.
        chart_width_per_device_wo_borders = (chart_width / number_of_horizontal_charts) - chart_spacing
        chart_height_per_device_wo_borders = (chart_height / number_of_vertical_charts) - chart_spacing

        # Set antialiasing level as "BEST" in order to avoid low quality chart line because of the highlight effect (more than one line will be overlayed for this appearance).
        ctx.set_antialias(cairo.Antialias.BEST)

        # Set line joining style as "LINE_JOIN_ROUND" in order to avoid spikes at the line joints due to high antialiasing level.
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # Performance data line paths will be used for highlighting the line.
        performance_data1_line_path_dict = {}
        performance_data2_line_path_dict = {}

        # Draw charts per-device.
        for device_name in device_name_list:

            # Draw and fill chart background.
            ctx.rectangle((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half, (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half, chart_width_per_device, chart_height_per_device)
            ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
            ctx.fill()

            # Draw horizontal and vertical gridlines.
            for i in range(3):
                ctx.move_to((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half, (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half + chart_height_per_device/4*(i+1))
                ctx.rel_line_to(chart_width_per_device-chart_spacing, 0)
            for i in range(4):
                ctx.move_to(chart_width_per_device/5*(i+1), 0)
                ctx.move_to((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half + chart_width_per_device/5*(i+1), (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half)
                ctx.rel_line_to(0, chart_height_per_device-chart_spacing)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
            ctx.set_line_width(1)
            ctx.stroke()

            # Draw outer border of the chart.
            ctx.rectangle((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half, (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half, chart_width_per_device-chart_spacing, chart_height_per_device-chart_spacing)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            # Draw outer border of the selected device by using thicker line if all devices are plotted.
            if device_name == selected_device:
                ctx.set_line_width(2)
                ctx.stroke()
            else:
                ctx.set_line_width(1)
                ctx.stroke()
            # Set the line thickness as 1 again in oder to avoid using thick line for the next drawings.
            ctx.set_line_width(1)

            if draw_performance_data1 == 1:

                performance_data1_current = performance_data1[device_name]

                # Draw performance data.
                ctx.move_to((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half, chart_height_per_device+(chart_height_per_device*chart_index_dict[device_name][1])-chart_spacing_half)
                ctx.rel_move_to(0, -chart_height_per_device_wo_borders*performance_data1_current[0]/chart_y_limit_dict[device_name])
                for i in range(chart_data_history - 1):
                    delta_x = (chart_width_per_device_wo_borders*chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width_per_device_wo_borders*chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height_per_device_wo_borders*performance_data1_current[i+1]/chart_y_limit_dict[device_name]) - (chart_height_per_device_wo_borders*performance_data1_current[i]/chart_y_limit_dict[device_name])
                    ctx.rel_line_to(delta_x, -delta_y)
                ctx.stroke_preserve()

                # Set line color (full transparent in order to prevent drawing bolder lines due to overlapping), close the drawn line to fill inside area of it and copy the performance line path to use it for highlighting.
                ctx.rel_line_to(0, chart_height_per_device_wo_borders*performance_data1_current[-1]/chart_y_limit_dict[device_name])
                ctx.rel_line_to(-(chart_width_per_device_wo_borders), 0)
                ctx.close_path()
                performance_data1_line_path_dict[device_name] = ctx.copy_path()
                ctx.set_source_rgba(0, 0, 0, 0)
                ctx.stroke()

                # Use previously copied performance line path and fill the closed area (area below the performance data line).
                ctx.append_path(performance_data1_line_path_dict[device_name])  
                gradient_pattern = cairo.LinearGradient(0, (chart_height_per_device*chart_index_dict[device_name][1])-chart_spacing_half, 0, (chart_height_per_device*chart_index_dict[device_name][1])-chart_spacing_half+chart_height_per_device_wo_borders)
                gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
                gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
                ctx.set_source(gradient_pattern)
                ctx.fill()

            if draw_performance_data2 == 1:

                performance_data2_current = performance_data2[device_name]

                # Set color and line dash style for this performance data line.
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.set_dash([5, 3])

                # Draw performance data.
                ctx.move_to((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half, chart_height_per_device+(chart_height_per_device*chart_index_dict[device_name][1])-chart_spacing_half)
                ctx.rel_move_to(0, -chart_height_per_device_wo_borders*performance_data2_current[0]/chart_y_limit_dict[device_name])
                for i in range(chart_data_history - 1):
                    delta_x = (chart_width_per_device_wo_borders*chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width_per_device_wo_borders*chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height_per_device_wo_borders*performance_data2_current[i+1]/chart_y_limit_dict[device_name]) - (chart_height_per_device_wo_borders*performance_data2_current[i]/chart_y_limit_dict[device_name])
                    ctx.rel_line_to(delta_x, -delta_y)
                ctx.stroke_preserve()

                # Set line color (full transparent in order to prevent drawing bolder lines due to overlapping), close the drawn line to fill inside area of it and copy the performance line path to use it for highlighting.
                ctx.rel_line_to(0, chart_height_per_device_wo_borders*performance_data2_current[-1]/chart_y_limit_dict[device_name])
                ctx.rel_line_to(-(chart_width_per_device_wo_borders), 0)
                ctx.close_path()
                performance_data2_line_path_dict[device_name] = ctx.copy_path()
                ctx.set_source_rgba(0, 0, 0, 0)
                ctx.stroke()

                # Set line style as solid line.
                ctx.set_dash([])

            # Draw device name per chart.
            if number_of_charts > 1:
                ctx.move_to((chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half+3, (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half+12)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.show_text(f'{device_name}')


        # Check if chart line will be highlighted.
        if self.chart_line_highlight == widget:

            # Define local variables for maouse position for lower CPU usage.
            try:
                mouse_position_x = self.mouse_position_x
                mouse_position_y = self.mouse_position_y
            # It gives error at the beginning of the mouse move on the chart.
            except AttributeError:
                return

            # Get the chart which mouse cursor in moved on.
            device_name_to_line_highlight = ""
            for device_name in device_name_list:
                if mouse_position_x > (chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half and mouse_position_x < (chart_width_per_device*chart_index_dict[device_name][0])+chart_spacing_half+chart_width_per_device_wo_borders:
                    if mouse_position_y > (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half and mouse_position_y < (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half+chart_height_per_device_wo_borders:
                        device_name_to_line_highlight = device_name
                        break

            # Prevent errors if mouse cursor on the empty area (chart spacing) between charts (if multiple charts are drawn).
            if device_name_to_line_highlight == "":
                return

            # Use previously copied performance line path(s).
            if draw_performance_data1 == 1:
                ctx.append_path(performance_data1_line_path_dict[device_name])

                # Set line features and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.stroke_preserve()

                # Set line features (white and semi-transparent color in order to overlay with the previous line and generate highlight effect) and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(1, 1, 1, 0.3)
                ctx.stroke()

            if draw_performance_data2 == 1:
                ctx.append_path(performance_data2_line_path_dict[device_name])

                # Set line style as solid line for this performance data line.
                ctx.set_dash([5, 3])

                # Set line features and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.stroke_preserve()

                # Set line features (white and semi-transparent color in order to overlay with the previous line and generate highlight effect) and append the path (draw it).
                ctx.set_line_width(2.5)
                ctx.set_source_rgba(1, 1, 1, 0.3)
                ctx.stroke()

                # Set line style as solid line.
                ctx.set_dash([])


            # Highlight chart point(s).
            # Calculate the length between chart data points.
            data_point_width = chart_width_per_device_wo_borders / (chart_data_history - 1)

            # Calculate number of data points from start (left) to the mouse cursor position and fraction after the last (first data point before the mouse cursor) data point.
            total_length_of_left_charts = (chart_width_per_device*chart_index_dict[device_name_to_line_highlight][0])+chart_spacing_half
            total_length_of_upper_charts = (chart_height_per_device*chart_index_dict[device_name_to_line_highlight][1])+chart_spacing_half
            mouse_position_x_current_chart = mouse_position_x-total_length_of_left_charts
            data_point_count_until_mouse_cursor = mouse_position_x_current_chart / data_point_width
            data_point_count_int = int(data_point_count_until_mouse_cursor)
            fraction = data_point_count_until_mouse_cursor - data_point_count_int

            # Determine the data point to be highlighted when mouse cursor is between two data points.
            if fraction > 0.5:
                chart_point_highlight = data_point_count_int + 1
            # if fraction <= 0.5:
            else:
                chart_point_highlight = data_point_count_int

            # Get location of the point(s) to be highlighted.
            loc_x = total_length_of_left_charts + chart_width_per_device_wo_borders * chart_x_axis[chart_point_highlight]/(chart_data_history-1)
            loc_y_list =[]
            if draw_performance_data1 == 1:
                loc_y1 = total_length_of_upper_charts + chart_height_per_device_wo_borders - (chart_height_per_device_wo_borders*performance_data1[device_name_to_line_highlight][chart_point_highlight]/chart_y_limit_dict[device_name_to_line_highlight])
                loc_y_list.append(loc_y1)
            if draw_performance_data2 == 1:
                loc_y2 = total_length_of_upper_charts + chart_height_per_device_wo_borders - (chart_height_per_device_wo_borders*performance_data2[device_name_to_line_highlight][chart_point_highlight]/chart_y_limit_dict[device_name_to_line_highlight])
                loc_y_list.append(loc_y2)

            # Draw a big point and fill it.
            # Set color for the point to be highlighted.
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            for loc_y in loc_y_list:
                ctx.arc(loc_x, loc_y, 5, 0, 2*3.14)
                ctx.fill()

            # Set font size and text for showing performance data of the highlighted point and get its location data in order to use it for showing a centered box under the text.
            ctx.set_font_size(13)
            performance_data_at_point_text_list =[]
            if draw_performance_data1 == 1:
                if widget_name == "da_cpu_usage":
                    performance_data1_at_point_text = f'{performance_data1[device_name_to_line_highlight][chart_point_highlight]:.{Config.performance_cpu_usage_percent_precision}f} %'
                elif widget_name == "da_memory_usage":
                    performance_data1_at_point_text = f'{performance_data1[device_name_to_line_highlight][chart_point_highlight]:.{Config.performance_memory_data_precision}f} %'
                elif widget_name == "da_disk_speed":
                    performance_data1_at_point_text = f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, performance_data1[device_name_to_line_highlight][chart_point_highlight], performance_disk_data_unit, performance_disk_data_precision)}/s'
                elif widget_name == "da_network_speed":
                    performance_data1_at_point_text = f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, performance_data1[device_name_to_line_highlight][chart_point_highlight], performance_network_data_unit, performance_network_data_precision)}/s'
                elif widget_name == "da_gpu_usage":
                    performance_data1_at_point_text = f'{performance_data1[device_name_to_line_highlight][chart_point_highlight]:.0f} %'
                elif widget_name == "processes_details_da_cpu_usage":
                    performance_data1_at_point_text = f'{performance_data1[device_name_to_line_highlight][chart_point_highlight]:.{Config.processes_cpu_precision}f} %'
                elif widget_name == "processes_details_da_memory_usage":
                    performance_data1_at_point_text = f'{self.performance_data_unit_converter_func("data", "none", performance_data1[device_name_to_line_highlight][chart_point_highlight], processes_memory_data_unit, processes_memory_data_precision)}'
                elif widget_name == "processes_details_da_disk_speed":
                    performance_data1_at_point_text = f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, performance_data1[device_name_to_line_highlight][chart_point_highlight], processes_disk_data_unit, processes_disk_data_precision)}/s'
                # Add "-" before the text if there are 2 performance data lines.
                if len(loc_y_list) == 2:
                    performance_data1_at_point_text = f'-  {performance_data1_at_point_text}'
                performance_data_at_point_text_list.append(performance_data1_at_point_text)

            if draw_performance_data2 == 1:
                if widget_name == "da_cpu_usage":
                    performance_data2_at_point_text = f'- -{performance_data2[device_name_to_line_highlight][chart_point_highlight]:.{Config.performance_cpu_usage_percent_precision}f} %'
                elif widget_name == "da_memory_usage":
                    performance_data2_at_point_text = f'- -{performance_data2[device_name_to_line_highlight][chart_point_highlight]:.{Config.performance_memory_swap_data_precision}f} %'
                elif widget_name == "da_disk_speed":
                    performance_data2_at_point_text = f'- -{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, performance_data2[device_name_to_line_highlight][chart_point_highlight], performance_disk_data_unit, performance_disk_data_precision)}/s'
                elif widget_name == "da_network_speed":
                    performance_data2_at_point_text = f'- -{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, performance_data2[device_name_to_line_highlight][chart_point_highlight], performance_network_data_unit, performance_network_data_precision)}/s'
                elif widget_name == "da_gpu_usage":
                    performance_data2_at_point_text = f'- -{performance_data2[device_name_to_line_highlight][chart_point_highlight]:.0f} %'
                elif widget_name == "processes_details_da_disk_speed":
                    performance_data2_at_point_text = f'- -{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, performance_data2[device_name_to_line_highlight][chart_point_highlight], processes_disk_data_unit, processes_disk_data_precision)}/s'
                performance_data_at_point_text_list.append(performance_data2_at_point_text)

            performance_data_at_point_text = '  |  '.join(performance_data_at_point_text_list)

            text_extends = ctx.text_extents(performance_data_at_point_text)
            text_start_x = text_extends.width / 2
            text_start_y = text_extends.height / 2
            text_border_margin = 10
            origin_for_text =  (chart_height_per_device*chart_index_dict[device_name][1])+chart_spacing_half + chart_height_per_device_wo_borders*0.35

            # Calculate correction value for x location of the text, box under the text and line between box and highligthed data point(s) in order to prevent them going out of the visible area (drawingara) when mouse is close to beginning/end of the drawingarea.
            box_under_text_location_correction = 0
            box_under_text_start = loc_x-text_start_x-text_border_margin
            box_under_text_end = loc_x+text_start_x+text_border_margin
            if box_under_text_start < 0 + chart_spacing_half:
                box_under_text_location_correction = -1 * box_under_text_start + chart_spacing_half
            if box_under_text_end > chart_width - chart_spacing_half:
                box_under_text_location_correction = chart_width - chart_spacing_half - box_under_text_end

            # Set grey color for the box under the text and draw the box.
            ctx.rectangle(box_under_text_start+box_under_text_location_correction,origin_for_text-text_start_y-text_border_margin, text_extends.width+2*text_border_margin, text_extends.height+2*text_border_margin)
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
            ctx.fill()

            # Set color for the text and show the text.
            ctx.move_to(loc_x-text_start_x+box_under_text_location_correction,origin_for_text+text_start_y)
            ctx.set_line_width(1)
            ctx.set_source_rgba(1.0, 1.0, 1.0, 0.7)
            ctx.show_text(performance_data_at_point_text)

            # Draw a line between the highlighted point and the box under the text.
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
            for loc_y in loc_y_list:
                ctx.move_to(loc_x, loc_y-5)
                ctx.line_to(box_under_text_start+box_under_text_location_correction, origin_for_text+text_start_y+15)
                ctx.rel_line_to(text_extends.width+2*text_border_margin, 0)
                ctx.stroke()


    def performance_line_charts_enter_notify_event(self, event, x, y):
        """
        Highlight performance chart line if mouse is moved onto the drawingarea.
        """

        widget = event.get_widget()
        self.chart_line_highlight = widget
        widget.queue_draw()


    def performance_line_charts_leave_notify_event(self, event):
        """
        Revert highlighted performance chart line if mouse is moved out of the drawingarea.
        """

        widget = event.get_widget()
        try:
            self.chart_line_highlight = ""
        except ValueError:
            pass
        widget.queue_draw()


    def performance_line_charts_motion_notify_event(self, event, x, y):
        """
        Highlight performance chart point and show performance data text if mouse is moved on the drawingarea.
        """

        widget = event.get_widget()

        # Get mouse position on the x and y coordinates on the drawingarea.
        self.mouse_position_x = x
        self.mouse_position_y = y

        # Update the chart in order to show visual changes.
        widget.queue_draw()


    def performance_bar_charts_draw(self, widget, ctx, width, height, widget_name):
        """
        Draw performance data as bar chart.
        """

        # Check if drawing will be for Memory tab.
        if widget_name == "da_swap_usage":

            # Get performance data to be drawn.
            from .Memory import Memory
            try:
                performance_data1 = Memory.swap_usage_percent[-1]
            # "swap_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
            except AttributeError:
                return

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Check if drawing will be for Disk tab.
        if widget_name == "da_disk_usage":

            # Get performance data to be drawn.
            from .Disk import Disk
            try:
                performance_data1 = Disk.disk_usage_percentage
            # "disk_usage_percentage" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
            except AttributeError:
                return

            # Get chart colors.
            chart_line_color = Config.chart_line_color_disk_speed_usage

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100

        # Check if widget is the drawingarea on the headerbar for CPU usage.
        if widget_name == "ps_hb_cpu_da":

            # Get performance data to be drawn.
            performance_data1 = self.cpu_usage_percent_ave[-1]

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100

        # Check if widget is the drawingarea on the headerbar for RAM usage.
        if widget_name == "ps_hb_ram_da":

            # Get performance data to be drawn.
            performance_data1 = self.ram_usage_percent[-1]

            # Get chart colors.
            chart_line_color = Config.chart_line_color_memory_percent

            # Get chart y limit value in order to show maximum value of the chart as 100.
            chart_y_limit = 100


        # Get chart background color.
        chart_background_color = [0.0, 0.0, 0.0, 0.0]

        # Get drawingarea size.
        chart_width = width
        chart_height = height

        # Draw and fill chart background.
        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.fill()

        # Draw outer border of the chart.
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.6 * chart_line_color[3])
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.stroke()

        # Draw performance data.
        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3])
        ctx.rectangle(0, 0, chart_width*performance_data1/chart_y_limit, chart_height)
        ctx.fill()


    def unit_converter_variables(self):
        """
        Define values for converting data units and set value precision.
        """

        self.data_unit_list = [[0, "B", "B", "b", "b"], [1, "KiB", "KB", "Kib", "Kb"], [2, "MiB", "MB", "Mib", "Mb"],
                              [3, "GiB", "GB", "Gib", "Gb"], [4, "TiB", "TB", "Tib", "Tb"], [5, "PiB", "PB", "Pib", "Pb"]]


    def performance_data_unit_converter_func(self, data_type, data_type_option, data, unit, precision):
        """
        Convert data units and set value precision (called from several modules).
        """

        data_unit_list = self.data_unit_list
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


Performance = Performance()

