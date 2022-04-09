#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import platform
import cairo

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Cpu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/CpuTab.ui")

        # Get GUI objects
        self.grid1101 = builder.get_object('grid1101')
        self.drawingarea1101 = builder.get_object('drawingarea1101')
        self.button1101 = builder.get_object('button1101')
        self.label1101 = builder.get_object('label1101')
        self.label1102 = builder.get_object('label1102')
        self.label1103 = builder.get_object('label1103')
        self.label1104 = builder.get_object('label1104')
        self.label1105 = builder.get_object('label1105')
        self.label1106 = builder.get_object('label1106')
        self.label1107 = builder.get_object('label1107')
        self.label1108 = builder.get_object('label1108')
        self.label1109 = builder.get_object('label1109')
        self.label1110 = builder.get_object('label1110')
        self.label1111 = builder.get_object('label1111')
        self.label1112 = builder.get_object('label1112')
        self.label1113 = builder.get_object('label1113')

        # Connect GUI signals
        self.button1101.connect("clicked", self.on_button1101_clicked)
        self.drawingarea1101.connect("draw", self.on_drawingarea1101_draw)


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1101_clicked(self, widget):

        from CpuMenu import CpuMenu
        CpuMenu.popover1101p.set_relative_to(widget)
        CpuMenu.popover1101p.set_position(1)
        CpuMenu.popover1101p.popup()


    # ----------------------- Called for drawing average or per-core CPU usage as line/bar chart -----------------------
    def on_drawingarea1101_draw(self, widget, ctx):

        # Draw "average CPU usage" if preferred.
        if Config.show_cpu_usage_per_core == 0:

            # Get chart data history.
            chart_data_history = Config.chart_data_history
            chart_x_axis = list(range(0, chart_data_history))

            # Get performance data to be drawn.
            cpu_usage_percent_ave = Performance.cpu_usage_percent_ave

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent
            chart_background_color = Config.chart_background_color_all_charts

            # Get drawingarea size.
            chart_width = Gtk.Widget.get_allocated_width(widget)
            chart_height = Gtk.Widget.get_allocated_height(widget)

            # Draw and fill chart background.
            ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
            ctx.rectangle(0, 0, chart_width, chart_height)
            ctx.fill()

            # Draw horizontal and vertical gridlines.
            ctx.set_line_width(1)
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
            for i in range(3):
                ctx.move_to(0, chart_height/4*(i+1))
                ctx.rel_line_to(chart_width, 0)
            for i in range(4):
                ctx.move_to(chart_width/5*(i+1), 0)
                ctx.rel_line_to(0, chart_height)
            ctx.stroke()

            # Draw outer border of the chart.
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            ctx.rectangle(0, 0, chart_width, chart_height)
            ctx.stroke()

            # Draw performance data.
            ctx.move_to(0, chart_height)
            ctx.rel_move_to(0, -chart_height*cpu_usage_percent_ave[0]/100)
            for i in range(chart_data_history - 1):
                delta_x = (chart_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y = (chart_height*cpu_usage_percent_ave[i+1]/100) - (chart_height*cpu_usage_percent_ave[i]/100)
                ctx.rel_line_to(delta_x, -delta_y)

            # Change line color before drawing lines for closing the drawn line in order to revent drawing bolder lines due to overlapping.
            ctx.stroke_preserve()
            ctx.set_source_rgba(0, 0, 0, 0)

            # Close the drawn line to fill inside area of it.
            ctx.rel_line_to(0, chart_height*cpu_usage_percent_ave[-1]/100)
            ctx.rel_line_to(-(chart_width), 0)
            ctx.close_path()

            # Fill the closed area.
            ctx.stroke_preserve()
            gradient_pattern = cairo.LinearGradient(0, 0, 0, chart_height)
            gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
            gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw "per-core CPU usage" if preferred.
        else:

            # Get chart data history.
            chart_data_history = Config.chart_data_history
            chart_x_axis = list(range(0, chart_data_history))

            # Get performance data to be drawn.
            logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
            number_of_logical_cores = Performance.number_of_logical_cores
            cpu_usage_percent_per_core1 = Performance.cpu_usage_percent_per_core

            # Get chart colors.
            chart_line_color = Config.chart_line_color_cpu_percent
            chart_background_color = Config.chart_background_color_all_charts

            # Get drawingarea size.
            chart_width = Gtk.Widget.get_allocated_width(widget)
            chart_height = Gtk.Widget.get_allocated_height(widget)

            from math import sqrt, ceil
            # Get number of horizontal and vertical charts (per-core).
            for i in range(1, 1000):
                if number_of_logical_cores % i == 0:
                    number_of_horizontal_charts = i
                    number_of_vertical_charts = number_of_logical_cores // i
                    if number_of_horizontal_charts >= number_of_vertical_charts:
                        if number_of_horizontal_charts > 2 * number_of_vertical_charts:
                            number_of_horizontal_charts = number_of_vertical_charts = ceil(sqrt(number_of_logical_cores))
                        break

            # Get chart index list for horizontal and vertical charts.
            chart_index_list = []
            for i in range(number_of_vertical_charts):
                for j in range(number_of_horizontal_charts):
                    chart_index_list.append([j, i])

            # Spacing 3 from left and right.
            chart_width_per_core = (chart_width / number_of_horizontal_charts) - 6
            # Spacing 3 from top and bottom.
            chart_height_per_core = (chart_height / number_of_vertical_charts) - 6

            # Draw charts per-core.
            for j, cpu_core in enumerate(logical_core_list_system_ordered):

                # Get performance data for the current core.
                cpu_usage_percent_per_core = cpu_usage_percent_per_core1[j]

                # Draw and fill chart background.
                ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
                ctx.rectangle(0, 0, chart_width_per_core, chart_height_per_core)
                ctx.fill()

                # Draw horizontal and vertical gridlines.
                ctx.set_line_width(1)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
                for i in range(3):
                    ctx.move_to((chart_width_per_core+6)*chart_index_list[j][0], chart_index_list[j][1]*(chart_height_per_core+6) + chart_height_per_core/4*(i+1))
                    ctx.rel_line_to(chart_width_per_core, 0)
                for i in range(4):
                    ctx.move_to((chart_width_per_core+6)*chart_index_list[j][0] + chart_width_per_core/5*(i+1), (chart_height_per_core+6)*chart_index_list[j][1])
                    ctx.rel_line_to(0, chart_height_per_core)
                ctx.stroke()

                # Draw outer border of the chart.
                ctx.set_line_width(1)
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.rectangle(chart_index_list[j][0]*(chart_width_per_core+6), chart_index_list[j][1]*(chart_height_per_core+6), chart_width_per_core, chart_height_per_core)
                ctx.stroke()

                # Draw performance data.
                ctx.move_to((chart_width_per_core+6)*chart_index_list[j][0], (chart_height_per_core)+(chart_height_per_core+6)*chart_index_list[j][1])
                ctx.rel_move_to(0, -chart_height_per_core*cpu_usage_percent_per_core[0]/100)
                for i in range(len(chart_x_axis) - 1):
                    delta_x = (chart_width_per_core * chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width_per_core * chart_x_axis[i]/(chart_data_history-1))
                    delta_y = (chart_height_per_core*cpu_usage_percent_per_core[i+1]/100) - (chart_height_per_core*cpu_usage_percent_per_core[i]/100)
                    ctx.rel_line_to(delta_x, -delta_y)

                # Change line color before drawing lines for closing the drawn line in order to revent drawing bolder lines due to overlapping.
                ctx.stroke_preserve()
                ctx.set_source_rgba(0, 0, 0, 0)

                # Close the drawn line to fill inside area of it.
                ctx.rel_line_to(0, chart_height_per_core*cpu_usage_percent_per_core[-1]/100)
                ctx.rel_line_to(-(chart_width_per_core), 0)
                ctx.close_path()

                # Fill the closed area.
                ctx.stroke_preserve()
                gradient_pattern = cairo.LinearGradient(0, (chart_height_per_core+6)*chart_index_list[j][1], 0, (chart_height_per_core)+(chart_height_per_core+6)*chart_index_list[j][1])
                gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
                gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
                ctx.set_source(gradient_pattern)
                ctx.fill()

                # Draw core number per chart.
                ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
                ctx.move_to(chart_index_list[j][0]*(chart_width_per_core+6)+4, chart_index_list[j][1]*(chart_height_per_core+6)+12)
                ctx.show_text(f'{cpu_core.split("cpu")[-1]}')


    # ----------------------------------- CPU - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
    def cpu_initial_func(self):

        logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]


        # Get information.
        cpu_core_min_frequency, cpu_core_max_frequency = self.cpu_core_min_max_frequency_func(selected_cpu_core_number_only)
        cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache = self.cpu_core_l1_l2_l3_cache_func(selected_cpu_core)
        cpu_architecture = self.cpu_architecture_func()


        # Show information on labels.
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            self.label1113.set_text(_tr("CPU Usage (Average)"))
        if show_cpu_usage_per_core == 1:
            self.label1113.set_text(_tr("CPU Usage (Per Core)"))
        if isinstance(cpu_core_max_frequency, str) is False:
            self.label1105.set_text(f'{cpu_core_min_frequency:.2f} - {cpu_core_max_frequency:.2f} GHz')
        else:
            self.label1105.set_text(f'{cpu_core_min_frequency} - {cpu_core_max_frequency}')
        self.label1108.set_text(cpu_architecture)
        self.label1109.set_text(f'{cpu_core_l1i_cache} - {cpu_core_l1d_cache}')
        self.label1110.set_text(f'{cpu_core_l2_cache} - {cpu_core_l3_cache}')

        self.initial_already_run = 1


    # ----------------------------------- CPU - Get CPU Data Function (gets CPU data, shows on the labels on the GUI) -----------------------------------
    def cpu_loop_func(self):

        number_of_logical_cores = Performance.number_of_logical_cores
        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
        selected_cpu_core_number = Performance.selected_cpu_core_number
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]
        # Run "cpu_initial_func" if selected CPU core is changed since the last loop.
        try:                                                                                      
            if self.selected_cpu_core_prev != selected_cpu_core:
                self.cpu_initial_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_cpu_core_prev = selected_cpu_core

        self.drawingarea1101.queue_draw()


        # Get information.
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = self.cpu_number_of_physical_cores_sockets_cpu_name_func(selected_cpu_core_number, number_of_logical_cores)
        cpu_core_current_frequency = self.cpu_core_current_frequency_func(selected_cpu_core_number_only)
        number_of_total_processes, number_of_total_threads = self.cpu_total_processes_threads_func()
        system_up_time = self.cpu_system_up_time_func()


        # Show information on labels.
        self.label1101.set_text(cpu_model_name)
        self.label1102.set_text(selected_cpu_core)
        self.label1111.set_text(f'{number_of_total_processes} - {number_of_total_threads}')
        self.label1112.set_text(system_up_time)
        self.label1103.set_text(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.label1104.set_text(f'{cpu_core_current_frequency:.2f} GHz')
        self.label1106.set_text(f'{number_of_cpu_sockets}')
        self.label1107.set_text(f'{number_of_physical_cores} - {number_of_logical_cores}')


    # ----------------------- Get minimum and maximum frequencies of the selected CPU core -----------------------
    def cpu_core_min_max_frequency_func(self, selected_cpu_core_number_only):

        try:
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_max_freq") as reader:
                cpu_core_max_frequency = float(reader.read().strip()) / 1000000
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_min_freq") as reader:
                cpu_core_min_frequency = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            cpu_core_max_frequency = "-"
            cpu_core_min_frequency = "-"

        return cpu_core_min_frequency, cpu_core_max_frequency


    # ----------------------- Get cache memory values of the selected CPU core -----------------------
    def cpu_core_l1_l2_l3_cache_func(self, selected_cpu_core):

        # Get l1d cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Data":
                cpu_core_l1d_cache = cache_size
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
                cpu_core_l1i_cache = cache_size
        except FileNotFoundError:
            cpu_core_l1i_cache = "-"

        # Get l2 cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "2":
                cpu_core_l2_cache = cache_size
        except FileNotFoundError:
            cpu_core_l2_cache = "-"

        # Get l3 cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "3":
                cpu_core_l3_cache = cache_size
        except FileNotFoundError:
            cpu_core_l3_cache = "-"

        return cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache


    # ----------------------- Get CPU architecture -----------------------
    def cpu_architecture_func(self):

        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"

        return cpu_architecture


    # ----------------------- Get number of physical cores, number_of_cpu_sockets, cpu_model_names -----------------------
    def cpu_number_of_physical_cores_sockets_cpu_name_func(self, selected_cpu_core_number, number_of_logical_cores):

        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_output = reader.read()
        proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "x86_64" architecture. Physical and logical cores and model name per core information are tracked easily on this platform.
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
            cpu_model_name = cpu_model_names[selected_cpu_core_number]

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture. Physical and logical cores and model name per core information are not tracked easily on this platform. Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
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

            # Redefine "selected_cpu_core_number" in order to get information of the selected CPU core.
            if len(cpu_implementer_list) == number_of_logical_cores:
                selected_cpu_core_number = selected_cpu_core_number
            # There may be only one instance of register values even if CPU has multiple cores.
            else:
                selected_cpu_core_number = 0

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
            search_text1 = cpu_implementer_list[selected_cpu_core_number].split("0x", 1)[-1]
            search_text2 = "\t" + cpu_part_list[selected_cpu_core_number].split("0x", 1)[-1]
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
                cpu_architecture = arm_architecture_dict[cpu_architecture_list[selected_cpu_core_number]]
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


    # ----------------------- Get current frequency of the selected CPU core -----------------------
    def cpu_core_current_frequency_func(self, selected_cpu_core_number_only):

        try:
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_cur_freq") as reader:
                cpu_core_current_frequency = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            with open("/proc/cpuinfo") as reader:
                proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
            proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(selected_cpu_core_number_only)].split("\n")
            for line in proc_cpuinfo_all_cores_lines:
                if line.startswith("cpu MHz"):
                    cpu_core_current_frequency = float(line.split(":")[1].strip()) / 1000
                    break

        return cpu_core_current_frequency


    # ----------------------- Get number_of_total_threads and number_of_total_processes -----------------------
    def cpu_total_processes_threads_func(self):

        thread_count_list = []
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]

        for pid in pid_list:
            try:
                with open("/proc/" + pid + "/status") as reader:
                    proc_status_output = reader.read()
            # try-except is used in order to skip to the next loop without application error if a "FileNotFoundError" error is encountered when process is ended after process list is get.
            except (FileNotFoundError, ProcessLookupError) as me:
                continue
            # Append number of threads of the process
            thread_count_list.append(int(proc_status_output.split("\nThreads:", 1)[1].split("\n", 1)[0].strip()))

        number_of_total_processes = len(thread_count_list)
        number_of_total_threads = sum(thread_count_list)

        return number_of_total_processes, number_of_total_threads


    # ----------------------- Get system up time (sut) -----------------------
    def cpu_system_up_time_func(self):

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


# Generate object
Cpu = Cpu()

