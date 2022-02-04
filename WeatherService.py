from datetime import date
from datetime import datetime
import pyowm

owm = pyowm.OWM("fc1d78e5bdb6e3e613600e91faa22e79")
mgr = owm.weather_manager()

reg = owm.city_id_registry()
#  list_of_locations = reg.locations_for('copenhagen', country='DK')
#  copenhagen = list_of_locations[0]
#  lon = copenhagen.lon
#  lat = copenhagen.lat
lon = 10.212030
lat = 56.158150

one_call = mgr.one_call(lat=lat, lon=lon)

now = datetime.now()
current_hour = int(now.strftime("%H"))
cloudiness = 0
visible = False


class WeatherService:
    def __init__(self, latitude, longitude):
        self.cloudiness = cloudiness
        self.visible = visible

    def hourlyclouds(self, hours):
        self.cloudiness = int(one_call.forecast_hourly[hours].clouds)

        if self.cloudiness < 25:
            self.visible = True

        return self.visible

    def dailyclouds(self, days):
        self.cloudiness = int(one_call.forecast_daily[days].clouds)

        if self.cloudiness < 25:
            self.visible = True

        return self.visible


aarhus = WeatherService(lat, lon)

print(aarhus.hourlyclouds(4))
print(aarhus.dailyclouds(4))
