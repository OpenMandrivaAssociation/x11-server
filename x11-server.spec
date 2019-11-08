%define git 0

%global optflags %{optflags} -O3

%define with_debug 0
%define enable_dmx 1
%define enable_kdrive 0
%define enable_builddocs 0
# /usr/lib/rpm/brp-python-bytecompile /usr/bin/python 1
# Error compiling '/builddir/build/BUILDROOT/x11-server-1.20.0-1.x86_64/usr/share/x11-server-source/config/fdi2iclass.py'...
#  File "/fdi2iclass.py", line 169
#    print 'Section "InputClass"'
%define _python_bytecompile_build 0
%define _python_bytecompile_errors_terminate_build 0

# Do magic with .rpmsave named links
%define pre_post_trans 1

# Need this for shared objects that reference X Server, or other modules symbols
%define _disable_ld_no_undefined 1

# Alternatives priority for standard libglx.so and mesa libs
%define priority 500

%define moduledir %{_libdir}/xorg/modules

# ABI versions.  Have to keep these manually in sync with the source
# because rpm is a terrible language.  HTFU.
%define ansic_major 0
%define ansic_minor 4
%define videodrv_major 24
%define videodrv_minor 0
%define xinput_major 24
%define xinput_minor 1
%define extension_major 10
%define extension_minor 0

Name:		x11-server
Version:	1.20.5
%if %{git}
Release:	0.%{git}.1
%else
Release:	6
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
# for finding & loading nvidia and flgrx drivers:
Source3:	00-modules.conf
Source4:	10-quirks.conf
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

Obsoletes:	%{name}-xfake < %{version}-%{release}

# FIXME: build with systemtap installed is broken
BuildConflicts:	systemtap
BuildRequires:	pkgconfig(dbus-1)
%ifarch %{ix86} %{x86_64}
BuildRequires:	pkgconfig(libunwind)
%endif
BuildRequires:	pkgconfig(gl)
BuildRequires:	pam-devel
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	pkgconfig(nettle)
BuildRequires:	pkgconfig(xkbcomp)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(xau) >= 1.0.0
BuildRequires:	pkgconfig(xaw7) >= 1.0.1
BuildRequires:	pkgconfig(xdmcp) >= 1.0.0
BuildRequires:	pkgconfig(xext) >= 1.1
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xfont) >= 1.5.2
BuildRequires:	pkgconfig(xfont2)
BuildRequires:	pkgconfig(xi) >= 1.1.3
BuildRequires:	pkgconfig(xkbfile) >= 1.0.4
BuildRequires:	pkgconfig(xmu) >= 1.0.0
BuildRequires:	pkgconfig(xpm) >= 3.5.4.2
BuildRequires:	pkgconfig(xrender) >= 0.9.4
BuildRequires:	pkgconfig(xres) >= 1.0.0
BuildRequires:	pkgconfig(xshmfence) >= 1.1
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-protocols) >= 1.14
BuildRequires:	pkgconfig(wayland-eglstream-protocols) >= 1.0.3
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
BuildRequires:	x11-proto-devel >= 2018.4
BuildRequires:	x11-util-macros >= 1.19.2
BuildRequires:	x11-xtrans-devel >= 1.3.5

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
BuildRequires:  hostname

Patch100:	xorg-server-1.20.4-det_mon-size.patch
Patch101:	http://cgit.openembedded.org/openembedded-core/plain/meta/recipes-graphics/xorg-xserver/xserver-xorg/0001-test-xtest-Initialize-array-with-braces.patch
Patch102:	xorg-server-1.20.5-fix-meson-xkb_output_dir.patch

# Fedora Patches
# From Debian use intel ddx driver only for gen4 and older chipsets
Patch7022:	06_use-intel-only-on-pre-gen4.diff
# Default to xf86-video-modesetting on GeForce 8 and newer
Patch7023:	0001-xfree86-use-modesetting-driver-by-default-on-GeForce.patch
# Default to va_gl on intel i965 as we use the modesetting drv there
# va_gl should probably just be the default everywhere ?
Patch7024:	0001-xf86-dri2-Use-va_gl-as-vdpau_driver-for-Intel-i965-G.patch
Patch7025:	0001-Always-install-vbe-and-int10-sdk-headers.patch
Patch7026:	0001-Xi-return-AlreadyGrabbed-for-key-grabs-255.patch

# do not upstream - do not even use here yet
Patch7027:	0001-autobind-GPUs-to-the-screen.patch
Patch7030:	0002-modesetting-Propagate-more-failure-in-drmmode_set_mo.patch
Patch7031:	0003-modesetting-Factor-out-drmmode_target_output.patch
Patch7032:	0004-modesetting-Use-atomic-instead-of-per-crtc-walks-whe.patch
Patch7033:	0001-xwayland-Avoid-a-crash-on-pointer-enter-with-a-grab.patch
Patch7034:	0001-xwayland-Check-status-in-GBM-pixmap-creation.patch
Patch7035:	0001-glamor-Make-pixmap-exportable-from-gbm_bo_from_pixma.patch
Patch7036:	0001-xwayland-Reset-scheduled-frames-after-hiding-tablet-.patch
Patch7037:	0001-Revert-present-scmd-Check-that-the-flip-and-screen-p.patch
Patch7038:	0001-compiler.h-Do-not-include-sys-io.h-on-ARM-with-glibc.patch

Patch7039:	0001-Xi-Use-current-device-active-grab-to-deliver-touch-e.patch
Patch7040:	0002-dri2-Sync-i965_pci_ids.h-from-mesa.patch
Patch7041:	0003-xwayland-Update-screen-pixmap-on-output-resize.patch
Patch7042:	0004-xwayland-Expand-the-RANDR-screen-size-limits.patch
# https://bugzilla.redhat.com/1729925
Patch7043:	0005-xwayland-Do-not-free-a-NULL-GBM-bo.patch
Patch7044:	0006-xsync-Add-resource-inside-of-SyncCreate-export-SyncC.patch
Patch7045:	0007-GLX-Add-a-per-client-vendor-mapping.patch
Patch7046:	0008-GLX-Use-the-sending-client-for-looking-up-XID-s.patch
Patch7047:	0009-GLX-Add-a-function-to-change-a-clients-vendor-list.patch
Patch7048:	0010-GLX-Set-GlxServerExports-major-minor-Version.patch
Patch7049:	0011-miext-sync-Fix-needless-ABI-change.patch
Patch7050:	0012-glx-Fix-previous-context-validation-in-xorgGlxMakeCu.patch
Patch7051:	0013-xwayland-Separate-DamagePtr-into-separate-window-dat.patch
Patch7052:	0014-xwayland-Refactor-surface-creation-into-a-separate-f.patch
Patch7053:	0015-xwayland-Handle-the-case-of-windows-being-realized-b.patch
# Backported Xwayland randr resolution change emulation support
Patch7054:	0001-dix-Add-GetCurrentClient-helper.patch
Patch7055:	0002-xwayland-Add-wp_viewport-wayland-extension-support.patch
Patch7056:	0003-xwayland-Use-buffer_damage-instead-of-surface-damage.patch
Patch7057:	0004-xwayland-Add-fake-output-modes-to-xrandr-output-mode.patch
Patch7058:	0005-xwayland-Use-RandR-1.2-interface-rev-2.patch
Patch7059:	0006-xwayland-Add-per-client-private-data.patch
Patch7060:	0007-xwayland-Add-support-for-storing-per-client-per-outp.patch
Patch7061:	0008-xwayland-Add-support-for-randr-resolution-change-emu.patch
Patch7062:	0009-xwayland-Add-xwlRRModeToDisplayMode-helper-function.patch
Patch7063:	0010-xwayland-Add-xwlVidModeGetCurrentRRMode-helper-to-th.patch
Patch7064:	0011-xwayland-Add-vidmode-mode-changing-emulation-support.patch
Patch7065:	0012-xwayland-xwl_window_should_enable_viewport-Add-extra.patch
Patch7066:	0013-xwayland-Set-_XWAYLAND_RANDR_EMU_MONITOR_RECTS-prope.patch
Patch7067:	0014-xwayland-Fix-emulated-modes-not-being-removed-when-s.patch
Patch7068:	0015-xwayland-Call-xwl_window_check_resolution_change_emu.patch
Patch7069:	0016-xwayland-Fix-setting-of-_XWAYLAND_RANDR_EMU_MONITOR_.patch
Patch7070:	0017-xwayland-Remove-unnecessary-xwl_window_is_toplevel-c.patch
# Fix building with new libglvnd-1.2.0 (E)GL headers and pkgconfig files
Patch7071:	0001-build-glx-Lower-gl-version-to-work-with-libglvnd.patch
Patch7072:	0001-glamor-xwayland-Define-EGL_NO_X11.patch

# because the display-managers are not ready yet, do not upstream
Patch10000:	0001-Fedora-hack-Make-the-suid-root-wrapper-always-start-.patch

# OpenMandriva/Mageia patches
# git format-patch --start-number 900 mdv-1.6.4-redhat..mdv-1.6.4-patches
Patch900:	0900-Use-a-X-wrapper-that-uses-pam-and-consolehelper-to-g.patch
Patch901:	0901-Don-t-print-information-about-X-Server-being-a-pre-r.patch
Patch902:	0902-Take-width-into-account-when-choosing-default-mode.patch
Patch903:	0903-LED-behavior-fixes.patch
Patch906:	0906-xfree86-need-to-press-Ctrl-Alt-Bksp-twice-to-termina.patch
Patch907:	0907-Add-nr-argument-for-backwards-compatibility.patch
Patch910:	xorg-1.13.0-link-tirpc.patch
Patch911:	xorg-server-1.16.0-blacklist-driver.patch

# Candidates for dropping:
# 902: by pixel, so that X11 choose the best resolution with a better algorithm
# 903: Input subsystem has changed *a lot* since this patch was written... I
#      fear it might break things now
# 906: All this patch does is force users to hit ctrl+alt+bksp twice (with
#      an annoying sound) IF the hotkey is enabled. If the user chooses to
#      enable ctrk+alt+bksp, why force him to hit twice? OTOH, the sound is
#      annoying, and it should teach users to not use ctrl+alt+bksp =D

# Do not crash if Xv is not initialized (patch from xorg-devel ML)
# The crash happened when v4l was loaded and xv was not registered,
# for example on RV610 with radeon driver
Patch4001:	1001-do-not-crash-if-xv-not-initialized.patch

# (cg) Point the user at the journal rather than a logfile at /dev/null
Patch5001:	point-user-at-journal-rather-than-dev-null.patch
Patch5002:	xorg-server-1.20.2-bug95301.patch

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
Requires:	pkgconfig(pixman-1)
Requires:	libpciaccess-devel
Requires:	libxkbfile-devel
Requires:	libxext-devel >= 1.1
Requires:	pkgconfig(dri)
Requires:	pkgconfig(xfont2)
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
Requires(post):	chkconfig >= 1.9.0
Requires(postun):	chkconfig
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
Obsoletes:	x11-driver-video-modesetting < 2:0.9.1
Provides:	x11-driver-video-modesetting = 2:0.9.1

Provides:	xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides:	xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides:	xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides:	xserver-abi(extension-%{extension_major}) = %{extension_minor}

%description common
X server common files.

%post common
%{_sbindir}/update-alternatives \
	--install %{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf %{priority}

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
%{_prefix}/X11R6/lib/X11

#------------------------------------------------------------------------------

%package xorg
Summary:	X.org X11 server
Group:		System/X11
License:	MIT
Requires:	x11-server-common = %{version}-%{release}
Requires:	x11-data-xkbdata > 1.3-5
Requires:	x11-font-alias
Requires:	libx11-common
Requires:	x11-driver-input-libinput >= 0.17.0
Requires:	udev
Conflicts:	drakx-kbd-mouse-x11 < 0.66
Conflicts:	compiz < 0.5.0-1mdv2007.1
Obsoletes:	x11-server13-xorg <= 1.2.99.905
Requires:	dri-drivers
# minimum libxfont needed for xserver-1.9:
Requires:	libxfont >= 1.4.2

# This package was used in the transition to modular:
Obsoletes:	xorg-x11-server

%description xorg
x11-server-xorg is the new generation of X server from X.Org.

%files xorg
%{_bindir}/X
%{_bindir}/Xorg
%{_libexecdir}/Xorg
%attr(4755,root,root)%{_libexecdir}/Xorg.wrap
%{_sysconfdir}/X11/X
%{_sysconfdir}/pam.d/xserver
%{_sysconfdir}/security/console.apps/xserver
%{_mandir}/man1/Xorg.*
%{_mandir}/man1/Xserver.*
%{_mandir}/man5/xorg.conf.*
%{_mandir}/man5/Xwrapper.config.*
%{_datadir}/X11/xorg.conf.d/10-quirks.conf
%{_datadir}/X11/xorg.conf.d/00-modules.conf
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
Requires:	dri-drivers

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

%define xserver_source_dir %{_datadir}/%{name}-source

%package source
Summary:	Xserver source code required to build unofficial servers
Group:		Development/X11
License:	MIT
BuildArch:     noarch

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
%autopatch -p1

# check the ABI in the source against what we expect.
getmajor() {
   grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
   tr '(),' '   ' | awk '{ print $4 }'
}

getminor() {
   grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
   tr '(),' '   ' | awk '{ print $5 }'
}

test $(getmajor ansic) == %{ansic_major}
test $(getminor ansic) == %{ansic_minor}
test $(getmajor videodrv) == %{videodrv_major}
test $(getminor videodrv) == %{videodrv_minor}
test $(getmajor xinput) == %{xinput_major}
test $(getminor xinput) == %{xinput_minor}
test $(getmajor extension) == %{extension_major}
test $(getminor extension) == %{extension_minor}

%build
%meson \
	-Dlog_dir="%{_logdir}" \
	-Dmodule_dir="%{moduledir}" \
	-Dbuilder_addr="%{disturl}" \
	-Dbuilder_string="Build ID: %{name} %{version}-%{release}" \
	-Dvendor_name="%{vendor}" \
	-Dos_vendor="%{vendor}" \
	-Dxorg=true \
	-Dsuid_wrapper=true \
	-Dxephyr=true \
	%ifnarch %{ix86} %{x86_64}
	-Dvbe=false \
	-Dint10=false \
	%else
	-Dint10=x86emu \
	%endif
	-Dvendor_web="%{bugurl}" \
	%if %enable_dmx
	-Ddmx=true \
	%endif
	-Ddefault_font_path="catalogue:%{_sysconfdir}/X11/fontpath.d,built-ins"
	
#pushd include && make xorg-server.h dix-config.h xorg-config.h && popd

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_sysconfdir}/X11/
ln -s %{_bindir}/Xorg %{buildroot}%{_sysconfdir}/X11/X
ln -sf %{_libexecdir}/Xorg.wrap %{buildroot}%{_bindir}/X

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/xserver
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
touch %{buildroot}%{_sysconfdir}/security/console.apps/xserver

mkdir -p %{buildroot}%{_datadir}/X11/xorg.conf.d
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/X11/xorg.conf.d
# Create xorg.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

mkdir -p %{buildroot}%{_sysconfdir}/X11/app-defaults
mkdir -p %{buildroot}%{_sysconfdir}/X11/fontpath.d

# for compatibility with legacy applications (see #23423, for example)
mkdir -p %{buildroot}%{_prefix}/X11R6/lib/
ln -s ../../%{_lib}/X11 %{buildroot}%{_prefix}/X11R6/lib/X11

# create more module directories to be owned by x11-server-common
install -d -m755 %{buildroot}%{_libdir}/xorg/modules/{input,drivers}

# (anssi) manage proprietary drivers
install -d -m755 %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL/standard.conf << EOF
# This file is knowingly empty since the libraries are in standard search
# path. Please do not remove this file.
EOF
touch %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL.conf

install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/xvfb-run
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/X11/xorg.conf.d/

mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}/lib/udev/rules.d/
install -m 0755 %{SOURCE5} %{buildroot}/sbin/mandriva-setup-keyboard
# (tpg) do not install this as running mandriva-setup-keyboard 
# with systemd configuration before X start produces keyboard layout issues
# https://issues.openmandriva.org/show_bug.cgi?id=274
#install -m 0644 %{SOURCE6} %{buildroot}/lib/udev/rules.d

install -m 755 %{SOURCE30} %{buildroot}%{_bindir}

# And enable Ctrl+Alt+Backspace by default
install -c -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/

# Add synaptics configuration
install -c -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/

# Make the source package
install -d %{buildroot}/%{xserver_source_dir}
rm -rf build
cp -r * %{buildroot}/%{xserver_source_dir}


%files
