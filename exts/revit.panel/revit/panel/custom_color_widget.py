__all__ = ["CustomColorWidget"]

from ctypes import Union
import re
from typing import List, Optional

import omni.ui as ui

from .custom_base_widget import CustomBaseWidget
from .style import BLOCK_HEIGHT

COLOR_PICKER_WIDTH = ui.Percent(35)
FIELD_WIDTH = ui.Percent(65)
COLOR_WIDGET_NAME = "color_block"
SPACING = 4


class CustomColorWidget(CustomBaseWidget):
    """取色工具，把RGB值转换为逗号隔开的字符串，展示在StringField中，反之同理"""

    def __init__(self, *args, model=None, **kwargs):
        self.__defaults: List[Union[float, int]] = [a for a in args if a is not None]
        self.__strfield: Optional[ui.StringField] = None
        self.__colorpicker: Optional[ui.ColorWidget] = None
        self.__color_sub = None
        self.__strfield_sub = None

        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__strfield = None
        self.__colorpicker = None
        self.__color_sub = None
        self.__strfield_sub = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        if self.__colorpicker:
            return self.__colorpicker.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        self.__colorpicker.model = value

    @staticmethod
    def simplify_str(val):
        s = str(round(val, 3))
        s_clean = re.sub(r'0*$', '', s)  # 清理附带的0
        s_clean = re.sub(r'[.]$', '', s_clean)  # 清理尾部
        s_clean = re.sub(r'^0', '', s_clean)  # 清理头部的0
        return s_clean

    def set_color_stringfield(self, item_model: ui.AbstractItemModel,
                              children: List[ui.AbstractItemModel]):
        """从取色器得到RGB值转换为字符串，将值赋给stringField

        参数：
            item_model : 取色器model
            children : 取色器的子项
        """
        # RGB转换为逗号隔开的字符
        field_str = ",".join([self.simplify_str(item_model.get_item_value_model(c).as_float)
                              for c in children])
        self.__strfield.model.set_value(field_str)
        if self.revert_img:
            self._on_value_changed()

    def set_color_widget(self, str_model: ui.SimpleStringModel,
                         children: List[ui.AbstractItem]):
        """解析新的StringField的值并设定给ColorWidget

        参数：
            str_model : SimpleStringModel（用与StringField）
            children : ui.ColorWidget的model的子项
        """
        joined_str = str_model.get_value_as_string()
        for model, comp_str in zip(children, joined_str.split(",")):
            comp_str_clean = comp_str.strip()
            try:
                self.__colorpicker.model.get_item_value_model(model).as_float = float(comp_str_clean)
            except ValueError:
                # 经常发生于输入时
                pass

    def _on_value_changed(self, *args):
        """把revert_img设为正确的状态（在值改变的时候）"""
        default_str = ",".join([self.simplify_str(val) for val in self.__defaults])
        cur_str = self.__strfield.model.as_string
        # 当前值与默认值不相等时即打开revert_img(变亮)
        self.revert_img.enabled = default_str != cur_str

    def _restore_default(self):
        """恢复到默认值"""
        if self.revert_img.enabled:
            field_str = ",".join([self.simplify_str(val) for val in self.__defaults])
            self.__strfield.model.set_value(field_str)
            self.revert_img.enabled = False

    def _build_body(self):
        """主体，包括取色器，stringfield，保持他们更新的回调函数"""
        with ui.HStack(spacing=SPACING):
            # 控件的建立基于用户输入，是默认值还是model
            if self.existing_model:
                # 用户提供model
                self.__colorpicker = ui.ColorWidget(
                    self.existing_model,
                    width=COLOR_PICKER_WIDTH,
                    height=BLOCK_HEIGHT,
                    name=COLOR_WIDGET_NAME
                )
                color_model = self.existing_model
            else:
                # 用户提供一个默认值列表
                self.__colorpicker = ui.ColorWidget(
                    *self.__defaults,
                    width=COLOR_PICKER_WIDTH,
                    height=BLOCK_HEIGHT,
                    name=COLOR_WIDGET_NAME
                )
                color_model = self.__colorpicker.model

            self.__strfield = ui.StringField(width=FIELD_WIDTH, name="attribute_color")
            self.__color_sub = self.__colorpicker.model.subscribe_item_changed_fn(
                lambda m, _, children=color_model.get_item_children():
                self.set_color_stringfield(m, children))
            self.__strfield_sub = self.__strfield.model.subscribe_value_changed_fn(
                lambda m, children=color_model.get_item_children():
                self.set_color_widget((m, children)))

            # 在开始时显示数据
            self.set_color_stringfield(self.__colorpicker.model,
                                       children=color_model.get_item_children()
                                       )
