#!/usr/bin/env python3

# ----------------------------------- GPU - GPU Tab Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def gpu_import_func():

    global Gtk, GLib, Thread, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os
    import subprocess


    global Config, MainGUI, Performance
    import Config, MainGUI, Performance


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- GPU - GPU GUI Function (the code of this module in order to avoid running them during module import and defines "GPU" tab GUI objects and functions/signals) -----------------------------------
def gpu_gui_func():

    # GPU tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/GpuTab.ui")

    # GPU tab GUI objects
    global grid1501, drawingarea1501, button1501, label1501, label1502
    global label1503, label1504, label1505, label1506, label1507, label1508, label1509, label1510, label1511, label1512
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
    glarea1501 = builder.get_object('glarea1501')


    # GPU tab GUI functions
    def on_button1501_clicked(widget):
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                      # Get gpu/graphics card list and set selected gpu
        if 'GpuMenu' not in globals():
            global GpuMenu
            import GpuMenu
            GpuMenu.gpu_menus_import_func()
            GpuMenu.gpu_menus_gui_func()
            GpuMenu.popover1501p.set_relative_to(button1501)                                  # Set widget that popover menu will display at the edge of.
            GpuMenu.popover1501p.set_position(1)                                              # Show popover menu at the right edge of the caller button.
        GpuMenu.popover1501p.popup()                                                          # Show GPU tab popover GUI


    # ----------------------------------- GPU - Plot FPS data as a Line Chart ----------------------------------- 
    def on_drawingarea1501_draw(widget, chart1501):

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

        chart1501_width = Gtk.Widget.get_allocated_width(drawingarea1501)
        chart1501_height = Gtk.Widget.get_allocated_height(drawingarea1501)

        chart1501.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1501.rectangle(0, 0, chart1501_width, chart1501_height)
        chart1501.fill()

        chart1501.set_line_width(1)
        chart1501.set_dash([4, 3])
        chart1501.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        for i in range(3):
            chart1501.move_to(0, chart1501_height/4*(i+1))
            chart1501.line_to(chart1501_width, chart1501_height/4*(i+1))
        for i in range(4):
            chart1501.move_to(chart1501_width/5*(i+1), 0)
            chart1501.line_to(chart1501_width/5*(i+1), chart1501_height)
        chart1501.stroke()

        chart1501.set_dash([], 0)
        chart1501.rectangle(0, 0, chart1501_width, chart1501_height)
        chart1501.stroke()

        chart1501.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1501.move_to(chart1501_width*chart_x_axis[0]/(chart_data_history-1), chart1501_height - chart1501_height*fps_count[0]/100)
        for i in range(len(chart_x_axis) - 1):
            delta_x_chart1501 = (chart1501_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1501_width * chart_x_axis[i]/(chart_data_history-1))
            delta_y_chart1501 = (chart1501_height*fps_count[i+1]/100) - (chart1501_height*fps_count[i]/100)
            chart1501.rel_line_to(delta_x_chart1501, -delta_y_chart1501)

        chart1501.rel_line_to(10, 0)
        chart1501.rel_line_to(0, chart1501_height+10)
        chart1501.rel_line_to(-(chart1501_width+20), 0)
        chart1501.rel_line_to(0, -(chart1501_height+10))
        chart1501.close_path()
        chart1501.stroke_preserve()
        chart1501.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
        chart1501.fill()


    # GPU tab GUI functions - connect
    button1501.connect("clicked", on_button1501_clicked)
    drawingarea1501.connect("draw", on_drawingarea1501_draw)


# ----------------------------------- GPU - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def gpu_initial_func():

    # Import required OpenGL modules for measuring FPS (glarea will be used).
    if "OpenGL" not in globals():                                                             # Import modules if they have not been imported before. This modeles are imported here because importing them takes about 0.15 seconds on a 4-cored i7-2630QM notebook and this slows application start a bit.
        import OpenGL
        # from OpenGL.GL import *                                                             # This code could not be run in a module because of the "*". Need to be imported in a module when "GPU" tab is opened. Because importing this module consumes about 11 MiB of RAM.
        from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, glFlush             # This code is used instead of "from OpenGL.GL import *" to be able to import required module in a function otherwise, module could not be imported in a module because of the "*".

    # Define initial values for fps_count and frame_latency values
    global fps_count, frame_latency
    fps_count = [0] * Config.chart_data_history
    frame_latency = 0

    # Measure FPS (Rendering is performed by using glarea in order to measure FPS. FPS on drawing area is counted. Lower FPS is obtained depending on the GPU load/performance.)
    if "frame_list" not in globals():
        global glarea1501, frame_list
        frame_list = []

        def on_glarea1501_realize(area):
            area.make_current()
            if (area.get_error() != None):
              return

        def on_glarea1501_render(area, context):
            glClearColor(0.5, 0.5, 0.5, 1.0)                                                  # Arbitrary color
            glClear(GL_COLOR_BUFFER_BIT)
            glFlush()
            global frame_list
            frame_list.append(0)
            glarea1501.queue_draw()
            return True

        glarea1501.connect('realize', on_glarea1501_realize)
        glarea1501.connect('render', on_glarea1501_render)

    # Get gpu_device_name value
    Performance.performance_get_gpu_list_and_set_selected_gpu_func()                          # Get gpu/graphics card list and set selected gpu
    gpu_vendor_id_list = Performance.gpu_vendor_id_list
    selected_gpu_number = Performance.selected_gpu_number
    gpu_device_id_list = Performance.gpu_device_id_list
    gpu_list = Performance.gpu_list
    default_gpu = Performance.default_gpu
    gpu_device_model_name = Performance.gpu_device_model_name
    # Get video_memory, if_unified_memory, direct_rendering, mesa_version, opengl_version values of the GPU which is preferred for running this application. "DRI_PRIME application-name" and "DRI_PRIME=1 application-name" could be used for running an application by using internal and external GPUs respectively.
    glxinfo_command_list = ["glxinfo -B", "DRI_PRIME=1 glxinfo -B"]
    for command in glxinfo_command_list:
        try:
            glxinfo_output_lines = (subprocess.check_output(command, shell=True)).decode().strip().split("\n")    # This command gives current GPU information. If application is run with "DRI_PRIME=1 application-name" this command gives external GPU information.
            for line in glxinfo_output_lines:
                if line.strip().startswith("Vendor:"):
                    gpu_vendor_in_driver = line.split()[-1].strip("()").split("x")[1].strip()
                if line.strip().startswith("Device:"):
                    gpu_device_in_driver = line.split()[-1].strip("()").split("x")[1].strip()
        except:
            gpu_vendor_in_driver = "-"
            gpu_device_in_driver = "-"
        if gpu_vendor_in_driver == gpu_vendor_id_list[selected_gpu_number].strip(" \n\t") and gpu_device_in_driver == gpu_device_id_list[selected_gpu_number].strip(" \n\t")[1:]:    # Check for matching GPU information from "sys/devices/pci0000:00/..." directory and from "glxinfo" command. "[1:]" is used for trimming "0" at the beginning of the device id which is get from "/sys/devices/..." directory.
            break
    try:
        for line in glxinfo_output_lines:
            if line.strip().startswith("OpenGL vendor string:"):
                gpu_vendor_name_in_driver = line.split(":")[1].strip()
            if line.strip().startswith("OpenGL renderer string:"):
                gpu_device_name_in_driver = line.split(":")[1].strip()
            if line.strip().startswith("Video memory:"):
                video_memory = line.split(":")[1].strip()
            if line.strip().startswith("Unified memory:"):
                if_unified_memory = _tr(line.split(":")[1].strip().capitalize())              # "_tr()" is used in order to translate ("yes" or "no" values are get from this line) the strings.
            if line.strip().startswith("direct rendering:"):
                direct_rendering = _tr(line.split(":")[1].strip())                            # "_tr()" is used in order to translate ("yes" or "no" values are get from this line) the strings.
            if line.strip().startswith("Version:"):
                mesa_version = line.split(":")[1].strip()
            if line.strip().startswith("OpenGL version string:"):
                opengl_version, display_driver = line.split(":")[1].strip().split(" ", 1)     # "split(" ", 1" is for splitting string by first space character
    except:
        gpu_vendor_name_in_driver = "-"
        gpu_device_name_in_driver = "-"
        video_memory = "-"
        if_unified_memory = "-"
        direct_rendering = "-"
        mesa_version = "-"
        opengl_version = "-"
        display_driver = "-"
    # Get if_default_gpu value
    if gpu_list[selected_gpu_number] == default_gpu:
        if_default_gpu = _tr("Yes")
    if gpu_list[selected_gpu_number] != default_gpu:
        if_default_gpu = _tr("No")

    # Set GPU tab label texts by using information get
    label1501.set_text(gpu_device_model_name[selected_gpu_number])
    label1502.set_text(f'{gpu_list[selected_gpu_number]} ({gpu_vendor_name_in_driver} {gpu_device_name_in_driver})')
    label1507.set_text(if_default_gpu)
    label1508.set_text(video_memory)
    label1509.set_text(if_unified_memory)
    label1510.set_text(direct_rendering)
    label1511.set_text(display_driver)
    label1512.set_text(opengl_version)


# ----------------------------------- GPU - Get GPU Data Function (gets GPU data, shows on the labels on the GUI) -----------------------------------
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
    xrandr_lines = (subprocess.check_output(["xrandr"], shell=False)).decode().strip().split("\n")
    for line in xrandr_lines:
        if "*" in line:
            current_resolution = line.split()[0]
            current_refresh_rate = line.split()[1].split("*")[0]
            break


    # Set and update GPU tab label texts by using information get
    label1503.set_text(f'{fps_count[-1]:.0f}')
    label1504.set_text(f'{frame_latency:.1f} ms')
    label1505.set_text(f'{current_refresh_rate} Hz')
    label1506.set_text(f'{current_resolution}')


# ----------------------------------- GPU Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def gpu_initial_thread_func():

    GLib.idle_add(gpu_initial_func)


# ----------------------------------- GPU Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def gpu_loop_thread_func(*args):                                                              # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1005.get_active() == True:
        global gpu_glib_source, update_interval                                               # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            gpu_glib_source.destroy()                                                         # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        gpu_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(gpu_loop_func)
        gpu_glib_source.set_callback(gpu_loop_thread_func)
        gpu_glib_source.attach(GLib.MainContext.default())                                    # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- GPU Thread Run Function (starts execution of the threads) -----------------------------------
def gpu_thread_run_func():

    if "update_interval" not in globals():                                                    # To be able to run initial thread for only one time
        gpu_initial_thread = Thread(target=gpu_initial_thread_func, daemon=True)
        gpu_initial_thread.start()
        gpu_initial_thread.join()
    gpu_loop_thread = Thread(target=gpu_loop_thread_func, daemon=True)
    gpu_loop_thread.start()
