#!/usr/bin/env python3
"""
SEOAI - SEO优化专家
智能SEO分析和优化系统
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SEOAnalysis:
    """SEO分析结果"""
    url: str
    score: int
    issues: List[Dict]
    recommendations: List[str]
    keywords: List[Dict]
    meta_tags: Dict
    headings: Dict
    links: Dict
    performance: Dict
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        return {
            "url": self.url,
            "score": self.score,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "keywords": self.keywords,
            "meta_tags": self.meta_tags,
            "headings": self.headings,
            "links": self.links,
            "performance": self.performance,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class KeywordAnalysis:
    """关键词分析"""
    keyword: str
    search_volume: int
    difficulty: int
    competition: str
    cpc: float
    related_keywords: List[str]
    trends: List[int]
    
    def to_dict(self) -> Dict:
        return {
            "keyword": self.keyword,
            "search_volume": self.search_volume,
            "difficulty": self.difficulty,
            "competition": self.competition,
            "cpc": self.cpc,
            "related_keywords": self.related_keywords,
            "trends": self.trends
        }


class ContentOptimizer:
    """内容优化器"""
    
    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.optimal_title_length = (50, 60)
        self.optimal_desc_length = (150, 160)
    
    def _load_stop_words(self) -> set:
        """加载停用词"""
        return {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'to', 'of', 'and', 'in', 'that', 'have', 'for', 'it', 'with'
        }
    
    def optimize_title(self, title: str, target_keyword: str) -> Dict:
        """优化标题"""
        issues = []
        recommendations = []
        
        # 检查长度
        length = len(title)
        if length < self.optimal_title_length[0]:
            issues.append(f"标题太短 ({length}字符)")
            recommendations.append(f"建议增加到{self.optimal_title_length[0]}-{self.optimal_title_length[1]}字符")
        elif length > self.optimal_title_length[1]:
            issues.append(f"标题太长 ({length}字符)")
            recommendations.append(f"建议缩短到{self.optimal_title_length[1]}字符以内")
        
        # 检查关键词
        if target_keyword.lower() not in title.lower():
            issues.append("标题未包含目标关键词")
            recommendations.append(f"建议在标题中加入'{target_keyword}'")
        
        # 检查品牌词
        if '|' not in title and '-' not in title:
            recommendations.append("建议添加品牌分隔符 (| 或 -)")
        
        score = max(0, 100 - len(issues) * 20)
        
        return {
            "original": title,
            "optimized": self._generate_optimized_title(title, target_keyword),
            "length": length,
            "score": score,
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _generate_optimized_title(self, title: str, keyword: str) -> str:
        """生成优化后的标题"""
        if keyword.lower() not in title.lower():
            return f"{keyword} | {title}"[:60]
        return title[:60]
    
    def optimize_meta_description(self, description: str, target_keyword: str) -> Dict:
        """优化Meta描述"""
        issues = []
        recommendations = []
        
        length = len(description)
        if length < self.optimal_desc_length[0]:
            issues.append(f"描述太短 ({length}字符)")
        elif length > self.optimal_desc_length[1]:
            issues.append(f"描述太长 ({length}字符)")
        
        if target_keyword.lower() not in description.lower():
            issues.append("描述未包含目标关键词")
            recommendations.append(f"建议在描述中自然融入'{target_keyword}'")
        
        if not any(c.isdigit() for c in description):
            recommendations.append("建议添加数字增强吸引力 (如: 5个方法、2024年)")
        
        score = max(0, 100 - len(issues) * 25)
        
        return {
            "original": description,
            "optimized": self._generate_optimized_description(description, target_keyword),
            "length": length,
            "score": score,
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _generate_optimized_description(self, desc: str, keyword: str) -> str:
        """生成优化后的描述"""
        if keyword.lower() not in desc.lower():
            return f"了解{keyword}的最佳方法。{desc}"[:160]
        return desc[:160]
    
    def optimize_content(self, content: str, target_keyword: str, 
                        related_keywords: List[str] = None) -> Dict:
        """优化内容"""
        if related_keywords is None:
            related_keywords = []
        
        issues = []
        recommendations = []
        
        # 检查关键词密度
        word_count = len(content.split())
        keyword_count = content.lower().count(target_keyword.lower())
        density = (keyword_count / word_count * 100) if word_count > 0 else 0
        
        if density < 1:
            issues.append(f"关键词密度过低 ({density:.1f}%)")
            recommendations.append("建议增加关键词出现频率至1-2%")
        elif density > 3:
            issues.append(f"关键词密度过高 ({density:.1f}%)，可能被视为关键词堆砌")
            recommendations.append("建议降低关键词密度至1-2%")
        
        # 检查标题结构
        h2_count = content.count('## ')
        h3_count = content.count('### ')
        
        if h2_count < 3:
            recommendations.append(f"建议增加H2标题 (当前{h2_count}个，建议至少3个)")
        
        # 检查段落长度
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        long_paragraphs = [p for p in paragraphs if len(p) > 300]
        
        if long_paragraphs:
            recommendations.append(f"建议将{len(long_paragraphs)}个长段落拆分为短段落")
        
        # 检查图片alt标签
        image_count = content.count('![')
        alt_missing = content.count(']()')
        
        if image_count > 0 and alt_missing > 0:
            recommendations.append(f"建议为图片添加alt标签 ({alt_missing}/{image_count}个缺失)")
        
        # 检查内部链接
        internal_links = len(re.findall(r'\[.*?\]\(.*?\)', content))
        if internal_links < 2:
            recommendations.append("建议添加更多内部链接")
        
        score = max(0, 100 - len(issues) * 15)
        
        return {
            "word_count": word_count,
            "keyword_density": round(density, 2),
            "h2_count": h2_count,
            "h3_count": h3_count,
            "image_count": image_count,
            "internal_links": internal_links,
            "score": score,
            "issues": issues,
            "recommendations": recommendations,
            "optimized_content": self._apply_content_improvements(content, target_keyword)
        }
    
    def _apply_content_improvements(self, content: str, keyword: str) -> str:
        """应用内容改进"""
        # 这里可以实现更复杂的优化逻辑
        return content


class KeywordResearcher:
    """关键词研究器"""
    
    def __init__(self):
        self.search_volumes = {}
    
    def analyze_keyword(self, keyword: str) -> KeywordAnalysis:
        """分析关键词"""
        # 模拟数据 - 实际应调用API
        search_volume = self._estimate_search_volume(keyword)
        difficulty = self._calculate_difficulty(keyword)
        competition = self._assess_competition(keyword)
        cpc = self._estimate_cpc(keyword)
        related = self._find_related_keywords(keyword)
        trends = self._get_trends(keyword)
        
        return KeywordAnalysis(
            keyword=keyword,
            search_volume=search_volume,
            difficulty=difficulty,
            competition=competition,
            cpc=cpc,
            related_keywords=related,
            trends=trends
        )
    
    def _estimate_search_volume(self, keyword: str) -> int:
        """估算搜索量"""
        # 模拟数据
        base_volumes = {
            "ai": 100000,
            "machine learning": 50000,
            "python": 200000,
            "seo": 80000,
            "marketing": 120000
        }
        return base_volumes.get(keyword.lower(), 1000 + len(keyword) * 100)
    
    def _calculate_difficulty(self, keyword: str) -> int:
        """计算难度"""
        # 模拟难度计算
        length_factor = min(len(keyword) * 2, 30)
        competition_factor = 40 if " " in keyword else 60
        return min(length_factor + competition_factor, 100)
    
    def _assess_competition(self, keyword: str) -> str:
        """评估竞争程度"""
        difficulty = self._calculate_difficulty(keyword)
        if difficulty < 30:
            return "low"
        elif difficulty < 60:
            return "medium"
        else:
            return "high"
    
    def _estimate_cpc(self, keyword: str) -> float:
        """估算CPC"""
        # 模拟CPC
        high_value_keywords = ['insurance', 'loans', 'mortgage', 'attorney', 'credit']
        if any(hv in keyword.lower() for hv in high_value_keywords):
            return round(5.0 + len(keyword) * 0.1, 2)
        return round(0.5 + len(keyword) * 0.05, 2)
    
    def _find_related_keywords(self, keyword: str) -> List[str]:
        """查找相关关键词"""
        # 模拟相关关键词
        related_map = {
            "seo": ["seo optimization", "seo tools", "seo strategy", "local seo"],
            "ai": ["artificial intelligence", "machine learning", "deep learning", "neural networks"],
            "marketing": ["digital marketing", "content marketing", "email marketing", "social media"]
        }
        return related_map.get(keyword.lower(), [f"{keyword} guide", f"{keyword} tutorial"])
    
    def _get_trends(self, keyword: str) -> List[int]:
        """获取趋势数据"""
        # 模拟12个月的趋势数据
        import random
        base = self._estimate_search_volume(keyword)
        return [int(base * (0.8 + random.random() * 0.4)) for _ in range(12)]
    
    def find_long_tail_keywords(self, seed_keyword: str) -> List[Dict]:
        """查找长尾关键词"""
        long_tails = []
        templates = [
            f"how to {seed_keyword}",
            f"best {seed_keyword}",
            f"{seed_keyword} for beginners",
            f"{seed_keyword} tutorial",
            f"{seed_keyword} tools",
            f"free {seed_keyword}",
            f"{seed_keyword} 2024",
            f"{seed_keyword} vs"
        ]
        
        for kw in templates:
            analysis = self.analyze_keyword(kw)
            long_tails.append({
                "keyword": kw,
                "volume": analysis.search_volume,
                "difficulty": analysis.difficulty,
                "opportunity": analysis.search_volume / (analysis.difficulty + 1)
            })
        
        return sorted(long_tails, key=lambda x: x["opportunity"], reverse=True)


class TechnicalAnalyzer:
    """技术SEO分析器"""
    
    def analyze_url_structure(self, url: str) -> Dict:
        """分析URL结构"""
        issues = []
        recommendations = []
        
        parsed = urlparse(url)
        path = parsed.path
        
        # 检查URL长度
        if len(url) > 75:
            issues.append(f"URL太长 ({len(url)}字符)")
            recommendations.append("建议缩短URL至75字符以内")
        
        # 检查是否包含关键词
        if '-' not in path and '_' not in path:
            recommendations.append("建议使用连字符(-)分隔URL中的单词")
        
        # 检查参数
        if '?' in url:
            issues.append("URL包含查询参数")
            recommendations.append("建议将动态URL重写为静态URL")
        
        return {
            "url": url,
            "length": len(url),
            "issues": issues,
            "recommendations": recommendations,
            "is_seo_friendly": len(issues) == 0
        }
    
    def analyze_site_speed(self, url: str) -> Dict:
        """分析网站速度"""
        # 模拟速度分析
        metrics = {
            "first_contentful_paint": 1.2,
            "largest_contentful_paint": 2.5,
            "time_to_interactive": 3.0,
            "cumulative_layout_shift": 0.05,
            "total_blocking_time": 150
        }
        
        issues = []
        if metrics["largest_contentful_paint"] > 2.5:
            issues.append(f"LCP过慢 ({metrics['largest_contentful_paint']}s)")
        if metrics["time_to_interactive"] > 3.8:
            issues.append(f"TTI过慢 ({metrics['time_to_interactive']}s)")
        
        score = max(0, 100 - len(issues) * 20)
        
        return {
            "url": url,
            "metrics": metrics,
            "score": score,
            "issues": issues
        }
    
    def check_mobile_friendly(self, url: str) -> Dict:
        """检查移动友好性"""
        return {
            "url": url,
            "is_mobile_friendly": True,
            "viewport_configured": True,
            "text_readable": True,
            "tap_targets_sized": True,
            "score": 95
        }


class SEOAI:
    """SEO优化专家主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.content_optimizer = ContentOptimizer()
        self.keyword_researcher = KeywordResearcher()
        self.technical_analyzer = TechnicalAnalyzer()
        self.analysis_history: List[SEOAnalysis] = []
        
        logger.info("SEOAI initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "target_keyword_density": 0.015,
            "min_content_length": 300,
            "optimal_title_length": [50, 60],
            "optimal_description_length": [150, 160]
        }
    
    def analyze_page(self, url: str, content: str, title: str = "", 
                   meta_desc: str = "", target_keyword: str = "") -> SEOAnalysis:
        """分析页面SEO"""
        issues = []
        recommendations = []
        
        # 技术SEO分析
        url_analysis = self.technical_analyzer.analyze_url_structure(url)
        speed_analysis = self.technical_analyzer.analyze_site_speed(url)
        mobile_analysis = self.technical_analyzer.check_mobile_friendly(url)
        
        issues.extend(url_analysis["issues"])
        issues.extend(speed_analysis["issues"])
        
        recommendations.extend(url_analysis["recommendations"])
        
        # 内容分析
        content_analysis = self.content_optimizer.optimize_content(
            content, target_keyword
        )
        
        issues.extend(content_analysis["issues"])
        recommendations.extend(content_analysis["recommendations"])
        
        # 标题分析
        title_analysis = self.content_optimizer.optimize_title(title, target_keyword)
        issues.extend(title_analysis["issues"])
        recommendations.extend(title_analysis["recommendations"])
        
        # 描述分析
        desc_analysis = self.content_optimizer.optimize_meta_description(
            meta_desc, target_keyword
        )
        issues.extend(desc_analysis["issues"])
        recommendations.extend(desc_analysis["recommendations"])
        
        # 计算总分
        score = self._calculate_overall_score([
            url_analysis.get("is_seo_friendly", False),
            speed_analysis.get("score", 0),
            mobile_analysis.get("score", 0),
            content_analysis.get("score", 0),
            title_analysis.get("score", 0),
            desc_analysis.get("score", 0)
        ])
        
        analysis = SEOAnalysis(
            url=url,
            score=score,
            issues=issues,
            recommendations=recommendations,
            keywords=[],
            meta_tags={"title": title, "description": meta_desc},
            headings={"h1": [], "h2": [], "h3": []},
            links={"internal": 0, "external": 0},
            performance={"speed": speed_analysis, "mobile": mobile_analysis},
            timestamp=datetime.now()
        )
        
        self.analysis_history.append(analysis)
        
        return analysis
    
    def _calculate_overall_score(self, scores: List) -> int:
        """计算总体得分"""
        numeric_scores = []
        for s in scores:
            if isinstance(s, bool):
                numeric_scores.append(100 if s else 50)
            else:
                numeric_scores.append(s)
        
        return int(sum(numeric_scores) / len(numeric_scores)) if numeric_scores else 0
    
    def research_keywords(self, seed_keyword: str) -> Dict:
        """研究关键词"""
        main_analysis = self.keyword_researcher.analyze_keyword(seed_keyword)
        long_tail = self.keyword_researcher.find_long_tail_keywords(seed_keyword)
        
        return {
            "main_keyword": main_analysis.to_dict(),
            "long_tail_keywords": long_tail,
            "recommendations": [
                f"主关键词 '{seed_keyword}' 月搜索量: {main_analysis.search_volume}",
                f"关键词难度: {main_analysis.difficulty}/100",
                f"推荐优先优化长尾关键词: {long_tail[0]['keyword'] if long_tail else 'N/A'}"
            ]
        }
    
    def generate_seo_report(self, url: str) -> str:
        """生成SEO报告"""
        # 查找历史分析
        analysis = None
        for a in self.analysis_history:
            if a.url == url:
                analysis = a
                break
        
        if not analysis:
            return f"未找到 {url} 的分析记录"
        
        report = f"""
# SEO分析报告

## 基本信息
- **URL**: {url}
- **分析时间**: {analysis.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- **SEO得分**: {analysis.score}/100

## 评分详情
- 🟢 优秀 (90-100)
- 🟡 良好 (70-89)
- 🟠 需改进 (50-69)
- 🔴 差 (0-49)

## 当前得分: {analysis.score} {"🟢" if analysis.score >= 90 else "🟡" if analysis.score >= 70 else "🟠" if analysis.score >= 50 else "🔴"}

## 发现的问题 ({len(analysis.issues)}个)
"""
        
        for i, issue in enumerate(analysis.issues, 1):
            report += f"{i}. {issue}\n"
        
        report += f"\n## 优化建议 ({len(analysis.recommendations)}条)\n"
        
        for i, rec in enumerate(analysis.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += """
## 下一步行动
1. 优先修复高优先级问题
2. 实施内容优化建议
3. 监控关键词排名变化
4. 定期重新评估SEO表现
"""
        
        return report
    
    def export_analysis(self, filepath: str):
        """导出分析数据"""
        data = {
            "analyses": [a.to_dict() for a in self.analysis_history],
            "config": self.config,
            "export_time": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis exported to {filepath}")


# 使用示例
if __name__ == "__main__":
    seo_ai = SEOAI()
    
    print("=" * 60)
    print("SEOAI - SEO优化专家")
    print("=" * 60)
    
    # 示例1: 关键词研究
    print("\n🔍 关键词研究: 'AI Agent'")
    print("-" * 60)
    
    keyword_data = seo_ai.research_keywords("AI Agent")
    main = keyword_data["main_keyword"]
    
    print(f"\n主关键词: {main['keyword']}")
    print(f"月搜索量: {main['search_volume']:,}")
    print(f"难度: {main['difficulty']}/100")
    print(f"竞争度: {main['competition']}")
    print(f"CPC: ${main['cpc']}")
    
    print("\n📈 长尾关键词机会:")
    for kw in keyword_data["long_tail_keywords"][:5]:
        print(f"  • {kw['keyword']} (搜索量: {kw['volume']}, 难度: {kw['difficulty']})")
    
    # 示例2: 页面分析
    print("\n" + "=" * 60)
    print("📄 页面SEO分析")
    print("-" * 60)
    
    sample_content = """
    # AI Agent Money Machine
    
    这是一个关于AI Agent赚钱的项目。
    
    ## 什么是AI Agent
    AI Agent是人工智能代理，可以自动执行任务。
    
    ## 如何赚钱
    通过部署AI Agent来创造收入。
    """
    
    analysis = seo_ai.analyze_page(
        url="https://example.com/ai-agent-money-machine",
        content=sample_content,
        title="AI Agent Money Machine",
        meta_desc="Learn how to make money with AI agents",
        target_keyword="AI Agent"
    )
    
    print(f"\nSEO得分: {analysis.score}/100")
    print(f"发现问题: {len(analysis.issues)}个")
    print(f"优化建议: {len(analysis.recommendations)}条")
    
    print("\n❌ 主要问题:")
    for issue in analysis.issues[:3]:
        print(f"  • {issue}")
    
    print("\n💡 优化建议:")
    for rec in analysis.recommendations[:3]:
        print(f"  • {rec}")
    
    # 示例3: 生成报告
    print("\n" + "=" * 60)
    print("📊 生成SEO报告")
    print("-" * 60)
    
    report = seo_ai.generate_seo_report("https://example.com/ai-agent-money-machine")
    print(report[:800] + "...")
    
    print("\n" + "=" * 60)
    print("✅ 分析完成!")
    print("=" * 60)
