#!/usr/bin/env bash
#
# Small script to install python-hsmclient to local filesystem

HSMCLIENT_ROOT_PATH=debian/python-hsmclient

VERSION=%VERSION%
RELEASE=%RELEASE%
export PBR_VERSION=${VERSION}.${RELEASE}

python setup.py build
python setup.py install -O1 --skip-build --root $HSMCLIENT_ROOT_PATH

#---------------------------
# usr/share/doc
#---------------------------
install -g root -o root -v -m 640 -d $HSMCLIENT_ROOT_PATH/usr/share/doc/python-hsmclient-${VERSION}
install -g root -o root -v -m 640 -t $HSMCLIENT_ROOT_PATH/usr/share/doc/python-hsmclient-${VERSION} LICENSE
