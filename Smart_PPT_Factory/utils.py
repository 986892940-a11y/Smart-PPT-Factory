import os

def parse_filename_to_json(file_path):
    """
    输入：PDF文件路径 (例如: "uploads/高中语文_高一_2025寒假_小组课_张三.pdf")
    输出：用于 PPT 封面的 JSON 字典
    """
    # 1. 获取纯文件名 (去掉路径和 .pdf 后缀)
    filename = os.path.basename(file_path)
    name_body = os.path.splitext(filename)[0] # 得到 "高中语文_高一_2025寒假_小组课_张三"
    
    # 2. 按照下划线切分
    try:
        parts = name_body.split('_')
        
        # 确保文件名里有足够的要素，否则报错
        if len(parts) < 5:
            # 尝试做一个宽容处理，如果有不够的，用默认值填充
            print(f"⚠️ 文件名格式警告: 期望5个要素，实际找到 {len(parts)} 个。将尝试尽可能解析。")
            if len(parts) == 0: raise ValueError("文件名为空")
        
        # 安全获取各个字段 (使用 get_part 辅助函数或简单的列表索引+默认值)
        def get_part(index, default=""):
            return parts[index] if index < len(parts) else default

        raw_subject = get_part(0, "课程")
        grade = get_part(1, "年级")
        semester = get_part(2, "学期")
        class_type = get_part(3, "班型")
        teacher_name = get_part(4, "老师")

        # 智能提取“大标题”
        main_subject_text = raw_subject[-2:] if len(raw_subject) >= 2 else raw_subject
        
        # 预处理学期后缀
        term_suffix = semester[-2:] if len(semester) >= 2 else semester

        # 4. 组装成你需要的 JSON 结构
        cover_data = {
            "page_id": 0,
            "layout_type": "cover_smart",
            
            # small_title: "小组课 · 暑假课堂"
            "small_title": f"{class_type} · {term_suffix}课堂", 
            
            # main_subject: "语文"
            "main_subject": main_subject_text,
            
            # sub_title: "2025寒假高中小组课"
            "sub_title": f"{semester}高中{class_type}",
            
            # grade_info: "高中语文 · 高一"
            "grade_info": f"{raw_subject} · {grade}",
            
            # teacher: "主讲人：张三老师" (自动加上老师二字，如果文件名里已有“老师”则不加)
            "teacher": f"主讲人：{teacher_name}" if "老师" in teacher_name else f"主讲人：{teacher_name}老师",
            
            # 背景词：可以写死白色极简，或者根据科目自动变
            "bg_keywords": "minimalist abstract white background"
        }
        
        print(f"文件名解析成功: {cover_data}")
        return cover_data

    except Exception as e:
        print(f"⚠️ 文件名解析失败: {e}")
        # 返回一个默认的兜底数据，防止程序崩溃
        return {
            "page_id": 0,
            "layout_type": "cover_smart",
            "main_subject": "课程",
            "small_title": "新东方 · 精品课",
            "sub_title": "课程讲义",
            "grade_info": "高中",
            "teacher": "主讲人",
            "bg_keywords": "white background"
        }
