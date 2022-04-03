#!/usr/bin/env python3
from setuptools import setup, find_packages, os
import sys


with open(os.path.dirname(os.path.realpath(__file__)) + "/src/__version__") as reader:
    version = reader.read().strip()


def files_in_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder)]:
        file_paths.append(folder + file)
    return file_paths


data_files = [
    ("/systemmonitoringcenter/applications/", ["integration/com.github.hakand34.system-monitoring-center.desktop"]),
    ("/systemmonitoringcenter/locale/cs/LC_MESSAGES/", ["translations/cs/system-monitoring-center.mo"]),
    ("/systemmonitoringcenter/locale/pl/LC_MESSAGES/", ["translations/pl/system-monitoring-center.mo"]),
    ("/systemmonitoringcenter/locale/pt_BR/LC_MESSAGES/", ["translations/pt_BR/system-monitoring-center.mo"]),
    ("/systemmonitoringcenter/locale/tr/LC_MESSAGES/", ["translations/tr/system-monitoring-center.mo"]),
    ("/systemmonitoringcenter/integration/", ["integration/com.github.hakand34.system-monitoring-center.desktop"]),
    ("/systemmonitoringcenter/database/", files_in_folder("database/")),
    ("/systemmonitoringcenter/src/", files_in_folder("src/")),
    ("/systemmonitoringcenter/ui/", files_in_folder("ui/")),
    ("/systemmonitoringcenter/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
    ("/systemmonitoringcenter/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
]


setup(
    name="system-monitoring-center",
    version=version,
    packages=find_packages(),
    install_requires=["PyGObject", "pycairo"],
    data_files=data_files,
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    description="Provides information about system performance and usage.",
    long_description="""Provides information about CPU/RAM/Disk/Network/GPU performance, sensors, 
        processes, users, storage, startup programs, services, environment variables 
        and system.""",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    license="GPLv3",
    keywords="system monitor task manager center performance speed frequency cpu usage ram usage swap memory memory usage storage network usage download speed fps frame ratio processes users startup programs services os",
    url="https://github.com/hakandundar34coding/system-monitoring-center",
    entry_points={"gui_scripts": ["system-monitoring-center = systemmonitoringcenter.start:start_app"]},
)
