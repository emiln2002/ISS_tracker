from astral import LocationInfo
from astral.sun import sun
import datetime
import pyowm
import time
#  Libraries needed to run this class.

owm = pyowm.OWM("fc1d78e5bdb6e3e613600e91faa22e79")
mgr = owm.weather_manager()
#  Stuff needed for OpenWeatherMap to work, including a subscription code.


class WeatherService:
    def __init__(self, latitude, longitude, unix):
        self.lat = latitude
        self.lon = longitude
        self.unix = int(unix)
        #  Class is asking for a latitude, longitude, and unix timestamp for the ISS's flyover.

        self.now = time.time()
        self.hours = int((self.unix - self.now) / 3600)
        self.days = int((self.unix - self.now) / 86400)
        #  Hours and days from now.

        self.year = int(datetime.datetime.fromtimestamp(self.unix).strftime("%Y"))
        self.month = int(datetime.datetime.fromtimestamp(self.unix).strftime("%m"))
        self.day = int(datetime.datetime.fromtimestamp(self.unix).strftime("%d"))
        self.minute = int(datetime.datetime.fromtimestamp(self.unix).strftime("%M"))
        self.hour = int(datetime.datetime.fromtimestamp(self.unix).strftime("%H"))
        if self.minute >= 30:
            self.hour += 1
        #  The year, month and day of the inputted unix timestamp.

        self.one_call = mgr.one_call(lat=self.lat, lon=self.lon)
        self.cloudiness = int()
        #  Location and cloud stuff for using OpenWeatherMap with PyOWM.

        self.loc = LocationInfo(timezone="Europe/London", latitude=self.lat, longitude=self.lon)
        self.s = sun(self.loc.observer, date=datetime.date(self.year, self.month, self.day))
        #  Location info stuff needed to find out when the sun goes up and down (thank you StackOverflow).
        self.sunup = str()
        self.sundown = str()
        self.uphour = int()
        self.downhour = int()
        #  Sun up/down stuff.

        self.visible = False
        #  Making the assumption that the night sky isn't visible.

    def clearsky(self):
        if self.hours < 0:
            return "Error: Negative timestamp"
        #  If the unix timestamp is in the past.

        elif 0 <= self.hours <= 47:
            self.cloudiness = int(self.one_call.forecast_hourly[self.hours].clouds)
        #  If the unix timestamp is within 48 hours from now, we can get an hourly cloud check.

        elif self.days <= 6:
            self.cloudiness = int(self.one_call.forecast_daily[self.days].clouds)
        #  If the unix timestamp is greater than 48 hours from now, we can get daily cloud checks for up to 7 days from
        #  now.

        else:
            return "Error: Timestamp too far into the future"
        #  We can't get any weather data further than a week from now.

        self.sunup = str(self.s["sunrise"]).split(" ")[1].split(".")[0]
        self.sundown = str(self.s["sunset"]).split(" ")[1].split(".")[0]
        #  Getting the time (hours:minutes:seconds) of sunset and sunrise on the day of the unix timestamp.

        self.uphour = int(self.sunup.split(":")[0])
        if int(self.sunup.split(":")[1]) >= 30:
            self.uphour += 1
        #  Getting the time of sunrise rounded to nearest hour.

        self.downhour = int(self.sundown.split(":")[0])
        if int(self.sundown.split(":")[1]) >= 30:
            self.downhour += 1
        #  Getting the time of sunset rounded to nearest hour.

        if self.cloudiness < 25 and (self.uphour > self.hour or self.downhour < self.hour):
            self.visible = True
        #  If there is less than 25% clouds and the unix time is before sunrise or after sunset.

        return self.visible
        #  Return a bool. True if the nightsky is visible.


aarhus = WeatherService(56.158150, 10.212030, 1644500918)

print(aarhus.clearsky())
