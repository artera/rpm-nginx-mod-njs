Summary: nginScript module for nginx
Name: nginx-mod-njs
Version: 0.3.7
Release: 1%{?dist}
Vendor: Artera
URL: https://nginx.org/en/docs/njs_about.html

%define _modname            njs
%define _nginxver           1.16.1
%define nginx_config_dir    %{_sysconfdir}/nginx
%define nginx_build_dir     %{_builddir}/nginx-%{_nginxver}

Source0: https://nginx.org/download/nginx-%{_nginxver}.tar.gz
Source1: https://hg.nginx.org/njs/archive/%{version}.tar.gz#/%{_modname}-%{version}.tar.gz

Requires: nginx = 1:%{_nginxver}
BuildRequires: nginx
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: perl-devel
BuildRequires: gd-devel
BuildRequires: GeoIP-devel
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: gperftools-devel

License: BSD

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
nginScript module for nginx.

%prep
%setup -q -n nginx-%{_nginxver}
%setup -T -D -b 1 -n %{_modname}-%{version}

%build
cd %{_builddir}/nginx-%{_nginxver}
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --with-stream --add-dynamic-module=../njs-%{version}/nginx
make modules

%install
%{__rm} -rf %{buildroot}

%{__install} -Dm755 %{nginx_build_dir}/objs/ngx_http_js_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_js_module.so
%{__install} -Dm755 %{nginx_build_dir}/objs/ngx_stream_js_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_stream_js_module.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*.so
