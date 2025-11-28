#!/bin/bash

# LinkedIn Jobs Dashboard Deployment Script
# This script helps you push your code to GitHub

echo "=========================================="
echo "LinkedIn Jobs Dashboard - GitHub Setup"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

echo ""
echo "Enter your GitHub username:"
read github_username

echo ""
echo "Enter your repository name (e.g., linkedin-jobs-dashboard):"
read repo_name

echo ""
echo "=========================================="
echo "Summary:"
echo "Username: $github_username"
echo "Repository: $repo_name"
echo "URL: https://github.com/$github_username/$repo_name"
echo "=========================================="
echo ""
echo "Make sure you've created this repository on GitHub first!"
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Add files
echo ""
echo "Adding files to git..."
git add app.py requirements.txt README.md DEPLOYMENT_GUIDE.md data/linkedin_jobs.csv .gitignore

# Commit
echo ""
echo "Committing files..."
git commit -m "Initial commit: LinkedIn Jobs Analytics Dashboard with 15 interactive visualizations"

# Set branch to main
echo ""
echo "Setting branch to main..."
git branch -M main

# Add remote
echo ""
echo "Adding remote repository..."
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin "https://github.com/$github_username/$repo_name.git"

# Push
echo ""
echo "Pushing to GitHub..."
echo "You may be prompted for your GitHub credentials."
echo "Use your GitHub username and Personal Access Token (not password)."
echo ""
git push -u origin main

echo ""
echo "=========================================="
echo "✓ Successfully pushed to GitHub!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select repository: $github_username/$repo_name"
echo "5. Set main file: app.py"
echo "6. Click Deploy!"
echo ""
echo "Your app will be live at:"
echo "https://$github_username-$repo_name.streamlit.app"
echo ""
echo "=========================================="

