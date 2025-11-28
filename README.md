# LinkedIn Jobs Market Analytics Dashboard

An interactive dashboard analyzing 37,955 LinkedIn job postings with salary and experience data.

## Features

### 10 Interactive Visualizations:

1. **Salary vs Experience Analysis** - Scatter plot with trend line showing correlation
2. **Salary by Career Level** - Bar chart with job counts by experience level
3. **Top Hiring Companies** - Analysis by job count and average salary
4. **Salary Distribution** - Histogram with percentile breakdowns
5. **Geographic Analysis** - Top states by salary with job counts
6. **Work Location Type** - Remote vs Hybrid vs On-site comparison
7. **Salary Box Plots** - Distribution analysis by career level
8. **Experience Requirements** - What experience do jobs require?
9. **Career Growth Trajectory** - Salary progression over 15 years
10. **Interactive Data Explorer** - Customizable charts with data download

### Interactive Filters:
- Years of Experience slider
- Salary Range slider
- Location Type selector
- Company filter (Top 50)

### Key Metrics:
- Total Jobs Count
- Median & Average Salary
- Average Experience Required
- Top Hiring Company

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Deploying to Streamlit Cloud (FREE & PUBLIC)

### Quick Deploy (Automated Script)

Run this command in your terminal:

```bash
cd /your-folder-location/linkedin_jobs
./deploy.sh
```

The script will guide you through the process!

### Manual Deploy (Step by Step)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**Quick Steps:**

1. **Create GitHub repository** (public) at github.com

2. **Push your code:**
```bash
cd /your-folder-location/linkedin_jobs
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

3. **Deploy on Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and `app.py`
   - Click "Deploy"

4. **Get your public URL:**
   ```
   https://YOUR_USERNAME-YOUR_REPO_NAME.streamlit.app
   ```

Your dashboard will be **publicly accessible** - anyone can view it without login!

## Data

- **Total Jobs**: 37,955
- **Columns**: job_title, company_name, location, salary, years_of_experience
- **Salary Range**: $20,000 - $925,350
- **Experience Range**: 0 - 40 years
- **Data Quality**: 100% complete (no null values)

## Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud (Free)

## License

Feel free to use and modify! Pls reach out - swagata1506@gmail.com

