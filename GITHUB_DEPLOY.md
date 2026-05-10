# GitHub 部署指南

## 🚀 快速部署到GitHub

### 1. 创建GitHub仓库

访问: https://github.com/new

设置:
- Repository name: `ai-agent-money-machine`
- Description: `6个AI Agent组成的印钞机系统 - 月入$5500-25000`
- Public 或 Private
- 勾选 "Add a README file" (可选)

### 2. 推送代码

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-money-machine.git

# 推送代码
git branch -M main
git push -u origin main
```

### 3. 启用GitHub Pages

1. 进入仓库 Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / docs folder
4. 点击 Save

### 4. 访问网站

几分钟后访问:
`https://YOUR_USERNAME.github.io/ai-agent-money-machine`

---

## 🔧 本地运行

```bash
cd ~/ai-agent-money-machine

# 安装依赖
pip install flask flask-cors

# 启动服务器
python3 api_server.py

# 或启动简单服务器
python3 simple_server.py
```

访问:
- http://localhost:5000 - 仪表盘
- http://localhost:5000/landing - 落地页
- http://localhost:5000/api/health - 健康检查

---

## 💰 变现方式

### 方式1: 自用
- 部署后为自己工作
- 6个Agent同时运行
- 预期收益: $5500-25000/月

### 方式2: 销售
- 打包出售代码
- 定价: $99-999
- 在Gumroad/Product Hunt销售

### 方式3: SaaS服务
- 部署为在线服务
- 订阅收费: $29-99/月
- 多租户架构

---

## 📁 文件说明

```
ai-agent-money-machine/
├── content_ai_agent.py      # 内容创作助手
├── service_ai_agent.py      # 智能客服机器人
├── research_ai_agent.py     # 产品研究分析师
├── trade_ai_agent.py        # 智能交易助手
├── seo_ai_agent.py          # SEO优化专家
├── email_ai_agent.py        # 邮件营销专员
├── api_server.py            # Flask API服务器
├── simple_server.py         # 纯Python服务器
├── landing-page.html        # 营销落地页
├── docs/                    # GitHub Pages目录
│   └── index.html
├── start_all.sh            # 一键启动脚本
├── requirements.txt         # Python依赖
├── config.example.json      # 配置模板
├── .env.example            # 环境变量模板
└── README.md               # 项目文档
```

---

## 🔌 API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 仪表盘 |
| `/landing` | GET | 营销落地页 |
| `/api/health` | GET | 健康检查 |
| `/api/dashboard` | GET | 所有Agent指标 |
| `/api/content/generate` | POST | 生成内容 |
| `/api/service/chat` | POST | 客服对话 |
| `/api/research/trend` | POST | 趋势分析 |
| `/api/trade/signal` | POST | 交易信号 |
| `/api/seo/keywords` | POST | 关键词研究 |
| `/api/email/generate` | POST | 生成邮件 |

---

## 📝 配置API密钥

1. 复制配置模板:
```bash
cp config.example.json config.json
cp .env.example .env
```

2. 编辑配置文件，填入你的API密钥

3. 支持的API:
   - OpenAI
   - Anthropic Claude
   - 阿里Dashscope
   - DeepSeek
   - 交易所API

---

## 🆘 常见问题

**Q: 需要编程基础吗？**
A: 不需要！提供一键启动脚本

**Q: 可以商用吗？**
A: 可以！MIT License，自由使用

**Q: 如何更新？**
A: git pull 获取最新代码

**Q: 支持哪些平台？**
A: Linux/Mac/Windows 都支持

---

**Built with ❤️ by AI Agent Money Machine**
