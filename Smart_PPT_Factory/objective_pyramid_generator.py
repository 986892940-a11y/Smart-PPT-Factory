"""
学习目标层级金字塔图生成器
根据学习目标的层级（识记/理解/操作）生成带奖杯的金字塔图
"""
from PIL import Image, ImageDraw, ImageFont
import io

# 层级颜色配置
LEVEL_COLORS = {
    "识记": "#7ED7C1",  # 浅绿色
    "理解": "#00A896",  # 深绿色
    "操作": "#F39C12",  # 橙色
    "运用": "#F39C12",  # 橙色
    "迁移": "#F39C12",  # 橙色
}

# 层级顺序（从上到下）
LEVEL_ORDER = ["识记", "理解", "操作", "运用", "迁移"]


def parse_objective_level(objective_text):
    """
    从学习目标文本中解析层级
    例如: "识记名著拓展题出题形式" -> "识记"
    """
    for level in LEVEL_ORDER:
        if level in objective_text:
            return level
    return "理解"  # 默认为理解


def generate_pyramid_image(objectives, width=800, height=600):
    """
    生成学习目标层级金字塔图
    
    参数:
        objectives: 学习目标列表
        width: 图片宽度
        height: 图片高度
    
    返回:
        BytesIO对象
    """
    # 创建白色背景图片
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 解析每个目标的层级
    levels = []
    for obj in objectives:
        level = parse_objective_level(obj)
        levels.append(level)
    
    # 计算金字塔位置（左侧1/3区域）
    pyramid_left = 50
    pyramid_width = width // 3 - 100
    pyramid_top = 100
    pyramid_height = height - 200
    
    # 绘制奖杯（简化版）
    trophy_center_x = pyramid_left + pyramid_width // 2
    trophy_y = pyramid_top - 80
    
    # 奖杯杯身
    draw.ellipse([trophy_center_x - 40, trophy_y, trophy_center_x + 40, trophy_y + 60], 
                 fill='#FFD700', outline='#FFA500', width=3)
    
    # 奖杯把手（左）
    draw.arc([trophy_center_x - 60, trophy_y + 10, trophy_center_x - 30, trophy_y + 40], 
             start=90, end=270, fill='#FFD700', width=5)
    
    # 奖杯把手（右）
    draw.arc([trophy_center_x + 30, trophy_y + 10, trophy_center_x + 60, trophy_y + 40], 
             start=270, end=90, fill='#FFD700', width=5)
    
    # 奖杯底座
    draw.rectangle([trophy_center_x - 50, trophy_y + 60, trophy_center_x + 50, trophy_y + 80], 
                   fill='#FFD700', outline='#FFA500', width=2)
    
    # 奖杯上的"1"
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
    except:
        font_large = ImageFont.load_default()
    
    draw.text((trophy_center_x, trophy_y + 30), "1", fill='white', 
              font=font_large, anchor="mm")
    
    # 绘制金字塔层级
    num_levels = len(objectives)
    layer_height = pyramid_height // num_levels
    
    for i, (obj, level) in enumerate(zip(objectives, levels)):
        # 计算梯形的位置
        y_top = pyramid_top + i * layer_height
        y_bottom = y_top + layer_height - 10  # 留10px间隙
        
        # 梯形宽度（从上到下逐渐变宽）
        top_width_ratio = 0.4 + (i * 0.3)
        bottom_width_ratio = 0.4 + ((i + 1) * 0.3)
        
        top_width = pyramid_width * top_width_ratio
        bottom_width = pyramid_width * bottom_width_ratio
        
        # 计算梯形四个顶点
        x_center = pyramid_left + pyramid_width // 2
        
        points = [
            (x_center - top_width // 2, y_top),      # 左上
            (x_center + top_width // 2, y_top),      # 右上
            (x_center + bottom_width // 2, y_bottom), # 右下
            (x_center - bottom_width // 2, y_bottom)  # 左下
        ]
        
        # 获取颜色
        color = LEVEL_COLORS.get(level, "#00A896")
        
        # 绘制梯形
        draw.polygon(points, fill=color, outline='white', width=3)
        
        # 在梯形上写层级编号和名称
        try:
            font_medium = ImageFont.truetype("arial.ttf", 28)
        except:
            font_medium = ImageFont.load_default()
        
        text = f"{i+1} {level}"
        text_y = (y_top + y_bottom) // 2
        draw.text((x_center, text_y), text, fill='white', 
                  font=font_medium, anchor="mm")
    
    # 在右侧绘制目标文本（与层级对齐）
    text_left = pyramid_left + pyramid_width + 80
    
    try:
        font_text = ImageFont.truetype("msyh.ttc", 24)  # 微软雅黑
    except:
        try:
            font_text = ImageFont.truetype("simhei.ttf", 24)  # 黑体
        except:
            font_text = ImageFont.load_default()
    
    for i, obj in enumerate(objectives):
        y_top = pyramid_top + i * layer_height
        y_bottom = y_top + layer_height - 10
        text_y = (y_top + y_bottom) // 2
        
        # 绘制连接线（虚线效果）
        line_start_x = pyramid_left + pyramid_width + 20
        line_end_x = text_left - 20
        
        # 绘制虚线
        for x in range(line_start_x, line_end_x, 15):
            draw.line([(x, text_y), (min(x + 10, line_end_x), text_y)], 
                     fill='#CCCCCC', width=2)
        
        # 绘制圆点
        draw.ellipse([line_end_x - 5, text_y - 5, line_end_x + 5, text_y + 5], 
                    fill=LEVEL_COLORS.get(levels[i], "#00A896"))
        
        # 绘制文字（去掉层级标识）
        clean_text = obj
        for level in LEVEL_ORDER:
            clean_text = clean_text.replace(level, "").strip()
        
        draw.text((text_left, text_y), clean_text, fill='#333333', 
                  font=font_text, anchor="lm")
    
    # 保存到BytesIO
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    
    return output


if __name__ == "__main__":
    # 测试
    test_objectives = [
        "识记名著拓展题出题形式",
        "理解《乡土中国》《红楼梦》相关概念",
        "运用答题思路，解答名著拓展分析题"
    ]
    
    img_stream = generate_pyramid_image(test_objectives)
    
    # 保存测试图片
    with open("Smart_PPT_Factory/data/test_pyramid.png", "wb") as f:
        f.write(img_stream.getvalue())
    
    print("✅ 测试图片已生成: Smart_PPT_Factory/data/test_pyramid.png")
