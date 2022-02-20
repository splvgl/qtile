# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, qtile
from libqtile.widget import Spacer
from widgets import pacman_widget, battery_icon

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

myterminal = "alacritty"


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [

# FULLSCREEN MODE
    Key([mod], "f", lazy.window.toggle_fullscreen()),

# TOGGLE BAR VISIBILITY
    #Key([mod], "f", lazy.hide_show_bar("top")),

# LOCKSCREEN

# QUITTING AND RELOADING
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod, "shift"], "space", lazy.prev_layout()),


# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "control"], "space", lazy.window.toggle_floating()),

# APPLICATION LAUNCHING
    # WEB BROWSER
    Key([mod], "b", lazy.spawn("brave")),
    Key([mod, "shift"], "b", lazy.spawn("brave --incognito")),
    # TERMINAL 
    Key([mod], "Return", lazy.spawn(myterminal)),
    # FILE MANAGERS
    Key([mod], "y", lazy.spawn("urxvt -e ranger")),
    Key([mod, "shift"], "y", lazy.spawn("nautilus")),
    # ROFI LAUNCHER
    # Key([mod], "r", lazy.spawn("rofi -modi combi -combi-modi window,drun -show combi -icon-theme Sardi-Arc -show-icons")),
    Key([mod], "r", lazy.spawn("rofi -modi combi -combi-modi window,drun -show combi")),
    # Key([mod], "r", lazy.spawn("rofi -show drun -config ~/.config/rofi/blurry.rasi")),
    # SLEEP TIMER
    Key([mod], "XF86PowerOff", lazy.spawn("/home/henrik/Dev/fish/sleep-timer.sh")),
    # POWER MODE SELECTOR
    Key([mod, "shift"], "p", lazy.spawn("fish -c pmenu")),

# FUNCTION KEYS
    # AUDIO CONTROL
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key(["shift"], "XF86AudioPlay", lazy.spawn("playerctl previous")),
    Key([mod], "XF86AudioPlay", lazy.spawn("playerctl next")),
    # BRIGHTNESS CONTROLL
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 4")),
    # LOGOUT MENU (arcolinux-logout)
    Key([], "XF86PowerOff", lazy.spawn("arcolinux-logout")),

    # Window switcher
    Key([mod], "Tab", lazy.spawn("rofi -show window -width 70 -location 2 -no-fixed-num-lines")),
    # Key([mod], "Tab", lazy.spawn("rofi -show window -config ~/.config/rofi/blurry.rasi")),
    
    # change variety wallpaper
    Key([mod], "n", lazy.spawn("variety -n")),
    Key([mod], "p", lazy.spawn("variety -p")),
    Key([mod], "s", lazy.spawn("variety -f")),

    ]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
group_labels = ["1","2","3","4","5","6","7","8","9","0",]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "max",]

# group_labels = ["λ", "π", "τ", "ω", "ν"]
# group_names = [str(i+1) for i in range(len(group_labels))]
# group_layouts = ["monadtall" for i in range(len(group_labels))]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]
#group_layouts = ["monadtall", "max", "monadwide", "matrix",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":8,
            "border_width":2,
            "border_focus": "#02dfe3", #"#3384d0", #"#5e81ac",
            "border_normal": "#000000" #"#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme, single_border_width = 0),
    layout.Max(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    #layout.RatioTile(**layout_theme),
]

# COLORS FOR THE BAR

def init_colors():
    return [["#2F343F", "#2F343F"], # color 0
            ["#000000", "#000000"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"]] # color 9


colors = init_colors()

# ADD COLORS FOR LINUX WALLPAPER
colors += [["#689d69", "#689d69"], ["#458587", "#458587"], ["#d79922", "#d79922"], ["#cc231c", "#cc231c"]]
    
# WIDGET FUNCTIONS
def pacman_update():
    qtile.cmd_spawn("alacritty -e 'sudo pacman -Syu'")

def arco_menu():
    subprocess.call(home + "/Programs/xmenu/xmenu.sh")

def rofi_windows():
    qtile.cmd_spawn("rofi -show window -no-fixed-num-lines -width 70 -location 2")

# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 18,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()
widget_spacing = 15

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
            # widget.Sep(
                # linewidth = 0,
                # padding = 12,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            widget.Image(
                filename = '~/.config/qtile/icons/arco2.png',
                margin_y = 2,
                margin_x = 0,
                mouse_callbacks = {'Button1': arco_menu},
                ),
            widget.Spacer(length = widget_spacing),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            widget.GroupBox(
                font="FontAwesome",
                fontsize = 18,
                margin_y = 3,
                margin_x = 0,
                padding_y = 0,
                padding_x = 5,
                borderwidth = 2,
                disable_drag = True,
                active = colors[8],
                inactive = colors[2],
                rounded = True,
                highlight_method = "border",
                this_current_screen_border = colors[8],
                foreground = colors[2],
                background = "#000000"
                ),
            widget.Spacer(length = widget_spacing),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            widget.CurrentLayoutIcon(
                font = "Noto Sans Bold",
                foreground = colors[5],
                background = colors[1],
                scale = 0.7
                ),
            widget.Spacer(length = widget_spacing),
            widget.Systray(
                background=colors[1],
                icon_size=22,
                padding = 8
                ),
            widget.Spacer(length = widget_spacing),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            # widget.Image(
                # filename = home + '/Pictures/topleft.png',
                # margin_y = 0,
                # margin_x = 0,
                # background = "#282828",
                # ),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            widget.WindowName(font="Noto Sans",
                foreground = colors[2],
                padding = 50,
                # background = "#282828", #colors[11],
                max_chars = 90,
                mouse_callbacks = {'Button1': rofi_windows},
                ),
            widget.Spacer(length = widget_spacing),
            # widget.Image(
                # filename = home + '/Pictures/topright.png',
                # margin_y = 0,
                # margin_x = 0,
                # background = "#282828",
                # ),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            widget.GenPollText(
                func = pacman_widget.pacman_dots,
                font="FontAwesome",
                update_interval = 300,
                mouse_callbacks = {'Button1': pacman_update},
                ),
            widget.Image(
                filename = '~/.config/qtile/icons/pacman.png',
                scale = 0.4,
                mouse_callbacks = {'Button1': pacman_update},
                ),
            widget.Spacer(length = widget_spacing),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            # widget.TextBox(
                # font="FontAwesome",
                # text="  ", # temp icon
                # foreground=colors[3],
                # background=colors[1],
                # padding = 0,
                # ),
            # widget.ThermalSensor(
                # foreground = colors[5],
                # foreground_alert = colors[6],
                # background = colors[1],
                # metric = True,
                # padding = 3,
                # threshold = 80
                # ),
            # widget.TextBox(
                # font="FontAwesome",
                # text="  ", # CPU icon
                # foreground=colors[6],
                # background=colors[1],
                # padding = 0,
                # ),
            # widget.CPU(
                # format = '{freq_current}GHz @ {load_percent}%'
                # ),
            # widget.TextBox(
                # font="FontAwesome",
                # text="  ", # Memory icon
                # foreground=colors[4],
                # background=colors[1],
                # padding = 0,
                # ),
            # widget.Memory(
                # font="Noto Sans",
                # format = '{MemUsed}M/{MemTotal}M',
                # update_interval = 1,
                # foreground = colors[5],
                # background = colors[1],
                # ),
            widget.GenPollText(
                func = battery_icon.battery_widget,
                font="FontAwesome",
                foreground=colors[10],
                update_interval = 300,
                padding = 4,
                ),
            widget.Battery(
                font="Noto Sans",
                update_interval = 10,
                foreground = colors[5],
                background = colors[1],
                discharge_char = "",
                charge_char = "",
                #format = '{char} {percent:2.0%} {hour:d}:{min:02d} {watt:.2f} W'
                format = '{percent:2.0%} {char}'
	        ),
            widget.Spacer(length = widget_spacing),
            # widget.Sep(
                # linewidth = 1,
                # padding = 10,
                # foreground = colors[2],
                # background = colors[1]
                # ),
            widget.TextBox(
                font="FontAwesome",
                text="  ", # Calendar icon
                foreground=colors[11],
                background=colors[1],
                padding = 0,
                ),
            widget.Clock(
                foreground = colors[5],
                background = colors[1],
                format="%d.%m.%Y  %H:%M  "
                ),
            # widget.Sep(
                # linewidth = 0,
                # padding = 4,
                # foreground = colors[2],
                # background = colors[1]
                # ),
                ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=28, opacity=0.8)),]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []


main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('/home/henrik')
    subprocess.call("libinput-gestures-setup restart")

@hook.subscribe.startup
def start_always():
    subprocess.call('/home/henrik/.config/qtile/scripts/autostart.sh')

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

###floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
###floating_layout = layout.Floating(float_rules=[
    ###{'wmclass': 'Arcolinux-welcome-app.py'},
    ###{'wmclass': 'Arcolinux-tweak-tool.py'},
    ###{'wmclass': 'Arcolinux-calamares-tool.py'},
    ###{'wmclass': 'confirm'},
    ###{'wmclass': 'dialog'},
    ###{'wmclass': 'download'},
    ###{'wmclass': 'error'},
    ###{'wmclass': 'file_progress'},
    ###{'wmclass': 'notification'},
    ###{'wmclass': 'splash'},
    ###{'wmclass': 'toolbar'},
    ###{'wmclass': 'confirmreset'},
    ###{'wmclass': 'makebranch'},
    ###{'wmclass': 'maketag'},
    ###{'wmclass': 'Arandr'},
    ###{'wmclass': 'feh'},
    ###{'wmclass': 'Galculator'},
    ###{'wmclass': 'arcolinux-logout'},
    ###{'wmclass': 'xfce4-terminal'},
    ###{'wname': 'branchdialog'},
    ###{'wname': 'Open File'},
    ###{'wname': 'pinentry'},
    ###{'wmclass': 'ssh-askpass'},
    ###{'wname': 'Picture in picture'},

###],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart
focus_on_window_activation = "smart" # or smart

wmname = "qtile"
