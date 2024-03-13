# Note to packagers/builders:
#
# If you wish to build the LookAhead or Beta variant of this package, make sure
# that you are setting --with=rlbeta or --with=rllookahead on your mock
# command. See the README for more information.

%bcond_with rlbeta
%bcond_with rllookahead
%bcond_with rloverride

%define debug_package %{nil}

# Product information
%define product_family Rocky Linux
%define variant_titlecase Server
%define variant_lowercase server

# Distribution Name and Version
%define distro_name  Rocky Linux
%define distro       %{distro_name}
%define distro_code  Green Obsidian
%define major        8
%define minor        8
%define rocky_rel    5%{?rllh:.%{rllh}}%{!?rllh:.0}
%define upstream_rel %{major}.%{minor}-0.8
%define rpm_license  BSD-3-Clause
%define dist         .el%{major}
%define home_url     https://rockylinux.org/
%define bug_url      https://bugs.rockylinux.org/
%define debug_url    https://debuginfod.rockylinux.org/
%define dist_vendor  RESF

%define contentdir   pub/rocky
%define sigcontent   pub/sig
%define rlosid       rocky

%define os_bug_name  Rocky-Linux-%{major}

################################################################################
# Rocky LookAhead Section
#
# Reset defines for LookAhead variant. Default is stable if 0 or undefined.
%if %{with rllookahead}
%define minor        8
%define contentdir   pub/rocky-lh
%define rltype       -lookahead
%define rlstatement  LookAhead
%endif
# End Rocky LookAhead Section
################################################################################

################################################################################
# Rocky Beta Section
#
# Reset defines for Beta variant. Default is stable if 0 or undefined.
# We do NOT override the minor version number here.
%if %{with rlbeta}
%define contentdir   pub/rocky-beta
%define rltype       -beta
%define rlstatement  Beta
%endif
# End Rocky Beta Section
################################################################################

################################################################################
# Rocky Override Section
#
# Resets only the dist tag for the override package. All this does is ensure
# that only the rhel macros and settings are provided - This is useful in the
# case of a build that cannot be properly debranded (eg dotnet).
%if %{with rloverride}
%define dist         .el%{major}.override
%define rlosid       rhel
%endif
# End Rocky Override Section
################################################################################

%define base_release_version %{major}
%define dist_release_version %{major}
%define full_release_version %{major}.%{minor}

%ifarch ppc64le
%define tuned_profile :server
%endif

# Avoids a weird anaconda problem
%global __requires_exclude_from %{_libexecdir}

# conditional section for future use

Name:           ciq-lts88-rocky-release%{?rltype}
Version:        %{full_release_version}
Release:        %{rocky_rel}%{dist}
Summary:        %{distro_name} release files - CIQ LTS 8.8
Group:          System Environment/Base
License:        %{rpm_license}
URL:            https://rockylinux.org
BuildArch:      noarch

# What do we provide? Some of these needs are a necesity (think comps and
# groups) and things like EPEL need it.
Provides:       rocky-release = %{version}-%{release}
Provides:       rocky-release(upstream) = %{full_release_version}
Provides:       redhat-release = %{upstream_rel}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{major}
Provides:       centos-release = %{version}-%{release}
Provides:       centos-release(upstream) = %{full_release_version}

## Required by libdnf
Provides:       base-module(platform:el%{major})

## This makes lorax/pungi/anaconda happy
Provides:       rocky-release-eula  = %{version}-%{release}
Provides:       redhat-release-eula = %{upstream_rel}
Provides:       centos-release-eula = %{version}-%{release}


# We require both stock rocky-repos *and* ciq-rocky88-repos, both are fulfilled by the CIQ LTS-8.8 repos subpackage
Requires: ciq-rocky88-repos(%{major})
Requires: rocky-repos(%{major})

# CIQ LTS 8.8 packages should obsolete and conflict with the canonical rocky-release package
# Also it conflicts/replaces older CIQ LTS release packages
Provides: ciq-rocky88-repos(%{major}) = %{upstream_rel}
Obsoletes: rocky-release
Conflicts: rocky-release
Obsoletes: ciq-rocky86-repos
Conflicts: ciq-rocky86-repos

# GPG Keys (100-199)
Source101:      RPM-GPG-KEY-rockyofficial
Source102:      RPM-GPG-KEY-rockytesting

# Release Sources (200-499)
Source200:      EULA
Source201:      LICENSE
Source202:      Contributors
Source203:      COMMUNITY-CHARTER

# !! Stable !!
Source300:      85-display-manager.preset
Source301:      90-default.preset
Source302:      99-default-disable.preset

# Repo Sources
Source1200:     Rocky-BaseOS.repo
Source1201:     Rocky-AppStream.repo
Source1202:     Rocky-PowerTools.repo
Source1203:     Rocky-Extras.repo

# Rocky Add-ons
Source1210:     Rocky-HighAvailability.repo
Source1211:     Rocky-ResilientStorage.repo
Source1212:     Rocky-RT.repo
Source1213:     Rocky-NFV.repo

# Rocky Special Stuff
Source1220:     Rocky-Media.repo
Source1221:     Rocky-Debuginfo.repo
Source1222:     Rocky-Sources.repo
Source1223:     Rocky-Devel.repo
Source1226:     Rocky-Plus.repo
Source1300:     rocky.1.gz

# rocky secureboot certs placeholder (1400-1499)
Source1400:     rockydup1.x509
Source1401:     rockykpatch1.x509
Source1402:     rocky-root-ca.der
#
Source1403:     rocky-fwupd.cer
Source1404:     rocky-grub2.cer
Source1405:     rocky-kernel.cer
Source1406:     rocky-shim.cer

%description
%{distro_name} release files.  Designed to enable CIQ LTS 8.8 support

# CIQ 8.8 specific: We conflict with the original rocky-repos, we want to force the 8.8 vault to be used
%package     -n ciq-rocky88-repos%{?rltype}
Provides: ciq-rocky88-repos(%{major}) = %{upstream_rel}
Conflicts: rocky-repos
Obsoletes: rocky-repos

# We also obsolete ciq-rocky-repos if a user has that installed. There can be only 1 -repos package:
Conflicts: ciq-rocky-repos
Obsoletes: ciq-rocky-repos
Conflicts: ciq-rocky86-repos
Obsoletes: ciq-rocky86-repos

Summary:        %{distro_name} Package Repositories
License:        %{rpm_license}
Provides:       system-repos = %{version}-%{release}
Provides:       rocky-repos(%{major}) = %{full_release_version}
Requires:       system-release = %{version}-%{release}
Requires:       rocky-gpg-keys%{?rltype}
Conflicts:      %{name} < 8.0

%description -n ciq-rocky88-repos%{?rltype}
%{distro_name} package repository files for yum/dnf  - CIQ LTS 8.8

%package     -n rocky-gpg-keys%{?rltype}
Summary:        Rocky RPM GPG Keys
Conflicts:      %{name} < 8.0

%description -n rocky-gpg-keys%{?rltype}
This package provides the RPM signature keys for Rocky.

%package     -n rocky-sb-certs%{?rltype}
Summary:        %{distro_name} public secureboot certificates
Group:          System Environment/Base
Provides:       system-sb-certs = %{version}-%{release}

%description -n rocky-sb-certs%{?rltype}
This package contains the %{distro_name} secureboot public certificates.

%prep
%if %{with rllookahead} && %{with rlbeta}
echo "!! WARNING !!"
echo "Both LookAhead and Beta were enabled. This is not supported."
echo "As a result: BUILD FAILED."
exit 1
%endif
echo Good.

%build
echo Good.

%install
# copy license and contributors doc here for %%license and %%doc macros
cp %{SOURCE201} %{SOURCE202} %{SOURCE203} .

################################################################################
# system-release data
install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro_name} release %{full_release_version}%{?rlstatement: %{rlstatement}} (%{distro_code})" > %{buildroot}%{_sysconfdir}/rocky-release
echo "Derived from Red Hat Enterprise Linux %{full_release_version}" > %{buildroot}%{_sysconfdir}/rocky-release-upstream
ln -s rocky-release %{buildroot}%{_sysconfdir}/system-release
ln -s rocky-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s rocky-release %{buildroot}%{_sysconfdir}/centos-release
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE1300} %{buildroot}%{_mandir}/man1/

# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{distro_name}"
VERSION="%{full_release_version} (%{distro_code})"
ID="%{rlosid}"
ID_LIKE="rhel centos fedora"
VERSION_ID="%{full_release_version}"
PLATFORM_ID="platform:el%{major}"
PRETTY_NAME="%{distro_name} %{full_release_version}%{?rlstatement: %{rlstatement}} (%{distro_code})"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:%{major}:GA"
HOME_URL="%{home_url}"
BUG_REPORT_URL="%{bug_url}"
SUPPORT_END="2029-05-31"
ROCKY_SUPPORT_PRODUCT="%{os_bug_name}"
ROCKY_SUPPORT_PRODUCT_VERSION="%{full_release_version}%{?rlstatement:-%{rlstatement}}"
REDHAT_SUPPORT_PRODUCT="%{distro_name}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{full_release_version}%{?rlstatement: %{rlstatement}}"
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:rocky:rocky:%{major}:GA" > %{buildroot}%{_sysconfdir}/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}%{_sysconfdir}/issue
echo 'Kernel \r on an \m' >> %{buildroot}%{_sysconfdir}/issue
cp %{buildroot}%{_sysconfdir}/issue{,.net}
echo >> %{buildroot}%{_sysconfdir}/issue

# set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%rocky_ver %{major}
%%rocky %{major}
%%centos_ver %{major}
%%centos %{major}
%%rhel %{major}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%{major}%%{?distsuffix}%%{?with_bootstrap:%{__bootstrap}}
%%el%{major} 1

%%dist_vendor         %{dist_vendor}
%%dist_name           %{distro}
%%dist_home_url       %{home_url}
%%dist_bug_report_url %{bug_url}
%%dist_debuginfod_url %{debug_url}
EOF

# Data directory
install -d -m 0755 %{buildroot}%{_datadir}/rocky-release
ln -s rocky-release %{buildroot}%{_datadir}/redhat-release
install -p -m 0644 %{SOURCE200} %{buildroot}%{_datadir}/rocky-release/

# end system-release data
################################################################################

################################################################################
# systemd section
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE300} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE301} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE302} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
# systemd section
################################################################################

################################################################################
# start secureboot section
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/sb-certs/
install -d -m 0755 %{buildroot}%{_datadir}/pki/sb-certs/

# Backported certs for now
install -m 0644 %{SOURCE1400} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1401} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1402} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1403} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1404} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1405} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1406} %{buildroot}%{_datadir}/pki/sb-certs/

# Placeholders
# x86_64
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-x86_64.cer

# aarch64
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-aarch64.cer

# ppc64le
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-ppc64le.cer

# armhfp
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-armhfp.cer

# symlinks for everybody
for x in $(ls %{buildroot}%{_datadir}/pki/sb-certs); do
  ln -sr %{buildroot}%{_datadir}/pki/sb-certs/${x} %{buildroot}%{_sysconfdir}/pki/sb-certs/${x}
done

# end secureboot section
################################################################################

################################################################################
# dnf repo section
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE1200} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1201} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1202} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1203} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1210} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1211} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1212} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1213} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1220} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1221} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1222} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1223} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1226} %{buildroot}%{_sysconfdir}/yum.repos.d/

# dnf stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/vars
echo "%{contentdir}" > %{buildroot}%{_sysconfdir}/dnf/vars/contentdir
echo "%{sigcontent}" > %{buildroot}%{_sysconfdir}/dnf/vars/sigcontentdir
echo "%{?rltype}" > %{buildroot}%{_sysconfdir}/dnf/vars/rltype
echo "%{major}-stream" > %{buildroot}%{_sysconfdir}/dnf/vars/stream

# Copy out GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
install -p -m 0644 %{SOURCE102} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
# end dnf repo section
################################################################################

%files
%license LICENSE
%doc Contributors COMMUNITY-CHARTER
%{_sysconfdir}/redhat-release
%{_sysconfdir}/centos-release
%{_sysconfdir}/system-release
%{_sysconfdir}/rocky-release
%{_sysconfdir}/rocky-release-upstream
%config(noreplace) %{_sysconfdir}/os-release
%config %{_sysconfdir}/system-release-cpe
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%{_rpmmacrodir}/macros.dist
%{_datadir}/redhat-release
%{_datadir}/rocky-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%{_mandir}/man1/rocky.1.gz

%files -n ciq-rocky88-repos%{?rltype}
%license LICENSE
%config(noreplace) %{_sysconfdir}/yum.repos.d/Rocky-*.repo
%config(noreplace) %{_sysconfdir}/dnf/vars/contentdir
%config(noreplace) %{_sysconfdir}/dnf/vars/sigcontentdir
%config(noreplace) %{_sysconfdir}/dnf/vars/rltype
%config(noreplace) %{_sysconfdir}/dnf/vars/stream

%files -n rocky-gpg-keys%{?rltype}
%{_sysconfdir}/pki/rpm-gpg/

%files -n rocky-sb-certs%{?rltype}
# care: resetting symlinks is intended
%dir %{_sysconfdir}/pki/sb-certs
%dir %{_datadir}/pki/sb-certs
%{_sysconfdir}/pki/sb-certs/*
%{_datadir}/pki/sb-certs/*

%changelog
* Tue Dec 05 2023 Matt Hink <mhink@ciq.com> - 8.8-5.0
- Fix missing section

* Tue Dec 05 2023 Matt Hink <mhink@ciq.com> - 8.8-4.0
- Add Provides: ciq-rocky88-repos(%{major}) = %{upstream_rel}

* Sun Dec 03 2023 Skip Grube <sgrube@ciq.com> - 8.8-3.0
- Forked and adapted to support CIQ LTS 8.8.  Repos point to vault

* Sat Jun 10 2023 Louis Abel <label@rockylinux.org> - 8.8-1.8
- Define the distro macro

* Tue Apr 25 2023 Louis Abel <label@rockylinux.org> - 8.8-1.7
- Update secure boot certificates

* Tue Apr 04 2023 Louis Abel <label@rockylinux.org> - 8.8-1.6
- Set redhat-release to match current upstream

* Fri Mar 17 2023 Louis Abel <label@rockylinux.org> - 8.8-1.5
- Backport rocky-sb-certs to Rocky Linux 8

* Wed Jan 01 2023 Louis Abel <label@rockylinux.org> - 8.8-1.3
- Move macros to a proper location

* Thu Dec 22 2022 Louis Abel <label@rockylinux.org> - 8.8-1.2
- Add SUPPORT_END to absolute EOL

* Tue Oct 18 2022 Louis Abel <label@rockylinux.org> - 8.8-1.1
- Bump to 8.8 for lookahead development

* Wed Sep 07 2022 Louis Abel <label@rockylinux.org> - 8.7-1.1
- Branch off and make system-release version use X.Y-A.B
  format in attempt to match upstream.
- Add stream dnf var

* Fri May 20 2022 Louis Abel <label@rockylinux.org> - 8.6-3
- Add pub/sig var for dnf

* Tue Mar 29 2022 Louis Abel <label@rockylinux.org> - 8.6-2
- 8.6 prepatory release
- Add REDHAT_SUPPORT_PRODUCT to /etc/os-release

* Mon Feb 14 2022 Louis Abel <label@rockylinux.org> - 8.5-4
- Add bootstrap to macros to match EL9

* Tue Dec 21 2021 Louis Abel <label@rockylinux.org> - 8.5-3
- Add countme=1 to base repositories

* Sat Dec 11 2021 Louis Abel <label@rockylinux.org> - 8.5-2
- Fix CPE to match upstreamed Rocky data

* Tue Oct 05 2021 Louis Abel <label@rockylinux.org> - 8.5-1
- 8.5 prepatory release

* Mon Sep 13 2021 Louis Abel <label@rockylinux.org> - 8.4-35
- Add missing CentOS provides and symlinks
- Add centos macros for some builds to complete successfully without relying
  on random patching

* Thu Sep 09 2021 Louis Abel <label@rockylinux.org> - 8.4-33
- Add centos as an id_like to allow current and future SIGs that rely on CentOS
  to work properly.

* Wed Jul 07 2021 Louis Abel <label@rockylinux.org> - 8.4-32
- Fix URLs for Plus and NFV
- Use a macro for the license across sub packages
- Fix bogus date in changelog

* Mon Jul 05 2021 Louis Abel <label@rockylinux.org> - 8.4-30
- Fix URLs for debuginfo

* Tue Jun 29 2021 Louis Abel <label@rockylinux.org> - 8.4-29
- Fix URLs
- Added debuginfo
- Added NFV (future state)

* Wed Jun 16 2021 Louis Abel <label@rockylinux.org> - 8.4-25
- Fix up outstanding issues

* Sat Jun 05 2021 Louis Abel <label@rockylinux.org> - 8.4-24
- Change all mirrorlist urls to https

* Tue May 25 2021 Louis Abel <label@rockylinux.org> - 8.4-23
- Add a version codename to satisfy vendors
- Change license
- Fix up /etc/os-release and CPE
- Remove unused infra var
- Change base_release_version to major

* Wed May 19 2021 Louis Abel <label@rockylinux.org> - 8.4-16
- Remove annoying /etc/issue banner

* Sat May 08 2021 Louis Abel <label@rockylinux.org> - 8.4-15
- Release for 8.4

* Wed May 05 2021 Louis Abel <label@rockylinux.org> - 8.3-14
- Add RT, Plus, and NFV repo files

* Mon May 03 2021 Louis Abel <label@rockylinux.org> - 8.3-13
- Add minor version to /etc/os-release to resolve issues
  with products that provide the "full version"

* Sat May 01 2021 Louis Abel <label@rockylinux.org> - 8.3-12
- Add resilient storage varient
- Fix vars

* Wed Apr 28 2021 Louis Abel <label@rockylinux.org> - 8.3-11
- Fix repo URL's where needed
- Change contentdir var

* Sun Apr 25 2021 Louis Abel <label@rockylinux.org> - 8.3-9
- Remove and add os-release references

* Sun Apr 18 2021 Louis Abel <label@rockylinux.org> - 8.3-8
- Emphasize that this is not a production ready release
- rpmlint

* Wed Apr 14 2021 Louis Abel <label@rockylinux.org> - 8.3-7
- Fix mantis links

* Thu Apr 08 2021 Louis Abel <label@rockylinux.org> - 8.3-5
- Combine release, repos, and keys together to simplify

* Mon Feb 01 2021 Louis Abel <label@rockylinux.org> - 8.3-4
- Initial Rocky Release 8.3 based on CentOS 8.3
- Keep centos rpm macro to reduce package modification burden
- Update /etc/issue
