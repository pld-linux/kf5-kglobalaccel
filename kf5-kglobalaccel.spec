#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.115
%define		qtver		5.15.2
%define		kfname		kglobalaccel

Summary:	Global desktop keyboard shortcuts
Name:		kf5-%{kfname}
Version:	5.115.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	97f8e0b90a7c2ae352a9c6b3442e1a1f
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kcrash-devel >= %{version}
BuildRequires:	kf5-kdbusaddons-devel >= %{version}
BuildRequires:	kf5-kwindowsystem-devel >= %{version}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{version}
Requires:	kf5-kcoreaddons >= %{version}
Requires:	kf5-kcrash >= %{version}
Requires:	kf5-kdbusaddons >= %{version}
Requires:	kf5-kwindowsystem >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KGlobalAccel allows you to have global accelerators that are
independent of the focused window. Unlike regular shortcuts, the
application's window does not need focus for them to be activated.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5DBus-devel >= %{qtver}
Requires:	Qt5Widgets-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kglobalaccel5
%ghost %{_libdir}/libKF5GlobalAccel.so.5
%attr(755,root,root) %{_libdir}/libKF5GlobalAccel.so.*.*
%ghost %{_libdir}/libKF5GlobalAccelPrivate.so.5
%attr(755,root,root) %{_libdir}/libKF5GlobalAccelPrivate.so.*.*
%{_datadir}/dbus-1/interfaces/kf5_org.kde.KGlobalAccel.xml
%{_datadir}/dbus-1/interfaces/kf5_org.kde.kglobalaccel.Component.xml
%{_datadir}/dbus-1/services/org.kde.kglobalaccel.service
%{_datadir}/kservices5/kglobalaccel5.desktop
%dir %{_libdir}/qt5/plugins/org.kde.kglobalaccel5.platforms
%attr(755,root,root) %{_libdir}/qt5/plugins/org.kde.kglobalaccel5.platforms/KF5GlobalAccelPrivateXcb.so
%{_datadir}/qlogging-categories5/kglobalaccel.categories
%{systemduserunitdir}/plasma-kglobalaccel.service
%{_datadir}/qlogging-categories5/kglobalaccel.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KGlobalAccel
%{_libdir}/cmake/KF5GlobalAccel
%{_libdir}/libKF5GlobalAccel.so
%{qt5dir}/mkspecs/modules/qt_KGlobalAccel.pri
