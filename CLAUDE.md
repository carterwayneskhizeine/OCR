# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **mature and fully tested** PaddleOCR document recognition system built with Streamlit that supports both PP-OCRv5 and PP-StructureV3 dual-mode recognition. The application provides a complete web interface for uploading images and extracting text with intelligent file management and robust error handling.

## Development Environment

**Critical**: This project must run in the `ppocrv5structurev3` conda environment. The environment contains all required dependencies including the latest PaddleOCR, PaddleX, Streamlit, and related packages.

### Environment Setup

**Critical**: Always activate the environment first before running any commands or installing packages.

```bash
# Activate the ppocrv5structurev3 environment
conda activate ppocrv5structurev3
```

### Complete Installation Method

For full functionality including PP-StructureV3, follow this complete installation procedure:

```bash
# Step 1: Activate the conda environment
conda activate ppocrv5structurev3

# Step 2: Download and install PaddleOCR from source (latest development version)
git clone https://github.com/PaddlePaddle/PaddleOCR.git D:\Code\PaddleOCR
pip install -e "D:\Code\PaddleOCR" -i https://mirrors.aliyun.com/pypi/simple/

# Step 3: Install PaddleX (required for PP-StructureV3)
pip install paddlex

# Step 4: Install PaddleX OCR components
pip install "paddlex[ocr]"

# Step 5: Install other dependencies
pip install -r requirements.txt
```

**Important Notes**:
- The installation may take several minutes as it downloads and compiles PaddlePaddle and related dependencies
- This setup supports both simple OCR and advanced document structure analysis
- Use the source installation to get the latest PP-StructureV3 features

### Windows Claude Code Environment Activation

To activate the conda environment in Claude Code on Windows:
```bash
# Use source command
source C:/ProgramData/anaconda3/etc/profile.d/conda.sh && conda activate ppocrv5structurev3
```

## Running the Application

### Primary Methods

1. **Batch Script (Recommended for users)**:
   ```bash
   # Double-click or run:
   start_PPocr_service.bat
   ```

2. **Manual Start (Recommended for development)**:
   ```bash
   conda activate ppocrv5structurev3
   streamlit run app.py
   ```

3. **Command Line (Absolute path)**:
   ```bash
   cd D:\Code\OCR && conda activate ppocrv5structurev3 && streamlit run app.py
   ```

### Application Access
- Default URL: http://localhost:8501
- The application automatically opens in the browser
- Models are cached after first load for faster subsequent startups

## Architecture

### Core Components

- **app.py**: **Production-ready** Streamlit application with dual-mode support and intelligent file management
- **PP-OCRv5.py**: Basic PaddleOCR example script (for testing and reference)
- **PP-StructureV3.py**: Advanced document parsing script using PP-StructureV3 (for testing and reference)
- **start_PPocr_service.bat**: One-click startup script for end users

### OCR Model Configuration

The application supports two recognition modes (simplified from previous three):

1. **PaddleOCR Standard Mode**: Fast text recognition, outputs plain text
2. **PP-StructureV3 Advanced Mode**: Document structure analysis, outputs markdown with images

**Critical Updates**:
- Removed deprecated `use_angle_cls` parameter completely
- Uses only `use_textline_orientation=False` for PaddleOCR
- PP-StructureV3 uses default advanced settings for maximum accuracy
- Both modes are fully functional and tested

### Key Functions

- `load_paddleocr_model()`: **@st.cache_resource** cached PaddleOCR model loader
- `load_ppstructurev3_model()`: **@st.cache_resource** cached PP-StructureV3 model loader
- `process_paddleocr()`: Enhanced text extraction with JSON fallback and proper error handling
- `process_ppstructurev3()`: Complete PP-StructureV3 integration with markdown extraction
- `main()`: Unified web interface with intelligent file management

### Important Implementation Details

#### PaddleOCR Text Extraction
```python
# Working extraction logic (v2.0.0)
if isinstance(res, dict) or hasattr(res, '__getitem__'):
    result_dict = res if isinstance(res, dict) else dict(res)
    if 'res' in result_dict and 'rec_texts' in result_dict['res']:
        text_content.extend(result_dict['res']['rec_texts'])
```

#### PP-StructureV3 Integration
```python
# Working PP-StructureV3 flow (v2.0.0)
for res in result:
    res.print()
    res.save_to_json(save_path=str(output_path))
    res.save_to_markdown(save_path=str(output_path))  # Critical: Generates temp_xxx.md
```

#### Intelligent File Management
```python
# MD5-based deduplication (v2.0.0)
import hashlib
file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()[:8]
temp_image_path = temp_dir / f"temp_{file_hash}_{uploaded_file.name}"

if not temp_image_path.exists():
    # Only save if unique
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
```

## File Structure

```
OCR/
├── app.py                     # ✅ Production-ready main application
├── PP-OCRv5.py               # 📝 Basic PaddleOCR example (testing)
├── PP-StructureV3.py         # 📄 Advanced document parsing (testing)
├── start_PPocr_service.bat   # 🚀 One-click startup script
├── requirements.txt          # 📋 Python dependencies
├── README.md                 # 📖 Comprehensive user documentation
├── CLAUDE.md                 # 🤖 Development guide (this file)
├── temp/                     # 📁 Temporary upload files (auto-deduplicated)
│   └── temp_*.png           # Uploaded images with hash-based naming
└── output/                   # 📊 Results output folder
    ├── paddleocr_text_*.txt  # PaddleOCR text output
    ├── temp_*.md             # PP-StructureV3 markdown output
    ├── *_res.json            # Structured OCR results
    ├── *_markdown.md         # ✨ Full markdown with images
    └── imgs/                 # Generated visualization images
```

## Common Development Tasks

### Testing OCR Functionality
```bash
# Always activate environment first
conda activate ppocrv5structurev3

# Test basic PaddleOCR (should work after proper installation)
python -c "import paddleocr; print('PaddleOCR OK')"

# Test PP-StructureV3 (critical for advanced features)
python -c "from paddleocr import PPStructureV3; print('PP-StructureV3 OK')"

# Test both example scripts
python PP-OCRv5.py        # Should generate output files
python PP-StructureV3.py  # Should generate markdown + images

# Test the web application (full integration)
streamlit run app.py
```

### Debugging Environment Issues

If encountering issues:

#### ModuleNotFoundError
1. **Verify conda environment**: `conda env list` - should show `ppocrv5structurev3` with asterisk
2. **Check specific packages**: `pip list | grep -E "(paddleocr|paddlex)"`
3. **Reinstall if needed**: Refer to installation section

#### PaddleOCR Not Working
1. **Test with PP-OCRv5.py**: `python PP-OCRv5.py`
2. **Check terminal output**: Should show text extraction results
3. **Verify json files**: Check `output/*.json` for `rec_texts` data

#### PP-StructureV3 Not Working
1. **Test with PP-StructureV3.py**: `python PP-StructureV3.py`
2. **Check for markdown files**: `output/temp_*.md` should be generated
3. **Verify images**: `output/imgs/` should contain visualization images

#### Web App Issues
1. **Check terminal**: Look for error messages in Streamlit output
2. **Test individual components**: Run PP-OCRv5.py and PP-StructureV3.py separately
3. **Check file paths**: Verify `temp/` and `output/` directories exist and are readable/writable

### Model Configuration Notes
- **First run**: Models auto-download (~200-500MB each) - be patient
- **Caching**: `@st.cache_resource` ensures models load once per session
- **Performance**: Second run is significantly faster due to caching
- **GPU**: GPU version available but requires proper CUDA setup

## Dependencies

### Latest Working Environment (ppocrv5structurev3)

**Core OCR Dependencies:**
- `paddleocr==3.4.0.dev22+g1f51b0de9` (installed from source: D:\Code\PaddleOCR)
- `paddlepaddle==3.2.1` (PaddlePaddle deep learning framework)
- `paddlex==3.3.6` (PP-StructureV3 support)

**Web Framework:**
- `streamlit==1.51.0` (Web application framework)

**Supporting Libraries:**
- `opencv-contrib-python==4.10.0.84` (Image processing)
- `numpy==2.3.4` (Numerical computations)
- `pandas==2.3.3` (Data handling)
- `pillow==12.0.0` (Image manipulation)
- `shapely==2.1.2` (Geometric operations)

### Installation Requirements

**Critical for PP-StructureV3:**
1. `paddleocr` (from source for latest features)
2. `paddlex[ocr]` (provides PP-StructureV3 components)
3. `paddlepaddle` (deep learning framework)

**Basic requirements.txt:**
```
streamlit>=1.50.0
numpy>=2.0.0
pandas>=2.0.0
pillow>=10.0.0
opencv-contrib-python>=4.0.0
```

**Important**: PaddleOCR and PaddleX must be installed separately as shown in the complete installation method.

## Troubleshooting

### Common Issues and Solutions

#### Empty Text Results
- **Cause**: Incorrect text extraction logic
- **Solution**: Implemented working extraction in v2.0.0 (refer to Key Functions)

#### PP-StructureV3 No Markdown Generated
- **Cause**: Missing `res.save_to_markdown()` call or wrong file lookup pattern
- **Solution**: Fixed in v2.0.0 with proper `temp_*.md` file pattern recognition

#### Multiple Duplicate Files in temp/
- **Cause**: Time-based naming for every upload
- **Solution**: Implemented MD5-based deduplication in v2.0.0

#### Model Not Loading
- **Cause**: Conda environment not activated or missing packages
- **Solution**: Verify environment and check installation steps

### Environment Verification
```bash
# Quick environment check
conda activate ppocrv5structurev3
python -c "import paddleocr, streamlit; from paddleocr import PPStructureV3; print('All dependencies OK')"

# Check versions (for debugging)
python -c "import paddleocr; print(f'PaddleOCR: {paddleocr.__version__}')"
python -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
```

## Development Guidelines

### When Making Changes

1. **Always test with PP-OCRv5.py** first for PaddleOCR changes
2. **Always test with PP-StructureV3.py** first for PP-StructureV3 changes
3. **Use proper environment**: `conda activate ppocrv5structurev3`
4. **Check both output formats**: TXT for PaddleOCR, MD for PP-StructureV3
5. **Verify file naming**: Follow the established patterns to avoid breaking file lookup

### Code Style Requirements

- Use proper error handling with `try/except` blocks
- Include informative print statements for debugging
- Follow the existing naming conventions
- Maintain the dual-mode structure if adding new features
- Test file deduplication logic when modifying upload handling

### Testing Checklist

Before considering a change complete:
- [ ] PaddleOCR mode generates proper `.txt` files
- [ ] PP-StructureV3 mode generates proper `.md` files with image references
- [ ] File deduplication works (same file uploaded multiple times doesn't create duplicates)
- [ ] Web interface displays results correctly
- [ ] Terminal output shows expected processing information
- [ ] Error handling works gracefully without crashing app

---

**This CLAUDE.md should be kept updated with the latest working implementation details.**