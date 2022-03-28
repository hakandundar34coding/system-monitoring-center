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
            gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.5 * chart_line_color[3])
            gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.1 * chart_line_color[3])
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
                gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.5 * chart_line_color[3])
                gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.1 * chart_line_color[3])
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

        # Get maximum and minimum frequencies of the selected CPU core
        try:
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_max_freq") as reader:
                cpu_max_frequency_selected_core = float(reader.read().strip()) / 1000000
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_min_freq") as reader:
                cpu_min_frequency_selected_core = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            cpu_max_frequency_selected_core = "-"
            cpu_min_frequency_selected_core = "-"

        # Get cache memory values of the selected CPU core
        # Get l1d cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Data":
                cpu_l1d_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l1d_cache_value_selected_core = "-"
        # Get li cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Instruction":
                cpu_l1i_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l1i_cache_value_selected_core = "-"
        # Get l2 cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "2":
                cpu_l2_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l2_cache_value_selected_core = "-"
        # Get l3 cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "3":
                cpu_l3_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l3_cache_value_selected_core = "-"

        # Get CPU architecture
        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"


        # Set CPU tab label texts by using information get
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            self.label1113.set_text(_tr("CPU Usage (Average)"))
        if show_cpu_usage_per_core == 1:
            self.label1113.set_text(_tr("CPU Usage (Per Core)"))
        if isinstance(cpu_max_frequency_selected_core, str) is False:
            self.label1105.set_text(f'{cpu_min_frequency_selected_core:.2f} - {cpu_max_frequency_selected_core:.2f} GHz')
        else:
            self.label1105.set_text(f'{cpu_min_frequency_selected_core} - {cpu_max_frequency_selected_core}')
        self.label1108.set_text(cpu_architecture)
        self.label1109.set_text(f'{cpu_l1i_cache_value_selected_core} - {cpu_l1d_cache_value_selected_core}')
        self.label1110.set_text(f'{cpu_l2_cache_value_selected_core} - {cpu_l3_cache_value_selected_core}')

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
        # try-except is used in order to avoid error if this is first loop of the function. Because "selected_cpu_core_prev" variable is not defined in this situation.
        except AttributeError:
            pass
        self.selected_cpu_core_prev = selected_cpu_core

        self.drawingarea1101.queue_draw()

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names
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
        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture. Physical and logical cores and model name per core information are not tracked easily on this platform. Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
        if "physical id" not in proc_cpuinfo_output:
            cpu_model_names = []
            number_of_physical_cores = number_of_logical_cores
            # Initial value of "number_of_cpu_sockets". This value may not be detected on systems with ARM CPUs.
            number_of_cpu_sockets = f'[{_tr("Unknown")}]'
            # Some processors have "processor", some processors have "Processor" and some processors have both "processor" and "Processor". "processor" is used for core number and "Processor" is used for model name. But "model name" is used for model name on some ARM processors. Model name is repeated for all cores on these processors. "Processor" is used for one time for the processor.
            if "model name" in proc_cpuinfo_output:
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("model name"):
                        cpu_model_names.append(line.split(":")[1].strip())
            if "model name" not in proc_cpuinfo_output and "Processor" in proc_cpuinfo_output:
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("Processor"):
                        cpu_model_names.append(line.split(":")[1].strip())
            if len(cpu_model_names) == 1:
                cpu_model_names = cpu_model_names * number_of_logical_cores
            if "Processor" in proc_cpuinfo_output:
                number_of_cpu_sockets = 0
                number_of_cpu_sockets = number_of_cpu_sockets + 1
            # Some ARM processors do not have model name information in "/proc/cpuinfo" file.
            if cpu_model_names == []:
                cpu_model_names = [_tr("Unknown")]

        # Get current frequency of the selected CPU core
        try:
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_cur_freq") as reader:
                cpu_current_frequency_selected_core = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            with open("/proc/cpuinfo") as reader:
                proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
            proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(selected_cpu_core_number_only)].split("\n")
            for line in proc_cpuinfo_all_cores_lines:
                if line.startswith("cpu MHz"):
                    cpu_current_frequency_selected_core = float(line.split(":")[1].strip()) / 1000
                    break

        # Get number_of_total_threads and number_of_total_processes
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


        # Set and update CPU tab label texts by using information get
        self.label1101.set_text(cpu_model_names[selected_cpu_core_number])
        self.label1102.set_text(selected_cpu_core)
        self.label1111.set_text(f'{number_of_total_processes} - {number_of_total_threads}')
        self.label1112.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
        self.label1103.set_text(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.label1104.set_text(f'{cpu_current_frequency_selected_core:.2f} GHz')
        self.label1106.set_text(f'{number_of_cpu_sockets}')
        self.label1107.set_text(f'{number_of_physical_cores} - {number_of_logical_cores}')


# Generate object
Cpu = Cpu()

