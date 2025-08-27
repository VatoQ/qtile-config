from qtile_extras import widget
from qtile_extras.popup import (
        PopupRelativeLayout,
        PopupWidget,
        PopupText,
)
from qtile_extras.widget.decorations import (
        RectDecoration
)
from constants import (
        FOCUS_COLOR,
        SECONDARY_COLOR,
        dim_color
)


def show_graphs(qtile):
    font_height = 0.06
    text_kwargs = {
            "height": font_height,
            "fontsize": 16,
            "font": "Adwaita Sans Semi-Bold"
    }
    graph_options = {
        "type": "linefill",
        "line_width": 5,
        "border_width": 0,
        "frequency": 0.1,
        "graph_color": SECONDARY_COLOR,
        "fill_color": dim_color(FOCUS_COLOR, 2),
        "margin_y": 8,
        "margin_x": 6,
        "samples": 400,
        "decorations": [
            RectDecoration(
                radius=15,
                line_colour=FOCUS_COLOR,
                line_width=5,
                #padding=-5
                ),
            ]
    }
    controls = [
        PopupText(
            name="CPU_Label",
            text="CPU Graph:",
            width=0.45,
            #height=font_height,
            pos_x = 0.05,
            pos_y = 0.05,
            **text_kwargs
            ),
        PopupWidget(
            widget=widget.CPUGraph(**graph_options),
            width=0.45 - 0.01,
            height=0.45 - font_height,
            pos_x = 0.05,
            pos_y = 0.1,
            #**graph_options
            ),
        PopupText(
            name="NetGraph_Label",
            text="Network Graph:",
            width = 0.45,
            # height = font_height,
            pos_x = 0.5,
            pos_y = 0.05,
            **text_kwargs
            ),
        PopupWidget(
            widget = widget.NetGraph(**graph_options),
            width=0.45,
            height=0.45 - font_height,
            pos_x = 0.5,
            pos_y = 0.1,
            #**graph_options
            ),
        PopupText(
            name="MemoryGraph_Label",
            text="Memory Graph:",
            width=0.9,
            #height=font_height,
            pos_x=0.05,
            pos_y=0.45 + font_height,
            **text_kwargs
            ),
        PopupWidget(
            widget = widget.MemoryGraph(**graph_options),
            width=0.9,
            height=0.45 - font_height,
            pos_x = 0.05,
            pos_y = 0.5 + font_height,
            #**graph_options
            ),
        ]
    layout = PopupRelativeLayout(
            qtile,
            #rows=4,
            #cols=4,
            width = 1000,
            height = 500,
            controls=controls,
            background="00000060",
            initial_focus=None,
            close_on_click=True,
            decorations=[
                RectDecoration(
                    radius=10,
                    colour="FF0000",
                    )
                ]
            )
    layout.show(centered=True)



