"""
物品识别器

基于现有的Recognizer类，专门用于识别仓库中的物品。
"""

import importlib.resources
from pathlib import Path

from endfield_essence_recognizer.core.recognition.base import (
    RecognitionProfile,
    TemplateDescriptor,
)
from endfield_essence_recognizer.core.recognition.recognizer import Recognizer
from endfield_essence_recognizer.utils.log import logger


class ItemRecognizer(Recognizer[str]):
    """
    物品识别器
    
    用于识别仓库中的物品图标或名称。
    """

    def __init__(
        self,
        item_names: list[str],
        high_threshold: float = 0.80,
        low_threshold: float = 0.60,
        templates_dir: Path | None = None,
    ):
        """
        初始化物品识别器
        
        Args:
            item_names: 要识别的物品名称列表
            high_threshold: 高置信度阈值
            low_threshold: 低置信度阈值
            templates_dir: 模板图像目录，如果为None则使用默认目录
        """
        # 确定模板目录
        if templates_dir is None:
            templates_dir = (
                importlib.resources.files("endfield_essence_recognizer")
                / "warehouse_transfer/templates/items"
            )

        # 构建模板描述符列表
        templates: list[TemplateDescriptor[str]] = []
        for item_name in item_names:
            template_path = templates_dir / f"{item_name}.png"
            templates.append(TemplateDescriptor(path=template_path, label=item_name))

        # 创建识别配置
        profile = RecognitionProfile(
            templates=templates,
            high_threshold=high_threshold,
            low_threshold=low_threshold,
        )

        # 初始化父类
        super().__init__(profile)

        logger.info(f"物品识别器已初始化，加载了 {len(item_names)} 个物品模板")

    @classmethod
    def from_config(
        cls, item_names: list[str], recognition_config
    ) -> "ItemRecognizer":
        """
        从配置对象创建物品识别器
        
        Args:
            item_names: 要识别的物品名称列表
            recognition_config: RecognitionConfig对象
        
        Returns:
            ItemRecognizer实例
        """
        return cls(
            item_names=item_names,
            high_threshold=recognition_config.item_high_threshold,
            low_threshold=recognition_config.item_low_threshold,
        )


def build_item_recognizer_from_transfer_config(transfer_config) -> ItemRecognizer:
    """
    从TransferConfig构建物品识别器
    
    Args:
        transfer_config: TransferConfig对象
    
    Returns:
        ItemRecognizer实例
    """
    # 提取所有要转移的物品名称
    item_names = [item.name for item in transfer_config.transfer_items]

    # 创建识别器
    recognizer = ItemRecognizer.from_config(
        item_names=item_names, recognition_config=transfer_config.recognition
    )

    # 加载模板
    recognizer.load_templates()

    return recognizer
