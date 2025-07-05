from tracking.domain.entities import TrackingRecord
from tracking.domain.services import TrackingRecordService
from tracking.infrastructure.repositories import TrackingRecordRepository
from iam.application.services import AuthApplicationService

class TrackingRecordApplicationService:
    """Application service for vehicle tracking records."""

    def __init__(self):
        self.tracking_repository = TrackingRecordRepository()
        self.tracking_service = TrackingRecordService()
        self.auth_service = AuthApplicationService()

    def authenticate_device(self, rfid_code: str, api_key: str):
        """Authenticate device using IAM service."""
        return self.auth_service.get_device_by_code_and_key(rfid_code, api_key)

    def create_tracking_record(self, rfid_code: str, api_key: str, latitude: float, longitude: float, created_at: str) -> TrackingRecord:
        """Create and persist a tracking record with authentication."""
        # Authenticate device first
        device = self.authenticate_device(rfid_code, api_key)
        if not device:
            raise ValueError("Invalid authentication credentials")
        
        # Use the device's RFID code as device_id
        record = self.tracking_service.create_record(device.rfid_code, latitude, longitude, created_at)
        return self.tracking_repository.save(record)

    def get_all_locations(self) -> list[TrackingRecord]:
        return self.tracking_repository.get_all()
    
    def get_locations_by_device(self, rfid_code: str, api_key: str) -> list[TrackingRecord]:
        """Get tracking records for authenticated device."""
        device = self.authenticate_device(rfid_code, api_key)
        if not device:
            raise ValueError("Invalid authentication credentials")
        
        return self.tracking_repository.get_by_device_id(device.rfid_code)