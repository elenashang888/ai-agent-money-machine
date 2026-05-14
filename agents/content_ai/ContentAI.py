#!/usr/bin/env python3
"""
📝 ContentAI - 智能内容创作助手
AI Agent #1: 内容创作助手
功能：爆款标题生成、文章大纲、完整文章、多平台适配、SEO优化
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import re


class ContentAI:
    """
    内容创作AI Agent
    
    核心能力：
    1. 爆款标题生成（10个备选+点击率预估）
    2. 文章大纲生成
    3. 完整文章创作
    4. 多平台内容适配（公众号/小红书/抖音/知乎/B站）
    5. SEO关键词优化
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BAILIAN_API_KEY")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
        # 平台配置
        self.platforms = {
            "wechat": {
                "name": "公众号",
                "max_title": 64,
                "style": "深度干货",
                "structure": "开头钩子+3-5观点+案例+金句+行动号召"
            },
            "xiaohongshu": {
                "name": "小红书",
                "max_title": 20,
                "style": "种草笔记",
                "structure": "痛点+解决方案+使用体验+购买引导"
            },
            "douyin": {
                "name": "抖音",
                "max_title": 30,
                "style": "短视频文案",
                "structure": "黄金3秒+情绪递进+反转+引导互动"
            },
            "zhihu": {
                "name": "知乎",
                "max_title": 50,
                "style": "专业回答",
                "structure": "问题背景+深度分析+数据支撑+结论"
            },
            "bilibili": {
                "name": "B站",
                "max_title": 40,
                "style": "视频脚本",
                "structure": "开场梗+内容展开+整活+求三连"
            }
        }
    
    def _call_api(self, messages: List[Dict], model: str = "qwen-max") -> str:
        """调用百炼API"""
        url = f"{self.base_url}/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "input": {"messages": messages},
            "parameters": {
                "result_format": "message",
                "max_tokens": 4000,
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["output"]["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"❌ API调用失败: {e}")
            return None
    
    def generate_titles(self, topic: str, platform: str = "wechat", count: int = 10) -> List[Dict]:
        """
        生成爆款标题
        
        Args:
            topic: 文章主题
            platform: 目标平台
            count: 生成标题数量
            
        Returns:
            标题列表，包含标题文本、预估点击率、优化建议
        """
        platform_config = self.platforms.get(platform, self.platforms["wechat"])
        
        prompt = f"""你是一个专业的标题党文案大师。请为以下主题生成{count}个爆款标题。

主题：{topic}
平台：{platform_config['name']}
风格要求：{platform_config['style']}

要求：
1. 每个标题都要有独特的角度和切入点
2. 标题要吸引人点击，但不要标题党
3. 包含数字、情绪词、悬念等元素
4. 预估每个标题的点击率（百分比）
5. 给出每个标题的优化建议

请按以下格式输出：
1. [标题文本]
   预估点击率：XX%
   优化建议：...

2. [标题文本]
   ...
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的内容营销专家，擅长撰写爆款标题。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages, model="qwen-turbo")
        if not result:
            return []
        
        return self._parse_titles(result)
    
    def _parse_titles(self, text: str) -> List[Dict]:
        """解析生成的标题"""
        titles = []
        lines = text.strip().split('\n')
        current_title = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 匹配标题行
            if re.match(r'^\d+\.', line):
                if current_title:
                    titles.append(current_title)
                title_text = re.sub(r'^\d+\.', '', line).strip()
                current_title = {"title": title_text, "ctr": "5%", "tips": ""}
            
            # 匹配点击率
            elif "点击率" in line:
                ctr_match = re.search(r'(\d+)%', line)
                if ctr_match:
                    current_title["ctr"] = f"{ctr_match.group(1)}%"
            
            # 匹配建议
            elif "建议" in line:
                current_title["tips"] = line.split("：")[-1].strip()
        
        if current_title:
            titles.append(current_title)
        
        return titles
    
    def generate_outline(self, title: str, topic: str, platform: str = "wechat") -> Dict:
        """
        生成文章大纲
        
        Args:
            title: 选定的标题
            topic: 文章主题
            platform: 目标平台
            
        Returns:
            大纲结构，包含引言、章节、关键词等
        """
        platform_config = self.platforms.get(platform, self.platforms["wechat"])
        
        prompt = f"""请为以下文章生成详细的大纲。

标题：{title}
主题：{topic}
平台：{platform_config['name']}
结构要求：{platform_config['structure']}

请提供：
1. 引言（钩子设计）
2. 3-5个核心章节，每个章节包含：
   - 章节标题
   - 核心论点
   - 案例/数据建议
3. 结尾（行动号召）
4. 关键词（5-10个）

输出格式：
## 引言
...

## 章节1: [标题]
- 核心论点：...
- 案例建议：...

## 关键词
keyword1, keyword2, ...
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的内容策划专家。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages, model="qwen-plus")
        
        # 解析大纲
        outline = {
            "title": title,
            "topic": topic,
            "platform": platform,
            "content": result or "生成失败",
            "sections": [],
            "keywords": []
        }
        
        # 提取章节
        section_pattern = r'##\s*章节\d+[:：]\s*(.+?)(?=##|$)'
        sections = re.findall(section_pattern, result, re.DOTALL)
        outline["sections"] = [s.strip() for s in sections]
        
        # 提取关键词
        keyword_match = re.search(r'##\s*关键词\s*\n(.+)', result, re.DOTALL)
        if keyword_match:
            keywords_text = keyword_match.group(1)
            outline["keywords"] = [k.strip() for k in keywords_text.split(',')]
        
        return outline
    
    def generate_article(self, title: str, outline: Dict, platform: str = "wechat") -> str:
        """
        生成完整文章
        
        Args:
            title: 文章标题
            outline: 文章大纲
            platform: 目标平台
            
        Returns:
            完整文章内容
        """
        platform_config = self.platforms.get(platform, self.platforms["wechat"])
        
        prompt = f"""请根据以下大纲生成一篇完整的文章。

标题：{title}
平台：{platform_config['name']}
风格：{platform_config['style']}

大纲：
{outline.get('content', '')}

写作要求：
1. 开头要吸引人，使用钩子技巧
2. 内容要有深度，提供真实价值
3. 使用短段落，每段不超过3行
4. 适当使用emoji和排版符号
5. 加入金句和案例
6. 结尾要有行动号召
7. 确保原创性

请直接输出文章内容。
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的撰稿人。"},
            {"role": "user", "content": prompt}
        ]
        
        return self._call_api(messages, model="qwen-max") or "生成失败"
    
    def optimize_seo(self, article: str, keywords: List[str]) -> Dict:
        """
        SEO优化分析
        
        Args:
            article: 文章内容
            keywords: 目标关键词
            
        Returns:
            SEO分析结果和建议
        """
        prompt = f"""请对以下文章进行SEO分析。

文章内容：
{article[:3000]}

目标关键词：{', '.join(keywords)}

请提供：
1. 关键词密度分析
2. 标题优化建议
3. 元描述建议
4. 可读性评分（1-10）
5. 具体改进建议

输出格式：
## 关键词密度
...

## 标题优化
...

## 元描述建议
...

## 可读性评分
...

## 改进建议
...
"""
        
        messages = [
            {"role": "system", "content": "你是一个SEO优化专家。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages, model="qwen-plus")
        
        return {
            "analysis": result or "分析失败",
            "keywords": keywords,
            "word_count": len(article)
        }
    
    def adapt_platform(self, article: str, from_platform: str, to_platform: str) -> str:
        """
        跨平台内容适配
        
        Args:
            article: 原文
            from_platform: 来源平台
            to_platform: 目标平台
            
        Returns:
            适配后的内容
        """
        from_config = self.platforms.get(from_platform, self.platforms["wechat"])
        to_config = self.platforms.get(to_platform, self.platforms["wechat"])
        
        prompt = f"""请将以下文章从{from_config['name']}风格改写为{to_config['name']}风格。

原文：
{article}

来源风格：{from_config['style']}
目标风格：{to_config['style']}
目标结构：{to_config['structure']}

改写要求：
1. 保持核心内容不变
2. 调整语言风格以适配目标平台
3. 优化排版格式
4. 添加平台特色元素（如emoji、标签等）
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的内容改写专家。"},
            {"role": "user", "content": prompt}
        ]
        
        return self._call_api(messages, model="qwen-plus") or "改写失败"
    
    def create_content_package(self, topic: str, platform: str = "wechat") -> Dict:
        """
        完整内容创作流程
        
        Args:
            topic: 主题
            platform: 平台
            
        Returns:
            完整内容包
        """
        print(f"🚀 ContentAI 开始创作: {topic}")
        
        # 1. 生成标题
        print("\n📝 生成爆款标题...")
        titles = self.generate_titles(topic, platform, 10)
        best_title = max(titles, key=lambda x: int(x.get("ctr", "0%").replace("%", "")))
        print(f"✅ 生成 {len(titles)} 个标题，最佳: {best_title['title']}")
        
        # 2. 生成大纲
        print("\n📋 生成文章大纲...")
        outline = self.generate_outline(best_title['title'], topic, platform)
        print(f"✅ 大纲生成完成，{len(outline.get('sections', []))} 个章节")
        
        # 3. 生成文章
        print("\n✍️ 生成完整文章...")
        article = self.generate_article(best_title['title'], outline, platform)
        print(f"✅ 文章生成完成，{len(article)} 字")
        
        # 4. SEO优化
        print("\n🔍 SEO优化分析...")
        seo = self.optimize_seo(article, outline.get('keywords', []))
        print(f"✅ SEO分析完成")
        
        package = {
            "topic": topic,
            "platform": platform,
            "created_at": datetime.now().isoformat(),
            "titles": titles,
            "selected_title": best_title,
            "outline": outline,
            "article": article,
            "seo": seo,
            "word_count": len(article)
        }
        
        print("\n🎉 ContentAI 创作完成！")
        return package
    
    def save_package(self, package: Dict, output_dir: str = "./output"):
        """保存内容包到文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ContentAI_{timestamp}_{package['topic'][:15]}.md"
        filepath = os.path.join(output_dir, filename)
        
        md_content = f"""# {package['selected_title']['title']}

> **ContentAI 智能创作**
> 主题：{package['topic']}
> 平台：{package['platform']}
> 字数：{package['word_count']}
> 生成时间：{package['created_at']}

---

## 📊 标题选择

**最佳标题：** {package['selected_title']['title']}
- 预估点击率：{package['selected_title']['ctr']}
- 优化建议：{package['selected_title']['tips']}

### 备选标题

"""
        
        for i, title in enumerate(package['titles'], 1):
            md_content += f"{i}. {title['title']} (预估点击率：{title['ctr']})\n"
        
        md_content += f"""

---

## 📋 文章大纲

{package['outline']['content']}

---

## 📝 正文

{package['article']}

---

## 🔍 SEO分析

{package['seo']['analysis']}

---

*Generated by ContentAI - AI Agent #1*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"💾 内容已保存: {filepath}")
        return filepath


# 使用示例
if __name__ == "__main__":
    # 初始化
    agent = ContentAI()
    
    # 创建内容
    package = agent.create_content_package(
        topic="AI如何帮助普通人赚钱",
        platform="wechat"
    )
    
    # 保存
    agent.save_package(package)
