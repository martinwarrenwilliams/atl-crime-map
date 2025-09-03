import sys
from pathlib import Path
# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime, timedelta
from src.data_loader import CrimeDataLoader
from dateutil.relativedelta import relativedelta
from config import config

st.set_page_config(
    page_title="Atlanta Crime Dashboard",
    page_icon="🚔",
    layout="wide"
)

@st.cache_resource
def load_crime_data():
    loader = CrimeDataLoader()
    loader.load_latest_data()
    return loader

loader = load_crime_data()
PRIMARY_ADDRESS = config.PRIMARY_ADDRESS

st.title("Atlanta Crime Statistics Dashboard")
st.subheader(f"Address: {PRIMARY_ADDRESS}")

# Date range filter
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime(2021, 1, 1),
        max_value=datetime.now()
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now(),
        max_value=datetime.now()
    )

# Filter data
filtered_df = loader.filter_by_address(PRIMARY_ADDRESS)

if start_date and end_date:
    mask = (filtered_df['OccurredFromDate'] >= pd.to_datetime(start_date)) & \
           (filtered_df['OccurredFromDate'] <= pd.to_datetime(end_date))
    filtered_df = filtered_df.loc[mask]

total_crimes = len(filtered_df)

if total_crimes == 0:
    st.warning("No data available for selected filters")
    st.stop()

# Map offenses to severity
crosswalk_path = str(config.SEVERITY_CROSSWALK_PATH)
if os.path.exists(crosswalk_path):
    severity_crosswalk = pd.read_csv(crosswalk_path)
    severity_dict = dict(zip(
        severity_crosswalk['offense_description'],
        severity_crosswalk['severity']
    ))
else:
    severity_dict = {}

filtered_df = filtered_df.copy()
filtered_df['severity'] = filtered_df['NIBRS_Offense'].map(severity_dict)
filtered_df['severity'] = filtered_df['severity'].fillna('Low')
filtered_df_for_severity = filtered_df[filtered_df['severity'] != 'Exclude']

# Overview metrics
start_dt = pd.to_datetime(start_date)
end_dt = pd.to_datetime(end_date)
rd = relativedelta(end_dt, start_dt)
duration_str = f"{rd.years} years, {rd.months} months"

# Build quarter range
q_start = start_dt.to_period('Q')
q_end = end_dt.to_period('Q')
quarter_index = pd.period_range(start=q_start, end=q_end, freq='Q')

# Average crimes per quarter
all_quarter_df = filtered_df.copy()
all_quarter_df['quarter'] = all_quarter_df['OccurredFromDate'].dt.to_period('Q')
all_counts = all_quarter_df.groupby('quarter').size().reindex(quarter_index, fill_value=0)
avg_crimes_per_quarter = float(all_counts.mean()) if len(all_counts) > 0 else 0.0

# High severity metrics
high_df = filtered_df_for_severity[filtered_df_for_severity['severity'] == 'High'].copy()
total_high = int(high_df.shape[0])
if not high_df.empty:
    high_df['quarter'] = high_df['OccurredFromDate'].dt.to_period('Q')
    high_counts = high_df.groupby('quarter').size().reindex(quarter_index, fill_value=0)
else:
    high_counts = pd.Series(0, index=quarter_index)
avg_high_per_quarter = float(high_counts.mean()) if len(high_counts) > 0 else 0.0

# Display overview stats
st.markdown("### Overview Statistics")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Duration", duration_str)
with col2:
    st.metric("Total Crimes", f"{total_crimes:,}")
with col3:
    st.metric("High Severity Crimes", f"{total_high:,}")
with col4:
    st.metric("Avg High Severity/Quarter", f"{avg_high_per_quarter:.1f}")
with col5:
    st.metric("Avg Crimes/Quarter", f"{avg_crimes_per_quarter:.1f}")

# Crime severity grouped chart
st.markdown("### Crimes by Severity Group")
severity_order = ['High', 'Medium', 'Low']
offense_counts_df = (
    filtered_df_for_severity
    .groupby(['severity', 'NIBRS_Offense'])
    .size()
    .reset_index(name='count')
)
offense_counts_df['severity'] = pd.Categorical(
    offense_counts_df['severity'], categories=severity_order, ordered=True
)

# Build y-axis order
y_order = []
for s in severity_order:
    subset = offense_counts_df[offense_counts_df['severity'] == s]
    subset = subset.sort_values('count', ascending=False)
    y_order.extend(subset['NIBRS_Offense'].tolist())

severity_grouped_fig = px.bar(
    offense_counts_df,
    x='count',
    y='NIBRS_Offense',
    color='severity',
    orientation='h',
    title='Crimes by Severity Group',
    labels={'count': 'Count', 'NIBRS_Offense': 'Crime Type', 'severity': 'Severity'},
    color_discrete_map={'High': '#dc3545', 'Medium': '#fd7e14', 'Low': '#ffc107'},
    category_orders={'severity': severity_order}
)
severity_grouped_fig.update_layout(
    height=600,
    showlegend=True,
    legend=dict(title='Severity', orientation='v', x=1.02, y=1),
    yaxis=dict(categoryorder='array', categoryarray=y_order, autorange='reversed')
)
st.plotly_chart(severity_grouped_fig, use_container_width=True)

# Severity definitions
with st.expander("View Severity Level Definitions"):
    st.markdown("""
    **High Severity (Violent Crimes)** - Crimes involving violence or threat of violence against persons:
    - Homicide
    - Rape / Sexual assault
    - Aggravated assault
    - Armed robbery (with weapon)
    
    **Medium Severity (Serious Property & Drug Crimes)** - Significant property loss/damage or serious drug offenses:
    - Burglary
    - Auto theft
    - Larceny-theft (large amounts)
    - Weapons charges
    - Drug trafficking
    
    **Low Severity (Minor Property & Nuisance Crimes)** - Minor offenses and public order violations:
    - Simple assault (no weapon, no serious injury)
    - Vandalism
    - Disorderly conduct
    - Trespassing
    - Public intoxication
    - Drug possession (personal use amounts)
    """)

# Time series and time of day charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Crime Trends Over Time (Quarterly)")
    time_data = loader.get_quarterly_time_series_data(PRIMARY_ADDRESS)
    if len(time_data) > 0:
        time_series_fig = go.Figure()
        time_series_fig.add_trace(go.Scatter(
            x=time_data['quarter_date'],
            y=time_data['count'],
            mode='lines+markers',
            name='Crimes',
            line=dict(color='#e74c3c', width=2),
            marker=dict(size=8),
            text=time_data['quarter_label'],
            customdata=time_data[['quarter_label', 'count']],
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Crimes: %{customdata[1]}<br>' +
                         '<extra></extra>'
        ))
        time_series_fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Number of Crimes",
            height=400,
            xaxis=dict(
                tickmode='array',
                tickvals=time_data['quarter_date'],
                ticktext=time_data['quarter_label'],
                tickangle=-45
            ),
            hovermode='x unified'
        )
        st.plotly_chart(time_series_fig, use_container_width=True)
    else:
        st.info("Insufficient data for time series")

with col2:
    st.markdown("### Crime by Time of Day")
    filtered_df['hour'] = filtered_df['OccurredFromDate'].dt.hour
    hour_counts = filtered_df['hour'].value_counts().sort_index()
    
    all_hours = pd.Series(0, index=range(24))
    all_hours.update(hour_counts)
    
    # Calculate day vs night percentages
    day_crimes = filtered_df[(filtered_df['hour'] >= 5) & (filtered_df['hour'] < 17)].shape[0]
    night_crimes = filtered_df[(filtered_df['hour'] >= 17) | (filtered_df['hour'] < 5)].shape[0]
    total_with_time = day_crimes + night_crimes
    
    if total_with_time > 0:
        day_percent = round((day_crimes / total_with_time) * 100, 1)
        night_percent = round((night_crimes / total_with_time) * 100, 1)
    else:
        day_percent = 0
        night_percent = 0
    
    time_df = pd.DataFrame({
        'hour': all_hours.index,
        'count': all_hours.values
    })
    
    time_of_day_fig = px.bar(
        time_df,
        x='hour',
        y='count',
        color='count',
        color_continuous_scale='Reds',
        labels={'hour': 'Hour of Day', 'count': 'Number of Crimes'}
    )
    time_of_day_fig.update_traces(
        hovertemplate='Hour: %{x}:00<br>Crimes: %{y}<extra></extra>'
    )
    time_of_day_fig.update_layout(
        height=400,
        showlegend=False,
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=2,
            tickformat='%d:00'
        )
    )
    st.plotly_chart(time_of_day_fig, use_container_width=True)
    
    # Day/Night statistics
    st.info(f"**Day (5am-5pm):** {day_percent}% | **Night (5pm-5am):** {night_percent}%")

# Crime details table
st.markdown("### Crime Details")
table_df = filtered_df[['IncidentNumber', 'OccurredFromDate', 'NIBRS_Offense', 
                        'LocationType', 'FireArmInvolved']].copy()
table_df['OccurredFromDate'] = table_df['OccurredFromDate'].dt.strftime('%Y-%m-%d %H:%M')
table_df = table_df.sort_values('OccurredFromDate', ascending=False)
table_df.columns = ['Incident #', 'Date/Time', 'Crime Type', 'Location Type', 'Firearm']

st.dataframe(
    table_df,
    use_container_width=True,
    height=500,
    hide_index=True
)