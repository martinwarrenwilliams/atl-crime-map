import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from lib.data_loader import CrimeDataLoader
from lib import config

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

st.title("Atlanta Crime Statistics")

# Initialize session state for selected location
if 'selected_address' not in st.session_state:
    st.session_state.selected_address = config.DEFAULT_LOCATION
    
# Create location selector
location_options = {f"{name} ({address})": address for address, name in config.LOCATIONS.items()}
selected_option = st.selectbox(
    "Select Location:",
    options=list(location_options.keys()),
    index=list(location_options.values()).index(st.session_state.selected_address),
    key='location_selector'
)

# Get the address from the selected option
selected_address = location_options[selected_option]
location_name = config.LOCATIONS[selected_address]

# Check if address changed
if selected_address != st.session_state.selected_address:
    st.session_state.selected_address = selected_address
    # Reset date filters when address changes
    if 'start_date_input' in st.session_state:
        del st.session_state.start_date_input
    if 'end_date_input' in st.session_state:
        del st.session_state.end_date_input
    st.rerun()

st.subheader(f"Location: {location_name}")
st.caption(f"Address: {selected_address}")

# Get the full data to determine min/max dates
full_df = loader.filter_by_address(selected_address)
min_date = full_df['OccurredFromDate'].min() if len(full_df) > 0 else datetime(2021, 1, 1)
max_date = full_df['OccurredFromDate'].max() if len(full_df) > 0 else datetime.now()

# Initialize session state for dates if not exists (using widget keys)
if 'start_date_input' not in st.session_state:
    st.session_state.start_date_input = min_date.date() if pd.notna(min_date) else datetime(2021, 1, 1).date()
if 'end_date_input' not in st.session_state:
    st.session_state.end_date_input = max_date.date() if pd.notna(max_date) else datetime.now().date()

# Date range filter with reset button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    start_date = st.date_input(
        "Start Date",
        min_value=min_date.date() if pd.notna(min_date) else datetime(2020, 1, 1).date(),
        max_value=datetime.now().date(),
        format="MM/DD/YYYY",
        key='start_date_input'
    )
with col2:
    end_date = st.date_input(
        "End Date",
        min_value=min_date.date() if pd.notna(min_date) else datetime(2020, 1, 1).date(),
        max_value=datetime.now().date(),
        format="MM/DD/YYYY",
        key='end_date_input'
    )
with col3:
    st.write("")  # Empty space for alignment
    if st.button("Reset Dates", type="secondary"):
        # Update the widget keys directly
        st.session_state.start_date_input = min_date.date() if pd.notna(min_date) else datetime(2021, 1, 1).date()
        st.session_state.end_date_input = max_date.date() if pd.notna(max_date) else datetime.now().date()
        st.rerun()
    
    # Display available date range as helper text
    if pd.notna(min_date) and pd.notna(max_date):
        st.caption(f"Available: {min_date.strftime(config.DISPLAY_DATE_FORMAT)} - {max_date.strftime(config.DISPLAY_DATE_FORMAT)}")

# Filter data
filtered_df = full_df.copy()

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
# Compact duration format
if rd.years > 0 and rd.months > 0:
    duration_str = f"{rd.years}y {rd.months}m"
elif rd.years > 0:
    duration_str = f"{rd.years}y"
elif rd.months > 0:
    duration_str = f"{rd.months}m"
else:
    days = (end_dt - start_dt).days
    duration_str = f"{days}d"

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
col1, col2, col3, col4, col5 = st.columns([1, 1, 1.2, 1, 1])
with col1:
    st.metric("Duration", duration_str)
with col2:
    st.metric("Total", f"{total_crimes:,}")
with col3:
    st.metric("High Severity", f"{total_high:,}")
with col4:
    st.metric("High/Qtr", f"{avg_high_per_quarter:.1f}")
with col5:
    st.metric("Total/Qtr", f"{avg_crimes_per_quarter:.1f}")

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
    time_data = loader.get_quarterly_time_series_data(selected_address, start_date, end_date)
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
# Sort by date BEFORE converting to string to ensure proper chronological order
table_df = table_df.sort_values('OccurredFromDate', ascending=False)
table_df['OccurredFromDate'] = table_df['OccurredFromDate'].dt.strftime(config.DISPLAY_DATETIME_FORMAT)
table_df.columns = ['Incident #', 'Date/Time', 'Crime Type', 'Location Type', 'Firearm']

st.dataframe(
    table_df,
    use_container_width=True,
    height=500,
    hide_index=True
)