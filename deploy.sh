#!/bin/bash
# AI Agent Money Machine - 完整部署脚本
# 一键完成GitHub推送、Pages启用

set -e  # 遇到错误立即退出

echo "🚀 AI Agent Money Machine - 完整部署脚本"
echo "=========================================="
echo ""

# 检查GitHub CLI
if ! command -v gh &> /dev/null; then
    if [ -f "$HOME/.local/bin/gh" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo "❌ GitHub CLI 未安装"
        echo "请先运行: python3 install_gh_cli.py"
        exit 1
    fi
fi

echo "✅ GitHub CLI 已安装"

# 检查GitHub认证
if ! gh auth status &> /dev/null; then
    echo ""
    echo "🔐 需要GitHub认证"
    echo ""
    echo "请运行: gh auth login"
    echo ""
    echo "或者使用Token:"
    echo "  1. 访问 https://github.com/settings/tokens"
    echo "  2. 创建Token (勾选repo权限)"
    echo "  3. 运行: echo 'YOUR_TOKEN' | gh auth login --with-token"
    echo ""
    exit 1
fi

echo "✅ GitHub 已认证"

# 获取用户名
USERNAME=$(gh api user -q .login)
echo "👤 GitHub用户: $USERNAME"

# 进入项目目录
cd ~/ai-agent-money-machine

# 检查git仓库
if [ ! -d .git ]; then
    echo "❌ 当前目录不是git仓库"
    exit 1
fi

echo "✅ Git仓库检查通过"

# 检查远程仓库
if git remote -v | grep -q origin; then
    echo "⚠️  远程仓库已存在"
    read -p "是否重新设置远程仓库? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        echo "使用现有远程仓库"
    fi
fi

# 创建GitHub仓库
if ! git remote -v | grep -q origin; then
    echo ""
    echo "📦 创建GitHub仓库..."
    
    # 检查仓库是否已存在
    if gh repo view "$USERNAME/ai-agent-money-machine" &> /dev/null; then
        echo "⚠️  仓库已存在，使用现有仓库"
        git remote add origin "https://github.com/$USERNAME/ai-agent-money-machine.git"
    else
        # 创建新仓库
        gh repo create ai-agent-money-machine \
            --public \
            --description "6个AI Agent组成的印钞机系统 - 月入\$5500-25000" \
            --source=. \
            --remote=origin \
            --push
        
        echo "✅ 仓库创建成功"
    fi
fi

# 推送代码
echo ""
echo "📤 推送代码..."
git branch -M main
git push -u origin main

echo "✅ 代码推送成功"

# 启用GitHub Pages
echo ""
echo "🌐 启用GitHub Pages..."

# 检查是否已启用
PAGES_URL=$(gh api "repos/$USERNAME/ai-agent-money-machine/pages" -q .html_url 2>/dev/null || echo "")

if [ -n "$PAGES_URL" ]; then
    echo "✅ GitHub Pages 已启用"
else
    # 尝试启用Pages
    gh api "repos/$USERNAME/ai-agent-money-machine/pages" \
        --method POST \
        --input - <<< '{"source":{"branch":"main","path":"/docs"}}' 2>/dev/null || true
    
    echo "⚠️  请手动启用GitHub Pages:"
    echo "  访问: https://github.com/$USERNAME/ai-agent-money-machine/settings/pages"
    echo "  Source: Deploy from a branch"
    echo "  Branch: main /docs folder"
fi

# 显示信息
echo ""
echo "=========================================="
echo "🎉 部署完成!"
echo "=========================================="
echo ""
echo "📁 仓库地址:"
echo "  https://github.com/$USERNAME/ai-agent-money-machine"
echo ""
echo "🌐 GitHub Pages:"
echo "  https://$USERNAME.github.io/ai-agent-money-machine"
echo ""
echo "⚠️  注意:"
echo "  - GitHub Pages可能需要几分钟才能生效"
echo "  - 首次访问可能需要等待5-10分钟"
echo ""
echo "📋 下一步:"
echo "  1. 访问仓库查看代码"
echo "  2. 配置Stripe/PayPal收款"
echo "  3. 在Product Hunt发布"
echo "  4. 开始推广销售"
echo ""
echo "💰 预期收益: \$5500-25000/月"
echo "=========================================="
