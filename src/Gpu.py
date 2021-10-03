#!/usr/bin/env python3

# ----------------------------------- GPU - GPU Tab GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def gpu_import_func():

    global Gtk, GLib, Thread, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os
    import subprocess


    global Config, MainGUI, Performance, GpuGUI
    import Config, MainGUI, Performance, GpuGUI


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
        glarea1501 = GpuGUI.glarea1501
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
            #GpuGUI.label1513.set_text(".")
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
    for command in glxinfo_command_list:                                                      # "10" is large enough to try for all GPUs on an average computer.
        try:
            glxinfo_output_lines = (subprocess.check_output(command, shell=True).strip()).decode().split("\n")    # This command gives current GPU information. If application is run with "DRI_PRIME=1 application-name" this command gives external GPU information.
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
                if_unified_memory = line.split(":")[1].strip().capitalize()
            if line.strip().startswith("direct rendering:"):
                direct_rendering = line.split(":")[1].strip()
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
    GpuGUI.label1501.set_text(gpu_device_model_name[selected_gpu_number])
    GpuGUI.label1502.set_text(f'{gpu_list[selected_gpu_number]} ({gpu_vendor_name_in_driver} {gpu_device_name_in_driver})')
    GpuGUI.label1507.set_text(if_default_gpu)
    GpuGUI.label1508.set_text(video_memory)
    GpuGUI.label1509.set_text(if_unified_memory)
    GpuGUI.label1510.set_text(direct_rendering)
    GpuGUI.label1511.set_text(display_driver)
    GpuGUI.label1512.set_text(opengl_version)


# ----------------------------------- GPU - Get GPU Data Function (gets GPU data, shows on the labels on the GUI) -----------------------------------
def gpu_loop_func():

    global frame_list, fps_count, fps_count_list, frame_latency
    #glarea1501.queue_draw()
    fps = len(frame_list) / update_interval
    del fps_count[0]
    fps_count.append(fps)
    frame_latency = 1 / (fps + 0.0000001)
    frame_list = []

    GpuGUI.drawingarea1501.queue_draw()

    current_resolution_and_refresh_rate = (subprocess.check_output("xrandr | grep '*'", shell=True).strip()).decode().split('*')[0].split(' ')
    current_resolution_and_refresh_rate = [i for i in current_resolution_and_refresh_rate if i != '']


    # Set and update GPU tab label texts by using information get
    GpuGUI.label1503.set_text(f'{fps_count[-1]:.0f}')
    GpuGUI.label1504.set_text(f'{frame_latency:.2f} ms')
    GpuGUI.label1505.set_text(f'{current_resolution_and_refresh_rate[1]} Hz')
    GpuGUI.label1506.set_text(f'{current_resolution_and_refresh_rate[0]}')


# ----------------------------------- GPU Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def gpu_initial_thread_func():

    GLib.idle_add(gpu_initial_func)


# ----------------------------------- GPU Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def gpu_loop_thread_func(dummy_variable):                                                     # "dummy_variable" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

#     GLib.idle_add(gpu_loop_func)
#     if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1005.get_active() == True:
#         global update_interval
#         update_interval = Config.update_interval
#         GLib.timeout_add(update_interval * 1000, gpu_loop_thread_func)

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
    gpu_loop_thread = Thread(target=gpu_loop_thread_func(None), daemon=True)                  # "None" is an arbitrary value which is required for using "GLib.timeout_source_new()".
    gpu_loop_thread.start()
