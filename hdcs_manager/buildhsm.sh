#!/usr/bin/env bash

set -e
set -o xtrace

TOPDIR=$(cd $(dirname "$0") && pwd)
TEMP=`mktemp`; rm -rfv $TEMP >/dev/null; mkdir -p $TEMP;

VERSION=`cat VERSION`
export VERSION
RELEASE=`cat RELEASE`
export RELEASE
BUILD="${VERSION}-${RELEASE}"

is_lsb_release=0
lsb_release -a >/dev/null 2>&1 && is_lsb_release=1

if [[ $is_lsb_release -gt 0 ]]; then
    OS=`lsb_release -a|grep "Distributor ID:"|awk -F ' ' '{print $3}'`
    OS_VERSION=`lsb_release -a|grep "Release"|awk -F ' ' '{print $2}'`
else
    var=`cat /etc/os-release|grep "PRETTY_NAME"|awk -F "=" '{print $2}'`
    if [[ $var =~ "CentOS Linux 7" ]]; then
        OS="CentOS"
        OS_VERSION="7"
    fi
fi

TEMP_HSM=`mktemp`; rm -rfv $TEMP_HSM >/dev/null; mkdir -p $TEMP_HSM;
mkdir -p $TEMP_HSM/release/$BUILD
cp -rf * $TEMP_HSM
cp -rf .lib $TEMP_HSM
cd $TEMP_HSM

function create_release() {
    if [[ $OS == "Ubuntu" && $OS_VERSION =~ "14" ]]; then
        bash +x builddeb
        cp diamond_4.0_all.deb release/$BUILD
    elif [[ $OS == "CentOS" && $OS_VERSION =~ "7" ]]; then
        bash +x buildrpm
        cp diamond-4-0.noarch.rpm release/$BUILD
    fi

    cp VERSION release/$BUILD
    cp RELEASE release/$BUILD
    cp README.md release/$BUILD
    cp install.sh release/$BUILD
    cp upgrade.sh release/$BUILD
    cp installrc release/$BUILD
    cp -r hsmrepo release/$BUILD

    cd release
    tar -czvf $BUILD.tar.gz $BUILD
    rm -rf $BUILD
    cp -r $TEMP_HSM/release $TOPDIR
    cp -r $TEMP_HSM/hsmrepo $TOPDIR

}

create_release

rm -rf $TEMP_HSM

cd ${TOPDIR}
echo -n $((++RELEASE)) > RELEASE

set +o xtrace

