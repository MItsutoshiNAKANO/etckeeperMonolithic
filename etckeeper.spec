# vim: set sw=4 ts=4 et nu:

# Copyright (c) 2014 Pascal Bleser <pascal.bleser@opensuse.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:               etckeeper
Version:            1.12
Release:            0
Summary:            Store /etc under Version Control
Source:             http://ftp.debian.org/debian/pool/main/e/etckeeper/etckeeper_%{version}.tar.gz
Source99:           etckeeper.rpmlintrc
# PATCH-FIX-UPSTREAM etckeeper-zypp.patch bnc#884154 bkbin005@rinku.zaq.ne.jp -- fix for ZYpp
Patch0:             etckeeper-zypp.patch
URL:                http://joeyh.name/code/etckeeper/
Group:              System/Management
License:            GPL-2.0+
BuildRoot:          %{_tmppath}/build-%{name}-%{version}
BuildRequires:      make
Requires:           git
%if 0%{?suse_version}
BuildRequires:      libzypp
Requires:           zypp-plugin-python
%define HPM zypper
%define LPM rpm
%else
BuildRequires:      yum
%define HPM yum
%define LPM rpm
%endif
Requires:           cron
BuildArch:          noarch

%description
The etckeeper program is a tool to let /etc be stored in a git,
mercurial, bzr or darcs repository. It hooks into yum to automatically
commit changes made to /etc during package upgrades. It tracks file
metadata that version control systems do not normally support, but that
is important for /etc, such as the permissions of /etc/shadow. It's
quite modular and configurable, while also being simple to use if you
understand the basics of working with version control.

%prep
%setup -q -n "%{name}"
%patch0 -p1

%__perl -pi -e '
s|^(\s*)(HIGHLEVEL_PACKAGE_MANAGER)=.+|$1$2=%{HPM}|;
s|^(\s*)(LOWLEVEL_PACKAGE_MANAGER)=.+|$1$2=%{LPM}|;
s|^(\s*)(VCS)=.+|$1$2=git|;
' ./etckeeper.conf

%build
make %{?_smp_mflags}

%install

make \
    DESTDIR="%{buildroot}" \
    PYTHON_INSTALL_OPTS="--prefix=%{_prefix} --root=%{buildroot}" \
    install

# who cares about bzr...
rm -rf "%{buildroot}%{_prefix}/lib"/python*

install -D debian/cron.daily "%{buildroot}/etc/cron.daily/%{name}"

%clean
%{?buildroot:%__rm -rf "%{buildroot}"}

%files
%defattr(-,root,root)
%doc GPL TODO README.md
%{_bindir}/etckeeper
%config(noreplace) /etc/cron.daily/etckeeper
%dir %{_sysconfdir}/etckeeper
%config(noreplace) %{_sysconfdir}/etckeeper/etckeeper.conf
%dir %{_sysconfdir}/etckeeper/*.d
%config %{_sysconfdir}/etckeeper/*.d/*
%if 0%{?suse_version}
%dir %{_prefix}/lib/zypp
%dir %{_prefix}/lib/zypp/plugins
%dir %{_prefix}/lib/zypp/plugins/commit
%{_prefix}/lib/zypp/plugins/commit/zypper-etckeeper.py
%endif
%if 0%{?fedora} || 0%{?rhel}
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/etckeeper.conf
%{_prefix}/lib/yum-plugins/etckeeper.*
%endif
%doc %{_mandir}/man8/etckeeper.8*
%config %{_sysconfdir}/bash_completion.d/etckeeper

%changelog
