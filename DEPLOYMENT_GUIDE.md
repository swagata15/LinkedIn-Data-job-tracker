# How to Deploy to Streamlit Cloud (FREE)

Follow these steps to publish your dashboard publicly so anyone can access it.

## Prerequisites
- GitHub account (free)
- Streamlit Cloud account (free - sign up with GitHub)

## Step-by-Step Deployment

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in:
   - **Repository name**: `linkedin-jobs-dashboard` (or any name you like)
   - **Description**: "Interactive LinkedIn Jobs Market Analytics Dashboard"
   - **Public** (select this - required for free Streamlit deployment)
   - **DO NOT** check "Initialize with README" (we already have files)
5. Click "Create repository"

### Step 2: Push Your Code to GitHub

Open Terminal and run these commands:

```bash
# Navigate to your project folder
cd /Users/swagataashwani/Documents/linkedin_jobs

# Initialize git repository
git init

# Add all files
git add app.py requirements.txt README.md data/linkedin_jobs.csv

# Commit the files
git commit -m "Initial commit: LinkedIn Jobs Analytics Dashboard"

# Add your GitHub repository (REPLACE with your actual GitHub username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/linkedin-jobs-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important**: Replace `YOUR_USERNAME` with your actual GitHub username!

If prompted for credentials, use your GitHub username and a Personal Access Token (not password).

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Click "Sign in with GitHub"

3. Authorize Streamlit to access your GitHub account

4. Click "New app" button

5. Fill in the deployment form:
   - **Repository**: Select your repository (e.g., `YOUR_USERNAME/linkedin-jobs-dashboard`)
   - **Branch**: `main`
   - **Main file path**: `app.py`
   
6. Click "Deploy!"

7. Wait 2-3 minutes for deployment (you'll see a progress indicator)

8. Once deployed, you'll get a public URL like:
   ```
   https://YOUR_USERNAME-linkedin-jobs-dashboard.streamlit.app
   ```

### Step 4: Share Your Dashboard

Your dashboard is now live! Share the URL with anyone:
- No login required for viewers
- Works on any device (mobile, tablet, desktop)
- Auto-updates if you push changes to GitHub

## Updating Your Dashboard

To update the dashboard after making changes:

```bash
cd /Users/swagataashwani/Documents/linkedin_jobs

# Make your changes to app.py or other files

# Commit and push
git add .
git commit -m "Description of your changes"
git push
```

Streamlit Cloud will automatically detect the changes and redeploy (takes 1-2 minutes).

## Troubleshooting

### If you get authentication errors:
1. Create a Personal Access Token on GitHub:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name and select "repo" scope
   - Copy the token
2. Use the token as your password when pushing to GitHub

### If deployment fails:
1. Check that `requirements.txt` is in your repository
2. Check that `data/linkedin_jobs.csv` is included
3. Look at the deployment logs in Streamlit Cloud for specific errors

### If the app loads slowly:
- This is normal for the first load (cold start)
- After first use, it loads much faster
- Consider upgrading to Streamlit Cloud paid tier for faster performance

## Custom Domain (Optional)

With Streamlit Cloud, you can:
1. Use the default URL: `*.streamlit.app`
2. Upgrade to paid plan to use custom domain

## Resource Limits (Free Tier)

- 1 GB RAM
- 1 CPU core
- Unlimited viewers
- Unlimited apps (but only 1 running at a time)

Your dashboard fits comfortably within these limits!

## Need Help?

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Forum: https://discuss.streamlit.io
- GitHub Issues: Create an issue in your repository

