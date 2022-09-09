__all__ = ["revit_panel_style"]

from omni.ui import color as cl
from omni.ui import constant as fl
from omni.ui import url
import omni.kit.app
import omni.ui as ui
import pathlib

EXTENSION_FOLDER_PATH = pathlib.Path(
    omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__)
)


ATTR_LABEL_WIDTH = 150
BLOCK_HEIGHT = 22
TAIL_WIDTH = 35
WIN_WIDTH = 600
WIN_HEIGHT = 900

cl.window_bg_color = cl(0.9,0.9,0.9,1)
cl.window_title_text = cl(0.1,0.1,0.1,1)

cl.collapsible_header_bg = cl(0.9,0.9,0.9,0.9)
cl.collapsible_header_text = cl(.1, .1, .1, .8)
cl.collapsible_header_text_hover = cl(.2, .2, .2, 1.0)

cl.main_attr_label_text = cl(.1,.1,.1,1)
cl.main_attr_label_text_hover = cl(.2, .2, .2, 1.0)
cl.multifield_label_text = cl(0.1,0.1,0.1,1)
cl.combobox_label_text = cl(0.1,0.1,0.1,1)

cl.field_bg = cl(0.9,0.9,0.9,0.8)
# Blue
cl.field_border = cl(0.5,0.8,0.8,0.5)
cl.btn_border = cl(0.5,0.8,0.8,0.5)
cl.slider_fill = cl(0.5,0.8,0.8,0.5)

cl.revert_arrow_enabled = cl(.25, .5, .75, 1.0)
cl.revert_arrow_disabled = cl(.8, .8, .8, 1.0)
cl.transparent = cl(0,0,0,0)

fl.main_label_attr_hspacing = 10
fl.attr_label_v_spacing = 3
fl.collapsable_group_spacing = 2
fl.outer_frame_padding = 15
fl.tail_icon_width = 15
fl.border_radius = 3
fl.border_width = 1
fl.window_title_font_size = 18
fl.field_text_font_size = 14
fl.main_label_font_size = 14
fl.multi_attr_label_font_size = 14
fl.radio_group_font_size = 14
fl.collapsable_header_font_size = 15
fl.range_text_size = 10

url.closed_arrow_icon = f"{EXTENSION_FOLDER_PATH}/icons/closed.png"
url.open_arrow_icon = f"{EXTENSION_FOLDER_PATH}/icons/opened.png"
url.revert_arrow_icon = f"{EXTENSION_FOLDER_PATH}/icons/revert_arrow.png"
url.checkbox_on_icon = f"{EXTENSION_FOLDER_PATH}/icons/checkbox_on.png"
url.checkbox_off_icon = f"{EXTENSION_FOLDER_PATH}/icons/checkbox_off.png"
url.radio_btn_on_icon = f"{EXTENSION_FOLDER_PATH}/icons/radio_btn_on.png"
url.radio_btn_off_icon = f"{EXTENSION_FOLDER_PATH}/icons/radio_btn_off.png"
url.diag_bg_lines_texture = f"{EXTENSION_FOLDER_PATH}/icons/bar.png"
url.wall_pos = f"{EXTENSION_FOLDER_PATH}/icons/wall1.png"
url.column_pos = f"{EXTENSION_FOLDER_PATH}/icons/column1.png"
url.slab_pos = f"{EXTENSION_FOLDER_PATH}/icons/floor1.png"
url.wall_type= f"{EXTENSION_FOLDER_PATH}/icons/wall.png"
url.slab_type= f"{EXTENSION_FOLDER_PATH}/icons/floor.png"
url.column_type= f"{EXTENSION_FOLDER_PATH}/icons/column.png"
url.mat_concrete= f"{EXTENSION_FOLDER_PATH}/icons/concrete.jpg"

# 风格词典主要部分
revit_panel_style = {
    # 窗体
    "Window":{
        "background_color":cl.window_bg_color,
        "border_radius":3,
        "border_width":3,
        "border_color":0xDDDDDDDD
    },
    # 按键
    "Button::tool_button": {
        "background_color": cl.field_bg,
        "margin_height": 0,
        "margin_width": 6,
        "border_color": cl.btn_border,
        "border_width": fl.border_width,
        "font_size": fl.field_text_font_size,
    },
    # 折叠组
    "CollapsableFrame::group": {
        "margin_height": fl.collapsable_group_spacing,
        "background_color": cl.window_bg_color,
        "secondary_color": cl.window_bg_color,
    },
    "CollapsableFrame::group:hovered": {
        "margin_height": fl.collapsable_group_spacing,
        "background_color": cl(0.8,0.8,0.8,1),
        "secondary_color": cl(0.7,0.7,0.7,1)
    },
    "HeaderLine": {"color": cl(.5, .5, .5, .5)},
    # TODO: For some reason this ColorWidget style doesn't respond much, if at all (ie, border_radius, corner_flag)
    "ColorWidget": {
        "border_radius": fl.border_radius,
        "border_color": cl(0.0, 0.0, 0.0, 0.0),
    },

    # Field
    "Field": {
        "background_color": cl.field_bg,
        "border_radius": fl.border_radius,
        "border_color": cl.field_border,
        "border_width": fl.border_width,
    },
    "Field::attr_field": {
        "color":cl(0.1,0.1,0.1,1),
        "corner_flag": ui.CornerFlag.RIGHT,
        "font_size": 2,
        # fl.field_text_font_size,  # Hack to allow for a smaller field border until field padding works
    },
    "Field::attribute_color": {
        "color":cl(0.1,0.1,0.1,1),
        "font_size": fl.field_text_font_size,
    },
    "Field::multi_attr_field": {
        "color":cl(0.1,0.1,0.1,1),
        "padding": 4,  # TODO: Hacky until we get padding fix
        "font_size": fl.field_text_font_size,
    },
    "Field::multi_attr_field:hovered": {
        "color":cl(0.1,0.1,0.1,1),
        "padding": 4,  # TODO: Hacky until we get padding fix
        "font_size": fl.field_text_font_size,
    },
    "Field::path_field": {
        "color":cl(0.1,0.1,0.1,1),
        "corner_flag": ui.CornerFlag.RIGHT,
        "font_size": fl.field_text_font_size,
    },

    "Image::collapsable_opened": {
        "color": cl.collapsible_header_text,
        "image_url": url.open_arrow_icon,
    },
    "Image::collapsable_opened:hovered": {
        "color": cl.collapsible_header_text_hover,
        "image_url": url.open_arrow_icon,
    },
    "Image::collapsable_closed": {
        "color": cl.collapsible_header_text,
        "image_url": url.closed_arrow_icon,
    },
    "Image::collapsable_closed:hovered": {
        "color": cl.collapsible_header_text_hover,
        "image_url": url.closed_arrow_icon,
    },
    "Image::radio_on": {"image_url": url.radio_btn_on_icon},
    "Image::radio_off": {"image_url": url.radio_btn_off_icon},
    "Image::revert_arrow": {
        "image_url": url.revert_arrow_icon,
        "color": cl.revert_arrow_enabled,
    },
    "Image::revert_arrow:disabled": {"color": cl.revert_arrow_disabled},
    "Image::checked": {"image_url": url.checkbox_on_icon},
    "Image::unchecked": {"image_url": url.checkbox_off_icon},
    "Image::slider_bg_texture": {
        "image_url": url.diag_bg_lines_texture,
        "border_radius": fl.border_radius,
        "corner_flag": ui.CornerFlag.LEFT,
    },
    "Image::wall_type": {"image_url": url.wall_type},
    "Image::slab_type": {"image_url": url.slab_type},
    "Image::column_type": {"image_url": url.column_type},
    "Image::wall_pos": {"image_url": url.wall_pos},
    "Image::column_pos": {"image_url": url.column_pos},
    "Image::slab_pos": {"image_url": url.slab_pos},
    "Image::mat_concrete": {"image_url": url.mat_concrete},

    "Label::attribute_name": {
        "alignment": ui.Alignment.RIGHT_TOP,
        "margin_height": fl.attr_label_v_spacing,
        "margin_width": fl.main_label_attr_hspacing,
        "color": cl.main_attr_label_text,
        "font_size": fl.main_label_font_size,
    },
    "Label::attribute_name:hovered": {"color": cl.main_attr_label_text_hover},
    "Label::collapsable_name": {"font_size": fl.collapsable_header_font_size},
    "Label::multi_attr_label": {
        "color": cl.multifield_label_text,
        "font_size": fl.multi_attr_label_font_size,
    },
    "Label::radio_group_name": {
        "font_size": fl.radio_group_font_size,
        "alignment": ui.Alignment.CENTER,
        "color": cl.main_attr_label_text,
    },
    "Label::range_text": {
        "font_size": fl.range_text_size,
    },
    "Label::window_title": {
        "font_size": fl.window_title_font_size,
        "color": cl.window_title_text,
    },
    "ScrollingFrame::window_bg": {
        "background_color": cl.window_bg_color,
        "padding": fl.outer_frame_padding,
        "border_radius": 20  # Not obvious in a window, but more visible with only a frame
    },
    "Slider::attr_slider": {
        "draw_mode": ui.SliderDrawMode.FILLED,
        "padding": 0,
        "color": cl.transparent,
        # Meant to be transparent, but completely transparent shows opaque black instead.
        "background_color": cl(0.8, 0.28, 0.28, 0.01),
        "secondary_color": cl.slider_fill,
        "border_radius": fl.border_radius,
        "corner_flag": ui.CornerFlag.LEFT,  # TODO: Not actually working yet OM-53727
    },

    # Combobox workarounds
    "Rectangle::combobox": {  # TODO: remove when ComboBox can have a border
        "background_color": cl.field_bg,
        "border_radius": fl.border_radius,
        "border_color": cl.btn_border,
        "border_width": fl.border_width,
    },
    "ComboBox::dropdown_menu": {
        "color": cl.combobox_label_text,  # label color
        "padding_height": 1.25,
        "margin": 2,
        "background_color": cl.field_bg,
        "border_radius": fl.border_radius,
        "font_size": fl.field_text_font_size,
        "secondary_color": cl.transparent,
        "secondary_selected_color":cl(0.2,0.2,0.2,1),# 下拉选项文字颜色
        "background_selected_color":cl(1,0.3,0,1),
        "selected_color":cl(0.6,0.6,0.6,1)# 下拉文字颜色
    },
    "Rectangle::combobox_icon_cover": {"background_color": cl.field_bg}
}
