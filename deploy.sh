#!/bin/bash

# SynaptiVerse Quick Deploy Script
# Prepares project for deployment to cloud platforms

echo "🚀 SynaptiVerse Deployment Preparation"
echo "======================================"
echo ""

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
else
    echo "✅ requirements.txt found"
fi

# Check deployment files
echo ""
echo "📋 Checking deployment configurations..."

if [ -f "render.yaml" ]; then
    echo "✅ Render config found (render.yaml)"
else
    echo "⚠️  render.yaml missing"
fi

if [ -f "railway.json" ]; then
    echo "✅ Railway config found (railway.json)"
else
    echo "⚠️  railway.json missing"
fi

if [ -f "fly.toml" ]; then
    echo "✅ Fly.io config found (fly.toml)"
else
    echo "⚠️  fly.toml missing"
fi

if [ -f "Procfile" ]; then
    echo "✅ Procfile found"
else
    echo "⚠️  Procfile missing"
fi

# Check .env setup
echo ""
echo "🔧 Checking environment configuration..."

if [ -f ".env.example" ]; then
    echo "✅ .env.example template found"
else
    echo "⚠️  .env.example missing"
fi

if [ -f ".env" ]; then
    echo "⚠️  .env found (make sure it's in .gitignore)"
else
    echo "ℹ️  .env not found (will use defaults in production)"
fi

# Check .gitignore
if [ -f ".gitignore" ]; then
    if grep -q "^\.env$" .gitignore; then
        echo "✅ .env is gitignored"
    else
        echo "⚠️  .env not in .gitignore - adding it..."
        echo ".env" >> .gitignore
        echo "✅ Added .env to .gitignore"
    fi
else
    echo "❌ .gitignore not found!"
    exit 1
fi

# Check if there are uncommitted changes
echo ""
echo "📝 Checking Git status..."
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No uncommitted changes"
else
    echo "⚠️  You have uncommitted changes:"
    git status --short
    echo ""
    read -p "Do you want to commit all changes? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message (or press Enter for default): " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg="Deploy SynaptiVerse for hackathon submission"
        fi
        git commit -m "$commit_msg"
        echo "✅ Changes committed"
    else
        echo "⏭️  Skipping commit"
    fi
fi

# Check for remote
echo ""
echo "🌐 Checking Git remote..."
if git remote | grep -q "origin"; then
    remote_url=$(git remote get-url origin)
    echo "✅ Remote 'origin' configured: $remote_url"
else
    echo "⚠️  No remote 'origin' configured"
    echo ""
    echo "To add a GitHub remote:"
    echo "  1. Create repo at https://github.com/new"
    echo "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/synaptiVerse.git"
    echo "  3. Run: git push -u origin main"
fi

# Test server locally
echo ""
echo "🧪 Testing server locally..."
echo "Starting server on port 8000..."
echo "(Press Ctrl+C to stop after a few seconds)"
echo ""

# Try to start server in background
python3 src/agents/web_ui.py &
SERVER_PID=$!

# Wait a bit for server to start
sleep 3

# Test health endpoint
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server started successfully!"
    echo "✅ Health check passed"
else
    echo "⚠️  Health check failed (this might be okay if server is still starting)"
fi

# Kill the test server
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo ""
echo "======================================"
echo "✅ Deployment Preparation Complete!"
echo "======================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Push to GitHub (if not done):"
echo "   git push -u origin main"
echo ""
echo "2. Deploy to cloud:"
echo ""
echo "   OPTION A: Render.com (Recommended)"
echo "   • Go to https://render.com"
echo "   • New → Blueprint"
echo "   • Connect your GitHub repo"
echo "   • Click 'Apply'"
echo "   • Get your link: https://synaptiverse.onrender.com"
echo ""
echo "   OPTION B: Railway.app"
echo "   • Go to https://railway.app"
echo "   • Deploy from GitHub"
echo "   • Generate domain"
echo "   • Get your link: https://synaptiverse.up.railway.app"
echo ""
echo "   OPTION C: Fly.io"
echo "   • Install: brew install flyctl"
echo "   • Run: flyctl launch --now"
echo "   • Get your link: https://synaptiverse.fly.dev"
echo ""
echo "3. Test your live site:"
echo "   • Visit: https://your-app-url.com"
echo "   • Test: Analyze symptoms"
echo "   • Check: /health endpoint"
echo ""
echo "4. Submit to hackathon:"
echo "   • Live demo: https://your-app-url.com"
echo "   • GitHub: $(git remote get-url origin 2>/dev/null || echo 'YOUR_GITHUB_URL')"
echo ""
echo "📖 Full guide: See DEPLOYMENT_GUIDE.md"
echo ""
echo "Good luck with your hackathon submission! 🍀"
