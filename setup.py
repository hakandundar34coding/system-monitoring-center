#!/usr/bin/env python3

from setuptools import setup, find_packages, os
import sys, shutil


with open(os.path.dirname(os.path.realpath(__file__)) + "/src/__version__") as reader:
    version = reader.read().strip()


def files_in_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder)]:
        file_paths.append(folder + file)
    return file_paths


def files_in_locale_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder) if filename.split(".")[-1] not in ["pot", "sh"]]:
        file_paths.append(folder + file + "/LC_MESSAGES/system-monitoring-center.mo")
    return file_paths


def data_files_in_locale_folder(target_folder, folder):
    data_files_in_locale_folder = []
    for file in [filename for filename in os.listdir(folder) if filename.split(".")[-1] not in ["pot", "sh"]]:
        data_files_in_locale_folder.append((target_folder + file + "/LC_MESSAGES/", [folder + file + "/LC_MESSAGES/system-monitoring-center.mo"]))
    return data_files_in_locale_folder


os.chmod("integration/io.github.hakandundar34coding.system-monitoring-center.desktop", 0o644)
for file in files_in_locale_folder("locale/"):
    os.chmod(file, 0o644)
for file in files_in_folder("database/"):
    os.chmod(file, 0o644)
for file in files_in_folder("src/"):
    os.chmod(file, 0o644)
for file in files_in_folder("ui/"):
    os.chmod(file, 0o644)
for file in files_in_folder("icons/hicolor/scalable/actions/"):
    os.chmod(file, 0o644)
os.chmod("icons/hicolor/scalable/apps/system-monitoring-center.svg", 0o644)

data_files = [
    ("/usr/share/applications/", ["integration/io.github.hakandundar34coding.system-monitoring-center.desktop"]),
    ("/usr/share/polkit-1/actions/", ["integration/io.github.hakandundar34coding.system-monitoring-center.policy"]),
    ("/usr/share/system-monitoring-center/database/", files_in_folder("database/")),
    ("/usr/share/system-monitoring-center/src/", files_in_folder("src/")),
    ("/usr/share/system-monitoring-center/ui/", files_in_folder("ui/")),
    ("/usr/share/system-monitoring-center/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
    ("/usr/share/system-monitoring-center/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
    ("/usr/share/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
    ("/usr/share/man/man1/", ["man/system-monitoring-center.1.gz"]),
    ("/usr/bin/", ["integration/system-monitoring-center"])
    ] + data_files_in_locale_folder("/usr/share/system-monitoring-center/locale/", "locale/")


setup(
    name="system-monitoring-center",
    version=version,
    description="Multi-featured system monitor",
    long_description="Provides information about CPU/RAM/Disk/Network/GPU performance, sensors, processes, users, services and system.",
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    url="https://github.com/hakandundar34coding/system-monitoring-center",
    keywords="system monitor task manager performance cpu ram swap memory disk network gpu processes users services",
    license="GPLv3",
    install_requires=["PyGObject"],
    packages=find_packages(),
    data_files=data_files,
)

