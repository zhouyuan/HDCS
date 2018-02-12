#!/bin/bash

set -ex
. /etc/os-release

if [ "$ID" = "ubuntu" ] || [ "$ID" = "debian" ]; then
    apt-get install -y libaio-dev libboost-all-dev
elif [ "$ID" = "centos" ] || [ "$ID" = "fedora" ]; then
    yum install -y libaio-devel boost-devel
fi


mkdir -p build
(
   #
   # building
   #
   cd build
   cmake ..
   make VERBOSE=1
   #
   # testing
   #
   #ctest -V
   #
   # source distribution and documentation
   #
   make VERBOSE=1 install
)
