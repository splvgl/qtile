#!/bin/bash

# autostart only if not already running
function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}


# systray stuff
run nm-applet
run blueberry-tray
run volumeicon

# compositor and wallpaper
run picom -b
run nitrogen --restore

# enabling natural scrolling for touchpad
run xinput set-prop 13 317 1

# automatically set the screen color temperature at night
time=$(date +%H)
(("$time" > "21")) || (("$time" < "7")) && sct 3500 || sct

# enabling touchpad gestures
run libinput-gestures-setup restart

# notifications using dunst
run dunst

# hide mouse cursor when not in use
run unclutter

# policykit
run lxsession -e QTILE
