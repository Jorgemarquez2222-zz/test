from app_public.app.geolocation.GeoPoint import GeoPoint


class LocationSearcher:
    def __init__(self, radius: int, max_number_results: int):
        self.radius = radius
        self.max_number_results = max_number_results

    def get_locations(self, geo_point: GeoPoint) -> list:
        pass
