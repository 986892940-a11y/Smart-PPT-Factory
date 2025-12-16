# Smart PPT Factory - 智能PPT讲义生成器

基于AI的自动化教学讲义生成系统，支持从PDF提取内容并生成完整的PPT课件。

## ✨ 核心特性

- 🤖 **AI驱动**: 使用Google Gemini 2.0 Flash进行内容提取，Imagen 4 Fast生成配图
- 📄 **PDF解析**: 自动从PDF文件提取课程内容和结构
- 🎨 **智能配图**: 根据内容自动生成相关的AI图片
- 📐 **模板化**: 使用统一的PPT母版，保持格式一致性
- 🔄 **知识点循环**: 智能处理多个知识点的重复结构
- 🎯 **占位符保留**: 保持原有文字格式、颜色、字体

## 🚀 快速开始

### 1. 环境配置

```bash
# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp .env.example .env
# 编辑.env文件，填入你的GOOGLE_API_KEY
```

### 2. 准备输入文件

将待制作的PDF讲义放入 `data/` 目录，文件名格式：
```
高中语文_高一_2025寒假_小组课_张三.pdf
```

### 3. 运行生成流程

```bash
# 步骤1: 从PDF提取内容
python Smart_PPT_Factory/parser.py

# 步骤2: 生成PPT
python Smart_PPT_Factory/main.py
```

生成的PPT位于：`Smart_PPT_Factory/output/Final_Courseware_*.pptx`

## 📁 项目结构

```
Smart_PPT_Factory/
├── main.py                    # 主程序 - PPT生成器
├── parser.py                  # PDF内容解析器
├── slide_builder.py           # 幻灯片构建器
├── ai_image_generator.py      # AI图片生成模块
├── config.py                  # 配置文件
├── utils.py                   # 工具函数
├── requirements.txt           # Python依赖
├── .env                       # 环境变量（API密钥）
├── .env.example               # 环境变量示例
├── 工作流程说明.md            # 详细工作流程文档
├── data/                      # 数据目录
│   ├── course.json            # 提取的课程数据
│   ├── raw_content.txt        # PDF原始文本
│   └── *.pdf                  # 源PDF文件
├── assets/                    # 素材目录
│   └── master_template.pptx   # PPT母版模板（18个布局）
└── output/                    # 输出目录
    └── Final_Courseware_*.pptx # 生成的PPT
```

## 📝 数据格式

### PDF文件命名规则

```
{科目}_{年级}_{学期}_{课程类型}_{教师}.pdf
例如: 高中语文_高一_2025寒假_小组课_张三.pdf
```

系统会自动解析文件名生成封面信息。

### course.json 结构

由 `parser.py` 自动生成，包含：

```json
{
  "lecture_title": "讲义标题",
  "learning_objectives": ["目标1", "目标2", "目标3"],
  "class_intro": "课程导入",
  "exam_analysis": "考情分析",
  "knowledge_points": [
    {
      "title": "知识点标题",
      "content": "知识点内容",
      "discussion": "讨论问题（可选）",
      "example_mother": "母题（可选）",
      "example_variant": "变式练习（可选）",
      "method": "解题方法（可选）"
    }
  ],
  "quiz_content": "出门测内容（可选）",
  "homework": "课后作业"
}
```

## 🎯 PPT生成流程

### 第一部分：开场（5页）
1. **封面** - 根据PDF文件名生成，带季节背景图（春/夏/秋/冬）
2. **课程体系** - 展示课程整体框架
3. **讲义标题** - 本节课主题（带AI配图）
4. **学习目标** - 3个学习目标（带AI配图）
5. **考情分析** - 考试情况说明

### 第二部分：知识点循环（每个知识点4-5页）

**对于每个知识点，重复以下结构：**

1. **知识点切片标题** - 知识点名称（带AI配图）
2. **知识点内容** - 详细讲解（带AI配图）
3. **开口说** - 互动讨论（仅第一个知识点后出现）
4. **经典例题（母题）** - 典型题目
5. **经典例题（变式/方法）** - 变式练习和解题方法

### 第三部分：结束（6页）
1. **上台讲** - 学生展示环节（所有知识点完成后）
2. **课堂总结过渡** - 总结引导页
3. **课堂总结内容** - 重点回顾（带AI配图）
4. **出门测过渡** - 测试引导页
5. **出门测计时** - 测试题目
6. **作业布置** - 课后任务
7. **告别** - 结束页

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
GOOGLE_API_KEY=your_api_key_here
```

### 配置文件 (config.py)

```python
# AI模型配置
TEXT_MODEL = "gemini-2.0-flash-exp"        # 文本生成模型
IMAGE_MODEL = "imagen-4.0-fast-generate-001"  # 图片生成模型

# 路径配置
MASTER_TEMPLATE = "Smart_PPT_Factory/assets/master_template.pptx"  # PPT模板
JSON_PATH = "Smart_PPT_Factory/data/course.json"                   # 课程数据
PDF_DIR = "Smart_PPT_Factory/data"                                 # PDF目录
OUTPUT_PATH = "Smart_PPT_Factory/output/Final_Courseware_*.pptx"   # 输出路径
```

## 🎨 AI图片生成

系统会在以下位置自动生成AI配图：

1. **封面背景** - 根据季节（春/夏/秋/冬）生成淡雅背景，不遮挡中间文字
2. **讲义标题** - 与标题内容相关的装饰图
3. **学习目标** - 辅助理解的示意图
4. **知识点切片** - 每个知识点的配图
5. **知识点内容** - 知识点详解配图
6. **课堂总结** - 总结思维导图

所有图片都会自动填充到PPT模板的图片占位符中。

## 📐 PPT模板布局

使用 `assets/master_template.pptx` 中的18个布局：

| 布局ID | 名称 | 说明 |
|--------|------|------|
| 0 | Cover_Layout | 封面（4个占位符）|
| 1 | 课程体系 | 课程框架展示 |
| 2 | 讲义标题 | 带图片占位符 |
| 3 | 学习目标 | 带图片占位符 |
| 4 | 学习目标思维导图 | 纯图片 |
| 5 | 考情 | 考试分析 |
| 6 | 知识点切片标题 | 带图片占位符 |
| 7 | 知识点 | 带图片占位符 |
| 8 | 开口说 | 互动讨论 |
| 9 | 经典例题母题 | 典型题目 |
| 10 | 经典例题变式 | 变式练习 |
| 11 | 上台讲 | 学生展示 |
| 12 | 课堂总结过渡 | 总结引导 |
| 13 | 课堂总结内容 | 带图片占位符 |
| 14 | 出门测过渡 | 测试引导 |
| 15 | 出门测计时 | 测试题目 |
| 16 | 作业布置 | 课后任务 |
| 17 | 告别 | 结束页 |

## 🔧 技术栈

- **Python 3.x**
- **python-pptx** - PPT文件操作
- **PyMuPDF (fitz)** - PDF文本提取
- **Google Generative AI** - AI内容生成和图片生成
- **python-dotenv** - 环境变量管理

## 📋 注意事项

1. **API配额**: 图片生成会消耗Google AI配额，请注意使用量
2. **文件命名**: PDF文件名必须符合规范格式才能正确解析封面信息
3. **模板修改**: 如需修改PPT样式，请编辑 `assets/master_template.pptx`
4. **占位符格式**: 系统会保留模板中占位符的原有格式（字体、颜色、大小）

## 🐛 问题反馈

如果生成的PPT有任何问题，请提供：
- 输入的PDF文件
- 生成的course.json
- 具体的问题描述

## 📄 许可证

MIT License
