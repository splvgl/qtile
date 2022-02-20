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
run picom -b --experimental-backends
run nitrogen --restore
# run variety

# setting cursor speed for touchpad
run xinput set-prop 13 326 0.35

# enabling natural scrolling for touchpad
run xinput set-prop 13 317 1

# hide mouse cursor when not in use
run unclutter

# automatically set the screen color temperature at night
time=$(date +%H)
(("$time" > "21")) || (("$time" < "7")) && sct 3500 || sct

# enabling touchpad gestures
run libinput-gestures-setup restart

# notifications using dunst
run dunst

# policykit
run lxsession -e QTILE

# latte-dock (configured in Plasma)
run latte-dock
