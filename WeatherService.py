import pyowm
from datetime import datetime

owm = pyowm.OWM("fc1d78e5bdb6e3e613600e91faa22e79")
mgr = owm.weather_manager()

reg = owm.city_id_registry()
list_of_locations = reg.locations_for('copenhagen', country='DK')
copenhagen = list_of_locations[0]
lon = copenhagen.lon
lat = copenhagen.lat

one_call = mgr.one_call(lat=lat, lon=lon)

now = datetime.now()
current_hour = int(now.strftime("%H"))


def hourlyclouds(hour):
    for i in range(48):
        print(f"{hour}: {one_call.forecast_hourly[i].clouds}% cloud cover")

        hour += 1

        if hour >= 24:
            hour = 0


hourlyclouds(current_hour)
