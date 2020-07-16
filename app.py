import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import defaultdict
from numpy import arange
from sgp4.api import Satrec, jday
from math import sin, cos, degrees, radians, atan2, atan
from datetime import timezone
from datetime import datetime

# GEO Display - NEXT
# Color Dots by Country
# User Select Filter (see country demo)
# Orbit Trace (1 day 2-body)


########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='GEO Web Display Test'
tabtitle='GEO Test'
myheading='GEO Environment'
label1='IBU'
label2='ABV'
githublink='https://github.com/decotoj/dash_app_demo'
sourceurl='https://celestrak.com/'
tlefile = 'tle.txt'
russian = ['Cosmos', 'COSMOS', 'cosmos']

def rot3(r, alpha):
    a = r[0]*cos(alpha) + r[1]*sin(alpha) + r[2]*0
    b = r[0]*-sin(alpha) + r[1]*cos(alpha) + r[2] * 0
    c = r[0]*0 + r[1]*0 + r[2]*1
    return [a,b,c]

def TEMEtoECEF(r, t):
    unix = t.replace(tzinfo=timezone.utc).timestamp()
    baseEpoch = datetime(2016,9,14,6)
    baseEpoch = baseEpoch.replace(tzinfo=timezone.utc).timestamp()
    alphaBase = radians(-83.6488)
    d = (unix-baseEpoch) / 86400
    dAlpha = radians(d*-360.985647471)
    theta = alphaBase + dAlpha
    S = rot3(r,-theta)

    return S

# Load and Parse Data File
s = defaultdict(list) # Key is Feature
with open(tlefile, 'r') as f:
    ln = f.readlines()
a = [ln[i] for i in arange(0,len(ln),3)]
b = [ln[i] for i in arange(1,len(ln),3)]
c = [ln[i] for i in arange(2,len(ln),3)]
s['id'] = [q[2:7] for q in b] # Norad ID
s['name'] = [q for q in a] # Common Name
for i in range(0,len(s['id'])):
        satellite = Satrec.twoline2rv(b[i], c[i])
        jd, fr = jday(2020, 7, 7, 12, 0, 0)
        e, r, v = satellite.sgp4(jd, fr) # pos/vel in TEME frame
        s['altRelGEO'].append((r[0]**2+r[1]**2+r[2]**2)**0.5-42164) # Altitude Relative to GEO (km)
        t = datetime(2020, 7, 7, 12, 0, 0)
        ecef = TEMEtoECEF(r, t)
        s['lon'].append(degrees(atan2(ecef[1],ecef[0]))) # Longitude (deg E)
        if s['lon'][-1] < 0:
            s['lon'][-1] += 360
        
        # Determine Color
        s['color'].append('gray')
        for q in russian:
            if q in s['name'][i]:
                s['color'][-1] = 'red'
                break


########### Set up the chart
# bitterness = go.Bar(
#     x=beers,
#     y=ibu_values,
#     name=label1,
#     marker={'color':color1}
# )
# alcohol = go.Bar(
#     x=beers,
#     y=abv_values,
#     name=label2,
#     marker={'color':color2}
# )

geoView = go.Scatter(
    x=s['lon'],
    y=s['altRelGEO'],
    name = 'GEO Environment',
    mode = 'markers',
    text = s['name'],
    marker_color = s['color']
)

#beer_data = [bitterness, alcohol, geoView]
beer_data = [geoView]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)


beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
