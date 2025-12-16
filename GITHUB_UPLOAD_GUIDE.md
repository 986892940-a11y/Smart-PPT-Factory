# GitHub上传指南

## ✅ 已完成的步骤

1. ✅ Git用户配置完成
   - user.name: "PPT-Factory-User"
   - user.email: "ppt.factory@example.com"

2. ✅ Git仓库初始化完成
   - 分支: main
   - 提交: f594c0b "Initial commit: Smart PPT Factory - AI驱动的智能PPT讲义生成系统"
   - 文件数: 19个文件，2968行代码

3. ✅ .gitignore配置完成
   - 已排除敏感文件（.env）
   - 已排除输出文件和临时文件

## 📋 接下来的步骤

### 1. 在GitHub上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `Smart-PPT-Factory` （或你喜欢的名字）
   - **Description**: `AI驱动的智能PPT讲义生成系统 - 自动从PDF提取内容并生成完整的教学课件`
   - **Visibility**: 选择 Public 或 Private
   - **⚠️ 重要**: 不要勾选 "Add a README file"、"Add .gitignore"、"Choose a license"（我们已经有这些文件了）
3. 点击 "Create repository"

### 2. 连接本地仓库到GitHub

创建仓库后，GitHub会显示一个页面，复制 "…or push an existing repository from the command line" 部分的命令。

在你的项目目录下运行：

```bash
# 添加远程仓库（替换<your-username>为你的GitHub用户名）
git remote add origin https://github.com/<your-username>/Smart-PPT-Factory.git

# 推送代码到GitHub
git push -u origin main
```

### 3. 验证上传

推送成功后：
1. 刷新GitHub仓库页面
2. 你应该能看到所有文件和README.md
3. README.md会自动显示在仓库首页

## 🔐 安全提醒

- ✅ `.env` 文件已被 `.gitignore` 排除，不会上传到GitHub
- ✅ 只有 `.env.example` 会被上传（不包含真实API密钥）
- ⚠️ 确保你的 `.env` 文件中的API密钥安全

## 📝 后续更新

当你修改代码后，使用以下命令更新GitHub仓库：

```bash
# 查看修改的文件
git status

# 添加所有修改
git add .

# 创建提交
git commit -m "描述你的修改"

# 推送到GitHub
git push
```

## 🎯 推荐的提交信息格式

- `feat: 添加新功能` - 新功能
- `fix: 修复bug` - 修复问题
- `docs: 更新文档` - 文档更新
- `style: 代码格式调整` - 格式化
- `refactor: 代码重构` - 重构
- `perf: 性能优化` - 优化
- `test: 添加测试` - 测试

## 📊 项目统计

- **总文件数**: 19个
- **代码行数**: 2968行
- **主要语言**: Python
- **核心模块**: 
  - PDF解析器 (parser.py)
  - PPT生成器 (main.py)
  - AI图片生成 (ai_image_generator.py)
  - 幻灯片构建器 (slide_builder.py)

## 🌟 可选：添加GitHub徽章

在README.md顶部添加徽章（上传后）：

```markdown
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

## 📞 需要帮助？

如果遇到问题：
1. 检查Git配置：`git config --list`
2. 检查远程仓库：`git remote -v`
3. 查看提交历史：`git log --oneline`
4. 查看当前状态：`git status`
