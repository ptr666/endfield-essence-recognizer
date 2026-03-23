"""
仓库转移任务配置

本文件定义转移任务的配置参数，包括：
- 源仓库和目标仓库
- 要转移的物品列表
- 延迟时间配置
- 识别阈值配置
"""

from dataclasses import dataclass, field


@dataclass
class TransferItem:
    """要转移的物品配置"""

    name: str
    """物品名称，必须与模板文件名匹配"""

    category: str
    """物品分类，如"矿物"、"材料"等"""

    count: int = -1
    """
    要转移的数量
    -1 表示全部转移
    正整数表示转移指定数量
    """

    template_path: str | None = None
    """
    自定义模板路径（可选）
    如果不指定，会使用默认路径: templates/items/{name}.png
    """


@dataclass
class DelayConfig:
    """延迟时间配置（单位：秒）"""

    after_click: float = 0.3
    """点击后的等待时间"""

    after_store: float = 0.5
    """自动存放后的等待时间"""

    after_switch: float = 0.5
    """切换仓库后的等待时间"""

    after_category_select: float = 0.3
    """选择分类后的等待时间"""

    after_scroll: float = 0.2
    """滚动后的等待时间"""

    loop_interval: float = 1.0
    """每次循环之间的间隔时间"""

    after_ctrl_right_click: float = 0.3
    """Ctrl+右键点击后的等待时间"""


@dataclass
class RecognitionConfig:
    """识别配置"""

    item_high_threshold: float = 0.80
    """物品识别的高置信度阈值"""

    item_low_threshold: float = 0.60
    """物品识别的低置信度阈值"""

    ui_high_threshold: float = 0.85
    """UI元素识别的高置信度阈值"""

    ui_low_threshold: float = 0.70
    """UI元素识别的低置信度阈值"""

    max_scroll_attempts: int = 5
    """查找物品时的最大滚动次数"""

    scroll_clicks: int = -3
    """每次滚动的滚轮点击数（负数表示向下滚动）"""


@dataclass
class TransferConfig:
    """仓库转移任务的完整配置"""

    source_warehouse: str
    """源仓库名称，必须与layout中的WAREHOUSE_SELECT_POSITIONS键匹配"""

    target_warehouse: str
    """目标仓库名称，必须与layout中的WAREHOUSE_SELECT_POSITIONS键匹配"""

    transfer_items: list[TransferItem]
    """要转移的物品列表"""

    delays: DelayConfig = field(default_factory=DelayConfig)
    """延迟时间配置"""

    recognition: RecognitionConfig = field(default_factory=RecognitionConfig)
    """识别配置"""

    max_loops: int = -1
    """
    最大循环次数
    -1 表示无限循环，直到手动停止
    正整数表示执行指定次数后自动停止
    """

    stop_on_error: bool = False
    """
    遇到错误时是否停止
    True: 遇到错误立即停止
    False: 记录错误日志但继续执行
    """

    def validate(self) -> None:
        """验证配置的有效性"""
        if not self.source_warehouse:
            raise ValueError("源仓库名称不能为空")

        if not self.target_warehouse:
            raise ValueError("目标仓库名称不能为空")

        if self.source_warehouse == self.target_warehouse:
            raise ValueError("源仓库和目标仓库不能相同")

        if not self.transfer_items:
            raise ValueError("转移物品列表不能为空")

        for item in self.transfer_items:
            if not item.name:
                raise ValueError("物品名称不能为空")
            if not item.category:
                raise ValueError("物品分类不能为空")


# ==================== 预定义配置示例 ====================


def create_blue_iron_ore_transfer_config() -> TransferConfig:
    """
    创建蓝铁矿转移配置的示例
    
    从四号谷底转移蓝铁矿到武陵
    """
    return TransferConfig(
        source_warehouse="四号谷底",
        target_warehouse="武陵",
        transfer_items=[
            TransferItem(
                name="蓝铁矿",
                category="矿物",
                count=-1,  # 全部转移
            )
        ],
        delays=DelayConfig(
            after_click=0.3,
            after_store=0.5,
            after_switch=0.5,
            loop_interval=1.0,
        ),
        recognition=RecognitionConfig(
            item_high_threshold=0.80,
            item_low_threshold=0.60,
            max_scroll_attempts=5,
        ),
        max_loops=-1,  # 无限循环
        stop_on_error=False,
    )


def create_multi_item_transfer_config() -> TransferConfig:
    """
    创建多物品转移配置的示例
    
    从四号谷底转移多种物品到武陵
    """
    return TransferConfig(
        source_warehouse="四号谷底",
        target_warehouse="武陵",
        transfer_items=[
            TransferItem(name="蓝铁矿", category="矿物", count=-1),
            TransferItem(name="红铜矿", category="矿物", count=-1),
            TransferItem(name="基础材料", category="材料", count=50),
        ],
        max_loops=10,  # 执行10次后停止
        stop_on_error=True,  # 遇到错误立即停止
    )
