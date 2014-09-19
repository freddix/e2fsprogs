Summary:	Utilities for managing the second extended (ext2) filesystem
Name:		e2fsprogs
Version:	1.42.12
Release:	1
License:	GPL
Group:		Core/System
Source0:	http://downloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
# Source0-md5:	68255f51be017a93f2f6402fab06c2bf
URL:		http://e2fsprogs.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
BuildRequires:	gettext-devel
BuildRequires:	libblkid-devel
BuildRequires:	pkg-config
BuildRequires:	texinfo
Requires:	util-linux
Requires:	libcom_err = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems. e2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck),
tune2fs (used to modify filesystem parameters) and most of the other
core ext2fs filesystem utilities.

%package libs
Summary:	ext2 filesystem-specific libraries
Group:		Libraries
Requires(post,postun):	/usr/sbin/ldconfig

%description libs
ext2 filesystem-specific libraries.

%package devel
Summary:	ext2 filesystem-specific libraries and headers
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libcom_err-devel = %{version}-%{release}

%description devel
e2fsprogs-devel contains the libraries and header files needed to
develop second extended (ext2) filesystem-specific programs.

%package -n libcom_err
Summary:	A Common Error Description Library for unices
Group:		Libraries

%description -n libcom_err
A Common Error Description Library for unices.

%package -n libcom_err-devel
Summary:	Development files for Common Error Description Library for unices
Group:		Development/Libraries
Requires:	libcom_err = %{version}-%{release}

%description -n libcom_err-devel
A Common Error Description Library for unices - development files.

%prep
%setup -q

tail -n +2604 aclocal.m4 > acinclude.m4

%build
%if 0
%{__libtoolize}
%{__gettextize}
%{__aclocal}
%{__autoconf}
%endif

%configure \
	--disable-e2initrd-helper	\
	--disable-fsck			\
	--disable-libblkid		\
	--disable-libuuid		\
	--disable-rpath			\
	--disable-uuidd			\
	--enable-elf-shlibs		\
	--with-root-prefix=""

%{__make} V=1 \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

echo "install-shlibs:" >> intl/Makefile

%{__make} -j1 install install-libs	\
	DESTDIR=$RPM_BUILD_ROOT		\
	LDCONFIG=/usr/sbin/ldconfig

touch $RPM_BUILD_ROOT/etc/e2fsck.conf

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/{mkfs,fsck}.ext[23].8*
echo '.so e2fsck.8' > $RPM_BUILD_ROOT%{_mandir}/man8/fsck.ext2.8
echo '.so e2fsck.8' > $RPM_BUILD_ROOT%{_mandir}/man8/fsck.ext3.8
echo '.so mke2fs.8' > $RPM_BUILD_ROOT%{_mandir}/man8/mkfs.ext2.8
echo '.so mke2fs.8' > $RPM_BUILD_ROOT%{_mandir}/man8/mkfs.ext3.8

[ "`file $RPM_BUILD_ROOT%{_datadir}/locale/it/LC_MESSAGES/e2fsprogs.mo |\
	sed -e 's/.*,//' -e 's/message.*//'`" -le 1 ] && rm -f $f
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%post	devel -p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-n libcom_err -p /usr/sbin/ldconfig
%postun	-n libcom_err -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING specifies license details for some parts of package
%doc COPYING README RELEASE-NOTES
%attr(755,root,root) %{_bindir}/chattr
%attr(755,root,root) %{_bindir}/lsattr
%attr(755,root,root) %{_bindir}/mk_cmds
%attr(755,root,root) %{_sbindir}/badblocks
%attr(755,root,root) %{_sbindir}/debugfs
%attr(755,root,root) %{_sbindir}/dumpe2fs
%attr(755,root,root) %{_sbindir}/e2freefrag
%attr(755,root,root) %{_sbindir}/e2fsck
%attr(755,root,root) %{_sbindir}/e2image
%attr(755,root,root) %{_sbindir}/e2label
%attr(755,root,root) %{_sbindir}/e2undo
%attr(755,root,root) %{_sbindir}/e4defrag
%attr(755,root,root) %{_sbindir}/filefrag
%attr(755,root,root) %{_sbindir}/fsck.ext2
%attr(755,root,root) %{_sbindir}/fsck.ext3
%attr(755,root,root) %{_sbindir}/fsck.ext4
%attr(755,root,root) %{_sbindir}/logsave
%attr(755,root,root) %{_sbindir}/mke2fs
%attr(755,root,root) %{_sbindir}/mkfs.ext2
%attr(755,root,root) %{_sbindir}/mkfs.ext3
%attr(755,root,root) %{_sbindir}/mkfs.ext4
%attr(755,root,root) %{_sbindir}/mklost+found
%attr(755,root,root) %{_sbindir}/resize2fs
%attr(755,root,root) %{_sbindir}/tune2fs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/e2fsck.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mke2fs.conf
%{_mandir}/man1/chattr.1*
%{_mandir}/man1/lsattr.1*
%{_mandir}/man1/mk_cmds.1*
%{_mandir}/man5/e2fsck.conf.5*
%{_mandir}/man5/ext*.5*
%{_mandir}/man5/mke2fs.conf.5*
%{_mandir}/man8/*
%{_datadir}/ss

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libe2p.so.?
%attr(755,root,root) %ghost %{_libdir}/libext2fs.so.?
%attr(755,root,root) %ghost %{_libdir}/libss.so.?
%attr(755,root,root) %{_libdir}/libe2p.so.*.*
%attr(755,root,root) %{_libdir}/libext2fs.so.*.*
%attr(755,root,root) %{_libdir}/libss.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/libblkid.txt
%attr(755,root,root) %{_libdir}/libe2p.so
%attr(755,root,root) %{_libdir}/libext2fs.so
%attr(755,root,root) %{_libdir}/libss.so
%{_includedir}/e2p
%{_includedir}/ext2fs
%{_includedir}/ss
%{_pkgconfigdir}/e2p.pc
%{_pkgconfigdir}/ext2fs.pc
%{_pkgconfigdir}/ss.pc
%{_infodir}/libext2fs.info*

%files -n libcom_err
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libcom_err.so.?
%attr(755,root,root) %{_libdir}/libcom_err.so.*.*

%files -n libcom_err-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/compile_et
%attr(755,root,root) %{_libdir}/libcom_err.so
%{_includedir}/com_err.h
%{_includedir}/et
%{_datadir}/et
%{_pkgconfigdir}/com_err.pc
%{_mandir}/man1/compile_et.1*
%{_mandir}/man3/com_err.3*

