import streamlit as st
import os
from pathlib import Path
import time
from datetime import datetime
import numpy as np
from PIL import Image

# Configure Streamlit page
st.set_page_config(
    page_title="PaddleOCR 与 PP-StructureV3 文档识别",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_paddleocr_model():
    """Load PaddleOCR model with default parameters"""
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )
    return ocr

@st.cache_resource
def load_ppstructurev3_model():
    """Load PPStructureV3 model with default parameters"""
    from paddleocr import PPStructureV3

    pipeline = PPStructureV3(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False
    )
    return pipeline

def process_paddleocr(ocr_model, image_data):
    """Process image with PaddleOCR and extract text using the working PP-OCRv5.py approach"""
    # Convert image to numpy array if it's a file path
    if isinstance(image_data, (str, Path)):
        image = Image.open(image_data)
        image_array = np.array(image)
    else:
        image_array = image_data

    result = ocr_model.predict(input=image_array)

    # Create output directory
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Extract text content using the same approach as PP-OCRv5.py
    text_content = []

    for res in result:
        # Print results (as in original PP-OCRv5.py)
        res.print()

        # Save images and JSON to output folder (as in original PP-OCRv5.py)
        res.save_to_img(str(output_path))
        res.save_to_json(str(output_path))

        # Extract text from the result - PaddleOCR returns OCRResult objects that can be accessed as dicts
        try:
            # Method 1: Direct dict-like access (most reliable for PaddleOCR)
            if isinstance(res, dict) or hasattr(res, '__getitem__'):
                result_dict = res if isinstance(res, dict) else dict(res)
                if 'res' in result_dict and 'rec_texts' in result_dict['res']:
                    text_content.extend(result_dict['res']['rec_texts'])
                elif 'rec_texts' in result_dict:
                    text_content.extend(result_dict['rec_texts'])

            # Method 2: Direct attribute access
            if not text_content:  # Only try if no text found yet
                if hasattr(res, 'rec_texts') and res.rec_texts:
                    text_content.extend(res.rec_texts)
                elif hasattr(res, 'texts') and res.texts:
                    text_content.extend(res.texts)

            # Method 3: From res attribute (for dict-like objects)
            if not text_content and hasattr(res, 'res'):
                res_obj = res.res
                if isinstance(res_obj, dict) and 'rec_texts' in res_obj:
                    text_content.extend(res_obj['rec_texts'])

        except Exception as e:
            print(f"⚠️ Error extracting text from result: {e}")
            # Continue processing, will try JSON fallback

    pure_text = '\n'.join(text_content)

    # Debug info in terminal
    print(f"📝 Extracted {len(text_content)} text lines")
    print(f"📄 Text preview: {pure_text[:200]}...")

    # Fallback: if no text extracted, try reading from the JSON file
    if len(text_content) == 0:
        print("🔍 No text extracted, trying to read from JSON files...")
        json_files = list(output_path.glob("*_res.json"))
        for json_file in json_files:
            try:
                import json
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    # JSON files have rec_texts at the root level
                    if 'rec_texts' in json_data:
                        text_content = json_data['rec_texts']
                        pure_text = '\n'.join(text_content)
                        print(f"✅ Successfully extracted {len(text_content)} text lines from JSON: {json_file.name}")
                        break
                    # Also check nested structure
                    elif 'res' in json_data and 'rec_texts' in json_data['res']:
                        text_content = json_data['res']['rec_texts']
                        pure_text = '\n'.join(text_content)
                        print(f"✅ Successfully extracted {len(text_content)} text lines from JSON (nested): {json_file.name}")
                        break
            except Exception as e:
                print(f"❌ Error reading JSON {json_file}: {e}")
                continue

    # Save pure text to output folder
    text_filename = output_path / f"paddleocr_text_{timestamp}.txt"
    with open(text_filename, 'w', encoding='utf-8') as f:
        f.write(pure_text)

    # Final debug info
    print(f"✅ Final result: {len(text_content)} text lines saved to: {text_filename}")
    print(f"📝 Final text preview: {pure_text[:300]}...")

    return pure_text, str(text_filename)

def process_ppstructurev3(pipeline, image_path):
    """Process image with PPStructureV3 and save markdown and images using the working PP-StructureV3.py approach"""
    # Ensure we have a proper string path
    image_path_str = str(image_path).replace('\\', '/')
    print(f"🔍 Processing image with PP-StructureV3: {image_path_str}")

    # Verify file exists
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    print(f"✅ File exists, size: {Path(image_path).stat().st_size} bytes")

    try:
        result = pipeline.predict(input=image_path_str)
        print(f"🎯 Pipeline processing completed, got {len(result)} result(s)")
    except Exception as e:
        print(f"❌ Pipeline processing failed: {e}")
        raise

    output_path = Path("output")
    output_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Process results using the same approach as PP-StructureV3.py
    print(f"Processing {len(result)} result(s) from PP-StructureV3")
    for i, res in enumerate(result):
        print(f"Processing result {i+1}/{len(result)}")
        # Print results (as in original PP-StructureV3.py)
        res.print()

        # Save JSON to output folder (as in original PP-StructureV3.py)
        res.save_to_json(save_path=str(output_path))

        # Save Markdown to output folder (the missing key step!)
        res.save_to_markdown(save_path=str(output_path))

    # Also save images (additional enhancement)
    for res in result:
        if hasattr(res, 'save_to_img'):
            res.save_to_img(save_path=str(output_path))

    # For display in web interface, try to load the generated markdown files
    # PP-StructureV3 creates markdown files with the pattern: temp_*.md or input_filename.md
    markdown_files = list(output_path.glob("temp_*.md"))
    if not markdown_files:
        # Try other patterns if temp_*.md not found
        markdown_files = list(output_path.glob("*.md"))

    print(f"🔍 Found {len(markdown_files)} markdown file(s): {[f.name for f in markdown_files]}")

    if markdown_files:
        # Use the most recent markdown file for display
        latest_md_file = max(markdown_files, key=lambda x: x.stat().st_mtime)
        print(f"📖 Using latest markdown file: {latest_md_file.name}")
        try:
            with open(latest_md_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            print(f"✅ Successfully loaded markdown content ({len(markdown_content)} chars)")
            return markdown_content, str(latest_md_file)
        except Exception as e:
            print(f"⚠️ Error reading generated markdown file: {e}")

    # Fallback: only create if no markdown files were found and processed
    if not markdown_files:
        print("📝 No markdown files found, creating fallback content...")
        text_content = []
        for res in result:
            # Try to extract text from result for display
            if hasattr(res, 'res') and isinstance(res.res, dict):
                if 'rec_texts' in res.res:
                    text_content.extend(res.res['rec_texts'])
            elif hasattr(res, 'texts'):
                text_content.extend(res.texts)

        fallback_markdown = '\n\n'.join([f"## 识别文本\n\n{txt}" for txt in text_content])
        fallback_filename = output_path / f"ppstructure_fallback_{timestamp}.md"

        with open(fallback_filename, 'w', encoding='utf-8') as f:
            f.write(fallback_markdown)

        return fallback_markdown, str(fallback_filename)
    else:
        # If we found markdown files, return a simple message
        return None, "markdown_files_generated"

def main():
    st.title("📄 PaddleOCR 与 PP-StructureV3 文档识别系统")

    # Sidebar for model selection
    st.sidebar.title("🔧 模型选择")
    model_type = st.sidebar.radio(
        "选择识别模型",
        ["PaddleOCR (标准OCR)", "PP-StructureV3 (文档解析)"],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 模型说明")
    if model_type == "PaddleOCR (标准OCR)":
        st.sidebar.info("""
        **PaddleOCR 标准模式**

        - ✅ 纯文本提取
        - ✅ 快速识别
        - ✅ 适合简单OCR任务
        - 📄 仅输出纯文本
        """)
    else:
        st.sidebar.info("""
        **PP-StructureV3 模式**

        - ✅ 文档结构分析
        - ✅ 版面布局识别
        - ✅ 表格和图像处理
        - 📝 输出 Markdown 格式
        - 💾 自动保存图片和文件
        """)

    # File upload section
    st.header("📁 上传图片")
    uploaded_file = st.file_uploader(
        "选择图片文件",
        type=['png', 'jpg', 'jpeg'],
        help="支持 PNG、JPG、JPEG 格式的图片文件"
    )

    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 📷 上传的图片")
            st.image(uploaded_file, caption="原始图片", width='stretch')

        # Save uploaded file temporarily (avoid duplicates)
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        # Use simple filename with hash to avoid duplicates for the same file
        import hashlib
        file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()[:8]
        temp_image_path = temp_dir / f"temp_{file_hash}_{uploaded_file.name}"

        # Only save if file doesn't exist
        if not temp_image_path.exists():
            with open(temp_image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.info(f"📁 图片已保存至: `{temp_image_path}`")
        else:
            st.info(f"📁 使用已存在的图片: `{temp_image_path}`")

        # Process button
        process_button = st.button(
            "🚀 开始识别",
            type="primary",
            use_container_width=True
        )

        if process_button:
            with st.spinner(f"正在使用 {model_type.split('(')[0].strip()} 处理图片..."):
                try:
                    start_time = time.time()

                    if model_type == "PaddleOCR (标准OCR)":
                        # Load PaddleOCR model
                        with st.spinner("加载 PaddleOCR 模型..."):
                            ocr_model = load_paddleocr_model()

                        # Process with PaddleOCR
                        with st.spinner("识别文本中..."):
                            # Open image and convert to numpy array
                            image = Image.open(temp_image_path)
                            image_array = np.array(image)
                            result_text, saved_file = process_paddleocr(ocr_model, image_array)

                        processing_time = time.time() - start_time

                        # Display results
                        with col2:
                            st.markdown("### 📝 识别结果")
                            st.success(f"处理完成！用时: {processing_time:.2f} 秒")

                            st.markdown("#### 纯文本输出:")
                            st.text_area("识别结果", result_text, height=300, key="paddleocr_result")

                            st.markdown("#### 文件信息:")
                            st.info(f"✅ 文本已保存至: `{saved_file}`")

                    else:  # PP-StructureV3
                        # Load PPStructureV3 model
                        with st.spinner("加载 PP-StructureV3 模型..."):
                            pipeline = load_ppstructurev3_model()

                        # Process with PPStructureV3
                        with st.spinner("文档解析中..."):
                            markdown_result, saved_file = process_ppstructurev3(pipeline, temp_image_path)

                        processing_time = time.time() - start_time

                        # Display results
                        with col2:
                            st.markdown("### 📝 识别结果")
                            st.success(f"处理完成！用时: {processing_time:.2f} 秒")

                            if markdown_result and saved_file != "markdown_files_generated":
                                st.markdown("#### Markdown 预览:")
                                st.markdown(markdown_result)
                                st.markdown("#### 文件信息:")
                                st.info(f"✅ Markdown 文件已保存至: `{saved_file}`")
                            elif saved_file == "markdown_files_generated":
                                st.markdown("#### Markdown 预览:")
                                st.info("✅ Markdown 文件已生成并保存至 `output/` 文件夹")
                                # Try to display the generated markdown
                                markdown_files = list(Path("output").glob("temp_*.md"))
                                if markdown_files:
                                    latest_md = max(markdown_files, key=lambda x: x.stat().st_mtime)
                                    try:
                                        with open(latest_md, 'r', encoding='utf-8') as f:
                                            content = f.read()
                                        st.markdown(content)
                                    except Exception as e:
                                        st.warning(f"无法显示markdown内容: {e}")
                            st.info(f"✅ 图片文件已保存至: `output/` 文件夹")

                    # Keep temporary files (as requested)
                    st.info(f"📁 临时文件保留在: `{temp_image_path}`")

                except Exception as e:
                    st.error(f"❌ 处理过程中出现错误: {str(e)}")
                    print(f"❌ Streamlit processing error: {e}")
                    st.markdown("#### 可能的解决方案:")
                    st.markdown("""
                    1. 确保已正确激活 `ppocrv5structurev3` conda 环境
                    2. 检查 PaddleOCR 和 PaddleX 是否正确安装
                    3. 确认图片格式正确
                    4. 查看终端输出获取详细错误信息
                    5. 确认临时文件存在且可访问
                    """)

    # Footer
    st.markdown("---")
    st.markdown("""
    ### 💡 使用说明
    - **PaddleOCR**: 快速文字识别，输出纯文本格式
    - **PP-StructureV3**: 高级文档解析，识别文档结构，输出 Markdown 格式
    - 所有处理结果都自动保存在 `output` 文件夹中
    - 支持的图片格式：PNG、JPG、JPEG
    """)

    # Environment status
    st.markdown("---")
    st.markdown("### 🔧 环境状态")
    st.info("""
    ✅ 当前环境: ppocrv5structurev3
    ✅ 支持模型: PaddleOCR, PP-StructureV3
    📁 输出目录: output/
    """)

if __name__ == "__main__":
    main()