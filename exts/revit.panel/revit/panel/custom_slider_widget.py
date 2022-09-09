__all__ = ["CustomSliderWidget"]

from typing import Optional

import omni.ui as ui
from omni.ui import color as cl
from omni.ui import constant as fl

from .custom_base_widget import CustomBaseWidget

NUM_FIELD_WIDTH = 50
SLIDER_WIDTH = ui.Percent(100)
FIELD_HEIGHT = 22  # TODO: Once Field padding is fixed, this should be 18
SPACING = 4
TEXTURE_NAME = "slider_bg_texture"

class CustomSliderWidget(CustomBaseWidget):
    """滑杆与键入的组合组件"""
    def __init__(self,
                 model:ui.AbstractItemModel=None,
                 num_type:str="float",
                 min=0.0,
                 max=1.0,
                 default_val=0.0,
                 display_range:bool=False,
                 **kwargs):
        self.__slider:Optional[ui.AbstractSlider]=None
        self.__numberfield:Optional[ui.AbstractField]=None
        self.__min=min
        self.__max=max
        self.__default_val=default_val
        self.__num_type=num_type
        self.__display_range=display_range

        # 在最后呼起，所以build_fn可以在所有构造器初始化后生效
        CustomBaseWidget.__init__(self,model=model,**kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider=None
        self.__numberfield=None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """组件的model"""
        if self.__slider:
            return self.__slider.model
    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """组件model的setter"""
        self.__slider.model=value
        self.__numberfield.model=value

    def _on_value_changed(self, *args):
        """把revert_img设为正确的状态"""
        if self.__num_type=="float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """恢复到默认值"""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """建立在滑杆下方的文字范围"""
        with ui.HStack():
            # 左为最小值
            ui.Label(str(self.__min),alighment=ui.Alignment.LEFT,name="range_text")
            # 中部内容
            if self.__min<0 and self.__max>0:
                # 在范围显示中加入中间值0，但根据数值范围决定是否为居中位置
                total_range = self.__max - self.__min
                # 为空出末端数字的宽度减去25%
                left = 100 * abs(0-self.__min)/total_range -25
                right = 100 * abs(self.__max -0)/total_range -25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0",alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            # 右为最大值
            ui.Label(str(self.__max),alighment=ui.Alignment.RIGHT, name="range_text")

    def _build_body(self):
        """组件的主要部分，滑杆、范围数字、输入框、并且设置回调函数保持更新"""
        with ui.HStack(spacing=0):
            # 用户提供一个列表的默认值
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                with ui.ZStack():
                    # 将滑杆背景图置于此，然后让上方的滑杆完全透明，背景部分灰色透明
                    with ui.Frame(width=SLIDER_WIDTH,height=FIELD_HEIGHT, horizontal_clipping=True):
                        # Hstack参数中spacing输入负值是将材质偏移，部分重合达到视觉上无缝
                        with ui.HStack():
                            for i in range(50):# 排布材质
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(
                        height=FIELD_HEIGHT,
                        min=self.__min, max=self.__max,
                        name="attr_slider"
                    )

                if self.__display_range:
                    self._build_display_range()

            with ui.VStack(width=ui.Fraction(1)):
                model=self.__slider.model
                model.set_value(self.__default_val)
                field_cls=(
                    ui.FloatField if self.__num_type=="float" else ui.IntField
                )
                # 因为bug，需要将text占用更多的Field的空间
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1是因为边缘，所有文字不会高于滑杆
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT-1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=2)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "color":cl(0.2,0.2,0.2,1),
                                "background_color":cl.transparent,
                                "border_color":cl.transparent,
                                "padding":4,
                                "font_size":fl.field_text_font_size
                                #"color":cl(0.9,0.9,0.9,1.0)
                            }
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)