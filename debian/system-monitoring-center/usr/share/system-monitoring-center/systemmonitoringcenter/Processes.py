import tkinter as tk
from tkinter import ttk, messagebox

import os
import time
import subprocess
from datetime import datetime

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Processes:

    def __init__(self):

        self.name = "Processes"

        self.tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.processes_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.information_frame()

        self.right_click_menu_gui()

        # Set initial value for process searching.
        self.process_search_type = "name"


    def tab_title_frame(self):
        """
        Generate tab name label, searchentry.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        # Label (Processes)
        label = Common.tab_title_label(frame, _tr("Processes"))

        # Grid (search widgets)
        search_frame = ttk.Frame(frame)
        search_frame.columnconfigure(0, weight=1)
        search_frame.grid(row=0, column=1, sticky="ew", padx=0, pady=0)

        # SearchEntry
        self.searchentry, self.searchentry_text_var = Common.searchentry(search_frame, self)
        self.searchentry.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # MenuButton (search customization)
        image = tk.PhotoImage(file=MainWindow.image_path + "smc-search.png")
        image = image.subsample(3, 3)
        self.search_customization_menubutton = ttk.Menubutton(search_frame, image=image, style="Toggle.TButton")
        self.search_customization_menubutton.image = image
        self.search_customization_menubutton.grid(row=0, column=1, sticky="w", padx=(3, 0), pady=0)

        # Search customization Menu
        self.search_customization_menubutton_var = tk.StringVar()
        self.search_customization_menubutton.menu = tk.Menu(self.search_customization_menubutton, tearoff=False)
        self.search_customization_menubutton["menu"] = self.search_customization_menubutton.menu
        self.search_customization_menubutton.menu.add_radiobutton(label=_tr("All"), activebackground="gray", variable=self.search_customization_menubutton_var, value="all", command=lambda: self.on_search_menu_cb_toggled("all"))
        self.search_customization_menubutton.menu.add_radiobutton(label=_tr("Name"), activebackground="gray", variable=self.search_customization_menubutton_var, value="name" , command=lambda: self.on_search_menu_cb_toggled("name"))
        self.search_customization_menubutton.menu.add_radiobutton(label=_tr("Command Line"), activebackground="gray", variable=self.search_customization_menubutton_var, value="command_line", command=lambda: self.on_search_menu_cb_toggled("command_line"))
        self.search_customization_menubutton.menu.add_radiobutton(label=_tr("PID"), activebackground="gray", variable=self.search_customization_menubutton_var, value="pid", command=lambda: self.on_search_menu_cb_toggled("pid"))
        self.search_customization_menubutton_var.set("name")


    def information_frame(self):
        """
        Generate information GUI objects.
        """

        # TreeView
        self.treeview, frame = Common.treeview(self.tab_frame, self)
        self.treeview.config(selectmode="extended")
        self.treeview.config(padding=[-10,0,0,0])
        self.treeview.bind('<Control-s>', lambda e: self.on_process_manage_items_activate("pause_process"))
        self.treeview.bind('<Control-S>', lambda e: self.on_process_manage_items_activate("pause_process"))
        self.treeview.bind('<Control-c>', lambda e: self.on_process_manage_items_activate("continue_process"))
        self.treeview.bind('<Control-C>', lambda e: self.on_process_manage_items_activate("continue_process"))
        self.treeview.bind('<Control-e>', lambda e: self.on_process_manage_items_activate("end_process"))
        self.treeview.bind('<Control-E>', lambda e: self.on_process_manage_items_activate("end_process"))
        self.treeview.bind('<Control-k>', lambda e: self.on_process_manage_items_activate("end_immediately_process"))
        self.treeview.bind('<Control-K>', lambda e: self.on_process_manage_items_activate("end_immediately_process"))
        self.treeview.bind('<Control-p>', self.on_change_priority_item_clicked)
        self.treeview.bind('<Control-P>', self.on_change_priority_item_clicked)
        self.treeview.bind('<Control-r>', self.on_set_cpu_affinity_item_clicked)
        self.treeview.bind('<Control-R>', self.on_set_cpu_affinity_item_clicked)


    def right_click_menu_gui(self):
        """
        Generate right click menu GUI.
        """

        # Do not generate a new menu if it is generated before.
        if hasattr(self, "right_click_menu") == False:
            self.right_click_menu = tk.Menu(self.treeview, tearoff=False, bd=3, activebackground="gray")
            self.right_click_menu.add_command(label=_tr("Pause Process"), accelerator="(Ctrl+S)", command=lambda: self.on_process_manage_items_activate("pause_process"))
            self.right_click_menu.add_command(label=_tr("Continue Process"), accelerator="(Ctrl+C)", command=lambda: self.on_process_manage_items_activate("continue_process"))
            self.right_click_menu.add_command(label=_tr("End Process"), accelerator="(Ctrl+E)", command=lambda: self.on_process_manage_items_activate("end_process"))
            self.right_click_menu.add_command(label=_tr("End Process Immediately"), accelerator="(Ctrl+K)", command=lambda: self.on_process_manage_items_activate("end_immediately_process"))
            self.right_click_menu.add_separator()
            self.right_click_menu.add_command(label=_tr("Change Priority"), accelerator="(Ctrl+P)", command=self.on_change_priority_item_clicked)
            self.right_click_menu.add_separator()
            self.right_click_menu.add_command(label=_tr("Set CPU Affinity"), accelerator="(Ctrl+R)", command=self.on_set_cpu_affinity_item_clicked)
            self.right_click_menu.add_separator()
            self.right_click_menu.add_command(label=_tr("Details"), accelerator="(Enter)", command=self.on_details_item_activate)

        # Add/remove "Expand All/Collapse All"" options to menu if processes are listed as tree/list.
        if Config.show_processes_as_tree == 1:
            if self.right_click_menu.index(tk.END) == 9:
                self.right_click_menu.insert_command(0, label=_tr("Expand All"), command=self.treeview_expand_all_rows)
                self.right_click_menu.insert_command(1, label=_tr("Collapse All"), command=self.treeview_collapse_all_rows)
                self.right_click_menu.insert_separator(2)
                # Set properties again. It is reset after menu item added or removed.
                self.right_click_menu.config(bd=3, activebackground="gray", relief="raised")
        # Delete the first three options. Indexes are updated after inserting/removing options.
        else:
            # Prevent removing the other options if "Expand All/Collapse All"" options are not added.
            # Last option index is 12 if "Expand All/Collapse All"" options are added.
            if self.right_click_menu.index(tk.END) == 12:
                self.right_click_menu.delete(0)
                self.right_click_menu.delete(0)
                self.right_click_menu.delete(0)
                self.right_click_menu.config(bd=3, activebackground="gray", relief="raised")

        self.right_click_menu.bind("<FocusOut>", self.right_click_menu_close)

        self.treeview.bind("<Button-3>", self.on_right_click)
        self.treeview.bind("<Double-1>", self.treeview_double_click_event)
        self.treeview.bind("<Return>", self.treeview_enter_press_event)
        # Treeview "FocusOut" signal may not close right click menu if certain areas of the GUI is clicked. The following signal is used for fixing this issue.
        self.treeview.winfo_toplevel().bind("<Button-1>", self.right_click_menu_close)

        return self.right_click_menu


    def treeview_expand_all_rows(self):
        for child in self.treeview.get_children():
            self.treeview.item(child, open=True)

    def treeview_collapse_all_rows(self):
        for child in self.treeview.get_children():
            self.treeview.item(child, open=False)


    def on_change_priority_item_clicked(self, event=None):

        self.get_selection()

        process_name_pid_dict = {}
        for pid in self.selected_process_pid_list:
            process_name_pid_dict[pid] = self.rows_data_dict[pid]["name"]

        # Get PIDs of the processes
        selected_process_pids = list(process_name_pid_dict.keys())

        # Get process current priority value if one process is selected.
        if len(self.selected_process_pid_list) == 1:
            selected_process_nice = Libsysmon.get_process_priority(str(self.selected_process_pid_list[0]))
            if selected_process_nice == "-":
                return
        else:
            selected_process_nice = 0

        # Get process name and PID text for dialog.
        process_name_pid_text = ""
        for pid in self.selected_process_pid_list:
            process_name_pid_text = process_name_pid_text + "\n" + self.rows_data_dict[pid]["name"] + " (" + pid + ")"

        # Window
        self.priority_window, frame = Common.window(MainWindow.main_window, _tr("Change Priority"))

        # Frame (Main)
        frame.rowconfigure(2, weight=1)

        label = Common.static_information_label(frame, _tr("Change priority of these processes") + ":")
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=(0, 4))

        label = Common.static_information_label(frame, _tr("Smaller value means higher process priority") + ":")
        label.grid(row=1, column=0, columnspan=2, sticky="w", padx=0, pady=(0, 4))

        # Frame
        frame = ttk.Frame(frame, style="Card.TFrame")
        frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        label = Common.dynamic_information_label(frame)
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        label.config(text=process_name_pid_text)

        self.priority_var = tk.IntVar()
        self.priority_slider = tk.Scale(frame, from_=-20, to=19, orient="horizontal", variable=self.priority_var, command=self.show_priority_text, length=250, showvalue=True)
        self.priority_slider.grid(row=3, column=0, columnspan=2, sticky="ew", padx=0, pady=(0, 4))

        self.priority_var.set(selected_process_nice)

        self.show_priority_text_label = Common.dynamic_information_label(frame)
        self.show_priority_text_label.grid(row=4, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        cancel_button = ttk.Button(frame, text =_tr("Cancel"), command=self.cancel_priority_button)
        cancel_button.grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 4))

        change_priority_button = ttk.Button(frame, text =_tr("Change Priority"), command=self.on_change_priority_button)
        change_priority_button.grid(row=5, column=1, sticky="ew", padx=5, pady=(0, 4))

        self.show_priority_text(selected_process_nice)


    def show_priority_text(self, selected_process_nice):

        selected_process_nice = int(selected_process_nice)

        if selected_process_nice <= -11 and selected_process_nice >= -20:
            priority_text = _tr("Very High")
        if selected_process_nice < 0 and selected_process_nice > -11:
            priority_text = _tr("High")
        if selected_process_nice == 0:
            priority_text = _tr("Normal")
        if selected_process_nice < 11 and selected_process_nice > 0:
            priority_text = _tr("Low")
        if selected_process_nice <= 19 and selected_process_nice >= 11:
            priority_text = _tr("Very Low")

        self.show_priority_text_label.config(text=priority_text)


    def on_change_priority_button(self):

        Libsysmon.change_process_priority(self.selected_process_pid_list, str(self.priority_var.get()))
        self.priority_window.destroy()


    def cancel_priority_button(self):
        self.priority_window.destroy()


    def on_set_cpu_affinity_item_clicked(self, event=None):

        self.get_selection()

        # Get process current CPU affinity value if one process is selected.
        if len(self.selected_process_pid_list) == 1:
            selected_process_cpu_affinity = Libsysmon.get_process_cpu_affinity(str(self.selected_process_pid_list[0]))
            if selected_process_cpu_affinity == "-":
                return
        else:
            selected_process_cpu_affinity = "-"

        # Get process name and PID text for dialog.
        process_name_pid_text = ""
        for pid in self.selected_process_pid_list:
            process_name_pid_text = process_name_pid_text + "\n" + self.rows_data_dict[pid]["name"] + " (" + pid + ")"

        # Window
        self.cpu_affinity_window, frame = Common.window(MainWindow.main_window, _tr("Set CPU Affinity"))

        frame.rowconfigure(2, weight=1)

        label = Common.static_information_label(frame, _tr("Processes") + ":")
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=(0, 4))

        # Frame
        frame1 = ttk.Frame(frame, style="Card.TFrame")
        frame1.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        """frame1.columnconfigure(0, weight=1)
        frame1.rowconfigure(0, weight=1)"""

        label = Common.dynamic_information_label(frame1)
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=(0, 4))
        label.config(text=process_name_pid_text)

        frame2 = ttk.Frame(frame, style="Card.TFrame")
        frame2.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        select_all_button = ttk.Button(frame2, text =_tr("Select All"), command=self.cpu_affinity_select_all_button)
        select_all_button.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        select_none_button = ttk.Button(frame2, text =_tr("Select None"), command=self.cpu_affinity_select_none_button)
        select_none_button.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)


        number_of_all_logical_cores = Libsysmon.get_number_of_all_logical_cores()
        self.cpu_affinity_dict = {}
        for i in range(number_of_all_logical_cores):
            cpu_affinity_var = tk.IntVar()
            cpu_affinity_cb = Common.checkbutton(frame2, "core"+str(i), cpu_affinity_var, command=None)
            cpu_affinity_cb.grid(row=i, column=0, sticky="w", padx=0, pady=2)

            if selected_process_cpu_affinity == "-":
                cpu_affinity_var.set(0)
            if selected_process_cpu_affinity != "-":
                if i in selected_process_cpu_affinity:
                    cpu_affinity_var.set(1)
            self.cpu_affinity_dict["core"+str(i)] = {"variable": cpu_affinity_var, "checkbutton": cpu_affinity_cb}

        cancel_button = ttk.Button(frame, text =_tr("Cancel"), command=self.cancel_cpu_affinity_button)
        cancel_button.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 4))

        change_cpu_affinity_button = ttk.Button(frame, text =_tr("Set CPU Affinity"), command=self.on_change_cpu_affinity_button)
        change_cpu_affinity_button.grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 4))


    def cpu_affinity_select_all_button(self):
        for core in self.cpu_affinity_dict:
            checkbutton_var = self.cpu_affinity_dict[core]["variable"]
            checkbutton_var.set(1)

    def cpu_affinity_select_none_button(self):
        for core in self.cpu_affinity_dict:
            checkbutton_var = self.cpu_affinity_dict[core]["variable"]
            checkbutton_var.set(0)


    def on_change_cpu_affinity_button(self):

        cpu_core_list = []
        for core in self.cpu_affinity_dict:
            core_int = int(core.strip("core"))
            if self.cpu_affinity_dict[core]["variable"].get() == 1:
                cpu_core_list.append(core_int)

        Libsysmon.set_process_cpu_affinity(self.selected_process_pid_list, cpu_core_list)
        self.cpu_affinity_window.destroy()


    def cancel_cpu_affinity_button(self):

        self.cpu_affinity_window.destroy()


    def on_process_manage_items_activate(self, action_name):
        """
        Pause, continue, end, end immediately processes.
        """

        self.get_selection()

        process_name_pid_dict = {}
        for pid in self.selected_process_pid_list:
            process_name_pid_dict[pid] = self.rows_data_dict[pid]["name"]

        # Get PIDs of the processes
        selected_process_pids = list(process_name_pid_dict.keys())

        # Get process name and PID text for dialog.
        process_name_pid_text = ""
        for pid in self.selected_process_pid_list:
            process_name_pid_text = process_name_pid_text + "\n" + self.rows_data_dict[pid]["name"] + " (" + pid + ")"

        # Pause Process
        if action_name == "pause_process":
            process_command = ["kill", "-19"] + selected_process_pids
            process_command_pkexec = ["pkexec", "kill", "-19"] + selected_process_pids

        # Continue Process
        if action_name == "continue_process":
            process_command = ["kill", "-18"] + selected_process_pids
            process_command_pkexec = ["pkexec", "kill", "-18"] + selected_process_pids

        # End Process
        if action_name == "end_process":
            process_command = ["kill", "-15"] + selected_process_pids
            process_command_pkexec = ["pkexec", "kill", "-15"] + selected_process_pids
            process_dialog_message = _tr("Do you want to end these processes?")

        # End Process Immediately
        if action_name == "end_immediately_process":
            process_command = ["kill", "-9"] + selected_process_pids
            process_command_pkexec = ["pkexec", "kill", "-9"] + selected_process_pids
            process_dialog_message = _tr("Do you want to end these processes immediately?")

        if Libsysmon.get_environment_type == "flatpak":
            process_command = ["flatpak-spawn", "--host"] + process_command
            process_command_pkexec = ["flatpak-spawn", "--host"] + process_command_pkexec

        if action_name in ["pause_process", "continue_process"]:

            # Try to end the process without using root privileges.
            try:
                (subprocess.check_output(process_command, stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                # End the process if root privileges are given.
                try:
                    (subprocess.check_output(process_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                # Prevent errors if wrong password is used or polkit dialog is closed by user.
                except subprocess.CalledProcessError:
                    pass

        # Show warning dialog if process is tried to be ended.
        if Config.warn_before_stopping_processes == 1 and action_name in ["end_process", "end_immediately_process"]:
            answer = messagebox.askyesno("Warning", process_dialog_message + "\n\n" + process_name_pid_text + "\n")
            if answer == True:
                # Try to end the process without using root privileges.
                try:
                    (subprocess.check_output(process_command, stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    # End the process if root privileges are given.
                    try:
                        (subprocess.check_output(process_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                    # Prevent errors if wrong password is used or polkit dialog is closed by user.
                    except subprocess.CalledProcessError:
                        pass


    def get_selection2(self, event):

        self.selected_row_names = []
        region = self.treeview.identify_region(event.x, event.y)
        # Prevent running code if rows are not clicked.
        if region in ["cell", "tree"]:
            #self.selected_row_id = self.treeview.identify_row(event.y)
            self.selected_row_ids = self.treeview.selection()
            # Get right clicked row id.
            if self.selected_row_ids != ():
                # Select the row visually if right clicked on a row.
                # Get data of the selected row.
                for self.selected_row_id in self.selected_row_ids:
                    self.treeview.selection_set(self.selected_row_id)
                    self.selected_row_names.append(self.treeview.item(self.selected_row_id, "values")[0])

        return self.selected_row_names


    def on_right_click2(self, event):

        self.get_selection(event)
        # Show menu on mouse coordinates
        self.right_click_menu.post(event.x_root, event.y_root)
        self.right_click_menu.focus_set()


    def get_selection(self, event=None):

        selected_rows = self.treeview.selection()

        if not selected_rows:
            return

        self.selected_row_names = []
        for item in selected_rows:
            # -1 is used in order to get values from treeview.
            pid = self.treeview.item(item)['values'][Config.processes_columns_shown.index("pid") - 1]
            self.selected_row_names.append(str(pid))
            self.selected_process_pid_list = list(self.selected_row_names)


    def on_right_click(self, event):

        clicked_row = self.treeview.identify_row(event.y)
        
        if clicked_row:
            # Clear previous selection if right clicked row is not selected.
            if clicked_row not in self.treeview.selection():
                self.treeview.selection_set(clicked_row)
            self.right_click_menu_gui()
            self.right_click_menu.post(event.x_root, event.y_root)


    def right_click_menu_close(self, event):
        """
        Close right click menu if clicked another part of the GUI.
        """

        self.right_click_menu.unpost()


    def on_details_item_activate(self):
        """
        Show process details window.
        """

        """self.selected_row_names = []
        self.selected_row_ids = self.treeview.selection()
        # Get right clicked row id.
        if self.selected_row_ids != ():
            # Select the row visually if right clicked on a row.
            self.treeview.selection_set(self.selected_row_ids)
            # Get data of the selected row.
            for self.selected_row_id in self.selected_row_ids: 
                self.selected_row_names.append(self.treeview.item(self.selected_row_id, "values")[0])
        self.selected_process_pid_list = list(self.selected_row_names)"""
        self.get_selection()
        from .ProcessesDetails import ProcessesDetails
        ProcessesDetails.process_details_show_process_details()


    def treeview_double_click_event(self, event):

        region = self.treeview.identify_region(event.x, event.y)
        # Prevent running code if rows are not clicked.
        if region in ["cell", "tree"]:
            self.get_selection()
            #self.selected_process_pid_list = list(self.selected_row_names)
            from .ProcessesDetails import ProcessesDetails
            ProcessesDetails.process_details_show_process_details()


    def treeview_enter_press_event(self, event=None):
        #def bilgi_ver(event=None):
        # 1. Önce seçili olanları al
        secili_itemlar = self.treeview.selection()
        
        # 2. Eğer seçim yoksa ama odaklanılmış (üzerine gelinmiş) bir satır varsa onu al
        if not secili_itemlar:
            odaktaki_item = self.treeview.focus()
            if odaktaki_item:
                secili_itemlar = (odaktaki_item,)
        
        # Eğer ikisi de boşsa fonksiyondan çık
        if not secili_itemlar:
            return

        self.get_selection()
        from .ProcessesDetails import ProcessesDetails
        ProcessesDetails.process_details_show_process_details()


    def search_popover_set_gui(self):
        """
        Select the default search option checkbutton.
        """

        self.search_process_name_cb.set_active(True)


    def on_search_menu_cb_toggled(self, search_type):
        """
        Search again if process search type (process name or command line) is changed.
        """

        self.process_search_type = search_type

        Common.searchentry_placeholder_text(self)


    def priority_custom_value_gui(self):
        """
        Generate process priority (nice) custom value window GUI.
        """

        # Window
        self.priority_custom_value_window = Gtk.Window()
        self.priority_custom_value_window.set_default_size(400, -1)
        self.priority_custom_value_window.set_title(_tr("Change Priority"))
        self.priority_custom_value_window.set_icon_name("system-monitoring-center")
        self.priority_custom_value_window.set_transient_for(MainWindow.main_window)
        self.priority_custom_value_window.set_resizable(False)
        self.priority_custom_value_window.set_modal(True)
        self.priority_custom_value_window.set_hide_on_close(True)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        main_grid.set_row_spacing(10)
        self.priority_custom_value_window.set_child(main_grid)

        # Label
        label = Gtk.Label()
        label.set_label(_tr("Change priority of these process:\n(Smaller value means higher process priority)"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 0, 1, 1)

        # Label (process name and PID)
        self.priority_process_name_and_pid_label = Gtk.Label()
        self.priority_process_name_and_pid_label.set_selectable(True)
        self.priority_process_name_and_pid_label.set_label("--")
        self.priority_process_name_and_pid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.priority_process_name_and_pid_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.priority_process_name_and_pid_label, 0, 1, 1, 1)

        # Adjustment (for scale)
        self.adjustment = Gtk.Adjustment()
        self.adjustment.set_step_increment(1.0)

        # Scale
        self.scale = Gtk.Scale(adjustment=self.adjustment)
        self.scale.set_draw_value(True)
        self.scale.set_digits(0)
        main_grid.attach(self.scale, 0, 2, 1, 1)

        # Grid (buttons)
        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(50)
        main_grid.attach(grid, 0, 3, 1, 1)

        # Button (Cancel)
        self.priority_custom_value_cancel_button = Gtk.Button()
        self.priority_custom_value_cancel_button.set_label(_tr("Cancel"))
        grid.attach(self.priority_custom_value_cancel_button, 0, 0, 1, 1)

        # Button (Change Priority)
        self.priority_custom_value_change_priority_button = Gtk.Button()
        self.priority_custom_value_change_priority_button.set_label(_tr("Change Priority"))
        grid.attach(self.priority_custom_value_change_priority_button, 1, 0, 1, 1)

        # Signals (buttons)
        self.priority_custom_value_cancel_button.connect("clicked", self.on_priority_custom_value_window_buttons_clicked)
        self.priority_custom_value_change_priority_button.connect("clicked", self.on_priority_custom_value_window_buttons_clicked)


    def on_priority_custom_value_window_buttons_clicked(self, widget):
        """
        Close the process custom priority window or change process priority.
        """

        if widget == self.priority_custom_value_cancel_button:
            self.priority_custom_value_window.set_visible(False)

        if widget == self.priority_custom_value_change_priority_button:
            # Get right clicked process pid and name.
            selected_process_pid = self.selected_process_pid

            # Get new priority (nice value) of the process.
            selected_process_nice = str(int(self.adjustment.get_value()))

            # Define commands for the process.
            priority_command = ["renice", "-n", selected_process_nice, "-p", selected_process_pid]
            priority_command_pkexec = ["pkexec", "renice", "-n", selected_process_nice, "-p", selected_process_pid]

            if Config.environment_type == "flatpak":
                priority_command = ["flatpak-spawn", "--host"] + priority_command
                priority_command_pkexec = ["flatpak-spawn", "--host"] + priority_command_pkexec

            # Try to change priority (nice value) of the process.
            try:
                (subprocess.check_output(priority_command, stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                # Try to change priority (nice value) of the process if root privileges are required.
                try:
                    (subprocess.check_output(priority_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                # Prevent errors if wrong password is used or polkit dialog is closed by user.
                except subprocess.CalledProcessError:
                    return

            self.priority_custom_value_window.set_visible(False)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.column_dict = {"name": {"column_title": _tr("Name"), "column_type": str, "converted_data": "no"},
                            "pid": {"column_title": _tr("PID"), "column_type": int, "converted_data": "no"},
                            "username": {"column_title": _tr("User"), "column_type": str, "converted_data": "no"},
                            "status": {"column_title": _tr("Status"), "column_type": str, "converted_data": "no"},
                            "cpu_usage": {"column_title": _tr("CPU"), "column_type": float, "converted_data": "yes"},
                            "memory": {"column_title": _tr("Memory"), "column_type": int, "converted_data": "yes"},
                            "memory_rss": {"column_title": _tr("Memory (RSS)"), "column_type": int, "converted_data": "yes"},
                            "memory_vms": {"column_title": _tr("Memory (VMS)"), "column_type": int, "converted_data": "yes"},
                            "memory_shared": {"column_title": _tr("Memory (Shared)"), "column_type": int, "converted_data": "yes"},
                            "read_data": {"column_title": _tr("Read Data"), "column_type": int, "converted_data": "yes"},
                            "written_data": {"column_title": _tr("Written Data"), "column_type": int, "converted_data": "yes"},
                            "read_speed": {"column_title": _tr("Read Speed"), "column_type": float, "converted_data": "yes"},
                            "write_speed": {"column_title": _tr("Write Speed"), "column_type": float, "converted_data": "yes"},
                            "nice": {"column_title": _tr("Priority"), "column_type": int, "converted_data": "no"},
                            "threads": {"column_title": _tr("Threads"), "column_type": int, "converted_data": "no"},
                            "ppid": {"column_title": _tr("PPID"), "column_type": int, "converted_data": "no"},
                            "uid": {"column_title": _tr("UID"), "column_type": int, "converted_data": "no"},
                            "gid": {"column_title": _tr("GID"), "column_type": int, "converted_data": "no"},
                            "start_time": {"column_title": _tr("Start Time"), "column_type": float, "converted_data": "yes"},
                            "path": {"column_title": _tr("Path"), "column_type": str, "converted_data": "no"},
                            "command_line": {"column_title": _tr("Command Line"), "column_type": str, "converted_data": "no"},
                            "cpu_time": {"column_title": _tr("CPU Time"), "column_type": float, "converted_data": "yes"},
                            "cpu_recursive": {"column_title": _tr('CPU') + " - " + _tr('Recursive'), "column_type": float, "converted_data": "yes"},
                            "memory_rss_recursive": {"column_title": _tr('Memory (RSS)') + " - " + _tr('Recursive'), "column_type": int, "converted_data": "yes"},
                            "memory_recursive": {"column_title": _tr('Memory') + " - " + _tr('Recursive'), "column_type": int, "converted_data": "yes"}
                            }

        # Define data unit conversion function objects in for lower CPU usage.
        global data_unit_converter, cpu_time_converter
        data_unit_converter = Libsysmon.data_unit_converter
        cpu_time_converter = Libsysmon.cpu_time_converter

        process_status_translation_list = [_tr("Running"), _tr("Sleeping"), _tr("Waiting"), _tr("Idle"), _tr("Zombie"), _tr("Stopped"), _tr("Dead")]

        pid_list_prev = []
        self.piter_dict = {}
        self.selected_data_rows_prev = {}
        self.rows_additional_data_dict_prev = {}
        self.rows_data_dict_prev = {}
        self.row_id_list_prev = []
        self.image_dict = {}
        self.treeview_columns_shown_prev = []

        #self.number_of_clock_ticks = Libsysmon.number_of_clock_ticks
        self.system_boot_time = Libsysmon.get_system_boot_time()

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        update_interval = Config.update_interval

        # Get configrations one time per floop instead of getting them multiple times (hundreds of times for many of them) in every loop which causes high CPU usage.
        global processes_cpu_precision
        global processes_memory_data_precision, processes_memory_data_unit
        global processes_disk_data_precision, processes_disk_data_unit, processes_disk_speed_bit
        processes_cpu_precision = Config.processes_cpu_precision
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        try:
            self.treeview_columns_shown_prev = list(self.treeview_columns_shown)
            self.row_sorting_column_prev = self.row_sorting_column
            self.row_sorting_order_prev = self.row_sorting_order
        except AttributeError:
            self.treeview_columns_shown_prev = []
            self.row_sorting_column_prev = 0
            self.row_sorting_order_prev = 0

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        self.treeview_columns_shown = Config.processes_columns_shown
        self.row_sorting_column = Config.processes_row_sorting_column
        self.row_sorting_order = Config.processes_row_sorting_order
        self.show_processes_of_all_users = Config.show_processes_of_all_users
        self.show_processes_as_tree = Config.show_processes_as_tree
        self.processes_cpu_divide_by_core = Config.processes_cpu_divide_by_core
        self.hide_kernel_threads = Config.hide_kernel_threads

        # Clear all rows in order to prevent multiple additions if certain settings are changed.
        reset_treeview_rows = 0
        try:
            if self.show_processes_of_all_users != self.show_processes_of_all_users_prev:
                reset_treeview_rows = 1
            if self.show_processes_as_tree != self.show_processes_as_tree_prev:
                reset_treeview_rows = 1
            if self.hide_kernel_threads != self.hide_kernel_threads_prev:
                reset_treeview_rows = 1
            if self.processes_cpu_divide_by_core != self.processes_cpu_divide_by_core_prev:
                reset_treeview_rows = 1
            if processes_memory_data_unit != self.processes_memory_data_unit_prev:
                reset_treeview_rows = 1
            if processes_disk_data_unit != self.processes_disk_data_unit_prev:
                reset_treeview_rows = 1
            if processes_disk_speed_bit != self.processes_disk_speed_bit_prev:
                reset_treeview_rows = 1
        except AttributeError:
            reset_treeview_rows = 0

        if reset_treeview_rows == 1:
            for row in self.treeview.get_children():
                self.treeview.delete(row)

        # Get process information
        global cmdline_list
        process_list = []
        if self.show_processes_of_all_users == 1:
            processes_of_user = "all"
        else:
            processes_of_user = "current"
        if self.processes_cpu_divide_by_core == 1:
            cpu_usage_divide_by_cores = "yes"
        else:
            cpu_usage_divide_by_cores = "no"
        detail_level = "medium"

        self.username_uid_dict = Libsysmon.get_username_uid_dict()

        self.rows_data_dict, self.rows_additional_data_dict = Libsysmon.get_processes_information(process_list, processes_of_user, self.hide_kernel_threads, cpu_usage_divide_by_cores, detail_level, self.rows_data_dict_prev, self.rows_additional_data_dict_prev, self.system_boot_time, self.username_uid_dict)
        self.row_id_list = list(self.rows_data_dict.keys())
        #self.row_id_list = [str(x) for x in self.row_id_list]
        pid_list = self.rows_additional_data_dict["pid_list"]
        ppid_list = self.rows_additional_data_dict["ppid_list"]
        username_list = self.rows_additional_data_dict["username_list"]
        cmdline_list = self.rows_additional_data_dict["cmdline_list"]

        self.pid_list = pid_list
        self.ppid_list = ppid_list
        self.cmdline_list = cmdline_list

        Common.add_columns_and_reset_rows_and_columns(self)

        process_image = tk.PhotoImage(file=MainWindow.image_path + "smc-process-row.png").subsample(3, 3)

        # Get CPU, Memory (RSS) and Memory recursive data of all processes.
        if "cpu_recursive" in self.treeview_columns_shown:
            cpu_usage_dict = {}
            for process_pid in self.row_id_list:
                row_data_dict = self.rows_data_dict[str(process_pid)]
                cpu_usage_dict[int(process_pid)] = row_data_dict["cpu_usage"]
            cpu_recursive_dict = Libsysmon.get_recursive_data(pid_list, ppid_list, cpu_usage_dict)
        if "memory_rss_recursive" in self.treeview_columns_shown:
            memory_rss_dict = {}
            for process_pid in self.row_id_list:
                row_data_dict = self.rows_data_dict[str(process_pid)]
                memory_rss_dict[int(process_pid)] = row_data_dict["memory_rss"]
            memory_rss_recursive_dict = Libsysmon.get_recursive_data(pid_list, ppid_list, memory_rss_dict)
        if "memory_recursive" in self.treeview_columns_shown:
            memory_dict = {}
            for process_pid in self.row_id_list:
                row_data_dict = self.rows_data_dict[str(process_pid)]
                memory_dict[int(process_pid)] = row_data_dict["memory"]
            memory_recursive_dict = Libsysmon.get_recursive_data(pid_list, ppid_list, memory_dict)

        selected_data_rows_raw = {}
        selected_data_rows = {}
        for process_pid in self.row_id_list:
            #process_pid = int(process_pid)
            row_data_dict = self.rows_data_dict[process_pid]
            if process_pid not in self.image_dict:
                self.image_dict[process_pid] = process_image
            selected_data_row_raw = []
            selected_data_row = []
            for column_shown in self.treeview_columns_shown:
                if column_shown == "name":
                    selected_data_row.append(row_data_dict["name"])
                    selected_data_row_raw.append(row_data_dict["name"])
                elif column_shown == "pid":
                    selected_data_row.append(row_data_dict["pid"])
                    selected_data_row_raw.append(row_data_dict["pid"])
                elif column_shown == "username":
                    selected_data_row.append(row_data_dict["username"])
                    selected_data_row_raw.append(row_data_dict["username"])
                elif column_shown == "status":
                    translated_data = _tr(row_data_dict["status"])
                    selected_data_row.append(translated_data)
                    selected_data_row_raw.append(translated_data)
                elif column_shown == "cpu_usage":
                    converted_data = f'{row_data_dict["cpu_usage"]:.{processes_cpu_precision}f} %'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["cpu_usage"])
                elif column_shown == "memory":
                    converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory"], processes_memory_data_unit, processes_memory_data_precision)}' 
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["memory"])
                elif column_shown == "memory_rss":
                    converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory_rss"], processes_memory_data_unit, processes_memory_data_precision)}' 
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["memory_rss"])
                elif column_shown == "memory_vms":
                    converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory_vms"], processes_memory_data_unit, processes_memory_data_precision)}' 
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["memory_vms"])
                elif column_shown == "memory_shared":
                    converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory_shared"], processes_memory_data_unit, processes_memory_data_precision)}' 
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["memory_shared"])
                elif column_shown == "read_data":
                    converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory_shared"], processes_disk_data_unit, processes_disk_data_precision)}' 
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["read_data"])
                elif column_shown == "written_data":
                    converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory_shared"], processes_disk_data_unit, processes_disk_data_precision)}'  
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["written_data"])
                elif column_shown == "read_speed":
                    converted_data = f'{data_unit_converter("speed", processes_disk_speed_bit, row_data_dict["read_speed"], processes_disk_data_unit, processes_disk_data_precision)}/s'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["read_speed"])
                elif column_shown == "write_speed":
                    converted_data = f'{data_unit_converter("speed", processes_disk_speed_bit, row_data_dict["write_speed"], processes_disk_data_unit, processes_disk_data_precision)}/s'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["write_speed"])
                elif column_shown == "nice":
                    selected_data_row.append(row_data_dict["nice"])
                    selected_data_row_raw.append(row_data_dict["nice"])
                elif column_shown == "threads":
                    selected_data_row.append(row_data_dict["number_of_threads"])
                    selected_data_row_raw.append(row_data_dict["number_of_threads"])
                elif column_shown == "ppid":
                    selected_data_row.append(row_data_dict["ppid"])
                    selected_data_row_raw.append(row_data_dict["ppid"])
                elif column_shown == "uid":
                    selected_data_row.append(row_data_dict["uid"])
                    selected_data_row_raw.append(row_data_dict["uid"])
                elif column_shown == "gid":
                    selected_data_row.append(row_data_dict["gid"])
                    selected_data_row_raw.append(row_data_dict["gid"])
                elif column_shown == "start_time":
                    if row_data_dict["start_time"] != 0:
                        converted_data = datetime.fromtimestamp(row_data_dict["start_time"]).strftime("%H:%M:%S %d.%m.%Y")
                    if row_data_dict["start_time"] == 0:
                        converted_data = "-"
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["start_time"])
                elif column_shown == "path":
                    selected_data_row.append(row_data_dict["path"])
                    selected_data_row_raw.append(row_data_dict["path"])
                elif column_shown == "command_line":
                    selected_data_row.append(row_data_dict["command_line"])
                    selected_data_row_raw.append(row_data_dict["command_line"])
                elif column_shown == "cpu_time":
                    converted_data = cpu_time_converter(row_data_dict["cpu_time"])
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["cpu_time"])
                elif column_shown == "cpu_recursive":
                    cpu_recursive = cpu_recursive_dict[int(process_pid)]
                    converted_data = f'{cpu_recursive:.{processes_cpu_precision}f} %'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(cpu_recursive)
                elif column_shown == "memory_rss_recursive":
                    memory_rss_recursive = memory_rss_recursive_dict[int(process_pid)]
                    converted_data = f'{data_unit_converter("data", "none", memory_rss_recursive, processes_memory_data_unit, processes_memory_data_precision)}'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(memory_rss_recursive)
                elif column_shown == "memory_recursive":
                    memory_recursive = memory_recursive_dict[int(process_pid)]
                    converted_data = f'{data_unit_converter("data", "none", memory_recursive, processes_memory_data_unit, processes_memory_data_precision)}'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(memory_recursive)

            selected_data_rows[process_pid] = selected_data_row
            selected_data_rows_raw[process_pid] = selected_data_row_raw


        new_rows, deleted_rows, existing_rows = Common.get_new_removed_updated_rows(self.row_id_list, self.row_id_list_prev)

        self.piter_dict = Common.add_remove_update_treeview_rows(self.treeview, self.piter_dict, self.selected_data_rows_prev, self.image_dict, selected_data_rows, selected_data_rows_raw, new_rows, deleted_rows, existing_rows, pid_list, ppid_list, self.show_processes_as_tree)

        self.row_count = len(self.row_id_list)
        self.row_information = _tr("Processes")
        self.selected_data_rows = selected_data_rows
        self.selected_data_rows_raw = selected_data_rows_raw
        Common.searchentry_placeholder_text(self)

        self.rows_data_dict_prev = dict(self.rows_data_dict)
        self.row_id_list_prev = self.row_id_list
        self.selected_data_rows_prev = self.selected_data_rows
        self.rows_additional_data_dict_prev = dict(self.rows_additional_data_dict)

        self.show_processes_of_all_users_prev = self.show_processes_of_all_users
        self.show_processes_as_tree_prev = self.show_processes_as_tree
        self.hide_kernel_threads_prev = self.hide_kernel_threads
        self.processes_cpu_divide_by_core_prev = self.processes_cpu_divide_by_core
        self.processes_memory_data_unit_prev = processes_memory_data_unit
        self.processes_disk_data_unit_prev = processes_disk_data_unit
        self.processes_disk_speed_bit_prev = processes_disk_speed_bit

        Common.sort_columns_on_every_loop(self)


Processes = Processes()

