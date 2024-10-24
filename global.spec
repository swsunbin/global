%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%bcond_with xemacs
%else
%bcond_without xemacs
%endif

Name:           global
Version:        6.5.6
Release:        4%{?dist}
Summary:        Source code tag system
Group:          Development/Tools
# The entire source code is GPLv3+ except
#   libglibc/ which is LGPLv2+
#   gtags-cscope/ which is BSD
#   libparser/ which is GPLv2+
#   jquery/ which is MIT
License:        GPLv3+ and LGPLv2+ and BSD and GPLv2+ and MIT
URL:            http://www.gnu.org/software/global
Source:         ftp://ftp.gnu.org/pub/gnu/global/global-%{version}.tar.gz
BuildRequires:  ncurses-devel, ctags-etags
BuildRequires:  libtool-ltdl-devel
%if 0%{?rhel} == 7
BuildRequires:  python%{python3_pkgversion}-devel
%else
BuildRequires:  python3-devel
%endif
BuildRequires:  emacs
%if %{with xemacs}
BuildRequires:  xemacs
Requires:       xemacs-filesystem >= %{_xemacs_version}
%endif
Requires:       emacs-filesystem >= %{_emacs_version}
Obsoletes:      emacs-global <= 6.5.1-1
Obsoletes:      emacs-global-el <= 6.5.1-1
Provides:       emacs-global = %{version}-%{release}
Provides:       emacs-global-el = %{version}-%{release}
Patch1:         global-string_validation.patch

%description
GNU GLOBAL is a source code tag system that works the same way across
diverse environments. It supports C, C++, Yacc, Java, PHP and
assembler source code.

%package        ctags
Summary:        Integration of Exuberant Ctags and Pygments with GLOBAL
License:        GPLv3+
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}, ctags-etags
%if 0%{?rhel} == 7
Requires:       python%{python3_pkgversion}-pygments
%else
Requires:       python3-pygments
%endif

%description    ctags
This package contains plug-ins that provides support for more languages
through Pygments and Exuberant Ctags.

%prep
%setup -q
%patch1 -p1 -b .gozilla

%build
export PYTHON=%{__python3}
%configure --with-posix-sort=/bin/sort --with-exuberant-ctags=/bin/ctags --localstatedir=/var/tmp/  --without-included-ltdl
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove empty useless directory
rm -f %{buildroot}%{_infodir}/dir

rm -f %{buildroot}%{_libdir}/gtags/*.*a
rm -f %{buildroot}%{_libdir}/gtags/user-custom.*

rm %{buildroot}/%{_datadir}/gtags/{gtags.el,gtags.conf}
rm %{buildroot}/%{_datadir}/gtags/{AUTHORS,COPYING,ChangeLog,DONORS,FAQ,INSTALL,LICENSE,NEWS,README,THANKS}

# fix rpmlint error
chmod +x %{buildroot}/%{_datadir}/gtags/{global,completion}.cgi

mkdir -p %{buildroot}%{_sysconfdir}
install gtags.conf -t %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_emacs_sitelispdir}
install gtags.el -p -t %{buildroot}%{_emacs_sitelispdir}
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/gtags.el
chmod -x %{buildroot}%{_emacs_sitelispdir}/gtags.el
%if %{with xemacs}
mkdir -p %{buildroot}%{_xemacs_sitelispdir}
install gtags.el -p -t %{buildroot}%{_xemacs_sitelispdir}
%{_xemacs_bytecompile} %{buildroot}%{_xemacs_sitelispdir}/gtags.el
chmod -x %{buildroot}%{_xemacs_sitelispdir}/gtags.el
%endif

## Remove executable flag
chmod -x %{buildroot}/%{_sysconfdir}/gtags.conf

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%files
%doc README THANKS AUTHORS FAQ NEWS
%doc DONORS ChangeLog
%license LICENSE COPYING
%config(noreplace) %{_sysconfdir}/gtags.conf
%{_bindir}/*
%{_infodir}/global.info*
%{_mandir}/man*/*
%{_datadir}/gtags
%{_emacs_sitelispdir}/gtags.el*
%if %{with xemacs}
%{_xemacs_sitelispdir}/gtags.el*
%endif


%files ctags
%dir %{_libdir}/gtags
%{_libdir}/gtags/*

%changelog
* Thu Mar 07 2019 Troy Dawson <tdawson@redhat.com> - 6.5.6-4
- Rebuilt to change main python from 3.4 to 3.6

* Fri Dec 22 2017 Pavel Zhukov <pzhukov@redhat.com> - 6.5.6-3
- fix command injection in gozilla (#1528416)

* Fri May 19 2017 Matěj Cepl <mcepl@redhat.com> - 6.5.6-2
- Add epel7 build (#1451800)

* Wed Mar  1 2017 Robin Lee <cheeselee@fedoraproject.org> - 6.5.6-1
- Update to 6.5.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 6.5.2-2
- Rebuild for Python 3.6

* Fri Mar 11 2016 Robin Lee <cheeselee@fedoraproject.org> - 6.5.2-1
- Update to 6.5.2
- Explicitly use Python3
- Use system ltdl

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Robin Lee <cheeselee@fedoraproject.org> - 6.5.1-1
- Update 6.5.1
- Dropped global-6.3.3-format-security.patch
- Fix plug-ins' paths (BZ#1268763)
- Dropped emacs subpackages (BZ#1234559)
- Include elisp addon also for XEmacs
- Fix some rpmlint errors
- Revised summary and description for ctags subpackage
- Revised license tags and use %%license to install LICENSE and COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 26 2014  Pavel Zhukov <landgraf@fedoraproject.org> - 6.3.3-1
- New version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 6.2.12-3
- Fix FTBFS with -Werror=format-security (#1106647)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 6.2.12-1
- New release 

* Wed Oct 30 2013 Sjoerd Mullender <sjoerd@acm.org> - 6.2.9-4
- Install exuberant-ctags.so (#801562).

* Tue Oct 08 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 6.2.9-3
- Remove deprecated defattr
- Cosmetic changes after review

* Mon Oct 07 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 6.2.9-1
- Unorphan package
- New release 6.2.9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Karel Klic <kklic@redhat.com> - 5.9.3-2
- Added --with-posix-sort=/bin/sort to %%configure to speed up
  indexing.

* Wed Dec  8 2010 Karel Klic <kklic@redhat.com> - 5.9.3-1
- Newest upstream release.

* Wed Dec  8 2010 Karel Klic <kklic@redhat.com> - 5.7.5-2
- Build gtags.elc and package it in the new emacs-global package.
- Package gtags.el in the new emacs-global-el package.
- Removed docs from /usr/share/gtags.
- Added more docs to %%doc.
- Install default gtags.conf into /etc.
- Removed deprecated %%clean section.
- Removed unused BuildRoot tag.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Gerard Milmeister <gemi@bluewin.ch> - 5.7.5-1
- new release 5.7.5

* Fri Nov 21 2008 Gerard Milmeister <gemi@bluewin.ch> - 5.7.3-1
- new release 5.7.3

* Sun Oct 19 2008 Gerard Milmeister <gemi@bluewin.ch> - 5.7.2-1
- new release 5.7.2

* Sat Aug  2 2008 Gerard Milmeister <gemi@bluewin.ch> - 5.7.1-1
- new release 5.7.1

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.4-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.4-2
- Autorebuild for GCC 4.3

* Sat Feb 24 2007 Gerard Milmeister <gemi@bluewin.ch> - 5.4-1
- new version 5.4

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.3-1
- new version 5.3

* Wed Aug 30 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.2-1
- new version 5.2

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.0-2
- Rebuild for FE6

* Sun Apr 30 2006 Gerard Milmeister <gemi@bluewin.ch> - 5.0-1
- new version 5.0

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 4.8.7-3
- Rebuild for Fedora Extras 5

* Wed Oct  5 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.8.7-2
- Remove dir in /usr/share/info

* Sat Oct  1 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.8.7-1
- New Version 4.8.7

* Tue Jul  5 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.8.6-1
- New Version 4.8.6

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 4.8.4-4
- fix build with gcc4 (#156212)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 4.8.4-3
- rebuild on all arches

* Thu Apr 07 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Mar  7 2005 Gerard Milmeister <gemi@bluewin.ch> - 4.8.4-1
- New Version 4.8.4

* Mon Dec 27 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:4.8.2-0.fdr.1
- New Version 4.8.2

* Sat Oct 23 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:4.8.1-0.fdr.1
- New Version 4.8.1

* Sat Jul 17 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:4.7.2-0.fdr.1
- New Version 4.7.2

* Fri Mar 19 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:4.7-0.fdr.1
- New Version 4.7

* Thu Nov 27 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:4.6.1-0.fdr.1
- First Fedora release

