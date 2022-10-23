#!/bin/sh

cd ..

flatpak-builder --force-clean build-dir io.github.hakandundar34coding.system-monitoring-center.yml
flatpak-builder --user --install --force-clean build-dir io.github.hakandundar34coding.system-monitoring-center.yml
flatpak run io.github.hakandundar34coding.system-monitoring-center
