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
from constants import *
from tkinter import Y
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras.widget.decorations import GradientDecoration, PowerLineDecoration, RectDecoration
from libqtile import hook
from qtile_extras import widget as extrawidgets
from qtile_extras.layout.decorations import GradientBorder
from qtile_extras.widget.groupbox2 import GroupBoxRule
from clock_widget import extended_clock, ExtendedClock
from libqtile.backend.wayland.inputs import InputConfig

# from qtile_extras.layout.decorations import borders.GradientBorder
from qtile_extras.layout.decorations.borders import GradientBorder, GradientFrame
import os
import subprocess
from settings import TIMER_MINUTES, BAR_CHOICE_LEFT, BAR_CHOICE_RIGHT, BAR_NORMAL

# from random_wallpaper import set_random_wallpaper
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

#mod = "mod4"
#terminal = "kitty"  # guess_terminal()
#power_menu = "~/.config/qtile/scripts/powermenu"
# launcher = "wofi --show drun"
# file_manager = "dolphin"  #  "pcmanfm"  # "nautilus"
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod, "shift"], "g", lazy.function(show_graphs)),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key(
        [mod, "shift"],
        "q",
        lazy.spawn(os.path.expanduser(power_menu)),
        desc="Spawn power menu",
        ),
    Key([mod], "q", lazy.spawn(terminal), desc="Launch terminal"),
    # Key(["control", "alt"], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(launcher), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Spawn file manager"),
    # Switching workspaces
    Key([mod], "right", lazy.screen.next_group(skip_empty=True)),
    Key([mod], "left", lazy.screen.prev_group(skip_empty=True)),
    Key([mod, "shift"], "right", lazy.screen.next_group(skip_empty=False)),
    # Key([mod], "up", lazy.layout.focus_next()),
    # Key([mod], "down", lazy.layout.focus_previous()),
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
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

gradient_border = GradientBorder(colours=[FOCUS_COLOR, SECONDARY_COLOR],
                                 radial=False)


def init_layout_theme():
    return {
        "margin": 5,
        # "margin_on_single": 5,
        "border_width": 4,
        "border_focus": gradient_border,
        "border_normal": NORMAL_COLORS,
        "border_on_single": True,
        "wrap_clients": True,
        "lower_right": True,
        "fair": True,
        "decorations": [gradient_border],
    }


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


def get_decoration_group(choice: int) -> dict:
    result = {}

    if choice == BAR_NORMAL:
        result["decorations"] = [
            RectDecoration(
                colour="#004040", radius=2, filled=True, padding=0, group=True
            )
        ]

        result["padding"] = 20

    elif choice == BAR_CHOICE_LEFT:
        result["decorations"] = [
            RectDecoration(
                # colour="#004040",
                use_widget_background=True,
                padding_y=5,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_left", padding_y=0),
        ]

        result["padding"] = 15
        # result["height"] = 30

    elif choice == BAR_CHOICE_RIGHT:
        result["decorations"] = [
            RectDecoration(
                # colour="#004040",
                use_widget_background=True,
                padding_y=5,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_right", padding_y=0),
        ]
        result["padding"] = 15

    return result


decoration_group = get_decoration_group(BAR_NORMAL)

decorations_left = get_decoration_group(BAR_CHOICE_LEFT)

decorations_right = get_decoration_group(BAR_CHOICE_RIGHT)

workspace_decoration = decorations_left.copy()
workspace_decoration["padding"] = 6
workspace_decoration["decorations"][0] = RectDecoration(
    #colour="#004040",
    use_widget_background=True,
    padding_y=20,
    filled=True,
    radius=9,
)


wifi_decoration =  decorations_right.copy()
wifi_decoration["padding"] = 8




#workspace_decoration["decorations"][0] = GradientDecoration(
#    colours = [YELLOW, ORANGE]
#)

def set_label(rule, box) -> bool:
    if box.focused:
        rule.text = "◉"
    elif box.occupied:
        rule.text = "◎"
    else:
        rule.text = "○"

    return True

# GroupBoxRule().when(func=set_label)
groupbox_rules = [
    GroupBoxRule(text_colour=dim_color(YELLOW, 1.4)).when(screen=GroupBoxRule.SCREEN_THIS),
    GroupBoxRule(text_colour=dim_color(CYAN, 1.4)).when(occupied=True),
    GroupBoxRule(text_colour=dim_color(CYAN, 2.7)).when(occupied=False),
    GroupBoxRule().when(func=set_label)
]

screens = [
    Screen(
        top=bar.Bar(
            [
                extrawidgets.CurrentLayoutIcon(
                    background=dim_color(BLUE, 1.5), 
                    **decorations_left
                ),
                extrawidgets.GroupBox2(
                    #fmt="",
                    fontsize=20,
                    highlight_method="block",
                    background=dim_color(GRAY, 4),
                    hide_unused=True,
                    rules=groupbox_rules,
                    **workspace_decoration,
                ),
                extrawidgets.WindowName(
                    seperator="/",
                    background=dim_color(GRAY, 2),
                    **decorations_right
                ),
                extrawidgets.StatusNotifier(background="#001020", **decorations_right),
                extrawidgets.WiFiIcon(
                    background=dim_color(BLUE, 6.8),
                    #fontsize=10,
                    interface="wlp2s0",
                    **wifi_decoration,
                    ),
                extrawidgets.Systray(
                    background=dim_color(BLUE, 6.7),
                    **decorations_right
                    ),
                extrawidgets.Clock(
                    background=dim_color(BLUE, 4),
                    # font="mono",
                    fontsize=11,
                    format="%a %d.%m.%y\n %H:%M:%S %p",
                    #mouse_callbacks = {
                    #    "Button1": extended_clock
                    #    },
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
                    **decorations_right,
                ),
                extrawidgets.PulseVolume(
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
        # wallpaper="~/Pictures/Wallpapers/colorful.png",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        # [mod],
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
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


@hook.subscribe.startup_once
def start_random_wallpaper_timer():
    random_wallpaper.Timer(TIMER_MINUTES * 60, random_wallpaper.set_random_wallpaper)


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
