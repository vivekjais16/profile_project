#!/usr/bin/env bash
# ==============================================================================
# GitHub Deployment & Branch Synchronization Script
# Author: Vivek Jaiswal <vivekjais16@gmail.com>
# Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
# ==============================================================================

set -e

echo "================================================================="
echo "  🚀 Vivek Jaiswal Portfolio — GitHub Remote Push Utility"
echo "================================================================="

# Ensure we are in project root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository."
    exit 1
fi

# Verify author details
echo "👤 Git Author: $(git config user.name) <$(git config user.email)>"

# Check existing remotes
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$CURRENT_REMOTE" ]; then
    if [ -n "$1" ]; then
        REMOTE_URL="$1"
    else
        echo ""
        echo "Please create a new repository on GitHub (e.g., https://github.com/new)"
        echo "Enter your GitHub repository URL (HTTPS or SSH):"
        echo "Example: https://github.com/vivekjaiswal/profile_project.git"
        read -r -p "Repository URL: " REMOTE_URL
    fi

    if [ -z "$REMOTE_URL" ]; then
        echo "❌ Error: Repository URL cannot be empty."
        exit 1
    fi

    echo "🔗 Setting remote origin to: $REMOTE_URL"
    git remote add origin "$REMOTE_URL"
else
    echo "🔗 Current remote origin: $CURRENT_REMOTE"
    if [ -n "$1" ]; then
        echo "Updating remote origin to: $1"
        git remote set-url origin "$1"
    fi
fi

# Push development branch
echo ""
echo "📦 [1/2] Pushing branch 'development' to GitHub..."
git push -u origin development

# Push master branch
echo ""
echo "📦 [2/2] Pushing branch 'master' to GitHub..."
git push -u origin master

# Push tags
echo ""
echo "🏷️  Pushing tags..."
git push --tags origin || true

echo ""
echo "================================================================="
echo "✅ SUCCESS! Both 'development' and 'master' branches pushed!"
echo "🌐 View your repository on GitHub."
echo "================================================================="
