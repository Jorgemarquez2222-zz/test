import logging
from math import radians, sin, cos, acos, sqrt

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


class GeoPoint:
    def __init__(self, latitude: float, longitude: float):
        if GeoPoint.valid_latitude(latitude):
            self.latitude = latitude
        else:
            logger.error("Latitude %f is not valid" % latitude)
            raise AttributeError("Invalid latitude value %f" % latitude)

        if GeoPoint.valid_longitude(longitude):
            self.longitude = longitude
        else:
            logger.error("Longitude %f is not valid" % longitude)
            raise AttributeError("Invalid longitude value %f" % longitude)

    @classmethod
    def valid_latitude(cls, latitude: float) -> bool:
        return -90 <= latitude < 90

    @classmethod
    def valid_longitude(cls, longitude: float) -> bool:
        return -180 <= longitude < 180

    def distance_from(self, point: 'GeoPoint') -> float:
        earth_radius = 6335.439
        latitude1 = radians(self.latitude)
        latitude2 = radians(point.latitude)
        delta_longitude = radians(point.longitude - self.longitude)
        return earth_radius * acos(sin(latitude1) * sin(latitude2) + cos(latitude1) * cos(latitude2) * cos(delta_longitude))

    def __str__(self):
        return "(%f,%f)" % self.latitude, self.longitude

