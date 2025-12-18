# 更新日志

## [2025-12-18] - 重大功能更新

### 新增功能 ✨

1. **知识类型智能标签**
   - 使用AI自动判断知识点类型（事实性、概念性、程序性）
   - 为每种类型生成专属的视觉标签图片
   - 自动填充到知识点页左下角
   - 标签图片保存在 `data/extracted_images/` 目录

2. **课堂引入图片优化**
   - AI智能分析课堂引入内容，提取视觉主题
   - 生成纯装饰性配图，不包含文字
   - 中国传统教育美学风格
   - 手绘水彩效果

3. **思维导图页修复**
   - 确保学习目标思维导图页始终生成（第6页）
   - 课堂总结页也使用相同的思维导图
   - 优化路径处理，支持多种路径方式

### 改进 🔧

1. **课堂引入页布局**
   - 修正占位符顺序：标题在上，内容在下
   - 优化文本和图片的位置关系

2. **配置文件优化**
   - 使用绝对路径，支持从任意目录运行
   - 自动检测项目根目录

3. **代码清理**
   - 删除所有测试和临时文件
   - 保留核心功能模块
   - 优化项目结构

### 技术细节 📋

**知识类型判断逻辑：**
- 事实性知识：基本要素、术语、具体细节
- 概念性知识：分类、原理、理论、模型
- 程序性知识：方法、步骤、技能、算法

**标签视觉风格：**
- 事实性知识：绿色，书本图标，"记笔记"
- 概念性知识：蓝色，灯泡图标，"理解"
- 程序性知识：橙色，齿轮图标，"操作"

### 文件结构 📁

```
Smart_PPT_Factory/
├── main.py                    # 主程序
├── parser.py                  # PDF解析器
├── ai_image_generator.py      # AI图片生成（新增知识标签功能）
├── slide_builder.py           # 幻灯片构建器
├── config.py                  # 配置文件（优化路径处理）
├── utils.py                   # 工具函数
├── requirements.txt           # 依赖列表
├── README.md                  # 项目文档
├── 工作流程说明.md            # 工作流程文档
├── data/
│   ├── course.json            # 课程数据
│   └── extracted_images/      # 提取的图片和生成的标签
├── assets/
│   └── master_template.pptx   # PPT模板
└── output/                    # 生成的PPT
```

### 使用方法 🚀

```bash
# 1. 解析PDF
python Smart_PPT_Factory/parser.py

# 2. 生成PPT
python Smart_PPT_Factory/main.py
```

### 依赖要求 📦

- Python 3.x
- python-pptx
- PyMuPDF (fitz)
- Google Generative AI (Gemini)
- python-dotenv
- Pillow

### 配置 ⚙️

在 `.env` 文件中设置：
```
GOOGLE_API_KEY=your_api_key_here
```

---

## [2025-12-17] - 初始版本

### 功能
- PDF内容提取
- AI图片生成
- PPT自动生成
- 多布局支持
