Name:       xorg-x11-server-misc
Summary:    X.Org X11 X server misc packages
Version:    0.0.1
Release:    99
ExclusiveArch:  %arm
Group:      System/X11
License:    MIT
Source0:    xserver-xorg-misc-%{version}.tar.gz

%description
Description: %{summary}


%package emulfb
Summary:    X11 X server misc files for emulfb
Group:      System/X11
Requires:   xorg-x11-server-core

%description emulfb
Xorg server misc package which contains startx, xinitrc and xorg.conf file for emulfb


%prep
%setup -q -n xserver-xorg-misc-%{version}


%build
{
for f in `find arm-common/ -name "*.in"`; do
	cat $f > ${f%.in};
	sed -i -e "s#@PREFIX@#/usr#g" ${f%.in};
	sed -i -e "s#@DATADIR@#/opt#g" ${f%.in};
	chmod a+x ${f%.in};
done
}

%reconfigure \
	--with-arch=arm \
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
cp -af arm-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xresources %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xinitrc %{buildroot}/%{_prefix}/etc/X11/
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S20xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S20xserver
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc3.d/S80xresources
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
cp -af arm-common/Xorg.sh %{buildroot}/etc/profile.d/
cp -af arm-common/Xmodmap %{buildroot}/opt/etc/X11/

cp -rf arm-emulfb %{buildroot}/opt/etc/X11/

%post emulfb
ln -s /opt/etc/X11/arm-emulfb/* /opt/etc/X11/

%preun
rm -f /opt/etc/X11/Xmodmap
rm -f /opt/etc/X11/xorg.conf.d.*

%files emulfb
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/Xorg.sh
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%attr(-,5000,5000) /opt/etc/X11/Xresources
/opt/etc/X11/xorg.conf
%{_prefix}/etc/X11/xinitrc
/opt/etc/X11/arm-common/Xmodmap
/opt/etc/X11/arm-emulfb/xorg.conf.d.*/*.conf
%{_bindir}/setcpu
%{_bindir}/setpoll
%{_bindir}/startx

