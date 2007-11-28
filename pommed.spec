# Taken from SUSE and initially modified for Mandriva by Sherwin
# Daganato: thanks

Summary:	Apple laptops hotkeys event handler
Name:		pommed
Version:	1.12
Release:	%mkrel 1
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://technologeek.org/projects/pommed/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	eject
BuildRequires:	libalsa-devel 
BuildRequires:	libaudiofile-devel
BuildRequires:	dbus-devel
BuildRequires:	gtk+2-devel
BuildRequires:	confuse-devel
BuildRequires:	libglade2-devel
BuildRequires:	libsmbios-devel
BuildRequires:	pciutils-devel
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	xpm-devel

%description
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

pommed also monitors the ambient light sensors to automatically light
up the keyboard backlight on the MacBook Pro and PowerBook.

Optional support for the Apple Remote control is available.

%package -n gpomme
Summary:	graphical client for pommed
Group:		Hardware/Mobile
Requires:	pommed
Requires:	dbus

%description -n gpomme
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

gpomme is a graphical client for pommed. It listens for signals sent by
pommed on DBus and displays the action taken by pommed along with the
current state associated to this action.

%package -n wmpomme
Summary:	WindowMaker dockapp client for pommed
Group:		Hardware/Mobile
Requires:	pommed
Requires:	dbus

%description -n wmpomme
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

wmpomme is a dockapp client for pommed. It displays the current level
of each item controlled by pommed.

%prep
%setup -q

%build
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,72x72,96x96,128x128,scalable}/apps
mkdir -p %{buildroot}%{_datadir}/gpomme
mkdir -p %{buildroot}%{_datadir}/locale
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 pommed/pommed %{buildroot}%{_sbindir}
%ifarch ppc ppc64
install -m 644 pommed.conf.pmac %{buildroot}%{_sysconfdir}/pommed.conf
%else
install -m 644 pommed.conf.mactel %{buildroot}%{_sysconfdir}/pommed.conf
%endif
install -m 644 dbus-policy.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/pommed.conf
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/pommed
install -m 644 pommed.1 %{buildroot}%{_mandir}/man1
# gpomme
install -m 755 gpomme/gpomme %{buildroot}%{_bindir}
install -m 644 gpomme/gpomme.1 %{buildroot}%{_mandir}/man1
install -m 644 gpomme/*.desktop %{buildroot}%{_datadir}/applications
for i in {16x16,22x22,24x24,32x32,48x48,64x64,72x72,96x96,128x128}; \
do install -m 644 icons/gpomme_$i.png %{buildroot}%{_iconsdir}/hicolor/$i/apps/gpomme.png; done
install -m 644 icons/gpomme.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/gpomme.svg
install -m 644 gpomme/gpomme.glade %{buildroot}%{_datadir}/gpomme
cp -a gpomme/themes %{buildroot}%{_datadir}/gpomme
rm -rfv %{buildroot}%{_datadir}/gpomme/themes/src
for mo in gpomme/po/*.mo ; do
    lang=`basename $mo .mo`
    mkdir -p %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
    install -m 644 $mo %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/gpomme.mo
done
# wmpomme
install -m 755 wmpomme/wmpomme %{buildroot}%{_bindir}
install -m 644 wmpomme/wmpomme.1 %{buildroot}%{_mandir}/man1
install -m 644 icons/gpomme_32x32.xpm %{buildroot}%{_iconsdir}/wmpomme.xpm

desktop-file-install --vendor="" \
  --remove-category="Utility" \
  --add-category="GTK" \
  --add-category="System" \
  --add-category="Monitor" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang gpomme

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README TODO
%config(noreplace) /etc/pommed.conf
%config(noreplace) /etc/dbus-1/system.d/pommed.conf
%{_initrddir}/pommed
%{_sbindir}/pommed
%{_mandir}/man1/po*

%files -n gpomme -f gpomme.lang
%defattr(-,root,root)
%{_bindir}/gpomme
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/gpomme
%{_mandir}/man1/gpo*

%files -n wmpomme
%defattr(-,root,root)
%{_bindir}/wmpomme
%{_iconsdir}/wmpomme.xpm
%{_mandir}/man1/wmpo*

