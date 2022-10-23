Name:           system-monitoring-center
Version:        1.4.0
Release:        1%{?dist}
Summary:        Provides information about system performance and usage.
License:        GPLv3
URL:            https://github.com/hakandundar34coding/system-monitoring-center

BuildArch:      noarch

BuildRequires:  python3-setuptools

Requires:       bash >= 4.4
Requires:       dmidecode
Requires:       iproute
Requires:       python3 >= 3.6
Requires:       python3-cairo
# python3-gobject is installed on Fedora (python3-gi on Debian-like systems)
Requires:       python3-gobject
Requires:       systemd
Requires:       util-linux >= 2.31

%description
Multi-featured system monitor.

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
/usr/bin/system-monitoring-center
/usr/share/applications/com.github.hakandundar34coding.system-monitoring-center.desktop
/usr/share/icons/hicolor/scalable/actions/system-monitoring-center*
/usr/share/icons/hicolor/scalable/apps/system-monitoring-center*
/usr/share/locale/*/LC_MESSAGES/system-monitoring-center.mo
/usr/share/man/man1/system-monitoring-center.1.gz
/usr/share/polkit-1/actions/com.github.hakandundar34coding.system-monitoring-center.policy
/usr/share/system-monitoring-center/*

%changelog
# pass

