# NOTE: This library has been deprecated in RHEL and Fedora for some
# time now.  While we have removed the word "deprecated" from the package
# name in modular X, the library does remain deprecated and will be
# removed from a future OS release at some point.  Developers should
# refrain from using this library in new software, and should migrate
# software which currently uses libXp to another printing interface such
# as gnome-print.  We may decide to stop shipping the development headers
# prior to removing libXp from the OS, which is what "without_devel"
# is for.  
%define without_devel  0

Summary: X.Org X11 libXp runtime library
Name: libXp
Version: 1.0.0
Release: 15.1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXau-devel
BuildRequires: libtool automake autoconf gettext

Patch0: add-proto-files.patch

%description
X.Org X11 libXp runtime library

%if ! %{without_devel}
%package devel
Summary: X.Org X11 libXp development package
Group: Development/Libraries
Requires: libXau-devel pkgconfig
Requires: %{name} = %{version}-%{release}

# needed by xp.pc
BuildRequires: xorg-x11-proto-devel

%description devel
X.Org X11 libXp development package
%endif

%prep
%setup -q

%patch0 -p1 -b .add-proto-files

%build
CPPFLAGS="$CPPFLAGS -I$RPM_BUILD_ROOT%{_includedir}"
export CPPFLAGS

autoreconf -v --install

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if %{without_devel}
{
   rm -f $RPM_BUILD_ROOT%{_libdir}/libXp.a
   rm -f $RPM_BUILD_ROOT%{_libdir}/libXp.so
   rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
   rm -rf $RPM_BUILD_ROOT%{_mandir}
}
%endif

# Don't encourage people to use the deprecated Xprint APIs.
rm -rf $RPM_BUILD_ROOT%{_mandir}

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL ChangeLog
%{_libdir}/libXp.so.6
%{_libdir}/libXp.so.6.2.0

%if ! %{without_devel}
%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Print.h
%{_includedir}/X11/extensions/Printstr.h
%{_libdir}/pkgconfig/printproto.pc
# FIXME: Should we remove the shared lib during deprecation, so that things
# that keep linking to libXp, will always get the static lib and not break
# when we eventually drop libXp?
%{_libdir}/libXp.so
%{_libdir}/pkgconfig/xp.pc
#%dir %{_mandir}/man3x
#%{_mandir}/man3/*.3x*
%endif

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.0.0-15.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.0-14
- Un-require xorg-x11-filesystem

* Thu Feb 26 2009 Adam Jackson <ajax@redhat.com> 1.0.0-13
- Rebuild for new libtool.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-11
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 1.0.0-10
- Merge-Review #226082
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed xorg-x11-deprecated-libs xorg-x11-deprecated-libs-devel as Obsoletes

* Mon Jan 14 2008 parag <paragn@fedoraproject.org> - 1.0.0-9
- Merge-Review #226082
- Removed BR:pkgconfig
- Removed zero-length README file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.0-8
- Rebuild for build id

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-8
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0.7
- Add requires for the devel package on libXau-devel (173530)

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- Add the proto files directly instead of attempting to build a separate
  tarball. Also remove last traces of printproto-1.0.3.tar.gz

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com>
- Remove printproto source. 

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- BuildRequire autoconf automake libtool gettext

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- Run autoreconf to make sure changes to configure.ac take effect

* Fri Aug 18 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-6
- Add patch to not check for printproto.pc. (Since it's part of this
  package now, it isn't installed at the time libXp is configured).

* Thu Aug 17 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.0-5
- Moved Print.h, Printstr.h and printproto.pc into the devel package here
  (they used to be in xorg-x11-proto-devel). 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Mon Jul 10 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-4
- Renamed libXp_deprecated rpm macro to "with_devel" to avoid confusion.  This
  library is still deprecated, we just decided to remove the word "deprecated"
  from the package name for library naming consistency.

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Replace "makeinstall" with "make install DESTDIR=..."
- Added "Requires: xorg-x11-proto-devel" to devel for xp.pc
- Remove package ownership of mandir/libdir/etc.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXp to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXp to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-3
- Added "Obsoletes: xorg-x11-deprecated-libs" to runtime package, and
  "Obsoletes: xorg-x11-deprecated-libs-devel" to devel package.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXp to version 0.99.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
