%define git 0

%define with_debug 0
%define enable_dmx 1
%define enable_kdrive 0
%define enable_xfake 1
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

%define rel 7.1

# ABI versions.  Have to keep these manually in sync with the source
# because rpm is a terrible language.  HTFU.
%define ansic_major 0
%define ansic_minor 4
%define videodrv_major 19
%define videodrv_minor 0
%define xinput_major 21
%define xinput_minor 0
%define extension_major 9
%define extension_minor 0

Name:		x11-server
Version:	1.17.1
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
Source7:	90-zap.conf
Source8:	50-synaptics.conf
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
BuildConflicts:	systemtap
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(pixman-1) >= 0.9.5
BuildRequires:	pkgconfig(xau) >= 1.0.0
BuildRequires:	pkgconfig(xaw7) >= 1.0.1
BuildRequires:	pkgconfig(xdmcp) >= 1.0.0
BuildRequires:	pkgconfig(xext) >= 1.1
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xfont) >= 1.2.8-2mdv
BuildRequires:	pkgconfig(xi) >= 1.1.3
BuildRequires:	pkgconfig(xkbfile) >= 1.0.4
BuildRequires:	pkgconfig(xmu) >= 1.0.0
BuildRequires:	pkgconfig(xpm) >= 3.5.4.2
BuildRequires:	pkgconfig(xrender) >= 0.9.4
BuildRequires:	pkgconfig(xres) >= 1.0.0
BuildRequires:	pkgconfig(xshmfence) >= 1.1
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-aux)
BuildRequires:	pkgconfig(xcb-icccm)
BuildRequires:	pkgconfig(xcb-image)
BuildRequires:	pkgconfig(xcb-shape)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-xv)
BuildRequires:	pkgconfig(xcb-renderutil)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(xcb-glx)
BuildRequires:	pkgconfig(xcb-xf86dri) > 1.6
BuildRequires:	x11-font-util >= 1.1
BuildRequires:	x11-proto-devel >= 7.6-4
BuildRequires:	x11-util-macros >= 1.15
BuildRequires:	x11-xtrans-devel >= 1.2.7-2

# Probably only needed if we change .l or .y files, but let's have them anyway:
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	bison

BuildRequires:	openssl-devel
BuildRequires:	pkgconfig(libudev) >= 186

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
BuildRequires:	pkgconfig(glib-2.0)
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
#Patch908:	0908-XKB-cache-xkbcomp-output-for-fast-start-up-v.1-for-1.patch
Patch910:	xorg-1.13.0-link-tirpc.patch
Patch911:	xorg-server-1.16.0-blacklist-driver.patch
Patch912:	xorg-server-1.17-fix-i386-asm-for-clang.patch

# Other patches

# Do not crash if Xv is not initialized (patch from xorg-devel ML)
# The crash happened when v4l was loaded and xv was not registered,
# for example on RV610 with radeon driver
Patch1001:	1001-do-not-crash-if-xv-not-initialized.patch
Patch1002:	xorg-server-1.17.1-add-missing-library-links.patch

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
Obsoletes:	libglamor-devel < 0.6.0-10

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
Requires:	udev
Requires:	mkcomposecache
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
Obsoletes:	%{_lib}glamor0 <= 0.6.0-10

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
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/90-zap.conf
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/50-synaptics.conf
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%{_sysconfdir}/ld.so.conf.d/GL/standard.conf
%{_bindir}/gtf
%{_bindir}/cvt
/sbin/mandriva-setup-keyboard
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
%{_mandir}/man4/modesetting.4.*
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
Requires:	x11-driver-input-evdev
Requires:	udev
Conflicts:	drakx-kbd-mouse-x11 < 0.66
Conflicts:	compiz < 0.5.0-1mdv2007.1
Obsoletes:	x11-server13-xorg <= 1.2.99.905

# minimum libxfont needed for xserver-1.9:
Requires:	libxfont >= 1.4.2

# This package was used in the transition to modular:
Obsoletes:	xorg-x11-server
Conflicts:	x11-driver-video-modesetting <= 0.9.0-4
%rename		x11-driver-video-modesetting

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
%{_datadir}/X11/xorg.conf.d/10-evdev.conf
%{_datadir}/X11/xorg.conf.d/10-quirks.conf

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

%package xwayland
Summary:	A X server for Wayland
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{EVRD}

%description xwayland
Wayland is a complete window system in itself, but even so, if we're migrating
away from X, it makes sense to have a good backwards compatibility story. With
a few changes, the Xorg server can be modified to use wayland input devices for
input and forward either the root window or individual top-level windows as
wayland surfaces. The server still runs the same 2D driver with the same
acceleration code as it does when it runs natively. The main difference is that
wayland handles presentation of the windows instead of KMS. 

%files xwayland
%{_bindir}/Xwayland

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
autoreconf -if

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
%serverbuild_hardened


# Copy the clean dir to a 'source' directory that will be used to make the
# x11-server-source subpackage
mkdir -p source
find . -maxdepth 1 ! -name source ! -name '\.' -exec cp -r '{}' source \;


%if %{with_debug}
CFLAGS='-DBUILDDEBUG -O0 -g3' \
%endif
CC=gcc CXX=g++ %configure \
	--with-log-dir=%{_logdir} \
	--with-builder-addr="www.openmandriva.org" \
	--with-vendor-name="%{vendor}" \
	--with-os-vendor="%{vendor}" \
	--with-os-name="`echo \`uname -s -r\` | sed -e s'/ /_/g'`" \
	--with-vendor-web="%{bugurl}" \
	--with-extra-module-dir=%{extra_module_dir} \
	%if %{with_debug}
	--enable-debug \
	%else
	--disable-debug \
	%endif
	--enable-config-udev \
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
	--enable-dri2 \
	--enable-dri3 \
	--enable-glamor \
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
	--disable-config-hal \
	--with-sha1=libcrypto \
	--enable-xwayland \
	--with-systemd-daemon \
	--with-default-font-path="catalogue:%{_sysconfdir}/X11/fontpath.d"

pushd include && make xorg-server.h dix-config.h xorg-config.h && popd

%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/X11/
ln -s %{_bindir}/Xorg %{buildroot}%{_sysconfdir}/X11/X
ln -sf %{_bindir}/Xwrapper %{buildroot}%{_bindir}/X

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/xserver
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

install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/xvfb-run

mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}/lib/udev/rules.d/
install -m 0755 %{SOURCE5} %{buildroot}/sbin/mandriva-setup-keyboard
# (tpg) do not install this as running mandriva-setup-keyboard 
# with systemd configuration before X start produces keyboard layout issues
# https://issues.openmandriva.org/show_bug.cgi?id=274
#install -m 0644 %{SOURCE6} %{buildroot}/lib/udev/rules.d

# Make the source package
cp -r source %{buildroot}/%{xserver_source_dir}

install -m 755 %{SOURCE30} %{buildroot}%{_bindir}

# Create xorg.conf.d
install -d -m 755 %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

# And enable Ctrl+Alt+Backspace by default
install -c -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/

# Add synaptics configuration
install -c -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/

%files
