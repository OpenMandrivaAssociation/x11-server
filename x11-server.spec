%define with_debug 0
%define kdrive_builds_vesa 0
%define enable_xvnc 0

%define mesasrcdir %{_prefix}/src/Mesa
%define mesaver 6.5.3

%ifarch %{ix86} alpha
%define kdrive_builds_vesa 1
%endif

Name: x11-server
Version: 1.3.0.0
Release: %mkrel 3
Summary:  X11 servers
Group: System/X11
Source: http://xorg.freedesktop.org/releases/individual/xserver/xorg-server-%{version}.tar.bz2
Source1: xserver.pamd
# xvfb-run script and manpage from debian's xorg-server source package
Source2: xvfb-run
Source3: xvfb-run.man.pre
License: MIT
BuildRoot: %{_tmppath}/%{name}-root
Obsoletes: x11-server13 <= 1.2.99.905

BuildRequires: libdmx-devel >= 1.0.1
BuildRequires: libfontenc-devel >= 1.0.1
BuildRequires: libmesagl-devel >= %{mesaver}
BuildRequires: libxau-devel >= 1.0.0
BuildRequires: libxaw-devel >= 1.0.1
BuildRequires: libxdmcp-devel >= 1.0.0
BuildRequires: libxext-devel >= 1.0.0
BuildRequires: libxfont-devel >= 1.0.0
BuildRequires: libxfixes-devel
BuildRequires: libxi-devel >= 1.0.0
BuildRequires: libxkbfile-devel >= 1.0.1
BuildRequires: libxau-devel >= 1.0.0
BuildRequires: libxkbui-devel >= 1.0.1
BuildRequires: libxmu-devel >= 1.0.0
BuildRequires: libxpm-devel >= 3.5.4.2
BuildRequires: libxrender-devel >= 0.9.0.2
BuildRequires: libxres-devel >= 1.0.0
BuildRequires: libxtst-devel >= 1.0.1
BuildRequires: libxxf86misc-devel >= 1.0.0
BuildRequires: libxxf86vm-devel >= 1.0.0
BuildRequires: libxfont-devel >= 1.0.0
BuildRequires: mesa-source >= %{mesaver}
BuildRequires: x11-proto-devel >= 1.0.3-2
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: x11-xtrans-devel >= 1.0.0
BuildRequires: libdmx-devel >= 1.0.1
BuildRequires: libpam-devel
BuildRequires: SDL-devel
# for VNC:
BuildRequires: libjpeg-devel


# --------- Patches ----------------------------------------------------------
Patch3:  0003-Use-a-X-wrapper-that-uses-pam-and-consolehelper-to-give-X-root-privileges.txt
Patch4:  0004-Blue-background-on-startup.txt
Patch7:  0007-find-free-VT.txt
Patch10: 0010-Xephyr-evdev-support.txt 
Patch17: 0017-Fix-index-matching-of-visuals.txt 
Patch18: 0018-vnc-support.txt 
Patch32: 0032-no-move-damage.txt
Patch33: 0033-dont-backfill-bg-none.txt
Patch34: 0034-offscreen-pixmaps.txt
Patch37: 0037-fdo8991-xorg-server-1.1.99.901-glXDRIbindTexImage-target.txt
Patch38: 0038-fdo9367-libdrm-ignore-load-requests-fixes-fglrx.txt
Patch40: xorg-server-1.2.0-xvfb-run.patch
Patch42: x11-server-64bit_fixes.patch

Patch43: xorg-server-1.3.0.0-mesa-6.5.3.patch
Patch44: xorg-server-1.3.0.0-glinterface.patch
Patch45: xorg-server-1.3.0.0-glinterface2.patch

# -----------------------------------------------------------------------------

Requires: %{name}-xorg
Requires: %{name}-xdmx
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
%{_includedir}/X11/bitmaps/*
%{_includedir}/X11/pixmaps/*
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
Requires: rgb
# for 'fixed' and 'cursor' fonts
Requires: x11-font-misc-misc
Requires: x11-font-cursor-misc
Requires: x11-font-alias                                                  

%description common
X server common files

%files common
%defattr(-,root,root)
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xserver
%{_bindir}/xorgcfg
%{_bindir}/xorgconfig
%{_bindir}/gtf
%{_bindir}/cvt
%{_bindir}/in*
%{_bindir}/ioport
%{_bindir}/out*
%{_bindir}/pcitweak
%{_bindir}/scanpci
%{_bindir}/vdltodmx
%{_libdir}/X11/Cards
%{_libdir}/X11/Options
%{_libdir}/xorg/modules/*
%{_libdir}/xserver/SecurityPolicy
%{_datadir}/X11/xkb/README.compiled
%{_mandir}/man1/xorgcfg.*.bz2
%{_mandir}/man1/xorgconfig.*.bz2
%{_mandir}/man1/gtf.*.bz2
%{_mandir}/man1/cvt.1.bz2
%{_mandir}/man1/pcitweak.*.bz2
%{_mandir}/man1/scanpci.*.bz2
%{_mandir}/man1/vdltodmx.*.bz2
%{_mandir}/man4/fbdevhw.4.bz2
%{_mandir}/man4/exa.4.bz2

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
#Obsoletes: xorg-x11-server < 7.0
#Provides: xorg-x11-server = 7.0

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
%{_mandir}/man1/Xorg.*.bz2
%{_mandir}/man1/Xserver.*.bz2
%{_mandir}/man5/xorg.conf.*.bz2

#------------------------------------------------------------------------------

%package xdmx
Summary: Distributed Multi-head X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}
#Obsoletes: xorg-x11-Xdmx < 7.0
#Provides: xorg-x11-Xdmx = 7.0

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
%{_mandir}/man1/Xdmx.*.bz2
%{_mandir}/man1/xdmxconfig.*.bz2
%{_mandir}/man1/dmxtodmx.*.bz2

#------------------------------------------------------------------------------

%package xnest
Summary: A nested X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}
#Obsoletes: xorg-x11-Xnest < 7.0
#Provides: xorg-x11-Xnest = 7.0

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
%{_mandir}/man1/Xnest.*.bz2

#------------------------------------------------------------------------------

%package xvfb
Summary: X virtual framebuffer server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}
Requires: xauth
#Obsoletes: xorg-x11-Xvfb < 7.0
#Provides: xorg-x11-Xvfb = 7.0

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
%{_mandir}/man1/Xvfb.*.bz2
%{_mandir}/man1/xvfb-run.*.bz2

#------------------------------------------------------------------------------

%if %enable_xvnc
%package xvnc
Summary: X VNC server
Group: System/X11
License: GPL
Requires: x11-server-common = %{version}-%{release}
#Obsoletes: xorg-x11-Xvnc < 7.0
#Provides: xorg-x11-Xvnc = 7.0

%description xvnc
Xvnc is a virtual X Windows System server like Xvfb, but it allows 
VNC clients access to the 'virtual' display it provides.

%files xvnc
%defattr(-,root,root)
%{_bindir}/Xvnc
#{_mandir}/man1/Xvnc.*.bz2

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
 
%package xneomagic
Summary: KDrive neomagic X server
Group: System/X11
License: MIT
Requires: x11-server-common = %{version}-%{release}

%description xneomagic
KDrive (formerly known as TinyX) is a light-weight X server targetting specific
chipsets. It is recommended to be used on thin-clients and embedded systems.
If you are on a standard desktop system you might want to use x11-server-xorg
and the video driver corresponding to your video card.

This KDrive server is targetted for neomagic chipsets.

%if %kdrive_builds_vesa
%files xneomagic
%defattr(-,root,root)
%{_bindir}/Xneomagic
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

# xvfb-run
cp %{SOURCE2} %{SOURCE3} hw/vfb/

#patches
%patch43 -p2 -b .mesa653
%patch44 -p1 -b .glinterface
%patch45 -p0 -b .glinterface2

%patch3  -p1 -b .xwrapper
%patch4  -p1 -b .blue_bg
%patch7  -p1 -b .vt7
%patch10 -p1 -b .evdev
%patch17 -p1 -b .visual_index_matching
%if %enable_xvnc
%patch18 -p1 -b .vnc
%endif
%patch32 -p0 -b .no_move_damage
%patch33 -p0 -b .dont_backfill
%patch34 -p0 -b .offscreen_pixmaps
%patch37 -p1 -b .glxdribindteximage
%patch38 -p0 -b .libdrm_fix
%patch40 -p1 -b .xvfb
%patch42 -p1 -b .64bit_fixes

%build
aclocal && autoconf && automake
%configure2_5x  --x-includes=%{_includedir} \
                --x-libraries=%{_libdir} \
 		--with-log-dir=%{_logdir} \
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
  		--enable-xorg-vnc \
  		--enable-xvnc \
  		--disable-xdmx-vnc \
		%endif
  		--enable-dmx \
  		--enable-xvfb \
  		--enable-xnest \
  		--disable-xwin \
  		--disable-xprint \
  		--disable-xgl \
  		--disable-xglx \
  		--disable-xegl \
  		--enable-kdrive \
  		--enable-xephyr \
  		--enable-xsdl \
		--disable-freetype \
  		--disable-install-setuid \
 		--enable-secure-rpc \
  		--enable-xorgcfg \
  		--enable-kbd_mode \
		--enable-xwrapper \
		--enable-pam \
		--with-fontdir="%{_datadir}/fonts" \
		--with-default-font-path="%{_datadir}/fonts/misc:unscaled,unix/:-1"
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

# move README.compiled outside compiled/ dir, so there won't be any problem with x11-data-xkbdata
mv -f %{buildroot}%{_datadir}/X11/xkb/compiled/README.compiled %{buildroot}%{_datadir}/X11/xkb/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)


