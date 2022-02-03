from datetime import date
from datetime import datetime
import pyowm

owm = pyowm.OWM("fc1d78e5bdb6e3e613600e91faa22e79")
mgr = owm.weather_manager()

reg = owm.city_id_registry()
list_of_locations = reg.locations_for('copenhagen', country='DK')
copenhagen = list_of_locations[0]
lon = copenhagen.lon
lat = copenhagen.lat

one_call = mgr.one_call(lat=lat, lon=lon)

now = datetime.now()
current_minute = int(now.strftime("%M"))
current_hour = int(now.strftime("%H"))
current_day = int(str(date.today()).split("-")[2])
current_month = int(str(date.today()).split("-")[1])
current_year = int(str(date.today()).split("-")[0])


class WeatherService:
    def __init__(self, latitude, longitude):
        self.minute = current_minute
        self.hour = current_hour
        self.day = current_day
        self.month = current_month
        self.year = current_month

    def hourlyclouds(self):
        for i in range(48):
            print(f"{self.hour}: {one_call.forecast_hourly[i].clouds}% cloud cover")

            self.hour += 1

            if self.hour >= 24:
                self.hour = 0


cph = WeatherService(lat, lon)
cph.minutelyclouds()
