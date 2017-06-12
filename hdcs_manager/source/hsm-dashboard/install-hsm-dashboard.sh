#!/usr/bin/env bash
#
# Small script to install hsm-dashboard to local filesystem

export HSM_DASHBOARD_ROOT_PATH=debian/hsm-dashboard

VERSION=%VERSION%
RELEASE=%RELEASE%
export PBR_VERSION=${VERSION}.${RELEASE}

python setup.py build

#---------------------------
# etc/apache2/conf-available
#---------------------------
install -g root -o root -v -m 755 -d $HSM_DASHBOARD_ROOT_PATH/etc/apache2/conf-available
sed -i "s,WSGISocketPrefix run/wsgi,# WSGISocketPrefix run/wsgi,g" hsm-dashboard.conf
install -g root -o root -v -m 755 -t $HSM_DASHBOARD_ROOT_PATH/etc/apache2/conf-available hsm-dashboard.conf

#---------------------------
# usr/bin
#---------------------------
install -g root -o root -v -m 755 -d $HSM_DASHBOARD_ROOT_PATH/usr/bin
install -g root -o root -v -m 755 -t $HSM_DASHBOARD_ROOT_PATH/usr/bin bin/less/lessc

#---------------------------
# usr/lib
#---------------------------
install -g root -o root -v -m 755 -d $HSM_DASHBOARD_ROOT_PATH/usr/lib
cp -av bin/lib/less $HSM_DASHBOARD_ROOT_PATH/usr/lib

#---------------------------
# usr/share/hsm-dashboard
#---------------------------
install -g root -o root -v -m 755 -d $HSM_DASHBOARD_ROOT_PATH/usr/share/hsm-dashboard
cp -av hsm_dashboard $HSM_DASHBOARD_ROOT_PATH/usr/share/hsm-dashboard
cp -av static $HSM_DASHBOARD_ROOT_PATH/usr/share/hsm-dashboard
install -g root -o root -v -m 755 -t $HSM_DASHBOARD_ROOT_PATH/usr/share/hsm-dashboard manage.py
