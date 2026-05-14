#!/usr/bin/env python3
"""
AI内容生成器 - 支持模拟模式演示
"""

import os
import sys
import json
from datetime import datetime

# 模拟数据生成器
class MockGenerator:
    """模拟生成器（当API不可用时使用）"""
    
    def generate_titles(self, topic, platform, count=5):
        templates = {
            "wechat": [
                {"title": f"深度解析：{topic}的5个核心秘诀", "ctr": "8.5%", "tips": "数字+干货，适合公众号"},
                {"title": f"为什么90%的人不懂{topic}？看完这篇你就赢了", "ctr": "12.3%", "tips": "悬念+数字，引发好奇"},
                {"title": f"{topic}完全指南：从入门到精通的实战手册", "ctr": "7.2%", "tips": "完整指南型，适合收藏"},
                {"title": f"我用{topic}月入3万的真实经历", "ctr": "15.8%", "tips": "真实案例+收入数字"},
                {"title": f"{topic}避坑指南：这7个错误千万别犯", "ctr": "9.6%", "tips": "避坑型，实用性强"},
            ],
            "xiaohongshu": [
                {"title": f"✨{topic}真的太香了！姐妹们快冲", "ctr": "18.2%", "tips": "emoji+口语化"},
                {"title": f"被问爆的{topic}方法🔥亲测有效", "ctr": "14.5%", "tips": "社交证明+emoji"},
                {"title": f"{topic}小白必看💯手把手教你入门", "ctr": "11.3%", "tips": "小白友好型"},
            ],
            "douyin": [
                {"title": f"{topic}？看完这个视频你就懂了", "ctr": "22.1%", "tips": "悬念+短平快"},
                {"title": f"99%的人不知道的{topic}秘密", "ctr": "19.8%", "tips": "数字+秘密"},
            ],
            "zhihu": [
                {"title": f"如何系统学习{topic}？", "ctr": "6.5%", "tips": "问题导向"},
                {"title": f"{topic}的本质是什么？", "ctr": "7.8%", "tips": "深度思考型"},
            ],
            "bilibili": [
                {"title": f"【硬核】{topic}全攻略，看完直接起飞", "ctr": "13.4%", "tips": "硬核+玩梗"},
                {"title": f"{topic}？我整了个大活", "ctr": "16.7%", "tips": "整活型"},
            ]
        }
        return templates.get(platform, templates["wechat"])[:count]
    
    def generate_outline(self, topic, platform):
        return {
            "introduction": f"介绍{topic}的背景和重要性",
            "sections": [
                {"title": "什么是" + topic, "points": ["定义", "核心概念", "发展历程"]},
                {"title": "为什么需要" + topic, "points": ["痛点分析", "市场需求", "个人价值"]},
                {"title": "如何开始" + topic, "points": ["入门步骤", "工具推荐", "避坑指南"]},
                {"title": "实战案例", "points": ["成功案例", "数据分析", "经验总结"]},
            ],
            "conclusion": f"总结{topic}的关键要点，给出行动建议"
        }
    
    def generate_content(self, topic, platform):
        return f"""
# {topic}完全指南

## 引言
在这个AI快速发展的时代，{topic}已经成为越来越多人关注的话题。本文将为你详细解析...

## 什么是{topic}
{topic}是指...

### 核心概念
- 概念一：...
- 概念二：...

## 为什么{topic}很重要
1. **市场需求大**：...
2. **入门门槛低**：...
3. **变现路径清晰**：...

## 如何开始
### 第一步：准备工作
...

### 第二步：实战操作
...

### 第三步：优化迭代
...

## 成功案例
某用户通过{topic}，在3个月内实现了...

## 总结
{topic}是一个值得投入的领域，关键是...

---
*本文生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    
    def generate_tags(self, topic, platform):
        base_tags = [topic, "AI", "赚钱", "副业", "干货"]
        platform_tags = {
            "wechat": ["公众号", "深度好文", "职场"],
            "xiaohongshu": ["种草", "必看", "推荐"],
            "douyin": ["热门", "爆款", "必看"],
            "zhihu": ["经验", "方法", "攻略"],
            "bilibili": ["教程", "干货", "分享"]
        }
        return base_tags + platform_tags.get(platform, [])

def main():
    print("🚀 AI内容生成器（模拟模式）")
    print("-" * 50)
    
    # 获取参数
    if len(sys.argv) >= 3:
        topic = sys.argv[1]
        platform = sys.argv[2]
    else:
        topic = input("📝 请输入主题：") or "AI Agent赚钱"
        platform = input("📱 请选择平台 (wechat/xiaohongshu/douyin/zhihu/bilibili)：") or "wechat"
    
    print(f"\n主题：{topic}")
    print(f"平台：{platform}")
    print("-" * 50)
    
    # 使用模拟生成器
    generator = MockGenerator()
    
    # 1. 生成标题
    print("\n🎯 生成爆款标题...")
    titles = generator.generate_titles(topic, platform)
    for i, t in enumerate(titles, 1):
        print(f"  {i}. {t['title']}")
        print(f"     预估点击率: {t['ctr']} | 建议: {t['tips']}")
    
    # 2. 生成大纲
    print("\n📋 生成文章大纲...")
    outline = generator.generate_outline(topic, platform)
    print(f"  引言: {outline['introduction']}")
    for section in outline['sections']:
        print(f"  - {section['title']}")
    
    # 3. 生成正文
    print("\n✍️ 生成正文内容...")
    content = generator.generate_content(topic, platform)
    
    # 4. 生成标签
    print("\n🏷️ 生成推荐标签...")
    tags = generator.generate_tags(topic, platform)
    print(f"  {' '.join(['#' + t for t in tags])}")
    
    # 保存文件
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{platform}_{topic.replace(' ', '_')[:20]}_{datetime.now().strftime('%m%d_%H%M')}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 内容已保存到: {filepath}")
    print("\n💡 提示：这是模拟模式，使用预设模板生成内容")
    print("   配置有效API Key后可调用真实AI生成")

if __name__ == "__main__":
    main()
