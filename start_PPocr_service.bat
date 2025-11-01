@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 PaddleOCR 文档识别系统启动器
echo ========================================
echo.
echo 📄 系统: PaddleOCR + PP-StructureV3 双模式识别
echo 🌐 地址: http://localhost:8501
echo.
echo ⏳ 首次运行模型下载需要 2-3 分钟
echo     后续启动会使用缓存模型，速度更快
echo.
echo 🛑 要停止服务请关闭此窗口
echo.

REM Change to the correct directory
cd /d "D:\Code\OCR"

REM Activate conda environment
echo 🔧 正在激活 ppocrv5structurev3 环境...

REM Get conda installation path
for /f "tokens=*" %%i in ('conda info --base') do set CONDA_PATH=%%i

REM Activate our specific environment
call "%CONDA_PATH%\Scripts\activate.bat" ppocrv5structurev3

REM Check if activation was successful
if errorlevel 1 (
    echo.
    echo ❌ 错误: 无法激活 ppocrv5structurev3 环境
    echo 请确认:
    echo    1. conda 已正确安装
    echo    2. ppocrv5structurev3 环境已创建
    echo    3. PaddleOCR 和 PaddleX 已正确安装
    echo.
    echo 💡 安装命令:
    echo    conda create -n ppocrv5structurev3 python=3.12
    echo    conda activate ppocrv5structurev3
    echo    pip install streamlit paddlex
    echo    pip install -e "D:\Code\PaddleOCR"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

echo ✅ ppocrv5structurev3 环境激活成功
echo.

REM Verify dependencies
echo 📦 正在检查依赖...
python -c "import streamlit, paddleocr; print('✅ 依赖检查通过')" 2>nul
if errorlevel 1 (
    echo.
    echo ❌ 错误: 缺少必要依赖
    echo 请运行以下命令安装:
    echo    conda activate ppocrv5structurev3
    echo    pip install streamlit
    echo    pip install -e "D:\Code\PaddleOCR"
    echo    pip install "paddlex[ocr]"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

echo ✅ 依赖检查完成
echo.

REM Launch the Streamlit application
echo 🌐 正在启动 PaddleOCR 文档识别系统...
echo 📱 浏览器将自动打开 http://localhost:8501
echo.
echo 如果浏览器没有自动打开，请手动访问上面的地址
echo.

streamlit run app.py

echo.
echo 👋 服务已停止
echo 感谢使用 PaddleOCR 文档识别系统！
echo.
pause >nul