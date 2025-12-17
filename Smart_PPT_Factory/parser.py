import os
import json
import glob
from google import genai
from google.genai import types
import fitz  # PyMuPDF
import config

# 配置区
MODEL_NAME = "gemini-2.0-flash-exp"  # 使用Gemini 2.0 Flash进行内容提取
PDF_FILE = "Smart_PPT_Factory/data/高中语文_高一_2025寒假_小组课_张三.pdf"  # 当前要处理的PDF
DEFAULT_PDF = "Smart_PPT_Factory/data/source.pdf"
INPUT_FILE = config.INPUT_FILE
OUTPUT_FILE = config.JSON_PATH
IMAGE_OUTPUT_DIR = "Smart_PPT_Factory/data/extracted_images"

client = genai.Client(api_key=config.API_KEY)

def extract_pdf_content_and_images():
    """提取PDF文字和图片（思维导图）"""
    target_pdf = None
    if os.path.exists(PDF_FILE):
        target_pdf = PDF_FILE
    elif os.path.exists(DEFAULT_PDF):
        target_pdf = DEFAULT_PDF
    else:
        # 尝试查找任何 PDF
        pdfs = glob.glob("Smart_PPT_Factory/data/*.pdf")
        if pdfs:
            target_pdf = pdfs[0]
    
    if not target_pdf:
        print("❌ 未找到PDF文件")
        return False, []
    
    print(f"📄 发现 PDF 文件: {target_pdf}")
    print("正在提取文字和思维导图...")
    
    try:
        doc = fitz.open(target_pdf)
        text_content = ""
        extracted_images = []
        mindmap_image = None
        
        # 创建图片输出目录
        os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
        
        # 提取文字和图片
        for page_num, page in enumerate(doc, 1):
            # 提取文字
            text_content += f"\n=== 第 {page_num} 页 ===\n"
            text_content += page.get_text() + "\n"
            
            # 只从第一页提取思维导图
            if page_num == 1:
                print(f"\n  🔍 分析第1页，寻找思维导图...")
                
                # 获取页面尺寸
                page_rect = page.rect
                page_width = page_rect.width
                page_height = page_rect.height
                
                # 提取图片及其位置信息
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    
                    # 获取图片在页面上的位置
                    img_rects = page.get_image_rects(xref)
                    
                    if img_rects:
                        img_rect = img_rects[0]  # 取第一个位置
                        
                        # 计算图片的相对位置和大小
                        img_width = img_rect.width
                        img_height = img_rect.height
                        img_x = img_rect.x0
                        img_y = img_rect.y0
                        
                        # 计算图片面积占页面的比例
                        img_area = img_width * img_height
                        page_area = page_width * page_height
                        area_ratio = img_area / page_area
                        
                        # 判断是否为思维导图：
                        # 1. 位置在页面中间（y坐标在页面35%-70%之间）
                        # 2. 宽度较大（占页面宽度的50%-95%）
                        # 3. 面积适中（占页面面积的8%-25%）
                        y_ratio = img_y / page_height
                        width_ratio = img_width / page_width
                        
                        is_mindmap = (
                            0.35 <= y_ratio <= 0.70 and
                            0.50 <= width_ratio <= 0.95 and
                            0.08 <= area_ratio <= 0.25
                        )
                        
                        print(f"    图片{img_index+1}: 位置Y={y_ratio:.2f}, 宽度比={width_ratio:.2f}, 面积比={area_ratio:.2f}", end="")
                        
                        if is_mindmap:
                            print(" ✅ [思维导图]")
                            
                            # 提取图片
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            
                            # 保存为思维导图
                            mindmap_filename = f"mindmap.{image_ext}"
                            mindmap_path = os.path.join(IMAGE_OUTPUT_DIR, mindmap_filename)
                            
                            with open(mindmap_path, "wb") as img_file:
                                img_file.write(image_bytes)
                            
                            mindmap_image = {
                                "page": 1,
                                "filename": mindmap_filename,
                                "path": mindmap_path,
                                "is_mindmap": True
                            }
                            
                            print(f"    💾 保存思维导图: {mindmap_filename}")
                        else:
                            print(" ⏭️ [跳过]")
        
        doc.close()
        
        # 保存文字内容
        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text_content)
        
        print(f"\n✅ PDF 提取成功！")
        print(f"  - 文字内容已保存至: {INPUT_FILE}")
        
        if mindmap_image:
            extracted_images.append(mindmap_image)
            print(f"  - 思维导图已提取: {mindmap_image['filename']}")
        else:
            print(f"  ⚠️ 未找到思维导图（将使用AI生成）")
        
        return True, extracted_images
        
    except Exception as e:
        print(f"❌ PDF 提取失败: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def parse_content():
    """解析PDF内容并生成结构化JSON"""
    # 第一步：提取PDF文字和图片
    success, extracted_images = extract_pdf_content_and_images()
    
    if not success:
        print("❌ PDF提取失败，无法继续")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"❌ 错误：未找到输入文件 {INPUT_FILE}")
        return

    print(f"\n📖 正在读取 {INPUT_FILE} ...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print(f"📝 文字内容长度: {len(raw_text)} 字符")

    # 第二步：使用AI进行内容提取和结构化
    prompt = f"""
你是一个专业的教育内容提取专家。请从以下PDF讲义的原始文本中提取完整的结构化内容。

**重要要求：**
1. **完整保留所有文字内容** - 这是语文学科讲义，包含大量文字，必须全部保留，不要省略或总结
2. **智能分页知识点** - 如果某个知识点内容过长（超过800字），请将其拆分为多个子知识点
3. **保留原文** - 例题、练习题等必须保留完整原文，不要改写
4. **识别思维导图位置** - 标注哪些页面包含思维导图（通常在"知识清单"部分）
5. **JSON格式规范** - 确保所有字符串中的引号、换行符都正确转义

**输出格式：**
请输出一个有效的JSON对象，包含以下字段：
- lecture_title: 讲义标题
- learning_objectives: 学习目标数组
- class_intro: 课程导入
- exam_analysis: 考情分析
- mindmap_pages: 思维导图所在页码数组
- knowledge_points: 知识点数组，每个知识点包含title, content, discussion, example_mother, example_variant, method
- teaching_process: 教学过程数组
- consolidation_exercises: 巩固练习数组
- quiz_content: 出门测内容
- homework: 课后作业
- bg_keywords: 背景关键词（英文）

**特别注意：**
- 所有文本内容中的双引号必须转义为 \\"
- 所有换行符使用 \\n 表示
- 确保JSON格式完全有效，可以被标准JSON解析器解析

**PDF原始内容：**
{raw_text}

请输出完整的JSON对象，用```json和```包裹：
"""

    print(f"\n🤖 正在调用 {MODEL_NAME} 进行深度解析...")
    print("⏳ 这可能需要1-2分钟，请耐心等待...")
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1  # 降低温度以获得更准确的提取
            )
        )
        
        # 清理 LLM 可能返回的 Markdown 标记
        json_content = response.text.strip()
        
        print(f"\n🔧 清理JSON格式...")
        print(f"  原始长度: {len(json_content)} 字符")
        print(f"  开头: {json_content[:50]}")
        
        # 1. 移除开头的 ```json
        if json_content.startswith("```json"):
            json_content = json_content[7:].strip()
            print(f"  ✅ 移除开头的 ```json")
        elif json_content.startswith("```"):
            json_content = json_content[3:].strip()
            print(f"  ✅ 移除开头的 ```")
        
        # 2. 移除结尾的 ```
        if json_content.endswith("```"):
            json_content = json_content[:-3].strip()
            print(f"  ✅ 移除结尾的 ```")
        
        # 3. 移除 JSON 结尾后的额外文本
        last_brace_index = json_content.rfind("}")
        if last_brace_index != -1 and last_brace_index < len(json_content) - 1:
            json_content = json_content[:last_brace_index+1]
            print(f"  ✅ 移除结尾额外文本")
        
        print(f"  清理后长度: {len(json_content)} 字符")
        print(f"  清理后开头: {json_content[:50]}")

        try:
            parsed_data = json.loads(json_content)
            print(f"✅ JSON解析成功！")
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            print("--- 清理后的数据 (前500字符) ---")
            print(json_content[:500])
            print("---------------------------")
            # 尝试保存原始JSON以便调试
            with open("Smart_PPT_Factory/data/debug_json.txt", "w", encoding="utf-8") as f:
                f.write(json_content)
            print(f"完整JSON已保存到: Smart_PPT_Factory/data/debug_json.txt")
            import sys
            sys.exit(1)
        
        # 添加提取的图片信息
        parsed_data["extracted_images"] = extracted_images
        
        # 保存结构化数据
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ 转换成功！结构化数据已保存至: {OUTPUT_FILE}")
        print(f"📊 统计信息:")
        print(f"  - 讲义标题: {parsed_data.get('lecture_title', '未提取')}")
        print(f"  - 学习目标: {len(parsed_data.get('learning_objectives', []))} 个")
        print(f"  - 知识点: {len(parsed_data.get('knowledge_points', []))} 个")
        print(f"  - 提取图片: {len(extracted_images)} 张")
        print(f"  - 思维导图页: {parsed_data.get('mindmap_pages', [])}")
        
    except Exception as e:
        print(f"❌ 解析过程发生错误: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)

if __name__ == "__main__":
    parse_content()
