# Quick Start Guide

## Run Locally

```bash
cd /Users/swagataashwani/Documents/linkedin_jobs
streamlit run app.py
```

Open browser to: http://localhost:8501

## Deploy Publicly (3 Steps)

### 1. Create GitHub Repo
Go to github.com → Create new **public** repository

### 2. Push Code
```bash
cd /Users/swagataashwani/Documents/linkedin_jobs
./deploy.sh
```
(Or follow prompts in the script)

### 3. Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repo → Set file: `app.py`
5. Click "Deploy"

**Done!** Your public URL: `https://YOUR_USERNAME-REPO_NAME.streamlit.app`

## Files You Need

✓ `app.py` - Main dashboard  
✓ `requirements.txt` - Dependencies  
✓ `data/linkedin_jobs.csv` - Dataset (3.2 MB)  
✓ `.gitignore` - Git configuration  

## Dashboard Features

- **15 interactive visualizations**
- **5 sidebar filters** (Experience, Salary, Location Type, Company, Job Category)
- **37,955 clean job records**
- **9 job categories** (Data Scientist, ML/AI Engineer, etc.)
- **Mobile responsive**

## Support

- Full guide: See `DEPLOYMENT_GUIDE.md`
- Issues: Create GitHub issue in your repo
- Streamlit docs: https://docs.streamlit.io

