from datetime import datetime

class TrackingRecord:
    """Domain entity representing a vehicle's GPS record."""

    def __init__(self, device_id: str, latitude: float, longitude: float, speed: float, created_at: datetime, id: int = None):
        self.id = id
        self.device_id = device_id
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.created_at = created_at
