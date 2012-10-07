#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Clutter Gesture library
Summary(pl.UTF-8):	Biblioteka gestów Clutter
Name:		clutter-gesture
Version:	0.0.2
%define	snap	20100106
Release:	0.%{snap}.1
License:	LGPL v2.1
Group:		Libraries
# git clone git://git.moblin.org/clutter-gesture
Source0:	%{name}.tar.xz
# Source0-md5:	7f3b287e4213f5be4e2f0054e1112e6b
Patch0:		%{name}-link.patch
URL:		http://www.moblin.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	clutter-devel >= 1.0.0
BuildRequires:	glib2-devel >= 2
#BuildRequires:	gtk-doc >= 1.9
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Clutter Gesture library allows clutter applications to be aware of
gestures and to easily attach some handlers to the gesture events.

%description -l pl.UTF-8
Biblioteka Clutter Gesture pozwala aplikacjom wykorzystujacych
bibliotekę clutter na obsługę gestów i łatwe podłączanie procedur
obsługi do zdarzeń gestów.

%package devel
Summary:	Header files for Clutter Gesture library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Clutter Gesture
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	clutter-devel >= 1.0.0
Requires:	glib2-devel >= 2

%description devel
Header files for Clutter Gesture library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Clutter Gesture.

%package static
Summary:	Static Clutter Gesture library
Summary(pl.UTF-8):	Statyczna biblioteka Clutter Gesture
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Clutter Gesture library.

%description static -l pl.UTF-8
Statyczna biblioteka Clutter Gesture.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# disable some warnings, so it builds with -Werror
CFLAGS="%{rpmcflags} -Wno-unused-but-set-variable -Wno-deprecated-declarations -Wno-switch -Wno-unused-result"
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libcluttergesture-0.0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcluttergesture-0.0.2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcluttergesture-0.0.2.so
%{_includedir}/clutter-gesture
%{_pkgconfigdir}/clutter-gesture.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcluttergesture-0.0.2.a
%endif
