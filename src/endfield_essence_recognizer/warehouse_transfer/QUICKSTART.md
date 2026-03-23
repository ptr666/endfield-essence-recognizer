# 快速开始指南

## 5分钟快速上手

### 前置条件

1. 游戏分辨率设置为 **1920×1080**
2. 游戏语言设置为 **简体中文**
3. 已安装项目依赖：
   ```bash
   # 安装所有依赖（包括仓库转移模块所需的依赖）
   uv sync --all-groups
   ```

### 步骤1：准备模板图像（5分钟）

#### 1.1 启动游戏并进入仓库界面

打开游戏，进入仓库界面。

#### 1.2 截取物品图标

使用Windows自带的截图工具（Win + Shift + S）：

1. 找到"蓝铁矿"物品
2. 截取物品图标或名称区域（建议60×60像素）
3. 保存为 `src/endfield_essence_recognizer/warehouse_transfer/templates/items/蓝铁矿.png`

**截图技巧**：
- 只截取物品图标或名称文字部分
- 确保截图清晰，没有模糊
- 背景尽量干净

#### 1.3 截取UI按钮（可选）

如果需要场景检测，可以截取以下按钮：
- 自动存放按钮 → `templates/ui/自动存放按钮.png`
- 仓库切换按钮 → `templates/ui/仓库切换按钮.png`

### 步骤2：校准坐标（10分钟）

运行坐标校准工具：

```bash
uv run python -m endfield_essence_recognizer.warehouse_transfer.examples.calibrate_coordinates
```

按照提示依次点击标记：
1. 仓库网格（8列×4行，共32个点）
2. 自动存放按钮
3. 仓库切换按钮
4. 确认按钮
5. 关闭按钮
6. 8个物品分类按钮

**标记技巧**：
- 点击每个格子的中心点
- 如果不确定，可以按 's' 跳过
- 标记完成后会生成配置文件
- 仓库选择位置和滚动区域使用默认配置，无需标记

### 步骤3：配置转移任务（2分钟）

编辑 `config/transfer_config.py`：

```python
from endfield_essence_recognizer.warehouse_transfer.config.transfer_config import (
    TransferConfig,
    TransferItem,
)

# 创建你的配置
my_config = TransferConfig(
    source_warehouse="仓库1",      # 源仓库名称
    target_warehouse="仓库2",      # 目标仓库名称
    transfer_items=[
        TransferItem(
            name="蓝铁矿",         # 物品名称（必须与模板文件名匹配）
            category="矿物",       # 物品分类
            count=-1,             # -1表示全部转移
        )
    ],
    max_loops=-1,                 # -1表示无限循环
)
```

### 步骤4：运行转移任务（1分钟）

```bash
uv run python -m endfield_essence_recognizer.warehouse_transfer.examples.run_transfer
```

程序会：
1. 检查游戏窗口
2. 加载配置和模板
3. 倒计时3秒后开始转移
4. 按 Ctrl+C 可以随时停止

## 常见问题

### Q1: 提示"未找到游戏窗口"

**解决方法**：
1. 确保游戏正在运行
2. 检查游戏窗口标题是否为"终末地"或"Endfield"
3. 如果不是，修改 `run_transfer.py` 中的 `supported_titles`

### Q2: 提示"无法加载模板图像"

**解决方法**：
1. 检查模板文件是否存在
2. 检查文件名是否与配置中的物品名称完全匹配
3. 检查文件格式是否为PNG

### Q3: 识别不到物品

**解决方法**：
1. 重新截取更清晰的模板图像
2. 降低识别阈值（修改 `recognition.item_low_threshold`）
3. 检查游戏界面是否与截图时一致

### Q4: 点击位置不准确

**解决方法**：
1. 重新运行坐标校准工具
2. 确保游戏分辨率为1920×1080
3. 确保游戏窗口没有被缩放

### Q5: 程序卡住不动

**解决方法**：
1. 检查游戏是否弹出对话框
2. 检查是否在正确的界面（仓库界面）
3. 按 Ctrl+C 停止程序

## 进阶使用

### 转移多个物品

```python
transfer_items=[
    TransferItem(name="蓝铁矿", category="矿物", count=-1),
    TransferItem(name="红铜矿", category="矿物", count=-1),
    TransferItem(name="基础材料", category="材料", count=50),
]
```

### 限制循环次数

```python
max_loops=10,  # 执行10次后自动停止
```

### 调整延迟时间

```python
from endfield_essence_recognizer.warehouse_transfer.config.transfer_config import DelayConfig

delays=DelayConfig(
    after_click=0.2,      # 点击后等待0.2秒
    after_store=0.3,      # 存放后等待0.3秒
    loop_interval=0.5,    # 循环间隔0.5秒
)
```

### 调整识别阈值

```python
from endfield_essence_recognizer.warehouse_transfer.config.transfer_config import RecognitionConfig

recognition=RecognitionConfig(
    item_high_threshold=0.85,  # 提高识别精度
    item_low_threshold=0.70,   # 提高最低阈值
    max_scroll_attempts=10,    # 增加滚动查找次数
)
```

## 安全提示

1. **首次使用建议**：
   - 先在测试环境运行
   - 观察几次循环确认无误
   - 再正式使用

2. **运行时注意**：
   - 不要移动或调整游戏窗口
   - 不要切换到其他窗口
   - 随时准备按 Ctrl+C 停止

3. **数据安全**：
   - 建议先备份重要物品
   - 不要转移已锁定的物品
   - 确认目标仓库有足够空间

## 获取帮助

如果遇到问题：
1. 查看日志输出，了解具体错误
2. 阅读完整的 README.md 文档
3. 在项目仓库提交 Issue

## 下一步

- 阅读完整的 [README.md](README.md) 了解详细功能
- 查看 [代码示例](examples/) 学习高级用法
- 自定义配置以适应你的需求
