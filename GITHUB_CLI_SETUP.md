# GitHub CLI 配置指南

## ✅ GitHub CLI 已安装

版本: 2.40.1
路径: ~/.local/bin/gh

---

## 🔐 配置GitHub认证

### 方法1: 使用浏览器登录 (推荐)

```bash
export PATH="$HOME/.local/bin:$PATH"
gh auth login
```

选择:
- ? What account do you want to log into? **GitHub.com**
- ? What is your preferred protocol for Git operations? **HTTPS**
- ? Authenticate Git with your GitHub credentials? **Yes**
- ? How would you like to authenticate? **Login with a web browser**

然后按提示在浏览器中完成授权。

### 方法2: 使用Token

1. 创建Token:
   - 访问: https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 勾选权限: **repo**, **workflow**, **read:org**
   - 生成Token

2. 配置CLI:
```bash
export PATH="$HOME/.local/bin:$PATH"
echo "YOUR_TOKEN" | gh auth login --with-token
```

---

## 🚀 创建仓库并推送

### 自动创建仓库

```bash
cd ~/ai-agent-money-machine
export PATH="$HOME/.local/bin:$PATH"

# 创建仓库
gh repo create ai-agent-money-machine \
  --public \
  --description "6个AI Agent组成的印钞机系统 - 月入$5500-25000" \
  --source=. \
  --remote=origin \
  --push
```

### 手动步骤

如果自动创建失败:

```bash
# 1. 创建仓库 (在GitHub网页上)
# 访问: https://github.com/new
# 填写:
#   - Repository name: ai-agent-money-machine
#   - Description: 6个AI Agent组成的印钞机系统
#   - 选择 Public
#   - 点击 Create repository

# 2. 推送代码
cd ~/ai-agent-money-machine
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-money-machine.git
git branch -M main
git push -u origin main
```

---

## 🌐 启用GitHub Pages

### 自动启用

```bash
export PATH="$HOME/.local/bin:$PATH"

# 启用Pages (需要gh v2.30+)
gh api repos/YOUR_USERNAME/ai-agent-money-machine/pages \
  --method POST \
  --input - <<< '{"source":{"branch":"main","path":"/docs"}}'
```

### 手动启用

1. 访问: `https://github.com/YOUR_USERNAME/ai-agent-money-machine/settings/pages`
2. Source: **Deploy from a branch**
3. Branch: **main** / **docs folder**
4. 点击 **Save**
5. 等待几分钟

网站地址: `https://YOUR_USERNAME.github.io/ai-agent-money-machine`

---

## 📋 常用命令

```bash
# 添加到PATH
export PATH="$HOME/.local/bin:$PATH"

# 查看帮助
gh --help

# 查看仓库
gh repo view

# 创建Issue
gh issue create --title "Bug" --body "描述"

# 创建PR
gh pr create --title "Feature" --body "描述"

# 查看工作流
gh workflow list

# 运行工作流
gh workflow run deploy.yml
```

---

## 🔧 添加到 .bashrc

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🆘 故障排除

### 问题: command not found
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 问题: authentication required
```bash
gh auth login
```

### 问题: 权限拒绝
```bash
# 检查Token权限
gh auth status

# 重新登录
gh auth logout
gh auth login
```

### 问题: 推送失败
```bash
# 检查远程仓库
git remote -v

# 重新添加远程
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-money-machine.git

# 推送
git push -u origin main
```

---

## ✅ 验证安装

```bash
export PATH="$HOME/.local/bin:$PATH"

# 检查版本
gh --version

# 检查登录状态
gh auth status

# 测试命令
gh repo list
```

---

**准备好推送到GitHub了吗？** 🚀
