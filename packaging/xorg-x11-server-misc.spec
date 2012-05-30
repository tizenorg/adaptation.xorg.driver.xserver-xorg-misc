%ifarch %ix86
%define ARCH i386
%endif

%ifarch %{arm}
%define ARCH arm
%endif

Name:       xorg-x11-server-misc
Summary:    X.Org X11 X server misc packages
Version:    0.0.1
Release:    1
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1001: packaging/xorg-x11-server-misc.manifest 

%description
Description: %{summary}


%package emulfb
Summary:    X11 X server misc files for s5pc110
Group:      System/X11
Requires:   xserver-xorg-core

%description emulfb
Xorg server misc package which contains startx, xinitrc and xorg.conf file for emulfb


%prep
%setup -q -n %{name}-%{version}


%build
cp %{SOURCE1001} .
for f in `find %{ARCH}-common/ -name "*.in"`; do
        cat $f > ${f%.in};
        sed -i -e "s#@PREFIX@#/usr#g" ${f%.in};
        sed -i -e "s#@DATADIR@#/opt#g" ${f%.in};
        chmod a+x ${f%.in};
done

./autogen.sh
%configure --with-arch=%{ARCH} --with-conf-prefix=/opt

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

#rm -fr %{buildroot}/opt/etc/X11/xorg.conf.d*
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/%{_prefix}/etc/X11/
cp -af %{ARCH}-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af %{ARCH}-common/xresources %{buildroot}/etc/rc.d/init.d/
cp -af %{ARCH}-common/xinitrc %{buildroot}/%{_prefix}/etc/X11/
ln -sf /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S20xserver
ln -sf /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S20xserver
ln -sf /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc3.d/S80xresources
ln -sf /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
cp -af %{ARCH}-common/Xorg.sh %{buildroot}/etc/profile.d/
cp -af %{ARCH}-common/Xmodmap %{buildroot}/opt/etc/X11/

cp -rf %{ARCH}-emulfb %{buildroot}/opt/etc/X11/
mkdir -p %{buildroot}/opt/etc/X11/xorg.conf.d

%post emulfb
if [ -d /opt/etc/X11/xorg.conf.d ]; then
    rm -rf /opt/etc/X11/xorg.conf.d
    ln -sf /opt/etc/X11/xorg.conf.d.default /opt/etc/X11/xorg.conf.d
fi
ln -s /opt/etc/X11/%{ARCH}-emulfb/* /opt/etc/X11/  

%preun emulfb
rm -f /opt/etc/X11/Xmodmap
rm -f /opt/etc/X11/xorg.conf.d.*

%post
chown -R 5000:5000 /opt/etc/X11/Xresources

%files emulfb
%manifest xorg-x11-server-misc.manifest
/opt/etc/X11/xorg.conf.d
%{_sysconfdir}/profile.d/Xorg.sh
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
/opt/etc/X11/Xresources
/opt/etc/X11/xorg.conf
%{_prefix}/etc/X11/xinitrc
%{_bindir}/setcpu
%{_bindir}/setpoll
%{_bindir}/startx
/opt/etc/X11/Xmodmap
/opt/etc/X11/%{ARCH}-emulfb/*

