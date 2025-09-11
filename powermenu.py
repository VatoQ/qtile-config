#!/bin/python
import os
import copy
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from fileinput import filename
from qtile_extras.popup import (
    PopupGridLayout,
    PopupImage,
    PopupText
)
from qtile_extras.widget.decorations import (
        RectDecoration
)

from my_utils import (
    BORDER_RADIUS,
    BORDER_WIDTH,
    FOCUS_COLOR,
    LIGHT,
    RED,
    GRAY,
    NEUTRAL,
    DARK2,
    LOCK_SCREEN,
    SECONDARY_COLOR,
    TRANSLUCENT0,
    TRANSLUCENT1,
    dim_color_alpha
)

def show_power_menu(qtile: Qtile) -> None:
    """
    Renders an array of logout options. Can be cycled with vim keys.
    """
    image_options = {
            "row_span": 1,
            "col_span": 1,
            "mask": True,
            "colour": dim_color_alpha(SECONDARY_COLOR, NEUTRAL, TRANSLUCENT1),
            "highlight": dim_color_alpha(FOCUS_COLOR, LIGHT, TRANSLUCENT0),
            "highlight_radius": BORDER_RADIUS,
            "highlight_border": BORDER_WIDTH,
            "highlight_method": "block",
            #"decorations": [
            #    RectDecoration(
            #        radius=15,
            #        line_colour=FOCUS_COLOR,
            #        line_width=5
            #        ),
            #    ]
            }

    shutdown_options = copy.deepcopy(image_options)
    #shutdown_options["highlight"] = dim_color_alpha(RED, NEUTRAL, TRANSLUCENT0)
    shutdown_options["colour"] = dim_color_alpha(RED, NEUTRAL, TRANSLUCENT1)

    controls = [
            PopupImage(
                filename = "~/Pictures/Icons/qtile/powermenu/padlock.png",
                row=0,
                col=0,
                mouse_callbacks={
                    "Button1": lazy.spawn(os.path.expanduser(LOCK_SCREEN)),
                    },
                **image_options,
                ),
            PopupImage(
                filename = "~/Pictures/Icons/qtile/powermenu/time.png",
                row=0,
                col=1,
                mouse_callbacks={
                    "Button1": lazy.spawn("systemctl suspend")
                    },
                **image_options,
                ),
            PopupImage(
                filename = "~/Pictures/Icons/qtile/powermenu/reboot.png",
                row=0,
                col=2,
                mouse_callbacks={
                    "Button1": lazy.spawn("systemctl reboot")
                    },
                **image_options,
                ),
            PopupImage(
                filename = "~/Pictures/Icons/qtile/powermenu/shutdown.png",
                row=0,
                col=3,
                mouse_callbacks = {
                    "Button1": lazy.spawn("systemctl poweroff")
                    },
                **shutdown_options,
                ),
            ]
    layout = PopupGridLayout(
            qtile,
            width=1920,
            margin=10,
            #height=200,
            rows=1,
            cols=4,
            controls=controls,
            background = dim_color_alpha(GRAY, DARK2, TRANSLUCENT0),
            close_on_click = True,
            )
    layout.show(centered=True)

if __name__ == "__main__":
    lazy.function(show_power_menu)


