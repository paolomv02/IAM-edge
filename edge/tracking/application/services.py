from tracking.domain.entities import TrackingRecord
from tracking.domain.services import TrackingRecordService
from tracking.infrastructure.repositories import TrackingRecordRepository
from tracking.infrastructure.httpClient import BackendHttpClient
from iam.application.services import AuthApplicationService
from typing import Dict, Any, Optional
import os
from datetime import datetime

class TrackingRecordApplicationService:
    """Application service for vehicle tracking records."""

    def __init__(self, backend_url: str = None, jwt_token: str = None):
        self.tracking_repository = TrackingRecordRepository()
        self.tracking_service = TrackingRecordService()
        self.auth_service = AuthApplicationService()

        # Initialize HTTP client for backend communication
        self.backend_url = backend_url or os.getenv('BACKEND_URL', 'http://localhost:8080')
        self.http_client = BackendHttpClient(self.backend_url, jwt_token)

    def authenticate_device(self, rfid_code: str, api_key: str):
        """Authenticate device using IAM service."""
        return self.auth_service.get_device_by_code_and_key(rfid_code, api_key)
    
    def get_trip_data_from_rfid(self, rfid_code: str) -> Dict[str, Any]:
        """Get trip data from RFID following the complete chain."""
        try:
            # Step 1: Get wristband by RFID
            wristband_data = self.http_client.get_wristband_by_rfid(rfid_code)
            
            if not wristband_data.get('student'):
                raise ValueError("No student found for this RFID")
            
            student_id = wristband_data['student']['id']
            
            # Step 2: Get student details
            student_data = self.http_client.get_student_by_id(student_id)
            
            if not student_data.get('driverId'):
                raise ValueError("No driver assigned to this student")
            
            driver_id = student_data['driverId']
            
            # Step 3: Get active trips for driver
            active_trips = self.http_client.get_active_trips_by_driver(driver_id)
            
            if not active_trips:
                raise ValueError("No active trips found for this driver")
            
            # Assume we take the first active trip
            trip_id = active_trips[0]['id']
            
            # Step 4: Get trip details to get vehicle ID
            trip_data = self.http_client.get_trip_by_id(trip_id)
            
            if not trip_data.get('vehicleId'):
                raise ValueError("No vehicle assigned to this trip")
            
            return {
                'vehicle_id': trip_data['vehicleId'],
                'trip_id': trip_id,
                'student_data': student_data,
                'wristband_data': wristband_data,
                'trip_data': trip_data
            }
            
        except Exception as e:
            raise ValueError(f"Failed to get trip data: {str(e)}")

    def create_tracking_record_with_backend(self, rfid_code: str, api_key: str, latitude: float, longitude: float, speed: float = 0, created_at: str = None) -> TrackingRecord:
        """Create tracking record and post to backend with complete data chain."""
        
        # Authenticate device first
        device = self.authenticate_device(rfid_code, api_key)
        if not device:
            raise ValueError("Invalid authentication credentials")

        
        try:
            # Get trip data from RFID chain
            trip_data = self.get_trip_data_from_rfid(rfid_code)
            
            # Create local tracking record
            record = self.tracking_service.create_record(device.rfid_code, latitude, longitude, speed, created_at)
            saved_record = self.tracking_repository.save(record)
            
            # Prepare data for backend
            timestamp = created_at or datetime.now().isoformat() + "Z"
            backend_tracking_data = {
                'vehicleId': trip_data['vehicle_id'],
                'tripId': trip_data['trip_id'],
                'latitude': latitude,
                'longitude': longitude,
                'speed': speed,
                'timestamp': timestamp
            }
            
            # Post to backend
            backend_response = self.http_client.post_tracking_to_backend(backend_tracking_data)
            
            # Log successful backend post
            print(f"Successfully posted tracking to backend: {backend_response}")
            
            return saved_record
            
        except Exception as e:
            # If backend fails, still save locally
            print(f"Backend operation failed, saving locally only: {str(e)}")
            record = self.tracking_service.create_record(device.rfid_code, latitude, longitude, speed, created_at)
            return self.tracking_repository.save(record)

    def create_tracking_record(self, rfid_code: str, api_key: str, latitude: float, longitude: float, speed: float, created_at: str) -> TrackingRecord:
        """Create and persist a tracking record with authentication."""
        # Authenticate device first
        device = self.authenticate_device(rfid_code, api_key)
        if not device:
            raise ValueError("Invalid authentication credentials")
        
        # Use the device's RFID code as device_id
        record = self.tracking_service.create_record(device.rfid_code, latitude, longitude, speed, created_at)
        return self.tracking_repository.save(record)

    def get_all_locations(self) -> list[TrackingRecord]:
        return self.tracking_repository.get_all()
    
    def get_locations_by_device(self, rfid_code: str, api_key: str) -> list[TrackingRecord]:
        """Get tracking records for authenticated device."""
        device = self.authenticate_device(rfid_code, api_key)
        if not device:
            raise ValueError("Invalid authentication credentials")
        
        return self.tracking_repository.get_by_device_id(device.rfid_code)