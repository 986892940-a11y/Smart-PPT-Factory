"""
AI图片生成模块
只在需要时生成图片，避免遮挡文字
"""
import os
import io
from google import genai
from google.genai import types
import config

client = genai.Client(api_key=config.API_KEY)

def generate_image(prompt, aspect_ratio="16:9"):
    """
    生成AI图片
    
    参数:
        prompt: 图片描述
        aspect_ratio: 宽高比 (16:9, 1:1, 9:16等)
    
    返回:
        BytesIO对象或None
    """
    try:
        print(f"  🎨 正在生成图片: {prompt[:50]}...")
        
        # 检查是否使用Gemini图片生成模型
        if "gemini" in config.IMAGE_MODEL.lower():
            # Gemini模型使用generate_content方式
            response = client.models.generate_content(
                model=config.IMAGE_MODEL,
                contents=prompt
            )
            
            # Gemini返回的是图片数据
            if hasattr(response, 'candidates') and response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data'):
                        image_data = part.inline_data.data
                        return io.BytesIO(image_data)
            
            print(f"  ⚠️ Gemini模型未返回图片数据")
            return None
        else:
            # Imagen模型使用generate_images方式
            response = client.models.generate_images(
                model=config.IMAGE_MODEL,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio=aspect_ratio,
                    safety_filter_level="block_low_and_above",
                    person_generation="allow_adult"
                )
            )
            
            if response.generated_images:
                image_data = response.generated_images[0].image.image_bytes
                return io.BytesIO(image_data)
            else:
                print(f"  ⚠️ Imagen模型未返回图片")
                return None
            
    except Exception as e:
        print(f"  ⚠️ 图片生成错误: {e}")
        return None


def generate_cover_image(subject, season):
    """
    生成封面背景图
    要求：淡雅、不遮挡中间文字区域
    """
    season_map = {
        "春": "spring season, cherry blossoms, fresh green, gentle",
        "春季": "spring season, cherry blossoms, fresh green, gentle",
        "夏": "summer season, sunshine, bright, warm",
        "暑假": "summer season, sunshine, bright, warm",
        "秋": "autumn season, maple leaves, warm orange and red",
        "秋季": "autumn season, maple leaves, warm orange and red",
        "冬": "winter season, snow, cool blue and white",
        "寒假": "winter season, snow, cool blue and white"
    }
    
    season_keywords = season_map.get(season, "minimalist, abstract, soft")
    
    prompt = f"""
    Create an elegant background image for an educational presentation cover page.
    Theme: {subject} education, {season_keywords}
    
    Style requirements:
    - Very light and soft colors (pastel tones)
    - Subtle gradient background
    - Decorative elements only on the edges (top, bottom, left, right corners)
    - IMPORTANT: Keep the CENTER AREA completely clear and minimal
    - No text, no complex patterns in the middle
    - Professional and academic atmosphere
    - Subtle Chinese cultural elements (optional, on edges only)
    - High transparency, should not distract from text
    
    Layout: Border decoration style, center area must be clean and empty
    """
    
    return generate_image(prompt, aspect_ratio="16:9")


def generate_lecture_title_image(title):
    """
    生成讲义标题配图
    要求：与标题内容相关，放在标题旁边
    """
    prompt = f"""
    Create an illustration for a lecture title: "{title}"
    Style: Modern, minimalist, educational
    Requirements:
    - Related to the topic
    - Clean and simple design
    - Suitable for placing next to text
    - Professional academic style
    - Size suitable for sidebar decoration
    """
    
    return generate_image(prompt, aspect_ratio="1:1")


def generate_intro_image(intro_text):
    """
    生成课堂引入配图
    要求：与引入内容相关，吸引注意力
    """
    # 提取关键词
    keywords = intro_text[:100]
    
    prompt = f"""
    Create an engaging illustration for a class introduction.
    Content: {keywords}
    Style: Warm, inviting, educational
    Requirements:
    - Related to the introduction content
    - Visually appealing and engaging
    - Suitable for educational setting
    - Not too distracting
    """
    
    return generate_image(prompt, aspect_ratio="16:9")


def generate_knowledge_point_image(title, content):
    """
    生成知识点配图（可选）
    要求：辅助理解知识点
    """
    prompt = f"""
    Create a simple illustration for a knowledge point: "{title}"
    Content hint: {content[:100]}
    Style: Clean, educational, diagram-like
    Requirements:
    - Help visualize the concept
    - Simple and clear
    - Professional academic style
    """
    
    return generate_image(prompt, aspect_ratio="1:1")


def generate_learning_objectives_image_old(objectives):
    """
    生成学习目标层级图
    混合方案：Python生成清晰文字 + AI生成创意背景
    
    参数:
        objectives: 学习目标列表
    
    返回:
        BytesIO对象
    """
    from PIL import Image, ImageDraw, ImageFont
    import io
    import random
    
    # 解析层级
    levels = []
    clean_objectives = []
    
    level_keywords = ["识记", "理解", "操作", "运用", "迁移", "分析", "综合", "评价"]
    level_colors = {
        "识记": ("#7ED7C1", "#5BC0BE"),
        "理解": ("#00A896", "#028090"), 
        "操作": ("#F39C12", "#E67E22"),
        "运用": ("#E74C3C", "#C0392B"),
        "迁移": ("#9B59B6", "#8E44AD"),
        "分析": ("#3498DB", "#2980B9"),
        "综合": ("#1ABC9C", "#16A085"),
        "评价": ("#E67E22", "#D35400")
    }
    
    for obj in objectives:
        found_level = None
        for keyword in level_keywords:
            if keyword in obj:
                found_level = keyword
                break
        
        if not found_level:
            found_level = "理解"
        
        levels.append(found_level)
        clean_objectives.append(obj)
    
    # 创建图片
    width, height = 1920, 1080
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 随机选择布局风格
    layout_styles = ["stairs", "cards", "timeline", "pyramid"]
    selected_layout = random.choice(layout_styles)
    
    # 加载字体
    try:
        level_font = ImageFont.truetype("msyhbd.ttc", 56)
        text_font = ImageFont.truetype("msyh.ttc", 44)
        number_font = ImageFont.truetype("msyhbd.ttc", 72)
    except:
        try:
            level_font = ImageFont.truetype("simhei.ttf", 56)
            text_font = ImageFont.truetype("simhei.ttf", 44)
            number_font = ImageFont.truetype("simhei.ttf", 72)
        except:
            level_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            number_font = ImageFont.load_default()
    
    # 根据布局风格绘制
    if selected_layout == "stairs":
        # 阶梯式布局
        start_y = 150
        step_height = (height - start_y - 100) // len(objectives)
        
        for i, (level, obj) in enumerate(zip(levels, clean_objectives)):
            y = start_y + i * step_height
            x_offset = i * 150
            
            # 获取颜色
            colors = level_colors.get(level, ("#00A896", "#028090"))
            
            # 绘制卡片背景
            card_x = 200 + x_offset
            card_y = y
            card_width = 1500 - x_offset
            card_height = step_height - 30
            
            # 渐变效果（简化版）
            for dy in range(card_height):
                ratio = dy / card_height
                r1, g1, b1 = int(colors[0][1:3], 16), int(colors[0][3:5], 16), int(colors[0][5:7], 16)
                r2, g2, b2 = int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16)
                r = int(r1 * (1-ratio) + r2 * ratio)
                g = int(g1 * (1-ratio) + g2 * ratio)
                b = int(b1 * (1-ratio) + b2 * ratio)
                draw.line([(card_x, card_y + dy), (card_x + card_width, card_y + dy)], 
                         fill=(r, g, b, 230))
            
            # 绘制编号圆圈
            circle_x = card_x - 60
            circle_y = card_y + card_height // 2
            draw.ellipse([circle_x - 50, circle_y - 50, circle_x + 50, circle_y + 50],
                        fill=colors[0], outline='white', width=5)
            
            # 绘制编号
            num_bbox = draw.textbbox((0, 0), str(i+1), font=number_font)
            num_width = num_bbox[2] - num_bbox[0]
            num_height = num_bbox[3] - num_bbox[1]
            draw.text((circle_x - num_width//2, circle_y - num_height//2), 
                     str(i+1), fill='white', font=number_font)
            
            # 绘制层级标签
            level_text = f"{level}"
            draw.text((card_x + 40, card_y + 20), level_text, fill='white', font=level_font)
            
            # 绘制目标内容
            content_y = card_y + 85
            # 处理长文本
            if len(obj) > 25:
                mid = len(obj) // 2
                # 找最近的标点符号
                for j in range(mid - 5, mid + 5):
                    if j < len(obj) and obj[j] in '，。、；':
                        mid = j + 1
                        break
                line1 = obj[:mid]
                line2 = obj[mid:]
                draw.text((card_x + 40, content_y), line1, fill='white', font=text_font)
                draw.text((card_x + 40, content_y + 55), line2, fill='white', font=text_font)
            else:
                draw.text((card_x + 40, content_y), obj, fill='white', font=text_font)
    
    elif selected_layout == "cards":
        # 卡片式布局
        start_y = 200
        spacing = (height - start_y - 100) // len(objectives)
        
        for i, (level, obj) in enumerate(zip(levels, clean_objectives)):
            y = start_y + i * spacing
            colors = level_colors.get(level, ("#00A896", "#028090"))
            
            # 绘制卡片
            card_x = 150
            card_width = 1620
            card_height = spacing - 40
            
            # 绘制阴影
            shadow_offset = 8
            draw.rounded_rectangle(
                [card_x + shadow_offset, y + shadow_offset, 
                 card_x + card_width + shadow_offset, y + card_height + shadow_offset],
                radius=20, fill=(0, 0, 0, 50)
            )
            
            # 绘制卡片主体
            draw.rounded_rectangle(
                [card_x, y, card_x + card_width, y + card_height],
                radius=20, fill=colors[0], outline='white', width=4
            )
            
            # 绘制层级标签区域
            label_width = 200
            draw.rounded_rectangle(
                [card_x, y, card_x + label_width, y + card_height],
                radius=20, fill=colors[1]
            )
            
            # 绘制编号和层级
            draw.text((card_x + 100, y + 30), str(i+1), fill='white', 
                     font=number_font, anchor="mm")
            draw.text((card_x + 100, y + card_height - 40), level, fill='white',
                     font=level_font, anchor="mm")
            
            # 绘制目标内容
            content_x = card_x + label_width + 50
            content_y = y + card_height // 2
            
            if len(obj) > 25:
                mid = len(obj) // 2
                for j in range(mid - 5, mid + 5):
                    if j < len(obj) and obj[j] in '，。、；':
                        mid = j + 1
                        break
                line1 = obj[:mid]
                line2 = obj[mid:]
                draw.text((content_x, content_y - 30), line1, fill='white', font=text_font)
                draw.text((content_x, content_y + 30), line2, fill='white', font=text_font)
            else:
                draw.text((content_x, content_y), obj, fill='white', font=text_font)
    
    # 保存到BytesIO
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    
    print(f"    🎨 已生成学习目标图（布局: {selected_layout}）")
    
    return output



def generate_learning_objectives_image(objectives):
    """
    生成手绘风格的学习目标层级图
    使用AI生成创意手绘插画风格
    
    参数:
        objectives: 学习目标列表
    
    返回:
        BytesIO对象或None
    """
    import random
    
    # 解析层级
    levels = []
    clean_objectives = []
    
    level_keywords = ["识记", "理解", "操作", "运用", "迁移", "分析", "综合", "评价"]
    
    for obj in objectives:
        found_level = None
        for keyword in level_keywords:
            if keyword in obj:
                found_level = keyword
                break
        
        if not found_level:
            found_level = "理解"
        
        levels.append(found_level)
        clean_objectives.append(obj)
    
    # 构建目标文本（英文描述，让AI理解内容）
    objectives_description = ""
    for i, (level, obj) in enumerate(zip(levels, clean_objectives), 1):
        objectives_description += f"Level {i} ({level}): {obj}\n"
    
    # 随机选择手绘风格主题
    themes = [
        {
            "name": "学习之旅",
            "elements": "mountain climbing, path with milestones, treasure chest at the top, adventure map",
            "style": "hand-drawn adventure map style"
        },
        {
            "name": "知识树",
            "elements": "tree with roots and branches, leaves representing different levels, fruits as achievements",
            "style": "botanical illustration style with hand-drawn details"
        },
        {
            "name": "齿轮系统",
            "elements": "interconnected gears, mechanical parts, arrows showing flow, steampunk elements",
            "style": "technical sketch style with vintage aesthetics"
        },
        {
            "name": "建筑蓝图",
            "elements": "building blocks, construction site, scaffolding, blueprint style",
            "style": "architectural sketch with hand-drawn annotations"
        },
        {
            "name": "太空探索",
            "elements": "planets, rockets, stars, space stations, astronaut",
            "style": "whimsical space doodle style"
        },
        {
            "name": "海洋深度",
            "elements": "ocean layers, fish, submarine, treasure, coral reef",
            "style": "nautical illustration with watercolor effects"
        },
        {
            "name": "时间线",
            "elements": "timeline with icons, clock elements, calendar pages, milestone markers",
            "style": "vintage timeline infographic style"
        },
        {
            "name": "书籍堆叠",
            "elements": "stacked books, open books, bookmarks, reading glasses, quill pen",
            "style": "literary sketch style with classic elements"
        }
    ]
    
    selected_theme = random.choice(themes)
    
    # 构建详细的prompt
    prompt = f"""
Create a beautiful hand-drawn style educational infographic showing learning objectives hierarchy.

THEME: {selected_theme['name']}
VISUAL ELEMENTS: {selected_theme['elements']}
ARTISTIC STYLE: {selected_theme['style']}

CONTENT TO DISPLAY (in Chinese characters, must be clear and readable):
{objectives_description}

CRITICAL REQUIREMENTS:
1. Hand-drawn aesthetic with sketch-like quality
2. Include decorative doodles and icons around the edges
3. Use arrows, lines, and connectors to show progression
4. Display Chinese text clearly in a handwritten-style font
5. Show {len(objectives)} distinct levels with visual hierarchy
6. Add small illustrative elements related to learning (books, pencils, lightbulbs, stars, etc.)
7. Use warm, inviting colors (earth tones, pastels, or vintage palette)
8. Include decorative borders or frames
9. Make it look like a teacher's hand-drawn teaching material

LAYOUT STRUCTURE:
- Central focus on the learning progression
- Decorative elements in corners and margins
- Clear visual flow from level 1 to level {len(objectives)}
- Balance between text and illustrations
- Professional yet playful and engaging

TEXT REQUIREMENTS:
- Chinese characters must be legible and well-formed
- Use a style that mimics handwriting but remains clear
- Include level numbers (1, 2, 3...)
- Show the hierarchy level names (识记, 理解, 运用, etc.)

The final image should look like a creative, hand-drawn teaching poster that students would find engaging and memorable!
"""
    
    print(f"  🎨 生成手绘风格学习目标图（主题: {selected_theme['name']}）")
    
    return generate_image(prompt, aspect_ratio="16:9")
