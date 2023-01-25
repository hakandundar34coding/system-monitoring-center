#!/bin/sh

current_directory=$(pwd)
parent_directory="$(dirname "$current_directory")"

cd $parent_directory
xgettext -k_tr -kN_tr --from-code utf-8  -o "${current_directory}/system-monitoring-center.pot" ./src/*.py ./ui/*.ui
