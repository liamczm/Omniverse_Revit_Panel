__all__ = ["RvCustomComboboxWidget"]

from typing import List, Optional

import omni.ui as ui

from .custom_base_widget import CustomBaseWidget
from .style import BLOCK_HEIGHT

class RvCustomComboboxWidget(CustomBaseWidget):

    def __init__(self,
                model: ui.AbstractItemModel = None,
                options: List[str] = None,
                default_value=0,
                **kwargs):
        self.__default_val = default_value
        self.__options = options or ["1", "2", "3"]
        self.__combobox_widget = None

        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__options = None
        self.__combobox_widget = None
    
    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__combobox_widget:
            return self.__combobox_widget.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__combobox_widget.model = value

    def _on_value_changed(self, *args):

        model = self.__combobox_widget.model
        index = model.get_item_value_model().get_value_as_int()
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):

        if self.revert_img.enabled:
            self.__combobox_widget.model.get_item_value_model().set_value(
                self.__default_val)
            self.revert_img.enabled = False

    def _build_body(self):
        with ui.HStack():
            with ui.ZStack():
                ui.Rectangle(name="combobox",
                height=BLOCK_HEIGHT)

                option_list=list(self.__options)
                self.__combobox_widget=ui.ComboBox(
                    0,*option_list,
                    name="dropdown_menu",
                    height=10
                )

                with ui.HStack():
                    ui.Spacer()
                    with ui.VStack(width=0):#宽度为0保持右端对齐
                        ui.Spacer(height=5)
                        with ui.ZStack():
                            ui.Rectangle(width=15,height=15,name="combobox_icon_cover")
                            ui.Image(name="collapsable_closed",width=12,height=12)
                    ui.Spacer(width=2) #右边距
            
            #ui.Spacer(width=ui.Percent(5))

        self.__combobox_widget.model.add_item_changed_fn(self._on_value_changed)