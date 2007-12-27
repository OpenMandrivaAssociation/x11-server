%define with_debug		0
%define kdrive_builds_vesa	0
%define enable_xvnc		1
%define enable_dmx		0
%define enable_hal		0
%define enable_dbus		%{enable_hal}

%define mesasrcdir %{_prefix}/src/Mesa
%define mesaver 7.0.1

%ifarch %{ix86} alpha
%define kdrive_builds_vesa 1
%endif

# Alternatives priority for standard libglx.so and mesa libs
%define priority 500

Name: x11-server
Version: 1.4
Release: %mkrel 18
Summary:  X11 servers
Group: System/X11
URL: http://xorg.freedesktop.org

########################################################################
# git clone git://git.mandriva.com/people/pcpa/xorg/xserver xorg/xserver
# cd xorg/xserver
# git-archive --format=tar --prefix=xorg-server-1.4/ xorg-server-1.4 | bzip2 -9 > xorg-server-1.4.tar.bz2
########################################################################
Source: xorg-server-1.4.tar.bz2
Source1: xserver.pamd

########################################################################
License: GPLv2+ and MIT

Obsoletes: x11-server13 <= 1.2.99.905

%if %enable_dmx
BuildRequires: libdmx-devel >= 1.0.1
%endif
BuildRequires: libfontenc-devel >= 1.0.1
BuildRequires: libmesagl-devel >= %{mesaver}
BuildRequires: libxau-devel >= 1.0.0
BuildRequires: libxaw-devel >= 1.0.1
BuildRequires: libxdmcp-devel >= 1.0.0
BuildRequires: libxext-devel >= 1.0.0
BuildRequires: libxfont-devel >= 1.2.8-2mdv
BuildRequires: libxfixes-devel
BuildRequires: libxi-devel >= 1.1.3
BuildRequires: libxkbfile-devel >= 1.0.4
BuildRequires: libxau-devel >= 1.0.0
BuildRequires: libxkbui-devel >= 1.0.1
BuildRequires: libxmu-devel >= 1.0.0
BuildRequires: libxpm-devel >= 3.5.4.2
BuildRequires: libxrender-devel >= 0.9.4
BuildRequires: libxres-devel >= 1.0.0
BuildRequires: libxtst-devel >= 1.0.1
BuildRequires: libxxf86misc-devel >= 1.0.0
BuildRequires: libxxf86vm-devel >= 1.0.0
BuildRequires: libxfont-devel >= 1.0.0
BuildRequires: mesa-source >= %{mesaver}
BuildRequires: x11-proto-devel >= 1.4.0
BuildRequires: x11-util-macros >= 1.1.5-4mdk
BuildRequires: x11-xtrans-devel >= 1.0.3
BuildRequires: libpam-devel
BuildRequires: libgpm-devel
BuildRequires: SDL-devel
BuildRequires: libgii-devel
BuildRequires: libpixman-1-devel >= 0.9.5
%if %{enable_dbus}
# so that input-hotplug is enabled:
BuildRequires: libhal-devel
%endif
%if %{enable_hal}
BuildRequires: libdbus-1-devel
%endif
%if %{enable_xvnc}
# for VNC:
BuildRequires: libjpeg-devel
%endif
BuildRequires: x11-util-modular

########################################################################
# git-format-patch xorg-server-1.4..origin/mandriva+gpl
Patch1:  0001-config-return-BadValue-to-caller-if-add-remove-does.patch
Patch2:  0002-config-Use-config-dbus-consistently-for-error-mes.patch
Patch3:  0003-Don-t-segfault-on-shutdown-if-we-never-managed-to-co.patch
Patch4:  0004-Set-noCompositeExtension-to-TRUE-when-failing-to-ini.patch
Patch5:  0005-configure.ac-XFree86-Only-build-XF86Misc-and-XF86Vi.patch
Patch6:  0006-Xi-Include-XI-protocol-header-in-exevents.h.patch
Patch7:  0007-XKB-Add-more-bits-to-xkbsrv.h.patch
Patch8:  0008-XFree86-Remove-ridiculous-SIGIO-debugging.patch
Patch9:  0009-xkb-Store-the-action-filters-per-device-in-the-XkbS.patch
Patch10: 0010-Save-processInputProc-before-wrapping-it-and-restore.patch
Patch11: 0011-xkb-enable-XI-event-processing-for-xkb.patch
Patch12: 0012-dix-add-XI-event-support-to-FixKeyState.patch
Patch13: 0013-dix-don-t-compress-motion-events-from-different-dev.patch
Patch14: 0014-xkb-xkbHandleActions-let-wrapping-take-care-of-eve.patch
Patch15: 0015-xkb-Unwrap-properly-in-ProcessPointerEvent.patch
Patch16: 0016-XKB-Don-t-update-indicators-on-all-devices-add-mis.patch
Patch17: 0017-XKB-Cope-with-all-events-in-XkbProcessKeyboardEvent.patch
Patch18: 0018-xfree86-wrap-keyboard-devices-for-XKB.patch
Patch19: 0019-Input-Generate-XKB-mapping-changes-for-all-core-sen.patch
Patch20: 0020-XFree86-Input-Save-restore-errno-around-SIGIO-bug.patch
Patch21: 0021-Config-HAL-Touchpads-are-pointers-too.patch
Patch22: 0022-DIX-XKB-Set-xkbInfo-to-NULL-as-well-as-freeing-it.patch
Patch23: 0023-Config-D-Bus-Fix-dbus_bus_request_name-failure-che.patch
Patch24: 0024-Screen-size-changing-should-leave-FB-alone-when-X-is.patch
Patch25: 0025-Prefer-configured-DisplaySize-to-probed-DDC-data-if.patch
Patch26: 0026-Actually-build-Secure-RPC-authentication-support-mi.patch
Patch27: 0027-.gitignore-Ignore-build-directories.patch
Patch28: 0028-Xephyr-don-t-initialise-the-GLX-extension.patch
Patch29: 0029-XFree86-Misc-VidMode-Remove-ridiculous-debug-ErrorF.patch
Patch30: 0030-Input-Fix-key-down-test-bug-12858.patch
Patch31: 0031-GetKeyboardEvents-Reject-out-of-range-keycodes-bug.patch
Patch32: 0032-XKB-Don-t-ring-the-bell-when-we-don-t-have-a-BellPr.patch
Patch33: 0033-EXA-Punt-on-fallback-case-not-handled-correctly-in.patch
Patch34: 0034-EXA-Make-sure-tile-offsets-passed-to-drivers-are-ne.patch
Patch35: 0035-EXA-Don-t-attempt-to-move-in-pixmaps-that-can-t-be.patch
Patch36: 0036-XKB-Generate-correct-key-repeat-events-bug-13114.patch
Patch37: 0037-First-version-of-code-to-make-symbols-default-to-h.patch
Patch38: 0038-This-is-a-set-of-patches-that-should-be-safe-to-ap.patch
Patch39: 0039-Blue-background-custom-patch.patch
Patch40: 0040-Fontpath.d-updated-documentation.patch
Patch41: 0041-Add-SAVE_CONTEXT-Mandriva-Custom-X-Server-patch-to.patch
Patch42: 0042-Use-a-X-wrapper-that-uses-pam-and-consolehelper-to-g.patch
Patch43: 0043-First-commit-in-new-branch-mandriva-gpl-adding-Xv.patch
Patch44: 0044-xvfb-run-support-patch-added-to-mandriva-gpl-branc.patch
Patch45: 0045-Fix-vnc-build-by-using-sh-.-script.sh-instead-of.patch
Patch46: 0046-Extra-symbols-that-must-be-exported-to-satisfy-sym.patch
########################################################################

Requires: %{name}-xorg
%if %enable_dmx
Requires: %{name}-xdmx
%endif
Requires: %{name}-xnest
Requires: %{name}-xvfb

%description
X11 servers

#------------------------------------------------------------------------------

%package devel
Summary: Development files for %{name}
Group: Development/X11
License: MIT

%define oldxorgnamedevel  %mklibname xorg-x11
Conflicts: %{oldxorgnamedevel}-devel < 7.0
Obsoletes: x11-server13-devel <= 1.2.99.905
Requires: libpixman-1-devel

%description devel
Development files for %{name}

%pre devel
if [ -h %{_includedir}/X11 ]; then
	rm -f %{_includedir}/X11
fi

%files devel
%defattr(-,root,root)
%dir %{_includedir}/xorg
%dir %{_includedir}/X11/bitmaps
%dir %{_includedir}/X11/pixmaps
%{_includedir}/xorg/*.h
%{_libdir}/pkgconfig/xorg-server.pc
%{_datadir}/aclocal/xorg-server.m4
%{_libdir}/xorg/modules/*.la
%{_libdir}/xorg/modules/extensions/*.la
%{_libdir}/xorg/modules/fonts/*.la
%{_libdir}/xorg/modules/linux/*.la
%{_libdir}/xorg/modules/multimedia/*.la
%{_datadir}/X11/mandriva/*.deps

#------------------------------------------------------------------------------

%package common
Summary: X server common files
Group: System/X11
License: MIT
Provides: XFree86 = 7.0.0
Conflicts: xorg-x11 <= 6.9.0-12mdk
Obsoletes: x11-server13-common <= 1.2.99.905
Obsoletes: x11-server-xprt <= 1.3.0.0-2mdv2008.0
Requires: rgb
# for 'fixed' and 'cursor' fonts
Requires: x11-font-misc-misc
Requires: x11-font-cursor-misc
Requires: x11-font-alias
Requires(post): update-alternatives >= 1.9.0
Requires(postun): update-alternatives
# see comment about /usr/X11R6/lib below
Conflicts: filesystem < 2.1.8

# xorgcfg requires these
Requires: x11-data-bitmaps

%description common
X server common files

# old packages had a dir structure on /usr/X11R6/lib/ but starting on
# filesystem-2.1.8 these dirs where kept there but were not owned by any
# package.  It now should be a compat symlink to the new path: /usr/lib/X11,
# but there are scenarios where /usr/lib/X11 and /usr/X11R6/lib/X11 both
# exist as directories.
%pre common
if [ -L %{_libdir}/X11 ]; then 
	rm -f %{_libdir}/X11
fi
if [ -d /usr/X11R6/lib/X11 ]; then
	mkdir -p %{_libdir}/X11
	rm -f /usr/X11R6/lib/X11/fs # old symlink, already on the target dir
	mv -f /usr/X11R6/lib/X11/* %{_libdir}/X11/ 2> /dev/null
	rm -rf /usr/X11R6/lib/X11
fi

%post common
%{_sbindir}/update-alternatives \
	--install %{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf %{priority} \
	--slave %{_libdir}/xorg/modules/extensions/libglx.so libglx %{_libdir}/xorg/modules/extensions/standard/libglx.so

# (anssi)
%triggerun common -- %{name}-common < 1.3.0.0-17
[ $1 -eq 2 ] || exit 0 # do not run if downgrading
[ -L %{_libdir}/xorg/modules/extensions/libglx.so ] || rm -f %{_libdir}/xorg/modules/extensions/libglx.so
current_glconf="$(readlink -e %{_sysconfdir}/ld.so.conf.d/GL.conf)"
if [ "${current_glconf#*mesa}" == "gl1.conf" ]; then
	# This an upgrade of a system with no proprietary drivers enabled, update
	# the link to point to the new standard.conf instead of libmesagl1.conf (2008.0 change).
	# This also replaces old libglx.so with a symlink.
	%{_sbindir}/update-alternatives --set gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf
else
	# XFdrake did not set symlink to manual mode before 2008.0, so we ensure it here.
	# This also replaces old libglx.so with a symlink.
	%{_sbindir}/update-alternatives --set gl_conf "${current_glconf}"
fi
true

%postun common
if [ ! -f %{_sysconfdir}/ld.so.conf.d/GL/standard.conf ]; then
	/usr/sbin/update-alternatives --remove gl_conf %{_sysconfdir}/ld.so.conf.d/GL/standard.conf
fi

%files common
%defattr(-,root,root)
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xserver
%dir %{_libdir}/X11
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/X11/app-defaults
%dir %{_sysconfdir}/X11/fontpath.d
%dir %{_sysconfdir}/ld.so.conf.d/GL
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%{_sysconfdir}/ld.so.conf.d/GL/standard.conf
%{_bindir}/xorgcfg
%{_bindir}/xorgconfig
%{_bindir}/gtf
%{_bindir}/cvt
%{_bindir}/in*
%{_bindir}/ioport
%{_bindir}/out*
%{_bindir}/pcitweak
%{_bindir}/scanpci
%if %enable_dmx
%{_bindir}/vdltodmx
%endif
%{_libdir}/X11/Cards
%{_libdir}/X11/Options
%dir %{_libdir}/xorg/modules
%{_libdir}/xorg/modules/*.so
%dir %{_libdir}/xorg/modules/drivers
%{_libdir}/xorg/modules/fonts/*.so
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/*.so
%dir %{_libdir}/xorg/modules/extensions/standard
%{_libdir}/xorg/modules/extensions/standard/*.so
%dir %{_libdir}/xorg/modules/fonts
%dir %{_libdir}/xorg/modules/input
%dir %{_libdir}/xorg/modules/linux
%{_libdir}/xorg/modules/linux/*.so
%dir %{_libdir}/xorg/modules/multimedia
%{_libdir}/xorg/modules/multimedia/*.so
# (anssi) We do not want this file to really exist, it is empty.
# This entry causes an rpm-build warning "file listed twice", but getting rid
# of the warning would need us to list all the other extensions one-by-one.
%ghost %{_libdir}/xorg/modules/extensions/libglx.so
%{_libdir}/xserver/SecurityPolicy
%{_datadir}/X11/xkb/README.compiled
%{_mandir}/man1/xorgcfg.*
%{_mandir}/man1/xorgconfig.*
%{_mandir}/man1/gtf.*
%{_mandir}/man1/cvt.*
%{_mandir}/man1/pcitweak.*
%{_mandir}/man1/scanpci.*
%if %enable_dmx
%{_mandir}/man1/vdltodmx.*
%endif
%{_mandir}/man4/fbdevhw.*
%{_mandir}/man4/exa.*
%{_mandir}/man5/SecurityPolicy.*
%dir %{_prefix}/X11R6
%dir %{_prefix}/X11R6/lib
%dir %{_prefix}/X11R6/lib/X11
# xorgcfg bitmaps/pixmaps
%{_includedir}/X11/bitmaps/*.xbm
%{_includedir}/X11/pixmaps/*.xpm


#------------------------------------------------------------------------------

%package xorg
Summary: X.org X11 server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}
Requires: x11-data-xkbdata >= 1.0.1 
Requires: x11-font-alias
Requires: libx11-common
Requires: x11-driver-input-mouse
Requires: x11-driver-input-keyboard
Conflicts: compiz < 0.5.0-1mdv2007.1
Obsoletes: x11-server13-xorg <= 1.2.99.905

# because of fontpath.d support
Requires: libxfont >= 1.2.8-2mdv

%description xorg
x11-server-xorg is the new generation of X server from X.Org.

%files xorg
%defattr(-,root,root)
%{_bindir}/X
%{_bindir}/Xorg
%attr(4755,root,root)%{_bindir}/Xwrapper
%{_sysconfdir}/X11/X
%{_sysconfdir}/pam.d/xserver
%{_sysconfdir}/security/console.apps/xserver
%{_datadir}/X11/app-defaults/XOrgCfg
%{_mandir}/man1/Xorg.*
%{_mandir}/man1/Xserver.*
%{_mandir}/man5/xorg.conf.*

#------------------------------------------------------------------------------

%if %enable_dmx
%package xdmx
Summary: Distributed Multi-head X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

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
%defattr(-,root,root)
%{_bindir}/Xdmx
%{_bindir}/xdmx*
%{_bindir}/dmx*
%{_mandir}/man1/Xdmx.*
%{_mandir}/man1/xdmxconfig.*
%{_mandir}/man1/dmxtodmx.*
%endif

#------------------------------------------------------------------------------

%package xnest
Summary: A nested X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

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
%defattr(-,root,root)
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.*

#------------------------------------------------------------------------------

%package xvfb
Summary: X virtual framebuffer server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}
Requires: xauth

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
%defattr(-,root,root)
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.*
%{_mandir}/man1/xvfb-run.*

#------------------------------------------------------------------------------

%if %enable_xvnc
%package xvnc
Summary: X VNC server
Group: System/X11
License: GPL
Requires: x11-server-common = %{version}-%{release}

%description xvnc
Xvnc is a virtual X Windows System server like Xvfb, but it allows 
VNC clients access to the 'virtual' display it provides.

%files xvnc
%defattr(-,root,root)
%{_bindir}/Xvnc
%endif
#------------------------------------------------------------------------------

%package xati
Summary: KDrive ati X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xati
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for ATI chipsets.

%if %kdrive_builds_vesa
%files xati
%defattr(-,root,root)
%{_bindir}/Xati
%endif

#------------------------------------------------------------------------------

%package xchips
Summary: KDrive chips X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xchips
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for Chips chipsets.

%if %kdrive_builds_vesa
%files xchips
%defattr(-,root,root)
%{_bindir}/Xchips
%endif

#------------------------------------------------------------------------------

%package xephyr
Summary: KDrive Xephyr X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

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

Possible uses include; 
- Xnest replacement - Window manager, Composite 'gadget', etc development tool. 
- Toolkit debugging - rendundant toolkit paints can be observered easily via
  the debugging mode. 
- X Server internals development - develop without the need for an extra
  machine

%files xephyr
%defattr(-,root,root)
%{_bindir}/Xephyr

#------------------------------------------------------------------------------

%package xepson
Summary: KDrive epson X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xepson
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for Epson chipsets.

%if %kdrive_builds_vesa
%files xepson
%defattr(-,root,root)
%{_bindir}/Xepson
%endif

#------------------------------------------------------------------------------
 
%package xfake
Summary: KDrive fake X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xfake
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for testing purposes.

%files xfake
%defattr(-,root,root)
%{_bindir}/Xfake

#------------------------------------------------------------------------------
  
%package xfbdev
Summary: KDrive fbdev X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xfbdev
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for being used on top of linux framebuffer.

%files xfbdev
%defattr(-,root,root)
%{_bindir}/Xfbdev

#------------------------------------------------------------------------------
 
%package xi810
Summary: KDrive i810 X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xi810
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for Intel chipsets.

%if %kdrive_builds_vesa
%files xi810
%defattr(-,root,root)
%{_bindir}/Xi810
%endif

#------------------------------------------------------------------------------
 
%package xmach64
Summary: KDrive mach64 X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xmach64
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for mach64 chipsets.

%if %kdrive_builds_vesa
%files xmach64
%defattr(-,root,root)
%{_bindir}/Xmach64
%endif

#------------------------------------------------------------------------------
 
%package xmga
Summary: KDrive mga X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xmga
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for mga chipsets.

%if %kdrive_builds_vesa
%files xmga
%defattr(-,root,root)
%{_bindir}/Xmga
%endif

#------------------------------------------------------------------------------
 
%package xnvidia
Summary: KDrive nvidia X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xnvidia
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for nvidia chipsets.

%if %kdrive_builds_vesa
%files xnvidia
%defattr(-,root,root)
%{_bindir}/Xnvidia
%endif

#------------------------------------------------------------------------------
 
%package xpm2
Summary: KDrive pm2 X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xpm2
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for Permedia2 chipsets.

%if %kdrive_builds_vesa
%files xpm2
%defattr(-,root,root)
%{_bindir}/Xpm2
%endif

#------------------------------------------------------------------------------
 
%package xr128
Summary: KDrive r128 X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xr128
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for rage128 chipsets.

%if %kdrive_builds_vesa
%files xr128
%defattr(-,root,root)
%{_bindir}/Xr128
%endif

#------------------------------------------------------------------------------
 
%package xsdl
Summary: KDrive sdl X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xsdl
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDriver server runs on top of the Simple DirectMedia Layer.

%files xsdl
%defattr(-,root,root)
%{_bindir}/Xsdl

#------------------------------------------------------------------------------
 
%package xsmi
Summary: KDrive smi X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xsmi
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for Silicon Motion chipsets.

%if %kdrive_builds_vesa
%files xsmi
%defattr(-,root,root)
%{_bindir}/Xsmi
%endif

#------------------------------------------------------------------------------
 
%package xvesa
Summary: KDrive vesa X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xvesa
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for VESA capable chipsets.

%if %kdrive_builds_vesa
%files xvesa
%defattr(-,root,root)
%{_bindir}/Xvesa
%endif

#------------------------------------------------------------------------------
 
%package xvia
Summary: KDrive via X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xvia
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for VIA chipsets.

%if %kdrive_builds_vesa
%files xvia
%defattr(-,root,root)
%{_bindir}/Xvia
%endif

#------------------------------------------------------------------------------

%prep
%setup -q -n xorg-server-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1

%build
autoreconf -ifs
%if %{with_debug}
CFLAGS='-DBUILDDEBUG -g' \
%endif
%configure	--with-log-dir=%{_logdir} \
		--with-os-vendor="Mandriva" \
		--with-os-name="`echo \`uname -s -r\` | sed -e s'/ /_/g'`" \
		--with-vendor-web="http://qa.mandriva.com" \
		%if %{with_debug}
  		--enable-debug \
		%else
		--disable-debug \
		%endif
 		--enable-builddocs \
  		--disable-install-libxf86config \
  		--enable-composite \
  		--enable-shm \
  		--enable-xres \
  		--enable-xtrap \
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
		--with-mesa-source=%{mesasrcdir} \
  		--enable-xinerama \
  		--enable-xf86vidmode \
  		--enable-xf86misc \
		--enable-xace \
  		--enable-xcsecurity \
		--enable-xevie \
  		--enable-appgroup \
  		--enable-cup \
  		--enable-evi \
  		--enable-xf86bigfont \
  		--enable-dpms \
  		--enable-xinput \
		--disable-xcalibrate \
		--disable-tslib \
  		--enable-multibuffer \
  		--enable-fontcache \
  		--enable-dbe \
		--enable-xfree86-utils \
  		--enable-xorg \
		%if %enable_xvnc
  		--enable-xvnc \
		%endif
		%if %enable_dmx
  		--enable-dmx \
		%else
		--disable-dmx \
		%endif
  		--enable-xvfb \
  		--enable-xnest \
  		--disable-xwin \
  		--disable-xprint \
  		--disable-xgl \
  		--disable-xglx \
  		--disable-xegl \
  		--enable-kdrive \
  		--enable-xfake \
  		--enable-xephyr \
  		--enable-xsdl \
		--disable-freetype \
  		--disable-install-setuid \
 		--enable-secure-rpc \
  		--enable-xorgcfg \
  		--enable-kbd_mode \
		--enable-xwrapper \
		--enable-pam \
		%if %{enable_dbus}
		--enable-config-dbus \
		%else
		--disable-config-dbus \
		%endif
		%if %{enable_hal}
		--enable-config-hal \
		%else
		--disable-config-hal \
		%endif
		--with-fontdir="%{_datadir}/fonts" \
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
install -m 0644 %{_sourcedir}/xserver.pamd %{buildroot}%{_sysconfdir}/pam.d/xserver     
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

# (anssi) manage proprietary drivers
install -d -m755 %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL/standard.conf << EOF
# This file is knowingly empty since the libraries are in standard search
# path. Please do not remove this file.
EOF
touch %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL.conf
install -d -m755 %{buildroot}%{_libdir}/xorg/modules/extensions/standard
mv %{buildroot}%{_libdir}/xorg/modules/extensions/libglx.so \
	%{buildroot}%{_libdir}/xorg/modules/extensions/standard/libglx.so
touch %{buildroot}%{_libdir}/xorg/modules/extensions/libglx.so

# FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
# FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
# This module is broken. Probably most code using it has been patched
# to not use it anymore, but it is still installed by default, and
# have missing symbols caused by api changes not updated back.
# For the moment, just don't install it.
# Afaik only the mga driver uses it; maybe it somehow works because
# the missing symbols are never used? Anyway, must be fixed.
# FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
# FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
rm -f %{buildroot}%{_libdir}/xorg/modules/libxf8_32bpp.*


# Create list of dependencies
x-check-deps.pl
for deps in *.deps; do
    install -D -m 644 $deps %{buildroot}/%{_datadir}/X11/mandriva/$deps
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
