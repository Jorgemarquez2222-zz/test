from django.test import TestCase
from app_public.app.geolocation.GeoPoint import GeoPoint


class TestGeoPoint(TestCase):
    def test_valid_latitude(self):
        self.assertTrue(GeoPoint.valid_latitude(0))
        self.assertTrue(GeoPoint.valid_latitude(45))
        self.assertFalse(GeoPoint.valid_latitude(-95.2))
        self.assertFalse(GeoPoint.valid_latitude(92.5))

    def test_valid_longitude(self):
        self.assertTrue(GeoPoint.valid_longitude(0))
        self.assertTrue(GeoPoint.valid_longitude(96))
        self.assertTrue(GeoPoint.valid_longitude(-130))
        self.assertFalse(GeoPoint.valid_longitude(-270))
        self.assertFalse(GeoPoint.valid_longitude(181))

    def test_distance_from(self):
        error_margin = 1 # KM
        lima_point = GeoPoint(-12.0432, -77.0282)
        huancayo_point = GeoPoint(-12.0651, -75.2049)
        distance = huancayo_point.distance_from(lima_point)
        self.assertTrue(abs(distance - 198) < error_margin) # error is about 1KM

        paris_point = GeoPoint(48.8534, 2.3488)
        london_point = GeoPoint(51.5085, -0.1257)
        distance = london_point.distance_from(paris_point)
        self.assertTrue(abs(distance - 341) < error_margin)