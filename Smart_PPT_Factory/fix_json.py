"""
手动修复course.json
"""
import json

# 手动创建正确的数据结构
data = {
    "lecture_title": "社科文-名著拓展分析《红楼梦》《乡土中国》",
    "learning_objectives": [
        "识记名著拓展题出题形式",
        "理解《乡土中国》《红楼梦》相关概念",
        "运用答题思路，解答名著拓展分析题"
    ],
    "class_intro": "通过高中语文的学习，相信大家对《红楼梦》《乡土中国》原著并不陌生了，那么今天我们来一起看看，它是如何与社科文结合进行考查的。",
    "exam_analysis": "本讲知识点在高考中的考查方式主要为结合《乡土中国》《红楼梦》重点概念和情节，对文章中的重要论点进行分析；分值一般为4-5分，在社科文板块分值中占比约30%。",
    "knowledge_points": [
        {
            "title": "名著拓展题考查形式",
            "content": "名著拓展题主要考查形式包括：\n1. 结合名著内容分析文章论点\n2. 联系名著情节理解文章观点\n3. 运用名著概念解读社科文内容",
            "discussion": "请思考：《红楼梦》和《乡土中国》中哪些概念和情节可以用来分析社科文？",
            "example_mother": "示例题目：请结合《乡土中国》中的相关概念，分析文中关于社会关系的论述。",
            "example_variant": "变式练习：请联系《红楼梦》中的人物关系，理解文中关于人际交往的观点。",
            "method": "答题方法：\n1. 准确理解名著概念\n2. 找到文章对应论点\n3. 建立两者联系\n4. 组织答案表述"
        },
        {
            "title": "名著拓展分析题答题思路",
            "content": "答题思路：\n1. 审题：明确题目要求\n2. 定位：找到名著相关内容\n3. 分析：建立名著与文章的联系\n4. 表述：组织规范答案",
            "discussion": None,
            "example_mother": "智媒时代的隐私困境相关题目",
            "example_variant": None,
            "method": "本题考查学生语句复位的能力。需要理解《乡土中国》中圈子的概念，并与文章内容建立联系。"
        }
    ],
    "quiz_content": "请完成讲义上的名著拓展分析练习题",
    "homework": "1. 复习《红楼梦》《乡土中国》重点概念\n2. 完成课后练习题\n3. 总结名著拓展题答题方法",
    "extracted_images": [
        {
            "filename": "mindmap.jpeg",
            "path": "Smart_PPT_Factory/data/extracted_images/mindmap.jpeg",
            "is_mindmap": True
        }
    ]
}

# 保存为JSON
with open('Smart_PPT_Factory/data/course.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ course.json 已修复并保存！")
