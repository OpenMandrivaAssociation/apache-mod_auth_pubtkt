#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_auth_pubtkt
%define mod_conf B32_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A pragmatic Web Single Sign-On (SSO) solution
Name:		apache-%{mod_name}
Version:	0.6a
Release:	%mkrel 3
Group:		System/Servers
License:	BSD-like
URL:		https://neon1.net/mod_auth_pubtkt/
Source0:	https://neon1.net/mod_auth_pubtkt/mod_auth_pubtkt-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRequires:  openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_auth_pubtkt is an Apache module that authenticates a user based on a cookie
with a ticket that has been issued by a central login server and digitally
signed using either RSA or DSA.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

%build
sh configure --apachever=2.2

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 src/.libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc php-login LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

