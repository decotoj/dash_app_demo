# Python Web App Demo
# GEO Space Environment Display
# Jul 17 2020
# Jake Decoto (decotoj@gmail.com)

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas
from collections import defaultdict

# GEO Display - Future Enhancements
# 1. Intuitive Colors by Country 
# 2. More efficient filtering of data for user selected selector bar

# Config
tabtitle='GEO Satellites'
myheading='GEO Environment'
githublink='https://github.com/decotoj/dash_app_demo'
sourceurl='https://celestrak.com/'
dataFile = 'data.csv'
sliderCategories = ['All', 'US','Russia', 'China']
sliderValues =[0,1,2,3]

# Import Data
df = pandas.read_csv(dataFile)

# Apply Filter
df_rus = defaultdict(list)
indices = [i for i in range(len(df['id'])) if df['operator'][i].strip() == 'Russia']
for k in df.keys():
    df_rus [k] = [df[k][i] for i in indices]

df_us = defaultdict(list)
indices = [i for i in range(len(df['id'])) if df['operator'][i].strip() == 'US']
for k in df.keys():
    df_us [k] = [df[k][i] for i in indices]

df_chi = defaultdict(list)
indices = [i for i in range(len(df['id'])) if df['operator'][i].strip() == 'China']
for k in df.keys():
    df_chi [k] = [df[k][i] for i in indices]

# Initiate App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# App Layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='geo'
    ),
    dcc.Slider(
        id='operator-slider',
        min=min(sliderValues),
        max=max(sliderValues),
        value=min(sliderValues),
        marks=sliderCategories,
        step=None
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

# Callback Function for Slider
@app.callback(
    Output('geo', 'figure'),
    [Input('operator-slider', 'value')])

# Plot/Chart
def update_figure(selected_operator):

    # # Apply Filter
    selected_operator = sliderCategories[selected_operator]

    if selected_operator == 'All':
        df2 = df
    elif selected_operator == 'Russia':
        df2 = df_rus
    elif selected_operator == 'US':
        df2 = df_us
    elif selected_operator == 'China':
        df2 = df_chi

    fig = px.line(df2, x='lon', y='altRelGEO', 
                    color = 'operator', hover_name='name', line_group='name',
                    labels={
                    "lon": "Longitude (deg)",
                    "altRelGEO": "Altitude Relative to GEO (km)",
                    "operator": "Operator",
                    "id": "Norad ID"
                        },
                    hover_data=["id", "operator", "lon", "altRelGEO"]
                    )

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server()