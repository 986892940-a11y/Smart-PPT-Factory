import os
import time
from dotenv import load_dotenv

# 获取项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "Smart_PPT_Factory" else SCRIPT_DIR

# 加载环境变量
env_path = os.path.join(SCRIPT_DIR, ".env")
load_dotenv(env_path)

# API 配置
API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not API_KEY:
    raise ValueError("请在 .env 文件中设置 GOOGLE_API_KEY")

# 模型配置
TEXT_MODEL = "gemini-2.0-flash-exp"
IMAGE_MODEL = "gemini-3-pro-image-preview"  # Gemini 3 Pro Image (中文支持最好)

# 路径配置 - 使用绝对路径
JSON_PATH = os.path.join(SCRIPT_DIR, "data", "course.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "output", f"Final_Courseware_{int(time.time())}.pptx")
MASTER_TEMPLATE = os.path.join(SCRIPT_DIR, "assets", "master_template.pptx")
ASSET_DIR = os.path.join(SCRIPT_DIR, "assets")
PDF_DIR = os.path.join(SCRIPT_DIR, "data")
INPUT_FILE = os.path.join(SCRIPT_DIR, "data", "raw_content.txt")

# 生成配置
IMAGE_GENERATION_TIMEOUT = 15  # 秒
DEFAULT_SLIDE_WIDTH = 16  # 英寸
DEFAULT_SLIDE_HEIGHT = 9  # 英寸
