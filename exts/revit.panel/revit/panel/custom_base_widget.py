__all__ = ["CustomBaseWidget"]

from typing import Optional

import omni.ui as ui

from .style import ATTR_LABEL_WIDTH

class CustomBaseWidget:
    """遵循标题-部件-尾部件的自定义部件基础类"""

    def __init__(self, *args, model=None, **kwargs):
        self.existing_model: Optional[ui.AbstractItemModel] = kwargs.pop("model", None)
        self.revert_img = None
        self.__attr_label: Optional[str] = kwargs.pop("label","")
        self.__frame=ui.Frame()
        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.existing_model = None
        self.revert_img = None
        self.__attr_label = None
        self.__frame = None

    def __getattr__(self, attr):
        """假设是self.__frame，所以可以得到高宽"""
        return getattr(self.__frame, attr)

    def _build_head(self):
        """建立标题，即组件行左部文字"""
        ui.Label(
            self.__attr_label,
            name="attribute_name",
            width=ATTR_LABEL_WIDTH
        )

    def _build_body(self):
        """建立组件部分，大部分都是重载"""
        ui.Spacer()

    def _build_tail(self):
        """建立组件行右部分尾部，这里作为复原键"""
        with ui.HStack(width=0):
            ui.Spacer(width=5)
            self.revert_img = ui.Image(
                name="revert_arrow",
                fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                width=12,
                height=13,
                enabled=False,
            )
        ui.Spacer(width=5)

        # 作为revert_img按键的call-back，重置为默认值
        self.revert_img.set_mouse_pressed_fn(
            lambda x, y, b, m:self._restore_default()
        )

    def _build_fn(self):
        """将头、身、尾组合在一起"""
        with ui.HStack():
            self._build_head()
            self._build_body()
            self._build_tail()

