%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

%define debug_package %{nil}

%define real_name	php-simplepcap
%define php_base	php55u
%define basever		5.5

Name:		SimplePcap
Version:	0.3
Release:	1%{?dist}
Summary:	SimplePcap PHP Module

License:	Unknown
URL:		https://github.com/giggsey/SimplePcap
Source0:	https://github.com/giggsey/SimplePcap/archive/%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	%{php_base}-devel
BuildRequires:	swig

%if 0%{?php_zend_api:1}
Requires:	%{php_base}(zend-abi) = %{php_zend_api}
Requires:	%{php_base}(api) = %{php_core_api}
%else
# for EL-5
Requires:	%{php_base}-api = %{php_apiver}
%endif


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
SimplePcap PHP Module

%prep
%setup -q


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{php_extdir}
%{__mkdir_p} %{buildroot}/usr/share/php
%{__mv} build/SimplePcap.so %{buildroot}%{php_extdir}/SimplePcap.so
%{__mv} build/SimplePcap.php %{buildroot}/usr/share/php/SimplePcap.php

%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/SimplePcap.ini << 'EOF'
; Enable %{realname} extension module
extension=SimplePcap.so
EOF


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/SimplePcap.ini
%{php_extdir}/SimplePcap.so
/usr/share/php/SimplePcap.php

%changelog

