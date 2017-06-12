#!/usr/bin/env bash
#
# Small script to install hsm to local filesystem

export HSM_ROOT_PATH=debian/hsm

VERSION=%VERSION%
RELEASE=%RELEASE%
echo $VERSION
echo $RELEASE
export PBR_VERSION=${VERSION}.${RELEASE}

getent group hsm >/dev/null || groupadd -r hsm --gid 265
if ! getent passwd hsm >/dev/null; then
  useradd -u 265 -r -g hsm -G hsm,nogroup -d /var/lib/hsm -s /usr/sbin/nologin -c "Hsm Storage Services" hsm
fi

python setup.py build
python setup.py install -O1 --skip-build --root $HSM_ROOT_PATH
cp -rf hsm/db/sqlalchemy/migrate_repo/migrate.cfg $HSM_ROOT_PATH/usr/local/lib/python2.7/dist-packages/hsm/db/sqlalchemy/migrate_repo
cp -rf hsm/diamond $HSM_ROOT_PATH/usr/local/lib/python2.7/dist-packages/hsm/

#---------------------------
# var/lib/hsm
#---------------------------
install -g hsm -o hsm -v -m 755 -d $HSM_ROOT_PATH/var/lib/hsm

#---------------------------
# var/log/hsm
#---------------------------
install -g hsm -o hsm -v -m 755 -d $HSM_ROOT_PATH/var/log/hsm

#---------------------------
# etc/init.d/
#---------------------------
install -g root -o root -v -m 755 -d $HSM_ROOT_PATH/etc/init.d
install -g root -o root -v -m 755 -t $HSM_ROOT_PATH/etc/init.d etc/init.d/ubuntu14/hsm-agent
install -g root -o root -v -m 755 -t $HSM_ROOT_PATH/etc/init.d etc/init.d/ubuntu14/hsm-api
install -g root -o root -v -m 755 -t $HSM_ROOT_PATH/etc/init.d etc/init.d/ubuntu14/hsm-conductor
install -g root -o root -v -m 755 -t $HSM_ROOT_PATH/etc/init.d etc/init.d/ubuntu14/hsm-scheduler

#---------------------------
# etc/logrotate.d
#---------------------------
install -g root -o root -v -m 755 -d $HSM_ROOT_PATH/etc/logrotate.d
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/logrotate.d etc/logrotate.d/hsmrotate

#---------------------------
# etc/sudoers.d
#---------------------------
install -g root -o root -v -m 755 -d $HSM_ROOT_PATH/etc/sudoers.d
install -g root -o root -v -m 640 -t $HSM_ROOT_PATH/etc/sudoers.d etc/sudoers.d/hsm

#---------------------------
# etc/hsm
#---------------------------
install -g root -o root -v -m 755 -d $HSM_ROOT_PATH/etc/hsm
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/hsm etc/hsm/api-paste.ini
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/hsm/ etc/hsm/hsm.conf.sample
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/hsm/ etc/hsm/logging_sample.conf
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/hsm etc/hsm/policy.json
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/hsm etc/hsm/rootwrap.conf
install -g root -o root -v -m 755 -d $HSM_ROOT_PATH/etc/hsm/rootwrap.d
install -g root -o hsm -v -m 640 -t $HSM_ROOT_PATH/etc/hsm/rootwrap.d etc/hsm/rootwrap.d/hsm.filters

#---------------------------
# usr/bin/
#---------------------------
install -g root -o root -v -m 755 -d $HSM_ROOT_PATH/usr/bin
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-agent
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-all
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-api
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-assist
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-conductor
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-manage
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-rootwrap
install -g root -o hsm -v -m 755 -t $HSM_ROOT_PATH/usr/bin bin/hsm-scheduler

#---------------------------
# usr/local/bin/
#---------------------------
rm -rf $HSM_ROOT_PATH/usr/local/bin/*

#---------------------------
# usr/share/doc
#---------------------------
install -g root -o root -v -m 640 -d $HSM_ROOT_PATH/usr/share/doc/hsm-${VERSION}
install -g root -o root -v -m 640 -t $HSM_ROOT_PATH/usr/share/doc/hsm-${VERSION} LICENSE
