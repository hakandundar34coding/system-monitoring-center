Name:       system-monitoring-center
Version:    0.1.21~beta19
Release:    1%{?dist}
Summary:    Provides information about system performance and usage.
License:    GPLv3
URL:        https://github.com/hakandundar34coding/system-monitoring-center

BuildRequires:  python3-setuptools

Requires:       python3 >= 3.7
# python3-gobject is installed on Fedora (python3-gi on Debian-like systems)
Requires:       python3-gobject
# python3-pyopengl is installed on Fedora (python3-opengl on Debian-like systems)
Requires:       python3-pyopengl
Requires:       util-linux >= 2.33
Requires:       glx-utils
Requires:       systemd
Requires:       bash >= 5.0
# hwdata package is installed on Fedora for pci.ids file.
Requires:       hwdata
Requires:       dmidecode

%description
Provides information about CPU/RAM/Disk/Network/GPU performance, sensors, processes, users, storage, startup programs, services, environment variables and system.

%prep
# pass

%build
# pass

%install
python3 setup.py install --user --rpm --%{?buildroot}

%post
sudo chown -R $USER /usr/share/system-monitoring-center/src/Main.py

%files
%defattr(-,root,root,-)
/usr/bin/system-monitoring-center
/usr/share/applications/tr.org.pardus.system-monitoring-center.desktop
/usr/share/icons/hicolor/scalable/actions/system-monitoring-center*
/usr/share/icons/hicolor/scalable/apps/system-monitoring-center*
/usr/share/locale/*/LC_MESSAGES/system-monitoring-center.mo
/usr/share/man/man1/system-monitoring-center.1.gz
/usr/share/polkit-1/actions/tr.org.pardus.pkexec.system-monitoring-center.policy
/usr/share/system-monitoring-center/*

%changelog
# pass

