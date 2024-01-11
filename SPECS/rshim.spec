# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2019 Mellanox Technologies. All Rights Reserved.
#

Name: rshim
Version: 2.0.8
Release: 1%{?dist}
Summary: User-space driver for Mellanox BlueField SoC

License: GPLv2

URL: https://github.com/mellanox/rshim-user-space
Source0: https://github.com/Mellanox/rshim-user-space/archive/refs/tags/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: rshim-sysconfig.patch

BuildRequires: gcc, autoconf, automake, make
BuildRequires: pkgconfig(libpci), pkgconfig(libusb-1.0), pkgconfig(fuse)
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

Requires: kmod(cuse.ko)
Suggests: kernel-modules-extra

%description
This is the user-space driver to access the BlueField SoC via the rshim
interface. It provides ways to push boot stream, debug the target or login
via the virtual console or network interface.

%prep
%autosetup -p1 -n rshim-user-space-%{name}-%{version}

%build
./bootstrap.sh
%configure
%make_build

%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rshim <<EOF
# Command-line options for rshim
OPTIONS=""
EOF

%post
%systemd_post rshim.service

%preun
%systemd_preun rshim.service

%postun
%systemd_postun_with_restart rshim.service

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/rshim.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rshim
%{_sbindir}/rshim
%{_sbindir}/bfb-install
%{_unitdir}/rshim.service
%{_mandir}/man8/rshim.8.gz
%{_mandir}/man8/bfb-install.8.gz

%changelog
* Tue May 23 2023 Dean Nelson <dnelson@redhat.com> - 2.0.8-1
- Update user-space rshim driver source to version 2.0.8
- Modify rshim.spec accordingly
- Resolves: rhbz#2196852

* Tue Apr 20 2021 Dean Nelson <dnelson@redhat.com> - 2.0.5-2
- Add sysconfig/rshim file and update rshim.service to source it.
- jbastian made the first cut of this patch, which needed to be
  modified due to the update to 2.0.5. And I chose to go with
  %%autosetup to handle Patch0, instead of sticking with %%setup.
- Resolves: rhbz#1946349

* Tue Apr 20 2021 Dean Nelson <dnelson@redhat.com> - 2.0.5-1
- Update user-space rshim driver source to version 2.0.5.
- Modify rshim.spec accordingly.
- Resolves: rhbz#1950425

* Tue Jan 26 2021 Dean Nelson <dnelson@redhat.com> - 2.0.4-4
- Expose gating.yaml file in order to enable manual CI gating for rshim
  in RHEL-8.4, by bumping release and doing a Brew build.
- Partially resolves: rhbz#1912248

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Apr 21 2020 Liming Sun <lsun@mellanox.com> - 2.0.4-1
- Update .spec file according to review comments
- Fix the 'KillMode' in rshim.service
- Support process termination by SIGTERM
- Fix some compiling warnings and configure issue for FreeBSD
- Fix a read()/write() issue in rshim_pcie.c caused by optimization

* Tue Apr 14 2020 Liming Sun <lsun@mellanox.com> - 2.0.3-1
- Enable pci device during probing
- Map the pci resource0 file instead of /dev/mem
- Add copyright header in bootstrap.sh
- Add 'Requires' tag check in the rpm .spec for kernel-modules-extra
- Fix the 'rshim --version' output

* Thu Apr 09 2020 Liming Sun <lsun@mellanox.com> - 2.0.2-1
- Remove unnecessary dependency in .spec and use make_build
- Add package build for debian/ubuntu
- Fix some format in the man page
- Add check for syslog headers

* Mon Mar 23 2020 Liming Sun <lsun@mellanox.com> - 2.0.1-1
- Rename bfrshim to rshim
- Remove rshim.spec since it's auto-generated from rshim.spec.in
- Fix warnings reported by coverity
- Add rhel/rshim.spec.in for fedora
- Move rshim to sbin and move man page to man8

* Fri Mar 13 2020 Liming Sun <lsun@mellanox.com> - 2.0-1
- Update the spec file according to fedora packaging-guidelines

* Mon Dec 16 2019 Liming Sun <lsun@mellanox.com>
- Initial packaging
