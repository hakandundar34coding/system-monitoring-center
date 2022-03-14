#!/usr/bin/env python3
from setuptools import setup, find_packages, os
import sys

changelog = 'debian/changelog'
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = ""
    f = open('src/__version__', 'w')
    f.write(version)
    f.close()


def files_in_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder)]:
        file_paths.append(folder + file)
    return file_paths


PREFIX = "/usr"

if "--rpm" in sys.argv:
    PREFIX = "RPM"
    sys.argv.remove("--rpm")
    build_root = sys.argv[-1].strip("--")
    del sys.argv[-1]


if PREFIX == "RPM":
    os.chmod("integration/com.github.hakand34.system-monitoring-center.desktop", 0o644)
    os.chmod("translations/cs/system-monitoring-center.mo", 0o644)
    os.chmod("translations/pl/system-monitoring-center.mo", 0o644)
    os.chmod("translations/pt_BR/system-monitoring-center.mo", 0o644)
    os.chmod("translations/tr/system-monitoring-center.mo", 0o644)
    os.chmod("man/system-monitoring-center.1.gz", 0o644)
    for file in files_in_folder("src/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("ui/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("icons/actions/"):
        os.chmod(file, 0o644)
    os.chmod("icons/apps/system-monitoring-center.svg", 0o644)
    os.chmod("integration/com.github.hakand34.system-monitoring-center.policy", 0o644)
    os.chmod("integration/system-monitoring-center", 0o644)
    data_files = [
        (build_root + "/usr/share/applications/", ["integration/com.github.hakand34.system-monitoring-center.desktop"]),
        (build_root + "/usr/share/locale/cs/LC_MESSAGES/", ["translations/cs/system-monitoring-center.mo"]),
        (build_root + "/usr/share/locale/pl/LC_MESSAGES/", ["translations/pl/system-monitoring-center.mo"]),
        (build_root + "/usr/share/locale/pt_BR/LC_MESSAGES/", ["translations/pt_BR/system-monitoring-center.mo"]),
        (build_root + "/usr/share/locale/tr/LC_MESSAGES/", ["translations/tr/system-monitoring-center.mo"]),
        (build_root + "/usr/share/man/man1/", ["man/system-monitoring-center.1.gz"]),
        (build_root + "/usr/share/system-monitoring-center/src/", files_in_folder("src/")),
        (build_root + "/usr/share/system-monitoring-center/ui/", files_in_folder("ui/")),
        (build_root + "/usr/share/icons/hicolor/scalable/actions/", files_in_folder("icons/actions/")),
        (build_root + "/usr/share/icons/hicolor/scalable/apps/", ["icons/apps/system-monitoring-center.svg"]),
        (build_root + "/usr/share/polkit-1/actions/", ["integration/com.github.hakand34.system-monitoring-center.policy"]),
        (build_root + "/usr/bin/", ["integration/system-monitoring-center"])
    ]

if PREFIX != "/app" and PREFIX != "RPM":
    for file in files_in_folder("ui/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("icons/actions/"):
        os.chmod(file, 0o644)
    os.chmod("icons/apps/system-monitoring-center.svg", 0o644)
    os.chmod("translations/cs/system-monitoring-center.mo", 0o644)
    os.chmod("translations/pl/system-monitoring-center.mo", 0o644)
    os.chmod("translations/pt_BR/system-monitoring-center.mo", 0o644)
    os.chmod("translations/tr/system-monitoring-center.mo", 0o644)
    os.chmod("integration/com.github.hakand34.system-monitoring-center.policy", 0o644)
    os.chmod("src/__version__", 0o644)
    data_files = [
        ("/usr/share/applications/", ["integration/com.github.hakand34.system-monitoring-center.desktop"]),
        ("/usr/share/locale/cs/LC_MESSAGES/", ["translations/cs/system-monitoring-center.mo"]),
        ("/usr/share/locale/pl/LC_MESSAGES/", ["translations/pl/system-monitoring-center.mo"]),
        ("/usr/share/locale/pt_BR/LC_MESSAGES/", ["translations/pt_BR/system-monitoring-center.mo"]),
        ("/usr/share/locale/tr/LC_MESSAGES/", ["translations/tr/system-monitoring-center.mo"]),
        ("/usr/share/man/man1/", ["man/system-monitoring-center.1.gz"]),
        ("/usr/share/system-monitoring-center/src/", files_in_folder("src/")),
        ("/usr/share/system-monitoring-center/ui/", files_in_folder("ui/")),
        ("/usr/share/icons/hicolor/scalable/actions/", files_in_folder("icons/actions/")),
        ("/usr/share/icons/hicolor/scalable/apps/", ["icons/apps/system-monitoring-center.svg"]),
        ("/usr/share/polkit-1/actions/", ["integration/com.github.hakand34.system-monitoring-center.policy"]),
        ("/usr/bin/", ["integration/system-monitoring-center"])
    ]

setup(
    name="System Monitoring Center",
    version=version,
    packages=find_packages(),
    scripts=["integration/system-monitoring-center"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    description="Provides information about system performance and usage.",
    license="GPLv3",
    keywords="system monitor task manager center performance speed frequency cpu usage ram usage swap memory memory usage storage network usage download speed fps frame ratio processes users startup programs services environment variables shell variables os",
    url="https://github.com/hakandundar34coding/system-monitoring-center",
)
