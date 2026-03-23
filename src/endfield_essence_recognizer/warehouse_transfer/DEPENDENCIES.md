# 依赖说明

## Python 依赖

本模块的所有依赖都已包含在项目的 `pyproject.toml` 中，无需单独安装。

### 新增依赖

为支持仓库转移功能，项目添加了以下依赖：

- **pynput >= 1.7.7** - 用于键盘控制（Ctrl键模拟）

### 复用的现有依赖

以下依赖项目已有，仓库转移模块直接复用：

- **pyautogui >= 0.9.54** - 鼠标控制和自动化
- **opencv-python >= 4.12.0.88** - 图像处理和模板匹配
- **numpy** - 数值计算（opencv-python的依赖）
- **pygetwindow >= 0.0.9** - 窗口管理
- **pywin32 >= 311** - Windows API调用

## 安装方法

### 使用 uv（推荐）

```bash
# 安装所有依赖
uv sync --all-groups
```

### 使用 pip

```bash
# 安装项目
pip install -e .

# 或者手动安装依赖
pip install pynput>=1.7.7 pyautogui>=0.9.54 opencv-python>=4.12.0.88 pygetwindow>=0.0.9 pywin32>=311
```

## 验证安装

运行以下命令验证依赖是否正确安装：

```bash
uv run python -c "import pynput; import pyautogui; import cv2; import numpy; print('所有依赖已正确安装！')"
```

## 依赖说明

### pynput

**用途**: 键盘控制

**使用场景**:
- 模拟 Ctrl 键按下和释放
- 实现 Ctrl+右键点击功能

**为什么需要**:
- `pyautogui` 的键盘控制在某些情况下不够精确
- `pynput` 提供更底层的键盘控制能力
- 可以精确控制按键的按下和释放时机

### pyautogui

**用途**: 鼠标控制和自动化

**使用场景**:
- 鼠标移动和点击
- 鼠标滚轮滚动
- 屏幕坐标转换

**为什么需要**:
- 提供跨平台的鼠标控制能力
- 简单易用的API
- 与 pynput 配合使用效果更好

### opencv-python

**用途**: 图像处理和识别

**使用场景**:
- 截图处理
- 模板匹配识别
- 图像预处理

**为什么需要**:
- 强大的图像处理能力
- 高效的模板匹配算法
- 项目已有，直接复用

### pygetwindow

**用途**: 窗口管理

**使用场景**:
- 查找游戏窗口
- 获取窗口位置和大小
- 激活窗口

**为什么需要**:
- 跨平台的窗口管理能力
- 简单的API
- 项目已有，直接复用

### pywin32

**用途**: Windows API调用

**使用场景**:
- 获取窗口句柄
- 截取窗口客户区
- 坐标转换

**为什么需要**:
- 提供底层的Windows API访问
- 高性能的窗口操作
- 项目已有，直接复用

## 平台支持

本模块目前仅支持 **Windows** 平台，因为：

1. 使用了 `pywin32` 进行Windows特定的窗口操作
2. 游戏本身只在Windows平台运行
3. 某些输入控制功能依赖Windows API

如需支持其他平台，需要：
- 替换 `pywin32` 相关的窗口操作代码
- 适配不同平台的输入控制方式
- 测试在不同平台上的兼容性

## 版本要求

- **Python**: >= 3.12
- **操作系统**: Windows 10/11
- **游戏分辨率**: 1920×1080

## 常见问题

### Q: 为什么需要 pynput 和 pyautogui 两个库？

A: 两个库各有优势：
- `pynput` 提供更精确的键盘控制，适合模拟组合键
- `pyautogui` 提供更简单的鼠标控制，适合点击和滚动
- 两者配合使用可以实现更可靠的自动化操作

### Q: 可以只用 pyautogui 吗？

A: 理论上可以，但实际测试发现：
- `pyautogui` 的键盘控制在某些情况下不够稳定
- `pynput` 的键盘控制更底层，更可靠
- 建议保持当前的组合使用方式

### Q: 依赖包很大吗？

A: 主要依赖包大小：
- `pynput`: ~100KB（新增）
- `pyautogui`: ~50KB（已有）
- `opencv-python`: ~90MB（已有）
- `numpy`: ~20MB（已有）

新增的 `pynput` 非常小，不会显著增加项目大小。

### Q: 安装失败怎么办？

A: 常见解决方法：
1. 确保使用 Python 3.12+
2. 更新 pip: `python -m pip install --upgrade pip`
3. 使用国内镜像: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pynput`
4. 检查网络连接
5. 查看详细错误信息

## 更新日志

### v1.0.0 (2026-02-10)
- ✅ 添加 `pynput>=1.7.7` 依赖
- ✅ 复用现有的 `pyautogui`, `opencv-python` 等依赖
- ✅ 所有依赖已添加到 `pyproject.toml`

## 相关文档

- [安装指南](INSTALLATION.md)
- [快速开始](QUICKSTART.md)
- [完整文档](README.md)
