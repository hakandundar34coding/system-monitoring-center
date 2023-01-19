Name:           system-monitoring-center
Version:        2.4.0
Release:        1%{?dist}
Summary:        Multi-featured system monitor
License:        GPLv3
URL:            https://github.com/hakandundar34coding/system-monitoring-center

BuildArch:      noarch

BuildRequires:  python3-setuptools

Requires:       dmidecode
Requires:       hwdata
Requires:       iproute
Requires:       python3 >= 3.6
Requires:       python3-cairo
# python3-gobject is installed on Fedora (python3-gi on Debian-like systems)
Requires:       python3-gobject
Requires:       util-linux >= 2.31

%description
Provides information about CPU/RAM/Disk/Network/GPU performance, sensors, processes, users, services and system.

%prep
# pass

%build
# pass

%install
python3 setup.py install --user --rpm_package --%{?buildroot}

%post
sudo chown -R $USER /usr/share/system-monitoring-center/src/Main.py

%files
%defattr(-,root,root,-)
/usr/share/applications/io.github.hakandundar34coding.system-monitoring-center.desktop
/usr/share/polkit-1/actions/io.github.hakandundar34coding.system-monitoring-center.policy
/usr/share/system-monitoring-center/database/*
/usr/share/system-monitoring-center/icons/hicolor/scalable/actions/system-monitoring-center*
/usr/share/system-monitoring-center/icons/hicolor/scalable/apps/system-monitoring-center*
/usr/share/system-monitoring-center/locale/*/LC_MESSAGES/system-monitoring-center.mo
/usr/share/system-monitoring-center/*
/usr/share/icons/hicolor/scalable/apps/system-monitoring-center*
/usr/share/man/man1/system-monitoring-center.1.gz
/usr/bin/system-monitoring-center

%changelog
# pass

