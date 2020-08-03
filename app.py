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
#sliderCategories = ['All', 'US','Russia', 'China']
sliderCategories = ['All']
#sliderValues =[0,1,2,3]
sliderValues =[0]

# Import Data
df = pandas.read_csv(dataFile)


# Initiate App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

fig = px.line(df, x='lon', y='altRelGEO', 
                color = 'operator', hover_name='name', line_group='name',
                labels={
                "lon": "Longitude (deg)",
                "altRelGEO": "Altitude Relative to GEO (km)",
                "operator": "Operator",
                "id": "Norad ID"
                    },
                hover_data=["id", "operator", "lon", "altRelGEO"],
                template = 'plotly_dark'
                )

# App Layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='geo', figure=fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()