# EmailAI - 邮件营销专员

智能邮件营销自动化系统，提供邮件创建、优化、分段和营销分析功能。

## 🎯 功能特性

- **主题行优化**: AI驱动的主题行分析和优化
- **内容个性化**: 动态内容替换和个性化
- **用户分段**: 基于参与度、标签、日期的智能分段
- **邮件活动管理**: 创建、安排、跟踪邮件活动
- **营销分析**: 详细的指标报告和洞察

## 🚀 快速开始

### 运行示例

```bash
python email_ai.py
```

### 基础使用

```python
from email_ai import EmailAI, EmailType

# 初始化
email_ai = EmailAI()

# 添加订阅者
subscriber = email_ai.add_subscriber(
    email="user@example.com",
    name="张三",
    tags=["vip", "tech"]
)

# 创建邮件活动
campaign = email_ai.create_campaign(
    name="欢迎新用户",
    email_type=EmailType.WELCOME,
    subject="🎁 欢迎加入！",
    content="<h1>欢迎{{first_name}}！</h1>"
)

# 优化主题行
analysis = email_ai.optimize_subject("欢迎邮件")
print(f"主题评分: {analysis['score']}")

# 用户分段
segments = email_ai.segment_subscribers("engagement")
```

## 📧 邮件类型

| 类型 | 用途 | 触发时机 |
|------|------|----------|
| WELCOME | 欢迎邮件 | 新用户订阅 |
| PROMOTIONAL | 促销邮件 | 活动推广 |
| NEWSLETTER | 新闻通讯 | 定期发送 |
| ABANDONED_CART | 购物车挽回 | 放弃购物车 |
| RE_ENGAGEMENT | 再激活 | 用户流失 |
| TRANSACTIONAL | 交易邮件 | 订单/通知 |
| SURVEY | 调研邮件 | 用户反馈 |

## 🎯 主题行优化

### 分析维度

- 长度检查 (20-60字符)
- 垃圾词检测
- 个性化建议
- 紧迫感建议
- 数字使用建议
- 表情符号建议

### 示例输出

```
原始主题: 欢迎加入我们的邮件列表
评分: 65/100

⚠️ 问题:
  • 主题太短 (15字符)
  • 缺少紧迫感词汇

💡 建议:
  • 建议添加个性化元素
  • 建议添加数字增强吸引力
  • 考虑添加表情符号

优化版本:
  • 🎁 欢迎加入！3个专属福利等你领取
  • 限时：欢迎{{first_name}}，你的专属优惠已到账
```

## 👥 用户分段

### 分段类型

1. **参与度分段**
   - Highly Engaged (≥80分)
   - Moderately Engaged (50-79分)
   - Low Engaged (20-49分)
   - Inactive (<20分)

2. **日期分段**
   - New (<7天)
   - Recent (7-30天)
   - Established (30-90天)
   - Veteran (>90天)

3. **标签分段**
   - 按自定义标签分组

## 📊 营销指标

| 指标 | 说明 | 行业基准 |
|------|------|----------|
| 送达率 | 成功送达比例 | 95%+ |
| 打开率 | 邮件打开比例 | 20-25% |
| 点击率 | 链接点击比例 | 2-5% |
| 退订率 | 退订比例 | <0.5% |
| 投诉率 | 投诉比例 | <0.1% |

## 📝 个性化变量

| 变量 | 说明 | 示例 |
|------|------|------|
| {{first_name}} | 名字 | 张三 |
| {{email}} | 邮箱 | user@example.com |
| {{company}} | 公司 | AgentVerse |
| {{signup_date}} | 注册日期 | 2024年5月11日 |
| {{last_purchase}} | 上次购买 | 产品A |

## ⚙️ 配置说明

编辑 `config.json`:

```json
{
  "sender_name": "AgentVerse",
  "sender_email": "noreply@agentverse.com",
  "send_time_optimization": true,
  "ab_testing": true
}
```

## 📈 输出示例

```
============================================================
EmailAI - 邮件营销专员
============================================================

📧 添加订阅者
------------------------------------------------------------
✅ 张三 (user1@example.com) - 标签: vip, tech
✅ 李四 (user2@example.com) - 标签: new
✅ 王五 (user3@example.com) - 标签: vip, marketing

📨 创建邮件活动
------------------------------------------------------------
✅ 活动创建: 欢迎新用户
   ID: campaign_20240511_143022_1234
   收件人: 4人

✨ 主题行优化
------------------------------------------------------------
原始主题: 🎁 欢迎加入！你的专属福利已到账
评分: 85/100

💡 建议:
  • 建议添加个性化元素

👥 用户分段分析
------------------------------------------------------------
highly_engaged: 0人
moderately_engaged: 0人
low_engaged: 0人
inactive: 4人

📊 生成营销报告
------------------------------------------------------------
# 邮件营销报告
...

✅ 演示完成!
```

## 📄 许可证

MIT License
