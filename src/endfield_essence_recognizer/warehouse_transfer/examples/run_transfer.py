"""
运行仓库转移任务的示例脚本

展示如何初始化和运行仓库转移扫描器。
"""

import sys
import time

from endfield_essence_recognizer.core.window import WindowManager
from endfield_essence_recognizer.utils.log import logger
from endfield_essence_recognizer.warehouse_transfer.config.layout_1080p import (
    WarehouseLayout1080p,
)
from endfield_essence_recognizer.warehouse_transfer.config.transfer_config import (
    create_blue_iron_ore_transfer_config,
)
from endfield_essence_recognizer.warehouse_transfer.core.input_controller import (
    InputController,
)
from endfield_essence_recognizer.warehouse_transfer.core.item_recognizer import (
    build_item_recognizer_from_transfer_config,
)
from endfield_essence_recognizer.warehouse_transfer.core.warehouse_scanner import (
    WarehouseTransferScanner,
)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("仓库物品转移工具")
    logger.info("=" * 60)

    # 1. 创建转移配置
    logger.info("步骤1: 加载转移配置...")
    config = create_blue_iron_ore_transfer_config()
    logger.info(f"  源仓库: {config.source_warehouse}")
    logger.info(f"  目标仓库: {config.target_warehouse}")
    logger.info(f"  转移物品: {[item.name for item in config.transfer_items]}")

    # 2. 初始化窗口管理器
    logger.info("步骤2: 初始化窗口管理器...")
    supported_titles = ["终末地", "Endfield"]  # 根据实际游戏窗口标题修改
    window_manager = WindowManager(supported_titles)

    if not window_manager.target_exists:
        logger.error("未找到游戏窗口！")
        logger.error(f"请确保游戏正在运行，窗口标题为: {supported_titles}")
        sys.exit(1)

    logger.info("  游戏窗口已找到")

    # 3. 初始化布局配置
    logger.info("步骤3: 加载布局配置...")
    layout = WarehouseLayout1080p()
    logger.info(f"  分辨率: {layout.RESOLUTION}")

    # 4. 初始化输入控制器
    logger.info("步骤4: 初始化输入控制器...")
    window = window_manager._get_window()
    if window is None:
        logger.error("无法获取窗口对象")
        sys.exit(1)
    input_controller = InputController(window)
    logger.info("  输入控制器已就绪")

    # 5. 初始化物品识别器
    logger.info("步骤5: 初始化物品识别器...")
    try:
        item_recognizer = build_item_recognizer_from_transfer_config(config)
        logger.info("  物品识别器已就绪")
    except Exception as e:
        logger.error(f"初始化物品识别器失败: {e}")
        logger.error("请确保模板图像已准备好")
        sys.exit(1)

    # 6. 创建并启动扫描器
    logger.info("步骤6: 创建仓库转移扫描器...")
    scanner = WarehouseTransferScanner(
        window_manager=window_manager,
        input_controller=input_controller,
        item_recognizer=item_recognizer,
        layout=layout,
        config=config,
    )

    logger.info("=" * 60)
    logger.info("准备启动转移任务...")
    logger.info("按 Ctrl+C 可以随时停止")
    logger.info("=" * 60)

    # 等待3秒，给用户准备时间
    for i in range(3, 0, -1):
        logger.info(f"将在 {i} 秒后开始...")
        time.sleep(1)

    # 启动扫描器
    logger.info("启动转移任务！")
    scanner.start()

    try:
        # 主线程等待，直到用户按Ctrl+C
        while scanner.is_running:
            time.sleep(1)

            # 定期输出状态
            if scanner.loop_count > 0 and scanner.loop_count % 10 == 0:
                logger.info(f"已完成 {scanner.loop_count} 次循环")

    except KeyboardInterrupt:
        logger.info("\n收到停止信号...")

    finally:
        # 停止扫描器
        scanner.stop()
        scanner.join(timeout=5)

        logger.info("=" * 60)
        logger.info(f"转移任务已停止，共完成 {scanner.loop_count} 次循环")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
