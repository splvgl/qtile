# standard qtile libraries
import os, re, socket, subprocess
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule
from libqtile import layout, bar, widget, hook, qtile

# my widgets
from widgets import pacman_widget, battery_icon

# standard mod/super key
mod = "mod4"
home = "/home/henrik"

# functions
# moving windows
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

# widget functions
def pacman_update():
    qtile.cmd_spawn("termite -e 'sudo pacman -Syu'")

def arco_menu():
    subprocess.call(home + "/Programs/xmenu/xmenu.sh")

def rofi_windows():
    qtile.cmd_spawn("rofi -show window -no-fixed-num-lines -width 70 -location 2")

# hook functions
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


# groups
group_names = [str(i+1) for i in range(9)]
group_labels = group_names
group_layouts = ["monadtall" for i in group_names]
groups = [group(name = group_names[i], layout = group_layouts[i].lower(), label = group_labels[i])]

keys = [
# FULLSCREEN MODE
    Key([mod], "f", lazy.window.toggle_fullscreen()),
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
    # TERMINAL (termite)
    Key([mod], "Return", lazy.spawn("termite")),
    # FILE MANAGERS
    Key([mod], "y", lazy.spawn("urxvt -e ranger")),
    Key([mod, "shift"], "y", lazy.spawn("nautilus")),
    # ROFI LAUNCHER
    Key([mod], "r", lazy.spawn("rofi -modi combi -combi-modi window,drun -show combi -icon-theme Sardi-Arc -show-icons")),
    # SLEEP TIMER
    Key([mod], "XF86PowerOff", lazy.spawn("/home/henrik/Dev/fish/sleep-timer.sh")),
    # POWE MODE SELECTOR
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
    ]

for i in groups:
    keys.extend([
#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

# layout
layout_theme = {
    "margin":8,
    "border_width":2,
    "border_focus":"#3384d0",
    "border_normal": "#000000",
}
layouts = [
    layout.MonadTall(**layout_theme, single_border_width = 0),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
]
colors = [
    ["000000", "000000"],
    ["c0c5ce", "c0c5ce"],
    ["#f3f4f5", "#f3f4f5"],
    ["#6790eb", "#6790eb"],
    ["#689d69", "#689d69"],
    ["#458587", "#458587"],
]

# widgets and bar
widget_defaults = {
    "font": "Noto Sans",
    "fontsize": 18,
    "padding": 2,
    "background": colors[0]
}

widgets_list = [
    widget.Sep(
        linewidth = 0,
        padding = 12,
        foreground = colors[1],
        ),
    widget.Image(
        filename = '~/.config/qtile/icons/arco2.png',
        margin_y = 2,
        margin_x = 0,
        mouse_callbacks = {'Button1': arco_menu},
        ),
    widget.Sep(
        linewidth = 1,
        padding = 10,
        foreground = colors[1],
        ),
    widget.GroupBox(
        font="FontAwesome",
        fontsize = 18,
        margin_y = 3,
        margin_x = 0,
        padding_y = 0,
        padding_x = 5,
        borderwidth = 2,
        disable_drag = True,
        active = colors[3],
        inactive = colors[2],
        rounded = True,
        highlight_method = "border",
        this_current_screen_border = colors[8],
        foreground = colors[1],
        ),
    widget.Sep(
        linewidth = 1,
        padding = 10,
        foreground = colors[1],
        ),
    widget.Systray(
        background=colors[1],
        icon_size=22,
        padding = 4
        ),
    widget.Sep(
        linewidth = 1,
        padding = 10,
        foreground = colors[1],
        ),
    widget.CurrentLayoutIcon(
        font = "Noto Sans Bold",
        foreground = colors[5],
        background = colors[1],
        scale = 0.7
        ),
    widget.WindowName(font="Noto Sans",
        foreground = colors[1],
        padding = 50,
        max_chars = 90,
        mouse_callbacks = {'Button1': rofi_windows},
        ),
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
    widget.Sep(
        linewidth = 1,
        padding = 10,
        foreground = colors[1],
        ),
    widget.GenPollText(
        func = battery_icon.battery_widget,
        font="FontAwesome",
        foreground=colors[3],
        update_interval = 300,
        padding = 4,
        ),
    widget.Battery(
        font="Noto Sans",
        update_interval = 10,
        foreground = colors[4],
        background = colors[1],
        discharge_char = "",
        charge_char = "",
        format = '{percent:2.0%} {char}'
	    ),
    widget.Sep(
        linewidth = 1,
        padding = 10,
        foreground = colors[1],
        ),
    widget.TextBox(
        font="FontAwesome",
        text="  ", # Calendar icon
        foreground=colors[1],
        padding = 0,
        ),
    widget.Clock(
        foreground = colors[1],
        format="%d.%m.%Y  %H:%M  "
        ),
    widget.Sep(
        linewidth = 0,
        padding = 4,
        foreground = colors[1],
        ),
]

screens = [
    Screen(top=bar.Bar(widgets=widgets_list, size=28, opacity=1)),
    Screen(top=bar.Bar(widgets=widgets_list, size=28, opacity=1)),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = False
bring_front_click = False
cursor_warp = False

floating_rules = [
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'Arcolinux-calamares-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
    {'wname': 'Picture in picture'},
],

floating_layout = layout.Floating(float_rules=floating_rules,  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "qtile"