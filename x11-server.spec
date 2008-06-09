%define with_debug		0
%define kdrive_builds_vesa	0
%define enable_xvnc		1
%define enable_dmx		1
%define enable_hal		0
%define enable_dbus		%{enable_hal}
%define enable_builddocs	1
# Do magic with .rpmsave named links
%define pre_post_trans		1

# Need this for shared objects that reference X Server, or other modules symbols
%define _disable_ld_no_undefined 1

%define mesasrcdir		%{_prefix}/src/Mesa
%define mesaver			7.0.3

%ifarch %{ix86} alpha
%define kdrive_builds_vesa	1
%endif

# Alternatives priority for standard libglx.so and mesa libs
%define priority 500

Name: x11-server
Version: 1.4.0.90
Release: %mkrel 21
Summary:  X11 servers
Group: System/X11
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: http://xorg.freedesktop.org
Source: http://xorg.freedesktop.org/releases/individual/xserver/xorg-server-%{version}.tar.bz2
Source1: xserver.pamd
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
BuildRequires: x11-util-macros >= 1.1.5
BuildRequires: x11-xtrans-devel >= 1.0.3
BuildRequires: libpam-devel
BuildRequires: libgpm-devel
BuildRequires: SDL-devel
BuildRequires: libgii-devel
BuildRequires: libpixman-1-devel >= 0.9.5

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

# git-format-patch xorg-server-1.4.0.90..origin/server-1.4-branch
Patch1:  0001-Bug-13308-Verify-and-reject-obviously-broken-modes.patch
Patch2:  0002-bgPixel-unsigned-long-is-64-bit-on-x86_64-so-1.patch
Patch3:  0003-Xprint-Clean-up-generated-files.patch
Patch4:  0004-Config-D-Bus-Don-t-leak-timers.patch
Patch5:  0005-Config-HAL-Don-t-leak-options-on-failure-to-add-de.patch
Patch6:  0006-OS-Don-t-leak-connection-translation-table-on-regen.patch
Patch7:  0007-KDrive-Xephyr-Don-t-leak-screen-damage-structure.patch
Patch8:  0008-Input-Don-t-reinit-devices.patch
Patch9:  0009-include-never-overwrite-realInputProc-with-enqueueI.patch
Patch10: 0010-OS-IO-Zero-out-client-buffers.patch
Patch11: 0011-XKB-XkbCopyKeymap-Don-t-leak-all-the-sections.patch
Patch12: 0012-Xephyr-One-time-keyboard-leak-fix.patch
Patch13: 0013-Fix-for-CVE-2007-5760-XFree86-Misc-extension-out-o.patch
Patch14: 0014-Fix-for-CVE-2007-6428-TOG-cup-extension-memory-cor.patch
Patch15: 0015-Fix-for-CVE-2007-6427-Xinput-extension-memory-corr.patch
Patch16: 0016-Fix-for-CVE-2007-6429-MIT-SHM-and-EVI-extensions-i.patch
Patch17: 0017-Fix-for-CVE-2008-0006-PCF-Font-parser-buffer-overf.patch
Patch18: 0018-Fix-for-CVE-2007-5958-File-existence-disclosure.patch
Patch19: 0019-CVE-2007-6429-Don-t-spuriously-reject-8bpp-shm-pix.patch
Patch20: 0020-dix-set-the-correct-number-of-valuators-in-valuator.patch
Patch21: 0021-xkb-don-t-update-LEDs-if-they-don-t-exist.-Bug-13.patch
Patch22: 0022-security-Fix-for-Bug-14480-untrusted-access-broke.patch
Patch23: 0023-Resize-composite-overlay-window-when-the-root-window.patch
Patch24: 0024-Fix-rotation-for-multi-monitor-situation.patch
Patch25: 0025-Don-t-break-grab-and-focus-state-for-a-window-when-r.patch
Patch26: 0026-CVE-2007-6429-Always-test-for-size-offset-wrapping.patch
Patch27: 0027-Fix-context-sharing-between-direct-indirect-contexts.patch
Patch28: 0028-Add-some-more-support-for-DragonFly.-From-Joerg-Sonn.patch
Patch29: 0029-configure.ac-DragonFly-BSD-support.patch
Patch30: 0030-Fixed-configure.ac-for-autoconf-2.62.patch
Patch31: 0031-EXA-Fix-off-by-one-in-polyline-drawing.patch
Patch32: 0032-XKB-Fix-processInputProc-wrapping.patch
Patch33: 0033-xfree86-fix-AlwaysCore-handling.-Bug-14256.patch
Patch34: 0034-Ignore-not-just-block-SIGALRM-around-Popen-Pcl.patch
Patch35: 0035-Fix-build-on-FreeBSD-after-Popen-changes.patch
Patch36: 0036-So-like-checking-return-codes-of-system-calls-sig.patch
Patch37: 0037-Check-for-sys-sdt.h-as-well-when-determining-to-en.patch
Patch38: 0038-dix-Always-add-valuator-information-if-present.patch
Patch39: 0039-Bug-10324-dix-Allow-arbitrary-value-ranges-in-Ge.patch
Patch40: 0040-Bug-10324-dix-Add-scaling-of-X-and-Y-on-the-repo.patch
Patch41: 0041-dix-Skip-call-to-clipAxis-for-relative-core-events.patch
Patch42: 0042-dix-Move-motion-history-update-until-after-screen-c.patch
Patch43: 0043-XKB-Actually-explain-keymap-failures.patch
Patch44: 0044-kdrive-allow-disabling-Composite.patch
Patch45: 0045-When-XKB-fails-to-open-rules-file-log-the-file-name.patch
Patch46: 0046-dmx-fix-build-by-adding-New-Delete-InputDeviceRequ.patch
Patch47: 0047-dmx-link-in-XSERVER_LIBS.patch
Patch48: 0048-xephyr-fix-linking-by-adding-pixman-and-using-XSERV.patch
Patch49: 0049-xprint-fix-build-by-adding-New-Delete-InputDeviceR.patch
Patch50: 0050-xprint-fix-linking-by-including-XSERVER_LIBS.patch
Patch51: 0051-Fix-RandR-1.2-driver-interface-conversion-of-two-col.patch
Patch52: 0052-Fix-overly-restrictive-integer-overflow-check-in-EXA.patch
Patch53: 0053-Fix-hal-shutdown-crash.patch
Patch54: 0054-Bump-DEFAULT_DPI-to-96.patch
Patch55: 0055-Bug-13962-Re-arm-the-DPMS-timer-when-re-enabling-D.patch
Patch56: 0056-Prevent-the-wm-command-line-option-from-causing-a-S.patch
Patch57: 0057-EXA-Skip-empty-glyphs.-cherry-picked-from-commit-c.patch
Patch58: 0058-xf86-Add-AutoConfig-driver-for-PCI-ID-1022-2081-to.patch
Patch59: 0059-xkb-when-copying-the-keymap-make-sure-the-structs.patch
Patch60: 0060-Fix-getValuatorEvents-to-compute-number-of-valuators.patch

# git-checkout patches
# git-rebase origin/server-1.4-branch
# git-format-patch --start-number 500 origin/server-1.4-branch..patches
Patch500: 0500-Move-around-a-list-traversal-while-free-ing-data.patch
Patch501: 0501-Fix-a-crash-if-xorg.conf-doesn-t-have-a-Files-sectio.patch
Patch502: 0502-Don-t-enable-mouse-keys-if-the-X-Server-was-not-star.patch
Patch503: 0503-Blue-background-custom-patch.patch
Patch504: 0504-SAVE_CONTEXT-Mandriva-Custom-X-Server-patch.patch
Patch505: 0505-Xvnc-support.patch
Patch506: 0506-fix-parsing-weird-EDID.patch
Patch507: 0507-xvfb-run-support.patch
Patch508: 0508-Use-a-X-wrapper-that-uses-pam-and-consolehelper-to-g.patch
Patch509: 0509-Fontpath.d-updated-documentation.patch
Patch510: 0510-Update-keyboard-leds.patch
Patch511: 0511-Mouse-moves-slower-than-hand-movement-in-games.patch
Patch512: 0512-fixes-mdvbz-35912.patch
Patch513: 0513-Don-t-print-information-about-X-Server-being-a-pre-r.patch

# Some cherry-picks from master
Patch514: 0514-reduce-wakeups-from-smart-scheduler.patch
Patch515: 0515-Don-t-frob-timers-unless-SmartSchedule-is-running.patch
Patch516: 0516-xkb-when-copying-sections-make-sure-num_rows-is-se.patch
Patch517: 0517-XkbCopyKeymap-was-mangling-doodads-and-overlays.patch
Patch518: 0518-regenerated-adds-GL_MAX_3D_TEXTURE_SIZE-see-bug-13.patch
Patch519: 0519-regenerated-to-add-framebuffer-object-tokens-bug-13.patch
Patch520: 0520-Fix-potential-crasher-in-xf86CrtcRotate.patch
Patch521: 0521-Document-the-AllowEmptyInput-AutoAddDevices-and-Aut.patch
Patch522: 0522-mi-change-infamous-Tossed-event-.-error-for-som.patch
Patch523: 0523-xfree86-don-t-call-xalloc-from-signal-handlers-when.patch
Patch524: 0524-XKB-Always-set-size-correctly-in-XkbCopyKeymap-s-ge.patch
Patch525: 0525-xf86DDCMonitorSet-Honor-the-DisplaySize-from-the-co.patch
Patch526: 0526-X86EMU-handle-CPUID-instruction.patch
Patch527: 0527-Fail-CRTC-configuration-if-vtSema.patch

# More mandriva custom patches, to be reordered in next rebase
# (latest xserver segfaults when mplayer runs) #40959
Patch528: 0528-Correct-a-NULL-pointer-deference.patch
Patch529: 0529-Autoconfigure-to-use-geode-driver-on-the-known-sup.patch
Patch530: 0530-Fix-mandriva-bug-37514-vncserver-segfaults-when-con.patch

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
Requires(pretrans): fontconfig
Requires(posttrans): symlinks
Requires(post): update-alternatives >= 1.9.0
Requires(postun): update-alternatives
# see comment about /usr/X11R6/lib below
Conflicts: filesystem < 2.1.8

# Fix: missing conflicts to allow upgrade from 2008.0 to cooker
# http://qa.mandriva.com/show_bug.cgi?id=36651
Conflicts: x11-driver-video-nvidia-current <= 100.14.19

# Avoid upgrade or just install problems with symlinks
Conflicts: x11-driver-video-fglrx < 8.476-2
Conflicts: libx11-common < 1.1.4-2

#   Some of these are more broken than thinking the own {base-dir}/X11,
# and should really be dropped from the distro, but adding a Conflicts
# to avoid update problems where they could mess with the symlinks.
Conflicts: groff-gxditview < 1.19.1-9
Conflicts: xmris < 4.0.5-5
Conflicts: xrn < 9.02-17

# xorgcfg requires these
Requires: x11-data-bitmaps
# xorgcfg requires bitmaps on this package...
Requires: bitmap

%description common
X server common files

# old packages had a dir structure on /usr/X11R6/lib/ but starting on
# filesystem-2.1.8 these dirs where kept there but were not owned by any
# package.  It now should be a compat symlink to the new path: /usr/lib/X11,
# but there are scenarios where /usr/lib/X11 and /usr/X11R6/lib/X11 both
# exist as directories.
%pretrans common
move () {
    #  Don't modify /usr if it is a symlink
    if [ x$3 = x ]; then
	[ -L $2 ] && rm $2
	mkdir -p $2
    fi
    #  Need to recurse to move any links themselves and not just the
    # parent directory, or broken symlinks may be left behind.
    for file in `find $1 -maxdepth 1 -mindepth 1`; do
	file=`basename $file`
	if [ `readlink -f $1/$file` = `readlink -f $2/$file` ]; then
	    [ -L $1/$file ] && rm $1/$file
	    continue
	fi
	if [ -L $1/$file ]; then
	    if [ ! -e $2/$file ]; then
		ln -s `readlink -f $1/$file` $2/$file
	    fi
	    rm $1/$file
	elif [ -d $1/$file ]; then
	    move $1/$file $2/$file
	else
	    if [ -e $2/$file ]; then
		mv $1/$file $2/$file.orig
	    else
		mv $1/$file $2
	    fi
	fi
    done
    rmdir $1
}
check () {
    if [ ! -L $1 -a -d $1 ]; then
	move $1 $2 $3
    fi
    # Magic: Symlink to a directory ending in .rpmsave so that
    # rpm will not attempt to remove newly installed files thinking
    # they are old files...
    [ ! -L $2.rpmsave ] && ln -s $2 $2.rpmsave
    # If the symlink already exists it was not removed in a previous
    # version of this script, or upgrade was cancelled.
    [ -L $1 ] && rm $1
    ln -s $2.rpmsave $1
}
check %{_sysconfdir}/X11 %{_datadir}/X11
check %{_libdir}/X11 %{_datadir}/X11
#   Don't use %{_prefix} because of ending /
check %{_prefix}/X11R6 `echo %{_prefix} | sed -e 's@/*$@@'` can-be-a-symlink
#   Only really required if fontpath.d symlinks are remade.
%{_bindir}/fc-cache

%posttrans common
usr=`echo %{_prefix} | sed -e 's@/*$@@'`
# Remove .rpmsave symlinks
rm %{_datadir}/X11.rpmsave
rm $usr.rpmsave
# And directly link to the proper directory
ln -sf ../../%{_datadir}/X11 %{_sysconfdir}/X11
ln -sf ../../%{_datadir}/X11 %{_libdir}/X11
ln -sf ../`echo %{_prefix} | sed -e 's@/*$@@'` %{_prefix}/X11R6
symlinks -cr %{_datadir}/X11

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
%if ! %{pre_post_trans}
%{_sysconfdir}/X11
%{_libdir}/X11
%{_prefix}/X11R6
%endif
%dir %{_libdir}/xorg/modules
%dir %{_datadir}/X11
%dir %{_datadir}/X11/app-defaults
%dir %{_datadir}/X11/fontpath.d
%dir %{_datadir}/X11/xserver
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
%{_datadir}/X11/Cards
%{_datadir}/X11/Options
%{_libdir}/xorg/modules/*
# (anssi) We do not want this file to really exist, it is empty.
# This entry causes an rpm-build warning "file listed twice", but getting rid
# of the warning would need us to list all the other extensions one-by-one.
%ghost %{_libdir}/xorg/modules/extensions/libglx.so
%{_datadir}/X11/xserver/SecurityPolicy
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
%{_datadir}/X11/X
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
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1

%patch500 -p1
%patch501 -p1
%patch502 -p1
%patch503 -p1
%patch504 -p1
%patch505 -p1
%patch506 -p1
%patch507 -p1
%patch508 -p1
%patch509 -p1
%patch510 -p1
%patch511 -p1
%patch512 -p1
%patch513 -p1
%patch514 -p1
%patch515 -p1
%patch516 -p1
%patch517 -p1
%patch518 -p1
%patch519 -p1
%patch520 -p1
%patch521 -p1
%patch522 -p1
%patch523 -p1
%patch524 -p1
%patch525 -p1
%patch526 -p1
%patch527 -p1
%patch528 -p1
%patch529 -p1
%patch530 -p1

%build
autoreconf -ifs
%if %{with_debug}
CFLAGS='-DBUILDDEBUG -O0 -g3' \
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
		--with-serverconfig-path="%{_datadir}/X11/xserver" \
		--with-fontdir="%{_datadir}/fonts" \
		--with-default-font-path="catalogue:%{_datadir}/X11/fontpath.d"
pushd include && make xorg-server.h dix-config.h xorg-config.h && popd
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/X11/
ln -s %{_bindir}/Xorg %{buildroot}%{_datadir}/X11/X
ln -sf %{_bindir}/Xwrapper %{buildroot}%{_bindir}/X

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{_sourcedir}/xserver.pamd %{buildroot}%{_sysconfdir}/pam.d/xserver
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
touch %{buildroot}%{_sysconfdir}/security/console.apps/xserver

mkdir -p %{buildroot}%{_datadir}/X11/fontpath.d

# move README.compiled outside compiled/ dir, so there won't be any problem with x11-data-xkbdata
mv -f %{buildroot}%{_datadir}/X11/xkb/compiled/README.compiled %{buildroot}%{_datadir}/X11/xkb/

%if ! %{pre_post_trans}
ln -s %{_prefix} %{buildroot}%{_prefix}/X11R6
%endif
# Move anything that is still being installed in /usr/lib/X11 or /etc/X11
# to /usr/share/X11 and adjust symbolic link
for dir in %{buildroot}{%{_libdir},%{_sysconfdir}}/X11; do
    if [ -d $dir ]; then
	for file in `find $dir -maxdepth 1 -mindepth 1`; do
	    mv $file %{buildroot}%{_datadir}/X11/`basename $f`
	done
	rmdir $dir
    fi
%if ! %{pre_post_trans}
    ln -sf %{_datadir}/X11 $dir
%endif
done

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
