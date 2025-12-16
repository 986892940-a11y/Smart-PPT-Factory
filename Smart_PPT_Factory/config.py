import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API 配置
API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not API_KEY:
    raise ValueError("请在 .env 文件中设置 GOOGLE_API_KEY")

# 模型配置
TEXT_MODEL = "gemini-2.0-flash-exp"
IMAGE_MODEL = "imagen-4.0-fast-generate-001"  # Imagen 4 Fast (快速稳定)
# IMAGE_MODEL = "gemini-3-pro-image-preview"  # Nano Banana Pro (可选，生成较慢)

# 路径配置
JSON_PATH = "Smart_PPT_Factory/data/course.json"
import time
OUTPUT_PATH = f"Smart_PPT_Factory/output/Final_Courseware_{int(time.time())}.pptx"
MASTER_TEMPLATE = "Smart_PPT_Factory/assets/master_template.pptx"  # 合并后的统一模板
ASSET_DIR = "Smart_PPT_Factory/assets"
PDF_DIR = "Smart_PPT_Factory/data"
INPUT_FILE = "Smart_PPT_Factory/data/raw_content.txt"

# 生成配置
IMAGE_GENERATION_TIMEOUT = 15  # 秒
DEFAULT_SLIDE_WIDTH = 16  # 英寸
DEFAULT_SLIDE_HEIGHT = 9  # 英寸
