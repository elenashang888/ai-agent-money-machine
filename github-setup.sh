#!/bin/bash
# GitHub 仓库创建和推送脚本

echo "🚀 AI Agent Money Machine - GitHub 部署脚本"
echo "=============================================="
echo ""

# 检查参数
if [ -z "$1" ]; then
    echo "❌ 请提供GitHub用户名"
    echo "用法: ./github-setup.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "或者手动运行以下命令:"
    echo ""
    echo "1. 在GitHub创建仓库:"
    echo "   访问: https://github.com/new"
    echo "   仓库名: ai-agent-money-machine"
    echo ""
    echo "2. 推送代码:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-agent-money-machine.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

USERNAME=$1
REPO_NAME="ai-agent-money-machine"

echo "📦 准备推送到: https://github.com/$USERNAME/$REPO_NAME"
echo ""

# 检查git
git status > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ 当前目录不是git仓库"
    exit 1
fi

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"

# 检查远程仓库
git remote -v

echo ""
echo "✅ 远程仓库已配置"
echo ""

# 推送代码
echo "📤 推送代码到GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 推送成功!"
    echo ""
    echo "🔗 仓库地址: https://github.com/$USERNAME/$REPO_NAME"
    echo "🌐 启用GitHub Pages:"
    echo "   1. 访问: https://github.com/$USERNAME/$REPO_NAME/settings/pages"
    echo "   2. Source: Deploy from a branch"
    echo "   3. Branch: main /docs folder"
    echo "   4. 点击 Save"
    echo ""
    echo "📄 网站将在几分钟后可用:"
    echo "   https://$USERNAME.github.io/$REPO_NAME"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因:"
    echo "   1. 仓库不存在 - 请先创建: https://github.com/new"
    echo "   2. 没有权限 - 请检查用户名和token"
    echo "   3. 网络问题 - 请检查网络连接"
    echo ""
    echo "手动创建仓库步骤:"
    echo "   1. 访问 https://github.com/new"
    echo "   2. Repository name: ai-agent-money-machine"
    echo "   3. 选择 Public 或 Private"
    echo "   4. 点击 Create repository"
    echo "   5. 按照页面提示推送代码"
fi
