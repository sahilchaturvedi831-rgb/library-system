# Deployment Guide for 24/7 Access

To make your Library Management System accessible 24/7 (even when your computer is off), follow these steps:

## Option 1: Deploy to Render.com (Free)

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `library-system`
3. Click "Create repository"

### Step 2: Upload Files
In a new terminal, run:
```
bash
cd C:/Users/yashc/Desktop
gh auth login
# Follow the prompts:
# - GitHub.com
# - HTTPS
# - Yes
# - Login with web browser

git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/library-system.git
git push -u origin main
```
Replace YOUR_USERNAME with your GitHub username.

### Step 3: Deploy to Render
1. Go to https://dashboard.render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Select your `library-system` repository
5. Configure:
   - Name: library-system
   - Build Command: (leave blank)
   - Start Command: `gunicorn app:app`
6. Click "Create Web Service"

### Step 4: Access Your App
- After deployment, Render will give you a URL like: `https://library-system.onrender.com`
- This link works 24/7!

---

## Option 2: Keep Using Local Server

Your current local server is running at:
- **Local:** http://localhost:5000
- **Network:** http://10.49.17.226:5000

The auto-start is already set up, so it will start automatically when you turn on your computer.
