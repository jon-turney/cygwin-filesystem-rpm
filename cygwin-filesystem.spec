%global debug_package %{nil}

# Place RPM macros in %%{_rpmconfigdir}/macros.d if it exists (RPM 4.11+)
# Otherwise, use %%{_sysconfdir}/rpm
# https://lists.fedoraproject.org/pipermail/devel/2014-January/195026.html
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           cygwin-filesystem
Version:        14
Release:        1%{?dist}
Summary:        Cygwin cross compiler base filesystem and environment

Group:          Development/Libraries
License:        GPLv2+
URL:            http://cygwinports.org/
BuildArch:      noarch

Source0:        COPYING
Source1:        macros.cygwin
Source2:        macros.cygwin32
Source3:        macros.cygwin64
Source4:        cygwin32.sh
Source5:        cygwin64.sh
Source6:        cygwin-find-debuginfo.sh
Source7:        cygwin-find-requires.sh
Source8:        cygwin-find-provides.sh
Source9:        cygwin-scripts.sh
Source10:       cygwin-rpmlint.config
Source11:       toolchain-cygwin32.cmake
Source12:       toolchain-cygwin64.cmake
Source13:       cygwin-find-lang.sh
Source14:       cygwin32.attr
Source15:       cygwin64.attr
# generated with:
# (rpm -ql cygwin32-w32api-runtime | grep '\.a$' | while read f ; do i686-pc-cygwin-dlltool -I $f 2>/dev/null ; done) | tr A-Z a-z | sort -u > standard-dlls-cygwin32
Source16:       standard-dlls-cygwin32
# (rpm -ql cygwin64-w32api-runtime | grep '\.a$' | while read f ; do x86_64-pc-cygwin-dlltool -I $f 2>/dev/null ; done) | tr A-Z a-z | sort -u > standard-dlls-cygwin64
Source17:       standard-dlls-cygwin64


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora Cygwin packages.


%package base
Summary:        Generic files which are needed for both cygwin32-filesystem and cygwin64-filesystem

%description base
This package contains the base filesystem layout, RPM macros and
environment for all Fedora Cygwin packages.


%package -n cygwin32-filesystem
Summary:        Cygwin cross compiler base filesystem and environment for the i686 target
Requires:       %{name}-base = %{version}-%{release}
Provides:       cygwin-filesystem
Obsoletes:      cygwin-filesystem < 7-1

# Note about 'Provides: cygwin32(foo.dll)'
# ------------------------------------------------------------
#
# We want to be able to build & install cygwin32 libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the Cygwin toolchain to develop software (ie. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
Provides:       %(sed "s/\(.*\)/cygwin32(\1) /g" %{SOURCE16} | tr "\n" " ")
Provides:       cygwin32(mscoree.dll)
# for backwards compatibility with cygwin-filesystem <= 6
Provides:       cygwin(advapi32.dll)
Provides:       cygwin(avicap32.dll)
Provides:       cygwin(comctl32.dll)
Provides:       cygwin(comdlg32.dll)
Provides:       cygwin(gdi32.dll)
Provides:       cygwin(imm32.dll)
Provides:       cygwin(kernel32.dll)
Provides:       cygwin(ntdll.dll)
Provides:       cygwin(opengl32.dll)
Provides:       cygwin(ole32.dll)
Provides:       cygwin(shell32.dll)
Provides:       cygwin(user32.dll)
Provides:       cygwin(winmm.dll)
Provides:       cygwin(winspool.drv)

%description -n cygwin32-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora Cygwin packages.


%package -n cygwin64-filesystem
Summary:        Cygwin cross compiler base filesystem and environment for the x86_64 target
Requires:       %{name}-base = %{version}-%{release}

Provides:       %(sed "s/\(.*\)/cygwin64(\1) /g" %{SOURCE17} | tr "\n" " ")
Provides:       cygwin64(mscoree.dll)

%description -n cygwin64-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora Cygwin packages.


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING


%build
# nothing


%install
mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{_libexecdir}/cygwin-scripts

mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
for i in cygwin32-configure cygwin32-cmake cygwin32-make cygwin32-pkg-config \
         cygwin64-configure cygwin64-cmake cygwin64-make cygwin64-pkg-config ; do
  ln -s %{_libexecdir}/cygwin-scripts $i
done
popd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{macrosdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{macrosdir}/macros.cygwin
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{macrosdir}/macros.cygwin32
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{macrosdir}/macros.cygwin64

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint/

# Create the folders required for gcc and binutils
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/lib

# The Cygwin system root which will contain Cygwin native binaries
# and Cygwin-specific header files, pkgconfig, etc.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/etc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/sbin

mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/etc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/sbin

# We don't normally package manual pages and info files, except
# where those are not supplied by a Fedora native package.  So we
# need to create the directories.
#
# Note that some packages try to install stuff in
#   /usr/x86_64-pc-cygwin32/sys-root/man and
#   /usr/x86_64-pc-cygwin32/sys-root/doc
# but those are both packaging bugs.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/man/man{1,2,3,4,5,6,7,8,l,n}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/aclocal
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/themes
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/cmake
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-cygwin/sys-root/usr/share/xml

mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/man/man{1,2,3,4,5,6,7,8,l,n}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/aclocal
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/themes
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/cmake
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-cygwin/sys-root/usr/share/xml

# NB. NOT _libdir
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_rpmconfigdir}
install -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_rpmconfigdir}
install -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_rpmconfigdir}
install -m 0755 %{SOURCE13} $RPM_BUILD_ROOT%{_rpmconfigdir}

mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm/fileattrs
install -m 0644 %{SOURCE14} $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs/
install -m 0644 %{SOURCE15} $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/cygwin
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/cygwin/
install -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/cygwin/


%files base
%doc COPYING
%dir %{_sysconfdir}/rpmlint/
%config(noreplace) %{_sysconfdir}/rpmlint/cygwin-rpmlint.config
%{macrosdir}/macros.cygwin
%{_libexecdir}/cygwin-scripts
%{_rpmconfigdir}/cygwin*
%dir %{_datadir}/cygwin/

%files -n cygwin32-filesystem
%{macrosdir}/macros.cygwin32
%config(noreplace) %{_sysconfdir}/profile.d/cygwin32.sh
%{_bindir}/cygwin32-configure
%{_bindir}/cygwin32-cmake
%{_bindir}/cygwin32-make
%{_bindir}/cygwin32-pkg-config
%{_prefix}/i686-pc-cygwin
%{_rpmconfigdir}/fileattrs/cygwin32.attr
%{_datadir}/cygwin/toolchain-cygwin32.cmake

%files -n cygwin64-filesystem
%{macrosdir}/macros.cygwin64
%config(noreplace) %{_sysconfdir}/profile.d/cygwin64.sh
%{_bindir}/cygwin64-configure
%{_bindir}/cygwin64-cmake
%{_bindir}/cygwin64-make
%{_bindir}/cygwin64-pkg-config
%{_prefix}/x86_64-pc-cygwin
%{_rpmconfigdir}/fileattrs/cygwin64.attr
%{_datadir}/cygwin/toolchain-cygwin64.cmake


%changelog
* Wed Nov 15 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 14-1
- Remove deprecated macros
- Update config.{guess,sub} in %%cygwin_configure
- Update list of default Win32 DLLs
- Implement MiniDebugInfo for Cygwin binaries

* Thu Jun 11 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 13-1
- Rename Toolchain-cygwin{32,64}.cmake to toolchain-cygwin{32,64}.cmake
- Add CMAKE_SYSTEM_PROCESSOR to the CMake toolchain files
- Allow verbose CMake output to be disabled
- Don't use verbose output by default in the CMake wrapper scripts
- Prevent CFLAGS and CXXFLAGS from being set when using CMake wrappers
- Don't set LIB_INSTALL_DIR any more in the CMake macros as it breaks CPack
- Allow empty CYGWIN{32,64}_{C,CPP,CXX}FLAGS environment variables

* Thu Jun 11 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 12-1
- Add cppflags, ldflags variables

* Wed Jun 10 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 11-3
- Place the RPM macros in /usr/lib/rpm/macros.d when using a modern RPM

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 11-2
- Fix typo

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 11-1
- Add %%cygwin_autoreconf

* Sun Jun 30 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 10-1
- Fix %%cygwin_find_lang.

* Fri Jun 28 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 9-1
- Fix debuginfo package handling.

* Thu Jun 27 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 8-1
- Accept CYGWIN*_CONFIGURE_ARGS and CYGWIN*_CMAKE_ARGS.
- Use cygwin-pkg-config with CMake.

* Wed Jun 26 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 7-1
- Support both i686 and x86_64 with separate cygwin32- and cygwin64- prefixes.

* Thu Dec 01 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 6-1
- Define AUTOPOINT if cygwin-gettext is installed.
- Forcefully disable /usr/bin/foo-config detection.
- Define RPM and CMake macros to use new cygwin-qt-qmake scheme.

* Thu Jul 07 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 5-1
- Define LIBTOOLIZE if cygwin-libtool is installed.
- Set CMAKE_RC_COMPILER and CMAKE_LEGACY_CYGWIN_WIN32.

* Mon Apr 04 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 4-1
- Honour PKG_CONFIG_PATH in i686-pc-cygwin-pkg-config when run outside of RPM.
- Install _cygwin_datadir/aclocal.
- Add _cygwin_autoreconf macro.
- Provide more Windows DLLs.

* Mon Mar 14 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 3-1
- Added _cygwin_datadir/pkgconfig and _datadir/pkgconfig to PKG_CONFIG_LIBDIR.

* Thu Feb 17 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2-1
- Added dependency on redhat-rpm-config for brp-strip-static-archive which
  respects $STRIP.

* Wed Feb 16 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1-1
- Initial RPM release, largely based on mingw32-filesystem.
