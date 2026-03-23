"""
1920×1080分辨率下的仓库界面布局配置

本文件定义了仓库界面中所有关键位置的坐标，包括：
- 仓库物品网格坐标（8列×4行）
- 功能按钮坐标
- 物品分类按钮坐标
- 仓库选择坐标
- 滚动区域

注意：这些坐标需要根据实际游戏界面进行校准！
使用 calibrate_coordinates.py 工具可以自动生成准确的坐标。
"""

from collections.abc import Sequence

import numpy as np

from endfield_essence_recognizer.core.layout.base import Point, Region


class WarehouseLayout1080p:
    """1920×1080分辨率的仓库界面布局配置"""

    @property
    def RESOLUTION(self) -> tuple[int, int]:
        """预期的游戏客户区分辨率 (宽, 高)"""
        return (1920, 1080)

    # ==================== 仓库物品网格坐标 ====================

    @property
    def warehouse_grid_x_list(self) -> Sequence[int]:
        """
        仓库物品网格的 X 坐标列表（8列）
        
        这些坐标表示每个物品格子的中心点X坐标。
        默认值是估算值，需要使用校准工具获取准确坐标。
        """
        # 假设仓库网格从X=200开始，到X=1400结束，均匀分布8列
        return np.linspace(200, 1400, 8).astype(int).tolist()

    @property
    def warehouse_grid_y_list(self) -> Sequence[int]:
        """
        仓库物品网格的 Y 坐标列表（4行，初始可见）
        
        这些坐标表示每个物品格子的中心点Y坐标。
        默认值是估算值，需要使用校准工具获取准确坐标。
        """
        # 假设仓库网格从Y=200开始，到Y=700结束，均匀分布4行
        return np.linspace(200, 700, 4).astype(int).tolist()

    @property
    def ITEM_GRID_CELL_SIZE(self) -> tuple[int, int]:
        """单个物品格子的尺寸 (宽, 高)"""
        return (80, 80)

    # ==================== 功能按钮坐标 ====================

    @property
    def AUTO_STORE_BUTTON_POS(self) -> Point:
        """
        自动存放按钮的点击坐标
        
        点击此按钮会将背包中的物品自动存放到当前仓库。
        """
        return Point(1700, 950)  # 示例坐标，需校准

    @property
    def WAREHOUSE_SWITCH_BUTTON_POS(self) -> Point:
        """
        仓库切换按钮的点击坐标
        
        点击此按钮会打开仓库切换界面。
        """
        return Point(100, 100)  # 示例坐标，需校准

    @property
    def WAREHOUSE_SELECT_BUTTON_POS(self) -> Point:
        """
        仓库选择按钮的点击坐标
        
        在仓库切换界面中，点击此按钮选择目标仓库。
        例如：从"四号谷底"切换到"武陵"时，点击"武陵"仓库的位置。
        """
        return Point(960, 400)  # 示例坐标，需校准

    @property
    def WAREHOUSE_CONFIRM_BUTTON_POS(self) -> Point:
        """
        仓库切换确认按钮的点击坐标
        
        在仓库切换界面中，选择目标仓库后点击此按钮确认。
        """
        return Point(960, 600)  # 示例坐标，需校准

    @property
    def WAREHOUSE_CLOSE_BUTTON_POS(self) -> Point:
        """
        关闭仓库切换界面按钮的点击坐标
        
        确认切换后，点击此按钮关闭切换界面。
        """
        return Point(1800, 100)  # 示例坐标，需校准

    # ==================== 物品分类按钮坐标 ====================

    @property
    def CATEGORY_BUTTONS(self) -> dict[str, Point]:
        """
        物品分类按钮的坐标字典
        
        游戏中有8种物品分类，每种分类对应一个按钮。
        点击分类按钮会筛选显示该分类的物品。
        
        Returns:
            字典，键为分类名称，值为按钮坐标
        """
        # 示例坐标，需要根据实际游戏界面校准
        # 假设分类按钮横向排列在顶部
        base_y = 150
        spacing = 120
        base_x = 200

        return {
            "全部": Point(base_x + spacing * 0, base_y),
            "矿物": Point(base_x + spacing * 1, base_y),
            "材料": Point(base_x + spacing * 2, base_y),
            "消耗品": Point(base_x + spacing * 3, base_y),
            "装备": Point(base_x + spacing * 4, base_y),
            "武器": Point(base_x + spacing * 5, base_y),
            "道具": Point(base_x + spacing * 6, base_y),
            "其他": Point(base_x + spacing * 7, base_y),
        }

    # ==================== 仓库选择坐标 ====================

    @property
    def WAREHOUSE_SELECT_POSITIONS(self) -> dict[str, Point]:
        """
        不同仓库的选择坐标
        
        在仓库切换界面中，点击对应坐标选择目标仓库。
        
        注意：这些是默认坐标，如果实际游戏界面不同，需要手动调整。
        实际游戏中的仓库名称：四号谷底、武陵等。
        
        Returns:
            字典，键为仓库名称，值为选择坐标
        """
        # 示例坐标，需要根据实际游戏界面校准
        # 假设仓库选项纵向排列在切换界面中央
        base_x = 960
        base_y = 300
        spacing = 80

        return {
            "四号谷底": Point(base_x, base_y + spacing * 0),
            "武陵": Point(base_x, base_y + spacing * 1),
            "仓库3": Point(base_x, base_y + spacing * 2),
            "仓库4": Point(base_x, base_y + spacing * 3),
            "仓库5": Point(base_x, base_y + spacing * 4),
        }

    # ==================== 滚动区域 ====================

    @property
    def SCROLL_AREA(self) -> Region:
        """
        仓库物品列表的滚动区域
        
        在此区域内滚动鼠标滚轮可以查看更多物品。
        
        注意：这是默认滚动区域，如果实际游戏界面不同，需要手动调整。
        """
        return Region(Point(200, 200), Point(1400, 800))

    @property
    def SCROLL_CENTER(self) -> Point:
        """滚动区域的中心点，用于执行滚动操作"""
        scroll_area = self.SCROLL_AREA
        center_x = (scroll_area.x0 + scroll_area.x1) // 2
        center_y = (scroll_area.y0 + scroll_area.y1) // 2
        return Point(center_x, center_y)

    # ==================== 场景检测ROI ====================

    @property
    def WAREHOUSE_UI_ROI(self) -> Region:
        """
        用于判定是否在仓库界面的 ROI 区域
        
        截取此区域并与模板匹配，可以判断当前是否在仓库界面。
        """
        return Region(Point(50, 50), Point(200, 120))

    # ==================== 物品识别ROI ====================

    def get_item_roi(self, col: int, row: int) -> Region:
        """
        获取指定网格位置的物品识别ROI区域
        
        Args:
            col: 列索引 (0-7)
            row: 行索引 (0-3)
        
        Returns:
            物品图标的ROI区域
        """
        if not (0 <= col < 8):
            raise ValueError(f"列索引必须在0-7之间，当前值: {col}")
        if not (0 <= row < 4):
            raise ValueError(f"行索引必须在0-3之间，当前值: {row}")

        center_x = self.warehouse_grid_x_list[col]
        center_y = self.warehouse_grid_y_list[row]

        cell_width, cell_height = self.ITEM_GRID_CELL_SIZE
        half_width = cell_width // 2
        half_height = cell_height // 2

        return Region(
            Point(center_x - half_width, center_y - half_height),
            Point(center_x + half_width, center_y + half_height),
        )

    def get_item_name_roi(self, col: int, row: int) -> Region:
        """
        获取指定网格位置的物品名称识别ROI区域
        
        物品名称通常显示在图标下方。
        
        Args:
            col: 列索引 (0-7)
            row: 行索引 (0-3)
        
        Returns:
            物品名称的ROI区域
        """
        center_x = self.warehouse_grid_x_list[col]
        center_y = self.warehouse_grid_y_list[row]

        # 名称区域在图标下方
        name_width = 100
        name_height = 30
        name_offset_y = 50  # 图标下方偏移

        return Region(
            Point(center_x - name_width // 2, center_y + name_offset_y),
            Point(center_x + name_width // 2, center_y + name_offset_y + name_height),
        )
