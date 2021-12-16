#! /bin/sh

cd ..

flatpak-builder --force-clean build-dir tr.org.pardus.system-monitoring-center.yml
flatpak-builder --user --install --force-clean build-dir tr.org.pardus.system-monitoring-center.yml
flatpak run tr.org.pardus.system-monitoring-center
