# Python Web App Demo - Pre-Process Data
# GEO Space Environment Display
# Jul 17 2020
# Jake Decoto (decotoj@gmail.com)

from collections import defaultdict
from numpy import arange
from sgp4.api import Satrec, jday
from math import sin, cos, degrees, radians, atan2, atan
from datetime import timezone
from datetime import datetime

# GEO Display - NEXT STEPS

# Color Dots by Country # PROTOTYPED
# User Select Filter (see country demo) # PROTOTYPED
# Orbit Trace (1 day 2-body) - PROTOTYPED
# Pre-Process Data & Test Web App Speed

# Config
tlefile = 'tle.txt'
t0 = [2020, 7, 7, 0, 0, 0] # Always start at 0 hour
op = defaultdict(str)
usa = ['TDRS','MUOS','USA','GOES']
rus = ['COSMOS', 'EXPRESS', 'LUCH', 'YAMAL', 'RADUGA']
chi = ['APSTAR','BEIDOU','GAOFEN','SHIJIAN','TIANLIAN','FENGYUN','CHINASAT','TJS','TIANTONG']
for q in usa:
    op[q] = 'US'
for q in rus:
    op[q] = 'Russia'
for q in chi:
    op[q] = 'China'
col = defaultdict(lambda:'gray')
col['Russia'] = 'yellow'
col['US'] = 'blue'
col['China'] = 'red'

def rot3(r, alpha):
    x = r[0]*cos(alpha) + r[1]*sin(alpha)
    y = r[0]*-sin(alpha) + r[1]*cos(alpha)
    z = r[2]*1
    return [x,y,z]

def TEMEtoECEF(r, t):
    baseEpoch = datetime(2016,9,14,6)
    baseEpoch = baseEpoch.replace(tzinfo=timezone.utc).timestamp()
    alphaBase = radians(-83.6488)
    unix = t.replace(tzinfo=timezone.utc).timestamp()
    d = (unix-baseEpoch) / 86400
    dAlpha = radians(d*-360.985647471)
    theta = alphaBase + dAlpha

    return rot3(r,-theta)

# Load and Parse Raw Data File
s = defaultdict(list) # Key is Feature
with open(tlefile, 'r') as f:
    ln = f.readlines()

# Extract Name and ID Values
a = [ln[i] for i in arange(0,len(ln),3)] # 1st Lines
b = [ln[i] for i in arange(1,len(ln),3)] # 2nd Lines
c = [ln[i] for i in arange(2,len(ln),3)] # 3rd Lines

# Derive Orbital Properties
for i in range(len(a)):

        satellite = Satrec.twoline2rv(b[i], c[i]) #sgp4 object

        for dt in arange(0,25,3): # hours

            dt2 = 0
            if dt > 23:
                dt2 = min(59,(dt-23)*60)
                dt = 23 

            jd, fr = jday(t0[0], t0[1], t0[2], t0[3]+dt, t0[4]+dt2, t0[5]) # Julian Day and Fractional Day
            t = datetime(t0[0], t0[1], t0[2], t0[3]+dt, t0[4]+dt2, t0[5]) # Datetime Object

            e, r, v = satellite.sgp4(jd, fr) # pos/vel in TEME frame
            
            # Altitude Relative to GEO (km)
            altRelGEO = (r[0]**2+r[1]**2+r[2]**2)**0.5-42164

            # Longitude (deg E)
            ecef = TEMEtoECEF(r, t)
            lon = degrees(atan2(ecef[1],ecef[0]))
            if lon < 0:
                lon += 360

            s['id'].append(b[i][2:7])
            s['name'].append(a[i].strip())
            s['dt'].append(dt*60+dt2)
        
            # Determine Color
            s['color'].append('gray')
            s['operator'].append('Other')
            for k in op.keys():
                if k in s['name'][-1]:
                    s['color'][-1] = col[op[k]]
                    s['operator'][-1] = op[k]
                    break

            s['altRelGEO'].append(altRelGEO) 
            s['lon'].append(lon)

#TEST1234
total = s['operator'].count('Other') + s['operator'].count('Russia') + s['operator'].count('US') + s['operator'].count('China')
print('Other: ', s['operator'].count('Other'))
print('Russia: ', s['operator'].count('Russia'))
print('US: ', s['operator'].count('US'))
print('China: ', s['operator'].count('China'))
print('\n', 'Check Sum', len(s['operator']), total)

# Output Data File
header = [','.join([k for k in s.keys()]) + '\n']
data = []
for i in range(len(s['id'])):
    tmp = ','.join([str(s[k][i]) for k in s.keys()])
    data.append(tmp+ '\n')

with open('data.csv', 'w') as f:
    f.writelines(header+data)

