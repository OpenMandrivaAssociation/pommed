# Taken from SUSE and initially modified for Mandriva by Sherwin
# Daganato: thanks

Summary:	Apple laptops hotkeys event handler
Name:		pommed
Version:	1.39
Release:	4
License:	GPLv2
Group:		System/Kernel and hardware
URL:		https://technologeek.org/projects/pommed/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.service
Requires:	eject
BuildRequires:	dbus-devel
BuildRequires:	confuse-devel
BuildRequires:	libsmbios-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	desktop-file-utils
BuildRequires:  dbus-glib-devel
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

pommed also monitors the ambient light sensors to automatically light
up the keyboard backlight on the MacBook Pro and PowerBook.

Optional support for the Apple Remote control is available.

%package -n gpomme
Summary:	Graphical client for pommed
Group:		System/Kernel and hardware
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
Group:		System/Kernel and hardware
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
sed -i -e "s/CFLAGS = -g -O2 /CFLAGS += /" -e "s/LDFLAGS =/LDFLAGS +=/" */Makefile

%build
perl -pi -e 's,/usr/lib,%{_libdir},g' pommed/Makefile
CFLAGS="%{optflags}" %make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -d %{buildroot}%{_unitdir}
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
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/pommed.service
install -m 644 pommed.1 %{buildroot}%{_mandir}/man1
# gpomme
install -m 755 gpomme/gpomme %{buildroot}%{_bindir}
install -m 644 gpomme/gpomme.1 %{buildroot}%{_mandir}/man1
install -m 644 gpomme/*.desktop %{buildroot}%{_datadir}/applications
for i in {16x16,22x22,24x24,32x32,48x48,64x64,72x72,96x96,128x128}; \
do install -m 644 icons/gpomme_$i.png %{buildroot}%{_iconsdir}/hicolor/$i/apps/gpomme.png; done
install -m 644 icons/gpomme.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/gpomme.svg
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

%files
%doc AUTHORS README TODO
%config(noreplace) /etc/pommed.conf
%config(noreplace) /etc/dbus-1/system.d/pommed.conf
%{_unitdir}/pommed.service
%{_sbindir}/pommed
%{_mandir}/man1/po*

%files -n gpomme -f gpomme.lang
%{_bindir}/gpomme
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/gpomme
%{_mandir}/man1/gpo*

%files -n wmpomme
%{_bindir}/wmpomme
%{_iconsdir}/wmpomme.xpm
%{_mandir}/man1/wmpo*
