%define version %{getenv:VERSION}
%define release %{getenv:RELEASE}

Name:             python-hsmclient
Version:          %{version}
Release:          %{release}
Summary:          Python API and CLI for hsm

Group:            Development/Languages
License:          Intel
URL:              http://intel.com
Source:           %{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python-pbr

Requires:         python-pbr
Requires:         python-babel
Requires:         python-six
Requires:         python-requests
Requires:         python-prettytable

%description
This is a client for the hsm API. There's a Python API
(the hsmclient module), and a command-line script (hsm).
Each implements 100% of the hsm API.

%prep
%setup -q -n python-hsmclient-%{version}

%build
export PBR_VERSION=%{version}.%{release}
%{__python} setup.py build

%install
export PBR_VERSION=%{version}.%{release}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/hsm
%{python_sitelib}/*
