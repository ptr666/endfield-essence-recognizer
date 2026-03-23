"""
坐标校准工具

帮助用户标记游戏界面中的关键位置，自动生成坐标配置文件。

使用方法:
1. 运行此脚本
2. 按照提示依次点击标记各个位置
3. 脚本会自动生成 layout_1080p.py 配置文件
"""

import sys
from pathlib import Path

import cv2
import numpy as np

from endfield_essence_recognizer.core.window import WindowManager
from endfield_essence_recognizer.utils.log import logger


class CoordinateCalibrator:
    """坐标校准工具"""

    def __init__(self, window_manager: WindowManager):
        self.window_manager = window_manager
        self.screenshot = None
        self.points = {}
        self.current_label = None

    def capture_screenshot(self) -> bool:
        """捕获游戏窗口截图"""
        try:
            self.screenshot = self.window_manager.screenshot()
            logger.info(f"截图成功，尺寸: {self.screenshot.shape[:2][::-1]}")
            return True
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return False

    def mouse_callback(self, event, x, y, flags, param):
        """鼠标回调函数"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.current_label:
                self.points[self.current_label] = (x, y)
                logger.info(f"已标记 '{self.current_label}': ({x}, {y})")

                # 在图像上绘制标记
                cv2.circle(self.screenshot, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(
                    self.screenshot,
                    self.current_label,
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )
                cv2.imshow("Calibration", self.screenshot)

    def mark_point(self, label: str, description: str) -> tuple[int, int] | None:
        """
        标记一个点
        
        Args:
            label: 标签名称
            description: 描述信息
        
        Returns:
            坐标 (x, y)，如果用户跳过则返回None
        """
        logger.info("=" * 60)
        logger.info(f"请标记: {description}")
        logger.info("在窗口中点击目标位置，或按 's' 跳过")
        logger.info("=" * 60)

        self.current_label = label

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                logger.warning(f"跳过标记: {label}")
                return None

            if label in self.points:
                return self.points[label]

    def mark_grid(
        self, rows: int, cols: int, description: str
    ) -> tuple[list[int], list[int]]:
        """
        标记网格
        
        Args:
            rows: 行数
            cols: 列数
            description: 描述信息
        
        Returns:
            (x_list, y_list) 坐标列表
        """
        logger.info("=" * 60)
        logger.info(f"请标记网格: {description}")
        logger.info(f"需要标记 {rows} 行 × {cols} 列 = {rows * cols} 个点")
        logger.info("=" * 60)

        points = []
        for row in range(rows):
            for col in range(cols):
                label = f"grid_{row}_{col}"
                pos = self.mark_point(
                    label, f"网格 第{row+1}行 第{col+1}列 的中心点"
                )
                if pos:
                    points.append(pos)

        # 提取X和Y坐标列表
        x_coords = [p[0] for p in points[::cols]]  # 每行第一个点的X坐标
        y_coords = [p[1] for p in points[:cols]]  # 第一行所有点的Y坐标

        return x_coords, y_coords

    def run(self):
        """运行校准流程"""
        logger.info("=" * 60)
        logger.info("坐标校准工具")
        logger.info("=" * 60)

        # 捕获截图
        if not self.capture_screenshot():
            return

        # 创建窗口
        cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Calibration", self.mouse_callback)
        cv2.imshow("Calibration", self.screenshot)

        # 标记各个位置
        calibration_data = {}

        # 1. 标记仓库网格
        logger.info("\n【第1步】标记仓库物品网格")
        x_list, y_list = self.mark_grid(4, 8, "仓库物品网格 (4行×8列)")
        calibration_data["warehouse_grid_x_list"] = x_list
        calibration_data["warehouse_grid_y_list"] = y_list

        # 2. 标记功能按钮
        logger.info("\n【第2步】标记功能按钮")
        pos = self.mark_point("auto_store", "自动存放按钮")
        if pos:
            calibration_data["AUTO_STORE_BUTTON_POS"] = pos

        pos = self.mark_point("warehouse_switch", "仓库切换按钮")
        if pos:
            calibration_data["WAREHOUSE_SWITCH_BUTTON_POS"] = pos

        pos = self.mark_point("warehouse_select", "仓库选择按钮（在切换界面中选择目标仓库）")
        if pos:
            calibration_data["WAREHOUSE_SELECT_BUTTON_POS"] = pos

        pos = self.mark_point("confirm", "确认按钮")
        if pos:
            calibration_data["WAREHOUSE_CONFIRM_BUTTON_POS"] = pos

        pos = self.mark_point("close", "关闭按钮")
        if pos:
            calibration_data["WAREHOUSE_CLOSE_BUTTON_POS"] = pos

        # 3. 标记分类按钮
        logger.info("\n【第3步】标记物品分类按钮")
        categories = ["全部", "矿物", "材料", "消耗品", "装备", "武器", "道具", "其他"]
        category_buttons = {}
        for category in categories:
            pos = self.mark_point(f"category_{category}", f"'{category}' 分类按钮")
            if pos:
                category_buttons[category] = pos
        calibration_data["CATEGORY_BUTTONS"] = category_buttons

        # 注意：仓库选择位置和滚动区域不需要标记，使用默认配置即可
        logger.info("\n【完成】坐标标记完成！")

        cv2.destroyAllWindows()

        # 生成配置文件
        self.generate_config_file(calibration_data)

    def generate_config_file(self, data: dict):
        """生成配置文件"""
        logger.info("\n" + "=" * 60)
        logger.info("生成配置文件...")
        logger.info("=" * 60)

        # 构建配置文件内容
        config_content = '''"""
自动生成的仓库布局配置文件

此文件由 calibrate_coordinates.py 工具自动生成。
"""

from collections.abc import Sequence
from endfield_essence_recognizer.core.layout.base import Point, Region


class WarehouseLayout1080p:
    """1920×1080分辨率的仓库界面布局配置（自动生成）"""

    @property
    def RESOLUTION(self) -> tuple[int, int]:
        return (1920, 1080)

'''

        # 添加网格坐标
        if "warehouse_grid_x_list" in data:
            x_list = data["warehouse_grid_x_list"]
            config_content += f"""    @property
    def warehouse_grid_x_list(self) -> Sequence[int]:
        return {x_list}

"""

        if "warehouse_grid_y_list" in data:
            y_list = data["warehouse_grid_y_list"]
            config_content += f"""    @property
    def warehouse_grid_y_list(self) -> Sequence[int]:
        return {y_list}

"""

        # 添加功能按钮
        for key in [
            "AUTO_STORE_BUTTON_POS",
            "WAREHOUSE_SWITCH_BUTTON_POS",
            "WAREHOUSE_SELECT_BUTTON_POS",
            "WAREHOUSE_CONFIRM_BUTTON_POS",
            "WAREHOUSE_CLOSE_BUTTON_POS",
        ]:
            if key in data:
                x, y = data[key]
                config_content += f"""    @property
    def {key}(self) -> Point:
        return Point({x}, {y})

"""

        # 添加分类按钮
        if "CATEGORY_BUTTONS" in data:
            buttons = data["CATEGORY_BUTTONS"]
            config_content += """    @property
    def CATEGORY_BUTTONS(self) -> dict[str, Point]:
        return {
"""
            for category, (x, y) in buttons.items():
                config_content += f'            "{category}": Point({x}, {y}),\n'
            config_content += """        }

"""

        # 注意：仓库选择位置和滚动区域使用默认配置，不需要生成

        # 保存文件
        output_path = Path(
            "src/endfield_essence_recognizer/warehouse_transfer/config/layout_1080p_generated.py"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        logger.info(f"配置文件已生成: {output_path}")
        logger.info("请检查生成的文件，确认坐标正确后使用")


def main():
    """主函数"""
    logger.info("坐标校准工具")

    # 初始化窗口管理器
    supported_titles = ["终末地", "Endfield"]
    window_manager = WindowManager(supported_titles)

    if not window_manager.target_exists:
        logger.error("未找到游戏窗口！")
        logger.error(f"请确保游戏正在运行，窗口标题为: {supported_titles}")
        sys.exit(1)

    # 创建校准器
    calibrator = CoordinateCalibrator(window_manager)

    # 运行校准
    calibrator.run()


if __name__ == "__main__":
    main()
