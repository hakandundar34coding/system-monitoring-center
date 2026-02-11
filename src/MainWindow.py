import tkinter as tk
from tkinter import ttk

import cairo
from PIL import Image, ImageTk

import sys
import os
import locale
import gettext

from .Config import Config

# Add theme path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import sv_ttk

def language_translation_support():
    """
    Configurations for language translation support.
    """

    from .Main import localedir
    if localedir == None:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if os.path.isdir(current_dir + "/../po/locale/") == True:
            # For running from source code
            localedir = current_dir + "/../po/locale/"
        else:
            # For installed code
            localedir = "/usr/share/locale"
    if Config.language == "system":
        application_language = os.environ.get("LANG")
    else:
        application_language = Config.language

    global _tr

    try:
        language = gettext.translation("system-monitoring-center", localedir=localedir, languages=[application_language])
        language.install()
        _tr = language.gettext
    # Prevent errors if there are problems with language installations on the system.
    except Exception:
        def _tr(text_for_translation):
            return text_for_translation

    Config._tr = _tr

language_translation_support()

from . import Common
from .Performance import Performance
from . import Libsysmon


class MainWindow():

    def __init__(self):
        """
        Run initial functions and generate main window.
        """

        self.main_window_gui()

        self.hide_services_tab()

        # Define these settings in order to avoid error on the first call 
        # of "main_gui_tab_loop" function. This value is used in order to detect
        # the current tab without checking GUI obejects for lower CPU usage.
        # This value is not saved into settings file.
        Config.current_main_tab = -1
        Config.performance_tab_current_sub_tab = -1

        self.switch_to_default_tab()

        self.connect_signals()


    def main_window_gui(self):
        """
        Generate main window GUI.
        """

        # Application window
        # Class name defined for taskbar image of the application. Same thing is defined in .desktop file.
        self.main_window = tk.Tk(className="smc_window")
        #self.main_window.tk.call("tk", "scaling", 1.5)
        self.light_dark_theme()
        self.define_image_path()
        self.main_window.geometry("670x570")
        self.main_window.minsize(670, 570)
        self.main_window.maxsize(3840, 2160)
        self.main_window.title(_tr("System Monitoring Center"))
        self.application_icon = tk.PhotoImage(file=self.image_path + "../../apps/system-monitoring-center.png")
        # "True" is for using the image for other windows of the application.
        self.main_window.iconphoto(True, self.application_icon)

        # Resize the main window if "remember window size" option is enabled.
        remember_window_size = Config.remember_window_size
        if remember_window_size != "0x0":
            self.main_window.update_idletasks()
            self.main_window.geometry(remember_window_size)

        self.main_window.rowconfigure(1, weight=1)
        self.main_window.columnconfigure(0, weight=1)

        # HeaderBar (Main window)
        # Frame (headerbar)
        self.window_headerbar = ttk.Frame(self.main_window)
        #self.window_headerbar.rowconfigure(0, weight=1)
        self.window_headerbar.columnconfigure(1, minsize=32)
        self.window_headerbar.columnconfigure(4, weight=1)
        self.window_headerbar.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

        # Performance summary on the window headerbar
        self.performance_summary_headerbar_gui()

        # Show warning if the application is run with root privileges. 
        if os.geteuid() == 0:
            label_root_warning = tk.Label(self.window_headerbar, text=_tr("Warning! The application has been run with root privileges, you may harm your system."), bg="red", wraplength=400, justify="center")
            label_root_warning.grid(row=0, column=4, rowspan=2, sticky="e", padx=5, pady=5)

        # Button (Refresh)
        image = tk.PhotoImage(file=self.image_path + "smc-reload.png")
        image = image.subsample(3, 3)
        self.refresh_button = ttk.Button(self.window_headerbar, image=image, command=self.current_tab_refresh)
        self.refresh_button.image = image
        self.refresh_button.grid(row=0, column=5, rowspan=2, sticky="e", padx=2, pady=0)
        tooltip = Common.tooltip(self.refresh_button, _tr("Refresh") + "     (F5)")

        # Button (Settings)
        image = tk.PhotoImage(file=self.image_path + "smc-customizations.png")
        image = image.subsample(3, 3)
        self.settings_button = ttk.Button(self.window_headerbar, image=image, command=self.settings_window_gui)
        self.settings_button.image = image
        self.settings_button.grid(row=0, column=6, rowspan=2, sticky="e", padx=2, pady=0)
        tooltip = Common.tooltip(self.settings_button, _tr("Settings") + "     (Ctrl+,)")

        # Button (About)
        image = tk.PhotoImage(file=self.image_path + "smc-info-about.png")
        image = image.subsample(3, 3)
        self.about_button = ttk.Button(self.window_headerbar, image=image, command=self.about_dialog_gui)
        self.about_button.image = image
        self.about_button.grid(row=0, column=7, rowspan=2, sticky="e", padx=2, pady=0)
        tooltip = Common.tooltip(self.about_button, _tr("About"))

        # Main Frame
        self.main_frame = ttk.Frame(self.main_window)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # Main tab (Performance, Processes, etc.) GUI
        self.main_tabs()

        # Performance tab sub-tab (Summary, CPU, etc.) GUI
        self.performance_tab_sub_tabs()


    def performance_summary_headerbar_gui(self):
        """
        Generate and configure performance summary GUI objects on the window headerbar.
        """

        # Label (CPU)
        label = Common.headerbar_label(self.window_headerbar, text=_tr("CPU") + ":")
        label.grid(row=0, column=0, sticky="w", padx=(3, 6), pady=1)

        # Label (RAM)
        label = Common.headerbar_label(self.window_headerbar, text=_tr("RAM") + ":")
        label.grid(row=1, column=0, sticky="w", padx=(3, 6), pady=1)

        # Label (for showing CPU usage graphics)
        self.ps_hb_cpu_da = ttk.Label(self.window_headerbar)
        self.ps_hb_cpu_da.grid(row=0, column=1, sticky="ew", padx=0, pady=1)

        # Label (for showing RAM usage graphics)
        self.ps_hb_ram_da = ttk.Label(self.window_headerbar)
        self.ps_hb_ram_da.grid(row=1, column=1, sticky="ew", padx=0, pady=1)

        # Label (Disk)
        label = Common.headerbar_label(self.window_headerbar, text=_tr("Disk") + ":")
        label.grid(row=0, column=2, sticky="w", padx=(14, 3), pady=1)
        tooltip = Common.tooltip(label, f'{_tr("Read Speed")} + {_tr("Write Speed")}')

        # Label (Network)
        label = Common.headerbar_label(self.window_headerbar, text=_tr("Network") + ":")
        label.grid(row=1, column=2, sticky="w", padx=(14, 3), pady=1)
        tooltip = Common.tooltip(label, f'{_tr("Download Speed")} + {_tr("Upload Speed")}')

        # Label (disk speed)
        self.ps_hb_disk_label = Common.headerbar_label(self.window_headerbar, text="--")
        self.ps_hb_disk_label.grid(row=0, column=3, sticky="w", padx=3, pady=1)

        # Label (network speed)
        self.ps_hb_network_label = Common.headerbar_label(self.window_headerbar, text="--")
        self.ps_hb_network_label.grid(row=1, column=3, sticky="w", padx=3, pady=1)


    def main_tabs(self):
        """
        Generate main tab (Performance, Processes, etc.) GUI objects.
        """

        # Frame (main tab togglebutton)
        self.main_tab_tb_frame = ttk.Frame(self.main_frame)
        self.main_tab_tb_frame.grid(row=0, column=0, sticky="n", padx=0, pady=0)
        # "equal" is an arbitrary key for the group
        self.main_tab_tb_frame.columnconfigure((0, 1, 2, 3, 4), minsize=132, uniform="equal")

        self.main_tab_var = tk.IntVar()

        # ToggleButton (Performance)
        self.performance_tb = Common.main_tab_togglebutton(self.main_tab_tb_frame, _tr("Performance"), self.image_path + "smc-performance.png", self.main_tab_var, 0)
        self.performance_tb.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (Processes)
        self.processes_tb = Common.main_tab_togglebutton(self.main_tab_tb_frame, _tr("Processes"), self.image_path + "smc-process.png", self.main_tab_var, 1)
        self.processes_tb.grid(row=0, column=1, sticky="ew", padx=0, pady=0)

        # ToggleButton (Users)
        self.users_tb = Common.main_tab_togglebutton(self.main_tab_tb_frame, _tr("Users"),  self.image_path + "smc-user.png", self.main_tab_var, 2)
        self.users_tb.grid(row=0, column=2, sticky="ew", padx=0, pady=0)

        # ToggleButton (Services)
        image_path = self.image_path + "actions/smc-service-white.png"
        self.services_tb = Common.main_tab_togglebutton(self.main_tab_tb_frame, _tr("Services"), self.image_path + "smc-service.png", self.main_tab_var, 3)
        self.services_tb.grid(row=0, column=3, sticky="ew", padx=0, pady=0)

        # ToggleButton (System)
        self.system_tb = Common.main_tab_togglebutton(self.main_tab_tb_frame, _tr("System"), self.image_path + "smc-system.png", self.main_tab_var, 4)
        self.system_tb.grid(row=0, column=4, sticky="ew", padx=0, pady=0)

        # Separator between main tab togglebuttons and main tabs
        separator = ttk.Separator(self.main_frame, orient="horizontal")
        separator.grid(row=1, column=0, sticky="new", padx=0, pady=4)

        # Stack (main tab)
        self.main_tab_stack = ttk.Frame(self.main_frame)
        self.main_tab_stack.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self.main_tab_stack.columnconfigure(0, weight=1)
        self.main_tab_stack.rowconfigure(0, weight=1)

        # Main Frame (Performance tab)
        self.performance_tab_main_frame = ttk.Frame(self.main_tab_stack)
        self.performance_tab_main_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.performance_tab_main_frame.columnconfigure(2, weight=1)
        self.performance_tab_main_frame.rowconfigure(0, weight=1)

        # Main Frame (Processes tab)
        self.processes_tab_main_frame = Common.tab_main_frame(self.main_tab_stack)

        # Main Frame (Users tab)
        self.users_tab_main_frame = Common.tab_main_frame(self.main_tab_stack)

        # Main Frame (Services tab)
        self.services_tab_main_frame = Common.tab_main_frame(self.main_tab_stack)

        # Main Frame (System tab)
        self.system_tab_main_frame = Common.tab_main_frame(self.main_tab_stack)


    def performance_tab_sub_tabs(self):
        """
        Generate Performance tab sub-tab (Summary, CPU, etc.) GUI.
        """

        # Main Frame (Performance tab sub-tab togglebuttons)
        self.sub_tab_tb_frame = ttk.Frame(self.performance_tab_main_frame)
        self.sub_tab_tb_frame.grid(row=0, column=0, sticky="nw", padx=0, pady=(35,0))
        # "equal" is an arbitrary key for the group
        #self.sub_tab_tb_frame.columnconfigure(0, weight=1)
        #self.sub_tab_tb_frame.columnconfigure(0, minsize=132)
        #self.sub_tab_tb_frame.rowconfigure(0, weight=1)
        #self.sub_tab_tb_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="equal")

        self.sub_tab_var = tk.IntVar()

        # ToggleButton (Summary)
        self.summary_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("Summary"), self.image_path + "smc-performance.png", self.sub_tab_var, 0)
        self.summary_tb.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (CPU)
        self.cpu_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("CPU"), self.image_path + "smc-cpu.png", self.sub_tab_var, 1)
        self.cpu_tb.grid(row=2, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (Memory)
        self.memory_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("Memory"), self.image_path + "smc-ram.png", self.sub_tab_var, 2)
        self.memory_tb.grid(row=4, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (Disk)
        self.disk_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("Disk"), self.image_path + "smc-disk.png", self.sub_tab_var, 3)
        self.disk_tb.grid(row=6, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (Network)
        self.network_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("Network"), self.image_path + "smc-network.png", self.sub_tab_var, 4)
        self.network_tb.grid(row=8, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (GPU)
        self.gpu_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("GPU"), self.image_path + "smc-gpu.png", self.sub_tab_var, 5)
        self.gpu_tb.grid(row=10, column=0, sticky="ew", padx=0, pady=0)

        # ToggleButton (Sensors)
        self.sensors_tb = Common.sub_tab_togglebutton(self.sub_tab_tb_frame, _tr("Sensors"), self.image_path + "smc-temperature.png", self.sub_tab_var, 6)
        self.sensors_tb.grid(row=12, column=0, sticky="ew", padx=0, pady=0)

        # Separator between Performance tab sub-tab togglebuttons and sub-tabs
        separator = ttk.Separator(self.performance_tab_main_frame, orient="vertical")
        separator.grid(row=0, column=1, sticky="ns", padx=2, pady=0)

        # Stack (Performance tab sub-tabs)
        self.sub_tab_stack = ttk.Frame(self.performance_tab_main_frame)
        self.sub_tab_stack.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        self.sub_tab_stack.columnconfigure(0, weight=1)
        self.sub_tab_stack.rowconfigure(0, weight=1)

        # Main Frame (Summary tab)
        self.summary_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)

        # Main Frame (CPU tab)
        self.cpu_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)

        # Main Frame (Memory tab)
        self.memory_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)

        # Main Frame (Disk tab)
        self.disk_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)

        # Main Frame (Network tab)
        self.network_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)

        # Main Frame (GPU tab)
        self.gpu_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)

        # Main Frame (Sensors tab)
        self.sensors_tab_main_frame = Common.tab_main_frame(self.sub_tab_stack)


    def connect_signals(self):
        """
        Connect GUI signals.
        """

        # Main window signals
        self.main_window.after(1, self.on_main_window_show)
        self.main_window.protocol('WM_DELETE_WINDOW', self.on_main_window_close_request)
        self.main_window.bind("<Configure>", self.update_graph_immediately)
        self.main_window.bind("<F5>", self.current_tab_refresh)
        self.main_window.bind("<Control-comma>", self.settings_window_gui)
        self.main_window.bind('<Control-f>', Common.searchentry_focus)
        self.main_window.bind('<Control-F>', Common.searchentry_focus)
        self.main_window.bind('<Control-q>', self.on_main_window_close_request)
        self.main_window.bind('<Control-Q>', self.on_main_window_close_request)
        self.main_window.bind('<Control-w>', self.on_main_window_close_request)
        self.main_window.bind('<Control-W>', self.on_main_window_close_request)

        # Main tab togglebutton signals
        self.performance_tb.config(command=self.main_gui_tab_switch)
        self.processes_tb.config(command=self.main_gui_tab_switch)
        self.users_tb.config(command=self.main_gui_tab_switch)
        self.services_tb.config(command=self.main_gui_tab_switch)
        self.system_tb.config(command=self.main_gui_tab_switch)

        # Performance tab sub-tabs togglebutton signals
        self.summary_tb.config(command=self.main_gui_tab_switch)
        self.cpu_tb.config(command=self.main_gui_tab_switch)
        self.memory_tb.config(command=self.main_gui_tab_switch)
        self.disk_tb.config(command=self.main_gui_tab_switch)
        self.network_tb.config(command=self.main_gui_tab_switch)
        self.gpu_tb.config(command=self.main_gui_tab_switch)
        self.sensors_tb.config(command=self.main_gui_tab_switch)


    def on_main_window_close_request(self, event=None):
        """
        Called when window is closed.
        """

        # Get and save window state (if full screen or not), window size (width, height)
        if Config.remember_window_size != "0x0":
            MainWindow.main_window.update_idletasks()
            main_window_width = MainWindow.main_window.winfo_width()
            main_window_height = MainWindow.main_window.winfo_height()
            Config.remember_window_size = str(main_window_width) + "x" + str(main_window_height)
            Config.config_save_func()

        # Delete ProcessesDetails objects and windows.
        if "ProcessesDetails" not in globals():
            from . import ProcessesDetails
            for obj in ProcessesDetails.processes_details_object_list:
                obj.process_details_window.after_cancel(obj.loop_id)
                obj.process_details_window.destroy()
                obj = None
            ProcessesDetails.processes_details_object_list = None
            ProcessesDetails = None

        # Delete child windows if they are opened.
        for window in self.main_window.winfo_children():
            if isinstance(window, tk.Toplevel) == True:
                window.destroy()
                window = None

        # Delete references of some global variables.
        from . import Common
        del Common.font_system, Common.font_bold_2x, Common.font_bold_underlined, Common.font_bold, Common.font_underlined, Common.font_small

        # Call manual deleter.
        self.application_icon.__del__()
        self.refresh_button.image.__del__()
        self.settings_button.image.__del__()
        self.about_button.image.__del__()
        self.performance_tb.image.__del__()
        self.processes_tb.image.__del__()
        self.users_tb.image.__del__()
        self.services_tb.image.__del__()
        self.system_tb.image.__del__()
        self.summary_tb.image.__del__()
        self.cpu_tb.image.__del__()
        self.memory_tb.image.__del__()
        self.disk_tb.image.__del__()
        self.network_tb.image.__del__()
        self.gpu_tb.image.__del__()
        self.sensors_tb.image.__del__()

        # Remove references to images.
        self.application_icon = None
        self.refresh_button.image = None
        self.settings_button.image = None
        self.about_button.image = None
        self.performance_tb.image = None
        self.processes_tb.image = None
        self.users_tb.image = None
        self.services_tb.image = None
        self.system_tb.image = None
        self.summary_tb.image = None
        self.cpu_tb.image = None
        self.memory_tb.image = None
        self.disk_tb.image = None
        self.network_tb.image = None
        self.gpu_tb.image = None
        self.sensors_tb.image = None

        # Call manuıal deleter and remove references for charts.
        """from .Performance import Performance
        from .Summary import Summary
        Performance.widget_to_clear_line_chart.image.__del__()
        Performance.widget_to_clear_line_chart.image = None
        Performance.widget_to_clear_bar_chart.image.__del__()
        Performance.widget_to_clear_bar_chart.image = None
        Summary.widget_to_clear_summary_chart.image.__del__()
        Summary.widget_to_clear_summary_chart.image = None
        Performance.widget_to_clear_line_chart = None
        Performance.widget_to_clear_bar_chart = None
        Summary.widget_to_clear_summary_chart = None"""

        # Delete widgets on main window.
        for widget in self.main_window.winfo_children():
            widget.destroy()

        # Call garbage collector manually.
        import gc
        gc.collect()

        # Clear all widger references manually.
        self.main_window.children.clear()

        # Cancel main loop.
        self.main_window.after_cancel(self.loop_id)
        # Delete main window and exit the application.
        self.main_window.destroy()
        # Stop TCL interpreter in order to avoid memory leak.
        self.main_window.quit()
        sys.exit()


    def on_main_window_show(self):
        """
        Run code after window is shown.
        """

        # Start the main loop function
        self.main_gui_tab_loop()

        # Run main tab function (It is also called when main tab togglebuttons are toggled).
        self.main_gui_tab_switch()

        self.unified_tab_device_list_width()


    def settings_window_gui(self, event=None):
        """
        Generate and show settings window.
        """

        from .SettingsWindow import SettingsWindow
        SettingsWindow.window_gui()


    def on_main_menu_about_button_clicked(self, action, parameter):
        """
        Generate and show about dialog.
        """

        self.about_dialog_gui()


    def about_dialog_gui(self):
        """
        Generate about dialog.
        """

        # Get software version
        with open(os.path.dirname(os.path.abspath(__file__)) + "/__version__") as reader:
            software_version = reader.read().strip()

        # Define translators dictionary
        translators_dict = {"cs": "panmourovaty",
                            "de": "Baumfinder",
                            "es": "haggen88",
                            "fa": "MasterKia",
                            "fr": "Metoto Sakamoto",
                            "hu": "Kálmán Szalai",
                            "pl": "ski007, K0RR, sdorpl",
                            "pt_BR": "Bruno do Nascimento",
                            "pt_PT": "Hugo Carvalho, Ricardo Simões",
                            "ru_RU": "badcast, akorny",
                            "tr": "Hakan Dündar",
                            "zh_CN": "yuzh496",
                            "zh_TW": "csc-chicken"
                           }

        # Get GUI language for getting translator name
        application_language = Config.language
        if application_language == "system":
            application_language = os.environ.get("LANG")
        application_language_code = application_language.split(".")[0]
        application_language_code_split = application_language_code.split("_")[0]

        # Define translators list
        try:
            translators = '\n'.join(translators_dict[application_language_code].split(", "))
        except Exception:
            try:
                translators = '\n'.join(translators_dict[application_language_code_split].split(", "))
            except Exception:
                translators = "-"
        translators = _tr("Translated by") + ": " + translators

        # Window (About)
        about_window, frame = Common.window(self.main_window, _tr("About"))
        about_window.resizable(False, False)

        # Label (application image)
        image_label = tk.Label(frame, image=self.application_icon)
        image_label.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Label (application name)
        name_label = Common.bold_label(frame, text=_tr("System Monitoring Center"))
        name_label.grid(row=1, column=0, sticky="ns", padx=0, pady=0)

        # Label (application version)
        version_label = tk.Label(frame, text=software_version)
        version_label.grid(row=2, column=0, sticky="ns", padx=0, pady=4)

        # Label (description)
        smc_label1 = tk.Label(frame, text=_tr("Multi-featured system monitor"))
        smc_label1.grid(row=3, column=0, sticky="ns", padx=0, pady=5)

        # Label (web page)
        web_page_label = Common.link_label(frame, _tr("Web Page"), "https://github.com/hakandundar34coding/system-monitoring-center")
        web_page_label.grid(row=4, column=0, sticky="ns", padx=0, pady=0)

        # Label (copyright)
        copyright_label = tk.Label(frame, text="© 2026 Hakan Dündar")
        copyright_label.grid(row=5, column=0, sticky="ns", padx=0, pady=4)

        # Label (translators)
        translators_label = tk.Label(frame, text=translators)
        translators_label.grid(row=6, column=0, sticky="ns", padx=0, pady=4)

        # Label (license)
        license_label = tk.Label(frame, text=_tr("This program comes with absolutely no warranty.\nSee the GNU General Public License, version 3 or later for details."))
        license_label.grid(row=7, column=0, sticky="ns", padx=1, pady=0)

        # Label (license link)
        license_link_label = Common.link_label(frame, "GPLv3", "https://www.gnu.org/licenses/gpl-3.0.html")
        license_link_label.grid(row=8, column=0, sticky="ns")


    def current_tab_refresh(self, event=None):
        """
        Refreshes current tab. This function is called if "F5" button is pressed.
        """

        # Prevent refreshing current tab very frequently for preventing GUI freeze
        # if refresh button is pressed for a long time.
        if Config.current_main_tab == 0:
            if Config.performance_tab_current_sub_tab in [0, 1, 2, 3, 4]:
                tab_refresh_time_difference = 0.4
            elif Config.performance_tab_current_sub_tab in [5, 6]:
                tab_refresh_time_difference = 0.4
        elif Config.current_main_tab in [1, 2]:
            tab_refresh_time_difference = 0.4
        elif Config.current_main_tab in [3, 4]:
            tab_refresh_time_difference = 1

        import time
        tab_refresh_time_current = time.time()
        try:
            if tab_refresh_time_current - self.tab_refresh_time_prev < tab_refresh_time_difference:
                return
        except AttributeError:
            pass
        self.tab_refresh_time_prev = tab_refresh_time_current

        # Reset "loop_already_run" values of Services and System tab for refreshing them.
        # These tabs are not refreshed on every main loop of the application if these values are "1".
        if Config.current_main_tab == 3:
            from .Services import Services
            Services.loop_already_run = 0
        elif Config.current_main_tab == 4:
            from .System import System
            System.loop_already_run = 0

        self.main_gui_tab_loop()


    def light_dark_theme(self):
        """
        Set light/dark theme for GUI.
        """

        if Config.light_dark_theme == "system":
            #sv_ttk.set_theme("dark")
            theme = Libsysmon.get_gnome_theme()
            if theme == "-":
                theme = Libsysmon.get_kde_theme()
                if theme == "-":
                    sv_ttk.set_theme("dark")
            if theme == "light":
                sv_ttk.set_theme("light")
            if theme == "dark":
                sv_ttk.set_theme("dark")

        elif Config.light_dark_theme == "light":
            sv_ttk.set_theme("light")

        elif Config.light_dark_theme == "dark":
            sv_ttk.set_theme("dark")

        if sv_ttk.get_theme() in ["light", "default"]:
            Config.theme = "light"
        if sv_ttk.get_theme() in ["dark"]:
            Config.theme = "dark"


    def define_image_path(self):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        if os.path.isdir(current_dir + "/../data/") == True:
            # For running from source code
            self.image_path = current_dir + "/../data/icons/hicolor/scalable/"
        else:
            # For installed code
            self.image_path = current_dir + "/../icons/hicolor/scalable/"

        if Config.theme == "light":
            self.image_path = self.image_path + "actions/dark/"
        if Config.theme == "dark":
            self.image_path = self.image_path + "actions/white/"


    def language_translation_support(self):
        """
        Configurations for language translation support.
        """

        locale.bindtextdomain("system-monitoring-center", os.path.dirname(os.path.realpath(__file__)) + "/../locale")
        locale.textdomain("system-monitoring-center")

        if Config.language == "system":
            application_language = os.environ.get("LANG")
        else:
            application_language = Config.language

        try:
            locale.setlocale(locale.LC_ALL, application_language)
        # Prevent errors if there are problems with language installations on the system.
        except Exception:
            pass


    def update_graph_immediately(self, event):
        """
        Resize the graph immediately (without waiting the update interval) if the window is resized.
        This function is called for every widget. But it is stopped if the widget is not the window.
        """

        # In order to avoid crashes, prevent too frequent graphic refresh during moving or scaling window
        tab_refresh_time_difference = 0.4
        import time
        tab_refresh_time_current = time.time()
        global tab_refresh_time_prev
        try:
            if tab_refresh_time_current - tab_refresh_time_prev < tab_refresh_time_difference:
                return
        except NameError:
            pass
        tab_refresh_time_prev = tab_refresh_time_current

        if event.widget != self.main_window:
            return

        if Config.current_main_tab == 0:
            if Config.performance_tab_current_sub_tab == 0:
                Summary.performance_summary_graph_draw("drawingarea_tag")
            elif Config.performance_tab_current_sub_tab == 1:
                Performance.performance_line_charts_draw(Cpu.da_cpu_usage, "da_cpu_usage")
            elif Config.performance_tab_current_sub_tab == 2:
                Performance.performance_line_charts_draw(Memory.da_memory_usage, "da_memory_usage")
            elif Config.performance_tab_current_sub_tab == 3:
                Performance.performance_line_charts_draw(Disk.da_disk_speed, "da_disk_speed_usage")
            elif Config.performance_tab_current_sub_tab == 4:
                Performance.performance_line_charts_draw(Network.da_network_speed, "da_network_speed")
            elif Config.performance_tab_current_sub_tab == 5:
                Performance.performance_line_charts_draw(Gpu.da_gpu_usage, "da_gpu_usage")
                Performance.performance_line_charts_draw(Gpu.da_gpu_memory_usage, "da_gpu_memory_usage")


    def main_gui_tab_switch(self):
        """
        Runs tab functions (Performance, Processes, CPU, Memory, etc.) when their togglebuttons is toggled).
        """

        # Switch to "Performance" tab
        if "selected" in self.performance_tb.state():
            self.performance_tab_main_frame.tkraise()
            if Config.remember_last_opened_tabs == 1:
                # No need to save Config values after this value is defined.Because save operation
                # is performed for Performance tab sub-tabs (CPU, Memory, Disk, Network, GPU, Sensors tabs).
                Config.default_main_tab = 0
            Config.current_main_tab = 0

            # Switch to "Summary" tab
            if "selected" in self.summary_tb.state():
                self.summary_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 0
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 0
                # Attach the grid to the grid (on the Main Window) at (0, 0) position if not attached.
                if "Summary" not in globals():
                    global Summary
                    from .Summary import Summary
                # Run initial function of the module if this is the first loop of the module.
                if Summary.initial_already_run == 0:
                    Summary.initial_func()
                # Run loop Summary loop function in order to get data without waiting update interval.
                Summary.loop_func()
                # Show device selection list on a listbox between radiobuttons of Performance tab sub-tabs.
                self.main_gui_device_selection_list()
                return

            # Switch to "CPU" tab
            if "selected" in self.cpu_tb.state():
                self.cpu_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 1
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 1
                if "Cpu" not in globals():
                    global Cpu
                    from .Cpu import Cpu
                if Cpu.initial_already_run == 0:
                    Cpu.initial_func()
                Cpu.loop_func()
                self.main_gui_device_selection_list()
                return

            # Switch to "Memory" tab
            elif "selected" in self.memory_tb.state():
                self.memory_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 2
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 2
                if "Memory" not in globals():
                    global Memory
                    from .Memory import Memory
                if Memory.initial_already_run == 0:
                    Memory.initial_func()
                Memory.loop_func()
                self.main_gui_device_selection_list()
                return

            # Switch to "Disk" tab
            elif "selected" in self.disk_tb.state():
                self.disk_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 3
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 3
                if "Disk" not in globals():
                    global Disk
                    from .Disk import Disk
                if Disk.initial_already_run == 0:
                    Disk.initial_func()
                Disk.loop_func()
                self.main_gui_device_selection_list()
                return

            # Switch to "Network" tab
            elif "selected" in self.network_tb.state():
                self.network_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 4
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 4
                if "Network" not in globals():
                    global Network
                    from .Network import Network
                if Network.initial_already_run == 0:
                    Network.initial_func()
                Network.loop_func()
                self.main_gui_device_selection_list()
                return

            # Switch to "GPU" tab
            elif "selected" in self.gpu_tb.state():
                self.gpu_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 5
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 5
                if "Gpu" not in globals():
                    global Gpu
                    from .Gpu import Gpu
                if Gpu.initial_already_run == 0:
                    Gpu.initial_func()
                Gpu.loop_func()
                try:
                    self.main_gui_device_selection_list()
                except AttributeError:
                    pass
                return

            # Switch to "Sensors" tab
            elif "selected" in self.sensors_tb.state():
                self.sensors_tab_main_frame.tkraise()
                if Config.remember_last_opened_tabs == 1:
                    Config.performance_tab_default_sub_tab = 6
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 6
                if "Sensors" not in globals():
                    global Sensors
                    from .Sensors import Sensors
                if Sensors.initial_already_run == 0:
                    Sensors.initial_func()
                Sensors.loop_func()
                self.main_gui_device_selection_list()
                return

        # Switch to "Processes" tab
        elif "selected" in self.processes_tb.state():
            self.processes_tab_main_frame.tkraise()
            if Config.remember_last_opened_tabs == 1:
                Config.default_main_tab = 1
                Config.config_save_func()
            Config.current_main_tab = 1
            if "Processes" not in globals():
                global Processes
                from .Processes import Processes
            if Processes.initial_already_run == 0:
                Processes.initial_func()
            Processes.loop_func()
            return

        # Switch to "Users" tab
        elif "selected" in self.users_tb.state():
            self.users_tab_main_frame.tkraise()
            if Config.remember_last_opened_tabs == 1:
                Config.default_main_tab = 2
                Config.config_save_func()
            Config.current_main_tab = 2
            if "Users" not in globals():
                global Users
                from .Users import Users
            if Users.initial_already_run == 0:
                Users.initial_func()
            Users.loop_func()
            return

        # Switch to "Services" tab
        elif "selected" in self.services_tb.state():
            self.services_tab_main_frame.tkraise()
            if Config.remember_last_opened_tabs == 1:
                Config.default_main_tab = 3
                Config.config_save_func()
            Config.current_main_tab = 3
            if "Services" not in globals():
                global Services
                from .Services import Services
            if Services.initial_already_run == 0:
                Services.initial_func()
            Services.loop_func()
            return

        # Switch to "System" tab
        elif "selected" in self.system_tb.state():
            self.system_tab_main_frame.tkraise()
            if Config.remember_last_opened_tabs == 1:
                Config.default_main_tab = 4
                Config.config_save_func()
            Config.current_main_tab = 4
            if "System" not in globals():
                global System
                from .System import System
            if System.initial_already_run == 0:
               System.initial_func()
            return


    def main_gui_device_selection_list(self):
        """
        Add device list into the listbox between the Performance tab sub-tab radiobuttons (CPU, Memory, etc.).
        """

        # Delete previous scrolledwindow and widgets in it in order to add a new one again.
        # Otherwise, removing all of the listbox rows requires removing them one by one.
        try:
            self.device_list_sw.destroy()
            # It has to be deleted after removal in order to prevent Gtk warnings when new one is added.
            del self.device_list_sw
        # Prevent error if this is the first tab switch and there is no scrolledwindow.
        except AttributeError:
            pass

        # Define variables for to be used for adding devices to list.
        # Check if Summary tab is selected.
        if Config.performance_tab_current_sub_tab == 0:
            device_list = [_tr("Summary")]
            selected_device = device_list[0]
            listbox_row_number = 1
            tooltip_text = ""

        # Check if CPU tab is selected.
        elif Config.performance_tab_current_sub_tab == 1:
            device_list = Performance.logical_core_list
            selected_device = Performance.selected_cpu_core
            listbox_row_number = 3
            tooltip_text = _tr("CPU core selection affects only frequency and cache memory information.")

        # Check if Memory tab is selected.
        elif Config.performance_tab_current_sub_tab == 2:
            device_list = [_tr("RAM") + "-" + _tr("Swap Memory")]
            selected_device = device_list[0]
            listbox_row_number = 5
            tooltip_text = ""

        # Check if Disk tab is selected.
        elif Config.performance_tab_current_sub_tab == 3:
            device_list_full = Performance.disk_list
            device_list = []
            for device in device_list_full:
                # Do not add the device into the listbox and skip to the next loop if
                # "hide_loop_ramdisk_zram_disks" option is enabled and device is a loop, ramdisk or zram device.
                if Config.hide_loop_ramdisk_zram_disks == 1:
                    if device.startswith("loop") == True or device.startswith("ram") == True or device.startswith("zram") == True:
                        continue
                device_list.append(device)
            # "selected_device" is get in a different way for Disk tab.
            # Because device list may be changed if "hide_loop_ramdisk_zram_disks" option is enabled.
            selected_device = Performance.selected_disk
            listbox_row_number = 7
            tooltip_text = ""

        # Check if Network tab is selected.
        elif Config.performance_tab_current_sub_tab == 4:
            device_list = Performance.network_card_list
            selected_device = Performance.selected_network_card
            listbox_row_number = 9
            tooltip_text = ""

        # Check if GPU tab is selected.
        elif Config.performance_tab_current_sub_tab == 5:
            device_list = Gpu.gpu_list
            selected_device = Gpu.selected_gpu
            listbox_row_number = 11
            tooltip_text = ""

        # Check if Sensors tab is selected.
        elif Config.performance_tab_current_sub_tab == 6:
            return

        # Generate new widgets.
        self.device_list_sw = ttk.Frame(self.sub_tab_tb_frame, height=130, width=70)
        self.device_list_sw.grid(row=listbox_row_number, column=0, sticky="nsew", padx=(8, 0), pady=0)
        #self.device_list_sw.columnconfigure(0, minsize=50)
        #self.device_list_sw.rowconfigure(0, minsize=130)
        self.device_list_sw.grid_propagate(0)
        # White dotted frames around the selection is hidden by using "activestyle".
        listbox = tk.Listbox(self.device_list_sw, selectmode="browse", selectbackground="#353535", highlightcolor="#353535", activestyle="none") # #292929
        listbox.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        tooltip = Common.tooltip(listbox, tooltip_text)

        self.device_list_sw.grid_columnconfigure(0, weight=1)
        self.device_list_sw.grid_rowconfigure(0, weight=1)

        # Add Scrollbars
        scrollbar_vertical = ttk.Scrollbar(self.device_list_sw, orient="vertical", command=listbox.yview)
        scrollbar_vertical.grid(row=0, column=1, sticky="ns", padx=0, pady=0)
        scrollbar_horizontal = ttk.Scrollbar(self.device_list_sw, orient="horizontal", command=listbox.xview)
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        listbox['yscrollcommand'] = scrollbar_vertical.set
        listbox['xscrollcommand'] = scrollbar_horizontal.set

        # Remove (hide) Scrollbars for first show after main window is opened.
        scrollbar_vertical.grid_remove()
        scrollbar_horizontal.grid_remove()

        # Show (add) Scrollbars if mouse arrow is inside its container.
        def show_scrollbars(event):
            scrollbar_vertical.grid(row=0, column=1, sticky="ns")
            scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        # Hide (remove) Scrollbars if mouse arrow is inside its container.
        def hide_scrollbars(event):
            scrollbar_vertical.grid_remove()
            scrollbar_horizontal.grid_remove()

        # Conect signals for auto show-hiding Scrollbars.
        self.device_list_sw.bind("<Enter>", show_scrollbars)
        listbox.bind("<Motion>", show_scrollbars)
        self.device_list_sw.bind("<Leave>", hide_scrollbars)

        # Run function when a listbox row is clicked.
        def on_row_activated(event):

            # Get selected device name.
            if listbox.curselection() == ():
                return
            selected_device = device_list[listbox.curselection()[0]]

            # Check if Summary tab is selected.
            if Config.performance_tab_current_sub_tab == 0:
                pass

            # Check if CPU tab is selected.
            elif Config.performance_tab_current_sub_tab == 1:
                # Set selected device.
                Config.selected_cpu_core = selected_device
                Performance.performance_set_selected_cpu_core_func()

                # Apply changes immediately (without waiting update interval).
                Cpu.initial_func()
                Cpu.loop_func()
                Config.config_save_func()

            # Check if Memory tab is selected.
            elif Config.performance_tab_current_sub_tab == 2:
                pass

            # Check if Disk tab is selected.
            elif Config.performance_tab_current_sub_tab == 3:
                Config.selected_disk = selected_device
                Performance.performance_set_selected_disk_func()

                # Apply changes immediately (without waiting update interval).
                Disk.initial_func()
                Disk.loop_func()
                Config.config_save_func()

            # Check if Network tab is selected.
            elif Config.performance_tab_current_sub_tab == 4:
                Config.selected_network_card = selected_device
                Performance.performance_set_selected_network_card_func()

                # Apply changes immediately (without waiting update interval).
                Network.initial_func()
                Network.loop_func()
                Config.config_save_func()

            # Check if GPU tab is selected.
            elif Config.performance_tab_current_sub_tab == 5:
                Config.selected_gpu = selected_device
                Libsysmon.get_gpu_list_and_boot_vga()

                # Apply changes immediately (without waiting update interval).
                Gpu.initial_func()
                Gpu.loop_func()
                Config.config_save_func()

            # Check if Sensors tab is selected.
            elif Config.performance_tab_current_sub_tab == 6:
                pass

        # Add devices to listbox.
        for i, device in enumerate(device_list):
            listbox.insert(i+1, device)

        # Connect signal for the listbox.
        listbox.bind('<<ListboxSelect>>', on_row_activated)

        selected_device_number = device_list.index(selected_device)

        try:
            listbox.selection_set(selected_device_number)
            # Scroll to the selected row.
            listbox.see(selected_device_number)
        # Prevent error if a disk is hidden by changing the relevant option while it was selected.
        # There is no need to update the list from this function because it will be set as hidden in the list
        # by another function (in Disk module) immediately.
        except IndexError:
            pass


    def hide_services_tab(self):
        """
        Hide Services tab if systemd is not used on the system.
        """

        init_system = Libsysmon.get_init_system()
        Config.init_system = init_system

        if init_system != "systemd":
            self.services_tb.grid_remove()
            self.system_tb.grid(row=0, column=3, sticky="ew", padx=0, pady=0)
            self.main_tab_tb_frame.columnconfigure((0, 1, 2, 3, 4), minsize=165, uniform="equal")
            self.main_tab_tb_frame.columnconfigure(4, minsize=0, uniform="not_equal")


    def unified_tab_device_list_width(self):
        """
        Set width of the unified tab name-device list width by checking disk name lenghts.
        Some disks such as NVME disks may have very long names such as "nvme2n2p10".
        """

        disk_name_length_list = []
        for disk in Performance.disk_list:
            disk_name_length_list.append(len(disk))

        max_disk_name_lenght = max(disk_name_length_list)
        if max_disk_name_lenght > 6:
            # Length value for text based widgets are calculated by number of characters.
            self.summary_tb.config(width=9)


    def switch_to_default_tab(self):
        """
        Switches to default main tab and sub-tab on initial run.
        This function have to be run before "main_gui_tab_loop" function.
        """

        self.main_tab_var.set(Config.default_main_tab)
        self.sub_tab_var.set(Config.performance_tab_default_sub_tab)


    def main_gui_tab_loop(self):
        """
        Called for running loop functions of opened tabs to get performance/usage data.
        """

        Performance.loop_func()

        self.performance_summary_headerbar_loop()

        if Config.current_main_tab == 0:
            if Config.performance_tab_current_sub_tab == 0:
                try:
                    Summary.loop_func()
                except NameError:
                    pass
            elif Config.performance_tab_current_sub_tab == 1:
                Cpu.loop_func()
            elif Config.performance_tab_current_sub_tab == 2:
                Memory.loop_func()
            elif Config.performance_tab_current_sub_tab == 3:
                Disk.loop_func()
            elif Config.performance_tab_current_sub_tab == 4:
                Network.loop_func()
            elif Config.performance_tab_current_sub_tab == 5:
                Gpu.loop_func()
            elif Config.performance_tab_current_sub_tab == 6:
                Sensors.loop_func()
        elif Config.current_main_tab == 1:
            Processes.loop_func()
        elif Config.current_main_tab == 2:
            Users.loop_func()
        elif Config.current_main_tab == 3:
            Services.loop_func()
        elif Config.current_main_tab == 4:
            System.loop_func()

        # Delete previous loop in order to prevent multiple calls of the function when Refresh button is pressed repeatedly
        # or some settings are changed from Settings window.
        try:
            self.main_window.after_cancel(self.loop_id)
        except AttributeError:
            pass
        # Define loop_id in order to delete it and start a new loop to avoid multiple loops.
        self.loop_id = self.main_window.after(int(Config.update_interval*1000), self.main_gui_tab_loop)


    def performance_summary_headerbar_loop(self):
        """
        Loop function of performance summary on window headerbar.
        Update performance data on the headerbar.
        """

        selected_disk = Performance.selected_disk
        selected_network_card = Performance.selected_network_card
        Performance.performance_bar_charts_draw(self.ps_hb_cpu_da, "ps_hb_cpu_da")
        Performance.performance_bar_charts_draw(self.ps_hb_ram_da, "ps_hb_ram_da")
        self.ps_hb_disk_label.config(text=f'{Libsysmon.data_unit_converter("speed", Config.performance_disk_speed_bit, (Performance.disk_read_speed[selected_disk][-1] + Performance.disk_write_speed[selected_disk][-1]), Config.performance_disk_data_unit, 1)}/s')
        self.ps_hb_network_label.config(text=f'{Libsysmon.data_unit_converter("speed", Config.performance_network_speed_bit, (Performance.network_receive_speed[selected_network_card][-1] + Performance.network_send_speed[selected_network_card][-1]), Config.performance_network_data_unit, 1)}/s')


MainWindow = MainWindow()

