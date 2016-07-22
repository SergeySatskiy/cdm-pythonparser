#!/bin/bash -x

export projectfull="$1"
export project="$2"
export version="$3"

export CDM_PROJECT_BUILD_VERSION="$3"

mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

cp ~/result/${projectfull}.tar.gz ~/rpmbuild/SOURCES/${projectfull}.tar.gz
tar xzf ~/result/${projectfull}.tar.gz
cp ${projectfull}/pkg/${project}.spec ~/rpmbuild/SPECS

sudo version=${version} yum-builddep -y ~/rpmbuild/SPECS/${project}.spec
rpmbuild -ba --define "version $version" ~/rpmbuild/SPECS/${project}.spec

rm ~/rpmbuild/RPMS/x86_64/*debuginfo*.rpm
mv -f ~/rpmbuild/RPMS/x86_64/*.rpm ~/result/

