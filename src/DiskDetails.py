#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Disk import Disk
from Performance import Performance


# Define class
class DiskDetails:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder1301w = Gtk.Builder()
        builder1301w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskDetailsWindow.ui")

        # Get GUI objects
        self.window1301w = builder1301w.get_object('window1301w')
        self.label1301w = builder1301w.get_object('label1301w')
        self.label1302w = builder1301w.get_object('label1302w')
        self.label1303w = builder1301w.get_object('label1303w')
        self.label1304w = builder1301w.get_object('label1304w')
        self.label1305w = builder1301w.get_object('label1305w')
        self.label1306w = builder1301w.get_object('label1306w')
        self.label1307w = builder1301w.get_object('label1307w')
        self.label1308w = builder1301w.get_object('label1308w')
        self.label1309w = builder1301w.get_object('label1309w')
        self.label1310w = builder1301w.get_object('label1310w')
        self.label1311w = builder1301w.get_object('label1311w')
        self.label1312w = builder1301w.get_object('label1312w')
        self.label1313w = builder1301w.get_object('label1313w')
        self.label1314w = builder1301w.get_object('label1314w')
        self.label1315w = builder1301w.get_object('label1315w')
        self.label1316w = builder1301w.get_object('label1316w')
        self.label1317w = builder1301w.get_object('label1317w')
        self.label1322w = builder1301w.get_object('label1322w')

        # Connect GUI signals
        self.window1301w.connect("delete-event", self.on_window1301w_delete_event)
        self.window1301w.connect("show", self.on_window1301w_show)

        # Run initial function
        self.disk_details_initial_func()


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window1301w_delete_event(self, widget, event):

        widget.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window1301w_show(self, widget):

        # Call this function in order to reset Disk Details window. Data from previous storage/disk remains visible (for a short time) until getting and showing new storage/disk data if window is closed and opened for an another storage/disk because window is made hidden when close button is clicked.
        self.disk_details_gui_reset_func()

        # Get and show disk information.
        self.disk_details_run_func()


    # ----------------------- Called for reseting labels on the GUI when window is shown -----------------------
    def disk_details_gui_reset_func(self):

        self.label1301w.set_text("--")
        self.label1302w.set_text("--")
        self.label1303w.set_text("--")
        self.label1304w.set_text("--")
        self.label1305w.set_text("--")
        self.label1306w.set_text("--")
        self.label1307w.set_text("--")
        self.label1308w.set_text("--")
        self.label1309w.set_text("--")
        self.label1310w.set_text("--")
        self.label1311w.set_text("--")
        self.label1312w.set_text("--")
        self.label1313w.set_text("--")
        self.label1314w.set_text("--")
        self.label1315w.set_text("--")
        self.label1316w.set_text("--")
        self.label1317w.set_text("--")
        self.label1322w.set_text("--")


    # ----------------------------------- Disk - Disk Details Function -----------------------------------
    def disk_details_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        # Disk data values from "/sys/class/block/[DISK_NAME]/" are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).
        self.disk_sector_size = 512


    # ----------------------------------- Disk - Disk Details Foreground Function -----------------------------------
    def disk_details_loop_func(self):

        # Get right clicked disk name and pci.ids file content
        disk = Disk.selected_disk
        pci_ids_output = Disk.pci_ids_output

        # Set Disk Details window title
        self.window1301w.set_title(_tr("Disk Details") + ": " + disk)

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        performance_disk_usage_data_precision = Config.performance_disk_usage_data_precision
        performance_disk_usage_data_unit = Config.performance_disk_usage_data_unit

        # Get all disks (disks and partitions)
        with open("/proc/partitions") as reader:
            # Get without first 2 lines (header line and an empty line).
            proc_partitions_lines = reader.read().split("\n")[2:-1]
        # Get disk list.
        disk_list = []
        for line in proc_partitions_lines:
            disk_list.append(line.split()[3])

        # Get disk path, mount point, file system and mode information
        with open("/proc/mounts") as reader:
            proc_mounts_lines = reader.read().strip().split("\n")
        # Get swap disk information
        with open("/proc/swaps") as reader:
            # Get without first line (header line). 
            proc_swaps_lines = reader.read().split("\n")[1:-1]
        swap_disk_list = []
        for line in proc_swaps_lines:
            swap_disk_list.append(line.split()[0].split("/")[-1])

        # Get disk device path
        # Some disks (such as zram0, zram1, etc. swap partitions) may not be present in "/dev/disk/by-path/" path.
        disk_device_path_list = os.listdir("/dev/disk/by-path/")
        disk_device_path_disk_list = []
        for disk_device_path in disk_device_path_list:
            # "os.readlink()" does not work with "/dev/disk/[folder_name]/[file_name]" files. "os.path.realpath()" is used for getting path.
            disk_device_path_disk_list.append(os.path.realpath("/dev/disk/by-path/" + disk_device_path).split("/")[-1])
        # Get disk specific data
        try:
            with open("/sys/class/block/" + disk + "/uevent") as reader:
                sys_class_block_disk_uevent_lines = reader.read().split("\n")
        except FileNotFoundError:
            self.window1301w.hide()
            return

        # Get disk type
        for line in sys_class_block_disk_uevent_lines:
            if "DEVTYPE" in line:
                disk_type = _tr(line.split("=")[1].capitalize())
                break

        # Get disk parent name
        disk_parent_name = "-"
        if disk_type == _tr("Partition"):
            for check_disk_dir in disk_list:
                if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + disk) == True:
                    disk_parent_name = check_disk_dir

        # Get disk mount point which will be used for getting disk free, used spaces, used space percentage and also will be shown on the label as "disk mount point" information.
        disk_mount_point = _tr("[Not mounted]")
        for line in proc_mounts_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == disk:
                # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                disk_mount_point = bytes(line_split[1], "utf-8").decode("unicode_escape")

        # Get if disk is system disk information
        disk_system_disk = _tr("No")
        # This variable (initial value) is defined here because system disk may not be detected by checking if mount point is "/" on some systems such as some ARM devices. "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
        disk_in_proc_mounts_lines = "no"
        for line in proc_mounts_lines:
            line_split = line.split(" ", 2)
            if line_split[0].split("/")[-1] == disk:
                disk_in_proc_mounts_lines = "yes"
                if line_split[1] == "/":
                    disk_system_disk = _tr("Yes")
                    break
        if disk_in_proc_mounts_lines == "no":
            for line in proc_mounts_lines:
                line_split = line.split(" ", 1)
                if line_split[0] == "dev/root":
                    with open("/proc/cmdline") as reader:
                        proc_cmdline = reader.read()
                    if "root=UUID=" in proc_cmdline:
                        disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                        system_disk = os.path.realpath("/dev/disk/by-uuid/" + disk_uuid_partuuid).split("/")[-1].strip()
                    if "root=PARTUUID=" in proc_cmdline:
                        disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                        system_disk = os.path.realpath("/dev/disk/by-partuuid/" + disk_uuid_partuuid).split("/")[-1].strip()
                    if system_disk == disk:
                        disk_system_disk = _tr("Yes")

        # Get disk file system
        # Initial value of the variable.
        disk_file_system = _tr("[Not mounted]")
        for line in proc_mounts_lines:
            if line.split()[0].strip() == ("/dev/" + disk):
                disk_file_system = line.split()[2].strip()
                break
        if disk_file_system == _tr("[Not mounted]"):
            # Show "[SWAP]" information for swap disks (if selected swap area is partition (not file))
            with open("/proc/swaps") as reader:
                proc_swaps_output_lines = reader.read().strip().split("\n")
            swap_disk_list = []
            for line in proc_swaps_output_lines:
                if line.split()[1].strip() == "partition":
                    swap_disk_list.append(line.split()[0].strip().split("/")[-1])
            if len(swap_disk_list) > 0 and disk in swap_disk_list:
                disk_file_system = _tr("[SWAP]")
        # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
        if disk_file_system  == "fuseblk":
            try:
                disk_for_file_system = "/dev/" + disk
                disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
            except Exception:
                pass

        # Get disk capacity (mass storage)
        try:
            with open("/sys/class/block/" + disk + "/size") as reader:
                disk_capacity_mass_storage = int(reader.read()) * self.disk_sector_size
        except FileNotFoundError:
            self.window1301w.hide()
            return

        # Get disk capacity, free, available and used space
        try:
            if disk_mount_point != _tr("[Not mounted]"):
                statvfs_disk_usage_values = os.statvfs(disk_mount_point)
                fragment_size = statvfs_disk_usage_values.f_frsize
                disk_capacity = statvfs_disk_usage_values.f_blocks * fragment_size
                disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
                disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
                disk_used = disk_capacity - disk_free
                # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values (same with "df" command output values). This is real usage percent.
                disk_usage_percent = disk_used / (disk_available + disk_used) * 100
                # Gives same result with "lsblk" command (mass storage values)
                disk_usage_percent_mass_storage = disk_used / disk_capacity * 100
            else:
                # "-9999" value is used as "disk_available" value if disk is not mounted. Code will recognize this valu e and show "[Not mounted]" information in this situation.
                disk_available = -9999
                disk_used = -9999
                disk_usage_percent = -9999
                disk_usage_percent_mass_storage = -9999
        except Exception:
            self.window1301w.hide()
            return

        # Get disk vendor and model
        if disk_type == _tr("Disk"):
            disk_or_parent_disk_name = disk
        if disk_type == _tr("Partition"):
            disk_or_parent_disk_name = disk_parent_name

        # Get disk vendor
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/vendor") as reader:
                disk_vendor = reader.read().strip()
            # Disk vendor information may be available as vendor id on some cases (such as on QEMU virtual machines).
            if disk_vendor.startswith("0x"):
                disk_vendor_id = "\n" + disk_vendor.split("x")[-1].strip() + "  "
                # "vendor" information may not be present in the pci.ids file.
                if disk_vendor_id in pci_ids_output:
                    rest_of_the_pci_ids_output = pci_ids_output.split(disk_vendor_id, 1)[1]
                    disk_vendor = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                if disk_vendor_id not in pci_ids_output:
                    disk_vendor = f'[{_tr("Unknown")}]'
        # Some disks such as NVMe SSDs do not have "vendor" file under "/sys/class/block/" + disk + "/device" directory. They have this file under "/sys/class/block/" + disk + "/device/device/vendor" directory.
        except FileNotFoundError:
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/vendor") as reader:
                    disk_vendor_id = "\n" + reader.read().strip().split("x")[-1] + "  "
                # "vendor" information may not be present in the pci.ids file.
                if disk_vendor_id in pci_ids_output:
                    rest_of_the_pci_ids_output = pci_ids_output.split(disk_vendor_id, 1)[1]
                    disk_vendor = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                if disk_vendor_id not in pci_ids_output:
                    disk_vendor = f'[{_tr("Unknown")}]'
            except Exception:
                disk_vendor = f'[{_tr("Unknown")}]'

        # Get disk model
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                disk_model = reader.read().strip()
            # Disk model information may be available as model id on some cases (such as on QEMU virtual machines).
            if disk_model.startswith("0x"):
                disk_model_id = "\n\t" + disk_model.split("x")[-1] + "  "
                if disk_vendor != f'[{_tr("Unknown")}]':
                    # "device name" information may not be present in the pci.ids file.
                    if disk_model_id in rest_of_the_pci_ids_output:
                        rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(disk_model_id, 1)[1]
                        disk_model = rest_of_the_rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                    else:
                        disk_model = f'[{_tr("Unknown")}]'
                else:
                    disk_model = f'[{_tr("Unknown")}]'
        except Exception:
            disk_model = f'[{_tr("Unknown")}]'
        disk_vendor_model = disk_vendor + " - " +  disk_model
        # Get disk vendor and model if disk is loop device or swap disk.
        if "loop" in disk:
            disk_vendor_model = "[Loop Device]"
        if "zram" in disk:
            disk_vendor_model = _tr("[SWAP]")

        # Get disk label
        disk_label = "-"
        try:
            disk_label_list = os.listdir("/dev/disk/by-label/")
            for label in disk_label_list:
                if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == disk:
                    # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                    disk_label = bytes(label, "utf-8").decode("unicode_escape")
        except FileNotFoundError:
            pass

        # Get disk partition label
        disk_partition_label = "-"
        try:
            disk_partition_label_list = os.listdir("/dev/disk/by-partlabel/")
            for label in disk_partition_label_list:
                if os.path.realpath("/dev/disk/by-partlabel/" + label).split("/")[-1] == disk:
                    disk_partition_label = label
        except FileNotFoundError:
            pass

        # Get disk path
        disk_path = "-"
        try:
            if os.path.exists("/dev/" + disk) == True:
                disk_path = "/dev/" + disk
        except FileNotFoundError:
            self.window1301w.hide()
            return

        # Get disk revision
        disk_revision = "-"
        if disk_type == _tr("Disk"):
            try:
                with open("/sys/class/block/" + disk + "/device/rev") as reader:
                    disk_revision = reader.read().strip()
            except Exception:
                pass

        # Get disk serial number
        disk_serial_number = "-"
        if disk_type == _tr("Disk"):
            disk_id_list = os.listdir("/dev/disk/by-id/")
            for id in disk_id_list:
                if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == disk and ("/dev/disk/by-id/" + id).startswith("wwn-") == False:
                    disk_serial_number = id.split("-")[-1]
                    if "part" in disk_serial_number:
                        disk_serial_number = id.split("-")[-2]

        # Get disk UUID
        disk_uuid = "-"
        try:
            disk_uuid_list = os.listdir("/dev/disk/by-uuid/")
            for uuid in disk_uuid_list:
                if os.path.realpath("/dev/disk/by-uuid/" + uuid).split("/")[-1] == disk:
                    disk_uuid = uuid
        except FileNotFoundError:
            pass


        # Set label text by using storage/disk data
        self.label1301w.set_text(disk)
        self.label1302w.set_text(disk_parent_name)
        self.label1303w.set_text(disk_system_disk)
        self.label1304w.set_text(disk_type)
        self.label1305w.set_text(f'{self.performance_data_unit_converter_func(disk_capacity_mass_storage, performance_disk_usage_data_unit, performance_disk_usage_data_precision)}')
        self.label1306w.set_text(disk_file_system)
        if disk_available == -9999:
            self.label1307w.set_text(_tr("[Not mounted]"))
            self.label1308w.set_text(_tr("[Not mounted]"))
            self.label1309w.set_text(_tr("[Not mounted]"))
            self.label1310w.set_text(_tr("[Not mounted]"))
        if disk_available != -9999:
            self.label1307w.set_text(f'{self.performance_data_unit_converter_func(disk_capacity, performance_disk_usage_data_unit, performance_disk_usage_data_precision)}')
            self.label1308w.set_text(f'{self.performance_data_unit_converter_func(disk_available, performance_disk_usage_data_unit, performance_disk_usage_data_precision)}')
            self.label1309w.set_text(f'{self.performance_data_unit_converter_func(disk_used, performance_disk_usage_data_unit, performance_disk_usage_data_precision)} - {disk_usage_percent:.1f}%')
            self.label1310w.set_text(f'{disk_usage_percent_mass_storage:.1f}%')
        self.label1311w.set_text(disk_vendor_model)
        self.label1312w.set_text(disk_label)
        self.label1313w.set_text(disk_partition_label)
        self.label1314w.set_text(disk_mount_point)
        self.label1315w.set_text(disk_path)
        self.label1316w.set_text(disk_revision)
        self.label1317w.set_text(disk_serial_number)
        self.label1322w.set_text(disk_uuid)


    # ----------------------------------- Disk Details - Run Function -----------------------------------
    def disk_details_run_func(self):

        if self.window1301w.get_visible() == True:
            GLib.idle_add(self.disk_details_loop_func)
            GLib.timeout_add(Config.update_interval * 1000, self.disk_details_run_func)


# Generate object
DiskDetails = DiskDetails()

