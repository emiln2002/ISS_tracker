import ephem
import datetime
from calendar import timegm
import requests
from math import degrees
import redis
import json
import os

lon = 10.1876224
lat = 56.1563259
alt = 40
n = 15
def getISSTLE():
    satellite = "ISS (ZARYA)"
    norad_url='https://www.celestrak.com/NORAD/elements/stations.txt'

    data = requests.get(norad_url).content.decode()
    lines = data.splitlines()

    issTLE=[]

    for index in range(len(lines)): #run through every line in the norad output.
        if satellite in lines[index]:
            issTLE.append(lines[index])
            issTLE.append(lines[index+1])
            issTLE.append(lines[index+2])

    #print(issTLE)
    return issTLE


def get_passes(lon, lat, alt, n):
    """Compute n number of passes of the ISS for a location"""

    # Get latest TLE from redis
    #tle = json.loads(r.get("iss_tle"))
    tle = getISSTLE()
    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    # Set location
    location = ephem.Observer()
    location.lat = str(lat)
    location.long = str(lon)
    location.elevation = alt

    # Override refration calculation
    location.pressure = 0
    location.horizon = '10:00'

    # Set time now
    now = datetime.datetime.utcnow()
    location.date = now

    # Predict passes
    passes = []
    for p in iter(range(n)):
        tr, azr, tt, altt, ts, azs = location.next_pass(iss)
        duration = int((ts - tr) * 60 * 60 * 24)
        year, month, day, hour, minute, second = tr.tuple()
        dt = datetime.datetime(year, month, day, hour, minute, int(second))

        if duration > 60:
            passes.append({"risetime": datetime.datetime.fromtimestamp(timegm(dt.timetuple())).strftime('%d-%m-%Y %H:%M:%S'), "duration": datetime.datetime.fromtimestamp(duration).strftime('%M:%S')})

        # Increase the time by more than a pass and less than an orbit
        location.date = tr + 25*ephem.minute

    # Return object
    obj = {"request": {
        "datetime": timegm(now.timetuple()),
        "latitude": lat,
        "longitude": lon,
        "altitude": alt,
        "passes": n,
        },
        "response": passes,
    }

    return obj

print(get_passes(lon, lat, alt, n))
