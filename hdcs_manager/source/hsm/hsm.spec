%define version %{getenv:VERSION}
%define release %{getenv:RELEASE}

Name:             hsm
Version:          %{version}
Release:          %{release}
Summary:          Hyperstash Manager for Managing Hyperstash(Client Side Cache)

Group:            Storage/System
License:          Intel
URL:              http://intel.com
Source:           %{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python-pbr

Requires:         MySQL-python
Requires:         python-pbr
Requires:         python-sqlalchemy
Requires:         python-amqplib
Requires:         python-anyjson
Requires:         python-eventlet
Requires:         python-kombu
Requires:         python-lxml
Requires:         python-routes
Requires:         python-webob
Requires:         python-greenlet
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python-migrate
Requires:         python-stevedore
Requires:         python-paramiko
Requires:         python-iso8601
Requires:         python-oslo-config
Requires:         python-psutil

%description
Hyperstash Manager (HSM) is software that Intel has developed
to help to manage Hyperstash(which is a Client Side Cache).

%prep
%setup -q -n hsm-%{version}

%build
export PBR_VERSION=%{version}.%{release}
%{__python} setup.py build

%install
export PBR_VERSION=%{version}.%{release}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

cp -rf hsm/db/sqlalchemy/migrate_repo/migrate.cfg %{buildroot}/usr/lib/python2.7/site-packages/hsm/db/sqlalchemy/migrate_repo
cp -rf hsm/diamond %{buildroot}/usr/lib/python2.7/site-packages/hsm/

#---------------------------
# var/lib/hsm
#---------------------------
install -d -m 755 %{buildroot}%{_sharedstatedir}/hsm

#---------------------------
# var/log/hsm
#---------------------------
install -d -m 755 %{buildroot}%{_localstatedir}/log/hsm

#---------------------------
# etc/rc.d/init.d
#---------------------------
install -d -m 755 %{buildroot}%{_initrddir}
install -p -D -m 755 etc/init.d/centos7/hsm-agent %{buildroot}%{_initrddir}/hsm-agent
install -p -D -m 755 etc/init.d/centos7/hsm-api %{buildroot}%{_initrddir}/hsm-api
install -p -D -m 755 etc/init.d/centos7/hsm-conductor %{buildroot}%{_initrddir}/hsm-conductor
install -p -D -m 755 etc/init.d/centos7/hsm-scheduler %{buildroot}%{_initrddir}/hsm-scheduler

#---------------------------
# etc/logrotate.d
#---------------------------
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -D -m 640 etc/logrotate.d/hsmrotate %{buildroot}%{_sysconfdir}/logrotate.d/hsmrotate

#---------------------------
# etc/sudoers.d
#---------------------------
install -d -m 755 %{buildroot}%{_sysconfdir}/sudoers.d
install -p -D -m 440 etc/sudoers.d/hsm %{buildroot}%{_sysconfdir}/sudoers.d/hsm

#---------------------------
# etc/hsm
#---------------------------
install -d -m 755 %{buildroot}%{_sysconfdir}/hsm
install -p -D -m 640 etc/hsm/api-paste.ini %{buildroot}%{_sysconfdir}/hsm/api-paste.ini
install -p -D -m 640 etc/hsm/hsm.conf.sample %{buildroot}%{_sysconfdir}/hsm/hsm.conf
install -p -D -m 640 etc/hsm/logging_sample.conf %{buildroot}%{_sysconfdir}/hsm/logging.conf
install -p -D -m 640 etc/hsm/policy.json %{buildroot}%{_sysconfdir}/hsm/policy.json
install -p -D -m 640 etc/hsm/rootwrap.conf %{buildroot}%{_sysconfdir}/hsm/rootwrap.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/hsm/rootwrap.d
install -p -D -m 640 etc/hsm/rootwrap.d/hsm.filters %{buildroot}%{_sysconfdir}/hsm/rootwrap.d/hsm.filters

#---------------------------
# usr/bin
#---------------------------
install -d -m 755 %{buildroot}%{_bindir}
install -p -D -m 755 bin/hsm-agent %{buildroot}%{_bindir}/hsm-agent
install -p -D -m 755 bin/hsm-all %{buildroot}%{_bindir}/hsm-all
install -p -D -m 755 bin/hsm-api %{buildroot}%{_bindir}/hsm-api
install -p -D -m 755 bin/hsm-assist %{buildroot}%{_bindir}/hsm-assist
install -p -D -m 755 bin/hsm-conductor %{buildroot}%{_bindir}/hsm-conductor
install -p -D -m 755 bin/hsm-manage %{buildroot}%{_bindir}/hsm-manage
install -p -D -m 755 bin/hsm-rootwrap %{buildroot}%{_bindir}/hsm-rootwrap
install -p -D -m 755 bin/hsm-scheduler %{buildroot}%{_bindir}/hsm-scheduler

%pre
getent group hsm >/dev/null || groupadd -r hsm --gid 265
if ! getent passwd hsm >/dev/null; then
  useradd -u 265 -r -g hsm -G hsm,nobody -d %{_sharedstatedir}/hsm -s /sbin/nologin -c "Hsm Storage Services" hsm
fi

exit 0

%files
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/*

%dir %attr(-, hsm, hsm) %{_sharedstatedir}/hsm

%dir %attr(-, hsm, hsm) %{_localstatedir}/log/hsm

%dir %{_initrddir}
%config(noreplace) %attr(-, root, hsm) %{_initrddir}/hsm-agent
%config(noreplace) %attr(-, root, hsm) %{_initrddir}/hsm-api
%config(noreplace) %attr(-, root, hsm) %{_initrddir}/hsm-conductor
%config(noreplace) %attr(-, root, hsm) %{_initrddir}/hsm-scheduler

%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/logrotate.d/hsmrotate

#%dir %{_sysconfdir}/sudoers.d
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/sudoers.d/hsm

%dir %{_sysconfdir}/hsm
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/hsm/api-paste.ini
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/hsm/hsm.conf
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/hsm/logging.conf
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/hsm/policy.json
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/hsm/rootwrap.conf

%dir %{_sysconfdir}/hsm/rootwrap.d
%config(noreplace) %attr(-, root, hsm) %{_sysconfdir}/hsm/rootwrap.d/hsm.filters

#%dir %{_bindir}
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-agent
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-all
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-api
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-assist
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-conductor
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-manage
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-rootwrap
%config(noreplace) %attr(-, root, hsm) %{_bindir}/hsm-scheduler
