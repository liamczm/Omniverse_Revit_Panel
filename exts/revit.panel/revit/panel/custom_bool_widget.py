__all__ = ["CustomBoolWidget"]

import omni.ui as ui

from .custom_base_widget import CustomBaseWidget


class CustomBoolWidget(CustomBaseWidget):
    """自定义CheckBox"""

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 default_value: bool = True,
                 **kwargs):
        self.__default_val = default_value
        self.__bool_image = None

        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__bool_image = None

    def _restore_default(self):
        if self.revert_img.enabled:
            self.__bool_image.checked = self.__default_val
            self.__bool_image.name = (
                "checked" if self.__bool_image.checked else "unchecked"
            )
            self.revert_img.enabled = False

    def _on_value_changed(self):
        """切换Checkbox的图像, 并把revert_img设为正确的状态"""
        self.__bool_image.checked = not self.__bool_image.checked
        self.__bool_image.name = (
            "checked" if self.__bool_image.checked else "unchecked"
        )
        self.revert_img.enabled = self.__default_val != self.__bool_image.checked

    def _build_body(self):
        """绘制checkbox并绑定回调函数"""
        with ui.HStack():
            with ui.VStack():
                # 将图片向下偏移2px，与其他列对齐
                self.__bool_image = ui.Image(
                    name="checked" if self.__default_val else "unchecked",
                    fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                    height=16, width=16, checked=self.__default_val
                )
                # 用Spacer占据剩余的空间
                ui.Spacer()

        # 鼠标按下时发生的事件
        self.__bool_image.set_mouse_pressed_fn(
            lambda x, y, b, m: self._on_value_changed()
        )
