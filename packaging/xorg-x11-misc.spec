%ifarch %ix86
%define ARCH i386
%endif

%ifarch %{arm}
%define ARCH arm
%endif

Name:	    xorg-x11-misc
Summary:    X.Org X11 X server misc packages
Version:    0.0.10
Release:    1
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz

%description
Description: %{summary}

%package common
Summary:    architecture independent set of X11 X server configuration files
Group:      System/X11
Requires:   xserver-xorg-core
Requires:   xorg-x11-drv-evdev-multitouch

%description common
Set of architecture independent files and scripts for X server

%package %{ARCH}-common
Summary:    X11 X server misc files for %{ARCH}
Group:      System/X11
Requires:   %{name}-common = %{version}

%description %{ARCH}-common
Set of architecture depended files and scripts for X server

# emulfb

%package emulfb
Summary:    X11 X server misc files for emulated framebuffer device
Group:      System/X11
Requires:   %{name}-%{ARCH}-common = %{version}
Provides:   xserver-xorg-misc-emulfb = %{version}

%description emulfb
Xorg server misc package which contains device specific configuration files


%prep
%setup -q

%install

mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}-emulfb


mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/X11/xorg.conf.d
mkdir -p %{buildroot}/etc/X11/arch-preinit.d
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/etc/rc.d/rc3.d
mkdir -p %{buildroot}/etc/rc.d/rc4.d
mkdir -p %{buildroot}/etc/profile.d

%ifarch %{arm}
install -m 755 common/startx %{buildroot}/usr/bin/startx
install -m 755 common/xinitrc %{buildroot}/etc/X11/xinitrc
install -m 755 common/xresources %{buildroot}/etc/rc.d/init.d/xresources
%endif

%ifarch %ix86
install -m 755 %{ARCH}-common/startx %{buildroot}/usr/bin/startx
install -m 755 %{ARCH}-common/xinitrc %{buildroot}/etc/X11/xinitrc
install -m 755 %{ARCH}-common/xresources %{buildroot}/etc/rc.d/init.d/xresources
%endif

install -m 755 common/scripts/setcpu %{buildroot}/usr/bin/setcpu
install -m 755 common/scripts/setpoll %{buildroot}/usr/bin/setpoll
install -m 644 common/xorg.conf %{buildroot}/etc/X11/xorg.conf

install -m 755 common/Xorg.sh %{buildroot}/etc/profile.d/Xorg.sh
install -m 755 common/xserver %{buildroot}/etc/rc.d/init.d/xserver

install -m 644 %{ARCH}-common/Xmodmap %{buildroot}/etc/X11/Xmodmap
install -m 644 %{ARCH}-common/Xresources %{buildroot}/etc/X11/Xresources
install -m 644 %{ARCH}-common/Xorg.arch-options %{buildroot}/etc/X11/Xorg.arch-options
install -m 755 %{ARCH}-common/xsetrc %{buildroot}/etc/X11/xsetrc

if [ -d %{ARCH}-common/arch-preinit.d ]; then
    cp -a %{ARCH}-common/arch-preinit.d %{buildroot}/etc/X11/
fi

%ifarch %ix86
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S20xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S20xserver
%endif

%ifarch %{arm}
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S02xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S02xserver
%endif

ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc3.d/S80xresources
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
%if "%{?tizen_profile_name}" == "wearable"
cp -Rd conf-%{ARCH}-emulfb-wearable %{buildroot}/etc/X11/conf-%{ARCH}-emulfb
%else
cp -Rd conf-%{ARCH}-emulfb-mobile %{buildroot}/etc/X11/conf-%{ARCH}-emulfb
%endif

# XXX Copy-paste terror - could some rpm guy help me unify this?

%ifarch %{ix86}
mkdir -p %{buildroot}%{_libdir}/systemd/system/basic.target.wants
install -m 0644 %{ARCH}-common/xorg.service %{buildroot}%{_libdir}/systemd/system/xorg.service
ln -s ../xorg.service %{buildroot}%{_libdir}/systemd/system/basic.target.wants/xorg.service
mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants
install -m 0644 %{ARCH}-common/xresources.service %{buildroot}%{_libdir}/systemd/system/xresources.service
ln -s ../xresources.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
%endif

# arm/i386 emulfb

%post emulfb
mkdir -p /etc/X11/xorg.conf.d
for i in /etc/X11/conf-%{ARCH}-emulfb/*; do
    f="${i##*/}"
    d="/etc/X11/xorg.conf.d/$f"
    rm -f "$d"
    ln -s "$i" "$d"
done

%files common
/usr/bin/startx
/usr/bin/setcpu
/usr/bin/setpoll
/etc/X11/xinitrc
/etc/profile.d/Xorg.sh
/etc/rc.d/init.d/*
/etc/rc.d/rc3.d/*
/etc/rc.d/rc4.d/*
/etc/X11/xorg.conf


%files %{ARCH}-common
/etc/X11/Xmodmap
/etc/X11/Xresources
%attr(755,root,root) /etc/X11/xsetrc
/etc/X11/Xorg.arch-options
%dir /etc/X11/arch-preinit.d
/etc/X11/arch-preinit.d/*

%ifarch %{ix86}
%files emulfb
%manifest xorg-x11-misc-emulfb.manifest
/usr/share/license/%{name}-emulfb
/etc/X11/conf-%{ARCH}-emulfb/*
%{_libdir}/systemd/system/xorg.service
%{_libdir}/systemd/system/basic.target.wants/xorg.service
%{_libdir}/systemd/system/xresources.service
%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
%endif

%ifarch %{arm}

%files emulfb
%manifest xorg-x11-misc-emulfb.manifest
/usr/share/license/%{name}-emulfb
/etc/X11/conf-%{ARCH}-emulfb/*

%endif
