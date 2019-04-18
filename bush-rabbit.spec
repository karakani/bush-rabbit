%define name              bush-rabbit
%define version           0.1
%define unmangled_version 0.1
%define release           1
%define INSTALLDIR        %{buildroot}/usr/local/sbin

Summary:   server management utilities
Name:      %{name}
Version:   %{version}
Release:   %{release}
License:   MIT
Prefix:    %{_prefix}
BuildArch: noarch
Source:    bush-rabbit.tgz
Requires:  python

%description
simple and small server management utilities.

%prep
%setup -n %{name}
rm -rf %{buildroot}

%build

%install
mkdir   -p                  %{INSTALLDIR}
install -m 755 cronrun2.py  %{INSTALLDIR}/cronrun

%clean
rm -rf %{buildroot}

%files
%defattr(755, root, root)
/usr/local/sbin/cronrun
