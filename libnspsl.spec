#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	NetSurf public suffix list handling
Name:		libnspsl
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	b09c9141bc157bf486a6950d2a5df58b
URL:		http://www.netsurf-browser.org/projects/libnspsl/
BuildRequires:	netsurf-buildsystem >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The public suffix list is a database of top level domain names
(https://publicsuffix.org). The database allows an application to
determine if if a domain name requires an additional label to be
valid.

%package devel
Summary:	libnspsl library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnspsl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate libnspsl into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnspsl w swoich
programach.

%package static
Summary:	libnspsl static library
Summary(pl.UTF-8):	Statyczna biblioteka libnspsl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnspsl library.

%description static -l pl.UTF-8
Statyczna biblioteka libnspsl.

%prep
%setup -q

%build
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libnspsl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnspsl.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnspsl.so
%{_includedir}/nspsl.h
%{_pkgconfigdir}/libnspsl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnspsl.a
%endif
