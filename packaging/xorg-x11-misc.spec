#sbs-git:slp/pkgs/xorg/driver/xserver-xorg-misc xserver-xorg-misc 0.0.1 13496ac354ad7f6709f1ef9b880a206a2df41c80

%ifarch %ix86
%define ARCH i386
%endif

%ifarch %{arm}
%define ARCH arm
%endif

Name:	xorg-x11-misc
Summary:    X.Org X11 X server misc packages
Version: 0.0.1
Release:    99
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz

%description
Description: %{summary}

%package emulfb
Summary:    X11 X server misc files for emulfb
Group:      System/X11
Requires:   xserver-xorg-core

%description emulfb
Xorg server misc package which contains startx, xinitrc and xorg.conf file for emulfb

%prep
%setup -q

%build
{
for f in `find %{ARCH}-common/ -name "*.in"`; do
	cat $f > ${f%.in};
	sed -i -e "s#@PREFIX@#/usr#g" ${f%.in};
	sed -i -e "s#@DATADIR@#/opt#g" ${f%.in};
	chmod a+x ${f%.in};
done
}

%reconfigure \
	--with-arch=%{ARCH} \
	--with-conf-prefix=/opt

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

rm -fr %{buildroot}/opt/etc/X11/xorg.conf.d*
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/%{_prefix}/etc/X11/
cp -af %{ARCH}-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af %{ARCH}-common/xresources %{buildroot}/etc/rc.d/init.d/
cp -af %{ARCH}-common/xinitrc %{buildroot}/%{_prefix}/etc/X11/
cp -af %{ARCH}-common/xsetrc %{buildroot}/%{_prefix}/etc/X11/
cp -af %{ARCH}-common/Xmodmap %{buildroot}/opt/etc/X11/
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
cp -af %{ARCH}-common/Xorg.sh %{buildroot}/etc/profile.d/

cp -rf %{ARCH}-emulfb %{buildroot}/opt/etc/X11/

%post emulfb
ln -s /opt/etc/X11/%{ARCH}-emulfb/* /opt/etc/X11/

%preun
rm -f /opt/etc/X11/Xmodmap
rm -f /opt/etc/X11/xorg.conf.d.*

%files emulfb
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/Xorg.sh
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%attr(-,inhouse,inhouse) /opt/etc/X11/Xresources
%{_prefix}/etc/X11/xinitrc
%{_prefix}/etc/X11/xsetrc
/opt/etc/X11/Xmodmap
%ifarch %{arm}
/opt/etc/X11/xorg.conf
/opt/etc/X11/arm-emulfb/xorg.conf.d.*/*.conf
%else
/opt/etc/X11/xorg.conf
/opt/etc/X11/i386-emulfb/xorg.conf.d/*
%endif
%{_bindir}/setcpu
%{_bindir}/setpoll
%{_bindir}/startx

