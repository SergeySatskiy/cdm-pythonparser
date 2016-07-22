#!/bin/bash -x

projectfull="$1"
project="$2"
version="$3"

cp ~/result/${projectfull}.tar.gz ${project}_${version}.orig.tar.gz

# Use unstable for all debians
# but must set distro name for ubuntu
DISTRO=unstable
VENDOR=$(lsb_release -si)

if [ "${VENDOR}" == "Ubuntu" ]; then
	DISTRO=$(lsb_release -sc)
fi

tar xzf ${project}_${version}.orig.tar.gz

(
	export DH_VERBOSE=1
	export DEBIAN_FRONTEND="noninteractive"
	export DEBFULLNAME="Sergey Satskiy"
	export DEBEMAIL="sergey.satskiy@gmail.com"
	export CDM_PROJECT_BUILD_VERSION="${version}"
	cd ${projectfull}
	sudo mk-build-deps -i --tool "apt-get -y"
	rm -f *.deb
	dch --force-bad-version --distribution ${DISTRO} --package ${project} --newversion ${version}-$(lsb_release -si)~$(lsb_release -sc) "new release"
	debuild --set-envvar CDM_PROJECT_BUILD_VERSION="${version}" -us -uc
)

#mv -f *.deb ~/result/

