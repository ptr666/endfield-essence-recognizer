# 安装和部署指南

## 文件清单

本模块包含以下文件（所有文件都已创建）：

### 📄 文档文件
- ✅ `README.md` - 完整配置指导文档
- ✅ `QUICKSTART.md` - 5分钟快速开始指南
- ✅ `FILES_OVERVIEW.md` - 文件总览和详细说明
- ✅ `INSTALLATION.md` - 本文件

### 🔧 配置模块 (`config/`)
- ✅ `__init__.py` - 配置模块初始化
- ✅ `layout_1080p.py` - 1080p分辨率布局配置
- ✅ `transfer_config.py` - 转移任务配置

### ⚙️ 核心功能模块 (`core/`)
- ✅ `__init__.py` - 核心模块初始化
- ✅ `input_controller.py` - 扩展输入控制器
- ✅ `item_recognizer.py` - 物品识别器
- ✅ `warehouse_scanner.py` - 仓库转移扫描器

### 🖼️ 模板资源 (`templates/`)
- ✅ `items/.gitkeep` - 物品图标模板目录
- ✅ `ui/.gitkeep` - UI元素模板目录
- ✅ `categories/.gitkeep` - 分类标签模板目录

### 📝 示例脚本 (`examples/`)
- ✅ `__init__.py` - 示例模块初始化
- ✅ `run_transfer.py` - 运行转移任务
- ✅ `calibrate_coordinates.py` - 坐标校准工具

### 📦 模块初始化
- ✅ `__init__.py` - 主模块初始化

## 安装步骤

### 1. 验证文件结构

确认所有文件都已创建：

```bash
cd src/endfield_essence_recognizer/warehouse_transfer
ls -R
```

应该看到以下目录结构：

```
warehouse_transfer/
├── README.md
├── QUICKSTART.md
├── FILES_OVERVIEW.md
├── INSTALLATION.md
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── layout_1080p.py
│   └── transfer_config.py
├── core/
│   ├── __init__.py
│   ├── input_controller.py
│   ├── item_recognizer.py
│   └── warehouse_scanner.py
├── templates/
│   ├── items/
│   │   └── .gitkeep
│   ├── ui/
│   │   └── .gitkeep
│   └── categories/
│       └── .gitkeep
└── examples/
    ├── __init__.py
    ├── run_transfer.py
    └── calibrate_coordinates.py
```

### 2. 安装项目依赖

本模块的依赖已经包含在项目的 `pyproject.toml` 中，只需安装项目依赖即可：

```bash
# 使用 uv 安装所有依赖
uv sync --all-groups
```

本模块使用的额外依赖：
- `pynput>=1.7.7` - 键盘控制（已添加到项目依赖）
- `pyautogui>=0.9.54` - 鼠标控制（项目已有）
- `opencv-python>=4.12.0.88` - 图像处理（项目已有）
- `numpy` - 数值计算（opencv-python的依赖）

### 3. 验证导入

测试模块是否可以正常导入：

```python
# 在Python中测试
from endfield_essence_recognizer.warehouse_transfer import (
    WarehouseTransferScanner,
    WarehouseLayout1080p,
    TransferConfig,
)

print("模块导入成功！")
```

或者运行：

```bash
uv run python -c "from endfield_essence_recognizer.warehouse_transfer import WarehouseTransferScanner; print('OK')"
```

### 4. 准备模板图像

创建模板图像目录并添加第一个模板：

```bash
# 确保模板目录存在
mkdir -p src/endfield_essence_recognizer/warehouse_transfer/templates/items
mkdir -p src/endfield_essence_recognizer/warehouse_transfer/templates/ui
mkdir -p src/endfield_essence_recognizer/warehouse_transfer/templates/categories
```

然后按照 QUICKSTART.md 中的说明截取模板图像。

### 5. 运行校准工具

```bash
uv run python -m endfield_essence_recognizer.warehouse_transfer.examples.calibrate_coordinates
```

### 6. 测试运行

```bash
uv run python -m endfield_essence_recognizer.warehouse_transfer.examples.run_transfer
```

## 依赖关系

### 复用的现有模块（只读，不修改）

- ✅ `core.window.WindowManager` - 窗口管理
- ✅ `core.window.windows_utils` - Windows API工具
- ✅ `core.recognition.Recognizer` - 图像识别引擎
- ✅ `core.recognition.base` - 识别配置基类
- ✅ `core.layout.base` - 布局定义基类
- ✅ `utils.image` - 图像处理工具
- ✅ `utils.log` - 日志工具

### 新增的外部依赖

- `pynput>=1.7.7` - 键盘控制（已添加到项目依赖）
- `pyautogui>=0.9.54` - 鼠标控制（项目已有）
- `opencv-python>=4.12.0.88` - 图像处理（项目已有）
- `numpy` - 数值计算（opencv-python的依赖）

所有依赖都已包含在项目的 `pyproject.toml` 中，运行 `uv sync` 即可安装。

## 卸载

如果需要移除本模块：

```bash
# 删除整个目录
rm -rf src/endfield_essence_recognizer/warehouse_transfer
```

注意：`pynput` 依赖已添加到项目依赖中，如果其他功能也需要使用，请不要从 `pyproject.toml` 中移除。

## 故障排查

### 问题1: 导入失败

```python
ModuleNotFoundError: No module named 'endfield_essence_recognizer.warehouse_transfer'
```

**解决方法**:
1. 确认所有 `__init__.py` 文件都已创建
2. 确认在项目根目录运行
3. 重新安装项目：`uv sync`

### 问题2: 缺少依赖

```python
ModuleNotFoundError: No module named 'pynput'
```

**解决方法**:
```bash
# 重新安装项目依赖
uv sync --all-groups
```

### 问题3: 模板加载失败

```python
FileNotFoundError: [Errno 2] No such file or directory: '.../templates/items/蓝铁矿.png'
```

**解决方法**:
1. 确认模板文件已创建
2. 确认文件名与配置中的物品名称完全匹配
3. 确认文件格式为PNG

### 问题4: 权限错误

```python
PermissionError: [Errno 13] Permission denied
```

**解决方法**:
1. 使用管理员权限运行（Windows）
2. 检查文件权限（Linux/Mac）

## 更新日志

### v1.0.0 (初始版本)
- ✅ 创建完整的模块结构
- ✅ 实现核心转移功能
- ✅ 提供坐标校准工具
- ✅ 编写完整文档

## 下一步

1. 阅读 [QUICKSTART.md](QUICKSTART.md) 快速上手
2. 阅读 [README.md](README.md) 了解详细功能
3. 阅读 [FILES_OVERVIEW.md](FILES_OVERVIEW.md) 了解代码结构
4. 开始使用！

## 获取帮助

如果遇到问题：
1. 查看本文档的故障排查部分
2. 查看日志输出了解具体错误
3. 在项目仓库提交 Issue

## 许可证

本模块遵循与主项目相同的许可证。
