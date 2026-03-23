"""
仓库转移扫描器

实现完整的仓库物品转移流程：
1. 自动存放背包物品
2. 选择物品分类
3. 查找并点击目标物品
4. Ctrl+右键转移物品
5. 切换仓库
6. 自动存放背包物品
7. 切换回源仓库
8. 循环执行
"""

import threading
import time

import numpy as np

from endfield_essence_recognizer.core.layout.base import Point
from endfield_essence_recognizer.core.window import WindowManager
from endfield_essence_recognizer.utils.log import logger
from endfield_essence_recognizer.warehouse_transfer.config.layout_1080p import (
    WarehouseLayout1080p,
)
from endfield_essence_recognizer.warehouse_transfer.config.transfer_config import (
    TransferConfig,
    TransferItem,
)
from endfield_essence_recognizer.warehouse_transfer.core.input_controller import (
    InputController,
)
from endfield_essence_recognizer.warehouse_transfer.core.item_recognizer import (
    ItemRecognizer,
)


class WarehouseTransferScanner(threading.Thread):
    """
    仓库物品转移扫描器
    
    后台线程，自动执行仓库之间的物品转移任务。
    """

    def __init__(
        self,
        window_manager: WindowManager,
        input_controller: InputController,
        item_recognizer: ItemRecognizer,
        layout: WarehouseLayout1080p,
        config: TransferConfig,
    ):
        """
        初始化仓库转移扫描器
        
        Args:
            window_manager: 窗口管理器
            input_controller: 输入控制器
            item_recognizer: 物品识别器
            layout: 仓库布局配置
            config: 转移任务配置
        """
        super().__init__(daemon=True)
        self._window_manager = window_manager
        self._input_controller = input_controller
        self._item_recognizer = item_recognizer
        self._layout = layout
        self._config = config

        self._running = threading.Event()
        self._loop_count = 0

        # 验证配置
        self._config.validate()

        logger.info("仓库转移扫描器已初始化")
        logger.info(f"源仓库: {config.source_warehouse}")
        logger.info(f"目标仓库: {config.target_warehouse}")
        logger.info(f"转移物品: {[item.name for item in config.transfer_items]}")

    def run(self) -> None:
        """执行转移循环"""
        logger.info("开始仓库转移任务...")
        self._running.set()

        # 检查窗口是否存在
        if not self._window_manager.target_exists:
            logger.error("未找到游戏窗口，停止转移任务")
            self._running.clear()
            return

        # 激活窗口
        if self._window_manager.restore():
            time.sleep(0.5)
        if self._window_manager.activate():
            time.sleep(0.5)

        # 主循环
        while self._running.is_set():
            try:
                # 检查是否达到最大循环次数
                if (
                    self._config.max_loops > 0
                    and self._loop_count >= self._config.max_loops
                ):
                    logger.info(
                        f"已达到最大循环次数 {self._config.max_loops}，停止转移任务"
                    )
                    break

                self._loop_count += 1
                logger.info(f"========== 开始第 {self._loop_count} 次循环 ==========")

                # 执行转移流程
                self._execute_transfer_cycle()

                logger.info(f"========== 第 {self._loop_count} 次循环完成 ==========")

                # 循环间隔
                time.sleep(self._config.delays.loop_interval)

            except Exception as e:
                logger.error(f"转移循环出错: {e}", exc_info=True)
                if self._config.stop_on_error:
                    logger.error("配置为遇到错误停止，终止转移任务")
                    break
                else:
                    logger.warning("继续执行下一次循环...")
                    time.sleep(self._config.delays.loop_interval)

        logger.info("仓库转移任务已停止")
        self._running.clear()

    def _execute_transfer_cycle(self) -> None:
        """执行一次完整的转移循环"""

        # 步骤1: 自动存放背包物品（在源仓库）
        logger.info("步骤1: 自动存放背包物品（源仓库）")
        self._auto_store_backpack()

        # 遍历所有要转移的物品
        for item in self._config.transfer_items:
            logger.info(f"开始转移物品: {item.name} (分类: {item.category})")

            # 步骤2: 选择物品分类
            logger.info(f"步骤2: 选择物品分类 - {item.category}")
            self._select_category(item.category)

            # 步骤3: 查找并点击目标物品
            logger.info(f"步骤3: 查找物品 - {item.name}")
            item_pos = self._find_item(item.name)

            if item_pos is None:
                logger.warning(f"未找到物品 {item.name}，跳过")
                continue

            # 步骤4: Ctrl+右键点击物品
            logger.info(f"步骤4: Ctrl+右键点击物品 - {item.name}")
            self._ctrl_right_click_item(item_pos)

        # 步骤5: 切换到目标仓库
        logger.info(f"步骤5: 切换到目标仓库 - {self._config.target_warehouse}")
        self._switch_warehouse(self._config.target_warehouse)

        # 步骤6: 自动存放背包物品（在目标仓库）
        logger.info("步骤6: 自动存放背包物品（目标仓库）")
        self._auto_store_backpack()

        # 步骤7: 切换回源仓库
        logger.info(f"步骤7: 切换回源仓库 - {self._config.source_warehouse}")
        self._switch_warehouse(self._config.source_warehouse)

    def _auto_store_backpack(self) -> None:
        """点击自动存放按钮"""
        pos = self._layout.AUTO_STORE_BUTTON_POS
        logger.debug(f"点击自动存放按钮: ({pos.x}, {pos.y})")

        self._window_manager.click(pos.x, pos.y)
        time.sleep(self._config.delays.after_store)

    def _select_category(self, category: str) -> None:
        """
        选择物品分类
        
        Args:
            category: 分类名称
        """
        category_buttons = self._layout.CATEGORY_BUTTONS

        if category not in category_buttons:
            logger.error(f"未知的物品分类: {category}")
            logger.error(f"可用的分类: {list(category_buttons.keys())}")
            raise ValueError(f"未知的物品分类: {category}")

        pos = category_buttons[category]
        logger.debug(f"点击分类按钮 '{category}': ({pos.x}, {pos.y})")

        self._window_manager.click(pos.x, pos.y)
        time.sleep(self._config.delays.after_category_select)

    def _find_item(self, item_name: str) -> Point | None:
        """
        在仓库网格中查找指定物品
        
        支持滚动查找。如果在当前可见区域未找到，会向下滚动继续查找。
        
        Args:
            item_name: 物品名称
        
        Returns:
            物品的坐标，如果未找到则返回None
        """
        scroll_attempts = 0
        max_scroll_attempts = self._config.recognition.max_scroll_attempts

        while scroll_attempts <= max_scroll_attempts:
            logger.debug(
                f"查找物品 '{item_name}' (滚动尝试 {scroll_attempts}/{max_scroll_attempts})"
            )

            # 遍历当前可见的网格
            for row_idx in range(len(self._layout.warehouse_grid_y_list)):
                for col_idx in range(len(self._layout.warehouse_grid_x_list)):
                    # 获取物品ROI区域
                    roi = self._layout.get_item_roi(col_idx, row_idx)

                    # 截取ROI图像
                    try:
                        screenshot = self._window_manager.screenshot(roi)
                    except Exception as e:
                        logger.warning(f"截取ROI失败 ({col_idx}, {row_idx}): {e}")
                        continue

                    # 识别物品
                    recognized_item, score = self._item_recognizer.recognize_roi(
                        screenshot
                    )

                    logger.trace(
                        f"网格 ({col_idx}, {row_idx}): 识别结果={recognized_item}, 分数={score:.3f}"
                    )

                    # 检查是否匹配
                    if (
                        recognized_item == item_name
                        and score >= self._config.recognition.item_low_threshold
                    ):
                        # 找到目标物品
                        center_x = self._layout.warehouse_grid_x_list[col_idx]
                        center_y = self._layout.warehouse_grid_y_list[row_idx]
                        logger.success(
                            f"找到物品 '{item_name}' 在网格 ({col_idx}, {row_idx}), "
                            f"坐标 ({center_x}, {center_y}), 分数 {score:.3f}"
                        )
                        return Point(center_x, center_y)

            # 当前可见区域未找到，尝试向下滚动
            if scroll_attempts < max_scroll_attempts:
                logger.debug(f"当前区域未找到物品 '{item_name}'，向下滚动...")
                self._scroll_down()
                scroll_attempts += 1
            else:
                break

        # 未找到物品
        logger.warning(
            f"在 {max_scroll_attempts + 1} 次尝试后仍未找到物品 '{item_name}'"
        )
        return None

    def _scroll_down(self) -> None:
        """向下滚动仓库列表"""
        scroll_center = self._layout.SCROLL_CENTER
        scroll_clicks = self._config.recognition.scroll_clicks

        logger.debug(
            f"在 ({scroll_center.x}, {scroll_center.y}) 向下滚动 {abs(scroll_clicks)} 次"
        )

        self._input_controller.scroll(scroll_center.x, scroll_center.y, scroll_clicks)
        time.sleep(self._config.delays.after_scroll)

    def _ctrl_right_click_item(self, pos: Point) -> None:
        """
        Ctrl+右键点击物品
        
        Args:
            pos: 物品坐标
        """
        logger.debug(f"Ctrl+右键点击物品: ({pos.x}, {pos.y})")

        self._input_controller.ctrl_right_click(pos.x, pos.y)
        time.sleep(self._config.delays.after_ctrl_right_click)

    def _switch_warehouse(self, warehouse_name: str) -> None:
        """
        切换仓库
        
        Args:
            warehouse_name: 目标仓库名称
        """
        warehouse_positions = self._layout.WAREHOUSE_SELECT_POSITIONS

        if warehouse_name not in warehouse_positions:
            logger.error(f"未知的仓库名称: {warehouse_name}")
            logger.error(f"可用的仓库: {list(warehouse_positions.keys())}")
            raise ValueError(f"未知的仓库名称: {warehouse_name}")

        # 1. 点击仓库切换按钮
        logger.debug("点击仓库切换按钮")
        pos = self._layout.WAREHOUSE_SWITCH_BUTTON_POS
        self._window_manager.click(pos.x, pos.y)
        time.sleep(self._config.delays.after_click)

        # 2. 选择目标仓库
        logger.debug(f"选择仓库: {warehouse_name}")
        pos = warehouse_positions[warehouse_name]
        self._window_manager.click(pos.x, pos.y)
        time.sleep(self._config.delays.after_click)

        # 3. 点击确认按钮
        logger.debug("点击确认按钮")
        pos = self._layout.WAREHOUSE_CONFIRM_BUTTON_POS
        self._window_manager.click(pos.x, pos.y)
        time.sleep(self._config.delays.after_switch)

        # 4. 关闭切换界面
        logger.debug("关闭切换界面")
        pos = self._layout.WAREHOUSE_CLOSE_BUTTON_POS
        self._window_manager.click(pos.x, pos.y)
        time.sleep(self._config.delays.after_click)

        logger.info(f"已切换到仓库: {warehouse_name}")

    def stop(self) -> None:
        """停止转移任务"""
        logger.info("正在停止仓库转移任务...")
        self._running.clear()

    @property
    def is_running(self) -> bool:
        """检查扫描器是否正在运行"""
        return self._running.is_set()

    @property
    def loop_count(self) -> int:
        """获取已执行的循环次数"""
        return self._loop_count
