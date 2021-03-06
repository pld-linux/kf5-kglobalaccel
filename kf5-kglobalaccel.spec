%define		kdeframever	5.79
%define		qtver		5.9.0
%define		kfname		kglobalaccel

Summary:	Global desktop keyboard shortcuts
Name:		kf5-%{kfname}
Version:	5.79.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	6e5217c6621e97fe90e99385720f968d
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kcrash-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
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

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

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
%attr(755,root,root) %ghost %{_libdir}/libKF5GlobalAccel.so.5
%attr(755,root,root) %{_libdir}/libKF5GlobalAccel.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5GlobalAccelPrivate.so.5
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
%{_includedir}/KF5/kglobalaccel_version.h
%{_libdir}/cmake/KF5GlobalAccel
%attr(755,root,root) %{_libdir}/libKF5GlobalAccel.so
#%attr(755,root,root) %{_libdir}/libKF5GlobalAccelPrivate.so
%{qt5dir}/mkspecs/modules/qt_KGlobalAccel.pri
