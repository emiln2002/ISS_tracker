from datetime import date
from datetime import datetime
import pyowm

owm = pyowm.OWM("fc1d78e5bdb6e3e613600e91faa22e79")
mgr = owm.weather_manager()

lon = 10.212030
lat = 56.158150


class WeatherService:
    def __init__(self, latitude, longitude, unix):
        self.one_call = mgr.one_call(lat=latitude, lon=longitude)
        self.cloudiness = 0
        self.visible = False
        self.hours = int(unix / 3600)
        self.days = int(unix / 86400)

    def getcloudiness(self):
        if 0 <= self.hours <= 47:
            self.cloudiness = int(self.one_call.forecast_hourly[self.hours].clouds)

        elif self.days <= 6:
            self.cloudiness = int(self.one_call.forecast_daily[self.days].clouds)

        else:
            return "Error: Unable to find weather info that far into the future."

        if self.cloudiness < 25:
            self.visible = True

        return self.visible


aarhus = WeatherService(lat, lon, 3235553)

print(aarhus.getcloudiness())
