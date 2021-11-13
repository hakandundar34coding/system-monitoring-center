#! /bin/sh

rpmdev-setuptree
cp -a ./. ~/rpmbuild/BUILD

rpmbuild -ba system-monitoring-center.spec

