import math
from math import sin, cos, tan, asin, acos, atan, pi

class Projection:
    def __init__(self, width=0, height=0):
        self.width = width;
        self.height = height;
        self.precision = 2
        self.centerLatitude = 0
        self.centerLongitude = 0
        self.centerX = width / 2
        self.centerY = height / 2

    def dimensions(self, width, height):
        self.width = width
        self.height = height
        self.centerX = width / 2
        self.centerY = height / 2
        return self

    def center(self, latitude, longitude):
        self.centerLatitude = math.radians(latitude)
        self.centerLongitude = math.radians(longitude)
        return self

    def formatGeoJSON(self, latitude, longitude):
        return (round(longitude, self.precision), round(latitude, self.precision))

    def toSphere(self, x, y):
        raise NotImplementedError
    def toPlane(self, latitude, longitude):
        raise NotImplementedError

class Mercator(Projection):
    def toSphere(self, x, y):
        x =  x - self.centerX
        y = -y + self.centerY
        lon = (x / self.centerX) * 180
        radius = self.width / (2 * math.pi)
        lat = math.degrees(2 * math.atan(math.exp(y / radius)) - math.pi/2)
        return self.formatGeoJSON(lat, lon)

class Equirectangular(Projection):
    def toSphere(self, x, y):
        x =  x - self.centerX
        y = -y + self.centerY
        lon = 180 * x / self.centerX
        lat =  90 * y / self.centerY
        return self.formatGeoJSON(lat, lon)

class AzimuthalEquidistant(Projection):
    def toSphere(self, x, y):
        x = (x - self.centerX) * 2 * pi / self.width
        y = (self.centerY - y) * 2 * pi / self.width
        c = math.sqrt(x**2 + y**2) # angular distance

        k = 0;
        if c != 0:
            k = y * sin(c) * cos(self.centerLatitude) / c
        latitude = asin(cos(c) * sin(self.centerLatitude) + k)
        longitude = 0;
        if self.centerLatitude == pi / 2:
            longitude = self.centerLongitude + math.atan2(-x, y)
        elif self.centerLatitude == -pi / 2:
            longitude = self.centerLongitude + math.atan2(x, y)
        else:
            longitude = self.centerLongitude + math.atan2(x * sin(c), c * cos(self.centerLatitude) * cos(c)  - y * sin(self.centerLatitude) * sin(c))

        return self.formatGeoJSON(math.degrees(latitude), math.degrees(longitude))

