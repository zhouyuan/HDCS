%define version %{getenv:VERSION}
%define release %{getenv:RELEASE}

Name:             hsm-dashboard
Version:          %{version}
Release:          %{release}
Url:              http://intel.com/itflex
License:          Apache-2.0
Group:            Development/Languages/Python
Source:           %{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Summary:          Web based management interface for HSM

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python-pbr

Requires:         python-setuptools
Requires:         python-pbr
Requires:         python-django
Requires:         python-django-horizon
Requires:         python-django-compressor
Requires:         python-keystoneclient
Requires:         python-django-openstack-auth
Requires:         python-hsmclient

%description
The HSM Dashboard is a reference implementation of a Django site that
uses the Django project to provide web based interactions with the
HSM cloud controller.

%prep
%setup -q -n %{name}-%{version}

%build
export PBR_VERSION=%{version}.%{release}
%{__python} setup.py build

%install
rm -rf %{buildroot}

#---------------------------
# httpd Configuration file
#---------------------------
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -D -m 755 hsm-dashboard.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/hsm-dashboard.conf

#---------------------------
# bin Files for lessc
#---------------------------
install -d -m 755 %{buildroot}%{_bindir}
install -p -D -m 755 bin/less/lessc %{buildroot}%{_bindir}/
cp -av bin/lib/ %{buildroot}%{_libdir}/

#---------------------------
# Source files.
#---------------------------
install -d -m 755 %{buildroot}%{_datadir}/hsm-dashboard
cp -av hsm_dashboard %{buildroot}%{_datadir}/hsm-dashboard/
cp -av static %{buildroot}%{_datadir}/hsm-dashboard/
install -p -D -m 755 manage.py %{buildroot}%{_datadir}/hsm-dashboard/

%clean
%{__rm} -rf %{buildroot}

%post

mkdir -p %{_sysconfdir}/hsm-dashboard
chown -R apache:apache %{_sysconfdir}/hsm-dashboard
rm -rf %{_sysconfdir}/hsm-dashboard/*
ln -sf %{_datadir}/hsm-dashboard/hsm_dashboard/local/local_settings.py %{_sysconfdir}/hsm-dashboard/local_settings

chmod -R a+r %{_datadir}/hsm-dashboard
chown -R apache:apache %{_datadir}/hsm-dashboard
chown -R apache:apache %{_sysconfdir}/hsm-dashboard
chown -R apache:apache %{_sysconfdir}/httpd/conf.d/hsm-dashboard.conf

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/httpd/conf.d
%config(noreplace) %attr(-, root, apache) %{_sysconfdir}/httpd/conf.d/hsm-dashboard.conf

#%dir %{_bindir}
%config(noreplace) %attr(-, root, apache) %{_bindir}/lessc

%dir %attr(0755, apache, apache) %{_libdir}/less
%{_libdir}/less/*

%dir %attr(0755, apache, apache) %{_datadir}/hsm-dashboard
%{_datadir}/hsm-dashboard/*
%config(noreplace) %attr(-, apache, apache) %{_datadir}/hsm-dashboard/hsm_dashboard/local/local_settings.py
