#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Config import Config
#from Processes import Processes
import Processes


# Define class
class ProcessesMenuCustomizations:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesMenuCustomizations.ui")

        # Get GUI objects
        self.popover2101p = builder.get_object('popover2101p')
        self.checkbutton2101p = builder.get_object('checkbutton2101p')
        self.checkbutton2102p = builder.get_object('checkbutton2102p')
        self.checkbutton2103p = builder.get_object('checkbutton2103p')
        self.button2102p = builder.get_object('button2102p')
        self.checkbutton2106p = builder.get_object('checkbutton2106p')
        self.checkbutton2107p = builder.get_object('checkbutton2107p')
        self.checkbutton2108p = builder.get_object('checkbutton2108p')
        self.checkbutton2109p = builder.get_object('checkbutton2109p')
        self.checkbutton2110p = builder.get_object('checkbutton2110p')
        self.checkbutton2111p = builder.get_object('checkbutton2111p')
        self.checkbutton2112p = builder.get_object('checkbutton2112p')
        self.checkbutton2113p = builder.get_object('checkbutton2113p')
        self.checkbutton2114p = builder.get_object('checkbutton2114p')
        self.checkbutton2115p = builder.get_object('checkbutton2115p')
        self.checkbutton2116p = builder.get_object('checkbutton2116p')
        self.checkbutton2117p = builder.get_object('checkbutton2117p')
        self.checkbutton2118p = builder.get_object('checkbutton2118p')
        self.checkbutton2119p = builder.get_object('checkbutton2119p')
        self.checkbutton2120p = builder.get_object('checkbutton2120p')
        self.checkbutton2121p = builder.get_object('checkbutton2121p')
        self.checkbutton2122p = builder.get_object('checkbutton2122p')
        self.checkbutton2123p = builder.get_object('checkbutton2123p')
        self.checkbutton2124p = builder.get_object('checkbutton2124p')
        self.combobox2101p = builder.get_object('combobox2101p')
        self.combobox2102p = builder.get_object('combobox2102p')
        self.combobox2103p = builder.get_object('combobox2103p')
        self.radiobutton2101p = builder.get_object('radiobutton2101p')
        self.radiobutton2102p = builder.get_object('radiobutton2102p')
        self.radiobutton2103p = builder.get_object('radiobutton2103p')
        self.radiobutton2104p = builder.get_object('radiobutton2104p')
        self.checkbutton2128p = builder.get_object('checkbutton2128p')

        # Connect GUI signals
        self.popover2101p.connect("show", self.on_popover2101p_show)
        self.button2102p.connect("clicked", self.on_button2102p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def processes_tab_customization_popover_connect_signals_func(self):

        self.checkbutton2101p.connect("toggled", self.on_checkbutton2101p_toggled)
        self.checkbutton2102p.connect("toggled", self.on_checkbutton2102p_toggled)
        self.checkbutton2103p.connect("toggled", self.on_checkbutton2103p_toggled)
        self.checkbutton2106p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2107p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2108p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2109p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2110p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2111p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2112p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2113p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2114p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2115p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2116p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2117p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2118p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2119p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2120p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2121p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2122p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2123p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2124p.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.combobox2101p.connect("changed", self.on_combobox2101p_changed)
        self.combobox2102p.connect("changed", self.on_combobox2102p_changed)
        self.combobox2103p.connect("changed", self.on_combobox2103p_changed)
        self.radiobutton2101p.connect("toggled", self.on_memory_data_unit_radiobuttons_toggled)
        self.radiobutton2102p.connect("toggled", self.on_memory_data_unit_radiobuttons_toggled)
        self.radiobutton2103p.connect("toggled", self.on_disk_data_unit_radiobuttons_toggled)
        self.radiobutton2104p.connect("toggled", self.on_disk_data_unit_radiobuttons_toggled)
        self.checkbutton2128p.connect("toggled", self.on_checkbutton2128p_toggled)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def processes_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton2101p.disconnect_by_func(self.on_checkbutton2101p_toggled)
        self.checkbutton2102p.disconnect_by_func(self.on_checkbutton2102p_toggled)
        self.checkbutton2103p.disconnect_by_func(self.on_checkbutton2103p_toggled)
        self.checkbutton2106p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2107p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2108p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2109p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2110p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2111p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2112p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2113p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2114p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2115p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2116p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2117p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2118p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2119p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2120p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2121p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2122p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2123p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.checkbutton2124p.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.combobox2101p.disconnect_by_func(self.on_combobox2101p_changed)
        self.combobox2102p.disconnect_by_func(self.on_combobox2102p_changed)
        self.combobox2103p.disconnect_by_func(self.on_combobox2103p_changed)
        self.radiobutton2101p.disconnect_by_func(self.on_memory_data_unit_radiobuttons_toggled)
        self.radiobutton2102p.disconnect_by_func(self.on_memory_data_unit_radiobuttons_toggled)
        self.radiobutton2103p.disconnect_by_func(self.on_disk_data_unit_radiobuttons_toggled)
        self.radiobutton2104p.disconnect_by_func(self.on_disk_data_unit_radiobuttons_toggled)
        self.checkbutton2128p.disconnect_by_func(self.on_checkbutton2128p_toggled)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover2101p_show(self, widget):
 
        try:
            self.processes_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.processes_tab_popover_set_gui()
        self.processes_tab_customization_popover_connect_signals_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button2102p_clicked(self, widget):

        # Load default settings
        Config.config_default_processes_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        self.processes_tab_customization_popover_disconnect_signals_func()
        self.processes_tab_popover_set_gui()
        self.processes_tab_customization_popover_connect_signals_func()


    # ----------------------- "Show processes of all users" Checkbutton -----------------------
    def on_checkbutton2101p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_processes_of_all_users = 1
        if widget.get_active() == False:
            Config.show_processes_of_all_users = 0

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Show processes as tree" Checkbutton -----------------------
    def on_checkbutton2102p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_processes_as_tree = 1
            self.checkbutton2103p.set_sensitive(True)
        if widget.get_active() == False:
            Config.show_processes_as_tree = 0
            self.checkbutton2103p.set_sensitive(False)

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Show tree lines" Checkbutton -----------------------
    def on_checkbutton2103p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_tree_lines = 1
        if widget.get_active() == False:
            Config.show_tree_lines = 0

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Add/Remove Columns (Name, PID, Username, etc.)" Checkbuttons -----------------------
    def on_add_remove_checkbuttons_toggled(self, widget):

        self.processes_add_remove_columns_function()


    # ----------------------- "CPU precision" Combobox -----------------------
    def on_combobox2101p_changed(self, widget):

        Config.processes_cpu_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Memory precision" Combobox -----------------------
    def on_combobox2102p_changed(self, widget):

        Config.processes_memory_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Disk precision" Combobox -----------------------
    def on_combobox2103p_changed(self, widget):

        Config.processes_disk_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Show units as powers of: 1024 or 1000 (for Memory)" Radiobuttons -----------------------
    def on_memory_data_unit_radiobuttons_toggled(self, widget):

        if self.radiobutton2101p.get_active() == True:
            Config.processes_memory_data_unit = 0
        elif self.radiobutton2102p.get_active() == True:
            Config.processes_memory_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Show units as powers of: 1024 or 1000 (for Disk)" Radiobuttons -----------------------
    def on_disk_data_unit_radiobuttons_toggled(self, widget):

        if self.radiobutton2103p.get_active() == True:
            Config.processes_disk_data_unit = 0
        elif self.radiobutton2104p.get_active() == True:
            Config.processes_disk_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- "Show speed units as multiples of bits (for Disk)" Checkbutton -----------------------
    def on_checkbutton2128p_toggled(self, widget):

        if widget.get_active() == True:
            Config.processes_disk_speed_bit = 1
        else:
            Config.processes_disk_speed_bit = 0

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def processes_tab_popover_set_gui(self):

        # Set GUI objects on View tab
        if Config.show_processes_of_all_users == 1:
            self.checkbutton2101p.set_active(True)
        if Config.show_processes_of_all_users == 0:
            self.checkbutton2101p.set_active(False)
        if Config.show_processes_as_tree == 1:
            self.checkbutton2102p.set_active(True)
            self.checkbutton2103p.set_sensitive(True)
        if Config.show_processes_as_tree == 0:
            self.checkbutton2102p.set_active(False)
            self.checkbutton2103p.set_sensitive(False)
        if Config.show_tree_lines == 1:
            self.checkbutton2103p.set_active(True)
        if Config.show_tree_lines == 0:
            self.checkbutton2103p.set_active(False)

        # Set GUI objects on Add/Remove Column tab
        if 0 in Config.processes_treeview_columns_shown:
            self.checkbutton2106p.set_active(True)
        else:
            self.checkbutton2106p.set_active(False)
        if 1 in Config.processes_treeview_columns_shown:
            self.checkbutton2107p.set_active(True)
        else:
            self.checkbutton2107p.set_active(False)
        if 2 in Config.processes_treeview_columns_shown:
            self.checkbutton2108p.set_active(True)
        else:
            self.checkbutton2108p.set_active(False)
        if 3 in Config.processes_treeview_columns_shown:
            self.checkbutton2109p.set_active(True)
        else:
            self.checkbutton2109p.set_active(False)
        if 4 in Config.processes_treeview_columns_shown:
            self.checkbutton2110p.set_active(True)
        else:
            self.checkbutton2110p.set_active(False)
        if 5 in Config.processes_treeview_columns_shown:
            self.checkbutton2111p.set_active(True)
        else:
            self.checkbutton2111p.set_active(False)
        if 6 in Config.processes_treeview_columns_shown:
            self.checkbutton2112p.set_active(True)
        else:
            self.checkbutton2112p.set_active(False)
        if 7 in Config.processes_treeview_columns_shown:
            self.checkbutton2113p.set_active(True)
        else:
            self.checkbutton2113p.set_active(False)
        if 8 in Config.processes_treeview_columns_shown:
            self.checkbutton2114p.set_active(True)
        else:
            self.checkbutton2114p.set_active(False)
        if 9 in Config.processes_treeview_columns_shown:
            self.checkbutton2115p.set_active(True)
        else:
            self.checkbutton2115p.set_active(False)
        if 10 in Config.processes_treeview_columns_shown:
            self.checkbutton2116p.set_active(True)
        else:
            self.checkbutton2116p.set_active(False)
        if 11 in Config.processes_treeview_columns_shown:
            self.checkbutton2117p.set_active(True)
        else:
            self.checkbutton2117p.set_active(False)
        if 12 in Config.processes_treeview_columns_shown:
            self.checkbutton2118p.set_active(True)
        else:
            self.checkbutton2118p.set_active(False)
        if 13 in Config.processes_treeview_columns_shown:
            self.checkbutton2119p.set_active(True)
        else:
            self.checkbutton2119p.set_active(False)
        if 14 in Config.processes_treeview_columns_shown:
            self.checkbutton2120p.set_active(True)
        else:
            self.checkbutton2120p.set_active(False)
        if 15 in Config.processes_treeview_columns_shown:
            self.checkbutton2121p.set_active(True)
        else:
            self.checkbutton2121p.set_active(False)
        if 16 in Config.processes_treeview_columns_shown:
            self.checkbutton2122p.set_active(True)
        else:
            self.checkbutton2122p.set_active(False)
        if 17 in Config.processes_treeview_columns_shown:
            self.checkbutton2123p.set_active(True)
        else:
            self.checkbutton2123p.set_active(False)
        if 18 in Config.processes_treeview_columns_shown:
            self.checkbutton2124p.set_active(True)
        else:
            self.checkbutton2124p.set_active(False)

        # Set GUI objects on Precision/Data Units tab 
        # Set data unit checkboxes.
        if Config.processes_memory_data_unit == 0:
            self.radiobutton2101p.set_active(True)
        if Config.processes_memory_data_unit == 1:
            self.radiobutton2102p.set_active(True)
        if Config.processes_disk_data_unit == 0:
            self.radiobutton2103p.set_active(True)
        if Config.processes_disk_data_unit == 1:
            self.radiobutton2104p.set_active(True)
        if Config.processes_disk_speed_bit == 1:
            self.checkbutton2128p.set_active(True)
        if Config.processes_disk_speed_bit == 0:
            self.checkbutton2128p.set_active(False)

        # Add CPU usage precision data into combobox
        liststore2101p = Gtk.ListStore()
        liststore2101p.set_column_types([str, int])
        self.combobox2101p.set_model(liststore2101p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2101p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2101p.pack_start(renderer_text, True)
        self.combobox2101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2101p.append([data[1], data[2]])
        self.combobox2101p.set_active(Config.processes_cpu_precision)

        # Add Memory data precision data into combobox
        liststore2102p = Gtk.ListStore()
        liststore2102p.set_column_types([str, int])
        self.combobox2102p.set_model(liststore2102p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2102p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2102p.pack_start(renderer_text, True)
        self.combobox2102p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2102p.append([data[1], data[2]])
        self.combobox2102p.set_active(Config.processes_memory_data_precision)

        # Add Disk data precision data into combobox
        liststore2103p = Gtk.ListStore()
        liststore2103p.set_column_types([str, int])
        self.combobox2103p.set_model(liststore2103p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2103p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2103p.pack_start(renderer_text, True)
        self.combobox2103p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2103p.append([data[1], data[2]])
        self.combobox2103p.set_active(Config.processes_disk_data_precision)


    # ----------------------- Called for adding/removing treeview columns -----------------------
    def processes_add_remove_columns_function(self):

        Config.processes_treeview_columns_shown = []

        if self.checkbutton2106p.get_active() == True:
            Config.processes_treeview_columns_shown.append(0)
        if self.checkbutton2107p.get_active() == True:
            Config.processes_treeview_columns_shown.append(1)
        if self.checkbutton2108p.get_active() == True:
            Config.processes_treeview_columns_shown.append(2)
        if self.checkbutton2109p.get_active() == True:
            Config.processes_treeview_columns_shown.append(3)
        if self.checkbutton2110p.get_active() == True:
            Config.processes_treeview_columns_shown.append(4)
        if self.checkbutton2111p.get_active() == True:
            Config.processes_treeview_columns_shown.append(5)
        if self.checkbutton2112p.get_active() == True:
            Config.processes_treeview_columns_shown.append(6)
        if self.checkbutton2113p.get_active() == True:
            Config.processes_treeview_columns_shown.append(7)
        if self.checkbutton2114p.get_active() == True:
            Config.processes_treeview_columns_shown.append(8)
        if self.checkbutton2115p.get_active() == True:
            Config.processes_treeview_columns_shown.append(9)
        if self.checkbutton2116p.get_active() == True:
            Config.processes_treeview_columns_shown.append(10)
        if self.checkbutton2117p.get_active() == True:
            Config.processes_treeview_columns_shown.append(11)
        if self.checkbutton2118p.get_active() == True:
            Config.processes_treeview_columns_shown.append(12)
        if self.checkbutton2119p.get_active() == True:
            Config.processes_treeview_columns_shown.append(13)
        if self.checkbutton2120p.get_active() == True:
            Config.processes_treeview_columns_shown.append(14)
        if self.checkbutton2121p.get_active() == True:
            Config.processes_treeview_columns_shown.append(15)
        if self.checkbutton2122p.get_active() == True:
            Config.processes_treeview_columns_shown.append(16)
        if self.checkbutton2123p.get_active() == True:
            Config.processes_treeview_columns_shown.append(17)
        if self.checkbutton2124p.get_active() == True:
            Config.processes_treeview_columns_shown.append(18)

        # Apply changes immediately (without waiting update interval).
        Processes.processes_treeview_column_order_width_row_sorting_func()
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


# Generate object
ProcessesMenuCustomizations = ProcessesMenuCustomizations()

