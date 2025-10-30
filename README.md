# 📄 PaddleOCR 文档识别系统

基于 Streamlit 的 PaddleOCR 网页应用，支持 PP-OCRv5 和 PP-StructureV3 双模式识别，以及三种上传模式。

## ✨ 功能特点

### 🎯 双模型识别系统

1. **PaddleOCR 标准模式** - 快速文字识别
   - ⚡ 识别速度最快，适合批量处理
   - ✅ 高精度文字识别，准确率 >95%
   - 📄 纯文本格式输出，便于后续处理

2. **PP-StructureV3 模式** - 高级文档解析
   - ✅ 智能版面分析，自动识别文档结构
   - ✅ 多类型内容处理：文本、表格、图像、公式
   - 📝 Markdown 格式输出，保持原始排版结构

### 📁 三种上传模式

1. **单张图片** - 适合处理单个文档
2. **多张图片** - 手动选择多张图片批量处理
3. **指定文件夹** - 自动读取文件夹内所有图片批量处理

## 🚀 快速开始

### ⚠️ 环境要求

**必须使用 `ppocrv5structurev3` conda 环境！**

### 🎯 完整安装方法

```bash
# 步骤 1：激活 conda 环境
conda activate ppocrv5structurev3

# 步骤 2：从源码安装最新版 PaddleOCR
git clone https://github.com/PaddlePaddle/PaddleOCR.git D:\Code\PaddleOCR
pip install -e "D:\Code\PaddleOCR" -i https://mirrors.aliyun.com/pypi/simple/

# 步骤 3：安装 PaddleX（PP-StructureV3 必需）
pip install paddlex
pip install "paddlex[ocr]"

# 步骤 4：安装其他依赖
pip install -r requirements.txt
```

### 🚀 启动方式

#### 方法一：一键启动脚本（推荐）
```bash
双击运行：start_PPocr_service.bat
```

#### 方法二：命令行启动
```bash
conda activate ppocrv5structurev3
streamlit run app.py
```

**访问地址**：http://localhost:8501

## 📖 使用指南

### 1. 选择识别模式

在左侧边栏选择：
- **🔤 PaddleOCR (标准OCR)** - 快速文字识别
- **📄 PP-StructureV3 (文档解析)** - 复杂文档结构分析

### 2. 选择上传模式

- **单张图片**：通过文件上传器选择一张图片
- **多张图片**：
  1. 选择"多张图片"上传模式
  2. 点击文件上传器，可同时选择多张图片（支持 Ctrl/Shift 多选）
  3. 预览已上传的图片（最多显示前8张缩略图）
  4. 点击"批量处理"按钮开始识别
- **指定文件夹**：
  1. 选择"指定文件夹"上传模式
  2. 输入文件夹完整路径（例如：`D:\Images\Documents`）
  3. 系统自动扫描并显示找到的图片数量
  4. 预览文件夹中的图片（最多显示前8张）
  5. 点击"批量处理文件夹"按钮开始识别

支持格式：PNG, JPG, JPEG（大小写不敏感）

### 3. 查看结果

**PaddleOCR 结果**：
- 📝 纯文本内容显示
- 💾 自动保存到 `output/paddleocr_text_时间戳.txt`

**PP-StructureV3 结果**：
- 📄 Markdown 格式预览
- 🖼️ 图片位置标记
- 💾 保存到 `output/temp_xxx.md` + 图片文件

## 📁 项目结构

```
OCR/
├── app.py                     # ✨ 主应用 - 完整Web界面
├── PP-OCRv5.py               # 📝 基础OCR示例
├── PP-StructureV3.py         # 📄 文档解析示例
├── start_PPocr_service.bat   # 🚀 一键启动脚本
├── requirements.txt          # 📋 依赖列表
├── temp/                     # 📁 临时上传文件（自动去重）
├── output/                   # 📊 结果输出文件夹
│   ├── *.txt                # PaddleOCR 纯文本结果
│   ├── *.md                 # PP-StructureV3 结构化结果
│   ├── *.json               # 详细结构化数据
│   └── imgs/                # 可视化图片
└── README.md                 # 📖 使用说明
```

## 💡 使用技巧

### 模式选择建议
| 场景类型 | 推荐模式 | 原因 |
|---------|---------|------|
| 简单文字识别 | PaddleOCR | 速度快、体积小 |
| 复杂文档 | PP-StructureV3 | 结构完整、格式保留 |
| 表格处理 | PP-StructureV3 | 自动表格识别 |
| 批量处理 | PaddleOCR | 高效处理 |

### 最佳实践
1. **图片质量**：建议分辨率 300DPI 以上
2. **文件大小**：控制在 10MB 以内获得最佳性能
3. **大批量处理**：建议单次不超过100张图片，避免内存占用过大
4. **路径格式**：Windows 路径使用反斜杠 `\` 或双反斜杠 `\\`

## 🔧 批量上传功能详解

### 核心函数

#### `get_images_from_folder(folder_path: str) -> List[Path]`
从指定文件夹获取所有支持的图片文件

#### `process_batch_images(model_type, image_paths, ocr_model=None, pipeline=None)`
批量处理多张图片，自动处理错误，不会因为单张图片失败而中断整个批处理

### 文件命名和去重
- 使用 MD5 哈希值前8位作为文件标识
- 相同文件不会重复保存到 temp 目录
- 文件命名格式：`temp_{hash}_{original_name}`

### 性能说明
- 批量处理时，模型只加载一次，提高处理效率
- 使用 `@st.cache_resource` 缓存模型，重复运行更快
- 第一次运行会下载模型（约200-500MB），请耐心等待

### 错误处理
1. **单张图片处理失败** - 不会中断整个批处理，错误会被记录在结果中
2. **文件夹不存在** - 显示友好的错误提示
3. **不支持的文件格式** - 自动跳过，只处理 PNG/JPG/JPEG
4. **模型加载失败** - 显示详细的错误信息和解决方案

## 📝 更新日志

### v2.1.0 (2025-10-31)
- ✅ 新增多张图片批量上传功能
- ✅ 新增指定文件夹批量上传功能
- ✅ 添加上传模式选择器
- ✅ 实现批量处理进度显示
- ✅ 添加处理结果汇总统计

### v2.0.0 (2025-10-31)
- ✅ 完全修复PP-StructureV3集成问题
- ✅ 智能去重：使用MD5哈希避免重复文件保存
- ✅ 正确文本提取：修复PaddleOCR文本提取逻辑
- ✅ 优化缓存：大幅提升模型加载和识别速度

## 🔍 故障排除

### 常见问题
1. **ModuleNotFoundError**：确认在 `ppocrv5structurev3` 环境中
2. **识别结果为空**：检查图片格式和清晰度
3. **PP-StructureV3失败**：尝试先运行 `python PP-StructureV3.py`
4. **模型下载慢**：等待首次模型下载完成

### 调试方法
```bash
# 检查环境
conda activate ppocrv5structurev3
python -c "import paddleocr, streamlit; print('Environment OK')"

# 测试基础功能
python PP-OCRv5.py
python PP-StructureV3.py
```

---

**开发环境**: ppocrv5structurev3  
**支持模型**: PaddleOCR v5, PP-StructureV3  
**框架**: Streamlit 1.51.0