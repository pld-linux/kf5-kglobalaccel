#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	5.116
%define		qt_ver		5.15.2
%define		kf_ver		%{version}
%define		kfname		kglobalaccel

Summary:	Global desktop keyboard shortcuts
Summary(pl.UTF-8):	Skróty klawiaturowe globalne dla pulpitu
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	6ce31a55aed1a20c18710c125efceca8
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
%{?with_tests:BuildRequires:	Qt5Test-devel >= %{qt_ver}}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5X11Extras-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	kf5-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kcrash-devel >= %{kf_ver}
BuildRequires:	kf5-kdbusaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kwindowsystem-devel >= %{kf_ver}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
# allow using also kp6-kglobalacceld service (for parallel install of kf5-kglobalacel and kp6-kglobalacceld)
Requires:	%{name}-service >= %{version}-%{release}
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5DBus >= %{qt_ver}
Requires:	Qt5Widgets >= %{qt_ver}
Requires:	Qt5X11Extras >= %{qt_ver}
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{kf_ver}
Requires:	kf5-kcoreaddons >= %{kf_ver}
Requires:	kf5-kwindowsystem >= %{kf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KGlobalAccel allows you to have global accelerators that are
independent of the focused window. Unlike regular shortcuts, the
application's window does not need focus for them to be activated.

%description -l pl.UTF-8
KGlobalAccel pozwala tworzyć skróty klawiaturowe niezależne od
wybranego okna. W przeciwieństwie do zwykłych skrótów, do ich
zadziałania okno aplikacji nie musi być wybranym.

%package service
Summary:	KDED global shortcuts server
Summary(pl.UTF-8):	Globalny serwer skrótów KDED
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	kf5-kcrash >= %{kf_ver}
Requires:	kf5-kdbusaddons >= %{kf_ver}
Conflicts:	kp6-kglobalacceld

%description service
KDED global shortcuts server.

%description service -l pl.UTF-8
Globalny serwer skrótów KDED.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5DBus-devel >= %{qt_ver}
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF5GlobalAccel.so.*.*
%ghost %{_libdir}/libKF5GlobalAccel.so.5
%attr(755,root,root) %{_libdir}/libKF5GlobalAccelPrivate.so.*.*
%ghost %{_libdir}/libKF5GlobalAccelPrivate.so.5
%{_datadir}/dbus-1/interfaces/kf5_org.kde.KGlobalAccel.xml
%{_datadir}/dbus-1/interfaces/kf5_org.kde.kglobalaccel.Component.xml
%{_datadir}/qlogging-categories5/kglobalaccel.categories
%{_datadir}/qlogging-categories5/kglobalaccel.renamecategories

%files service
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kglobalaccel5
%dir %{_libdir}/qt5/plugins/org.kde.kglobalaccel5.platforms
%attr(755,root,root) %{_libdir}/qt5/plugins/org.kde.kglobalaccel5.platforms/KF5GlobalAccelPrivateXcb.so
%{_datadir}/dbus-1/services/org.kde.kglobalaccel.service
%{_datadir}/kservices5/kglobalaccel5.desktop
%{systemduserunitdir}/plasma-kglobalaccel.service

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5GlobalAccel.so
%{_includedir}/KF5/KGlobalAccel
%{_libdir}/cmake/KF5GlobalAccel
%{qt5dir}/mkspecs/modules/qt_KGlobalAccel.pri
