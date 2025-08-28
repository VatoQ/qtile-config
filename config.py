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

from ast import mod
from my_utils import *
from tkinter import Y
from libqtile import bar, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras.widget.decorations import GradientDecoration, PowerLineDecoration, RectDecoration
from libqtile import hook
from qtile_extras import widget as extrawidgets
from clock_widget import extended_clock, ExtendedClock
from libqtile.backend.wayland.inputs import InputConfig
from qtile_extras.layout.decorations.borders import GradientFrame
import os
import subprocess
from qtile_graphs import show_graphs
import random_wallpaper

launcher = ""
file_manager = ""

if qtile.core.name == "x11":
    term = "urxvt"
    launcher = "rofi -show drun"
    file_manager = "pcmanfm"
elif qtile.core.name == "wayland":
    term = "foot"
    launcher = "wofi --show drun"
    file_manager = "dolphin"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([MOD, SHIFT], "g", lazy.function(show_graphs)),
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [MOD, SHIFT], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [MOD, SHIFT],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([MOD, SHIFT], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, SHIFT], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([MOD, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [MOD, SHIFT],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key(
        [MOD, SHIFT],
        "q",
        lazy.spawn(os.path.expanduser(POWER_MENU)),
        desc="Spawn power menu",
        ),
    Key([MOD], "q",
        lazy.spawn(TERMINAL),
        desc="Launch terminal"),
    # Key(["control", "alt"], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([MOD], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"),
    Key([MOD], "c",
        lazy.window.kill(),
        desc="Kill focused window"),
    Key(
        [MOD],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [MOD],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([MOD, "control"], "r",
        lazy.reload_config(),
        desc="Reload the config"),
    Key([MOD, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),
    Key([MOD], "r",
        lazy.spawn(launcher),
        desc="Spawn a command using a prompt widget"),
    Key([MOD], "e",
        lazy.spawn(file_manager),
        desc="Spawn file manager"),
    # Switching workspaces
    Key([MOD], "right",
        lazy.screen.next_group(skip_empty=True)),
    Key([MOD], "left",
        lazy.screen.prev_group(skip_empty=True)),
    Key([MOD, SHIFT], "right",
        lazy.screen.next_group(skip_empty=False)),
    # Key([mod], "up", lazy.layout.focus_next()),
    # Key([mod], "down", lazy.layout.focus_previous()),
    Key([], "XF86AudioRaiseVolume",
        lazy.widget["volume"].increase_vol(),
        desc="Increase Volume"),
    Key([], "XF86AudioLowerVolume",
        lazy.widget["volume"].decrease_vol(),
        desc="Decrease Volume"),
    Key([], "XF86AudioMute",
        lazy.widget["volume"].mute(),
        desc="Toggle Mute"),
    Key([], "XF86MonBrightnessUp",
        lazy.widget["brightness"].brightness_up(),
        desc="Brightness Up"),
    Key([], "XF86MonBrightnessDown",
        lazy.widget["brightness"].brightness_down(),
        desc="Brightness Down"),
    Key([CONTROL], "l",
        lazy.spawn(os.path.expanduser(LOCK_SCREEN)))
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [MOD],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [MOD, SHIFT],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, SHIFT], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )



layout_theme = init_layout_theme()


layouts = [
    # layout.Columns(border_focus_stack=[FOCUS_COLOR, SECONDARY_COLOR], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Spiral(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
]

widget_defaults = dict(
    font="Adwaita Sans SemiBold",
    fontsize=18,
    padding=0,
)
extension_defaults = widget_defaults.copy()


decoration_group = get_decoration_group(BAR_NORMAL)
decorations_left = get_decoration_group(BAR_CHOICE_LEFT)
decorations_right = get_decoration_group(BAR_CHOICE_RIGHT)

# some widgets look better with slightly other settings:
workspace_decoration = decorations_left.copy()
workspace_decoration["padding"] = 6
workspace_decoration["decorations"][0] = RectDecoration(
    use_widget_background=True,
    padding_y=20,
    filled=True,
    radius=9,
)


wifi_decoration =  decorations_right.copy()
wifi_decoration["padding"] = 8


screens = [
    Screen(
        top=bar.Bar(
            [
                extrawidgets.CurrentLayoutIcon(
                    background=dim_color(BLUE, 1.8), 
                    **decorations_left
                ),
                extrawidgets.GroupBox2(
                    fontsize=20,
                    highlight_method="block",
                    background=dim_color(GRAY, 4),
                    hide_unused=True,
                    rules=GROUPBOX_RULES,
                    **workspace_decoration,
                ),
                extrawidgets.WindowName(
                    background=dim_color(GRAY, 2),
                    **decorations_right
                ),
                extrawidgets.StatusNotifier(background="#001020", **decorations_right),
                extrawidgets.WiFiIcon(
                    background=dim_color(BLUE, 6.8),
                    interface="wlp2s0",
                    wifi_arc=75,
                    **wifi_decoration,
                    ),
                extrawidgets.Bluetooth(
                    background=dim_color(BLUE, 6.8),
                    default_text="󰂯 {connected_devices}",
                    **decorations_right
                    ),
                extrawidgets.Systray(
                    background=dim_color(BLUE, 6.7),
                    **decorations_right
                    ),
                extrawidgets.Clock(
                    background=dim_color(BLUE, 4),
                    fontsize=11,
                    format="%a %d.%m.%y\n %H:%M:%S %p",
                    **decorations_right,
                ),
                extrawidgets.Battery(
                    background=dim_color(BLUE, 2.5),
                    format="{char} {percent:2.0%}",
                    empty_char="󰁺",
                    discharge_char="󰁿",
                    charge_char="󰂄",
                    full_char="󰁹",
                    low_background=RED,
                    low_percentage=0.2,
                    charge_controller=lambda: (0, 95),
                    update_interval= 4,
                    **decorations_right,
                ),
                extrawidgets.BrightnessControl(
                    name="brightness",
                    background=dim_color(CYAN, 2),
                    bar_colour=dim_color(CYAN, 3),
                    bar_height=25,
                    min_brightness=35,
                    device="/sys/class/backlight/amdgpu_bl1",
                    format="{percent:2.0%}",
                    step=5,
                    **decorations_right
                ),
                extrawidgets.PulseVolume(
                    name="volume",
                    volume_app = "pavucontrol",
                    emoji_list= [
                        "",
                        "",
                        "",
                        "",
                        ],
                    background=dim_color(CYAN, 1.5), 
                    emoji=True, 
                    **decorations_right
                ),
                extrawidgets.ScriptExit(
                    background=dim_color(ORANGE, 1),
                    default_text="󰅙",  # "",
                    countdown_format="{}",
                    countdown_start=5,
                    **decorations_right,
                ),
                extended_clock,
            ],
            35,
            # radius=10,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        # Set Wallpaper
        wallpaper="~/Pictures/Wallpapers/1343823.png",
        wallpaper_mode = "fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        # [mod],
        [MOD],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="pcmanfm"),
        Match(wm_class="gnome-calendar"),
        Match(title="Figure 1"),
        Match(wm_class="powermenu"),
    ],
    max_border_width=4,
    border_width=4,
    border_focus=FOCUS_COLOR,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "type:keyboard": InputConfig(kb_layout="de"),
    "type:touchpad": InputConfig(tap=True, natural_scroll=True, pointer_accel=0.4),
}
# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24


sticky_windows = []


@lazy.function
def toggle_sticky_windows(qtile, window=None):
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window


@hook.subscribe.setgroup
def move_sticky_windows():
    for window in sticky_windows:
        window.togroup()
    return


@hook.subscribe.client_killed
def remove_sticky_windows(window):
    if window in sticky_windows:
        sticky_windows.remove(window)


@hook.subscribe.client_managed
def auto_sticky_windows(window):
    info = window.info()
    if (
        info["wm_class"] == ["Toolkit", "firefox"]
        and info["name"] == "Picture-in-Picture"
    ):
        sticky_windows.append(window)


@hook.subscribe.startup_once
def autostart():
    if qtile.core.name == "x11":
        home = os.path.expanduser("~/.config/qtile/autostart.sh")
        subprocess.call(home)
    elif qtile.core.name == "wayland":
        home = os.path.expanduser("~/.config/qtile/autostart_wayland.sh")
        subprocess.call(home)


# @hook.subscribe.startup_once
# def start_random_wallpaper_timer():
#     random_wallpaper.Timer(TIMER_MINUTES * 60, random_wallpaper.set_random_wallpaper)


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
