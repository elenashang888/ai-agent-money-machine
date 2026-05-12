# AI内容自动化系统

真正可用的自动化内容生成工具，集成百炼API。

## 🚀 快速开始

### 1. 配置API Key

```bash
# 方法1：环境变量
export BAILIAN_API_KEY=your_api_key

# 方法2：编辑 .env 文件
cp .env.example .env
# 编辑 .env 填入你的API Key
```

### 2. 启动系统

```bash
chmod +x start.sh
./start.sh
```

### 3. 使用

```python
from content_generator import ContentPipeline

# 创建流水线
pipeline = ContentPipeline("your_api_key")

# 生成内容
content = pipeline.create_content(
    topic="AI如何帮助普通人赚钱",
    platform="wechat",
    title_count=10
)

# 保存
pipeline.save_content(content)
```

## 📋 功能特性

### ✅ 已实现
- [x] 自动生成爆款标题（10个备选）
- [x] 预估点击率分析
- [x] 自动生成文章大纲
- [x] 自动生成完整文章
- [x] SEO优化建议
- [x] 多平台适配（公众号/小红书/抖音/知乎/B站）
- [x] 导出Markdown格式
- [x] 内容历史记录

### 🚧 开发中
- [ ] 自动发布到公众号
- [ ] 自动发布到小红书
- [ ] 定时任务调度
- [ ] 批量生成
- [ ] 数据分析

## 🔧 系统架构

```
content_automation/
├── content_generator.py  # 核心生成器
├── config.json         # 配置文件
├── start.sh            # 启动脚本
├── requirements.txt    # 依赖
├── output/             # 输出目录
│   └── 20240511_xxx.md # 生成的文章
└── logs/               # 日志目录
```

## 📝 使用示例

### 示例1：生成公众号文章

```python
from content_generator import ContentPipeline

pipeline = ContentPipeline()
content = pipeline.create_content(
    topic="一人公司如何用AI月入过万",
    platform="wechat",
    title_count=10
)

# 查看生成的标题
for title in content['titles']:
    print(f"{title['title']} - 预估点击率：{title['ctr']}")

# 保存
pipeline.save_content(content)
```

### 示例2：批量生成

```python
from content_generator import ContentPipeline

pipeline = ContentPipeline()

topics = [
    "AI头像定制赚钱",
    "AI简历优化服务",
    "AI短视频矩阵"
]

for topic in topics:
    content = pipeline.create_content(topic, "wechat")
    pipeline.save_content(content)
    print(f"✅ {topic} 完成")
```

## 🎯 平台适配

| 平台 | 特点 | 最佳长度 | 风格 |
|------|------|---------|------|
| 公众号 | 深度阅读 | 2000字 | 专业干货 |
| 小红书 | 视觉+短内容 | 500字 | 种草笔记 |
| 抖音 | 短视频 | 300字 | 情绪+悬念 |
| 知乎 | 问答形式 | 3000字 | 深度分析 |
| B站 | 视频脚本 | 1500字 | 年轻化+梗 |

## 🔑 API Key获取

### 百炼（推荐）
1. 访问 https://dashscope.aliyun.com/
2. 注册/登录阿里云账号
3. 创建API Key
4. 复制Key到环境变量

### OpenAI（备选）
1. 访问 https://platform.openai.com/
2. 创建API Key
3. 需要海外信用卡

## 🛠️ 高级配置

编辑 `config.json`：

```json
{
  "content_generation": {
    "default_platform": "wechat",
    "default_title_count": 10,
    "default_article_length": "medium",
    "output_dir": "./output"
  },
  "automation": {
    "schedule_enabled": true,
    "schedule_time": "09:00",
    "auto_publish": false
  }
}
```

## 📝 输出格式

生成的文章包含：
- 10个备选标题（含点击率预估）
- 文章大纲（JSON格式）
- 完整正文（Markdown）
- SEO优化建议
- 元数据（时间、字数、平台）

## 🐛 故障排除

### API调用失败
- 检查API Key是否正确
- 检查网络连接
- 查看百炼控制台是否有额度

### 生成内容质量低
- 调整temperature参数
- 提供更详细的主题描述
- 尝试不同平台风格

### 保存失败
- 检查output目录权限
- 确保磁盘空间充足

## 📈 性能优化

- 使用缓存避免重复调用API
- 批量生成时使用并发
- 大文章分段生成后合并

## 🔒 安全注意

- 不要将API Key提交到Git
- 定期更换API Key
- 使用环境变量存储敏感信息

## 🎁 后续计划

1. **自动发布模块**
   - 公众号API对接
   - 小红书API对接
   - 定时发布

2. **数据分析模块**
   - 阅读数据分析
   - 转化率追踪
   - A/B测试

3. **工作流自动化**
   - 定时任务
   - 批量处理
   - 邮件通知

---

**现在就开始使用吧！**

```bash
./start.sh
```
