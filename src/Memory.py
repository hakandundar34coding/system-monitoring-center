import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Memory:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.da_grid()

        self.information_grid()


    def tab_title_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Memory)
        label = Common.tab_title_label(_tr("Memory"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label()
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label()
        grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.tab_grid.attach(grid, 0, 1, 1, 1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(_tr("RAM Usage"), Gtk.Align.START)
        grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea (RAM/Memory usage)
        self.da_memory_usage = Common.drawingarea(Performance.performance_line_charts_draw, "da_memory_usage")
        grid.attach(self.da_memory_usage, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Common.performance_info_grid()
        performance_info_grid.set_row_homogeneous(False)
        performance_info_grid.set_row_spacing(6)
        self.tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Label - Title (RAM)
        label = Common.title_label(_tr("RAM"))
        performance_info_grid.attach(label, 0, 0, 1, 1)

        # Styled information widgets (Used and Available)
        # ScrolledWindow (Used and Available)
        scrolledwindow, self.ram_used_label, self.ram_available_label = Common.styled_information_scrolledwindow(_tr("Used"), None, _tr("Available"), None)
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Grid - Lower left information labels
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(2)
        grid.set_row_spacing(3)
        performance_info_grid.attach(grid, 0, 2, 1, 1)

        # Label (Capacity)
        label = Common.static_information_label(_tr("Capacity") + ":")
        grid.attach(label, 0, 0, 1, 1)
        # Label (Capacity)
        self.ram_capacity_label = Common.dynamic_information_label()
        grid.attach(self.ram_capacity_label, 1, 0, 1, 1)

        # Label (Free)
        label = Common.static_information_label(_tr("Free") + ":")
        grid.attach(label, 0, 1, 1, 1)
        # Label (Free)
        self.ram_free_label = Common.dynamic_information_label()
        grid.attach(self.ram_free_label, 1, 1, 1, 1)

        # Label (Hardware)
        label = Common.static_information_label(_tr("Hardware") + ":")
        grid.attach(label, 0, 2, 1, 1)
        # Label (Show...)
        self.ram_hardware_label = Common.clickable_label(_tr("Show..."), self.on_details_label_released)
        grid.attach(self.ram_hardware_label, 1, 2, 1, 1)

        # Label - Title (Swap Memory)
        label = Common.title_label(_tr("Swap Memory"))
        performance_info_grid.attach(label, 1, 0, 1, 1)

        # Styled information widgets (Used and Free)
        # ScrolledWindow (Used and Free)
        scrolledwindow, self.swap_used_label, self.swap_free_label = Common.styled_information_scrolledwindow(_tr("Used"), None, _tr("Free"), None)
        performance_info_grid.attach(scrolledwindow, 1, 1, 1, 1)

        # Grid (lower right information labels)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(2)
        grid.set_row_spacing(3)
        performance_info_grid.attach(grid, 1, 2, 1, 1)

        # Label (Used (swap percent))
        label = Common.static_information_label(_tr("Used") + ":")
        grid.attach(label, 0, 0, 1, 1)
        # Label and DrawingArea (Used (swap percent))
        grid_label_and_da = Gtk.Grid()
        grid_label_and_da.set_column_spacing(5)
        grid.attach(grid_label_and_da, 1, 0, 1, 1)
        # DrawingArea (Used (swap percent))
        self.da_swap_usage = Common.drawingarea(Performance.performance_bar_charts_draw, "da_swap_usage")
        self.da_swap_usage.set_vexpand(False)
        grid_label_and_da.attach(self.da_swap_usage, 0, 0, 1, 1)
        # Label (Used (swap percent))
        self.swap_used_percent_label = Common.dynamic_information_label()
        grid_label_and_da.attach(self.swap_used_percent_label, 1, 0, 1, 1)

        # Label (Capacity (swap))
        label = Common.static_information_label(_tr("Capacity") + ":")
        grid.attach(label, 0, 1, 1, 1)
        # Label (Capacity (swap))
        self.swap_capacity_label = Common.dynamic_information_label()
        grid.attach(self.swap_capacity_label, 1, 1, 1, 1)

        # Label (Details (swap))
        label = Common.static_information_label(_tr("Details") + ":")
        grid.attach(label, 0, 2, 1, 1)
        # Label (Show... (swap))
        self.swap_details_label = Common.clickable_label(_tr("Show..."), self.on_details_label_released)
        grid.attach(self.swap_details_label, 1, 2, 1, 1)


    def on_details_label_released(self, event, count, x, y):
        """
        Show RAM hardware window or swap details window.
        """

        widget = event.get_widget()

        # Show RAM hardware window
        if widget == self.ram_hardware_label:
            memory_ram_hardware_info = Libsysmon.get_ram_hardware_info()
            try:
                self.ram_hardware_window.present()
            except AttributeError:
                # Avoid generating window multiple times on every button click.
                self.ram_hardware_window_gui()
                self.ram_hardware_window.present()
            self.ram_hardware_win_label.set_label(memory_ram_hardware_info)

        # Show swap details window
        if widget == self.swap_details_label:
            try:
                self.swap_details_window.present()
            except AttributeError:
                # Avoid generating window multiple times on every button click.
                self.swap_details_window_gui()
                self.swap_details_window.present()
            memory_swap_details_info = Libsysmon.get_swap_details_info(Config.performance_memory_data_precision, Config.performance_memory_data_unit)
            self.swap_details_win_label.set_label(memory_swap_details_info)
            self.swap_details_update()


    def ram_hardware_window_gui(self):
        """
        RAM hardware window GUI.
        """

        # Window
        self.ram_hardware_window = Gtk.Window()
        self.ram_hardware_window.set_default_size(400, 480)
        self.ram_hardware_window.set_title(_tr("Physical RAM"))
        self.ram_hardware_window.set_icon_name("system-monitoring-center")
        self.ram_hardware_window.set_transient_for(MainWindow.main_window)
        self.ram_hardware_window.set_modal(True)
        self.ram_hardware_window.set_hide_on_close(True)

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.ram_hardware_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid (Main)
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        viewport.set_child(main_grid)

        # Label
        self.ram_hardware_win_label = Gtk.Label()
        self.ram_hardware_win_label.set_halign(Gtk.Align.START)
        self.ram_hardware_win_label.set_valign(Gtk.Align.START)
        self.ram_hardware_win_label.set_selectable(True)
        self.ram_hardware_win_label.set_label("--")
        main_grid.attach(self.ram_hardware_win_label, 0, 0, 1, 1)


    def swap_details_window_gui(self):
        """
        Swap details window GUI.
        """

        # Window
        self.swap_details_window = Gtk.Window()
        self.swap_details_window.set_default_size(320, 280)
        self.swap_details_window.set_title(_tr("Swap Memory"))
        self.swap_details_window.set_icon_name("system-monitoring-center")
        self.swap_details_window.set_transient_for(MainWindow.main_window)
        self.swap_details_window.set_modal(True)
        self.swap_details_window.set_hide_on_close(True)

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.swap_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        viewport.set_child(main_grid)

        # Label
        self.swap_details_win_label = Gtk.Label()
        self.swap_details_win_label.set_halign(Gtk.Align.START)
        self.swap_details_win_label.set_valign(Gtk.Align.START)
        self.swap_details_win_label.set_selectable(True)
        self.swap_details_win_label.set_label("--")
        main_grid.attach(self.swap_details_win_label, 0, 0, 1, 1)


    def swap_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        if self.swap_details_window.get_visible() == True:
            # Destroy GLib source for preventing it repeating the function.
            try:
                self.main_glib_source.destroy()
            # Prevent errors if this is first run of the function.
            except AttributeError:
                pass
            self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)
            memory_swap_details_info = Libsysmon.get_swap_details_info(Config.performance_memory_data_precision, Config.performance_memory_data_unit)
            self.swap_details_win_label.set_label(memory_swap_details_info)
            self.main_glib_source.set_callback(self.swap_details_update)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
            # A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # List for language translation
        memory_swap_details_text_list = [_tr("Partition"), _tr("File")]

        total_physical_ram = Libsysmon.get_physical_ram()


        # Set Memory tab label texts by using information get
        if total_physical_ram != "-":
            self.device_vendor_model_label.set_label(_tr("Physical RAM") + ": " + str(Libsysmon.data_unit_converter("data", "none", total_physical_ram, 0, 1)))
        else:
            self.device_vendor_model_label.set_label(_tr("RAM") + " - " + _tr("Capacity") + ": " + str(Libsysmon.data_unit_converter("data", "none", ram_total, 0, 1)))

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        memory_info = Libsysmon.get_memory_info()

        ram_used = memory_info["ram_used"]
        ram_usage_percent = Performance.ram_usage_percent
        ram_available = memory_info["ram_available"]
        ram_free = memory_info["ram_free"]
        ram_total = memory_info["ram_total"]

        self.swap_usage_percent = Performance.swap_usage_percent
        swap_used = memory_info["swap_used"]
        swap_free = memory_info["swap_free"]
        swap_total = memory_info["swap_total"]

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        self.da_memory_usage.queue_draw()
        self.da_swap_usage.queue_draw()


        # Set and update Memory tab label texts by using information get
        self.device_kernel_name_label.set_label(_tr("Swap Memory") + ": " + str(Libsysmon.data_unit_converter("data", "none", swap_total, 0, 1)))
        self.ram_used_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", ram_used, performance_memory_data_unit, performance_memory_data_precision)}  ( {ram_usage_percent[-1]:.0f}% )')
        self.ram_available_label.set_label(Libsysmon.data_unit_converter("data", "none", ram_available, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_capacity_label.set_label(Libsysmon.data_unit_converter("data", "none", ram_total, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_free_label.set_label(Libsysmon.data_unit_converter("data", "none", ram_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_used_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}  ( {self.swap_usage_percent[-1]:.0f}% )')
        self.swap_used_percent_label.set_label(f'{self.swap_usage_percent[-1]:.0f}%')
        self.swap_free_label.set_label(Libsysmon.data_unit_converter("data", "none", swap_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_capacity_label.set_label(Libsysmon.data_unit_converter("data", "none", swap_total, performance_memory_data_unit, performance_memory_data_precision))


Memory = Memory()

