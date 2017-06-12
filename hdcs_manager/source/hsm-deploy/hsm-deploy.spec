%define version %{getenv:VERSION}
%define release %{getenv:RELEASE}

Name:             hsm-deploy
Version:          %{version}
Release:          %{release}
Summary:          Deployment tool for HSM

Group:            Deploy/HSM
License:          Intel
URL:              http://intel.com
Source:           %{name}-%{version}.tar.gz

%description
Intel HSM Storage System Tools Kit.

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p %{buildroot}

%install

#---------------------------
# usr/bin/
#---------------------------
install -d -m 755 %{buildroot}%{_usr}/local/bin/

install -p -D -m 755 hsm-deploy %{buildroot}%{_usr}/local/bin/hsm-deploy
install -p -D -m 755 hsm-generate-deployrc %{buildroot}%{_usr}/local/bin/hsm-generate-deployrc
install -p -D -m 755 hsm-preinstall %{buildroot}%{_usr}/local/bin/hsm-preinstall

cp -rf hsm-lib %{buildroot}%{_usr}/local/bin/

%files
%defattr(-,root,root,-)
%dir %{_usr}/local/bin
%config(noreplace) %attr(-, root, hsm) %{_usr}/local/bin/hsm-deploy
%config(noreplace) %attr(-, root, hsm) %{_usr}/local/bin/hsm-generate-deployrc
%config(noreplace) %attr(-, root, hsm) %{_usr}/local/bin/hsm-preinstall

%dir %{_usr}/local/bin/hsm-lib
%config(noreplace) %attr(-, root, hsm) %{_usr}/local/bin/hsm-lib/*
