#!/bin/sh

cat <<EOF | xmenu -r | sh &
Applications
	IMG:/home/.config/qtile/icons/web.png	Web Browser	brave
	IMG:./../icons/gimp.png	Image editor	gimp
	IMG:./icons/gimp.png	Image yeeter	gimp
Terminal (termite)	termite

Shutdown		poweroff
Reboot			reboot
EOF
