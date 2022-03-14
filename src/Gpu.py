#!/usr/bin/env python3

# ----------------------------------- GPU - GPU Tab Import Function -----------------------------------
def gpu_import_func():

    global Gtk, GLib, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gtk, GLib, Gdk
    import os
    import subprocess


    global Config, Performance
    import Config, Performance


    global _tr
    from locale import gettext as _tr


# ----------------------------------- GPU - GPU GUI Function -----------------------------------
def gpu_gui_func():

    # GPU tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuTab.ui")

    # GPU tab GUI objects
    global grid1501, drawingarea1501, button1501, label1501, label1502
    global label1503, label1504, label1505, label1506, label1507, label1508, label1509, label1510, label1511, label1512, label1513
    global glarea1501

    # GPU tab GUI objects - get
    grid1501 = builder.get_object('grid1501')
    drawingarea1501 = builder.get_object('drawingarea1501')
    button1501 = builder.get_object('button1501')
    label1501 = builder.get_object('label1501')
    label1502 = builder.get_object('label1502')
    label1503 = builder.get_object('label1503')
    label1504 = builder.get_object('label1504')
    label1505 = builder.get_object('label1505')
    label1506 = builder.get_object('label1506')
    label1507 = builder.get_object('label1507')
    label1508 = builder.get_object('label1508')
    label1509 = builder.get_object('label1509')
    label1510 = builder.get_object('label1510')
    label1511 = builder.get_object('label1511')
    label1512 = builder.get_object('label1512')
    label1513 = builder.get_object('label1513')
    glarea1501 = builder.get_object('glarea1501')


    # GPU tab GUI functions
    def on_button1501_clicked(widget):
        gpu_get_gpu_list_and_set_selected_gpu_func()                                          # Get gpu/graphics card list and set selected gpu
        if 'GpuMenu' not in globals():
            global GpuMenu
            import GpuMenu
            GpuMenu.gpu_menus_import_func()
            GpuMenu.gpu_menus_gui_func()
            GpuMenu.popover1501p.set_relative_to(button1501)
            GpuMenu.popover1501p.set_position(1)
        GpuMenu.popover1501p.popup()


    # ----------------------------------- GPU - Plot FPS data as a Line Chart ----------------------------------- 
    def on_drawingarea1501_draw(widget, ctx):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        try:                                                                                  # "try-except" is used in order to handle errors because chart signals are connected before running relevant performance thread (in the GPU module) to be able to use GUI labels in this thread. Chart could not get any performance data before running of the relevant performance thread.
            fps_count_check = fps_count
        except NameError:
            return

        chart_line_color = Config.chart_line_color_fps
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

        chart1501_width = Gtk.Widget.get_allocated_width(widget)
        chart1501_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart1501_width, chart1501_height)
        ctx.fill()

        ctx.set_line_width(1)
        ctx.set_dash([4, 3])
        ctx.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        for i in range(3):
            ctx.move_to(0, chart1501_height/4*(i+1))
            ctx.line_to(chart1501_width, chart1501_height/4*(i+1))
        for i in range(4):
            ctx.move_to(chart1501_width/5*(i+1), 0)
            ctx.line_to(chart1501_width/5*(i+1), chart1501_height)
        ctx.stroke()

        chart1501_y_limit = 1.1 * (max(fps_count) + 0.0000001)                                # Maximum FPS value is multiplied by 1.1 in order to scale chart when FPS is increased or decreased for preventing the line being out of the chart border.

        # ---------- Start - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------
        chart1501_y_limit_float = chart1501_y_limit
        number_of_digits = len(str(int(chart1501_y_limit)))
        multiple = 10 ** (number_of_digits - 1)
        number_to_get_next_multiple = chart1501_y_limit_float + (multiple - 0.0001)
        next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
        label1513.set_text(f'{next_multiple} FPS')
        chart1501_y_limit = (chart1501_y_limit * next_multiple / (chart1501_y_limit_float + 0.0000001) + 0.0000001)
        # ---------- End - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------

        ctx.set_dash([], 0)
        ctx.rectangle(0, 0, chart1501_width, chart1501_height)
        ctx.stroke()

        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        ctx.move_to(chart1501_width*chart_x_axis[0]/(chart_data_history-1), chart1501_height - chart1501_height*fps_count[0]/chart1501_y_limit)
        for i in range(len(chart_x_axis) - 1):
            delta_x_chart1501 = (chart1501_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1501_width * chart_x_axis[i]/(chart_data_history-1))
            delta_y_chart1501 = (chart1501_height*fps_count[i+1]/chart1501_y_limit) - (chart1501_height*fps_count[i]/chart1501_y_limit)
            ctx.rel_line_to(delta_x_chart1501, -delta_y_chart1501)

        ctx.rel_line_to(10, 0)
        ctx.rel_line_to(0, chart1501_height+10)
        ctx.rel_line_to(-(chart1501_width+20), 0)
        ctx.rel_line_to(0, -(chart1501_height+10))
        ctx.close_path()
        ctx.stroke_preserve()
        ctx.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        ctx.fill()


    # ----------------------------------- GPU - Used for measuring FPS ----------------------------------- 
    def on_glarea1501_realize(widget):

        widget.make_current()
        if (widget.get_error() != None):
          return


    # ----------------------------------- GPU - Plot OpenGL graphics for measuring FPS (Rendering is performed by using glarea in order to measure FPS. FPS on drawing area is counted. Lower FPS is obtained depending on the GPU load/performance.) ----------------------------------- 
    def on_glarea1501_render(widget, ctx):

        global frame_list
        try:
            frame_list.append(0)
        except NameError:
            return
        widget.queue_draw()                                                               # "queue_draw()" is used in order to obtain higher FPS if screen refresh rate is not reached.
        return True


    # GPU tab GUI functions - connect
    button1501.connect("clicked", on_button1501_clicked)
    drawingarea1501.connect("draw", on_drawingarea1501_draw)
    glarea1501.connect('realize', on_glarea1501_realize)
    glarea1501.connect('render', on_glarea1501_render)


# ----------------------------------- GPU - Initial Function -----------------------------------
def gpu_initial_func():

    # Define initial values
    global fps_count, frame_latency, frame_list
    fps_count = [0] * Config.chart_data_history
    frame_latency = 0
    frame_list = []

    # Get GPU information by using a function.
    gpu_get_gpu_list_and_set_selected_gpu_func()                                              # Get gpu/graphics card list and set selected gpu
    global gpu_vendor_id_list, gpu_device_id_list, selected_gpu_number, gpu_list, default_gpu, gpu_device_model_name

    # Fill GPU information lists with "-" values for all GPUs. These informations will be get from driver (for example: glxinfo). Values of some GPUs will be left as "-" if information of these GPUs can not be get from drivers.
    global gpu_vendor_name_in_driver_list, gpu_device_name_in_driver_list, video_memory_list, if_unified_memory_list, direct_rendering_list, opengl_version_list, display_driver_list
    gpu_vendor_name_in_driver_list = ["-"] * len(gpu_vendor_id_list)
    gpu_device_name_in_driver_list = ["-"] * len(gpu_vendor_id_list)
    video_memory_list = ["-"] * len(gpu_vendor_id_list)
    if_unified_memory_list = ["-"] * len(gpu_vendor_id_list)
    direct_rendering_list = ["-"] * len(gpu_vendor_id_list)
    opengl_version_list = ["-"] * len(gpu_vendor_id_list)
    display_driver_list = ["-"] * len(gpu_vendor_id_list)

    # Get video_memory, if_unified_memory, direct_rendering, opengl_version values of the GPU which is preferred for running this application. "DRI_PRIME=0 application-name" and "DRI_PRIME=1 application-name" could be used for running an application by using internal and external GPUs respectively.
    glxinfo_for_integrated_gpu = ["env", "DRI_PRIME=0", "glxinfo", "-B"]                      # "env" command is used for running a program in a modified environment. "DRI_PRIME=1 application_name" does not work when "(subprocess.check_output(command, shell=False))" is used in order to prevent shell injection. "DRI_PRIME=1" is environment variable name, it is not an application/package name.
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
    # Vendor and device id numbers (0x[id number]) are not printed in closed sourced drivers. Vendor and device IDs can be get from vendor and device files in "/sys/class/drm/card[card number]/device/" directories.
    # But IDs from these folders and IDs from drivers can not be matched when closed sourced drivers are used for the selected GPU.
    # IDs matching can be performed if there is 1 GPU on the system (with open or closed sourced drivers), if there are 2 GPUs (with both open sourced driver or 1 open sourced and 1 closed source driver) on the system.
    # IDs may be "0xffffffff" for vendor and device on virtual machines. ID matching is performed on these systems because there is 1 GPU on these systems (default configuration).
    # "libGL error: failed to create dri screen\nlibGL error: failed to load driver: nouveau" lines may be printed if closed sourced drivers are used and some GPU configurations are made on some systems. For example some Asus ROG notebooks with "asusctl" utility.
    # "prime-run" for NVIDIA GPUs and "progl" for AMD GPUs are used for running applications with discrete GPU if "DRI_PRIME=1" does not work on systems with closed sourced GPU drivers. Usage: "prime-run glxinfo -B", "progl glxinfo -B".
    # But "prime-run" may not work on some systems (for example some Asus ROG notebooks with "asusctl" utility). More information is needed to know if same situation is valid for "progl".
    if len(gpu_vendor_id_list) == 1:
        if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_integrated_gpu):
            gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "open_sourced")
        if len(gpu_vendor_id_list) == 1 and ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_integrated_gpu) and ("Extended renderer info (GL_NVX_gpu_memory_info):" in glxinfo_output_integrated_gpu):
            gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "closed_sourced")
    if len(gpu_vendor_id_list) >= 2:
        if glxinfo_output_integrated_gpu != glxinfo_output_discrete_gpu:
            if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_integrated_gpu):
                gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "check", "open_sourced")
            if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_discrete_gpu):
                gpu_get_information_from_driver_func(glxinfo_output_discrete_gpu_lines, "check", "open_sourced")
            if len(gpu_vendor_id_list) == 2:
                if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_integrated_gpu) and ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_discrete_gpu):
                    gpu_get_information_from_driver_func(glxinfo_output_discrete_gpu_lines, "no_check", "closed_sourced")
                if ("Extended renderer info (GLX_MESA_query_renderer):" in glxinfo_output_discrete_gpu) and ("Extended renderer info (GLX_MESA_query_renderer):" not in glxinfo_output_integrated_gpu):
                    gpu_get_information_from_driver_func(glxinfo_output_integrated_gpu_lines, "no_check", "closed_sourced")

    # Get if_default_gpu value
    if gpu_list[selected_gpu_number] == default_gpu:
        if_default_gpu = _tr("Yes")
    if gpu_list[selected_gpu_number] != default_gpu:
        if_default_gpu = _tr("No")

    # Set GPU tab label texts by using information get
    label1501.set_text(gpu_device_model_name[selected_gpu_number])
    label1502.set_text(f'{gpu_list[selected_gpu_number]} ({gpu_vendor_name_in_driver_list[selected_gpu_number]} - {gpu_device_name_in_driver_list[selected_gpu_number]})')
    label1507.set_text(if_default_gpu)
    label1508.set_text(video_memory_list[selected_gpu_number])
    label1509.set_text(if_unified_memory_list[selected_gpu_number])
    label1510.set_text(direct_rendering_list[selected_gpu_number])
    label1511.set_text(display_driver_list[selected_gpu_number])
    label1512.set_text(opengl_version_list[selected_gpu_number])


# ----------------------------------- GPU - Get GPU Data Function -----------------------------------
def gpu_loop_func():

    global frame_list, fps_count, fps_count_list, frame_latency
    #glarea1501.queue_draw()
    fps = len(frame_list) / update_interval
    del fps_count[0]
    fps_count.append(fps)
    frame_latency = 1 / (fps + 0.0000001) * 1000                                              # Frame latency in milliseconds
    frame_list = []

    drawingarea1501.queue_draw()

    # Get current resolution and current refresh rate
    current_screen = Gdk.Screen.get_default()
    current_resolution = str(current_screen.get_width()) + "x" + str(current_screen.get_height())
    try:
        current_monitor_number = current_screen.get_monitor_at_window(current_screen.get_active_window())
        current_display = Gdk.Display.get_default()
        current_refresh_rate = f'{(current_display.get_monitor(current_monitor_number).get_refresh_rate() / 1000):.2f} Hz'
    except Exception:
        current_refresh_rate = "[" + "Unknown" + "]"


    # Set and update GPU tab label texts by using information get
    label1503.set_text(f'{fps_count[-1]:.0f}')
    label1504.set_text(f'{frame_latency:.1f} ms')
    label1505.set_text(current_refresh_rate)
    label1506.set_text(f'{current_resolution}')


# ----------------------------------- GPU - Get Information From Driver Function -----------------------------------
def gpu_get_information_from_driver_func(output_to_search_gpu_information_from_driver, check_vendor_device_id_match, check_driver_open_sourced):

    # Define initial values of the variables. These values will be used if values can not be get.
    gpu_vendor_in_driver = "-"
    gpu_device_in_driver = "-"
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
    for i in range(len(gpu_vendor_id_list)):
        if gpu_vendor_id_in_driver != gpu_vendor_id_list[i] and gpu_device_id_in_driver != gpu_device_id_list[i].lstrip("0") and check_vendor_device_id_match == "check":    # Check if GPU from the "glxinfo" command and GPU from "/sys/class/drm/card[number]/device/device" file are same. Outputs from "DRI_PRIME=0 glxinfo -B" and "DRI_PRIME=1 glxinfo -B" commands may be reversed sometimes (very rare). ".lstrip("0")" is used in order to remove "0" (if exists) at the beginning at the device id. Checking GPU vendor and device id match between "/sys/class/drm/card[number]/device/..." files and driver is skipped if "check_vendor_device_id_match" value is "check". This check is not performed if there is only 1 GPU/Graphics Card on the system.
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
                    if_unified_memory = _tr(line.split(":")[1].strip().capitalize())          # "_tr()" is used in order to translate ("yes" or "no" values are get from this line) the strings.
                    continue
            if check_driver_open_sourced == "closed_sourced":
                if line.strip().startswith("Dedicated video memory:"):
                    video_memory = line.split(":")[1].strip()
                    if_unified_memory = _tr("No")                                             # "_tr()" is used in order to translate ("yes" or "no" values are get from this line) the strings.
                    continue
            if line.strip().startswith("direct rendering:"):
                direct_rendering = _tr(line.split(":")[1].strip())                            # "_tr()" is used in order to translate ("yes" or "no" values are get from this line) the strings.
                continue
            if line.strip().startswith("OpenGL version string:"):
                opengl_version, display_driver = line.split(":")[1].strip().split(" ", 1)     # "split(" ", 1" is for splitting string by first space character
                continue
        # Replace "-" values in the list with the values which are get from "glxinfo" output. Information of the selected GPU will be get from this list by using "selected_gpu_number" value. To be able to match GPU information from "/sys/class/drm/card[number]" and GPU information from "glxinfo" command are used. None of these informations contain the information of "integrated/discrete GPU". This matching is performed by using vendor and device ids.
        global gpu_vendor_name_in_driver_list, gpu_device_name_in_driver_list, video_memory_list, if_unified_memory_list, direct_rendering_list, opengl_version_list, display_driver_list
        gpu_vendor_name_in_driver_list[i] = gpu_vendor_name_in_driver
        gpu_device_name_in_driver_list[i] = gpu_device_name_in_driver
        video_memory_list[i] = video_memory
        if_unified_memory_list[i] = if_unified_memory
        direct_rendering_list[i] = direct_rendering
        opengl_version_list[i] = opengl_version
        display_driver_list[i] = display_driver


# ----------------------------------- GPU - Run Function -----------------------------------
def gpu_run_func(*args):

    if "update_interval" not in globals():
        GLib.idle_add(gpu_initial_func)
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 4:
        global gpu_glib_source, update_interval
        try:
            gpu_glib_source.destroy()
        except NameError:
            pass
        update_interval = Config.update_interval
        gpu_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(gpu_loop_func)
        gpu_glib_source.set_callback(gpu_run_func)
        gpu_glib_source.attach(GLib.MainContext.default())


# ----------------------------------- GPU - Set Selected GPU/Graphics Card Function -----------------------------------
def gpu_get_gpu_list_and_set_selected_gpu_func():

    global gpu_list, default_gpu, gpu_device_model_name, gpu_vendor_id_list, gpu_device_id_list
    gpu_device_model_name = []
    gpu_vendor_id_list = []
    gpu_device_id_list = []
    default_gpu = ""                                                                          # Initial value of "default_gpu" variable.
    try:
        with open("/usr/share/misc/pci.ids") as reader:                                       # Read "pci.ids" file if it is located in "/usr/share/misc/pci.ids" in order to use it as directory. This directory is used in Debian-like systems.
            pci_ids_output = reader.read()
    except FileNotFoundError:
        with open("/usr/share/hwdata/pci.ids") as reader:                                     # Read "pci.ids" file if it is located in "/usr/share/hwdata/pci.ids" in order to use it as directory. This directory is used in systems other than Debian-like systems.
            pci_ids_output = reader.read()
    gpu_list = [gpu_name for gpu_name in os.listdir("/dev/dri/") if gpu_name.rstrip("0123456789") == "card"]
    for gpu in gpu_list:
        try:
            with open("/sys/class/drm/" + gpu + "/device/boot_vga") as reader:
                if reader.read().strip() == "1":
                    default_gpu = gpu
        except FileNotFoundError:
            pass
        try:                                                                                  # "vendor" and "device" files may not be present on ARM systems even if there is a GPU.
            with open("/sys/class/drm/" + gpu + "/device/vendor") as reader:
                gpu_vendor_id = reader.read().split("x")[1].strip()
            with open("/sys/class/drm/" + gpu + "/device/device") as reader:
                gpu_device_id = reader.read().split("x")[1].strip()
        except FileNotFoundError:
            gpu_vendor_id = "_unknown_vendor_"
            gpu_device_id = "_unknown_device_"
        gpu_vendor_id_for_search = "\n" + gpu_vendor_id + "  "
        gpu_device_id_for_search = "\n\t" + gpu_device_id + "  "
        if gpu_vendor_id_for_search in pci_ids_output:                                        # "vendor" information may not be present in the pci.ids file.
            rest_of_the_pci_ids_output = pci_ids_output.split(gpu_vendor_id_for_search, 1)[1]    # "1" in the ".split("[string", 1)" is used in order to split only the first instance in the whole text for faster split operation.
            gpu_vendor_name = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
        else:
            gpu_vendor_name = f'[{_tr("Unknown")}]'
        if gpu_device_id_for_search in rest_of_the_pci_ids_output and gpu_vendor_name != f'[{_tr("Unknown")}]':    # "device name" information may not be present in the pci.ids file.
            rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(gpu_device_id_for_search, 1)[1]
            gpu_device_name = rest_of_the_rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
        else:
            gpu_device_name = f'[{_tr("Unknown")}]'
        gpu_device_model_name.append(f'{gpu_vendor_name} - {gpu_device_name}')
        gpu_vendor_id_list.append(gpu_vendor_id)                                              # This list will be used for matching with GPU information from "glxinfo" command.
        gpu_device_id_list.append(gpu_device_id)                                              # This list will be used for matching with GPU information from "glxinfo" command.

    # Set selected gpu/graphics card
    if Config.selected_gpu == "":                                                             # "" is predefined gpu name before release of the software. This statement is used in order to avoid error, if no gpu selection is made since first run of the software.
        if default_gpu != "":
            set_selected_gpu = default_gpu
        if default_gpu == "":
            set_selected_gpu = gpu_list[0]
    if Config.selected_gpu in gpu_list:
        set_selected_gpu = Config.selected_gpu
    if Config.selected_gpu not in gpu_list:
        if default_gpu != "":
            set_selected_gpu = default_gpu
        if default_gpu == "":
            set_selected_gpu = gpu_list[0]
    global selected_gpu_number
    selected_gpu_number = gpu_list.index(set_selected_gpu)
