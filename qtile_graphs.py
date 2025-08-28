from qtile_extras import widget
from qtile_extras.popup import (
        PopupRelativeLayout,
        PopupWidget,
        PopupText,
)
from qtile_extras.widget.decorations import (
        RectDecoration
)
from my_utils import (
        SECONDARY_COLOR,
        FOCUS_COLOR,
        GRAY,
        dim_color
)

#from constants import (
#        FOCUS_COLOR,
#        SECONDARY_COLOR,
#        dim_color
#)


def show_graphs(qtile):
    font_height = 0.15
    first_row_height = 0.45 - font_height
    basic_width = 0.45
    basic_unit = 0.01
    text_background = dim_color(GRAY, 5) + "C0"
    graph_color = dim_color(SECONDARY_COLOR, 1.0) + "E0"
    fill_color = dim_color(FOCUS_COLOR, 2) + "C0"
    text_kwargs = {
            "height": font_height - 0.4 * font_height,
            "fontsize": 16,
            "h_align": "center",
            "background": text_background,
            "font": "Adwaita Sans Semi-Bold"
    }
    graph_options = {
        "type": "linefill",
        "line_width": 5,
        "border_width": 0,
        "frequency": 0.1,
        "graph_color": graph_color,
        "fill_color": fill_color,
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
            width=basic_width - basic_unit,
            #height=font_height,
            pos_x = 0.05,
            pos_y = 0.05,
            **text_kwargs
            ),
        PopupWidget(
            widget=widget.CPUGraph(**graph_options),
            width = basic_width - 0.01,
            height=first_row_height,
            pos_x = 0.05,
            pos_y = font_height + basic_unit,
            #**graph_options
            ),
        PopupText(
            name="NetGraph_Label",
            text="Network Graph:",
            width = basic_width,
            # height = font_height,
            pos_x = 0.5,
            pos_y = 0.05,
            **text_kwargs
            ),
        PopupWidget(
            widget = widget.NetGraph(**graph_options),
            width = basic_width,
            height=first_row_height,
            pos_x = 0.5,
            pos_y = font_height + basic_unit,
            #**graph_options
            ),
        PopupText(
            name="MemoryGraph_Label",
            text="Memory Graph:",
            width=2 * basic_width,
            #height=font_height,
            pos_x=0.05,
            pos_y= first_row_height + font_height + 2 * basic_unit,
            **text_kwargs
            ),
        PopupWidget(
            widget = widget.MemoryGraph(**graph_options),
            width= 2 * basic_width,
            height= first_row_height,
            pos_x = 0.05,
            pos_y = first_row_height + 2 * (font_height - basic_unit),
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
            background="00000000",
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



