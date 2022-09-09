__all__ = ["RevitPanelExtension"]

import asyncio
from functools import partial

import omni.ext
from omni.kit.window.popup_dialog import style
import omni.ui as ui

from .style import WIN_WIDTH, WIN_HEIGHT
from .window import RevitPanelWindow


class RevitPanelExtension(omni.ext.IExt):
    """窗口入口"""
    WINDOW_NAME = "Revit View Panel"
    MENU_PATH = f"Window/{WINDOW_NAME}"

    def on_startup(self):
        ui.Workspace.set_show_window_fn(RevitPanelExtension.WINDOW_NAME, partial(self.show_window, None))

        # 添加新菜单
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item(
                RevitPanelExtension.MENU_PATH,
                self.show_window,
                toggle=True,
                value=True
            )

        # 显示窗口，会呼起self.show_window方法
        ui.Workspace.show_window(RevitPanelExtension.WINDOW_NAME)

    def on_shutdown(self):
        self._menu = None
        if self._window:
            self._window.destroy()
            self._window = None

        # 从omni.ui取消注册显示窗口的方法
        ui.Workspace.set_show_window_fn(RevitPanelExtension.WINDOW_NAME, None)

    def _set_menu(self, value):
        """创建控制窗口开关的菜单"""
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(RevitPanelExtension.MENU_PATH, value)

    async def _destroy_window_async(self):
        await omni.kit.app.get_app().next_update_async()
        if self._window:
            self._window.destroy()
            self._window = None

    def _visibility_changed_fn(self, visible):
        # 当用户按下关闭按键时呼起
        self._set_menu(visible)
        if not visible:
            # 摧毁窗口，因为在show_window中创建新窗口
            asyncio.ensure_future(self._destroy_window_async())

    def show_window(self, menu, value):
        if value:
            self._window = RevitPanelWindow(
                RevitPanelExtension.WINDOW_NAME, width=WIN_WIDTH, height=WIN_HEIGHT,
            )
            self._window.set_visibility_changed_fn(self._visibility_changed_fn)
        elif self._window:
            self._window.visible = False
