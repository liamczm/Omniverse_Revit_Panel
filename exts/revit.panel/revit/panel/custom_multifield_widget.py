__all__ = ["CustomMultifieldWidget"]

from typing import List, Optional

import omni.ui as ui

from .custom_base_widget import CustomBaseWidget


class CustomMultifieldWidget(CustomBaseWidget):
    """自定义多行填入框，以及自定义子标签"""

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 sublabels: Optional[List[str]] = None,
                 default_vals: Optional[List[float]] = None,
                 **kwargs):
        self.__field_labels = sublabels or ["X", "Y", "Z"]
        self.__default_vals = default_vals or [0.0] * len(self.__field_labels)
        self.__multifields = []

        # 在所有数据初始化再build_fn
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__multifields = []

    @property
    def model(self, index: int = 0) -> Optional[ui.AbstractItemModel]:
        """组件的model"""
        if self.__multifields:
            return self.__multifields[index].model

    @model.setter
    def model(self,value:ui.AbstractItemModel,index:int=0):
        """组件model的setter"""
        self.__multifields[index].model=value

    def _restore_default(self):
        if self.revert_img.enabled:
            for i in range(len(self.__multifields)):
                model = self.__multifields[i].model
                model.as_float=self.__default_vals[i]
            self.revert_img.enabled=False

    def _on_value_changed(self,val_model:ui.SimpleFloatModel,index:int):
        """将revert_img设为正确的状态"""
        val=val_model.as_float
        self.revert_img.enabled=self.__default_vals[index]!=val

    def _build_body(self):
        """主体：建立各个label下的field，及回调函数保持更新"""
        with ui.HStack():
            for i, (label,val) in enumerate(zip(self.__field_labels,self.__default_vals)):
                with ui.HStack(spacing=3):
                    ui.Label(label, name="multi_attr_label",width=0)
                    model=ui.SimpleFloatModel(val)
                    # 这里有bug
                    self.__multifields.append(
                        ui.IntField(model=model,name="multi_attr_field")
                    )
                if i<len(self.__default_vals)-1:
                    # 只在field之间设置spacing，最后一个不需要
                    ui.Spacer(width=10)

        for i,f in enumerate(self.__multifields):
            f.model.add_value_changed_fn(lambda v: self._on_value_changed(v, i))
