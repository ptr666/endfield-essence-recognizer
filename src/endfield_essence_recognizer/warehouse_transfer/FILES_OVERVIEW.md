# 文件总览

本文档详细说明仓库转移模块中每个文件的作用和相互关系。

## 目录结构

```
warehouse_transfer/
├── README.md                          # 完整配置指导文档
├── QUICKSTART.md                      # 5分钟快速开始指南
├── FILES_OVERVIEW.md                  # 本文件 - 文件总览
├── __init__.py                        # 模块初始化
│
├── config/                            # 配置模块
│   ├── __init__.py                   # 配置模块初始化
│   ├── layout_1080p.py               # 1080p布局配置
│   └── transfer_config.py            # 转移任务配置
│
├── core/                              # 核心功能模块
│   ├── __init__.py                   # 核心模块初始化
│   ├── input_controller.py           # 输入控制器
│   ├── item_recognizer.py            # 物品识别器
│   └── warehouse_scanner.py          # 仓库扫描器
│
├── templates/                         # 模板资源
│   ├── items/                        # 物品图标模板
│   │   └── .gitkeep
│   ├── ui/                           # UI元素模板
│   │   └── .gitkeep
│   └── categories/                   # 分类标签模板
│       └── .gitkeep
│
└── examples/                          # 示例脚本
    ├── __init__.py
    ├── run_transfer.py               # 运行转移任务
    └── calibrate_coordinates.py      # 坐标校准工具
```

## 核心文件详解

### 1. 配置文件

#### `config/layout_1080p.py`
**作用**: 定义1920×1080分辨率下仓库界面的所有坐标位置

**包含内容**:
- `WarehouseLayout1080p` 类
  - `warehouse_grid_x_list`: 仓库网格8列的X坐标
  - `warehouse_grid_y_list`: 仓库网格4行的Y坐标
  - `AUTO_STORE_BUTTON_POS`: 自动存放按钮坐标
  - `WAREHOUSE_SWITCH_BUTTON_POS`: 仓库切换按钮坐标
  - `WAREHOUSE_CONFIRM_BUTTON_POS`: 确认按钮坐标
  - `WAREHOUSE_CLOSE_BUTTON_POS`: 关闭按钮坐标
  - `CATEGORY_BUTTONS`: 8种物品分类按钮坐标字典
  - `WAREHOUSE_SELECT_POSITIONS`: 仓库选择坐标字典
  - `SCROLL_AREA`: 滚动区域定义
  - `get_item_roi()`: 获取指定网格位置的ROI区域
  - `get_item_name_roi()`: 获取物品名称的ROI区域

**使用场景**:
- 初始化时加载布局配置
- 扫描器根据坐标执行点击操作
- 识别器根据ROI区域截取图像

**依赖关系**:
- 依赖: `core.layout.base` (Point, Region)
- 被依赖: `warehouse_scanner.py`, `run_transfer.py`

---

#### `config/transfer_config.py`
**作用**: 定义转移任务的配置参数

**包含内容**:
- `TransferItem`: 单个物品的转移配置
  - `name`: 物品名称
  - `category`: 物品分类
  - `count`: 转移数量（-1表示全部）
  - `template_path`: 自定义模板路径（可选）

- `DelayConfig`: 延迟时间配置
  - `after_click`: 点击后等待时间
  - `after_store`: 存放后等待时间
  - `after_switch`: 切换仓库后等待时间
  - `after_category_select`: 选择分类后等待时间
  - `after_scroll`: 滚动后等待时间
  - `loop_interval`: 循环间隔时间
  - `after_ctrl_right_click`: Ctrl+右键后等待时间

- `RecognitionConfig`: 识别配置
  - `item_high_threshold`: 物品识别高阈值
  - `item_low_threshold`: 物品识别低阈值
  - `ui_high_threshold`: UI识别高阈值
  - `ui_low_threshold`: UI识别低阈值
  - `max_scroll_attempts`: 最大滚动次数
  - `scroll_clicks`: 每次滚动的点击数

- `TransferConfig`: 完整的转移任务配置
  - `source_warehouse`: 源仓库名称
  - `target_warehouse`: 目标仓库名称
  - `transfer_items`: 要转移的物品列表
  - `delays`: 延迟配置
  - `recognition`: 识别配置
  - `max_loops`: 最大循环次数
  - `stop_on_error`: 遇到错误是否停止

- 预定义配置函数:
  - `create_blue_iron_ore_transfer_config()`: 蓝铁矿转移配置示例
  - `create_multi_item_transfer_config()`: 多物品转移配置示例

**使用场景**:
- 用户创建自定义转移任务
- 扫描器读取配置执行任务
- 识别器根据配置调整阈值

**依赖关系**:
- 依赖: 无
- 被依赖: `warehouse_scanner.py`, `item_recognizer.py`, `run_transfer.py`

---

### 2. 核心功能模块

#### `core/input_controller.py`
**作用**: 提供扩展的输入控制功能

**包含内容**:
- `InputController` 类
  - `ctrl_right_click()`: Ctrl+右键点击
  - `scroll()`: 鼠标滚轮滚动
  - `press_key()`: 按键模拟
  - `hold_key()`: 按住按键
  - `release_key()`: 释放按键
  - `type_text()`: 输入文本
  - `double_click()`: 双击
  - `drag()`: 拖拽操作

**实现原理**:
- 使用 `pyautogui` 模拟鼠标操作
- 使用 `pynput.keyboard` 模拟键盘操作
- 通过 `_get_client_rect()` 获取窗口客户区坐标
- 将相对坐标转换为屏幕坐标后执行操作

**使用场景**:
- 扫描器执行Ctrl+右键转移物品
- 扫描器滚动查找物品
- 未来可能的键盘快捷键操作

**依赖关系**:
- 依赖: `pyautogui`, `pynput`, `core.window.windows_utils`
- 被依赖: `warehouse_scanner.py`

---

#### `core/item_recognizer.py`
**作用**: 识别仓库中的物品

**包含内容**:
- `ItemRecognizer` 类（继承自 `Recognizer[str]`）
  - `__init__()`: 初始化识别器，加载物品模板
  - `from_config()`: 从配置对象创建识别器

- `build_item_recognizer_from_transfer_config()`: 从TransferConfig构建识别器

**实现原理**:
- 基于现有的 `Recognizer` 类
- 使用模板匹配算法（OpenCV的matchTemplate）
- 为每个物品加载对应的模板图像
- 返回识别结果和置信度分数

**使用场景**:
- 扫描器在仓库网格中查找目标物品
- 识别物品图标或名称

**依赖关系**:
- 依赖: `core.recognition.Recognizer`, `core.recognition.base`
- 被依赖: `warehouse_scanner.py`, `run_transfer.py`

---

#### `core/warehouse_scanner.py`
**作用**: 实现完整的仓库转移流程

**包含内容**:
- `WarehouseTransferScanner` 类（继承自 `threading.Thread`）
  - `run()`: 主循环，执行转移任务
  - `_execute_transfer_cycle()`: 执行一次完整的转移循环
  - `_auto_store_backpack()`: 自动存放背包
  - `_select_category()`: 选择物品分类
  - `_find_item()`: 查找物品（支持滚动）
  - `_scroll_down()`: 向下滚动
  - `_ctrl_right_click_item()`: Ctrl+右键点击物品
  - `_switch_warehouse()`: 切换仓库
  - `stop()`: 停止扫描器
  - `is_running`: 检查是否正在运行
  - `loop_count`: 获取循环次数

**执行流程**:
```
1. 自动存放背包（源仓库）
2. 选择物品分类
3. 查找目标物品
   ├─ 遍历网格
   ├─ 截取ROI
   ├─ 识别物品
   └─ 如果未找到，滚动继续查找
4. Ctrl+右键点击物品
5. 切换到目标仓库
6. 自动存放背包（目标仓库）
7. 切换回源仓库
8. 重复循环
```

**使用场景**:
- 主程序创建并启动扫描器
- 后台线程自动执行转移任务
- 用户可以随时停止

**依赖关系**:
- 依赖: `WindowManager`, `InputController`, `ItemRecognizer`, `WarehouseLayout1080p`, `TransferConfig`
- 被依赖: `run_transfer.py`

---

### 3. 示例脚本

#### `examples/run_transfer.py`
**作用**: 运行转移任务的示例脚本

**执行流程**:
```
1. 加载转移配置
2. 初始化窗口管理器
3. 检查游戏窗口是否存在
4. 加载布局配置
5. 初始化输入控制器
6. 初始化物品识别器
7. 创建仓库转移扫描器
8. 倒计时3秒
9. 启动扫描器
10. 等待用户按Ctrl+C停止
11. 停止扫描器并输出统计
```

**使用方法**:
```bash
uv run python -m endfield_essence_recognizer.warehouse_transfer.examples.run_transfer
```

**依赖关系**:
- 依赖: 所有核心模块和配置模块
- 被依赖: 无（入口脚本）

---

#### `examples/calibrate_coordinates.py`
**作用**: 坐标校准工具

**包含内容**:
- `CoordinateCalibrator` 类
  - `capture_screenshot()`: 捕获游戏窗口截图
  - `mouse_callback()`: 鼠标点击回调
  - `mark_point()`: 标记单个点
  - `mark_grid()`: 标记网格
  - `run()`: 运行校准流程
  - `generate_config_file()`: 生成配置文件

**执行流程**:
```
1. 捕获游戏窗口截图
2. 显示截图窗口
3. 用户依次点击标记各个位置:
   ├─ 仓库网格（8列×4行）
   ├─ 功能按钮（4个）
   └─ 分类按钮（8个）
4. 生成配置文件
5. 保存为 layout_1080p_generated.py
```

**注意**：仓库选择位置和滚动区域使用默认配置，无需标记。

**使用方法**:
```bash
uv run python -m endfield_essence_recognizer.warehouse_transfer.examples.calibrate_coordinates
```

**依赖关系**:
- 依赖: `WindowManager`, `cv2`, `numpy`
- 被依赖: 无（工具脚本）

---

### 4. 模板资源

#### `templates/items/`
**作用**: 存放物品图标或名称的截图模板

**文件格式**: `{物品名称}.png`

**示例**:
- `蓝铁矿.png`
- `红铜矿.png`
- `基础材料.png`

**使用场景**:
- `ItemRecognizer` 加载模板进行识别
- 扫描器查找物品时使用

---

#### `templates/ui/`
**作用**: 存放UI按钮的截图模板

**文件格式**: `{按钮名称}.png`

**示例**:
- `自动存放按钮.png`
- `仓库切换按钮.png`
- `确认按钮.png`

**使用场景**:
- 场景检测（可选）
- 验证当前界面是否正确

---

#### `templates/categories/`
**作用**: 存放物品分类标签的截图模板

**文件格式**: `{分类名称}.png`

**示例**:
- `矿物.png`
- `材料.png`
- `消耗品.png`

**使用场景**:
- 验证分类选择是否成功（可选）

---

## 数据流图

```
┌─────────────────┐
│  用户配置文件    │
│ transfer_config │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│   主程序入口     │────>│ WindowManager│
│ run_transfer.py │     └──────────────┘
└────────┬────────┘              │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────┐
│  布局配置       │     │InputController│
│ layout_1080p.py │     └──────────────┘
└────────┬────────┘              │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────┐
│  物品识别器     │     │TemplateImages│
│item_recognizer  │<────│ (templates/) │
└────────┬────────┘     └──────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      仓库转移扫描器              │
│   warehouse_scanner.py          │
│                                 │
│  1. 自动存放背包                 │
│  2. 选择分类                     │
│  3. 查找物品 ──> 识别器          │
│  4. Ctrl+右键 ──> 输入控制器     │
│  5. 切换仓库 ──> 窗口管理器      │
│  6. 自动存放背包                 │
│  7. 切换回源仓库                 │
│  8. 循环                        │
└─────────────────────────────────┘
```

## 模块依赖关系

```
run_transfer.py
    ├── WindowManager (复用原有)
    ├── InputController (新增)
    ├── ItemRecognizer (新增)
    ├── WarehouseLayout1080p (新增)
    ├── TransferConfig (新增)
    └── WarehouseTransferScanner (新增)
            ├── WindowManager
            ├── InputController
            ├── ItemRecognizer
            ├── WarehouseLayout1080p
            └── TransferConfig

calibrate_coordinates.py
    ├── WindowManager (复用原有)
    ├── cv2
    └── numpy
```

## 扩展点

### 1. 添加新物品
- 截取新物品模板 → `templates/items/{物品名称}.png`
- 在配置中添加 `TransferItem`

### 2. 支持新分辨率
- 创建新的布局配置类 `WarehouseLayout{分辨率}.py`
- 使用校准工具生成坐标

### 3. 自定义转移逻辑
- 继承 `WarehouseTransferScanner`
- 重写 `_execute_transfer_cycle()` 方法

### 4. 添加场景检测
- 截取UI模板 → `templates/ui/`
- 在扫描器中添加场景验证逻辑

### 5. 添加统计功能
- 在扫描器中记录转移数量
- 在停止时输出统计报告

## 总结

本模块采用清晰的分层架构：

1. **配置层**: 定义坐标和任务参数
2. **核心层**: 实现输入控制、识别、扫描逻辑
3. **资源层**: 存放模板图像
4. **应用层**: 提供示例脚本和工具

所有代码都是独立的，不修改原有项目代码，可以安全地添加到现有项目中。
