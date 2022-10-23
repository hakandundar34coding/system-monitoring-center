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


"""
# Debian package
if "--debian_package" in sys.argv:
    package_type_var = "debian_package"
    sys.argv.remove("--debian_package")

# RPM package
if "--rpm_package" in sys.argv:
    package_type_var = "rpm_package"
    sys.argv.remove("--rpm_package")

# Arch Linux package
if "--arch_package" in sys.argv:
    package_type_var = "arch_package"
    sys.argv.remove("--arch_package")
"""

# Flatpak package
if "--flatpak_package" in sys.argv:
    package_type_var = "flatpak_package"
    sys.argv.remove("--flatpak_package")

# Python package
elif "egg_info" in sys.argv or "sdist" in sys.argv or "bdist_wheel" in sys.argv:
    for argv in sys.argv:
        if "/in_process/_in_process.py" in argv:
            package_type_var = "python_package"

# Debian, RPM, Arch Linux another other package
else:
    package_type_var = "debian_rpm_archlinux_or_another_package"


print("\n" + "_____package_type: " + package_type_var + "_____" + "\n")



if package_type_var == "debian_rpm_archlinux_or_another_package":

    install_requires=["PyGObject"]
    entry_points={}

    os.chmod("integration/io.github.hakandundar34coding.system-monitoring-center.desktop", 0o644)
    os.chmod("locale/de/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/cs/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/fa/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/hu/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/pl/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/tr/LC_MESSAGES/system-monitoring-center.mo", 0o644)
    os.chmod("locale/zh_CN/LC_MESSAGES/system-monitoring-center.mo", 0o644)
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
        ("/usr/share/system-monitoring-center/locale/de/LC_MESSAGES/", ["locale/de/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/cs/LC_MESSAGES/", ["locale/cs/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/fa/LC_MESSAGES/", ["locale/fa/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/hu/LC_MESSAGES/", ["locale/hu/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/pl/LC_MESSAGES/", ["locale/pl/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/pt_BR/LC_MESSAGES/", ["locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/pt_PT/LC_MESSAGES/", ["locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/ru_RU/LC_MESSAGES/", ["locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/tr/LC_MESSAGES/", ["locale/tr/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/locale/zh_CN/LC_MESSAGES/", ["locale/zh_CN/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/usr/share/system-monitoring-center/database/", files_in_folder("database/")),
        ("/usr/share/system-monitoring-center/src/", files_in_folder("src/")),
        ("/usr/share/system-monitoring-center/ui/", files_in_folder("ui/")),
        ("/usr/share/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
        ("/usr/share/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
        ("/usr/share/man/man1/", ["man/system-monitoring-center.1.gz"]),
        ("/usr/bin/", ["integration/system-monitoring-center"])
    ]



if package_type_var == "flatpak_package":

    install_requires=["PyGObject"]
    entry_points={}

    os.rename("icons/hicolor/scalable/apps/system-monitoring-center.svg", "icons/hicolor/scalable/apps/io.github.hakandundar34coding.system-monitoring-center.svg")
    icon_list = os.listdir("icons/hicolor/scalable/actions/")
    for icon in icon_list:
        os.rename("icons/hicolor/scalable/actions/" + icon, "icons/hicolor/scalable/actions/io.github.hakandundar34coding.system-monitoring-center." + icon.split("system-monitoring-center-")[-1])

    with open("integration/io.github.hakandundar34coding.system-monitoring-center.desktop") as reader:
        desktop_file_content = reader.read()
    desktop_file_content = desktop_file_content.replace("Icon=system-monitoring-center", "Icon=io.github.hakandundar34coding.system-monitoring-center")
    with open("integration/io.github.hakandundar34coding.system-monitoring-center.desktop", "w") as writer:
        writer.write(desktop_file_content)

    with open("integration/system-monitoring-center") as reader:
        script_file_content = reader.read()
    script_file_content = script_file_content.replace("/usr/share/system-monitoring-center/src/", "/app/share/system-monitoring-center/src/")
    with open("integration/system-monitoring-center", "w") as writer:
        writer.write(script_file_content)

    data_files = [
        ("/app/share/applications/", ["integration/io.github.hakandundar34coding.system-monitoring-center.desktop"]),
        #("/app/share/polkit-1/actions/", ["integration/io.github.hakandundar34coding.system-monitoring-center.policy"]),
        ("/app/share/system-monitoring-center/locale/de/LC_MESSAGES/", ["locale/de/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/cs/LC_MESSAGES/", ["locale/cs/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/fa/LC_MESSAGES/", ["locale/fa/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/hu/LC_MESSAGES/", ["locale/hu/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/pl/LC_MESSAGES/", ["locale/pl/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/pt_BR/LC_MESSAGES/", ["locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/pt_PT/LC_MESSAGES/", ["locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/ru_RU/LC_MESSAGES/", ["locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/tr/LC_MESSAGES/", ["locale/tr/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/locale/zh_CN/LC_MESSAGES/", ["locale/zh_CN/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/app/share/system-monitoring-center/database/", files_in_folder("database/")),
        ("/app/share/system-monitoring-center/src/", files_in_folder("src/")),
        ("/app/share/system-monitoring-center/ui/", files_in_folder("ui/")),
        ("/app/share/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
        ("/app/share/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/io.github.hakandundar34coding.system-monitoring-center.svg"]),
        ("/app/share/man/man1/", ["man/system-monitoring-center.1.gz"]),
        ("/app/share/appdata/", ["io.github.hakandundar34coding.system-monitoring-center.appdata.xml"]),
        ("/app/bin/", ["integration/system-monitoring-center"])
    ]



if package_type_var == "python_package":

    install_requires=["PyGObject", "pycairo"]
    entry_points={"gui_scripts": ["system-monitoring-center = systemmonitoringcenter.start:start_app"]}

    data_files = [
        ("/systemmonitoringcenter/integration/", ["integration/io.github.hakandundar34coding.system-monitoring-center.desktop"]),
        ("/systemmonitoringcenter/locale/de/LC_MESSAGES/", ["locale/de/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/cs/LC_MESSAGES/", ["locale/cs/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/fa/LC_MESSAGES/", ["locale/fa/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/hu/LC_MESSAGES/", ["locale/hu/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/pl/LC_MESSAGES/", ["locale/pl/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/pt_BR/LC_MESSAGES/", ["locale/pt_BR/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/pt_PT/LC_MESSAGES/", ["locale/pt_PT/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/ru_RU/LC_MESSAGES/", ["locale/ru_RU/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/tr/LC_MESSAGES/", ["locale/tr/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/locale/zh_CN/LC_MESSAGES/", ["locale/zh_CN/LC_MESSAGES/system-monitoring-center.mo"]),
        ("/systemmonitoringcenter/database/", files_in_folder("database/")),
        ("/systemmonitoringcenter/src/", files_in_folder("src/")),
        ("/systemmonitoringcenter/ui/", files_in_folder("ui/")),
        ("/systemmonitoringcenter/icons/hicolor/scalable/actions/", files_in_folder("icons/hicolor/scalable/actions/")),
        ("/systemmonitoringcenter/icons/hicolor/scalable/apps/", ["icons/hicolor/scalable/apps/system-monitoring-center.svg"]),
    ]


setup(
    name="system-monitoring-center",
    version=version,
    description="Multi-featured system monitor.",
    long_description="Provides information about CPU/RAM/Disk/Network/GPU performance, sensors, processes, users, services and system.",
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    url="https://github.com/hakandundar34coding/system-monitoring-center",
    keywords="system monitor task manager performance cpu ram swap memory disk network gpu processes users services",
    license="GPLv3",
    install_requires=install_requires,
    python_requires=">=3.6",
    packages=find_packages(),
    data_files=data_files,
    entry_points=entry_points,
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
        "Topic :: System :: Monitoring",
    ],
)
