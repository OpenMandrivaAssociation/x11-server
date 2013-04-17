%define git 0

%define with_debug 0
%define enable_dmx 1
%define enable_kdrive 0
%define enable_xfake 1
%define enable_udev 1
%define enable_dbus 0
%define enable_builddocs 0
# Do magic with .rpmsave named links
%define pre_post_trans 1

# Need this for shared objects that reference X Server, or other modules symbols
%define _disable_ld_no_undefined 1

# Alternatives priority for standard libglx.so and mesa libs
%define priority 500

# Search for modules in extra_module_dir before the default path.
# This will allow fglrx to install its modified modules in more cleaner way.
%define extra_module_dir %{_libdir}/xorg/extra-modules
%define xorg1_6_extra_modules %{_libdir}/xorg/xorg-1.6-extra-modules

%define rel 1

# ABI versions.  Have to keep these manually in sync with the source
# because rpm is a terrible language.  HTFU.
%define ansic_major 0
%define ansic_minor 4
%define videodrv_major 14
%define videodrv_minor 1
%define xinput_major 19
%define xinput_minor 1
%define extension_major 7
%define extension_minor 0

Name:		x11-server
Version:	1.14.1
%if %{git}
Release:	0.%{git}.%{rel}
%else
Release:	%{rel}
%endif
Summary:	X11 servers
Group:		System/X11
URL:		http://xorg.freedesktop.org
%if %{git}
Source0:	xorg-server-%{git}.tar.bz2
%else
Source0:	http://xorg.freedesktop.org/releases/individual/xserver/xorg-server-%{version}.tar.bz2
%endif
Source1:	xserver.pamd
Source2:	xvfb-run.sh
Source5:	mandriva-setup-keyboard-udev
Source6:	61-x11-input.rules
# from RH/FC:
# for requires generation in drivers
Source30:	xserver-sdk-abi-requires
Source100:	x11-server.rpmlintrc
License:	GPLv2+ and MIT

Requires:	%{name}-xorg
%if %{enable_dmx}
Requires:	%{name}-xdmx
%else
Obsoletes:	%{name}-xdmx < %{version}-%{release}
%endif
Requires:	%{name}-xnest
Requires:	%{name}-xvfb

# This should be removed when any of the vnc packages provide x11-server-xvnc:
Obsoletes:	%{name}-xvnc < %{version}-%{release}

%if !%{enable_xfake}
Obsoletes:	%{name}-xfake < %{version}-%{release}
%endif

# FIXME: build with systemtap installed is broken
BuildConflicts: systemtap

BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	libmesagl-devel >= 7.1
BuildRequires:	pam-devel
BuildRequires:	libpciaccess-devel
BuildRequires:	pkgconfig(pixman-1) >= 0.9.5
BuildRequires:	libxau-devel >= 1.0.0
BuildRequires:	libxaw-devel >= 1.0.1
BuildRequires:	libxdmcp-devel >= 1.0.0
BuildRequires:	libxext-devel >= 1.1
BuildRequires:	libxfixes-devel
BuildRequires:	libxfont-devel >= 1.2.8-2mdv
BuildRequires:	libxi-devel >= 1.1.3
BuildRequires:	libxkbfile-devel >= 1.0.4
BuildRequires:	libxmu-devel >= 1.0.0
BuildRequires:	libxpm-devel >= 3.5.4.2
BuildRequires:	libxrender-devel >= 0.9.4
BuildRequires:	libxres-devel >= 1.0.0
BuildRequires:	libxv-devel
BuildRequires:	x11-font-util >= 1.1
BuildRequires:	x11-proto-devel >= 7.6-4
BuildRequires:	x11-util-macros >= 1.15
BuildRequires:	x11-xtrans-devel >= 1.2.7-2

# Probably only needed if we change .l or .y files, but let's have them anyway:
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	bison

# for xkbcomp patch
BuildRequires:	openssl-devel

%if %{enable_udev}
BuildRequires:	pkgconfig(libudev) >= 186
%endif

%if %{enable_dbus}
BuildRequires:	libdbus-devel
%endif

%if %{enable_dmx}
BuildRequires:	libdmx-devel
BuildRequires:	libxtst-devel >= 1.1
%endif

%if %{enable_builddocs}
BuildRequires:	doxygen
#BuildRequires:	fop
BuildRequires:	lynx
BuildRequires:	xmlto
BuildRequires:	x11-sgml-doctools >= 1.8
%endif
BuildRequires:	pkgconfig(libtirpc) >= 0.2.0
BuildRequires:	glib2-devel
# Instructions to setup your repository clone
# git://anongit.freedesktop.org/git/xorg/xserver
# git checkout origin/server-1.7-branch
# git checkout -b mdv-1.7-cherry-picks
# git am ../03??-*.patch
# git checkout -b mdv-1.7-redhat
# git am ../04??-*.patch
# git checkout -b mdv-1.7-patches
# git am ../09??-*.patch

# Sync with server-1.6-branch
# git format-patch --start-number 100 xorg-server-1.6.4..server-1.6-branch

# Upstream cherry picks from master branch
# git format-patch --start-number 300 origin/server-1.6-branch..mdv-1.6.4-cherry-picks

# Patches "liberated" from Fedora:
# http://pkgs.fedoraproject.org/gitweb/?p=xorg-x11-server.git
# git format-patch --start-number 400 mdv-1.6.4-cherry-picks..mdv-1.6.4-redhat
# (eugeni) obsoleted with '-background none' option

# Mandriva patches
# git format-patch --start-number 900 mdv-1.6.4-redhat..mdv-1.6.4-patches
Patch900:	0900-Use-a-X-wrapper-that-uses-pam-and-consolehelper-to-g.patch
Patch901:	0901-Don-t-print-information-about-X-Server-being-a-pre-r.patch
Patch902:	0902-Take-width-into-account-when-choosing-default-mode.patch
Patch904:	0904-LED-behavior-fixes.patch
Patch905:	0905-Add-noAutoDevices-command-line-option.patch
Patch906:	0906-Xorg-add-an-extra-module-path.patch
Patch907:	0907-Add-nr-argument-for-backwards-compatibility.patch
Patch908:	0908-XKB-cache-xkbcomp-output-for-fast-start-up-v.1-for-1.patch
Patch910:	xorg-1.13.0-link-tirpc.patch

# (tv) fix issues with new cairo (fdo#47266):
Patch3000:	exa-glyphs-fallback.diff

# Other patches

# Do not crash if Xv is not initialized (patch from xorg-devel ML)
# The crash happened when v4l was loaded and xv was not registered,
# for example on RV610 with radeon driver
Patch1001: 1001-do-not-crash-if-xv-not-initialized.patch
Patch1002:	xserver_xorg-server-aarch64-support.patch

%description
X11 servers.

#------------------------------------------------------------------------------

%package	devel
Summary:	Development files for %{name}
Group:		Development/X11
License:	MIT

%define oldxorgnamedevel  %mklibname xorg-x11
Conflicts:	%{oldxorgnamedevel}-devel < 7.0
Obsoletes:	x11-server13-devel <= 1.2.99.905
Requires:	pkgconfig(pixman-1) >= 0.9.5
Requires:	libpciaccess-devel
Requires:	libxkbfile-devel
Requires:	libxext-devel >= 1.1
Requires:	pkgconfig(dri)

%description devel
Development files for %{name}.

%pre devel
if [ -h %{_includedir}/X11 ]; then
	rm -f %{_includedir}/X11
fi

%files devel
%dir %{_includedir}/xorg
%{_bindir}/xserver-sdk-abi-requires
%{_includedir}/xorg/*.h
%{_libdir}/pkgconfig/xorg-server.pc
%{_datadir}/aclocal/xorg-server.m4

#------------------------------------------------------------------------------

%package common
Summary:	X server common files
Group:		System/X11
License:	MIT
Provides:	XFree86 = 7.0.0
Conflicts:	xorg-x11 <= 6.9.0-12mdk
Obsoletes:	x11-server13-common <= 1.2.99.905
Obsoletes:	x11-server-xprt <= 1.3.0.0-2mdv2008.0
Requires:	rgb
# for 'fixed' and 'cursor' fonts
Requires:	x11-font-misc-misc
Requires:	x11-font-cursor-misc
Requires:	x11-font-alias
Requires:	x11-data-xkbdata
Requires:	xkbcomp
%if %{enable_udev}
Requires:	udev
%endif
Requires(post):	update-alternatives >= 1.9.0
Requires(postun):	update-alternatives
# see comment about /usr/X11R6/lib below
Conflicts:	filesystem < 2.1.8
# nvidia-71xx does not support X.org server >= 1.5
Conflicts:	x11-driver-video-nvidia71xx < 71.86.09-2
# old fglrx does not support X.org server >= 1.7
Conflicts:	x11-driver-video-fglrx < 8.720
# Fix: missing conflicts to allow upgrade from 2008.0 to cooker
# http://qa.mandriva.com/show_bug.cgi?id=36651
Conflicts:	x11-driver-video-nvidia-current <= 100.14.19
Conflicts:	x11-xorg1_5-server < 1.5.3-4

Provides:	xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides:	xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides:	xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides:	xserver-abi(extension-%{extension_major}) = %{extension_minor}

%description common
X server common files.

%post common
%{_sbindir}/update-alternatives \
	--install %{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf %{priority} \
	--slave %{extra_module_dir} xorg_extra_modules %{xorg1_6_extra_modules}

# (anssi)
%triggerun common -- %{name}-common < 1.3.0.0-17
[ $1 -eq 2 ] || exit 0 # do not run if downgrading
current_glconf="$(readlink -e %{_sysconfdir}/ld.so.conf.d/GL.conf)"
if [ "${current_glconf#*mesa}" == "gl1.conf" ]; then
	# This an upgrade of a system with no proprietary drivers enabled, update
	# the link to point to the new standard.conf instead of libmesagl1.conf (2008.0 change).
	%{_sbindir}/update-alternatives --set gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf
else
	# XFdrake did not set symlink to manual mode before 2008.0, so we ensure it here.
	%{_sbindir}/update-alternatives --set gl_conf "${current_glconf}"
fi
true

%postun common
if [ ! -f %{_sysconfdir}/ld.so.conf.d/GL/standard.conf ]; then
	/usr/sbin/update-alternatives --remove gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf
fi

%files common
%dir %{_libdir}/xorg/modules
%dir %{xorg1_6_extra_modules}
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/X11/app-defaults
%dir %{_sysconfdir}/X11/fontpath.d
%dir %{_sysconfdir}/ld.so.conf.d/GL
%dir %{_sysconfdir}/X11/xorg.conf.d
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%{_sysconfdir}/ld.so.conf.d/GL/standard.conf
%if %{enable_dbus}
%{_sysconfdir}/dbus-1/system.d/xorg-server.conf
%endif
%{_bindir}/gtf
%{_bindir}/cvt
%if %{enable_udev}
/sbin/mandriva-setup-keyboard
/lib/udev/rules.d/61-x11-input.rules
%endif
%if %{enable_dmx}
%{_bindir}/vdltodmx
%endif
%{_libdir}/xorg/modules/*
%{_libdir}/xorg/protocol.txt
%{_datadir}/X11/xkb/README.compiled
%{_mandir}/man1/gtf.*
%{_mandir}/man1/cvt.*
%if %{enable_dmx}
%{_mandir}/man1/vdltodmx.*
%endif
%{_mandir}/man4/fbdevhw.*
%{_mandir}/man4/exa.*
%dir %{_prefix}/X11R6
%dir %{_prefix}/X11R6/lib
%dir %{_prefix}/X11R6/lib/X11


#------------------------------------------------------------------------------

%package xorg
Summary:	X.org X11 server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}
Requires:	x11-data-xkbdata > 1.3-5
Requires:	x11-font-alias
Requires:	libx11-common
%if %{enable_udev}
Requires:	x11-driver-input-evdev
Requires:	udev
Conflicts:	drakx-kbd-mouse-x11 < 0.66
%else
Requires:	x11-driver-input-mouse
Requires:	x11-driver-input-keyboard
%endif
Conflicts:	compiz < 0.5.0-1mdv2007.1
Obsoletes:	x11-server13-xorg <= 1.2.99.905

# minimum libxfont needed for xserver-1.9:
Requires:	libxfont >= 1.4.2

# This package was used in the transition to modular:
Obsoletes:	xorg-x11-server

%description xorg
x11-server-xorg is the new generation of X server from X.Org.

%files xorg
%{_bindir}/X
%{_bindir}/Xorg
%attr(4755,root,root)%{_bindir}/Xwrapper
%{_sysconfdir}/X11/X
%{_sysconfdir}/pam.d/xserver
%{_sysconfdir}/security/console.apps/xserver
%{_mandir}/man1/Xorg.*
%{_mandir}/man1/Xserver.*
%{_mandir}/man5/xorg.conf.*
%if %{enable_udev}
%{_datadir}/X11/xorg.conf.d/10-evdev.conf
%endif

#------------------------------------------------------------------------------

%if %{enable_dmx}
%package xdmx
Summary:	Distributed Multi-head X server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}

# This package was used in the transition to modular:
Obsoletes:	xorg-x11-Xdmx

%description xdmx
Xdmx is a proxy X server that uses one or more other X servers
as its display devices. It provides multi-head X functionality
for displays that might be located on different machines.
Xdmx functions as a front-end X server that acts as a proxy
to a set of back-end X servers. All of the visible rendering is
passed to the back-end X servers. Clients connect to the Xdmx
front-end, and everything appears as it would in a regular
multi-head configuration. If Xinerama is enabled (e.g.,
with +xinerama on the command line), the clients see a single large screen.

Xdmx communicates to the back-end X servers using the standard X11 protocol,
and standard and/or commonly available X server extensions.

%files xdmx
%{_bindir}/Xdmx
%{_bindir}/xdmx*
%{_bindir}/dmx*
%{_mandir}/man1/Xdmx.*
%{_mandir}/man1/xdmxconfig.*
%{_mandir}/man1/dmxtodmx.*
%endif

#------------------------------------------------------------------------------

%package xnest
Summary:	A nested X server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}

# This package was used in the transition to modular:
Obsoletes:	xorg-x11-Xnest

%description xnest
Xnest is an X Window System server which runs in an X window.
Xnest is a 'nested' window server, actually a client of the
real X server, which manages windows and graphics requests
for Xnest, while Xnest manages the windows and graphics
requests for its own clients.

You will need to install Xnest if you require an X server which
will run as a client of your real X server (perhaps for
testing purposes).

%files xnest
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.*

#------------------------------------------------------------------------------

%package xvfb
Summary:	X virtual framebuffer server
Group:		System/X11
# xvfb-run is GPLv2, rest is MIT
License:	MIT and GPLv2
Requires:	x11-server-common = %{version}-%{release}
Requires:	xauth

# This package was used in the transition to modular:
Obsoletes:	xorg-x11-Xvfb

%description xvfb
Xvfb (X Virtual Frame Buffer) is an X Windows System server
that is capable of running on machines with no display hardware and no
physical input devices.  Xvfb emulates a dumb framebuffer using virtual
memory.  Xvfb doesn't open any devices, but behaves otherwise as an X
display.  Xvfb is normally used for testing servers.  Using Xvfb, the mfb
or cfb code for any depth can be exercised without using real hardware
that supports the desired depths.  Xvfb has also been used to test X
clients against unusual depths and screen configurations, to do batch
processing with Xvfb as a background rendering engine, to do load testing,
to help with porting an X server to a new platform, and to provide an
unobtrusive way of running applications which really don't need an X
server but insist on having one.

If you need to test your X server or your X clients, you may want to
install Xvfb for that purpose.

%files xvfb
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.*

#------------------------------------------------------------------------------

%package xephyr
Summary:	KDrive Xephyr X server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}

%description xephyr
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

Xephyr is a X Server which targets a window on a host X Server
as its framebuffer. Unlike Xnest it supports modern X extensions ( even
if host server doesn't ) such as Composite, Damage, randr etc. It uses SHM
Images and shadow framebuffer updates to provide good performance. It also
has a visual debugging mode for observing screen updates.

Possible uses include:
- Xnest replacement - Window manager, Composite 'gadget', etc development tool.
- Toolkit debugging - rendundant toolkit paints can be observered easily via
  the debugging mode.
- X Server internals development - develop without the need for an extra
  machine.

%files xephyr
%{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1*

#------------------------------------------------------------------------------

%if %{enable_xfake}
%package xfake
Summary:	KDrive fake X server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}

%description xfake
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for testing purposes.

%files xfake
%{_bindir}/Xfake
%endif

#------------------------------------------------------------------------------

%package xfbdev
Summary:	KDrive fbdev X server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}

%description xfbdev
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for being used on top of linux framebuffer.

%files xfbdev
%{_bindir}/Xfbdev

#------------------------------------------------------------------------------

%define xserver_source_dir %{_datadir}/%{name}-source

%package source
Summary:	Xserver source code required to build unofficial servers
Group:		Development/X11
License:	MIT
BuildArch:	noarch

%description source
Xserver source code needed to build unofficial servers, like Xvnc.

%files source
%{xserver_source_dir}

#------------------------------------------------------------------------------

%prep
%if %{git}
%setup -q -n xorg-server-%{git}
%else
%setup -q -n xorg-server-%{version}
%endif
%apply_patches

# check the ABI in the source against what we expect.
getmajor() {
   grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
   tr '(),' '   ' | awk '{ print $4 }'
}

getminor() {
   grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
   tr '(),' '   ' | awk '{ print $5 }'
}

test `getmajor ansic` == %{ansic_major}
test `getminor ansic` == %{ansic_minor}
test `getmajor videodrv` == %{videodrv_major}
test `getminor videodrv` == %{videodrv_minor}
test `getmajor xinput` == %{xinput_major}
test `getminor xinput` == %{xinput_minor}
test `getmajor extension` == %{extension_major}
test `getminor extension` == %{extension_minor}


%build

autoreconf -if

# Copy the clean dir to a 'source' directory that will be used to make the
# x11-server-source subpackage
mkdir source
find . -maxdepth 1 ! -name source ! -name '\.' -exec cp -r '{}' source \;


%if %{with_debug}
CFLAGS='-DBUILDDEBUG -O0 -g3' \
%endif
%configure2_5x \
	--with-log-dir=%{_logdir} \
	--with-os-vendor="%_vendor" \
	--with-os-name="`echo \`uname -s -r\` | sed -e s'/ /_/g'`" \
	--with-vendor-web="http://qa.mandriva.com" \
	--with-extra-module-dir=%{extra_module_dir} \
		%if %{with_debug}
		--enable-debug \
		%else
		--disable-debug \
		%endif
		%if %{enable_builddocs}
		--enable-builddocs \
		%else
		--disable-builddocs \
		%endif
		%if %{enable_udev}
		--enable-config-udev \
		%else
		--disable-config-udev \
		%endif
		--disable-strict-compilation \
		--disable-install-libxf86config \
		--enable-composite \
		--enable-xres \
		--enable-record \
		--enable-xv \
		--enable-xvmc \
		--enable-dga \
		--enable-screensaver \
		--enable-xdmcp \
		--enable-xdm-auth-1 \
		--enable-glx \
		--enable-aiglx \
		--enable-glx-tls \
		--enable-dri \
		--enable-xinerama \
		--enable-xf86vidmode \
		--enable-xace \
		--enable-xcsecurity \
		--enable-xf86bigfont \
		--enable-dpms \
		--disable-tslib \
		--enable-dbe \
		--enable-xfree86-utils \
		--enable-xorg \
		%if %enable_dmx
		--enable-dmx \
		%else
		--disable-dmx \
		%endif
		--enable-xvfb \
		--enable-xnest \
		--disable-xwin \
		--enable-kdrive \
		%if %enable_xfake
		--enable-xfake \
		%else
		--disable-xfake \
		%endif
		--enable-xephyr \
		--disable-install-setuid \
		--enable-secure-rpc \
		--enable-xwrapper \
		--enable-pam \
		%if %{enable_dbus}
		--enable-config-dbus \
		%else
		--disable-config-dbus \
		%endif
		--disable-config-hal \
		--with-sha1=libcrypto \
		--with-default-font-path="catalogue:%{_sysconfdir}/X11/fontpath.d"

pushd include && make xorg-server.h dix-config.h xorg-config.h && popd

%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/X11/
ln -s %{_bindir}/Xorg %{buildroot}%{_sysconfdir}/X11/X
ln -sf %{_bindir}/Xwrapper %{buildroot}%{_bindir}/X

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %SOURCE1 %{buildroot}%{_sysconfdir}/pam.d/xserver
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
touch %{buildroot}%{_sysconfdir}/security/console.apps/xserver

mkdir -p %{buildroot}%{_sysconfdir}/X11/app-defaults
mkdir -p %{buildroot}%{_sysconfdir}/X11/fontpath.d

# move README.compiled outside compiled/ dir, so there won't be any problem with x11-data-xkbdata
mv -f %{buildroot}%{_datadir}/X11/xkb/compiled/README.compiled %{buildroot}%{_datadir}/X11/xkb/

# for compatibility with legacy applications (see #23423, for example)
mkdir -p %{buildroot}%{_prefix}/X11R6/lib/
ln -s ../../%{_lib}/X11 %{buildroot}%{_prefix}/X11R6/lib/X11

# create more module directories to be owned by x11-server-common
install -d -m755 %{buildroot}%{_libdir}/xorg/modules/{input,drivers}
install -d -m755 %{buildroot}%{xorg1_6_extra_modules}

# (anssi) manage proprietary drivers
install -d -m755 %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL/standard.conf << EOF
# This file is knowingly empty since the libraries are in standard search
# path. Please do not remove this file.
EOF
touch %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL.conf

install -m 0755 %SOURCE2 %{buildroot}%{_bindir}/xvfb-run

%if %enable_udev
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}/lib/udev/rules.d/
install -m 0755 %{SOURCE5} %{buildroot}/sbin/mandriva-setup-keyboard
install -m 0644 %{SOURCE6} %{buildroot}/lib/udev/rules.d
%endif

# Make the source package
cp -r source %{buildroot}/%{xserver_source_dir}

install -m 755 %{SOURCE30} %{buildroot}%{_bindir}

# Create xorg.conf.d
install -d -m 755 %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

%files


%changelog
* Sat Dec 1 2012 akdengi <akdengi>
- bump videodrv minor
- drop merged patches
- 1.13.1-rc1

* Wed Nov 14 2012 akdengi <akdengi>
- fix Cairo corruption (fdo#55723)
- update glyphs cache patch
- use new pixman API for caching glyphs (3.45x firefox speedup)
- dri2: invalidate drawable after sharing pixmap (for PRIME, from Dave Airlie, Fedora)

* Thu Oct 04 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.13.0-3
+ Revision: 818405
+ rebuild (emptylog)

* Thu Oct 04 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.13.0-2
+ Revision: 818394
- Require pkgconfig(dri) for -devel, as the pkgconfig file implies
- Link to tirpc for sunrpc bits that have been removed from glibc

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - Patch1000: use new pixman API 0.27.2 (patch spotted on mageia, orginally form Soren Sandmann <ssp@redhat.com>)

* Mon Sep 17 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.13.0-1
+ Revision: 817053
- rediff 0905-Add-noAutoDevices-command-line-option.patc version update 1.13.0

* Mon Aug 27 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.12.4-2
+ Revision: 815837
- Update to 1.12.4

* Wed Jul 11 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.12.3-2
+ Revision: 808919
- install udev rules in /lib/udev instead of /etc/udev
- adjust mandriva-setup-keyboard to udev changes

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Update to 1.12.3

* Sun Jul 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.12.2.902-2
+ Revision: 808507
- Build against libudev.so.1

* Thu Jul 05 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.12.2.902-1
+ Revision: 808251
- update to new version 1.12.2.902

* Thu Jun 28 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.12.2.901-1
+ Revision: 807327
- 1.12.2.901

* Wed Jun 20 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.12.2-1
+ Revision: 806553
- drop patch 1000, fixed long time ago in nvidia proprietary drivers
- rediff other patches
- update to new version 1.12.2

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Update to 1.12.1

* Tue Apr 10 2012 Franck Bui <franck.bui@mandriva.com> 1.12.0-2
+ Revision: 790250
+ rebuild (emptylog)

* Tue Mar 20 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.12.0-1
+ Revision: 785839
- 1.12.0
- Fix use-of-RPM_SOURCE_DIR
- Don't BuildConflict with systemtap, seems to have been fixed upstream
- Update to 1.11.4

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added obsoletes xfbdev is not built

* Thu Dec 29 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.11.3-1
+ Revision: 748174
- enable_xfbdev is also part of kdrive
- removed installed backup files
- tied xfake build to kdrive
- grouped enable/disable zephyr with kdrive build option
- added build option to disable kdrive by default
- build is broken and not a default option
- removed disable strict compile
- cleaned up spec
- try using --disable-strict-compilation to fix build error
- employed apply_patches

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - correct buildrequire to pam-devel
    - update to new version 1.11.3

* Sun Nov 06 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.11.2-1
+ Revision: 722818
- update to new version 1.11.2

* Sat Oct 22 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.11.1-3
+ Revision: 705660
- disable patch 1000 because nVIDIA has released a fixed driver 290.03 (keep patch for a while)

* Sun Oct 09 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.11.1-2
+ Revision: 703940
- small spec file clean
- rediff patch 904
- Patch1000: this patch restores a missing miTrapezoids function which is used by nVIDIA proprietary drivers, this patch should be removed if a major slowdown problem will be fixed in next driver release by nVIDIA

* Sat Oct 08 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.11.1-1
+ Revision: 703608
- rediff patch 900
- Patch403: add systemd multi-seat support (from Fedora)
- bump required version for x11-util-macros
- bump required version for x11-proto-devel and x11-sgml-doctools
- remove dead configure switches
- update to new version 1.11.1
- disable patches 900 and 904

* Fri Oct 07 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.10.4-1
+ Revision: 703492
- update to new version 1.10.4
- add build requires on bison and glib2-devel
- export %%serverbuild macro
- enable-builddocs switch no longer works with configure script, pass valid switches for building docs

* Tue Jul 26 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.10.3-1
+ Revision: 691663
- Updated to 1.10.3

  + Thierry Vignaud <tv@mandriva.org>
    - use %%_vendor

* Thu Jun 09 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.10.2-1
+ Revision: 683527
- Add lynx as BR for documentation.
- New version 1.10.2.
  Changed ABI major.
  Comment non-compatible patches for now.

* Tue May 24 2011 Funda Wang <fwang@mandriva.org> 1.9.5-1
+ Revision: 678059
- new version 1.9.5

* Sun May 15 2011 Oden Eriksson <oeriksson@mandriva.com> 1.9.4-4
+ Revision: 674764
- try to build without fop for now
- sync with what's actually in cooker
- mass rebuild

  + Paulo Ricardo Zanoni <pzanoni@mandriva.com>
    - New version: 1.10.0
    - Dropped patches:
      - 401: partially applied, see patch 907
      - 402: the place where we copied the patch from is not using it anymore
      - 1000: applied upstream
    - New patches:
      - 907: implement what's left from old patch 401
    - Rediff other patches, fix patch numbering

* Sat Feb 26 2011 Funda Wang <fwang@mandriva.org> 1.9.4-3
+ Revision: 639943
- rebuild

* Tue Feb 15 2011 Thierry Vignaud <tv@mandriva.org> 1.9.4-2
+ Revision: 637876
- patches 1000: Fix garbaged screeen with latest ati driver 6.14 on open
  openoffice.org startup I (color tiling issue, fdo bug #33929)

  + Paulo Ricardo Zanoni <pzanoni@mandriva.com>
    - New version: 1.9.4

* Wed Feb 02 2011 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.9.3.902-1
+ Revision: 635187
- New version: 1.9.3.902

* Wed Dec 29 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.9.3-3mdv2011.0
+ Revision: 626003
- Remove useless udev rules
- Create /etc/X11/xorg.conf.d

* Tue Dec 21 2010 Thierry Vignaud <tv@mandriva.org> 1.9.3-2mdv2011.0
+ Revision: 623554
- patches 950 & 951: Fix edge case in SYNC extension resulting in GNOME
  screensaver's fade-to-screensaver being uninteruptible (from Ubuntu)

* Mon Dec 13 2010 Thierry Vignaud <tv@mandriva.org> 1.9.3-1mdv2011.0
+ Revision: 620682
- new release

* Wed Dec 08 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.9.2.902-3mdv2011.0
+ Revision: 616332
- Copy the whole source to the "-source" subpackage, avoiding hacks.

* Mon Dec 06 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.9.2.902-2mdv2011.0
+ Revision: 612188
- Add more files to the -source subpackage (for tigervnc)

* Sun Dec 05 2010 Thierry Vignaud <tv@mandriva.org> 1.9.2.902-1mdv2011.0
+ Revision: 610592
- 1.9.3 RC2
- drop patch 903 (merged upsteam long ago, see quirk_detailed_sync_pp())

* Sun Nov 14 2010 Thierry Vignaud <tv@mandriva.org> 1.9.2.901-1mdv2011.0
+ Revision: 597541
- 1.9.3 RC1

* Tue Nov 02 2010 Thierry Vignaud <tv@mandriva.org> 1.9.2-1mdv2011.0
+ Revision: 591815
- new release

* Sun Oct 24 2010 Thierry Vignaud <tv@mandriva.org> 1.9.1-2mdv2011.0
+ Revision: 588677
- provides actual ABI so that drivers can requires xorg ABIs
  (taken from Fedora, but we do will use it unlike them)
- x11-server-xorg only requires x11-driver-input-{keyboard,mouse} if not using
  hal or udev

* Sun Oct 24 2010 Funda Wang <fwang@mandriva.org> 1.9.1-1mdv2011.0
+ Revision: 587886
- 1.9.1 final
- fontdir switch becomes unrecognized

* Tue Oct 19 2010 Thierry Vignaud <tv@mandriva.org> 1.9.0.902-2mdv2011.0
+ Revision: 586767
- make x11-server-xorg requires x11-driver-input-evdev since it's a must have with udev

* Fri Oct 15 2010 Thierry Vignaud <tv@mandriva.org> 1.9.0.902-1mdv2011.0
+ Revision: 585880
- 1.9.0.902 (aka 1.9.1rc2)

* Sun Oct 10 2010 Thierry Vignaud <tv@mandriva.org> 1.9.0-3mdv2011.0
+ Revision: 584858
- mandriva-setup-keyboard-udev: update for xserver-1.9 (Andrey Borzenkov)

* Sun Oct 10 2010 Thierry Vignaud <tv@mandriva.org> 1.9.0-2mdv2011.0
+ Revision: 584843
- use udev instead of hal
- fix file list when enabling udev

* Sun Oct 10 2010 Thierry Vignaud <tv@mandriva.org> 1.9.0-1mdv2011.0
+ Revision: 584624
- new release
- refresh patch 401
- drop patch 400 & 403 (rh patches droped by rh)
- rediff xkb cache patch
- BuildRequires: x11-font-util >= 1.1
- require new enough libxfont (prevent startup breakage)
- Xsdl is dead

* Tue May 04 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.7-1mdv2010.1
+ Revision: 542076
- New version: 1.7.7

* Thu Apr 29 2010 Pascal Terjan <pterjan@mandriva.org> 1.7.6.902-5mdv2010.1
+ Revision: 540801
- rebuild with normal ld

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.7.6.902-4mdv2010.1
+ Revision: 539609
- rebuild so that shared libraries are properly stripped again

* Tue Apr 27 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.6.902-3mdv2010.1
+ Revision: 539412
- Add patch from "nominations" branch that should fix the current problems

* Thu Apr 22 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.6.902-1mdv2010.1
+ Revision: 537967
- New version: 1.7.6.902
- Patch 0909 applied upstream
- Re-enable xfake
- Improve mouse-quirks documentation

* Tue Apr 13 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.6-6mdv2010.1
+ Revision: 534199
- Add mouse-quirks.fdi that should replace imwheel

* Mon Apr 05 2010 Funda Wang <fwang@mandriva.org> 1.7.6-5mdv2010.1
+ Revision: 531722
- rebuild for new openssl

* Tue Mar 30 2010 Anssi Hannula <anssi@mandriva.org> 1.7.6-4mdv2010.1
+ Revision: 528934
- allow fglrx 8.720+ as they have X.org server 1.7 support

* Fri Mar 26 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.6-3mdv2010.1
+ Revision: 527643
- x11-server-source: remove noarch and add License

* Wed Mar 24 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.6-2mdv2010.1
+ Revision: 527275
- Add x11-server-source package (for Xvnc)
  Thanks to Shlomi Fish for providing the patche.
  This commit also removes some trailing whitespaces in the spec file.

* Wed Mar 24 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.6-1mdv2010.1
+ Revision: 527233
- New version: 1.7.6
  Only apply udev patches if udev is enabled (and it won't be until 2011.0)

* Fri Mar 12 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.5-4mdv2010.1
+ Revision: 518396
- Add patch to warn us if we run out of opcodes

* Thu Mar 11 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.5-3mdv2010.1
+ Revision: 518021
- Don't explicitly enable multibuffer extension (use upstream default, which is
  "disabled" for now)
  This extension is old, deprecated and has 2 events. Nvidia closed source driver
  adds 5 events and makes us exceed the event limit (64). This causes random (and
  probably important) extensions to be disabled.
  This bug was triggered by the last rebuild, which uses the new dri2 proto, which
  contains 1 more event.
  Thanks to Anssi for debugging and finding the fix.
  See bug #57889

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.5-2mdv2010.1
+ Revision: 511662
- rebuilt against openssl-0.9.8m

* Wed Feb 17 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.5-1mdv2010.1
+ Revision: 507004
- New version: 1.7.5
- Apply xkb mapping to all input devices with keys (by Andrey Borzenkov)
- 61-x11-input.rules: do nothing if ACTION!="add"
  (saves calls to mandriva-setup-keyboard when keyboards are removed)
  Thanks to Andrey Borzenkov for spotting this.
- Add disabled libudev input hotplug backend support

  + Anssi Hannula <anssi@mandriva.org>
    - add conflict with fglrx driver, does not work with 1.7+ server

* Fri Jan 08 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.4-1mdv2010.1
+ Revision: 487684
- Remove patch 907 because it was required only by the older xkbcomp patch
- New version: 1.7.4
  Rediff patch ctrl+alt+backspace patch

* Wed Jan 06 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.3-2mdv2010.1
+ Revision: 486868
- x11-server-common should require xkbcomp and x11-data-xkbdata (#56818)

* Thu Dec 03 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.3-1mdv2010.1
+ Revision: 473018
- New version: 1.7.3
- Re-enable xkbcomp patch.
  Now it creates the temporary file in the same directory as the final file, so
  reanme() won't have problems with multiple partitions.
  Also, the file name is now tmp-<display>.xkm, which eliminates the possibility
  of race conditions since each X server will have its own file name. This removes
  the usage of the deprecated functions used to create temporary files

* Wed Dec 02 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.2-3mdv2010.1
+ Revision: 472715
- Temporarily disable xkbcomp patch again because it uses "rename", which doesn't
  work between multiple file systems.
  This is just to prevent more systems breaking. New version is coming soon.

* Tue Dec 01 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.2-2mdv2010.1
+ Revision: 472433
- Re-enable xkbcomp patch, but now based on Yan Li's version (smaller patch)

* Fri Nov 27 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.2-1mdv2010.1
+ Revision: 470564
- New version: 1.7.2

* Fri Nov 13 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.1-5mdv2010.1
+ Revision: 465889
- Obsolete xorg-x11-server

* Fri Nov 13 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.1-4mdv2010.1
+ Revision: 465827
- Obsolete xorg-x11-Xnest and xorg-x11-Xvfb
- Remove unrecognized configure options
- Remove kdrive-vesa modules.
  They have been removed from the xserver code a long time ago and won't come
  back, so we can clean the spec.

  + Thierry Vignaud <tv@mandriva.org>
    - add a warning

* Wed Nov 11 2009 Thierry Vignaud <tv@mandriva.org> 1.7.1-3mdv2010.1
+ Revision: 464384
+ rebuild (emptylog)

* Tue Nov 10 2009 Thierry Vignaud <tv@mandriva.org> 1.7.1-2mdv2010.1
+ Revision: 464381
- make it installable on x86_64

* Tue Nov 10 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.7.1-1mdv2010.1
+ Revision: 464242
- New version: 1.7.1
  Updated and reorganized patches
  Enabled xdmx
  Temporarily disabled xvnc and the xkbcomp patch (this will be fixed soon)
- Obsolete xorg-x11-Xdmx: package was used in the transition to modular

* Tue Oct 13 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.6.5-1mdv2010.0
+ Revision: 457143
- 1.6.5 release

* Tue Sep 29 2009 Colin Guthrie <cguthrie@mandriva.org> 1.6.4-2mdv2010.0
+ Revision: 451066
- DGA driver fixes (KeithP's third attempt - brown paper bag firmly in place)

* Tue Sep 29 2009 Colin Guthrie <cguthrie@mandriva.org> 1.6.4-1mdv2010.0
+ Revision: 450839
- New version: 1.6.4

  + Paulo Ricardo Zanoni <pzanoni@mandriva.com>
    - Fix double BuildRequires for libxfont-devel

* Fri Sep 18 2009 Jérôme Quelin <jquelin@mandriva.org> 1.6.3.901-2mdv2010.0
+ Revision: 444263
- rebuild
- fix bug 52928

* Thu Aug 27 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.3.901-1mdv2010.0
+ Revision: 421758
- Update to version 1.6.3.901 (1.6.4 RC1)

* Tue Aug 18 2009 Colin Guthrie <cguthrie@mandriva.org> 1.6.3-2mdv2010.0
+ Revision: 417657
- Cherry-pick fix for fdo#21554 (reprobe randr after resume from suspend)

* Mon Aug 17 2009 Colin Guthrie <cguthrie@mandriva.org> 1.6.3-1mdv2010.0
+ Revision: 417170
- New version: 1.6.3
- Drop upstream applied patches
- Rediff patches that need it
- Cherry pick fix for gnome screenblanking issue

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.6.2-4mdv2010.0
+ Revision: 416534
- rebuilt against libjpeg v7

* Tue Jul 21 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.6.2-3mdv2010.0
+ Revision: 398291
- Don't allow build with systemtap (build fails, dtrace support
  conflicts).
- Apply fix for http://bugs.freedesktop.org/show_bug.cgi?id=22642 (from
  xorg git repository). Fix assertions triggering with EXA after
  libpixman 0.15.16 update.

* Thu Jul 09 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.2-2mdv2010.0
+ Revision: 393980
- Sync with server-1.6-branch
 o Fix build of drivers with 1.6.2 when not using --install-libxf86config
 o xdmcp: Don't crash on X -query with more than 255 IP addresses. (fdo #20675)

* Wed Jul 08 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.2-1mdv2010.0
+ Revision: 393521
- Update to newer version 1.6.2

* Tue Jun 30 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1.902-4mdv2010.0
+ Revision: 391048
- sync with server-1.6-branch
- update to 1.6.1.902
- xvfb-run: fix Xauthority creation when TMPDIR is set

* Thu Jun 18 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1.901-4mdv2010.0
+ Revision: 387219
- add ZapWarning option enabled by default (OpenSUSE patch)

  + Colin Guthrie <cguthrie@mandriva.org>
    - Use the offical %%apply_patches macro

* Wed Jun 17 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1.901-3mdv2010.0
+ Revision: 386506
- sync with server-1.6-branch
- mandriva-setup-keyboard: set XkbModel
- reenable Zapping (default behaviour unchanged due to xkeyboard-config 1.6)

* Tue Jun 02 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1.901-2mdv2010.0
+ Revision: 382303
- sync with server-1.6-branch
- add patch to fix mdv #48821

* Tue May 19 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1.901-1mdv2010.0
+ Revision: 377787
- Update to version 1.6.1.901

* Mon May 04 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1-1mdv2010.0
+ Revision: 371954
- Fix crash while using Xinerama and holding key pressed (mdv #50472)

  + Christophe Fergeau <cfergeau@mandriva.com>
    - Fix typo noticed by Colin Gunthrie, thanks :)
    - Make it possible to run mandriva-setup-keyboard standalone (for now it's only
      a HAL callout). drakx-x11-keyboard-mouse needs it to be able to update the
      HAL xkb keys when the user chooses a different keyboard layout so that it's
      preserved on X restarts.

* Tue Apr 14 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.1-1mdv2009.1
+ Revision: 367232
- New version 1.6.1

* Mon Apr 13 2009 Anssi Hannula <anssi@mandriva.org> 1.6.0-12mdv2009.1
+ Revision: 366756
- add conflicts on now-removed nvidia71xx driver as it does not support
  X.org server 1.5+

* Mon Apr 13 2009 Anssi Hannula <anssi@mandriva.org> 1.6.0-11mdv2009.1
+ Revision: 366533
- drop alternatives on /usr/bin/Xorg as fglrx no longer needs 1.5 server

* Thu Apr 09 2009 Colin Guthrie <cguthrie@mandriva.org> 1.6.0-10mdv2009.1
+ Revision: 365459
- Fix GLX memory leak (fdo#20704)

* Mon Apr 06 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-9mdv2009.1
+ Revision: 364529
- sync with server-1.6-branch
- fix crash with a device section for an unplugged wacom device (#49349)

* Tue Mar 24 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-8mdv2009.1
+ Revision: 360906
- port xkb cache patch to server 1.6
- remove some disabled patches:
  - blue background (503): stick to X new default, black
  - fix incorrect keyboard test (532): similar patch applied upstream
  - fix crash in xorgcfg (901): xorgcfg was removed before the release of 1.6

* Thu Mar 19 2009 Anssi Hannula <anssi@mandriva.org> 1.6.0-7mdv2009.1
+ Revision: 357876
- add a ghost file for Xorg and remove hacks

* Thu Mar 19 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-6mdv2009.1
+ Revision: 357778
- Move libglx and libdri to default path. (mdv #48936)

* Thu Mar 19 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-5mdv2009.1
+ Revision: 357773
- common: call update-alternatives to ensure the links exist after the install step in %%post

* Wed Mar 18 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-4mdv2009.1
+ Revision: 357470
- Fix upgrade from versions <= 1.6.0-2
  Since the /usr/bin/Xorg file was provided by x11-server-xorg, which depends on x11-server-common
  but the new alternative link is created by x11-server-common, it got removed when the old
  x11-server-xorg was removed and had to be manually created.

* Tue Mar 17 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-3mdv2009.1
+ Revision: 356864
- Patch to search extra modules directory befero default module path
- Use alternatives for the Xorg binary.

* Thu Mar 05 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.6.0-2mdv2009.1
+ Revision: 349183
- Honour Option "DPMS" "off" in xorg.conf

* Thu Feb 26 2009 Colin Guthrie <cguthrie@mandriva.org> 1.6.0-1mdv2009.1
+ Revision: 345307
- Replace old tarball with 1.6.0 source.
- Remove reverted change as it was fixed differently upstream

  + Ander Conselvan de Oliveira <ander@mandriva.com>
    - New version 1.6.0

* Mon Feb 23 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.903-2mdv2009.1
+ Revision: 344041
- Add upstream patch to fix compilation (fontmod.h)
- Upstream c-p to initialise glx properly.
- Revert glx retval checks as it seems to break compiz (further investigation needed)

* Wed Feb 18 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.903-1mdv2009.1
+ Revision: 342642
- New version 1.5.99.903 (1.6 RC 3)

* Wed Feb 11 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.902-1.20090131.5mdv2009.1
+ Revision: 339487
- revert "only call mandriva-setup-keyboard for devices with input.capabilities = keyboard" (mdv #47647)
- remove patch 0301-RH-xserver-1.4.99-dont-backfill-bg-none (mdv #47126)

* Mon Feb 09 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.902-1.20090131.4mdv2009.1
+ Revision: 338999
- Add patch by Eric Anholt to unbreak GLX visuals

* Sat Feb 07 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.902-1.20090131.3mdv2009.1
+ Revision: 338363
- Update 10-x11-keymap.fdi: only call mandriva-setup-keyboard for devices with input.capabilities = keyboard (rh#484217)

* Sat Feb 07 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.902-1.20090131.2mdv2009.1
+ Revision: 338362
- Update upstream cherry-picks from the X.org wiki
- Replace local patch (composite from fdo#19337) with upstream fix (well, it hopefully fixes...)

* Sat Jan 31 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.902-1.20090131.1mdv2009.1
+ Revision: 335753
- X.Org X Server 1.5.99.902 (1.6.0 RC 2)
- Rediff & drop upstream applied patches
- Add extra patch from RH

* Wed Jan 28 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20090110.13mdv2009.1
+ Revision: 334930
- Remove auto-enable IgnoreABI patch. It worked only for nvidia devices for
  which drivers have been update
- Add -noAutoAddDevices command line option.

* Tue Jan 27 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20090110.12mdv2009.1
+ Revision: 334412
- Fix leds state reset on xkb layout changes

* Fri Jan 23 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20090110.11mdv2009.1
+ Revision: 333119
- Call slave devices ctrl proc in CoreKeyboardCtl to sync leds (bug #36893)

* Wed Jan 21 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20090110.10mdv2009.1
+ Revision: 332299
- Fix crash with multimedia keys (mdv #46863)
- Keep trying to connect to HAL at startup
- Use built-in fonts only if fixed font is not found in the fontpath

* Mon Jan 19 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20090110.9mdv2009.1
+ Revision: 331361
- Fix crash on startup due to unallocated private in xf86Crtc.c

* Fri Jan 16 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.3-1.20090110.8mdv2009.1
+ Revision: 330140
- Remove double buildrequire on libdmx-devel
- Move the xfake disabling into the header (still need to fix the build properly)
- Add obsoletes when disabling parts of the xserver build process (to smooth upgrades)

* Thu Jan 15 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20090110.7mdv2009.1
+ Revision: 329957
- Re-enable Xvnc support
- Remove disabled patch 0530 since it is included in new patch 0700

* Tue Jan 13 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.3-1.20090110.6mdv2009.1
+ Revision: 329209
- Apply patch to fix some startup errors
- Ignore ABI for nvidia/fglrx/vboxvideo

* Sat Jan 10 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.3-1.20090110.5mdv2009.1
+ Revision: 328001
- Update to latest snapshot
- Track the server-1.6-enterleave branch to test new enterleave model
- Remove upstream cherry picks merged in upstream
- Rediff patches
- Remove unneeded configure options

* Thu Jan 08 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20081222.4mdv2009.1
+ Revision: 327125
- Disable XAA offscreen pixmaps by default

* Mon Jan 05 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.99.3-1.20081222.3mdv2009.1
+ Revision: 325074
- Disable built-in fonts support

* Thu Jan 01 2009 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.3-1.20081222.2mdv2009.1
+ Revision: 323202
- Apply the proposes upstream cherry-picks to our package
- Add an additional patch from RH
- Add a patch to protect against the CopyKeyClass segv
- Use a shortcut method of applying all pathes to ease management

* Tue Dec 30 2008 Colin Guthrie <cguthrie@mandriva.org> 1.5.99.3-1.20081222.1mdv2009.1
+ Revision: 321373
- Add BuildRequire for flex
- BuildRequires byacc
- Add BuildRequire on libxinerama-devel
- Update to the 1.6 branch version
- Drop upstream patches
- Update Fedora patches
- Drop xorgconf related stuff (no longer upstream)
- Add a few upstream patches scheduled to land in 1.6 branch soon.
- Disable more patches. Not 100%% sure if these need migrated in some way

* Mon Dec 22 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.3-8mdv2009.1
+ Revision: 317613
- Revert XTest patch. It caused crashes with input hotplug disabled.

* Thu Dec 18 2008 Frederic Crozat <fcrozat@mandriva.com> 1.5.3-7mdv2009.1
+ Revision: 315701
- Sources 3/4 : install hal callouts to autoconfigure keyboard layout based on /etc/sysconfig/keyboard (idea from Fedora)

* Wed Dec 17 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.5.3-6mdv2009.1
+ Revision: 315299
- Pass XTest fake key event through mieq (should fix bug #36893)

* Tue Dec 16 2008 Colin Guthrie <cguthrie@mandriva.org> 1.5.3-5mdv2009.1
+ Revision: 314983
- Fix compilation with -Werror=format-security (thanks to pcpa for tips)
- Fix gnome-screensaver eating CPU bug with upstream cherry-pick

* Tue Dec 02 2008 Colin Guthrie <cguthrie@mandriva.org> 1.5.3-4mdv2009.1
+ Revision: 309216
- Require evdev if hal/dbus support is enabled (which is currently the case)

* Sat Nov 29 2008 Adam Williamson <awilliamson@mandriva.org> 1.5.3-3mdv2009.1
+ Revision: 308131
- obsolete x11-server-xgl: cleanest way to kill Xgl (finally)

* Sat Nov 29 2008 Colin Guthrie <cguthrie@mandriva.org> 1.5.3-2mdv2009.1
+ Revision: 308045
- Add missing requires to the -devel package (due to header includes)

* Sat Nov 29 2008 Colin Guthrie <cguthrie@mandriva.org> 1.5.3-1mdv2009.1
+ Revision: 308007
- Add missing BuildRequires for libxv-devel
- Add missing BuildRequires for libpciaccess-devel
- Disable xvnc for now until patches are rediffed
- Enable hal/dbus support for input auto-detection
- Add xvfb-run.sh script from fedora (alternative to our previous patch)
- Disable Xfake due to build problems (will try and fix shortly)
- Disable (temporarily) patches that need more than simple rediffs
- Drop patches merged/available upstream
- Adapt patches that no longer apply cleanly but are still desired
- Liberate fedora patches
- Update to 1.5.3
- Copy blue background to the disabled folder for reference. The approach to reenable this is quite different due to the -nr patch from fedora
- Copy some patches that no longer apply to a 'disabled' folder for short term easy reference

* Fri Oct 31 2008 Olivier Blin <blino@mandriva.org> 1.4.2-8mdv2009.1
+ Revision: 298890
- buildrequire openssl-devel for xkbcomp patch
- require newer x11-data-xkbdata (so that user can write in /var/lib/xkb)
- use cache for xkb (rediffed from pcpa's patch), to speed up X start
- fix typo in save context patch

* Mon Aug 25 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-7mdv2009.0
+ Revision: 275956
- Bump release number.
- Solve gtk+ apps crash when server and client have different endianess.
- Obsoletes vesa based kdrive X servers for clean upgrade.

* Fri Aug 22 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-6mdv2009.0
+ Revision: 275122
- Bump release.
- Fix Xvnc crash when run with -depth 16 (mandriva bug #41583)
- Fix X server bug when run wiht Xkb disabled (mandriva bug #41585)

* Mon Aug 11 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-5mdv2009.0
+ Revision: 270862
- Disable vesa based kdrive X servers
- Reverse Xaa offscreen pixmaps logic. To enable, use "XaaOffscreenPixmaps" "on"

  + Anssi Hannula <anssi@mandriva.org>
    - use alternatives for libdri.so as well, next fglrx provides its own
      version

* Mon Jun 23 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-4mdv2009.0
+ Revision: 228396
- Bump release number
- Fix incorrect test

* Mon Jun 23 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-3mdv2009.0
+ Revision: 228391
- Test if important directories are links and report consistent error messages.

* Fri Jun 20 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-2mdv2009.0
+ Revision: 227492
- Increse release number
- Check if /usr/X11R6 is a link. Do not update if it is.

* Thu Jun 19 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.2-1mdv2009.0
+ Revision: 226405
- Do not install if x11-server-common if /etc/X11 or /usr/lib/X11 is a symlink
- * Updated to xorg version 1.4.2
 * Removes {pre,post}trans which created symlinks from /etc/X11 and
   /usr/lib/X11 to /usr/share/X11 and a symlink from /usr/X11R6 to /usr
   (this may cause breakage between cooker upgrades)

* Mon Jun 09 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.4.0.90-21mdv2009.0
+ Revision: 217245
- Fix mandriva bug #37514 (vncserver segfaults when connected)

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Autoconfigure to use geode driver on the known supported hardware.

* Fri May 23 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-20mdv2009.0
+ Revision: 210701
- o Add _disable_ld_no_undefined due to modules that reference X Server,
  libraries linked to the X Server, or other modules symbols.
- o Correct a harmless problem with the .rpmsave magic where, if it did
  not need to move any files, and the directory link already existed,
  it would create a link to the directory inside of the directory, and
  fail to remove it in %%postrans.
  o Create only relative symlinks.
  o Correct #40959 (latest xserver segfaults when mplayer runs)

* Mon May 19 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-19mdv2009.0
+ Revision: 209187
- o Patches regenerated. When git-am fails, something like:
  -%%<-
  $ git-am --skip
  $ git-reset --hard <last-good-commit>
  <hack-patch-file-to-not-apply-to-problematic-file>
  <fix-problematic-file-by-hand>
  $ git-apply <patch-file>
  $ git-commit -a
  Aparently will not work as expected, as the Xvnc patch was incorrectly
  regenerated when running "git-format-patch", but fixed now.
- o Update to latest X Server 1.4 branch.
  o Patch "fix-parsing-weird-EDID" was modified to also include
  "Avoid-an-infinite-loop-at-initialization-if-Preferre"
  o Remade small portion of Xvnc patch that did not apply anymore
  o Use a new schema in x11-server-common to avoid rpm upgrade problems.
  This schema doesn't need external help, like running the %%pre
  of the previous package before actually upgrading packages.
  To avoid rpm removing files it just installed, now the scriplet
  %%pretrans creates a symlink ending in ".rpmsave", and the scriptlet
  %%posttrans corrects the symlink to the proper directory.

* Thu May 15 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-18mdv2009.0
+ Revision: 207659
- Correct a problem in %%pre where it would not properly handle symlinks,
  and cause upgrade problems.

  + Anssi Hannula <anssi@mandriva.org>
    - do not uselessy remove symlinks in pre of common when migrating
      directories to symlinks, symlink => symlink is handled by rpm fine

* Wed May 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-17mdv2009.0
+ Revision: 207244
- o Update to latest git "server-1.4-branch".
  o Update %%pre script to finish moving <basedir>/X11 files to %%{_datadir}/X11.
  The script has been updated to a recursive version because moving relative
  symlinks may leave broken ones.
  o Also change /usr/X11R6 from a real directory to a symlink to /usr.

* Wed May 07 2008 Anssi Hannula <anssi@mandriva.org> 1.4.0.90-16mdv2009.0
+ Revision: 202682
- fix error in %%pre of x11-server-common that caused it to try moving
  symlinks that have already been deleted
- make /usr/X11R6/lib/X11 point directly to /etc/X11
- fix the compatibility modules directory on lib64, the correct path is
  /usr/X11R6/lib64/modules

* Tue May 06 2008 Anssi Hannula <anssi@mandriva.org> 1.4.0.90-15mdv2009.0
+ Revision: 202173
- create destination directory in %%pre of common package when moving
  files to new directory
- do not create symlinks in %%pre of common package, let RPM handle those
- do not try to symlink /usr/X11R6/lib/modules/dri, since
  /usr/X11R6/lib/modules is already a symlink; instead create the dri
  symlink in /usr/lib/xorg/modules
- create absolute symlinks in %%install for clarity and let spec-helper
  make them relative; this also fixes invalid /etc/X11/app-defaults
  symlink

* Tue May 06 2008 Anssi Hannula <anssi@mandriva.org> 1.4.0.90-14mdv2009.0
+ Revision: 201795
- fix versioning of conflicts
- conflict with old libx11-common instead of libx11

* Mon May 05 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-13mdv2009.0
+ Revision: 201576
- Update to latest code in Xorg XServer 1.4 branch.
  Make x11-server-common owner of most configuration directories, and
  properly updated these.

* Mon Apr 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-12mdv2009.0
+ Revision: 193420
- Reenable dmx.
- Remake patches to sync with 1.4 branch.
- Cherry pick 3 new patches that fixes:
   o randr accessing bad memory if used when X Server was not in the active VT.
   o dpms timer not being restarted after it being temporarily disabled.
   o better processInput proc wrapping fix, that should fix all possible
     failure conditions (currently we already had a patch to fix some
     related problems).

* Fri Mar 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-11mdv2008.1
+ Revision: 187971
- Patch 0524 appeared to be not going to cause any problems, but it caused
  enough regressions to not be worth applying. Regressions are cases of
  misconfiguration of monitor refresh rate. Too bad it also appears to have
  fixed problems for some people.

* Tue Mar 11 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-10mdv2008.1
+ Revision: 186957
- Add custom patch to not print warning about this being a pre release
  version. X Server 1.4.1 should have been released long ago, and this is
  the most stable version. No reason to warn users, and this is done by
  all "major" distros.
  Add a few new cherry-picks from git master.
  This is also an oportunity to recompile with the changes to mesa that
  now is now 7.0.3-rc2, and ensure the X Server is compiled with the latest
  mesa-source.

* Wed Mar 05 2008 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4.0.90-9mdv2008.1
+ Revision: 180143
- update Blue-background-custom-patch RGB values to match current
  installer theme (requested by Frederic Crozat).

* Mon Mar 03 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-8mdv2008.1
+ Revision: 178110
- Rebase server-1.4-branch.
  Close Fix crash due to unhandled SIGALRM (#38325).
  This adds some noise to regenerated patches due to update of git version.

* Wed Feb 20 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-7mdv2008.1
+ Revision: 173358
- Update package to match latest X Server 1.4 branch.
  Also in this revision started using a different starting number for
  local patches and "cherry-picks" that should avoid future unnecessary
  patch renames.
  Note that some git master patches were added to 1.4 branch, so order
  of some patches has changed.
- Rebase to origin/server-1.4-branch.
  Cherry-pick commits that fixes #37768 that caused a crash when using the
  evdev driver and changing xkb model/layout with setxkbmap.

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - fix description-line-too-long

* Mon Feb 11 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-6mdv2008.1
+ Revision: 165283
- Fix http://qa.mandriva.com/show_bug.cgi?id=36651
- Review all patches to avoid the risk corrupted patches. Did a reset --hard
  in the previous commit and git-am'ed back custom patches.
  Read change to update keyboard leds, this time on it's own patch.
  Use git-cherry-pick to pull some bug fixes from master.

* Thu Feb 07 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-4mdv2008.1
+ Revision: 163793
- Revert to use latest upstream tarball.
  Revert build requires.
  Add patches to sync tag xorg-server-1.4.0.90 with tip of branch
  server-1.4-branch, and mandriva custom patches on top of it.
  The only large patch kept is the SAVE_CONTEXT patch.

* Mon Feb 04 2008 Pixel <pixel@mandriva.com> 1.4.0.90-3mdv2008.1
+ Revision: 162099
- "fixes" setxkbmap not working in installer (DrakX) (#35912)

* Mon Jan 28 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-2mdv2008.1
+ Revision: 159522
- Again some rework and git-format-patch seens to not scale very well with
  the svn repository due to generating different names, but git-rebase is
  the easiest and most reliable way to keep these patches for the moment.
  Keeping 3 different branches up to date isn't as simple as originally thought...
  This patch adapts all recent security updates to server branch 1.4 (patches
  25 to 31).
  Add a fix for an infinite loop when using the PreferredMode option and
  having 2 or more modes with the same name (patch 15).

* Fri Jan 25 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4.0.90-1mdv2008.1
+ Revision: 158106
- Rebase to xorg-server-1.4.0.90 tag.
  Commands used basically were:
  $ git-checkout mandriva
  $ git-rebase xorg-server-1.4.0.90		# no conflicts
  $ git-checkout mandriva+custom
  $ git-rebase mandriva				# no conflicts
  $ git-checkout mandriva+gpl
  $ git-rebase mandriva+custom			# no conflicts
  Updated git.mandriva.com to match local changes. And spec
  to generate a matching tarball and patches.
  Please don't mdvsys submit it till monday to have some time for
  testings, as this is the first large update, to a different version.

* Thu Jan 24 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4-23mdv2008.1
+ Revision: 157684
- Fix http://qa.mandriva.com/show_bug.cgi?id=35713
  From a0b4b3be94c6f00c71855598c0d46416f3877367 Mon Sep 17 00:00:00 2001
  From: Peter Hutterer <peter@cs.unisa.edu.au>
  Date: Wed, 19 Dec 2007 16:20:36 +1030
  Subject: [PATCH] include: never overwrite realInputProc with enqueueInputProc.
  Bug #13511
  In some cases (triggered by a key repeat during a sync grab) XKB unwrapping
  can overwrite the device's realInputProc with the enqueueInputProc. When the
  grab is released and the events are replayed, we end up in an infinite loop.
  Each event is replayed and in replaying pushed to the end of the queue again.
  This fix is a hack only. It ensures that the realInputProc is never
  overwritten with the enqueueInputProc.
  This fixes Bug #13511 (https://bugs.freedesktop.org/show_bug.cgi?id=13511)
  (cherry picked from commit eace88989c3b65d5c20e9f37ea9b23c7c8e19335)

* Tue Jan 22 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4-22mdv2008.1
+ Revision: 156688
- Export symbol required by wacom input device driver.

  + Ademar de Souza Reis Jr <ademar@mandriva.com.br>
    - re-enable rpm debug packages support

* Mon Jan 21 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4-21mdv2008.1
+ Revision: 155634
- Export symbols used by nouveau driver and fpit input driver.
  These symbols shouldn't really be used, as they are private exa symbols
  and one randr 1.0 symbol kept for binary compatibility.

* Wed Jan 16 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4-20mdv2008.1
+ Revision: 153772
- Add missing symbol found when analyzing recent changes and upgrade to ati
  driver. Missing symbol is required by the i810 driver and was not being
  exported by the X Server code.

* Wed Jan 16 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4-19mdv2008.1
+ Revision: 153677
- Fix compilation on x86_64.
  Reenable build docs.
- Update build requires.
  git-cherry-pick 2338d5c9914e2a43c3a4f7ee0f4355ad0a1ad9e7 to
  fix http://qa.mandriva.com/show_bug.cgi?id=36746
- Fix build due to incorrect patch for pci, reverted and rewritten in git.
  Update BuildRequires based on x-check-rpm-deps.pl output, and kept
  BuildRequires not listed as they can be required only link or as some
  binary to process some file.

  + Colin Guthrie <cguthrie@mandriva.org>
    - Update buildrequires to be architecture independent (i.e. for x86_64)

* Wed Jan 09 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.4-18mdv2008.1
+ Revision: 147323
- Disable debug package for the moment.
  Fix problem with binary nvidia driver.
  Fix problem with symbols accessed using LoaderSymbol/dlsym in pci code
  Fix some other symbols  accessed using LoaderSymbol/dlsym by the vnc patch code
- Don't install .la files in -devel and don't generate .deps files. .la
  files should not be installed anymore and .deps should be handled externally,
  instead of adding them to packages.
- Move all .la files to -devel.
  Require proper version of x11-util-macros.
  Add patch to fix issue with bugzilla #34879 (log is wrong, 8587 is attachment
  id...)
- Update to use tag xorg-server-1.4 and add all patches in server 1.4 branch
  as well as Mandriva specific ones in mandriva branch.
- First version of X Server compiled with most symbols hidden.
  Symbols used by all modules in the distro are exported.
  This patch also stores old patches in the git repository, and uses
  git-archive to generate the tarball and git-format-patch to extract patches
  from the branches:
  	mandriva		: should be safe to apply upstream
  	mandriva+custom		: either distro specific or experimental code
  	mandriva+gpl		: no restriction to gpl licensed code

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 28 2007 Paulo Andrade <pcpa@mandriva.com.br> 1.4-17mdv2008.1
+ Revision: 113710
- Minor updates. Also, at least for now, disable config-hal.

* Fri Nov 23 2007 David Walluck <walluck@mandriva.org> 1.4-15mdv2008.1
+ Revision: 111699
- enable xvnc (needed by tightvnc)

  + Ademar de Souza Reis Jr <ademar@mandriva.com.br>
    - pass --enable-config-hal to configure, to enable
      support for hal (input-hotplug) explicitly.

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Patch to fix a crash in the "expert mode" xorgcfg interface if the config files
      doesn't hava a Files Section.

* Mon Nov 19 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-14mdv2008.1
+ Revision: 110213
- new snapshot of the 1.4-branch git patch
- drop fix-keyboard-events.patch and fix-keyboard-events2.patch
  (already on the branch)
- add build-requirements for hal and dbus devel, so that
  input-hotplug is enabled in our official builds
  (thanks Andrey Borzenkov for pointing this)

* Wed Nov 14 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-13mdv2008.1
+ Revision: 108712
- adding one more patch for keyboard events, fix for upstream bugs:
  #13223 (server 1.4.1: Input Events Duplicated Across Different Windows)
  and #13114 (xserver-1.4 keyboard repeat rate strange behavior)

* Tue Nov 13 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-12mdv2008.1
+ Revision: 108494
- update 1.4 git branch patch (minor fix on XEphyr)
- disable debug (was enabled by accident in a previous commit)

* Mon Nov 12 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-11mdv2008.1
+ Revision: 108261
- update git patch (from 1.4.1 branch)
- add keyboard-events patch (upstream bug #12858)

* Tue Nov 06 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-10mdv2008.1
+ Revision: 106559
- remove more obsolete patches from old xserver package:
  o Xephyr-evdev-support.txt: feature already upstream;
  o 64bit_fixes.patch: code partially removed and changed
    upstream and patch not documented anywhere;
  o Fix-index-matching-of-visuals.txt: fixed upstream
    in a different way
- enabled xvnc again (patch appears to be OK now)
- minor spec cleanup: remove dead (commented-out) fields

* Tue Nov 06 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-9mdv2008.1
+ Revision: 106533
- add git-branch-fixes-<date>.patch, with the fixes
  from the 1.4 branch on upstream git.
- minor fix on save-context.patch so that it applies
  on top of the new code;
- minor cosmetic spec change

* Tue Nov 06 2007 Funda Wang <fwang@mandriva.org> 1.4-8mdv2008.1
+ Revision: 106460
- rebuild for new lzma

* Tue Oct 30 2007 Paulo Andrade <pcpa@mandriva.com.br> 1.4-7mdv2008.1
+ Revision: 103858
- Only bitmaps/pixmaps generated are the ones used by xorgcfg, still keep
  x11-devel as owner of images directories.
- Err, use global Xserver flag, pDev would need to be cast to another data type
  used only by de input module.
- Fix wrong patch (edited by hand patch).
- Update keyboard-led patch for proper Xkb extension handling.
  Move xorgcfg bitmaps/pixmaps from x11-server-devel to x11-server-common as
  the xorgcfg program isn in the common package.
- Update keyboard leds. Still not submitting because I believe Scroll_Lock
  behaviour should be better i.e. use the led. But this patch should cause it
  to work like previous Xorg servers regarding to keyboard leds.
  The problem was that mieq.c:mieqProcessInputEvents() calls
  dix/getevents.c:SwitchCoreKeyboard() switching the core keyboard to the keyboard
  associated with the event, but the xkb feedback data structure is pointing to
  a fallback initial function in the "virtual core keyboard" structure. To fix
  the problem I wrapped the fallback function, but could also update the "virtual
  core keyboard" at dix/gevents.c, but that would mean changing xkb internal
  data structures...

  + Colin Guthrie <cguthrie@mandriva.org>
    -Fix Xvnc build
    -Fix vnc module on x86_64

* Fri Oct 19 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-6mdv2008.1
+ Revision: 100507
- disable xvnc by now, the compilation is broken
  because it uses headers installed on the system
  instead of the ones from the build tree
- removed glXDRIbindTexImage-target.txt. It was considered
  fixed upstream with a different approach (see #8991 on
  fd.o bugzilla).
- ported some more patches from our xserver-1.3:
  . blue-background.patch
  . search-best-DPI-using-also-width.patch
- Added preferred-mode-override-monitor-pre.patch
  (patch from git that gives priority to modes declared
  in xorg.conf, substitutes old patches which were removed:
  . randr12-config-hack.patch
  . fix-deadloop-using-PreferredMode.patch)
- fix blue-background.patch

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Add initial support for an attempt to crash recovery the X server when
      a failure happens.
      Basically keyboard events are handled using SIGIO, and Ctrl+Alt+Backspace
      can be used to exit an inifinite loop anywhere (provided sigio is not blockedt),
      and if main code is processing a client request, try to kill the client,
      otherwise terminate the server.
      Same is done when a crash happens, first try to kill client if processing a
      request, otherwise try to exit cleanly, i.e. running all cleanup routines.
      Also add a few fix for clear bugs, and fix some crashes found while debugging
      this code.

  + Colin Guthrie <cguthrie@mandriva.org>
    - Reenable vnc support

* Wed Oct 17 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-4mdv2008.1
+ Revision: 99779
- err, disable blue-background.patch, it's still not
  working. :(
- ported blue-background.patch to xserver 1.4
- removing patches for problems already fixed upstream:
  . add-needed-quirk-for-Samsung-225BW-like.patch
  . cursor-and-randr-fixes.patch

* Wed Oct 17 2007 Anssi Hannula <anssi@mandriva.org> 1.4-3mdv2008.1
+ Revision: 99605
- readd ghost filelist entry for libglx.so so that users do not get
  empty libglx.so

* Tue Oct 16 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-2mdv2008.1
+ Revision: 99077
- x11-server-devel requires libpixman-1-devel

* Thu Oct 11 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.4-1mdv2008.1
+ Revision: 97207
- new upstream version: 1.4 (notice this package is a
  work-in-progress, the upgrade scenario is complex)
- removed all patches which have already been applied
- ported xvfb-run and fontpath_d patches
- disabled DMX by now (compilation is broken)
- disabled VNC (major patch, no 1.4 version yet)
- added some version to build-requirements (may be still incomplete)
- enabled xfake explicitly (it's now disabled by default)
- minor spec cleanup

* Mon Oct 01 2007 Pixel <pixel@mandriva.com> 1.3.0.0-24mdv2008.0
+ Revision: 94119
- remake pcpa's patch to avoid an infinite list, simply taking first matching mode

* Sat Sep 29 2007 Paulo Andrade <pcpa@mandriva.com.br> 1.3.0.0-23mdv2008.0
+ Revision: 93811
- Remake Pixel's patch to avoid an infinite loop, but instead of trying to handle
  duplicate modes, just use the first on the list.
  This fix several problems in intel based cards, and doesn't require any changes
  to xorg.conf, and allow using the PreferredMode option, that is an alternative
  to Patch54: xserver-1.3.0-randr12-config-hack.patch. But this change should make
  it possible to keep using Patch54 without any problems.

* Tue Sep 25 2007 Pixel <pixel@mandriva.com> 1.3.0.0-22mdv2008.0
+ Revision: 92850
- add patch from Fedora that ensures backward compatibility with previous Xorg
  behaviour: prefered mode is the first Modes in Subsection "Display"
- fix deadloop occurring if preferred resolution matches more than one mode

* Fri Sep 21 2007 Pixel <pixel@mandriva.com> 1.3.0.0-21mdv2008.0
+ Revision: 91759
- drop patch128 ("Possible fix for bugzilla #31183"),
  otherwise it crashes on at least ati, openchrome, vesa, fglrx

* Thu Sep 20 2007 Pixel <pixel@mandriva.com> 1.3.0.0-20mdv2008.0
+ Revision: 91573
- fix parsing weird EDID (fixes intel driver defaulting to smallest resolution) (#31183)
- take into account screen width when looking for prefered resolution instead of
  only using screen height (helps choosing 1024x768 instead of the weird 1152x768)

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Don't compile unoptmized and with debug code by default.
    - Possible fix for bugzilla #31183, that should not interfere, and work with
      other drivers that may have the same problem

* Mon Sep 17 2007 Paulo Andrade <pcpa@mandriva.com.br> 1.3.0.0-19mdv2008.0
+ Revision: 89337
- Fix last patch that broke build. Use underline character to replace space in
  string of build operating system and fix double quotes.
- Better description in /var/log/Xorg.X.log than:
  Build Operating System: UNKNOWN
- Until Xorg Bugzilla #12414 receives any response, this patch fixes the problem
  with a hack that tries to make sure CreatePixmap is allways properly wrapped,
  i.e. all extensions know about it.
- Fix what appears to be a serious off by one bug. After this patch opengl apps
  works under Xnest (but very slowly), so it should also fix the bug of remote GL
  apps crashing the Xserver (Bugzilla #27397). It is clearly poorly checked code,
  as it was even checking if an unsigned variable is greater than or equal to 0.
- Modify XOrgCfg resources file to only require fixed fonts.
  For the moment still requiring x11-data-bitmaps, but those can be removed if it
  is undesirable to install that package also.
- Add requires to xorgcfg so that missing bitmaps and/or fonts should
  not cause problems.
- Fixes bug #31211 by not starting/enabling MouseKeys support (neither showing the
  dialog with help screen). Maybe a better fix would be to still show the help
  screen, but instead of enabling it, tell the user how to enable/disable (i.e.
  pressing Shift+Num_Lock).

  + Ademar de Souza Reis Jr <ademar@mandriva.com.br>
    - add security fix for CVE-2007-4730 (xorg-git-CVE-2007-4730.patch)
      Closes: #33479
    - remove 0033-dont-backfill-bg-none patch, which is incompatible with the
      fix for CVE-2007-4730 (there's no history for this patch, but odds are
      it's a workaround for the very same problem fixed as a security problem.
      Anyway, the code in question was reviewed and tested as part of the
      security audit, so our guess is that our old patch is unecessary).

  + Anssi Hannula <anssi@mandriva.org>
    - own /usr/lib(64)/xorg/modules/input,drivers

* Sun Aug 26 2007 Anssi Hannula <anssi@mandriva.org> 1.3.0.0-17mdv2008.0
+ Revision: 71692
- use alternatives for libglx.so

* Tue Aug 21 2007 Colin Guthrie <cguthrie@mandriva.org> 1.3.0.0-16mdv2008.0
+ Revision: 68152
- Rediff Xvnc patch from xserver 1.2 and reenable (#32578)

  + Thierry Vignaud <tv@mandriva.org>
    - fix man pages extension

* Mon Aug 13 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.3.0.0-15mdv2008.0
+ Revision: 62706
- do not crash on VT switching when the Xv adaptor is active (#32328)

* Fri Aug 10 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.3.0.0-14mdv2008.0
+ Revision: 61432
- Backported many randr 1.2 fixes and additions from xserver git
- Removed the multiple randr 1.2 fixes patch and re-add the fixes
  as git-cherry-picked patches

* Fri Aug 03 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.3.0.0-13mdv2008.0
+ Revision: 58655
- Fix the patch, which was wrongly regenerated including changes from Paulo's
  patch
- Remove obsolete randr1.2 patches
- Add two new patches that fixes the problem and eliminates the side-effects
  previously seen (crashes)

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Fix crash with VT switch and access of unalocated cursor memory

* Tue Jul 31 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.3.0.0-12mdv2008.0
+ Revision: 57097
- Disable the randr1.2 fixes for now, as they cause a undesirable side-effect
  which still should have to be figured out

* Tue Jul 24 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.3.0.0-11mdv2008.0
+ Revision: 55078
- Fix the output->crtc initialization in the old randr setup

* Mon Jul 23 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.3.0.0-10mdv2008.0
+ Revision: 54868
- Fix the randr output change notifying problem in another way (as suggested by
  Keith Packard)
- Remove manpage extensions
- Fix randr1.2 output changing notification

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.3.0.0-9mdv2008.0
+ Revision: 48627
- change default fontpath to fontpath.d, xfs is now
  deprecated.
  (there are some fonts which are not included in
  fontpath.d yet, see #31756)

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.3.0.0-8mdv2008.0
+ Revision: 48312
- proper cleanup/fix for handling of the legacy X11R6 directory.
  There are scenarios where both /usr/X11R6/lib/X11 and
  /usr/lib/X11 exist. Since the legacy files/dirs were owned by an
  ancient version of the filesystem package, we don't need a
  trigger, all we need is a %%post with the necessary changes and a
  conflict. Fix: #23423 and #31737

* Mon Jul 02 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.3.0.0-7mdv2008.0
+ Revision: 47202
- Add legacy X11R6 directory structure to x11-server-common
  (still needed by some closed-source applications)
- Require filesystem >= 2.1.8 (when the X11R6 directory structure
  was changed)

* Fri Jun 22 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.3.0.0-6mdv2008.0
+ Revision: 43202
- added patch that documents fontpath.d support

* Fri Jun 15 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.3.0.0-5mdv2008.0
+ Revision: 40081
- improve autotools calls, fixing build on x86_64
  which was b0rken after the latest autoconf update.
- add dirs /etc/X11 and /etc/X11/app-defaults to
  x11-server-common

* Fri Jun 08 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.3.0.0-4mdv2008.0
+ Revision: 37587
- Rebuild with libslang2.

* Tue May 22 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.3.0.0-3mdv2008.0
+ Revision: 29855
- disable xprint server support. It was never functional before and
  is not much useful nowadays anyway. User's can still play with it by
  downloading functional packages from the project website.

* Fri May 04 2007 Colin Guthrie <cguthrie@mandriva.org> 1.3.0.0-2mdv2008.0
+ Revision: 22447
- Add hard build requirement for Mesa 6.5.3
- Apply patches to work with Mesa 6.5.3.

* Fri Apr 20 2007 Colin Guthrie <cguthrie@mandriva.org> 1.3.0.0-1mdv2008.0
+ Revision: 15618
- New Release 1.3.0.0
- Obsolete latest x11-server13 package

* Thu Apr 19 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.2.99.905-1mdv2008.0
+ Revision: 15184
- new upstream RC release: 1.2.99.905 (1.3 RC4)
  The main highlight is the RandR 1.2 support (that was being experimentally
  used in the x11-server13 package).
- Obsoleted some patches that were either not needed or applied upstream
- The vnc patch is broken again. Disable support by now.

* Thu Apr 19 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.2.0-10mdv2008.0
+ Revision: 14961
- Fixed a crash of the server when setting a pixmap for the root window and
  later trying to restore the defaults. Thanks Frederic Crozat for the report.

