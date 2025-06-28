#!/bin/bash
# Quick deployment script for Render.com

echo "🚀 Preparing for Render.com Deployment"
echo "====================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Free AI Agent API for Render deployment"
    
    echo "🌐 Please create a GitHub repository and run:"
    echo "git remote add origin https://github.com/yourusername/your-repo-name.git"
    echo "git branch -M main"
    echo "git push -u origin main"
else
    echo "✅ Git repository already initialized"
    echo "📤 Adding changes and committing..."
    git add .
    git commit -m "Updated AI Agent API for free deployment"
    
    echo "🚀 Pushing to GitHub..."
    git push
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com and sign up (FREE)"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Render will auto-detect render.yaml"
echo "5. Click 'Create Web Service'"
echo ""
echo "💡 Your API will be available at: https://your-service-name.onrender.com"
echo "💰 Total cost: $0.00"