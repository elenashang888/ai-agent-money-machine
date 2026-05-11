#!/usr/bin/env python3
"""
ContentAI - AI内容创作助手
自动生成文章、视频脚本、社媒文案
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
import openai

class ContentAI:
    """
    ContentAI - 智能内容创作助手
    
    功能：
    1. 自动生成文章（公众号、知乎、今日头条等）
    2. 生成视频脚本（抖音、B站、视频号等）
    3. 改写社媒文案（小红书、微博等）
    4. SEO优化建议
    5. 多平台内容分发
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化ContentAI"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key)
        self.output_dir = os.path.expanduser("~/content-output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 内容模板库
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """加载内容模板"""
        return {
            "wechat": {
                "style": "深度长文，专业有温度",
                "structure": ["钩子", "痛点", "解决方案", "案例", "行动指南", "结尾"],
                "tone": "亲切、专业",
                "emoji": False
            },
            "xiaohongshu": {
                "style": "清单式，emoji丰富",
                "structure": ["封面", "要点", "互动", "标签"],
                "tone": "亲切、种草",
                "emoji": True
            },
            "douyin": {
                "style": "短视频脚本，黄金3秒",
                "structure": ["钩子", "痛点", "方案", "效果", "CTA"],
                "tone": "快节奏、情绪化",
                "emoji": False
            },
            "zhihu": {
                "style": "专业问答，数据支撑",
                "structure": ["结论", "分析", "方法论", "案例", "总结"],
                "tone": "理性、深度",
                "emoji": False
            },
            "toutiao": {
                "style": "资讯式，段落短",
                "structure": ["导语", "正文", "总结"],
                "tone": "客观、信息量大",
                "emoji": False
            }
        }
    
    async def generate_article(
        self,
        topic: str,
        platform: str,
        word_count: int = 2000,
        style: Optional[str] = None
    ) -> Dict:
        """
        生成文章
        
        Args:
            topic: 文章主题
            platform: 目标平台 (wechat/zhihu/toutiao)
            word_count: 字数要求
            style: 自定义风格
            
        Returns:
            包含标题、正文、标签的字典
        """
        template = self.templates.get(platform, self.templates["wechat"])
        
        prompt = f"""
        请为{platform}平台生成一篇关于"{topic}"的文章。
        
        要求：
        - 字数：{word_count}字左右
        - 风格：{template['style']}
        - 结构：{' -> '.join(template['structure'])}
        - 语气：{template['tone']}
        - Emoji：{'使用' if template['emoji'] else '不使用'}
        
        请输出：
        1. 标题（吸引人的标题）
        2. 正文（完整文章内容）
        3. 标签（5-8个相关标签）
        4. 摘要（100字以内）
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一位专业的内容创作专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # 解析结果
            result = self._parse_article(content)
            result["platform"] = platform
            result["topic"] = topic
            result["created_at"] = datetime.now().isoformat()
            
            # 保存到文件
            await self._save_content(result)
            
            return result
            
        except Exception as e:
            return {"error": str(e), "platform": platform, "topic": topic}
    
    async def generate_video_script(
        self,
        topic: str,
        platform: str,
        duration: int = 60
    ) -> Dict:
        """
        生成视频脚本
        
        Args:
            topic: 视频主题
            platform: 平台 (douyin/bilibili/channels)
            duration: 时长（秒）
            
        Returns:
            包含脚本、分镜、字幕的字典
        """
        template = self.templates.get(platform, self.templates["douyin"])
        
        prompt = f"""
        请为{platform}平台生成一个{duration}秒的视频脚本，主题是"{topic}"。
        
        要求：
        - 平台特点：{template['style']}
        - 包含：时间轴、画面描述、台词、字幕、BGM建议
        - 黄金3秒必须有吸引力
        - 结尾有明确的CTA
        
        请按以下格式输出：
        
        ## 视频信息
        - 主题：{topic}
        - 时长：{duration}秒
        - 平台：{platform}
        
        ## 分镜脚本
        [时间] [画面] [台词] [字幕] [BGM]
        
        ## 拍摄要求
        
        ## 剪辑建议
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一位专业的短视频编导。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            
            result = {
                "type": "video_script",
                "platform": platform,
                "topic": topic,
                "duration": duration,
                "script": content,
                "created_at": datetime.now().isoformat()
            }
            
            await self._save_content(result)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    async def rewrite_for_platforms(
        self,
        source_content: str,
        platforms: List[str]
    ) -> Dict[str, Dict]:
        """
        将内容改写为多个平台格式
        
        Args:
            source_content: 原始内容
            platforms: 目标平台列表
            
        Returns:
            各平台改写结果
        """
        results = {}
        
        for platform in platforms:
            template = self.templates.get(platform, self.templates["wechat"])
            
            prompt = f"""
            请将以下内容改写为{platform}平台的格式。
            
            原始内容：
            {source_content[:1000]}...
            
            平台要求：
            - 风格：{template['style']}
            - 结构：{' -> '.join(template['structure'])}
            - 语气：{template['tone']}
            
            请直接输出改写后的内容。
            """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "你是一位专业的内容改写专家。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                
                results[platform] = {
                    "content": response.choices[0].message.content,
                    "platform": platform,
                    "created_at": datetime.now().isoformat()
                }
                
            except Exception as e:
                results[platform] = {"error": str(e)}
        
        # 保存所有结果
        await self._save_content({
            "type": "multi_platform",
            "results": results,
            "created_at": datetime.now().isoformat()
        })
        
        return results
    
    def _parse_article(self, content: str) -> Dict:
        """解析生成的文章"""
        lines = content.split('\n')
        
        title = ""
        body = ""
        tags = []
        summary = ""
        
        current_section = None
        
        for line in lines:
            if "标题" in line or line.startswith("# "):
                title = line.replace("标题：", "").replace("# ", "").strip()
            elif "标签" in line:
                current_section = "tags"
            elif "摘要" in line:
                current_section = "summary"
            elif current_section == "tags":
                tags = [t.strip() for t in line.replace("#", "").split(",") if t.strip()]
            elif current_section == "summary":
                summary += line
            else:
                body += line + "\n"
        
        return {
            "title": title,
            "content": body.strip(),
            "tags": tags,
            "summary": summary.strip()
        }
    
    async def _save_content(self, content: Dict):
        """保存内容到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform = content.get("platform", "general")
        topic = content.get("topic", "untitled")[:20]
        
        filename = f"{platform}_{topic}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 内容已保存: {filepath}")
    
    async def generate_content_calendar(
        self,
        topics: List[str],
        days: int = 7
    ) -> Dict:
        """
        生成内容日历
        
        Args:
            topics: 主题列表
            days: 天数
            
        Returns:
            内容日历
        """
        calendar = {}
        
        for i, topic in enumerate(topics[:days]):
            date = (datetime.now() + __import__('datetime').timedelta(days=i)).strftime("%Y-%m-%d")
            
            calendar[date] = {
                "topic": topic,
                "platforms": ["wechat", "xiaohongshu", "douyin"],
                "status": "planned"
            }
        
        # 保存日历
        calendar_path = os.path.join(self.output_dir, "content_calendar.json")
        with open(calendar_path, 'w', encoding='utf-8') as f:
            json.dump(calendar, f, ensure_ascii=False, indent=2)
        
        return calendar


# 使用示例
async def main():
    """主函数示例"""
    
    # 初始化ContentAI
    content_ai = ContentAI()
    
    print("🚀 ContentAI 内容创作助手已启动\n")
    
    # 示例1: 生成公众号文章
    print("📝 正在生成公众号文章...")
    article = await content_ai.generate_article(
        topic="如何用AI搭建一人公司",
        platform="wechat",
        word_count=2500
    )
    print(f"✅ 文章标题: {article.get('title', 'N/A')}\n")
    
    # 示例2: 生成抖音脚本
    print("🎬 正在生成抖音脚本...")
    script = await content_ai.generate_video_script(
        topic="AI赚钱方法",
        platform="douyin",
        duration=60
    )
    print(f"✅ 脚本已生成\n")
    
    # 示例3: 多平台改写
    print("🔄 正在改写为多平台格式...")
    source = "AI可以帮助普通人实现月入3万，关键是选对赛道和方法..."
    results = await content_ai.rewrite_for_platforms(
        source_content=source,
        platforms=["xiaohongshu", "weibo", "zhihu"]
    )
    print(f"✅ 已改写 {len(results)} 个平台\n")
    
    print("🎉 所有内容生成完成！")


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
