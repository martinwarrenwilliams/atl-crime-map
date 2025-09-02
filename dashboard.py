import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
from datetime import datetime, timedelta
from data_loader import CrimeDataLoader

app = dash.Dash(__name__)

loader = CrimeDataLoader()
loader.load_latest_data()

PRIMARY_ADDRESS = "234 MEMORIAL DR SW"

app.layout = html.Div([
    html.Div([
        html.H1("Atlanta Crime Statistics Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.H3(f"Address: {PRIMARY_ADDRESS}", style={'textAlign': 'center', 'color': '#34495e'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H4("Overview Statistics", style={'color': '#2c3e50'}),
            html.Div(id='overview-stats')
        ], style={'width': '100%', 'padding': '20px', 'backgroundColor': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], style={'padding': '10px'}),
    
    html.Div([
        html.Div([
            html.H4("Date Range Filter", style={'color': '#2c3e50'}),
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=datetime(2021, 1, 1),
                end_date=datetime.now(),
                display_format='YYYY-MM-DD',
                style={'width': '100%'}
            )
        ], style={'padding': '20px', 'backgroundColor': 'white', 
                  'borderRadius': '10px', 'marginBottom': '20px'})
    ], style={'padding': '10px'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='crime-type-chart'),
            html.Div(id='crime-severity-box', style={
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'padding': '10px',
                'marginTop': '10px',
                'textAlign': 'center',
                'border': '1px solid #dee2e6'
            })
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='crime-severity-grouped-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='time-series-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='time-of-day-chart'),
            html.Div(id='time-stats-box', style={
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'padding': '10px',
                'marginTop': '10px',
                'textAlign': 'center',
                'border': '1px solid #dee2e6'
            })
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    html.Div([
        html.Div([
            html.H4("Crime Details", style={'color': '#2c3e50', 'padding': '10px'}),
            html.Div(id='crime-table-container', style={'paddingBottom': '50px'})
        ], style={'padding': '10px', 'backgroundColor': 'white', 
                  'borderRadius': '10px', 'margin': '20px', 'marginBottom': '80px'})
    ])
], style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh'})

@app.callback(
    [Output('overview-stats', 'children'),
     Output('crime-type-chart', 'figure'),
     Output('crime-severity-box', 'children'),
     Output('crime-severity-grouped-chart', 'figure'),
     Output('time-series-chart', 'figure'),
     Output('time-of-day-chart', 'figure'),
     Output('time-stats-box', 'children'),
     Output('crime-table-container', 'children')],
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_dashboard(start_date, end_date):
    filtered_df = loader.filter_by_address(PRIMARY_ADDRESS)
    
    if start_date and end_date:
        mask = (filtered_df['OccurredFromDate'] >= start_date) & (filtered_df['OccurredFromDate'] <= end_date)
        filtered_df = filtered_df.loc[mask]
    
    total_crimes = len(filtered_df)
    
    if total_crimes == 0:
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="No data available for selected filters",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        
        overview = html.Div([
            html.P(f"Total Crimes: 0", style={'fontSize': '18px', 'fontWeight': 'bold'})
        ])
        
        return overview, empty_fig, html.Div("No data available"), empty_fig, empty_fig, empty_fig, html.Div("No data available"), html.Div("No crimes found for this period")
    
    overview = html.Div([
        html.Div([
            html.Div([
                html.H2(str(total_crimes), style={'margin': '0', 'color': '#e74c3c'}),
                html.P("Total Crimes", style={'margin': '0'})
            ], style={'textAlign': 'center', 'width': '33.33%', 'display': 'inline-block'}),
            
            html.Div([
                html.H2(str(filtered_df['NIBRS_Offense'].nunique()), style={'margin': '0', 'color': '#3498db'}),
                html.P("Crime Types", style={'margin': '0'})
            ], style={'textAlign': 'center', 'width': '33.33%', 'display': 'inline-block'}),
            
            html.Div([
                html.H2(str((filtered_df['FireArmInvolved'] == 'yes').sum()), style={'margin': '0', 'color': '#f39c12'}),
                html.P("Firearm Involved", style={'margin': '0'})
            ], style={'textAlign': 'center', 'width': '33.33%', 'display': 'inline-block'})
        ])
    ])
    
    crime_types = filtered_df['NIBRS_Offense'].value_counts().sort_values(ascending=True).tail(10)
    crime_type_fig = px.bar(
        x=crime_types.values,
        y=crime_types.index,
        orientation='h',
        title=f"Top Crime Types at {PRIMARY_ADDRESS}",
        labels={'x': 'Count', 'y': 'Crime Type'},
        color=crime_types.values,
        color_continuous_scale='Reds'
    )
    crime_type_fig.update_layout(height=400, showlegend=False)
    
    # Load severity crosswalk
    crosswalk_path = os.path.join('data-processing', 'atl_ucr_nibrs_severity_crosswalk_full.csv')
    if os.path.exists(crosswalk_path):
        severity_crosswalk = pd.read_csv(crosswalk_path)
        severity_dict = dict(zip(
            severity_crosswalk['offense_description'], 
            severity_crosswalk['severity']
        ))
    else:
        severity_dict = {}
    
    # Create a copy to avoid SettingWithCopyWarning and calculate severity
    filtered_df = filtered_df.copy()
    
    # Apply severity classification
    filtered_df['severity'] = filtered_df['NIBRS_Offense'].map(severity_dict)
    filtered_df['severity'] = filtered_df['severity'].fillna('Low')
    
    # Remove any 'Exclude' severity entries
    filtered_df_for_severity = filtered_df[filtered_df['severity'] != 'Exclude']
    
    # Calculate severity percentages
    severity_counts = filtered_df_for_severity['severity'].value_counts()
    total_crimes_with_severity = severity_counts.sum()
    
    if total_crimes_with_severity > 0:
        high_percent = round((severity_counts.get('High', 0) / total_crimes_with_severity * 100), 1)
        medium_percent = round((severity_counts.get('Medium', 0) / total_crimes_with_severity * 100), 1)
        low_percent = round((severity_counts.get('Low', 0) / total_crimes_with_severity * 100), 1)
    else:
        high_percent = medium_percent = low_percent = 0
    
    # Function to get red gradient color based on percentage
    def get_red_gradient_color(percent):
        # Map 0-100% to gradient from light to dark red
        intensity = percent / 100
        # Using RGB interpolation for smooth gradient
        r = 254 - int(intensity * 115)  # 254 to 139
        g = 229 - int(intensity * 229)  # 229 to 0
        b = 229 - int(intensity * 229)  # 229 to 0
        return f'rgb({r}, {g}, {b})'
    
    # Create severity stats box
    severity_stats = html.Div([
        html.Span([
            html.B('High: ', style={'color': 'black'}),
            html.Span(f'{high_percent}%', style={
                'color': 'black',
                'fontSize': '16px',
                'fontWeight': 'bold'
            })
        ]),
        html.Span(' | ', style={'margin': '0 5px', 'color': '#6c757d'}),
        html.Span([
            html.B('Med: ', style={'color': 'black'}),
            html.Span(f'{medium_percent}%', style={
                'color': 'black',
                'fontSize': '16px',
                'fontWeight': 'bold'
            })
        ]),
        html.Span(' | ', style={'margin': '0 5px', 'color': '#6c757d'}),
        html.Span([
            html.B('Low: ', style={'color': 'black'}),
            html.Span(f'{low_percent}%', style={
                'color': 'black',
                'fontSize': '16px',
                'fontWeight': 'bold'
            })
        ])
    ])
    
    # Create severity-grouped chart
    # Group crimes by severity and crime type
    severity_crime_counts = filtered_df_for_severity.groupby(['severity', 'NIBRS_Offense']).size().reset_index(name='count')
    
    # Sort by severity order (High, Medium, Low) and count
    severity_order = ['High', 'Medium', 'Low']
    severity_crime_counts['severity'] = pd.Categorical(severity_crime_counts['severity'], 
                                                       categories=severity_order, 
                                                       ordered=True)
    severity_crime_counts = severity_crime_counts.sort_values(['severity', 'count'], ascending=[False, True])
    
    # Create the grouped bar chart
    severity_grouped_fig = px.bar(
        severity_crime_counts,
        x='count',
        y='NIBRS_Offense',
        color='severity',
        orientation='h',
        title='Crimes by Severity Group',
        labels={'count': 'Count', 'NIBRS_Offense': 'Crime Type', 'severity': 'Severity'},
        color_discrete_map={'High': '#dc3545', 'Medium': '#fd7e14', 'Low': '#ffc107'},
        category_orders={'severity': severity_order}
    )
    
    # Update layout to show all crimes without bundling
    severity_grouped_fig.update_layout(
        height=600,  # Taller to show all crime types
        showlegend=True,
        legend=dict(title='Severity', orientation='v', x=1.02, y=1),
        yaxis=dict(categoryorder='total ascending')  # Order by total count
    )
    
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
    
    # Create dataframe for plotly express
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
        title="Crime by Time of Day",
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
    
    # Create the statistics box content
    time_stats = html.Div([
        html.Span([
            html.B('Day (5am-5pm): ', style={'color': 'black'}),
            html.Span(f'{day_percent}%', style={
                'color': get_red_gradient_color(day_percent),
                'fontSize': '18px',
                'fontWeight': 'bold'
            })
        ]),
        html.Span(' | ', style={'margin': '0 10px', 'color': '#6c757d'}),
        html.Span([
            html.B('Night (5pm-5am): ', style={'color': 'black'}),
            html.Span(f'{night_percent}%', style={
                'color': get_red_gradient_color(night_percent),
                'fontSize': '18px',
                'fontWeight': 'bold'
            })
        ])
    ])
    
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
            title="Crime Trends Over Time (Quarterly)",
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
    else:
        time_series_fig = go.Figure()
        time_series_fig.add_annotation(
            text="Insufficient data for time series",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    table_df = filtered_df[['IncidentNumber', 'OccurredFromDate', 'NIBRS_Offense', 
                            'LocationType', 'FireArmInvolved']].copy()
    table_df['OccurredFromDate'] = table_df['OccurredFromDate'].dt.strftime('%Y-%m-%d %H:%M')
    table_df = table_df.sort_values('OccurredFromDate', ascending=False)
    
    crime_table = dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[
            {'name': 'Incident #', 'id': 'IncidentNumber'},
            {'name': 'Date/Time', 'id': 'OccurredFromDate'},
            {'name': 'Crime Type', 'id': 'NIBRS_Offense'},
            {'name': 'Location Type', 'id': 'LocationType'},
            {'name': 'Firearm', 'id': 'FireArmInvolved'}
        ],
        virtualization=True,
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {'column_id': 'FireArmInvolved', 'filter_query': '{FireArmInvolved} = yes'},
                'backgroundColor': '#ffcccc'
            }
        ],
        style_table={
            'height': '500px',
            'overflowY': 'auto'
        },
        sort_action='native',
        filter_action='native'
    )
    
    return overview, crime_type_fig, severity_stats, severity_grouped_fig, time_series_fig, time_of_day_fig, time_stats, crime_table

if __name__ == '__main__':
    print(f"Starting dashboard for {PRIMARY_ADDRESS}...")
    print("Dashboard will be available at http://127.0.0.1:8050/")
    app.run_server(debug=True)