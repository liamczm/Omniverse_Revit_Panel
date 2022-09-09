__all__ = ["CustomPathButtonWidget"]

from typing import Callable, Optional

import omni.ui as ui

from .style import ATTR_LABEL_WIDTH, BLOCK_HEIGHT


class CustomPathButtonWidget:
    """一个StringField存储路径，一个Buttong执行动作的复合组件
        TODO:要使ellision在路径栏起作用，用...开头
    """

    def __init__(self,
                 label: str,
                 path: str,
                 btn_label: str,
                 btn_callback: Callable):
        self.__attr_label = label
        self.__pathfield = ui.StringField = None
        self.__path = path
        self.__btn_label = btn_label
        self.__btn = None
        self.__callback = btn_callback
        self.__frame = ui.Frame()

        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.__pathfield = None
        self.__btn = None
        self.__callback = None
        self.__frame = None

    @property
    def model(self) -> Optional[ui.AbstractItem]:
        if self.__pathfield:
            return self.__pathfield.model

    @model.setter
    def model(self, value: ui.AbstractItem):
        self.__pathfield.model = value

    def get_path(self):
        return self.model.as_string

    def _build_fn(self):
        with ui.HStack():
            ui.Label(
                self.__attr_label,
                name="attribute_name",
                width=ATTR_LABEL_WIDTH
            )
            self.__pathfield = ui.StringField(
                name="path_field",
                height=BLOCK_HEIGHT,
                width=ui.Fraction(2)
            )
            # TODO: 为长文字加上clippingType=ELLIPSIS_LEFT
            self.__pathfield.model.set_value(self.__path)

            self.__btn = ui.Button(
                self.__btn_label,
                name="tool_button",
                height=BLOCK_HEIGHT,
                width=ui.Fraction(1),
                clicked_fn=lambda path=self.get_path(): self.__callback(path)
            )
