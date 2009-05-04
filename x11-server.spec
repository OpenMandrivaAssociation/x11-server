%define git 0
%define applypatches() for patch in %patches; do cat $patch | patch -p1; done

%define with_debug		0
%define kdrive_builds_vesa	0
%define enable_xvnc		1
%define enable_dmx		0
# (cg) Disable xfake temporarily due to build errors
%define enable_xfake		0
%define enable_hal		1
%define enable_dbus		%{enable_hal}
%define enable_builddocs	1
# Do magic with .rpmsave named links
%define pre_post_trans		1

# Need this for shared objects that reference X Server, or other modules symbols
%define _disable_ld_no_undefined 1

%define mesasrcdir		%{_prefix}/src/Mesa
%define mesaver			7.0.3

# Alternatives priority for standard libglx.so and mesa libs
%define priority 500

# Search for modules in extra_module_dir before the default path.
# This will allow fglrx to install its modified modules in more cleaner way.
%define extra_module_dir        %{_libdir}/xorg/extra-modules
%define xorg1_6_extra_modules	%{_libdir}/xorg/xorg-1.6-extra-modules

%define version 1.6.1
%define rel	1

Name: x11-server
Version: %{version}
%if %{git}
Release: %mkrel 1.%{git}.%{rel}
%else
Release: %mkrel %{rel}
%endif
Summary:  X11 servers
Group: System/X11
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: http://xorg.freedesktop.org
%if %{git}
Source0:	xorg-server-%{git}.tar.bz2
%else
Source0: http://xorg.freedesktop.org/releases/individual/xserver/xorg-server-%{version}.tar.bz2
%endif
Source1: xserver.pamd
Source2: xvfb-run.sh
Source3: 10-x11-keymap.fdi
Source4: mandriva-setup-keyboard
License: GPLv2+ and MIT

Obsoletes: x11-server13 <= 1.2.99.905

# vesa based kdrive X servers are not built anymore.
# Obsoleted for clean upgraded
Obsoletes: x11-server-xati	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xchips	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xepson	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xi810	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xmach64	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xmga	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xnvidia	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xpm2	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xr128	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xsmi	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xvesa	<= 1.4.2-4mdv2009.0
Obsoletes: x11-server-xvia	<= 1.4.2-4mdv2009.0

# die, Xgl, die - AdamW 2008/11
Obsoletes: x11-server-xgl <= 0.0.1-0.20080722.3mdv2009.0

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
BuildRequires: x11-util-macros >= 1.1.5
BuildRequires: x11-xtrans-devel >= 1.0.3
BuildRequires: libpam-devel
BuildRequires: libgpm-devel
BuildRequires: SDL-devel
BuildRequires: libgii-devel
BuildRequires: libpixman-1-devel >= 0.9.5
BuildRequires: libpciaccess-devel
BuildRequires: libxv-devel
BuildRequires: libxinerama-devel
BuildRequires: byacc
BuildRequires: flex
# for xkbcomp patch
BuildRequires: openssl-devel

%if %{enable_hal}
# For the moment only really required if compiling with --config-dbus
# But if available at build time, will include headers, but do nothing
BuildRequires: libhal-devel
%endif

%if %{enable_dbus}
BuildRequires: libdbus-devel
%endif

%if %{enable_dmx}
BuildRequires: libdmx-devel
%endif

%if %{enable_xvnc}
BuildRequires: libjpeg-devel
%endif

# (cg) Notes on disabled patches
# ==============================
# This no longer seems to apply:
#  0512-fixes-mdvbz-35912.patch

# Paulo's save context stuff. This conflicts with some changes upstream
# so is currently disabled. Some changes upstream may partly do the same
# functionality (e.g. the moving of the backtrace generation code)
#  0504-SAVE_CONTEXT-Mandriva-Custom-X-Server-patch.patch
#  xorg-server-1.4.2-save_context_fix.patch




# Instructions to setup your repository clone
# git://anongit.freedesktop.org/git/xorg/xserver
# git checkout origin/server-1.6-branch
# git branch -b mdv-1.6-cherry-picks
# git am ../01??-*.patch
# git branch -b mdv-1.6-redhat
# git am ../03??-*.patch
# git branch -b mdv-1.6-xvnc
# git am ../07??-*.patch
# git branch -b mdv-1.6-patches
# git am ../09??-*.patch

# Upstream cherry picks
# git format-patch --start-number 100 xorg-server-1.6.0..mdv-1.6-cherry-picks

# Some patches nominated to 1.6 branch (i.e. no yet acknoledged by the release manager)
Patch200: 0200-xfree86-Remove-device-from-inputInfo.devices-if-Act.patch
Patch201: 0201-dix-ignore-non-pointer-events-in-XineramaCheckMotio.patch

# Patches "liberated" from Fedora: 
# http://cvs.fedoraproject.org/viewvc/rpms/xorg-x11-server/devel/
# git format-patch --start-number 300 mdv-1.6-cherry-picks..mdv-1.6-redhat
Patch300: 0300-RH-xorg-x11-server-1.1.0-no-move-damage-v1.3.patch
Patch302: 0301-RH-xserver-1.5.0-bg-none-root-v1.5.patch
Patch303: 0302-RH-xserver-1.5.0-bad-fbdev-thats-mine-v1.2.patch
Patch304: 0303-RH-xserver-1.5.99.3-dmx-xcalloc-v1.1.patch
Patch305: 0304-RH-xserver-1.5.99.3-ddx-rules-v1.1.patch
Patch306: 0305-RH-xserver-1.5.99.3-broken-mtrr-header-v1.3.patch

# Patches to make Xvnc work
# git format-patch --start-number 700 mdv-1.6-redhat..mdv-1.6-xvnc
Patch700: 0700-Rediff-of-http-www.linuxfromscratch.org-dnicholso.patch
Patch701: 0701-Fix-for-X-server-1.6-input-interface-changes.patch
Patch702: 0702-Use-xorgVersion.h-instead-of-xf86Version.h.patch
Patch703: 0703-Fix-for-DevPrivates-interface-changes.patch
Patch704: 0704-Fix-compilation-Werror-format-security.patch
Patch705: 0705-Fix-bug-41583.patch

# Mandriva patches
# git format-patch --start-number 900 mdv-1.6-xvnc..mdv-1.6-patches
Patch900: 0900-Use-a-X-wrapper-that-uses-pam-and-consolehelper-to-g.patch
Patch901: 0901-Don-t-print-information-about-X-Server-being-a-pre-r.patch
Patch902: 0902-Autoconfigure-to-use-geode-driver-on-the-known-suppo.patch
Patch903: 0903-Take-width-into-account-when-choosing-default-mode.patch
Patch904: 0904-Quirk-Samsung-SyncMaster-205BW.patch
Patch905: 0905-LED-behavior-fixes.patch
Patch906: 0906-Add-noAutoAddDevices-command-line-option.patch
Patch907: 0907-Honour-Option-DPMS-off-on-xorg.conf.patch
Patch908: 0908-Xorg-add-an-extra-module-path.patch
Patch909: 0909-Revert-drop-xprint-remnants-InitGlobals.patch
Patch910: 0910-Port-of-pcpa-s-xkb-compile-cache-patch-to-X-server-1.patch


Requires: %{name}-xorg
%if %{enable_dmx}
Requires: %{name}-xdmx
%else
Obsoletes: %{name}-xdmx < %{version}-%{release}
%endif
Requires: %{name}-xnest
Requires: %{name}-xvfb
%if !%{enable_xvnc}
Obsoletes: %{name}-xvnc < %{version}-%{release}
%endif
%if !%{enable_xfake}
Obsoletes: %{name}-xfake < %{version}-%{release}
%endif

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
Requires: libpciaccess-devel
Requires: libxkbfile-devel

%description devel
Development files for %{name}

%pre devel
if [ -h %{_includedir}/X11 ]; then
	rm -f %{_includedir}/X11
fi

%files devel
%defattr(-,root,root)
%dir %{_includedir}/xorg
%{_includedir}/xorg/*.h
%{_libdir}/pkgconfig/xorg-server.pc
%{_datadir}/aclocal/xorg-server.m4


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
# nvidia-71xx does not support X.org >= 1.5
Conflicts: x11-driver-video-nvidia71xx < 71.86.09-2
# Fix: missing conflicts to allow upgrade from 2008.0 to cooker
# http://qa.mandriva.com/show_bug.cgi?id=36651
Conflicts: x11-driver-video-nvidia-current <= 100.14.19

Conflicts: x11-xorg1_5-server < 1.5.3-4

%description common
X server common files

# old packages had a dir structure on /usr/X11R6/lib/ but starting on
# filesystem-2.1.8 these dirs where kept there but were not owned by any
# package.  It now should be a compat symlink to the new path: /usr/lib/X11,
# but there are scenarios where /usr/lib/X11 and /usr/X11R6/lib/X11 both
# exist as directories.
%pre common
for link in /etc/X11 /usr/lib/X11 /usr/X11R6; do
	if [ -L $link ]; then
		echo "$link is a symbolic link. You must run the"
		echo "script in http://wiki.mandriva.com/en/CookerX11Upgrade"
		echo "before continuing."
		exit 1
	fi
done

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
%defattr(-,root,root)
%dir %{_libdir}/xorg/modules
%dir %{xorg1_6_extra_modules}
%dir %{_libdir}/X11
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/X11/app-defaults
%dir %{_sysconfdir}/X11/fontpath.d
%dir %{_sysconfdir}/ld.so.conf.d/GL
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%{_sysconfdir}/ld.so.conf.d/GL/standard.conf
%if %enable_dbus
%{_sysconfdir}/dbus-1/system.d/xorg-server.conf
%endif
%{_bindir}/gtf
%{_bindir}/cvt
%if %enable_hal
%{_bindir}/mandriva-setup-keyboard
%{_datadir}/hal/fdi/policy/10osvendor/*.fdi
%endif
%if %enable_dmx
%{_bindir}/vdltodmx
%endif
%{_libdir}/X11/Options
%{_libdir}/xorg/modules/*
%{_libdir}/xorg/protocol.txt
%{_datadir}/X11/xkb/README.compiled
%{_mandir}/man1/gtf.*
%{_mandir}/man1/cvt.*
%if %enable_dmx
%{_mandir}/man1/vdltodmx.*
%endif
%{_mandir}/man4/fbdevhw.*
%{_mandir}/man4/exa.*
%dir %{_prefix}/X11R6
%dir %{_prefix}/X11R6/lib
%dir %{_prefix}/X11R6/lib/X11


#------------------------------------------------------------------------------

%package xorg
Summary: X.org X11 server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}
Requires: x11-data-xkbdata > 1.3-5
Requires: x11-font-alias
Requires: libx11-common
Requires: x11-driver-input-mouse
Requires: x11-driver-input-keyboard
%if %{enable_hal}
Requires: x11-driver-input-evdev
Conflicts: drakx-kbd-mouse-x11 < 0.66
%endif
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
# xvfb-run is GPLv2, rest is MIT
License: MIT and GPLv2
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

%if %kdrive_builds_vesa
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

%files xati
%defattr(-,root,root)
%{_bindir}/Xati
%endif

#------------------------------------------------------------------------------

%if %kdrive_builds_vesa
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
%{_mandir}/man1/Xephyr.1*

#------------------------------------------------------------------------------

%if %kdrive_builds_vesa
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

%files xepson
%defattr(-,root,root)
%{_bindir}/Xepson
%endif

#------------------------------------------------------------------------------

%if %enable_xfake
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
%endif

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
 
%if %kdrive_builds_vesa
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

%files xi810
%defattr(-,root,root)
%{_bindir}/Xi810
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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

%files xmach64
%defattr(-,root,root)
%{_bindir}/Xmach64
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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

%files xmga
%defattr(-,root,root)
%{_bindir}/Xmga
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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

%files xnvidia
%defattr(-,root,root)
%{_bindir}/Xnvidia
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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

%files xpm2
%defattr(-,root,root)
%{_bindir}/Xpm2
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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
 
%if %kdrive_builds_vesa
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

%files xsmi
%defattr(-,root,root)
%{_bindir}/Xsmi
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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

%files xvesa
%defattr(-,root,root)
%{_bindir}/Xvesa
%endif

#------------------------------------------------------------------------------
 
%if %kdrive_builds_vesa
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

%files xvia
%defattr(-,root,root)
%{_bindir}/Xvia
%endif

#------------------------------------------------------------------------------

%prep
%if %{git}
%setup -q -n xorg-server-%{git}
%else
%setup -q -n xorg-server-%{version}
%endif

%applypatches

%build
autoreconf -ifs
%if %{with_debug}
CFLAGS='-DBUILDDEBUG -O0 -g3' \
%endif
%configure	--with-log-dir=%{_logdir} \
		--with-os-vendor="Mandriva" \
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
		--enable-kdrive \
		%if %enable_xfake
		--enable-xfake \
		%else
		--disable-xfake \
		%endif
		--enable-xephyr \
		--enable-xsdl \
		%if %kdrive_builds_vesa
		--enable-kdrive-vesa \
		%else
		--disable-kdrive-vesa \
		%endif
		--disable-freetype \
		--disable-install-setuid \
		--enable-secure-rpc \
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
		--disable-builtin-fonts \
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
install -d -m755 %{buildroot}%{xorg1_6_extra_modules}

# (anssi) manage proprietary drivers
install -d -m755 %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL/standard.conf << EOF
# This file is knowingly empty since the libraries are in standard search
# path. Please do not remove this file.
EOF
touch %{buildroot}%{_sysconfdir}/ld.so.conf.d/GL.conf

install -m 0755 %{_sourcedir}/xvfb-run.sh %{buildroot}%{_bindir}/xvfb-run

%if %enable_hal
# autoconfigure keyboard layout based on system settings
mkdir -p $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/10osvendor
install -m 0444 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/10osvendor
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
