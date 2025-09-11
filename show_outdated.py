#!/bin/env python
import subprocess
from libqtile.core.manager import Qtile
from qtile_extras.popup.toolkit import PopupGridLayout, PopupText

from my_utils import (
    BAR_HEIGHT,
    DARK2,
    DARKER,
    GRAY,
    TRANSLUCENT0,
    TRANSLUCENT1,
    dim_color_alpha
)

_COMMAND = "checkupdates"

def _str_get_outdated() -> str:
    """
    Get current outdated packages as an unformatted string.

    :return: Outdated packages as a string.
    """
    return subprocess.run([_COMMAND],
                          check=False,
                          stdout=subprocess.PIPE). \
        stdout.decode(encoding="utf-8")



def show_outdated(qtile: Qtile) -> None:
    """
    Renders the current outdated packages as a popup.

    :param qtile: Root object
    """
    outdated_pkgs = _str_get_outdated().strip()

    if len(outdated_pkgs) < 4:
        outdated_pkgs = "No updates available"


    pkg_list = outdated_pkgs.split("\n")

    height = len(pkg_list)
    width = max(len(line) for line in pkg_list)

    base_width = 10
    base_height = 40
    fontsize = 16

    text_kwargs = {
        "fontsize": fontsize,
        "h_align": "center",
        "v_align": "middle",
        "height": height * base_height,
        "background": dim_color_alpha(GRAY, DARKER, TRANSLUCENT1),
        "font": "Adwaita Sans Semi-Bold"
    }

    controls = [
        PopupText(
            name="Outdated_Packages",
            text=outdated_pkgs,
            row=0,
            col=0,
            **text_kwargs
            ),
    ]

    layout = PopupGridLayout(
            qtile,
            width=width * base_width,
            height=height * base_height,
            rows=1,
            cols=1,
            controls=controls,
            background = dim_color_alpha(GRAY, DARK2, TRANSLUCENT0)
            )
    layout.show(y=BAR_HEIGHT * 0 // 2,
                relative_to_bar=True,
                relative_to=2
                )


