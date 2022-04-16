#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Gpu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuTab.ui")

        # Get GUI objects
        self.grid1501 = builder.get_object('grid1501')
        self.drawingarea1501 = builder.get_object('drawingarea1501')
        self.button1501 = builder.get_object('button1501')
        self.label1501 = builder.get_object('label1501')
        self.label1502 = builder.get_object('label1502')
        self.label1503 = builder.get_object('label1503')
        self.label1504 = builder.get_object('label1504')
        self.label1505 = builder.get_object('label1505')
        self.label1506 = builder.get_object('label1506')
        self.label1507 = builder.get_object('label1507')
        self.label1508 = builder.get_object('label1508')
        self.label1509 = builder.get_object('label1509')
        self.label1510 = builder.get_object('label1510')
        self.label1511 = builder.get_object('label1511')
        self.label1512 = builder.get_object('label1512')
        self.label1513 = builder.get_object('label1513')
        self.glarea1501 = builder.get_object('glarea1501')

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_line_charts_draw_func = Performance.performance_line_charts_draw_func
        self.performance_line_charts_enter_notify_event_func = Performance.performance_line_charts_enter_notify_event_func
        self.performance_line_charts_leave_notify_event_func = Performance.performance_line_charts_leave_notify_event_func
        self.performance_line_charts_motion_notify_event_func = Performance.performance_line_charts_motion_notify_event_func

        # Connect GUI signals
        self.button1501.connect("clicked", self.on_button1501_clicked)
        self.drawingarea1501.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea1501.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea1501.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea1501.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)
        self.glarea1501.connect('realize', self.on_glarea1501_realize)
        self.glarea1501.connect('render', self.on_glarea1501_render)

        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea1501.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1501_clicked(self, widget):

        # Get gpu/graphics card list and set selected gpu
        self.gpu_get_gpu_list_and_set_selected_gpu_func()

        # Open customizations menu
        from GpuMenu import GpuMenu
        GpuMenu.popover1501p.set_relative_to(widget)
        GpuMenu.popover1501p.set_position(1)
        GpuMenu.popover1501p.popup()


    # ----------------------- Called for measuring FPS -----------------------
    def on_glarea1501_realize(self, widget):

        widget.make_current()
        if (widget.get_error() != None):
          return


    # ----------------------- Called for drawing OpenGL graphics for measuring FPS (Rendering is performed by using glarea in order to measure FPS. FPS on drawing area is counted. Lower FPS is obtained depending on the GPU load/performance.) -----------------------
    def on_glarea1501_render(self, widget, ctx):

        try:
            self.frame_list.append(0)
        except AttributeError:
            return
        # "queue_draw()" is used in order to obtain higher FPS if screen refresh rate is not reached. Otherwise it draws a few frames.
        widget.queue_draw()
        return True


    # ----------------------------------- GPU - Initial Function -----------------------------------
    def gpu_initial_func(self):

        # Define initial values
        self.fps_count = [0] * Config.chart_data_history
        self.frame_latency = 0
        self.frame_list = []

        # Get GPU information by using a function.
        # Get gpu/graphics card list and set selected gpu
        self.gpu_get_gpu_list_and_set_selected_gpu_func()

        # Fill GPU information lists with "-" values for all GPUs. These informations will be get from driver (for example: glxinfo). Values of some GPUs will be left as "-" if information of these GPUs can not be get from drivers.
        number_of_gpus = len(self.gpu_vendor_id_list)
        self.gpu_vendor_name_in_driver_list = ["-"] * number_of_gpus
        self.gpu_device_name_in_driver_list = ["-"] * number_of_gpus
        self.video_memory_list = ["-"] * number_of_gpus
        self.if_unified_memory_list = ["-"] * number_of_gpus
        self.direct_rendering_list = ["-"] * number_of_gpus
        self.opengl_version_list = ["-"] * number_of_gpus
        self.display_driver_list = ["-"] * number_of_gpus

        # Get video_memory, if_unified_memory, direct_rendering, opengl_version values of the GPU which is preferred for running this application. "DRI_PRIME=0 application-name" and "DRI_PRIME=1 application-name" could be used for running an application by using internal and external GPUs respectively.
        # "env" command is used for running a program in a modified environment. "DRI_PRIME=1 application_name" does not work when "(subprocess.check_output(command, shell=False))" is used in order to prevent shell injection. "DRI_PRIME=1" is environment variable name, it is not an application/package name.
        glxinfo_for_integrated_gpu = ["env", "DRI_PRIME=0", "glxinfo", "-B"]
        glxinfo_for_discrete_gpu = ["env", "DRI_PRIME=1", "glxinfo", "-B"]
        try:
            glxinfo_output_integrated_gpu = (subprocess.check_output(glxinfo_for_integrated_gpu, shell=False)).decode().strip()
        except Exception:
            glxinfo_output_integrated_gpu = ""
        try:
            glxinfo_output_discrete_gpu = (subprocess.check_output(glxinfo_for_discrete_gpu, shell=False)).decode().strip()
        except Exception:
            glxinfo_output_discrete_gpu = ""
        if "libGL error: failed to create dri screen" in glxinfo_output_discrete_gpu or "libGL error: failed to load driver:" in glxinfo_output_discrete_gpu:    # "libGL error: failed to create dri screen\nlibGL error: failed to load driver: nouveau" information may be printed when DRI_PRIME=1 glxinfo -B" command is used if closed sourced driver and GPU configurations are used for NVIDIA cards. Same output contains information of integrated GPU.
            glxinfo_output_discrete_gpu = "-"
        glxinfo_output_integrated_gpu_lines = glxinfo_output_integrated_gpu.split("\n")
        glxinfo_output_discrete_gpu_lines = glxinfo_output_discrete_gpu.split("\n")
        # Check GPU/driver configuration to be able to get GPU/Graphics Card information from drive without wrong information.
        # INFORMATION ABOUT GPU/DRIVER CONFIGURATIONS:
        # "Extended renderer info (GLX_MESA_query_renderer):" information exists in the output of "glxinfo" command if open sourced driver of GPU is used.
        # "Extended renderer info (GL_NVX_gpu_memory_info):" information exists in the output of "glxinfo" command if closed sourced driver of GPU is used. Both "Extended renderer info (GLX_MESA_query_renderer):" and "Extended renderer info (GLX_MESA_query_renderer):" informations are printed if open sourced driver is used for AMD GPUs.
        # "Extended renderer info (GLX_MESA_query_renderer):" information may not exist and "OpenGL vendor string:" may exist in the output of "glxinfo" command if closed sourced driver is used for some ARM devices (such as Nvidia Tegra devices).
        # Vendor and device id numbers (0x[id number]) are not printed in closed sourced drivers. Vendor and device IDs can be get from vendor and device files in "/sys/class/drm/card[card number]/device/" directories.
        # But IDs from these folders and IDs from drivers can not be matched when closed sourced drivers are used for the selected GPU.
        # IDs matching can be performed if there is 1 GPU on the system (with open or closed sourced drivers), if there are 2 GPUs (with both open sourced driver or 1 open sourced and 1 closed source driver) on the system.
        # IDs may be "0xffffffff" for vendor and device on virtual machines. ID matching is performed on these systems because there is 1 GPU on these systems (default configuration).
        # "libGL error: failed to create dri screen\nlibGL error: failed to load driver: nouveau" lines may be printed if closed sourced drivers are used and some GPU configurations are made on some systems. For example some Asus ROG notebooks with "asusctl" utility.
        # "prime-run" for NVIDIA GPUs and "progl" for AMD GPUs are used for running applications with discrete GPU if "DRI_PRIME=1" does not work on systems with closed sourced GPU drivers. Usage: "prime-run glxinfo -B", "progl glxinfo -B".
        # But "prime-run" may not work on some systems (for example some Asus ROG notebooks with "asusctl" utility). More information is needed to know if same situation is valid for "progl".
        if number_of_gpus == 1:
            if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_integrated_gpu):
                self.gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "open_sourced")
            if ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_integrated_gpu) and ("Extended renderer info (GL_NVX_gpu_memory_info):" in glxinfo_output_integrated_gpu):
                self.gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "closed_sourced")
            if ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_integrated_gpu) and ("OpenGL vendor string:" in glxinfo_output_integrated_gpu):
                self.gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "closed_sourced")
        if number_of_gpus >= 2:
            if glxinfo_output_integrated_gpu != glxinfo_output_discrete_gpu:
                if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_integrated_gpu):
                    self.gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "check", "open_sourced")
                if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_discrete_gpu):
                    self.gpu_get_information_from_driver_func(glxinfo_output_discrete_gpu_lines, "check", "open_sourced")
                if number_of_gpus == 2:
                    if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_integrated_gpu) and ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_discrete_gpu):
                        self.gpu_get_information_from_driver_func(glxinfo_output_discrete_gpu_lines, "no_check", "closed_sourced")
                    if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_discrete_gpu) and ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_integrated_gpu):
                        self.gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "closed_sourced")

        # Get if_default_gpu value
        # Set default GPU if there is only 1 GPU on the system and these is not "boot_vga" file (on some systems such as ARM devices) which means default_gpu = "".
        if len(self.gpu_list) == 1:
            if_default_gpu = _tr("Yes")
        else:
            if self.gpu_list[self.selected_gpu_number] == self.default_gpu:
                if_default_gpu = _tr("Yes")
            else:
                if_default_gpu = _tr("No")


        # Set GPU tab label texts by using information get
        self.label1501.set_text(self.gpu_device_model_name[self.selected_gpu_number])
        self.label1502.set_text(f'{self.gpu_list[self.selected_gpu_number]} ({self.gpu_vendor_name_in_driver_list[self.selected_gpu_number]} - {self.gpu_device_name_in_driver_list[self.selected_gpu_number]})')
        self.label1507.set_text(if_default_gpu)
        self.label1508.set_text(self.video_memory_list[self.selected_gpu_number])
        self.label1509.set_text(self.if_unified_memory_list[self.selected_gpu_number])
        self.label1510.set_text(self.direct_rendering_list[self.selected_gpu_number])
        self.label1511.set_text(self.display_driver_list[self.selected_gpu_number])
        self.label1512.set_text(self.opengl_version_list[self.selected_gpu_number])

        self.initial_already_run = 1


    # ----------------------------------- GPU - Get GPU Data Function -----------------------------------
    def gpu_loop_func(self):

        fps = len(self.frame_list) / Config.update_interval
        del self.fps_count[0]
        self.fps_count.append(fps)
        # Frame latency in milliseconds
        self.frame_latency = 1 / (fps + 0.0000001) * 1000
        self.frame_list = []

        self.drawingarea1501.queue_draw()


        # Get information.
        current_resolution, current_refresh_rate = self.gpu_resolution_refresh_rate_func()


        # Set and update GPU tab label texts by using information get
        self.label1503.set_text(f'{self.fps_count[-1]:.0f}')
        self.label1504.set_text(f'{self.frame_latency:.1f} ms')
        self.label1505.set_text(current_refresh_rate)
        self.label1506.set_text(f'{current_resolution}')


    # ----------------------------------- GPU - Get Information From Driver Function -----------------------------------
    def gpu_get_information_from_driver_func(self, output_to_search_gpu_information_from_driver, check_vendor_device_id_match, check_driver_open_sourced):

        # Define initial values of the variables. These values will be used if values can not be get.
        gpu_vendor_id_in_driver = "-"
        gpu_device_id_in_driver = "-"
        gpu_vendor_name_in_driver = "-"
        gpu_device_name_in_driver = "-"
        video_memory = "-"
        if_unified_memory = "-"
        direct_rendering = "-"
        opengl_version = "-"
        display_driver = "-"
        # Get GPU/Graphic Card information
        if check_driver_open_sourced == "open_sourced":
            for line in output_to_search_gpu_information_from_driver:
                if line.strip().startswith("Vendor:"):
                    gpu_vendor_id_in_driver = line.split()[-1].strip("()").split("x")[1].strip()
                if line.strip().startswith("Device:"):
                    gpu_device_id_in_driver = line.split()[-1].strip("()").split("x")[1].strip()
        number_of_gpus = len(self.gpu_vendor_id_list)
        for i in range(number_of_gpus):
            # Check if GPU from the "glxinfo" command and GPU from "/sys/class/drm/card[number]/device/device" file are same. Outputs from "DRI_PRIME=0 glxinfo -B" and "DRI_PRIME=1 glxinfo -B" commands may be reversed sometimes (very rare). ".lstrip("0")" is used in order to remove "0" (if exists) at the beginning at the device id. Checking GPU vendor and device id match between "/sys/class/drm/card[number]/device/..." files and driver is skipped if "check_vendor_device_id_match" value is "check". This check is not performed if there is only 1 GPU/Graphics Card on the system.
            if gpu_vendor_id_in_driver != self.gpu_vendor_id_list[i] and gpu_device_id_in_driver != self.gpu_device_id_list[i].lstrip("0") and check_vendor_device_id_match == "check":
                continue
            for line in output_to_search_gpu_information_from_driver:
                if line.strip().startswith("OpenGL vendor string:"):
                    gpu_vendor_name_in_driver = line.split(":")[1].strip()
                    continue
                if line.strip().startswith("OpenGL renderer string:"):
                    gpu_device_name_in_driver = line.split(":")[1].strip()
                    continue
                if check_driver_open_sourced == "open_sourced":
                    if line.strip().startswith("Video memory:"):
                        video_memory = line.split(":")[1].strip()
                        continue
                    if line.strip().startswith("Unified memory:"):
                        if_unified_memory = _tr(line.split(":")[1].strip().capitalize())
                        continue
                if check_driver_open_sourced == "closed_sourced":
                    if line.strip().startswith("Dedicated video memory:"):
                        video_memory = line.split(":")[1].strip()
                        if_unified_memory = _tr("No")
                        continue
                if line.strip().startswith("direct rendering:"):
                    direct_rendering = _tr(line.split(":")[1].strip())
                    continue
                if line.strip().startswith("OpenGL version string:"):
                    opengl_version, display_driver = line.split(":")[1].strip().split(" ", 1)
                    continue
            # Replace "-" values in the list with the values which are get from "glxinfo" output. Information of the selected GPU will be get from this list by using "selected_gpu_number" value. To be able to match GPU information from "/sys/class/drm/card[number]" and GPU information from "glxinfo" command are used. None of these informations contain the information of "integrated/discrete GPU". This matching is performed by using vendor and device ids.
            self.gpu_vendor_name_in_driver_list[i] = gpu_vendor_name_in_driver
            self.gpu_device_name_in_driver_list[i] = gpu_device_name_in_driver
            self.video_memory_list[i] = video_memory
            self.if_unified_memory_list[i] = if_unified_memory
            self.direct_rendering_list[i] = direct_rendering
            self.opengl_version_list[i] = opengl_version
            self.display_driver_list[i] = display_driver


    # ----------------------------------- GPU - Set Selected GPU/Graphics Card Function -----------------------------------
    def gpu_get_gpu_list_and_set_selected_gpu_func(self):

        self.gpu_device_model_name = []
        self.gpu_vendor_id_list = []
        self.gpu_device_id_list = []
        # Initial value of "default_gpu" variable.
        self.default_gpu = ""

        # Get GPU list from "/sys/class/drm/" directory which is used by many x86_64 desktop systems.
        try:
            self.gpu_list = [gpu_name for gpu_name in os.listdir("/dev/dri/") if gpu_name.rstrip("0123456789") == "card"]
            gpu_card_directory = "/sys/class/drm/"
            gpu_card_directory_sub = "/device/"
        # Try to get GPU list from "/sys/devices/" folder which is used by some ARM systems.
        except FileNotFoundError:
            self.gpu_list = [gpu_name for gpu_name in os.listdir("/sys/devices/") if gpu_name.split(".")[0] == "gpu"]
            gpu_card_directory = "/sys/devices/"
            gpu_card_directory_sub = "/"
        for gpu in self.gpu_list:
            try:
                with open(gpu_card_directory + gpu + gpu_card_directory_sub + "boot_vga") as reader:
                    if reader.read().strip() == "1":
                        self.default_gpu = gpu
            except FileNotFoundError:
                pass
            # Read device vendor and model ids by reading "modalias" file.
            with open(gpu_card_directory + gpu + gpu_card_directory_sub + "modalias") as reader:
                modalias_output = reader.read().strip()
            # Determine device subtype.
            device_subtype, device_alias = modalias_output.split(":", 1)
            device_vendor_name, device_model_name, device_vendor_id, device_model_id = Performance.performance_get_device_vendor_model_func(modalias_output)
            if device_vendor_name == "Unknown":
                device_vendor_name = "[" + _tr("Unknown") + "]"
            if device_model_name == "Unknown":
                device_model_name = "[" + _tr("Unknown") + "]"
            self.gpu_device_model_name.append(f'{device_vendor_name} - {device_model_name}')
            # These lists will be used for matching with GPU information from "glxinfo" command. First "v" or "d" and zeros trimmed by using ".lstrip("d0")".
            self.gpu_vendor_id_list.append(device_vendor_id.lstrip("v0").lower())
            self.gpu_device_id_list.append(device_model_id.lstrip("d0").lower())

        # Set selected gpu/graphics card
        # "" is predefined gpu name before release of the software. This statement is used in order to avoid error, if no gpu selection is made since first run of the software.
        if Config.selected_gpu == "":
            if self.default_gpu != "":
                set_selected_gpu = self.default_gpu
            if self.default_gpu == "":
                set_selected_gpu = self.gpu_list[0]
        if Config.selected_gpu in self.gpu_list:
            set_selected_gpu = Config.selected_gpu
        else:
            if self.default_gpu != "":
                set_selected_gpu = self.default_gpu
            if self.default_gpu == "":
                set_selected_gpu = self.gpu_list[0]
        self.selected_gpu_number = self.gpu_list.index(set_selected_gpu)


    # ----------------------- Get screen resolution and refresh rate -----------------------
    def gpu_resolution_refresh_rate_func(self):

        # Get current resolution
        current_screen = Gdk.Screen.get_default()
        current_resolution = str(current_screen.get_width()) + "x" + str(current_screen.get_height())

        # Get current refresh rate
        try:
            current_monitor_number = current_screen.get_monitor_at_window(current_screen.get_active_window())
            current_display = Gdk.Display.get_default()
            current_refresh_rate = current_display.get_monitor(current_monitor_number).get_refresh_rate()
            current_refresh_rate = int(current_refresh_rate) / 1000
        except Exception:
            current_refresh_rate = "Unknown"
        # If refresh rate is not get or it is smaller than 30 (incorrect values such as 1, 2.14 are get on some systems such as RB-Pi devices), get it by using xrandr (if there is only one monitor connected).
        if current_refresh_rate == "Unknown" or current_refresh_rate < 30:
            try:
                xrandr_output = (subprocess.check_output(["xrandr"], shell=False)).decode().strip()
                xrandr_output_lines = xrandr_output.split("\n")
                number_of_monitors = xrandr_output.count(" connected")
                if number_of_monitors == 1:
                    for line in xrandr_output_lines:
                        if "*" in line:
                            line_split = line.split()
                            for string_in_line in line_split:
                                if "*" in string_in_line:
                                    current_refresh_rate = float(string_in_line.strip().rstrip("*+"))
                                    break
            except Exception:
                pass
        if current_refresh_rate != "Unknown":
            current_refresh_rate = f'{current_refresh_rate:.2f} Hz'
        else:
            current_refresh_rate = f'[{_tr("Unknown")}]'

        return current_resolution, current_refresh_rate


# Generate object
Gpu = Gpu()

