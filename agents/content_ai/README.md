# ContentAI - AI内容创作助手

## 📝 简介

ContentAI是一个智能内容创作助手，可以自动生成文章、视频脚本、社媒文案，并支持多平台内容分发。

## 🎯 核心功能

### 1. 文章生成
- ✅ 公众号长文章
- ✅ 知乎专业回答
- ✅ 今日头条资讯
- ✅ SEO优化文章

### 2. 视频脚本生成
- ✅ 抖音短视频脚本（60秒）
- ✅ B站长视频脚本（10-15分钟）
- ✅ 视频号脚本
- ✅ 快手脚本

### 3. 社媒文案改写
- ✅ 小红书图文
- ✅ 微博短文案
- ✅ 多平台一键改写

### 4. 内容管理
- ✅ 内容日历生成
- ✅ 自动保存和归档
- ✅ 多平台发布计划

## 🚀 快速开始

### 安装依赖

```bash
pip install openai
```

### 配置API Key

```bash
export OPENAI_API_KEY="your-api-key"
```

### 运行示例

```python
import asyncio
from content_ai import ContentAI

async def main():
    # 初始化
    ai = ContentAI()
    
    # 生成公众号文章
    article = await ai.generate_article(
        topic="如何用AI赚钱",
        platform="wechat",
        word_count=2500
    )
    
    print(f"标题: {article['title']}")
    print(f"内容: {article['content'][:500]}...")

# 运行
asyncio.run(main())
```

## 📊 使用场景

### 场景1: 自媒体运营
```python
# 生成一周内容
topics = [
    "AI副业入门指南",
    "ChatGPT赚钱方法",
    "一人公司模式",
    "AI工具推荐",
    "副业避坑指南",
    "自动化赚钱系统",
    "被动收入搭建"
]

calendar = await ai.generate_content_calendar(topics, days=7)
```

### 场景2: 多平台分发
```python
# 1篇内容 → 10个平台
source = "AI可以帮助普通人实现月入3万..."

results = await ai.rewrite_for_platforms(
    source_content=source,
    platforms=["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"]
)
```

### 场景3: 视频内容生产
```python
# 生成视频脚本
script = await ai.generate_video_script(
    topic="AI赚钱方法",
    platform="douyin",
    duration=60
)
```

## 💰 收益模式

| 服务类型 | 定价 | 月收入潜力 |
|----------|------|-----------|
| 文章代写 | 100-500元/篇 | 5,000-20,000元 |
| 脚本撰写 | 200-800元/个 | 3,000-10,000元 |
| 多平台分发 | 500-2000元/套 | 8,000-30,000元 |
| 内容日历 | 1000-3000元/月 | 固定收入 |

## 🔧 配置说明

### config.json

```json
{
  "default_model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 4000,
  "output_dir": "~/content-output"
}
```

### 环境变量

```bash
OPENAI_API_KEY=your-api-key
```

## 📁 输出文件

所有生成的内容保存在 `~/content-output/` 目录：

```
~/content-output/
├── wechat_topic_20240511_143022.json
├── douyin_topic_20240511_143045.json
├── xiaohongshu_topic_20240511_143108.json
└── content_calendar.json
```

## 🎨 平台模板

### 公众号 (wechat)
- 字数：1500-3000字
- 风格：深度长文
- 结构：钩子→痛点→方案→案例→行动

### 小红书 (xiaohongshu)
- 字数：300-800字
- 风格：清单式、emoji丰富
- 结构：封面→要点→互动→标签

### 抖音 (douyin)
- 时长：60秒
- 风格：快节奏、黄金3秒
- 结构：钩子→痛点→方案→效果→CTA

### 知乎 (zhihu)
- 字数：2000-5000字
- 风格：专业问答
- 结构：结论→分析→方法论→案例→总结

## ⚡ 性能指标

- 文章生成速度：30-60秒/篇
- 脚本生成速度：20-40秒/个
- 多平台改写：10-20秒/平台
- API成本：约0.1-0.3元/篇

## 🔮 未来规划

- [ ] 接入更多AI模型（Claude、Gemini）
- [ ] 支持图片生成（DALL-E、Midjourney）
- [ ] 自动发布到各平台API
- [ ] 数据分析与优化建议
- [ ] 团队协作功能

## 📞 联系方式

- 作者：AgentVerse
- 邮箱：151804947@qq.com
- GitHub：https://github.com/elenashang888/ai-agent-money-machine

---

**ContentAI - 让内容创作效率提升10倍** 🚀
