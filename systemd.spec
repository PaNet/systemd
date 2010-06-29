%global git_date    20100629
%global git_version 4176e5

Name:           systemd
Url:            http://www.freedesktop.org/wiki/Software/systemd
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Version:        0
Release:        0.7.%{git_date}git%{git_version}%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Summary:        A System and Session Manager
BuildRequires:  libudev-devel
BuildRequires:  libcap-devel
BuildRequires:  libcgroup-devel
BuildRequires:  tcp_wrappers-devel
BuildRequires:  pam-devel
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  dbus-glib-devel
BuildRequires:  vala
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
Requires:	systemd-units = %{version}-%{release}
Requires:       dbus
Requires:       udev
Requires:       pkgconfig
Requires:       initscripts
Requires:       selinux-policy >= 3.8.5

# git clone git://anongit.freedesktop.org/systemd
# cd systemd;
# git archive --format=tar --prefix=systemd/ {git_version} | xz  > systemd-{version}.{git_date}git{git_version}.tar.xz

Source0:        %{name}-%{version}.%{git_date}git%{git_version}.tar.xz
#Source0:       http://www.freedesktop.org/FIXME/%{name}-%{version}.tar.bz2

%description
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package units
Group:          System Environment/Base
Summary:        Configuration files, directories and installation tool for systemd

%description units
Basic configuration files, directories and installation tool for the systemd
system and session manager.

%package gtk
Group:          System Environment/Base
Summary:        Graphical frontend for systemd
Requires:       %{name} = %{version}-%{release}

%description gtk
Graphical front-end for systemd.

%package sysvinit
Group:          System Environment/Base
Summary:        systemd System V init tools
Requires:       %{name} = %{version}-%{release}
Obsoletes:      SysVinit < 2.86-24, sysvinit < 2.86-24
Provides:       SysVinit = 2.86-24, sysvinit = 2.86-24
#Obsoletes:      upstart <= 0.6.99
Conflicts:      upstart

%description sysvinit
Drop-in replacement for the System V init tools of systemd.

%prep
%setup -q -n %{name}
./bootstrap.sh ac

%build
%configure --with-rootdir= --with-distro=fedora
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -exec rm {} \;
mkdir -p %{buildroot}/sbin
ln -s /bin/systemd %{buildroot}/sbin/init
ln -s /bin/systemctl %{buildroot}/sbin/reboot
ln -s /bin/systemctl %{buildroot}/sbin/halt
ln -s /bin/systemctl %{buildroot}/sbin/poweroff
ln -s /bin/systemctl %{buildroot}/sbin/shutdown
ln -s /bin/systemctl %{buildroot}/sbin/telinit
ln -s /bin/systemctl %{buildroot}/sbin/runlevel
rmdir %{buildroot}/cgroup

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_sysconfdir}/rc.d/init.d/reboot
/bin/systemd
/bin/systemctl
/bin/systemd-notify
/lib/systemd/systemd-*
/lib/udev/rules.d/*.rules
/%{_lib}/security/pam_systemd.so
%{_mandir}/man1/systemd.*
%{_mandir}/man1/systemctl.*
%{_mandir}/man1/systemd-notify.*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/pam_systemd.*
%{_datadir}/systemd
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/pkgconfig/systemd.pc
%{_docdir}/systemd

%files units
%defattr(-,root,root,-)
%{_sysconfdir}/systemd
%{_sysconfdir}/xdg/systemd
%dir /lib/systemd
/lib/systemd/system
%{_bindir}/systemd-install
%{_mandir}/man1/systemd-install.*

%files gtk
%defattr(-,root,root,-)
%{_bindir}/systemadm
%{_mandir}/man1/systemadm.*

%files sysvinit
%defattr(-,root,root,-)
/sbin/init
/sbin/reboot
/sbin/halt
/sbin/poweroff
/sbin/shutdown
/sbin/telinit
/sbin/runlevel
%{_mandir}/man1/init.*
%{_mandir}/man8/halt.*
%{_mandir}/man8/reboot.*
%{_mandir}/man8/shutdown.*
%{_mandir}/man8/poweroff.*
%{_mandir}/man8/telinit.*
%{_mandir}/man8/runlevel.*

%changelog
* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.7.20100622gita3723b
- New snapshot
- Split off -units package where other packages can depend on without pulling in the whole of systemd

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.6.20100622gita3723b
- Add missing libtool dependency.

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.5.20100622gita3723b
- Update snapshot

* Mon Jun 14 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.4.20100614git393024
- Pull the latest snapshot that fixes a segfault. Resolves rhbz#603231

* Thu Jun 11 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.3.20100610git2f198e
- More minor fixes as per review

* Thu Jun 10 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.2.20100610git2f198e
- Spec improvements from David Hollis

* Wed Jun 09 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.1.20090609git2f198e
- Address review comments

* Tue Jun 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.0.git2010-06-02
- Initial spec (adopted from Kay Sievers)