__all__ = ["CustomRadioCollection"]

from typing import List, Optional

import omni.ui as ui

from .style import ATTR_LABEL_WIDTH

SPACING=5

class CustomRadioCollection:
    """自定义RadioButton，group_name为第一行，接下来每行为label和radioButton
        没有从CustomBaseWidget继承是因为结构不同，也没有复原按键
    """

    def __init__(self,
                 group_name:str,
                 labels:List[str],
                 model:ui.AbstractItemModel=None,
                 default_value:bool=True,
                 **kwargs):
        self.__group_name=group_name
        self.__labels=labels
        self.__default_val=default_value
        self.__images=[]
        self.__selection_model=ui.SimpleIntModel(default_value)
        self.__frame=ui.Frame()
        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.__images=[]
        self.__selection_model=None
        self.__frame=None

    @property
    def model(self)->Optional[ui.AbstractValueModel]:
        if self.__selection_model:
            return self.__selection_model

    @model.setter
    def model(self,value:int):
        self.__selection_model.set(value)

    def __getattr__(self, attr):
        # 得到frame的宽高
        return getattr(self.__frame,attr)

    def _on_value_changed(self,index:int=0):
        """为所有的radiobutton设置状态，保证只有一个开启"""
        self.__selection_model.set_value(index)
        for i,img in enumerate(self.__images):
            img.checked= i==index
            img.name="radio_on" if img.checked else "radio_off"

    def _build_fn(self):
        """主体，绘制group_name标题，和每行的radiobutton及回调函数"""
        with ui.VStack(spacing=SPACING):
            ui.Spacer(height=2)
            ui.Label(self.__group_name.upper(),name="radio_group_name",
                     width=ATTR_LABEL_WIDTH)

            for i,label in enumerate(self.__labels):
                with ui.HStack():
                    with ui.VStack():
                        ui.Spacer(height=2)
                        self.__images.append(
                            ui.Image(
                                name=("radio on" if self.__default_val==i else "radio off"),
                                fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                                height=16,width=16,checked=self.__default_val
                            )
                        )
                    ui.Spacer()
            ui.Spacer(height=2)

        # 为每个radio button的图设置一个鼠标点击的回调
        for i in range(len(self.__labels)):
            self.__images[i].set_mouse_pressed_fn(
                lambda x,y,b,m,i=i:self._on_value_changed(i)
            )