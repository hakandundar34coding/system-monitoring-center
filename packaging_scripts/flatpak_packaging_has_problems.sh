#! /bin/sh

cd ..

flatpak-builder --force-clean build-dir com.github.hakand34.system-monitoring-center.yml
flatpak-builder --user --install --force-clean build-dir com.github.hakand34.system-monitoring-center.yml
flatpak run com.github.hakand34.system-monitoring-center
