#! /bin/sh

current_directory=$(pwd)
parent_directory="$(dirname "$current_directory")"

version_file="${parent_directory}/src/__version__"
version=$(cat "$version_file")
new_version="Version: ${version} "

deb_files_directory="${current_directory}/system-monitoring-center_${version}_amd64"


mkdir -p "${deb_files_directory}"

mkdir -p "${deb_files_directory}/DEBIAN/"
cp -R control "${deb_files_directory}/DEBIAN/"

mkdir -p "${deb_files_directory}/usr/bin/"
cp -R "${parent_directory}/integration/system-monitoring-center" "${deb_files_directory}/usr/bin/"

mkdir -p "${deb_files_directory}/usr/share/applications/"
cp -R "${parent_directory}/integration/tr.org.pardus.system-monitoring-center.desktop" "${deb_files_directory}/usr/share/applications/"

mkdir -p "${deb_files_directory}/usr/share/doc/system-monitoring-center/"
cp -R "${parent_directory}/debian/copyright" "${deb_files_directory}/usr/share/doc/system-monitoring-center/"
mkdir -p "${deb_files_directory}/usr/share/doc/system-monitoring-center/changelog/"
cp -R "${parent_directory}/debian/changelog" "${deb_files_directory}/usr/share/doc/system-monitoring-center/changelog/"

mkdir -p "${deb_files_directory}/usr/share/icons/hicolor/scalable/"
cp -R "${parent_directory}/icons/actions/" "${deb_files_directory}/usr/share/icons/hicolor/scalable/"
cp -R "${parent_directory}/icons/apps/" "${deb_files_directory}/usr/share/icons/hicolor/scalable/"

mkdir -p "${deb_files_directory}/usr/share/locale/tr/LC_MESSAGES/"
cp -R "${parent_directory}/translations/tr/system-monitoring-center.mo" "${deb_files_directory}/usr/share/locale/tr/LC_MESSAGES/"

mkdir -p "${deb_files_directory}/usr/share/polkit-1/actions/"
cp -R "${parent_directory}/integration/tr.org.pardus.pkexec.system-monitoring-center.policy" "${deb_files_directory}/usr/share/polkit-1/actions/"

mkdir -p "${deb_files_directory}/usr/share/system-monitoring-center/"
cp -R "${parent_directory}/src/" "${deb_files_directory}/usr/share/system-monitoring-center/"
cp -R "${parent_directory}/ui/" "${deb_files_directory}/usr/share/system-monitoring-center/"


sed -i "s/^.*\bVersion: \b.*$/$new_version/" "${deb_files_directory}/DEBIAN/control"


size_of_deb_files_directory=$(du -sb "$deb_files_directory" | cut -f1)
size_of_deb_files_directory=$(( $size_of_deb_files_directory / 1024 ))
size_string="Installed-Size: "$size_of_deb_files_directory
sed -i "s/^.*\bInstalled-Size: \b.*$/$size_string/" "${deb_files_directory}/DEBIAN/control"


dpkg-deb --build $deb_files_directory
