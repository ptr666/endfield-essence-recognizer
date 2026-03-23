"""
扩展的输入控制器

提供额外的输入控制功能，包括：
- Ctrl+右键点击
- 鼠标滚轮滚动
- 键盘按键模拟

这些功能是对现有WindowManager的补充，不修改原有代码。
"""

import time

import pyautogui
import pygetwindow
from pynput import keyboard

from endfield_essence_recognizer.core.window.windows_utils import _get_client_rect
from endfield_essence_recognizer.utils.log import logger


class InputController:
    """
    扩展的输入控制器
    
    提供WindowManager未包含的输入功能。
    """

    def __init__(self, window: pygetwindow.Window):
        """
        初始化输入控制器
        
        Args:
            window: 目标窗口对象
        """
        self._window = window
        self._keyboard = keyboard.Controller()

    def ctrl_right_click(self, relative_x: int, relative_y: int) -> None:
        """
        在指定位置执行Ctrl+右键点击
        
        Args:
            relative_x: 相对于窗口客户区的X坐标
            relative_y: 相对于窗口客户区的Y坐标
        """
        # 获取客户区坐标
        client_rect = _get_client_rect(self._window)
        screen_x = client_rect.x0 + relative_x
        screen_y = client_rect.y0 + relative_y

        logger.debug(
            f"执行Ctrl+右键点击: 相对坐标({relative_x}, {relative_y}) -> "
            f"屏幕坐标({screen_x}, {screen_y})"
        )

        try:
            # 移动鼠标到目标位置
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            time.sleep(0.05)

            # 按下Ctrl键
            self._keyboard.press(keyboard.Key.ctrl)
            time.sleep(0.05)

            # 右键点击
            pyautogui.rightClick(screen_x, screen_y)
            time.sleep(0.05)

            # 释放Ctrl键
            self._keyboard.release(keyboard.Key.ctrl)

            logger.debug("Ctrl+右键点击完成")

        except Exception as e:
            logger.error(f"Ctrl+右键点击失败: {e}")
            # 确保释放Ctrl键
            try:
                self._keyboard.release(keyboard.Key.ctrl)
            except Exception:
                pass
            raise

    def scroll(
        self, relative_x: int, relative_y: int, clicks: int, duration: float = 0.1
    ) -> None:
        """
        在指定位置滚动鼠标滚轮
        
        Args:
            relative_x: 相对于窗口客户区的X坐标
            relative_y: 相对于窗口客户区的Y坐标
            clicks: 滚动的点击数（正数向上，负数向下）
            duration: 滚动持续时间（秒）
        """
        # 获取客户区坐标
        client_rect = _get_client_rect(self._window)
        screen_x = client_rect.x0 + relative_x
        screen_y = client_rect.y0 + relative_y

        logger.debug(
            f"执行滚轮滚动: 相对坐标({relative_x}, {relative_y}) -> "
            f"屏幕坐标({screen_x}, {screen_y}), 点击数={clicks}"
        )

        try:
            # 移动鼠标到目标位置
            pyautogui.moveTo(screen_x, screen_y, duration=duration)
            time.sleep(0.05)

            # 滚动鼠标滚轮
            pyautogui.scroll(clicks, x=screen_x, y=screen_y)

            logger.debug("滚轮滚动完成")

        except Exception as e:
            logger.error(f"滚轮滚动失败: {e}")
            raise

    def press_key(self, key: str, duration: float = 0.1) -> None:
        """
        按下并释放指定按键
        
        Args:
            key: 按键名称（如'a', 'enter', 'esc'等）
            duration: 按键持续时间（秒）
        """
        logger.debug(f"按下按键: {key}")

        try:
            pyautogui.press(key)
            time.sleep(duration)
            logger.debug(f"按键 {key} 完成")

        except Exception as e:
            logger.error(f"按键 {key} 失败: {e}")
            raise

    def hold_key(self, key: str) -> None:
        """
        按住指定按键（不释放）
        
        Args:
            key: 按键名称
        """
        logger.debug(f"按住按键: {key}")
        pyautogui.keyDown(key)

    def release_key(self, key: str) -> None:
        """
        释放指定按键
        
        Args:
            key: 按键名称
        """
        logger.debug(f"释放按键: {key}")
        pyautogui.keyUp(key)

    def type_text(self, text: str, interval: float = 0.05) -> None:
        """
        输入文本
        
        Args:
            text: 要输入的文本
            interval: 每个字符之间的间隔时间（秒）
        """
        logger.debug(f"输入文本: {text}")

        try:
            pyautogui.write(text, interval=interval)
            logger.debug("文本输入完成")

        except Exception as e:
            logger.error(f"文本输入失败: {e}")
            raise

    def double_click(self, relative_x: int, relative_y: int) -> None:
        """
        在指定位置执行双击
        
        Args:
            relative_x: 相对于窗口客户区的X坐标
            relative_y: 相对于窗口客户区的Y坐标
        """
        # 获取客户区坐标
        client_rect = _get_client_rect(self._window)
        screen_x = client_rect.x0 + relative_x
        screen_y = client_rect.y0 + relative_y

        logger.debug(
            f"执行双击: 相对坐标({relative_x}, {relative_y}) -> "
            f"屏幕坐标({screen_x}, {screen_y})"
        )

        try:
            pyautogui.doubleClick(screen_x, screen_y)
            logger.debug("双击完成")

        except Exception as e:
            logger.error(f"双击失败: {e}")
            raise

    def drag(
        self,
        from_x: int,
        from_y: int,
        to_x: int,
        to_y: int,
        duration: float = 0.5,
    ) -> None:
        """
        拖拽操作
        
        Args:
            from_x: 起始X坐标（相对于窗口客户区）
            from_y: 起始Y坐标（相对于窗口客户区）
            to_x: 目标X坐标（相对于窗口客户区）
            to_y: 目标Y坐标（相对于窗口客户区）
            duration: 拖拽持续时间（秒）
        """
        # 获取客户区坐标
        client_rect = _get_client_rect(self._window)
        screen_from_x = client_rect.x0 + from_x
        screen_from_y = client_rect.y0 + from_y
        screen_to_x = client_rect.x0 + to_x
        screen_to_y = client_rect.y0 + to_y

        logger.debug(
            f"执行拖拽: ({from_x}, {from_y}) -> ({to_x}, {to_y}), "
            f"屏幕坐标: ({screen_from_x}, {screen_from_y}) -> ({screen_to_x}, {screen_to_y})"
        )

        try:
            # 移动到起始位置
            pyautogui.moveTo(screen_from_x, screen_from_y, duration=0.1)
            time.sleep(0.05)

            # 拖拽到目标位置
            pyautogui.drag(
                screen_to_x - screen_from_x,
                screen_to_y - screen_from_y,
                duration=duration,
            )

            logger.debug("拖拽完成")

        except Exception as e:
            logger.error(f"拖拽失败: {e}")
            raise
