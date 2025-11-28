import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="LinkedIn Jobs Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    .stMetric label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
        font-size: 1.5rem !important;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
        padding-bottom: 10px;
    }
    h3 {
        color: #34495e;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to categorize job titles
def categorize_job_title(title):
    """Categorize job titles into standardized role types"""
    if pd.isna(title):
        return 'Other'
    
    title_lower = str(title).lower()
    
    # Data Scientist category
    if any(term in title_lower for term in ['data scientist', 'data science']):
        return 'Data Scientist'
    
    # Machine Learning / AI category
    elif any(term in title_lower for term in ['machine learning', 'ml engineer', 'ai engineer', 
                                                'ai architect', 'ml scientist', 'applied scientist']):
        return 'ML/AI Engineer'
    
    # Data Engineer category
    elif any(term in title_lower for term in ['data engineer', 'data infrastructure', 'data platform']):
        return 'Data Engineer'
    
    # Data Analyst category
    elif any(term in title_lower for term in ['data analyst', 'business analyst', 'analytics']):
        return 'Data Analyst'
    
    # Research Scientist category
    elif any(term in title_lower for term in ['research scientist', 'researcher']):
        return 'Research Scientist'
    
    # Product/Decision Scientist category
    elif any(term in title_lower for term in ['product scientist', 'decision scientist']):
        return 'Product/Decision Scientist'
    
    # Statistician category
    elif any(term in title_lower for term in ['statistician', 'biostatistician']):
        return 'Statistician'
    
    # Manager/Lead category
    elif any(term in title_lower for term in ['manager', 'director', 'head of', 'vp', 'chief']):
        return 'Manager/Lead'
    
    else:
        return 'Other'

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('data/linkedin_jobs.csv')
    
    # Create additional columns for analysis
    df['experience_level'] = pd.cut(df['years_of_experience'], 
                                     bins=[-1, 2, 5, 10, 50],
                                     labels=['Entry (0-2)', 'Mid (3-5)', 'Senior (6-10)', 'Expert (10+)'])
    
    df['salary_range'] = pd.cut(df['salary'], 
                                 bins=[0, 100000, 150000, 200000, 250000, 1000000],
                                 labels=['<$100k', '$100k-$150k', '$150k-$200k', '$200k-$250k', '>$250k'])
    
    # Extract location type
    df['location_type'] = df['location'].apply(lambda x: 
        'Remote' if 'Remote' in str(x) else 
        'Hybrid' if 'Hybrid' in str(x) else 
        'On-site' if 'On-site' in str(x) else 
        'Unknown')
    
    # Extract state from location
    df['state'] = df['location'].str.extract(r', ([A-Z]{2})')[0]
    
    # Categorize job roles
    df['job_category'] = df['job_title'].apply(categorize_job_title)
    
    return df

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.title("Filters")

# Experience filter
exp_range = st.sidebar.slider(
    "Years of Experience",
    min_value=int(df['years_of_experience'].min()),
    max_value=int(df['years_of_experience'].max()),
    value=(int(df['years_of_experience'].min()), int(df['years_of_experience'].max()))
)

# Salary filter
salary_range = st.sidebar.slider(
    "Salary Range (USD)",
    min_value=int(df['salary'].min()),
    max_value=int(df['salary'].max()),
    value=(int(df['salary'].min()), int(df['salary'].max())),
    step=10000,
    format="$%d"
)

# Location type filter
location_types = ['All'] + list(df['location_type'].unique())
selected_location_type = st.sidebar.selectbox("Location Type", location_types)

# Company filter
top_companies = ['All'] + list(df['company_name'].value_counts().head(50).index)
selected_company = st.sidebar.selectbox("Company (Top 50)", top_companies)

# Job category filter
job_categories = ['All'] + sorted(list(df['job_category'].unique()))
selected_category = st.sidebar.selectbox("Job Category", job_categories)

# Apply filters
filtered_df = df[
    (df['years_of_experience'] >= exp_range[0]) &
    (df['years_of_experience'] <= exp_range[1]) &
    (df['salary'] >= salary_range[0]) &
    (df['salary'] <= salary_range[1])
]

if selected_location_type != 'All':
    filtered_df = filtered_df[filtered_df['location_type'] == selected_location_type]

if selected_company != 'All':
    filtered_df = filtered_df[filtered_df['company_name'] == selected_company]

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['job_category'] == selected_category]

# Main title
st.title("LinkedIn Jobs Market Analytics Dashboard")
st.markdown(f"Analyzing **{len(filtered_df):,}** jobs from a dataset of **{len(df):,}** total positions")
st.markdown("**15 Interactive Visualizations** | Filter data using sidebar controls")

# Key metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Jobs", f"{len(filtered_df):,}")
    
with col2:
    st.metric("Median Salary", f"${filtered_df['salary'].median():,.0f}")
    
with col3:
    st.metric("Avg Salary", f"${filtered_df['salary'].mean():,.0f}")
    
with col4:
    st.metric("Avg Experience", f"{filtered_df['years_of_experience'].mean():.1f} yrs")
    
with col5:
    st.metric("Top Company", filtered_df['company_name'].value_counts().index[0] if len(filtered_df) > 0 else "N/A")

st.markdown("---")

# Visualization 1: Salary vs Experience Scatter Plot
st.header("1. Salary vs Experience Analysis")
col1, col2 = st.columns([3, 1])

with col1:
    fig1 = px.scatter(
        filtered_df, 
        x='years_of_experience', 
        y='salary',
        color='salary',
        color_continuous_scale='Viridis',
        hover_data=['job_title', 'company_name', 'location'],
        title='Salary vs Years of Experience (Hover for details)',
        labels={'years_of_experience': 'Years of Experience', 'salary': 'Salary (USD)'},
        height=500
    )
    
    # Add trend line
    z = np.polyfit(filtered_df['years_of_experience'], filtered_df['salary'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(filtered_df['years_of_experience'].min(), 
                          filtered_df['years_of_experience'].max(), 100)
    
    fig1.add_trace(go.Scatter(
        x=x_trend, 
        y=p(x_trend),
        mode='lines',
        name='Trend Line',
        line=dict(color='red', dash='dash', width=2)
    ))
    
    fig1.update_layout(showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Insights")
    correlation = filtered_df['years_of_experience'].corr(filtered_df['salary'])
    st.metric("Correlation", f"{correlation:.3f}")
    
    avg_increase = (filtered_df[filtered_df['years_of_experience'] > 5]['salary'].mean() - 
                   filtered_df[filtered_df['years_of_experience'] <= 5]['salary'].mean())
    st.metric("Salary Jump (5+ yrs)", f"${avg_increase:,.0f}")
    
    st.markdown(f"""
    **Key Findings:**
    - {len(filtered_df)} data points analyzed
    - Salary increases ~${z[0]:,.0f} per year
    - Strong positive correlation
    """)

st.markdown("---")

# Visualization 2: Average Salary by Experience Level
st.header("2. Salary by Career Level")

exp_level_stats = filtered_df.groupby('experience_level', observed=False).agg({
    'salary': ['mean', 'median', 'count']
}).round(0)
exp_level_stats.columns = ['Average Salary', 'Median Salary', 'Job Count']
exp_level_stats = exp_level_stats.reset_index()

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Bar(
        x=exp_level_stats['experience_level'],
        y=exp_level_stats['Average Salary'],
        name='Average Salary',
        marker_color='lightblue',
        text=exp_level_stats['Average Salary'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ),
    secondary_y=False
)

fig2.add_trace(
    go.Scatter(
        x=exp_level_stats['experience_level'],
        y=exp_level_stats['Job Count'],
        name='Job Count',
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(size=10)
    ),
    secondary_y=True
)

fig2.update_xaxes(title_text="Career Level")
fig2.update_yaxes(title_text="Average Salary (USD)", secondary_y=False)
fig2.update_yaxes(title_text="Number of Jobs", secondary_y=True)
fig2.update_layout(title="Average Salary and Job Count by Career Level", height=500)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Visualization 3: Top Companies Analysis
st.header("3. Top Hiring Companies")

col1, col2 = st.columns(2)

with col1:
    st.subheader("By Job Count")
    top_companies_count = filtered_df['company_name'].value_counts().head(20).reset_index()
    top_companies_count.columns = ['Company', 'Job Count']
    
    # Add average salary
    top_companies_count['Avg Salary'] = top_companies_count['Company'].apply(
        lambda x: filtered_df[filtered_df['company_name'] == x]['salary'].mean()
    )
    
    fig3a = px.bar(
        top_companies_count,
        y='Company',
        x='Job Count',
        orientation='h',
        color='Avg Salary',
        color_continuous_scale='RdYlGn',
        hover_data={'Avg Salary': ':$,.0f'},
        title='Top 20 Companies by Job Postings',
        height=600
    )
    fig3a.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3a, use_container_width=True)

with col2:
    st.subheader("By Average Salary")
    company_salary = filtered_df.groupby('company_name', observed=False).agg({
        'salary': 'mean',
        'job_title': 'count'
    }).reset_index()
    company_salary.columns = ['Company', 'Avg Salary', 'Job Count']
    company_salary = company_salary[company_salary['Job Count'] >= 5]  # At least 5 jobs
    company_salary = company_salary.nlargest(20, 'Avg Salary')
    
    fig3b = px.bar(
        company_salary,
        y='Company',
        x='Avg Salary',
        orientation='h',
        color='Job Count',
        color_continuous_scale='Blues',
        hover_data={'Job Count': True},
        title='Top 20 Highest Paying Companies (min 5 jobs)',
        height=600
    )
    fig3b.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3b, use_container_width=True)

st.markdown("---")

# Visualization 4: Salary Distribution
st.header("4. Salary Distribution Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    fig4 = go.Figure()
    
    fig4.add_trace(go.Histogram(
        x=filtered_df['salary'],
        nbinsx=50,
        name='Salary Distribution',
        marker_color='steelblue',
        opacity=0.7
    ))
    
    # Add median line
    median_salary = filtered_df['salary'].median()
    fig4.add_vline(
        x=median_salary, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Median: ${median_salary:,.0f}",
        annotation_position="top"
    )
    
    # Add mean line
    mean_salary = filtered_df['salary'].mean()
    fig4.add_vline(
        x=mean_salary, 
        line_dash="dash", 
        line_color="green",
        annotation_text=f"Mean: ${mean_salary:,.0f}",
        annotation_position="bottom"
    )
    
    fig4.update_layout(
        title='Salary Distribution with Median and Mean',
        xaxis_title='Salary (USD)',
        yaxis_title='Number of Jobs',
        height=500
    )
    
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("Percentiles")
    percentiles = [10, 25, 50, 75, 90, 95]
    perc_data = []
    for p in percentiles:
        value = filtered_df['salary'].quantile(p/100)
        perc_data.append({'Percentile': f'{p}th', 'Salary': f'${value:,.0f}'})
    
    perc_df = pd.DataFrame(perc_data)
    st.dataframe(perc_df, use_container_width=True, hide_index=True)
    
    st.subheader("Salary Ranges")
    salary_range_counts = filtered_df['salary_range'].value_counts().sort_index()
    for range_name, count in salary_range_counts.items():
        pct = (count / len(filtered_df)) * 100
        st.write(f"**{range_name}**: {count:,} jobs ({pct:.1f}%)")

st.markdown("---")

# Visualization 5: Geographic Analysis
st.header("5. Geographic Salary Analysis")

state_stats = filtered_df.groupby('state', observed=False).agg({
    'salary': ['mean', 'median', 'count']
}).round(0)
state_stats.columns = ['Avg Salary', 'Median Salary', 'Job Count']
state_stats = state_stats[state_stats['Job Count'] >= 50].sort_values('Avg Salary', ascending=False).head(20)
state_stats = state_stats.reset_index()

col1, col2 = st.columns([2, 1])

with col1:
    fig5 = px.bar(
        state_stats,
        x='state',
        y='Avg Salary',
        color='Job Count',
        color_continuous_scale='Plasma',
        hover_data=['Median Salary', 'Job Count'],
        title='Top 20 States by Average Salary (min 50 jobs)',
        labels={'state': 'State', 'Avg Salary': 'Average Salary (USD)'},
        height=500
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("Top States Table")
    display_df = state_stats[['state', 'Avg Salary', 'Job Count']].copy()
    display_df['Avg Salary'] = display_df['Avg Salary'].apply(lambda x: f'${x:,.0f}')
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

st.markdown("---")

# Visualization 6: Remote vs Hybrid vs On-site
st.header("6. Work Location Type Analysis")

col1, col2 = st.columns(2)

with col1:
    location_stats = filtered_df.groupby('location_type', observed=False).agg({
        'salary': ['mean', 'median', 'count']
    }).round(0)
    location_stats.columns = ['Average', 'Median', 'Count']
    location_stats = location_stats.reset_index()
    
    fig6a = go.Figure()
    
    fig6a.add_trace(go.Bar(
        x=location_stats['location_type'],
        y=location_stats['Average'],
        name='Average Salary',
        marker_color='lightblue',
        text=location_stats['Average'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig6a.add_trace(go.Bar(
        x=location_stats['location_type'],
        y=location_stats['Median'],
        name='Median Salary',
        marker_color='orange',
        text=location_stats['Median'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig6a.update_layout(
        title='Salary Comparison by Location Type',
        xaxis_title='Location Type',
        yaxis_title='Salary (USD)',
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig6a, use_container_width=True)

with col2:
    fig6b = px.pie(
        filtered_df,
        names='location_type',
        title='Distribution of Jobs by Location Type',
        hole=0.4,
        height=500
    )
    fig6b.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig6b, use_container_width=True)

st.markdown("---")

# Visualization 7: Salary Box Plot by Experience Level
st.header("7. Salary Distribution by Career Level")

fig7 = px.box(
    filtered_df,
    x='experience_level',
    y='salary',
    color='experience_level',
    points='outliers',
    title='Salary Distribution Box Plot by Career Level',
    labels={'experience_level': 'Career Level', 'salary': 'Salary (USD)'},
    height=600
)

fig7.update_layout(showlegend=False)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("""
**How to read this chart:**
- Box shows the middle 50% of salaries (25th to 75th percentile)
- Line in the box is the median
- Whiskers show the reasonable range
- Dots are outliers (unusually high/low salaries)
""")

st.markdown("---")

# Visualization 8: Experience Requirements Distribution
st.header("8. What Experience Do Jobs Require?")

col1, col2 = st.columns(2)

with col1:
    exp_dist = filtered_df['years_of_experience'].value_counts().sort_index().head(15)
    
    fig8a = go.Figure()
    fig8a.add_trace(go.Bar(
        x=exp_dist.index,
        y=exp_dist.values,
        marker_color='teal',
        text=exp_dist.values,
        textposition='outside'
    ))
    
    fig8a.update_layout(
        title='Job Count by Years of Experience Required',
        xaxis_title='Years of Experience',
        yaxis_title='Number of Jobs',
        height=500
    )
    
    st.plotly_chart(fig8a, use_container_width=True)

with col2:
    exp_level_dist = filtered_df['experience_level'].value_counts()
    
    fig8b = px.pie(
        values=exp_level_dist.values,
        names=exp_level_dist.index,
        title='Jobs by Career Level',
        hole=0.3,
        height=500
    )
    fig8b.update_traces(textposition='inside', textinfo='percent+label+value')
    st.plotly_chart(fig8b, use_container_width=True)

st.markdown("---")

# Visualization 9: Salary Growth Trajectory
st.header("9. Career Salary Growth Trajectory")

# Group by years of experience and calculate percentiles
exp_years = range(0, 16)
salary_data = []

for year in exp_years:
    year_data = filtered_df[filtered_df['years_of_experience'] == year]['salary']
    if len(year_data) >= 5:  # At least 5 data points
        salary_data.append({
            'years': year,
            '25th': year_data.quantile(0.25),
            '50th': year_data.quantile(0.50),
            '75th': year_data.quantile(0.75),
            'mean': year_data.mean(),
            'count': len(year_data)
        })

salary_trajectory_df = pd.DataFrame(salary_data)

if len(salary_trajectory_df) > 0:
    fig9 = go.Figure()
    
    # Add 75th percentile
    fig9.add_trace(go.Scatter(
        x=salary_trajectory_df['years'],
        y=salary_trajectory_df['75th'],
        name='75th Percentile',
        line=dict(color='lightblue', width=2),
        mode='lines'
    ))
    
    # Add median (50th percentile)
    fig9.add_trace(go.Scatter(
        x=salary_trajectory_df['years'],
        y=salary_trajectory_df['50th'],
        name='Median (50th)',
        line=dict(color='blue', width=3),
        mode='lines+markers'
    ))
    
    # Add 25th percentile
    fig9.add_trace(go.Scatter(
        x=salary_trajectory_df['years'],
        y=salary_trajectory_df['25th'],
        name='25th Percentile',
        line=dict(color='lightblue', width=2),
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(173, 216, 230, 0.2)'
    ))
    
    # Add mean
    fig9.add_trace(go.Scatter(
        x=salary_trajectory_df['years'],
        y=salary_trajectory_df['mean'],
        name='Average',
        line=dict(color='red', width=2, dash='dash'),
        mode='lines'
    ))
    
    fig9.update_layout(
        title='Salary Growth Trajectory (First 15 Years)',
        xaxis_title='Years of Experience',
        yaxis_title='Salary (USD)',
        height=600,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig9, use_container_width=True)
    
    st.markdown("""
    **Insights from the trajectory:**
    - Shaded area represents the middle 50% of earners
    - Median line shows typical salary progression
    - Steeper slopes indicate faster salary growth periods
    """)
else:
    st.warning("Not enough data to generate salary trajectory for filtered dataset")

st.markdown("---")

# NEW Visualization: Job Category Distribution
st.header("10. Job Category Distribution")

col1, col2 = st.columns(2)

with col1:
    category_counts = filtered_df['job_category'].value_counts().reset_index()
    category_counts.columns = ['Job Category', 'Count']
    
    fig_cat1 = px.pie(
        category_counts,
        values='Count',
        names='Job Category',
        title='Distribution of Jobs by Category',
        hole=0.4,
        height=500
    )
    fig_cat1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_cat1, use_container_width=True)

with col2:
    fig_cat2 = px.bar(
        category_counts,
        x='Count',
        y='Job Category',
        orientation='h',
        title='Job Count by Category',
        height=500,
        text='Count'
    )
    fig_cat2.update_traces(textposition='outside')
    fig_cat2.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_cat2, use_container_width=True)

st.markdown("---")

# NEW Visualization: Salary by Job Category
st.header("11. Salary Analysis by Job Category")

category_salary = filtered_df.groupby('job_category', observed=False).agg({
    'salary': ['mean', 'median', 'min', 'max', 'count']
}).round(0)
category_salary.columns = ['Average', 'Median', 'Min', 'Max', 'Count']
category_salary = category_salary[category_salary['Count'] >= 10]  # At least 10 jobs
category_salary = category_salary.sort_values('Median', ascending=False).reset_index()

col1, col2 = st.columns([2, 1])

with col1:
    fig_cat3 = go.Figure()
    
    fig_cat3.add_trace(go.Bar(
        y=category_salary['job_category'],
        x=category_salary['Median'],
        name='Median Salary',
        orientation='h',
        marker_color='lightblue',
        text=category_salary['Median'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig_cat3.add_trace(go.Bar(
        y=category_salary['job_category'],
        x=category_salary['Average'],
        name='Average Salary',
        orientation='h',
        marker_color='orange',
        text=category_salary['Average'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig_cat3.update_layout(
        title='Average vs Median Salary by Job Category',
        xaxis_title='Salary (USD)',
        yaxis_title='Job Category',
        barmode='group',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig_cat3, use_container_width=True)

with col2:
    st.subheader("Salary Statistics")
    
    # Create a styled dataframe
    display_salary_df = category_salary[['job_category', 'Median', 'Average', 'Count']].copy()
    display_salary_df.columns = ['Category', 'Median', 'Average', 'Jobs']
    display_salary_df['Median'] = display_salary_df['Median'].apply(lambda x: f'${x:,.0f}')
    display_salary_df['Average'] = display_salary_df['Average'].apply(lambda x: f'${x:,.0f}')
    
    st.dataframe(display_salary_df, use_container_width=True, hide_index=True, height=400)

st.markdown("---")

# NEW Visualization: Job Category vs Experience Requirements
st.header("12. Experience Requirements by Job Category")

category_exp = filtered_df.groupby('job_category', observed=False).agg({
    'years_of_experience': ['mean', 'median', 'count']
}).round(1)
category_exp.columns = ['Avg Experience', 'Median Experience', 'Job Count']
category_exp = category_exp[category_exp['Job Count'] >= 10]
category_exp = category_exp.sort_values('Median Experience', ascending=False).reset_index()

fig_cat4 = px.scatter(
    category_exp,
    x='Median Experience',
    y='Avg Experience',
    size='Job Count',
    color='job_category',
    hover_data=['Job Count'],
    title='Experience Requirements: Median vs Average (Bubble size = Job Count)',
    labels={'Median Experience': 'Median Years Required', 'Avg Experience': 'Average Years Required'},
    height=600
)

# Add diagonal line
max_exp = max(category_exp['Median Experience'].max(), category_exp['Avg Experience'].max())
fig_cat4.add_trace(go.Scatter(
    x=[0, max_exp],
    y=[0, max_exp],
    mode='lines',
    line=dict(color='red', dash='dash'),
    name='Equal Line',
    showlegend=True
))

st.plotly_chart(fig_cat4, use_container_width=True)

st.markdown("""
**Insight**: Points above the diagonal line indicate categories where the average experience 
is higher than median (influenced by high-experience outliers).
""")

st.markdown("---")

# NEW Visualization: Category Salary Heatmap
st.header("13. Salary Heatmap: Job Category vs Experience Level")

# Create pivot table
heatmap_data = filtered_df.groupby(['job_category', 'experience_level'], observed=False)['salary'].mean().reset_index()
heatmap_pivot = heatmap_data.pivot(index='job_category', columns='experience_level', values='salary')

# Filter to categories with data
heatmap_pivot = heatmap_pivot.dropna(how='all')

fig_cat5 = px.imshow(
    heatmap_pivot,
    labels=dict(x="Experience Level", y="Job Category", color="Avg Salary"),
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    color_continuous_scale='RdYlGn',
    aspect='auto',
    title='Average Salary Heatmap by Category and Experience Level',
    height=600
)

fig_cat5.update_xaxes(side="bottom")
fig_cat5.update_layout(
    xaxis_title="Experience Level",
    yaxis_title="Job Category"
)

st.plotly_chart(fig_cat5, use_container_width=True)

st.markdown("---")

# NEW Visualization: Top Companies by Job Category
st.header("14. Top Hiring Companies by Job Category")

selected_cat_for_companies = st.selectbox(
    "Select a job category to see top hiring companies:",
    sorted(filtered_df['job_category'].unique())
)

cat_filtered = filtered_df[filtered_df['job_category'] == selected_cat_for_companies]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top Companies Hiring {selected_cat_for_companies}")
    top_companies_cat = cat_filtered['company_name'].value_counts().head(15).reset_index()
    top_companies_cat.columns = ['Company', 'Job Count']
    
    fig_cat6a = px.bar(
        top_companies_cat,
        y='Company',
        x='Job Count',
        orientation='h',
        title=f'Top 15 Companies Hiring {selected_cat_for_companies}',
        height=500,
        text='Job Count'
    )
    fig_cat6a.update_traces(textposition='outside', marker_color='steelblue')
    fig_cat6a.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_cat6a, use_container_width=True)

with col2:
    st.subheader(f"Salary Distribution for {selected_cat_for_companies}")
    
    fig_cat6b = go.Figure()
    fig_cat6b.add_trace(go.Box(
        y=cat_filtered['salary'],
        name=selected_cat_for_companies,
        marker_color='lightblue',
        boxmean='sd'
    ))
    
    fig_cat6b.update_layout(
        title=f'{selected_cat_for_companies} Salary Distribution',
        yaxis_title='Salary (USD)',
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig_cat6b, use_container_width=True)
    
    # Show statistics
    st.metric("Median Salary", f"${cat_filtered['salary'].median():,.0f}")
    st.metric("Average Salary", f"${cat_filtered['salary'].mean():,.0f}")
    st.metric("Total Jobs", f"{len(cat_filtered):,}")

st.markdown("---")

# Visualization 15: Interactive Data Explorer
st.header("15. Interactive Data Explorer")

st.subheader("Customize Your Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    x_axis = st.selectbox(
        "X-axis",
        ['years_of_experience', 'salary', 'experience_level', 'location_type', 'job_category', 'company_name'],
        index=0
    )

with col2:
    y_axis = st.selectbox(
        "Y-axis",
        ['salary', 'years_of_experience'],
        index=0
    )

with col3:
    color_by = st.selectbox(
        "Color by",
        ['experience_level', 'salary_range', 'location_type', 'job_category', 'None'],
        index=0
    )

# Sample data if too many points
plot_df = filtered_df.sample(min(5000, len(filtered_df))) if len(filtered_df) > 5000 else filtered_df

if color_by == 'None':
    fig10 = px.scatter(
        plot_df,
        x=x_axis,
        y=y_axis,
        hover_data=['job_title', 'company_name', 'location', 'salary', 'years_of_experience'],
        title=f'{y_axis} vs {x_axis}',
        height=600
    )
else:
    fig10 = px.scatter(
        plot_df,
        x=x_axis,
        y=y_axis,
        color=color_by,
        hover_data=['job_title', 'company_name', 'location', 'salary', 'years_of_experience'],
        title=f'{y_axis} vs {x_axis} (colored by {color_by})',
        height=600
    )

st.plotly_chart(fig10, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>LinkedIn Jobs Market Analytics Dashboard</p>
    <p>Data Source: LinkedIn Job Postings | Total Dataset: 37,955 jobs</p>
    <p>Built with Streamlit and Plotly</p>
</div>
""", unsafe_allow_html=True)

