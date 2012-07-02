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
%configure --with-arch=%{ARCH}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d/
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc3.d/
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc4.d/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
mkdir -p %{buildroot}/opt/%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/X11/
ln -sf %{_sysconfdir}/X11 %{buildroot}/opt/%{_sysconfdir}/X11
cp -af %{ARCH}-common/xserver %{buildroot}%{_sysconfdir}/rc.d/init.d/
cp -af %{ARCH}-common/xresources %{buildroot}%{_sysconfdir}/rc.d/init.d/
cp -af %{ARCH}-common/xinitrc %{buildroot}/%{_sysconfdir}/X11/
ln -sf %{_sysconfdir}/rc.d/init.d/xserver %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S20xserver
ln -sf %{_sysconfdir}/rc.d/init.d/xserver %{buildroot}%{_sysconfdir}/rc.d/rc4.d/S20xserver
ln -sf %{_sysconfdir}/rc.d/init.d/xresources %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S80xresources
ln -sf %{_sysconfdir}/rc.d/init.d/xresources %{buildroot}%{_sysconfdir}/rc.d/rc4.d/S80xresources
cp -af %{ARCH}-common/Xorg.sh %{buildroot}%{_sysconfdir}/profile.d/
cp -af %{ARCH}-common/Xmodmap %{buildroot}/%{_sysconfdir}/X11/

cp -rf %{ARCH}-emulfb %{buildroot}/%{_sysconfdir}/X11/
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

ln -s %{_sysconfdir}/X11/%{ARCH}-emulfb/xorg.conf.d.default/ %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

mv %{buildroot}/opt/%{_sysconfdir}%{_sysconfdir}/X11/Xresources %{buildroot}%{_sysconfdir}/X11/Xresources
mv %{buildroot}/opt/%{_sysconfdir}%{_sysconfdir}/X11/xorg.conf %{buildroot}%{_sysconfdir}/X11/xorg.conf

%files emulfb
%manifest xorg-x11-server-misc.manifest
%{_sysconfdir}/profile.d/Xorg.sh
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%{_sysconfdir}/X11/xinitrc
%{_bindir}/setcpu
%{_bindir}/setpoll
%{_bindir}/startx
%config %{_sysconfdir}/X11/Xmodmap
/opt/%{_sysconfdir}/X11
%ifarch %{ix86}
   %{_sysconfdir}/X11/%{ARCH}-emulfb/xorg.conf.d/dummy
%else
   %config %{_sysconfdir}/X11/arm-emulfb/xorg.conf.d.default/display.conf
   %config %{_sysconfdir}/X11/arm-emulfb/xorg.conf.d.default/input.conf
%endif
%{_sysconfdir}/X11/xorg.conf.d
%config %attr(-,app,app) %{_sysconfdir}/X11/Xresources
%config %{_sysconfdir}/X11/xorg.conf
