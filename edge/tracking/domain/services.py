from datetime import datetime, timezone
from dateutil.parser import parse
from tracking.domain.entities import TrackingRecord

class TrackingRecordService:
    """Business logic for vehicle GPS tracking."""

    @staticmethod
    def create_record(device_id: str, latitude: float, longitude: float, created_at: str | None) -> TrackingRecord:
        try:
            lat = float(latitude)
            lon = float(longitude)

            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Invalid latitude or longitude values")

            if created_at:
                created_time = parse(created_at).astimezone(timezone.utc)
            else:
                created_time = datetime.now(timezone.utc)

        except Exception:
            raise ValueError("Invalid input format")

        return TrackingRecord(device_id, lat, lon, created_time)
