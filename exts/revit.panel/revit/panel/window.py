__all__ = ["RevitPanelWindow"]




import omni.ui as ui
from omni.ui import color as cl
from omni.kit.window.popup_dialog import MessageDialog

from .style import revit_panel_style, ATTR_LABEL_WIDTH

from .custom_slider_widget import CustomSliderWidget
from .custom_multifield_widget import CustomMultifieldWidget
from .custom_color_widget import CustomColorWidget
from .custom_bool_widget import CustomBoolWidget
from .custom_radio_collection import CustomRadioCollection
from .custom_path_button_widget import CustomPathButtonWidget
from .custom_combobox_widget import RvCustomComboboxWidget
from .treeview import TreeViewLayout

SPACING = 5
SPACER_HEIGHT=6


class RevitPanelWindow(ui.Window):
    """窗口的class"""

    # show_window()调用该类的构造器，即__init__
    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = ATTR_LABEL_WIDTH

        # 初始化该类的所有基础类(ui.Window)
        super().__init__(title, **kwargs)

        # 将风格应用与所有窗口组件
        self.frame.style = revit_panel_style

        # 设置窗口可见时建立所有组件的方法
        self.frame.set_build_fn(self._build_fn)

    def destroy(self):
        super().destroy()

    @property
    def label_width(self):
        """属性标题的宽度"""
        return self.__label_width

    @label_width.setter
    def label_width(self, value):
        """属性标题的宽度setter"""
        self.__label_width = value
        self.frame.rebuild()

    def on_export_btn_click(self, path):
        """当导出按钮按下的实例方法"""
        dialog = MessageDialog(
            title="Button Pressed",
            message=f"Import from {path}",
            ok_handler=lambda dialog: dialog.hide()
        )
        dialog.show()

    def _build_title(self):
        with ui.VStack(height=50):
            ui.Spacer(height=5)
            ui.Label("Revit Panel beta", name="window_title")
            ui.Spacer(height=5)

    def _build_collapsable_header(self, collapsed, title):
        """建立一个CollapsableFrame的自定义标题"""
        with ui.VStack():
            ui.Spacer(height=8)
            with ui.HStack():
                ui.Label(title, name="collapsable_name", style={"color":cl(0.2,0.2,0.2,1)})
                # 更换图标
                if collapsed:
                    image_name = "collapsable_opened"
                else:
                    image_name = "collapsable_closed"
            ui.Spacer(height=8)
            ui.Line(style_type_name_override="HeaderLine")

    def _build_geoInfos(self):
        with ui.CollapsableFrame("Geometry".upper(), name="group",height=0,
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)
                with ui.HStack():
                    ui.Spacer(width=20)
                    ui.Image(name="wall_type",
                            width=100,
                            fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                            alignment=ui.Alignment.LEFT_TOP)
                    #ui.Spacer(width=10)
                    with ui.VStack(spacing=SPACING):
                        with ui.HStack():
                            ui.Label("Family",name="attribute_name")
                            family_field=ui.StringField(style={"color":cl(0.2,0.2,0.2,1)})
                            family_field.model.set_value("Wall")
                        with ui.HStack():
                            ui.Label("Type",name="attribute_name")
                            type_field=ui.StringField(style={"color":cl(0.2,0.2,0.2,1)})
                            type_field.model.set_value("ConcreteWall")

    def _build_geoPosition(self):
        with ui.CollapsableFrame("Position".upper(),name="group",height=0,
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)
                with ui.HStack():
                    ui.Image(name="wall_pos",
                            width=100,
                            fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                            alignment=ui.Alignment.LEFT_TOP
                            )
                    ui.Spacer(width=5)
                    with ui.VStack():
                        ui.Spacer(height=6)

                        CustomSliderWidget(min=0,max=2000,num_type="float",
                                        label="TopOffset",default_val=0)
                        CustomSliderWidget(min=0,max=6,num_type="int",
                                        label="BaseStory",default_val=1)
                        CustomSliderWidget(min=0, max=2000, num_type="float",
                                        label="BottomOffset", default_val=0)

    def _build_looks(self):
        with ui.CollapsableFrame("Material Wizzard".upper(),name="group",height=0,
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0,spacing=SPACING):
                ui.Spacer(height=6)
                with ui.HStack(spacing=SPACING):
                    ui.Image(name="mat_concrete",
                            fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                            width=90,
                            alignment=ui.Alignment.LEFT_TOP,
                            style={"border_radius":10})
                    ui.Spacer(width=6)
                    with ui.VStack():
                        ui.Spacer(height=2)
                        RvCustomComboboxWidget(label="MaterialType",
                                                options=["Concrete", "Wood","Metal","Glass","Water"])
                        CustomSliderWidget(min=0,max=1,num_type="float",
                                            label="Reflective",default_val=0.5)
                        CustomSliderWidget(min=0,max=1,num_type="float",
                                            label="Roughness")
                        CustomBoolWidget(label="Emissive", default_value=True)
                        CustomSliderWidget(min=0,max=500000,num_type="int",
                                            label="Strength")
                        CustomBoolWidget(label="Opacity", default_value=False)
                        CustomSliderWidget(min=0,max=1.0,num_type="float",
                                            label="OpacityAmount")
    
    def _build_cameras(self):
        with ui.CollapsableFrame("Cameras".upper(),name="group",height=0,
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0,spacing=SPACING):
                ui.Spacer(height=6)
                with ui.HStack():
                    TreeViewLayout.InitLayout(self)
                    with ui.VStack():
                        RvCustomComboboxWidget(label="CameraType",
                                            options=["Perspective", "Orthographic"])
                        # TODO:CameraList
                        # camera_field=ui.TreeView()
                        # camera_field.model.set_value("Wall","tree")
                        
                        CustomSliderWidget(min=0,max=300,num_type="int",
                        label="Focal Length",default_val=30)
                        CustomSliderWidget(min=0,max=1000,num_type="float",
                        label="Focus Distance",default_val=100)
                        CustomSliderWidget(min=0,max=30,num_type="float",
                        label="fStop",default_val=0)

    def _build_parameters(self):
        """建立Parameters组"""
        with ui.CollapsableFrame("Parameters".upper(), name="group",
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                CustomSliderWidget(min=-2, max=2, display_range=True,
                                   label="Height", default_val=0.75)
                CustomSliderWidget(min=0, max=2, display_range=True,
                                   label="Thickness", default_val=0.65)
                CustomSliderWidget(min=0, max=2, display_range=True,
                                   label="Area", default_val=0.65)

    def _build_environment(self):
        """建立Scene组"""
        with ui.CollapsableFrame("Environment".upper(), name="group",height=0,
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0,spacing=SPACING):
                ui.Spacer(height=6)

                # CustomPathButtonWidget(
                #     label="importHDR",
                #     path="hdrPath",
                #     btn_label="Import",
                #     btn_callback=self.on_export_btn_click,
                # )
                CustomSliderWidget(min=0, max=1.0, display_range=False,
                                 label="Strength", default_val=1)
                with ui.HStack():
                    CustomBoolWidget(label="Sun", default_value=False)
                    CustomColorWidget(0.9, 0.9, 0.1, label="Temprature")
                CustomMultifieldWidget(
                    label="Date",
                    sublabels=["Day", "Month","Time"],
                    default_vals=[31, 11,14]
                )

    def _build_scene(self):
        """Build the widgets of the "Scene" group"""
        with ui.CollapsableFrame("Environment".upper(), name="group",
                                    build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                CustomSliderWidget(min=0.0, max=10, display_range=False,
                                     label="Strength", default_val=1)

                CustomMultifieldWidget(
                    label="Orientation",
                    default_vals=[0.0, 0.0, 0.0]
                )

                CustomSliderWidget(min=0, max=2, label="Camera Distance", default_val=.1)

                CustomBoolWidget(label="Antialias", default_value=False)

                CustomBoolWidget(label="Ambient Occlusion", default_value=True)

                CustomMultifieldWidget(
                    label="Ambient Distance",
                    sublabels=["Min", "Max"],
                    default_vals=[0.0, 200.0]
                )

                CustomComboboxWidget(label="Ambient Falloff",
                                        options=["Linear", "Quadratic", "Cubic"])

                CustomColorWidget(.6, 0.62, 0.9, label="Background Color")

                CustomRadioCollection("Render Method", labels=["Path Traced", "Volumetric"],
                                        default_value=1)

                CustomPathButtonWidget(
                    label="Export Path",
                    path=".../icon/",
                    btn_label="Export",
                    btn_callback=self.on_export_btn_click,
                )

                ui.Spacer(height=10)
    def _build_fn(self):
        """当窗口可见时建立所有的UI组"""
        with ui.ScrollingFrame(name="window_big",
                               vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
                               horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF):
            with ui.VStack():
                self._build_title()
                self._build_geoInfos()
                self._build_geoPosition()
                self._build_parameters()
                self._build_looks()
                self._build_cameras()
                self._build_environment()


