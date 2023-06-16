import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os

import cairo
from math import sin, cos

from locale import gettext as _tr

from .Config import Config
from .Performance import Performance
from . import Common
from . import Libsysmon


class Summary:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        # Label (Summary)
        label = Common.tab_title_label(_tr("Summary"))
        self.tab_grid.attach(label, 0, 0, 1, 1)

        # Summary tab drawingarea
        self.da_summary = Common.drawingarea(self.performance_summary_graph_draw, "da_summary")
        self.tab_grid.attach(self.da_summary, 0, 1, 1, 1)


    def summary_initial_func(self):
        """
        Initial code.
        """

        self.initial_already_run = 1


    def summary_loop_func(self):
        """
        Draw graphics for showing performance data.
        """

        self.da_summary.queue_draw()


    def performance_summary_graph_draw(self, widget, ctx, width, height):
        """
        Draw performance summary data.
        """

        # Get chart colors of performance tab sub-tab charts.
        chart_line_color_cpu_percent = Config.chart_line_color_cpu_percent
        chart_line_color_memory_percent = Config.chart_line_color_memory_percent
        chart_line_color_disk_speed_usage = Config.chart_line_color_disk_speed_usage
        chart_line_color_network_speed_data = Config.chart_line_color_network_speed_data

        # Get performance data and set text format.
        performance_cpu_usage_percent_precision = 0
        cpu_usage_text = f'{Performance.cpu_usage_percent_ave[-1]:.{performance_cpu_usage_percent_precision}f}'
        performance_memory_data_precision = 0
        ram_usage_text = f'{Performance.ram_usage_percent[-1]:.{performance_memory_data_precision}f}'
        if Libsysmon.get_environment_type() == "flatpak":
            import subprocess
            ls_proc_list = (subprocess.run(["flatpak-spawn", "--host", "ls", "/proc/"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split()
            processes_number_text = f'{len([filename for filename in ls_proc_list if filename.isdigit()])}'
        else:
            processes_number_text = f'{len([filename for filename in os.listdir("/proc/") if filename.isdigit()])}'
        swap_usage_text = f'{Performance.swap_usage_percent[-1]:.0f}%'
        performance_disk_data_precision = 1
        performance_disk_data_unit = Config.performance_disk_data_unit
        performance_disk_speed_bit = Config.performance_disk_speed_bit
        disk_read_speed_text = f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, Performance.disk_read_speed[Performance.selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s'
        disk_write_speed_text = f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, Performance.disk_write_speed[Performance.selected_disk][-1], performance_disk_data_unit, performance_disk_data_precision)}/s'
        performance_network_data_precision = 1
        performance_network_data_unit = Config.performance_network_data_unit
        performance_network_speed_bit = Config.performance_network_speed_bit
        network_download_speed_text = f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, Performance.network_receive_speed[Performance.selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s'
        network_upload_speed_text = f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, Performance.network_send_speed[Performance.selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s'


        # Set antialiasing level as "BEST" in order to avoid low quality chart line because of the highlight effect (more than one line will be overlayed for this appearance).
        ctx.set_antialias(cairo.Antialias.BEST)

        # Set line joining style as "LINE_JOIN_ROUND" in order to avoid spikes at the line joints due to high antialiasing level.
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # Define pi number
        pi_number = 3.14159

        # Get drawingarea size.
        chart_width = width
        chart_height = height

        # Get biggest outer frame size. Aspect ratio of this frame is fixed in order to avoid changing aspect ratio of the drawn objects when window size is changed.
        if chart_width > chart_height * 1.384:
            frame_width = chart_height * 1.384
            frame_height = chart_height
        else:
            frame_width = chart_width
            frame_height = chart_width / 1.384


        # Define dimensions, locations, etc. to use them for scalable graphics.
        gauge_outer_radius = frame_height * 0.43
        gauge_circular_center_x = chart_width / 2 - gauge_outer_radius * 0.48
        gauge_inner_radius = gauge_outer_radius * 0.57
        background_upper_lower_band_height = chart_height * 0.1
        background_upper_lower_band_vertex = chart_height * 0.15
        background_upper_lower_band_vertex_width = gauge_outer_radius * 2.26
        shadow_radius = gauge_outer_radius * 0.8
        shadow_center_loc_y = frame_height * 0.485
        gauge_indicator_line_major_thickness = gauge_outer_radius * 0.02
        gauge_indicator_line_minor_thickness = gauge_outer_radius * 0.01
        gauge_indicator_line_major_length = gauge_outer_radius * 0.04
        gauge_indicator_line_minor_length = gauge_outer_radius * 0.026
        gauge_indicator_line_major_move = gauge_outer_radius * 0.053
        gauge_indicator_line_minor_move = gauge_outer_radius * 0.063
        gauge_indicator_text_radius = gauge_outer_radius * 0.73
        gauge_indicator_text_correction = gauge_outer_radius * 0.047
        gauge_indicator_text_move = gauge_outer_radius * 0.027
        gauge_indicator_text_size = gauge_outer_radius * 0.091
        gauge_indicator_text_size_smaller = gauge_indicator_text_size * 0.78
        gauge_indicator_text_size_smallest = gauge_indicator_text_size * 0.64
        gauge_cpu_ram_label_text_move = gauge_outer_radius * 0.266
        gauge_cpu_ram_label_text_margin = gauge_outer_radius * 0.07
        gauge_cpu_ram_usage_text_size = gauge_outer_radius * 0.25
        gauge_cpu_ram_usage_text_shadow_move = gauge_outer_radius * 0.014
        gauge_cpu_ram_usage_text_move = gauge_outer_radius * 0.026
        gauge_percentage_label_text_below_cpu_ram_move = gauge_outer_radius * 0.074
        gauge_percentage_label_text_below_cpu_ram_size = gauge_outer_radius * 0.08
        gauge_processes_swap_label_text_size = gauge_indicator_text_size * 0.88
        gauge_processes_swap_label_text_move = gauge_outer_radius * 0.22
        gauge_processes_swap_usage_text_size = gauge_cpu_ram_usage_text_size * 0.45
        gauge_processes_swap_usage_text_move = gauge_outer_radius * 0.34
        gauge_processes_swap_usage_text_shadow_move = gauge_cpu_ram_usage_text_shadow_move * 0.5
        gauge_separator_line_vertical_center_length = gauge_outer_radius * 0.94
        gauge_separator_line_vertical_upper_start = gauge_outer_radius * 0.83
        gauge_separator_line_vertical_upper_length = gauge_outer_radius * 0.23
        gauge_separator_line_vertical_lower_start = gauge_outer_radius * 0.6
        gauge_separator_line_vertical_lower_length = gauge_outer_radius * 0.23
        gauge_right_outer_radius = gauge_outer_radius * 1.05
        gauge_right_move = gauge_outer_radius * 0.938
        gauge_right_upper_lower_edge_thickness = gauge_outer_radius * 0.07
        gauge_right_upper_lower_edge_move_horizontal = gauge_right_outer_radius * 0.027
        gauge_separator_line_horizontal_start = gauge_outer_radius * 0.23
        gauge_separator_line_horizontal_length = gauge_outer_radius * 0.6
        gauge_separator_thickness = gauge_outer_radius * 0.00887
        gauge_disk_network_label_text_size = gauge_indicator_text_size * 0.88
        gauge_disk_read_speed_label_text_move_x = gauge_outer_radius * 0.09
        gauge_disk_read_speed_label_text_move_y = gauge_outer_radius * 0.5
        gauge_disk_write_speed_label_text_move_x = gauge_outer_radius * 0.21
        gauge_disk_write_speed_label_text_move_y = gauge_outer_radius * 0.2
        gauge_network_download_speed_label_text_move_x = gauge_outer_radius * 0.21
        gauge_network_download_speed_label_text_move_y = gauge_outer_radius * 0.15
        gauge_network_upload_speed_label_text_move_x = gauge_outer_radius * 0.09
        gauge_network_upload_speed_label_text_move_y = gauge_outer_radius * 0.43
        gauge_disk_network_usage_text_size = gauge_cpu_ram_usage_text_size * 0.4
        gauge_disk_network_usage_text_shadow_move = gauge_outer_radius * 0.009
        gauge_disk_network_usage_text_move_y = gauge_outer_radius * 0.11


        # Draw a rounded rectangle to use it as outer frame of the chart.
        chart_bg_border_thickness = 0
        chart_bg_width = chart_width - 2 * chart_bg_border_thickness
        chart_bg_height = chart_height - 2 * chart_bg_border_thickness
        chart_bg_radius = gauge_outer_radius * 0.06
        ctx.arc(chart_bg_border_thickness+chart_bg_radius, chart_bg_border_thickness+chart_bg_radius, chart_bg_radius, pi_number, 3*pi_number/2)
        ctx.arc(chart_bg_border_thickness+chart_bg_width-chart_bg_radius, chart_bg_border_thickness+chart_bg_radius, chart_bg_radius, 3*pi_number/2, 0)
        ctx.arc(chart_bg_border_thickness+chart_bg_width-chart_bg_radius, chart_bg_border_thickness+chart_bg_height-chart_bg_radius, chart_bg_radius, 0, pi_number/2)
        ctx.arc(chart_bg_border_thickness+chart_bg_radius, chart_bg_border_thickness+chart_bg_height-chart_bg_radius, chart_bg_radius, pi_number/2, pi_number)
        ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
        ctx.fill()

        # Generate a smaller second rounded rectangle for clipping the latter drawings.
        # Drawings outside this shape will not be drawn/shown because of clipping.
        chart_bg_border_thickness = gauge_outer_radius * 0.023
        chart_bg_width = chart_width - 2 * chart_bg_border_thickness
        chart_bg_height = chart_height - 2 * chart_bg_border_thickness
        chart_bg_radius = gauge_outer_radius * 0.04
        ctx.arc(chart_bg_border_thickness+chart_bg_radius, chart_bg_border_thickness+chart_bg_radius, chart_bg_radius, pi_number, 3*pi_number/2)
        ctx.arc(chart_bg_border_thickness+chart_bg_width-chart_bg_radius, chart_bg_border_thickness+chart_bg_radius, chart_bg_radius, 3*pi_number/2, 0)
        ctx.arc(chart_bg_border_thickness+chart_bg_width-chart_bg_radius, chart_bg_border_thickness+chart_bg_height-chart_bg_radius, chart_bg_radius, 0, pi_number/2)
        ctx.arc(chart_bg_border_thickness+chart_bg_radius, chart_bg_border_thickness+chart_bg_height-chart_bg_radius, chart_bg_radius, pi_number/2, pi_number)
        ctx.clip()

        # Draw and fill chart background.
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.set_source_rgba(44/255, 60/255, 73/255, 1.0)
        ctx.fill()

        # Save current (default) transformations (translation, rotation, scale, color, line thickness, etc.) to restore back.
        ctx.save()

        # Draw background upper band.
        ctx.move_to(0, 0)
        ctx.rel_line_to(0, (chart_height - frame_height) / 2)
        ctx.rel_line_to(0, background_upper_lower_band_height)
        ctx.rel_line_to((chart_width - frame_width) / 2, 0)
        ctx.rel_line_to(background_upper_lower_band_vertex_width / 2, background_upper_lower_band_vertex - background_upper_lower_band_height)
        ctx.rel_line_to(background_upper_lower_band_vertex_width / 2, -(background_upper_lower_band_vertex - background_upper_lower_band_height))
        ctx.rel_line_to(frame_width - background_upper_lower_band_vertex_width, 0)
        ctx.rel_line_to((chart_width - frame_width) / 2, 0)
        ctx.rel_line_to(0, -background_upper_lower_band_height)
        ctx.rel_line_to(0, -(chart_height - frame_height) / 2)
        ctx.rel_line_to(-chart_width, 0)
        ctx.close_path()
        background_upper_lower_band_path = ctx.copy_path()
        gradient_pattern = cairo.LinearGradient(0, (chart_height - frame_height) / 2 + background_upper_lower_band_height * 0.66, 0, (chart_height - frame_height) / 2 + background_upper_lower_band_vertex)
        gradient_pattern.add_color_stop_rgba(0, 80/255, 107/255, 137/255, 1)
        gradient_pattern.add_color_stop_rgba(0.10, 85/255, 117/255, 147/255, 1)
        gradient_pattern.add_color_stop_rgba(0.55, 110/255, 187/255, 197/255, 1)
        gradient_pattern.add_color_stop_rgba(0.70, 149/255, 236/255, 251/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 179/255, 236/255, 240/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()

        # Flip (scale), rotate and translate the copied background upper band and draw background lower band.
        ctx.scale(-1, 1)
        ctx.translate(0, chart_height)
        ctx.rotate(180*pi_number/180)
        ctx.append_path(background_upper_lower_band_path)
        ctx.set_source(gradient_pattern)
        ctx.fill()

        # Restore current (default) transformations (translation, rotation, scale, etc.)
        ctx.restore()


        # Translate, rotate and scale coordinate system and draw shadow of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, (chart_height / 2) + shadow_center_loc_y)
        ctx.scale(1, 0.25)
        ctx.arc(0, 0, shadow_radius, 2*pi_number*0.5, 0)
        gradient_pattern = cairo.LinearGradient(0, -shadow_radius/2, 0, 0)
        gradient_pattern.add_color_stop_rgba(0, 50/255, 50/255, 50/255, 0.55)
        gradient_pattern.add_color_stop_rgba(1, 50/255, 50/255, 50/255, 0)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        # Restore default transformations.
        ctx.restore()


        # Draw rectangle part of the background of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90+40)*pi_number/180
        ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
        angle1 = (90-40)*pi_number/180
        ctx.line_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -2*gauge_right_outer_radius*cos(angle1))
        ctx.set_source_rgba(34/255, 52/255, 71/255, 1)
        ctx.fill()
        ctx.restore()


        # Draw circular (partial) part of the background and edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = -40*pi_number/180
        end_angle = 40*pi_number/180

        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        # Draw upper edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90+40)*pi_number/180
        # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
        ctx.move_to(gauge_right_outer_radius*sin(angle1)-gauge_right_upper_lower_edge_move_horizontal, gauge_right_outer_radius*cos(angle1))
        ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)+gauge_right_outer_radius, 0, gauge_right_outer_radius*cos(angle1))
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw lower edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90-40)*pi_number/180
        # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
        ctx.move_to(gauge_right_outer_radius*sin(angle1)-gauge_right_upper_lower_edge_move_horizontal, gauge_right_outer_radius*cos(angle1))
        ctx.rel_move_to(0, -gauge_right_outer_radius*0.07)
        ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)-gauge_right_outer_radius, 0, gauge_right_outer_radius*cos(angle1))
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw fillet on the connection point of the upper right corner of the right gauge for continuous gauge edge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = -90*pi_number/180
        end_angle = -55*pi_number/180
        angle1 = (90-40)*pi_number/180
        ctx.translate(gauge_right_outer_radius*sin(angle1), -gauge_right_outer_radius*cos(angle1))
        ctx.translate(-gauge_right_outer_radius*0.03, gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius*0.07)
        scale_value = 1-0.93
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba((0.93 - 0.93) / scale_value, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba((0.94 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.95 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba((0.98 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.99 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius*0.07, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        # Draw fillet on the connection point of the lower right corner of the right gauge for continuous gauge edge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = 55*pi_number/180
        end_angle = 90*pi_number/180
        angle1 = (90+40)*pi_number/180
        ctx.translate(gauge_right_outer_radius*sin(angle1), -gauge_right_outer_radius*cos(angle1))
        ctx.translate(-gauge_right_outer_radius*0.03, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius*0.07)
        scale_value = 1-0.93
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba((0.93 - 0.93) / scale_value, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba((0.94 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.95 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba((0.98 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.99 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius*0.07, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)

        # Draw white reflection on upper right area of the circular edge of the right gauge.
        for i in range(2):
            start_angle = (305+15)*pi_number/180
            end_angle = (305+25+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_right_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_right_outer_radius*0.992, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_right_outer_radius*0.992, 0, 0, gauge_right_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection on upper area of the upper edge of the right gauge.
        for i in range(2):
            angle1 = (90+40)*pi_number/180
            # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
            ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
            ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
            ctx.rel_line_to(-gauge_right_outer_radius, 0)
            ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
            gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)*0.98, 0, gauge_right_outer_radius*cos(angle1))
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection on lower area of the lower edge of the right gauge.
        for i in range(2):
            angle1 = (90-40)*pi_number/180
            # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
            ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
            ctx.rel_move_to(0, -gauge_right_outer_radius*0.07)
            ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
            ctx.rel_line_to(-gauge_right_outer_radius, 0)
            ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
            gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)*0.98, 0, gauge_right_outer_radius*cos(angle1))
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        ctx.restore()


        # Draw shadow on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + 0, chart_height / 2)
        start_angle = -40*pi_number/180
        end_angle = 40*pi_number/180

        gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius, 0, 0, gauge_right_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 0/255, 0/255, 0/255, 0)
        gradient_pattern.add_color_stop_rgba(0, 0/255, 0/255, 0/255, 0.5)
        gradient_pattern.add_color_stop_rgba(1, 0/255, 0/255, 0/255, 0)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius, start_angle, end_angle)
        ctx.rel_line_to(-gauge_right_outer_radius, -gauge_outer_radius*0.067)
        ctx.rel_line_to(0, -gauge_right_outer_radius-gauge_outer_radius*0.333)
        ctx.fill()
        ctx.restore()


        # Draw horizontal separator line on the center of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        ctx.move_to(gauge_separator_line_horizontal_start, 0)
        ctx.rel_line_to(gauge_separator_line_horizontal_length, 0)
        ctx.set_line_width(gauge_separator_thickness)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()
        ctx.restore()


        # Draw circular (partial) line on the left of the disk read/write labels on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        start_angle = -30.5*pi_number/180
        end_angle = -4*pi_number/180

        ctx.set_line_width(gauge_separator_thickness)
        ctx.set_source_rgba(chart_line_color_disk_speed_usage[0], chart_line_color_disk_speed_usage[1], chart_line_color_disk_speed_usage[2], chart_line_color_disk_speed_usage[3])
        ctx.arc(0, 0, gauge_outer_radius * 1.07, start_angle, end_angle)
        ctx.stroke()
        ctx.restore()


        # Draw circular (partial) line on the left of the network download/upload labels on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        start_angle = 4*pi_number/180
        end_angle = 30.5*pi_number/180

        ctx.set_line_width(gauge_separator_thickness)
        ctx.set_source_rgba(chart_line_color_network_speed_data[0], chart_line_color_network_speed_data[1], chart_line_color_network_speed_data[2], chart_line_color_network_speed_data[3])
        ctx.arc(0, 0, gauge_outer_radius * 1.07, start_angle, end_angle)
        ctx.stroke()
        ctx.restore()


        # Draw background and outer circle of the circular gauge.
        ctx.arc(gauge_circular_center_x, chart_height / 2, gauge_outer_radius, 0, 2*pi_number)
        gradient_pattern = cairo.RadialGradient(gauge_circular_center_x, chart_height / 2, 0, gauge_circular_center_x, chart_height / 2, gauge_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.86, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.88, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.90, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.96, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()


        # Draw background and inner circle of the circular gauge.
        ctx.arc(gauge_circular_center_x, chart_height / 2, gauge_inner_radius, 0, 2*pi_number)
        gradient_pattern = cairo.RadialGradient(gauge_circular_center_x, chart_height / 2, 0, gauge_circular_center_x, chart_height / 2, gauge_inner_radius)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.96, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()


        # Rotate the coordinate system and draw reflection on the background of the inner circle.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.rotate(-45*pi_number/180)
        ctx.arc(0, 0, gauge_inner_radius*0.94, 0, 2*pi_number)
        gradient_pattern = cairo.LinearGradient(0, -gauge_inner_radius*0.94/2, 0, gauge_inner_radius*0.94/2)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.5, 72/255, 88/255, 107/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 32/255, 41/255, 49/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Save translations.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)

        # Draw white reflection (on 180 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (180-40-i)*pi_number/180
            end_angle = (180+40+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 305 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (305-20-i)*pi_number/180
            end_angle = (305+20+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 45 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (45-20-i)*pi_number/180
            end_angle = (45+20+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 270 degree) on the inner circle of the circular gauge.
        for i in range(3):
            start_angle = (270-35-i)*pi_number/180
            end_angle = (270+35+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_inner_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_inner_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius*0.98, 0, 0, gauge_inner_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 90 degree) on the inner circle of the circular gauge.
        for i in range(3):
            start_angle = (90-25-i)*pi_number/180
            end_angle = (90+25+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_inner_radius*0.96, end_angle, start_angle)
            ctx.arc(0, 0, gauge_inner_radius*0.94, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius*0.94, 0, 0, gauge_inner_radius*0.96)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Restore translations.
        ctx.restore()


        # Draw percentage indicator lines on the left side.
        for i, angle in enumerate([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
            ctx.save()
            ctx.translate(gauge_circular_center_x, chart_height / 2)
            ctx.rotate(((i*15)+15)*pi_number/180)

            if angle % 20 == 0:
                ctx.rectangle(-gauge_indicator_line_major_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_major_move, gauge_indicator_line_major_thickness, gauge_indicator_line_major_length)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            else:
                ctx.rectangle(-gauge_indicator_line_minor_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_minor_move, gauge_indicator_line_minor_thickness, gauge_indicator_line_minor_length)
                ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
            ctx.fill()

            ctx.restore()

            # Draw percentage numbers on the left side if angle value is power of 20 ("gauge_indicator_text_correction" is a correction number for aligning the texts).
            if angle % 20 == 0:
                ctx.save()
                ctx.translate((gauge_circular_center_x)-gauge_indicator_text_correction, (chart_height / 2)+gauge_indicator_text_correction)
                angle1 = -((i*15)+15)*pi_number/180
                ctx.move_to((gauge_indicator_text_radius-gauge_indicator_text_move)*sin(angle1), (gauge_indicator_text_radius-gauge_indicator_text_move)*cos(angle1))
                ctx.set_font_size(gauge_indicator_text_size)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                ctx.show_text(f'{angle}')
                ctx.restore()

        # Draw percentage indicator lines on the right side.
        for i, angle in enumerate([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
            ctx.save()
            ctx.translate(gauge_circular_center_x, chart_height / 2)
            ctx.rotate(-((i*15)+15)*pi_number/180)

            if angle % 20 == 0:
                ctx.rectangle(-gauge_indicator_line_major_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_major_move, gauge_indicator_line_major_thickness, gauge_indicator_line_major_length)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            else:
                ctx.rectangle(-gauge_indicator_line_minor_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_minor_move, gauge_indicator_line_minor_thickness, gauge_indicator_line_minor_length)
                ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
            ctx.fill()

            ctx.restore()

            # Draw percentage numbers on the right side if angle value is power of 20 ("gauge_indicator_text_correction" is a correction number for aligning the texts).
            if angle % 20 == 0:
                ctx.save()
                ctx.translate((gauge_circular_center_x)-gauge_indicator_text_correction, (chart_height / 2)+gauge_indicator_text_correction)
                angle1 = ((i*15)+15)*pi_number/180
                ctx.move_to((gauge_indicator_text_radius-gauge_indicator_text_move)*sin(angle1), (gauge_indicator_text_radius-gauge_indicator_text_move)*cos(angle1))
                ctx.set_font_size(gauge_indicator_text_size)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                ctx.show_text(f'{angle}')
                ctx.restore()


        # Draw vertical separator line on the center of the inner circle of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.move_to(0, -gauge_separator_line_vertical_center_length / 2)
        ctx.rel_line_to(0, gauge_separator_line_vertical_center_length)
        ctx.set_line_width(gauge_separator_thickness)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()

        # Draw vertical separator line on the center of the outer circle of the circular gauge (upper side).
        ctx.move_to(0, -gauge_separator_line_vertical_upper_start)
        ctx.rel_line_to(0, gauge_separator_line_vertical_upper_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()

        # Draw vertical separator line on the center of the outer circle of the circular gauge (lower side).
        ctx.move_to(0, gauge_separator_line_vertical_lower_start)
        ctx.rel_line_to(0, gauge_separator_line_vertical_lower_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()


        # Draw "CPU" label on the upper-left side of the inner circle of the circular gauge.
        cpu_text = _tr("CPU")
        ctx.set_font_size(gauge_indicator_text_size)
        text_extends = ctx.text_extents(cpu_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(cpu_text)

        # Draw "RAM" label on the upper-right side of the inner circle of the circular gauge.
        ram_text = _tr("RAM")
        ctx.set_font_size(gauge_indicator_text_size)
        text_extends = ctx.text_extents(ram_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(ram_text)

        # Draw "Processes" label on the lower-left side of the inner circle of the circular gauge.
        processes_text = _tr("Processes")
        ctx.set_font_size(gauge_processes_swap_label_text_size)
        if len(processes_text) > 9:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        text_extends = ctx.text_extents(processes_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(processes_text)

        # Draw "Swap" label on the upper-right side of the inner circle of the circular gauge.
        ram_text = _tr("Swap")
        ctx.set_font_size(gauge_processes_swap_label_text_size)
        if len(ram_text) > 9:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        text_extends = ctx.text_extents(ram_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(ram_text)


        # Draw "%" labels below the CPU and RAM percentages on the inner circle of the circular gauge.
        percentage_text = "%"
        ctx.set_font_size(gauge_percentage_label_text_below_cpu_ram_size)
        text_extends = ctx.text_extents(percentage_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_percentage_label_text_below_cpu_ram_move)
        ctx.set_source_rgba(180/255, 180/255, 180/255, 1.0)
        ctx.show_text(percentage_text)
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_percentage_label_text_below_cpu_ram_move)
        ctx.set_source_rgba(180/255, 180/255, 180/255, 1.0)
        ctx.show_text(percentage_text)


        # Draw lowest layer of the shadow of the CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        text_extends = ctx.text_extents(cpu_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move + 2 * gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(cpu_usage_text)

        # Draw shadow of the CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move + gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(cpu_usage_text)

        # Draw CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(cpu_usage_text)

        # Draw lowest layer of the shadow of the RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        text_extends = ctx.text_extents(ram_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move + 2 * gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(ram_usage_text)

        # Draw shadow of the RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move + gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(ram_usage_text)

        # Draw RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(ram_usage_text)

        # Draw lowest layer of the shadow of the Processes label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        text_extends = ctx.text_extents(processes_number_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move + 2 * gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(processes_number_text)

        # Draw shadow of the Processes label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move + gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(processes_number_text)

        # Draw Processes label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(processes_number_text)

        # Draw lowest layer of the shadow of the Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        text_extends = ctx.text_extents(swap_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move + 2 * gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(swap_usage_text)

        # Draw shadow of the Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move + gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(swap_usage_text)

        # Draw Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(swap_usage_text)

        # Reset translating.
        ctx.restore()
        ctx.move_to(0, 0)
        ctx.stroke()


        # Draw CPU usage indicator.
        cpu_usage_angle = Performance.cpu_usage_percent_ave[-1] / 10
        start_angle = ((0*15)+105)*pi_number/180
        end_angle = ((cpu_usage_angle*15)+105)*pi_number/180

        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.arc_negative(0, 0, gauge_outer_radius*0.86, end_angle, start_angle)
        ctx.arc(0, 0, gauge_inner_radius, start_angle, end_angle)
        gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius, 0, 0, gauge_outer_radius*0.86)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 0)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 0.5)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 1)
        gradient_pattern.add_color_stop_rgba(1, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw RAM usage indicator.
        ram_usage_angle = Performance.ram_usage_percent[-1] / 10
        end_angle = (75-(0*15))*pi_number/180
        start_angle = (75-(ram_usage_angle*15))*pi_number/180

        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.arc_negative(0, 0, gauge_outer_radius*0.86, end_angle, start_angle)
        ctx.arc(0, 0, gauge_inner_radius, start_angle, end_angle)
        gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius, 0, 0, gauge_outer_radius*0.86)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 0)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 0.5)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 1)
        gradient_pattern.add_color_stop_rgba(1, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw "Read Speed" label on the upper-left side of the inner circle of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        read_speed_text = _tr("Read Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        text_length = len(read_speed_text)
        if text_length > 16 and text_length < 20:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        elif text_length >= 20:
            ctx.set_font_size(gauge_indicator_text_size_smallest)
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(read_speed_text)

        # Draw "Write Speed" label on the upper-left side of the inner circle of the circular gauge.
        write_speed_text = _tr("Write Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        text_length = len(write_speed_text)
        if text_length > 16 and text_length < 20:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        elif text_length >= 20:
            ctx.set_font_size(gauge_indicator_text_size_smallest)
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(write_speed_text)

        # Draw "Download Speed" label on the upper-left side of the inner circle of the circular gauge.
        download_speed_text = _tr("Download Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        text_length = len(download_speed_text)
        if text_length > 16 and text_length < 20:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        elif text_length >= 20:
            ctx.set_font_size(gauge_indicator_text_size_smallest)
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(download_speed_text)

        # Draw "Upload Speed" label on the upper-left side of the inner circle of the circular gauge.
        upload_speed_text = _tr("Upload Speed")
        ctx.set_font_size(gauge_disk_network_label_text_size)
        text_length = len(upload_speed_text)
        if text_length > 16 and text_length < 20:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        elif text_length >= 20:
            ctx.set_font_size(gauge_indicator_text_size_smallest)
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(upload_speed_text)


        # Draw lowest layer of the shadow of the Disk Read Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(disk_read_speed_text)

        # Draw shadow of the Disk Read Speed label on the right gauge.
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_read_speed_text)

        # Draw Disk Read Speed label on the right gauge.
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_read_speed_text)

        # Draw lowest layer of the shadow of the Disk Write Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(disk_write_speed_text)

        # Draw shadow of the Disk Write Speed label on the right gauge.
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_write_speed_text)

        # Draw Disk Write Speed label on the right gauge.
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_write_speed_text)

        # Draw lowest layer of the shadow of the Network Download Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(network_download_speed_text)

        # Draw shadow of the Network Download Speed label on the right gauge.
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_download_speed_text)

        # Draw Network Download Speed label on the right gauge.
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_download_speed_text)

        # Draw lowest layer of the shadow of the Network Upload Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(network_upload_speed_text)

        # Draw shadow of the Network Upload Speed label on the right gauge.
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_upload_speed_text)

        # Draw Network Upload Speed label on the right gauge.
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_upload_speed_text)

        ctx.restore()


Summary = Summary()

