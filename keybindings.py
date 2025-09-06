"""
Contains `get_keys()`, which returns the list of keybindings to
be used by qtile.
"""

import os
from libqtile.config import Key
from libqtile.lazy import lazy
from my_utils import (
    MOD,
    SHIFT,
    CONTROL,
    TERMINAL,
    LOCK_SCREEN,
    launcher,
    file_manager,
)
from qtile_graphs import show_graphs
from powermenu import show_power_menu


def get_keys() -> list[Key]:
    """
    Keybindings for qtile.

    :return: list of Key objects
    """
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    keybindings = [ Key([MOD, SHIFT], "g", lazy.function(show_graphs)),
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
    Key([MOD, SHIFT], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([MOD, SHIFT], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([MOD, "control"], "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key(
        [MOD, "control"], "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
    ),
    Key([MOD, "control"], "j",
        lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([MOD, "control"], "k",
        lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([MOD], "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"),
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
        #lazy.spawn(os.path.expanduser(POWER_MENU)),
        lazy.function(show_power_menu),
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
    Key([CONTROL, SHIFT], "l",
        lazy.spawn(os.path.expanduser(LOCK_SCREEN)))]

    return keybindings
