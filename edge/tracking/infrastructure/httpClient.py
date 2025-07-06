import requests
from typing import Dict, Any, Optional
import logging
import os

class BackendHttpClient:
    """HTTP client for communicating with deployed backend with JWT authentication."""
    
    def __init__(self, base_url: str, jwt_token: str = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.jwt_token = jwt_token or os.getenv('JWT_TOKEN')
        
        if not self.jwt_token:
            raise ValueError("JWT token is required. Set JWT_TOKEN environment variable or pass it directly.")
    
    def get_jwt_headers(self) -> Dict[str, str]:
        """Get headers with JWT token."""
        return {
            'Authorization': f'Bearer {self.jwt_token}',
            'Content-Type': 'application/json'
        }
        
    def get_wristband_by_rfid(self, rfid_code: str) -> Dict[str, Any]:
        """Get wristband data by RFID code."""
        try:
            url = f"{self.base_url}/api/v1/wristbands/rfid/{rfid_code}"
            headers = self.get_jwt_headers()
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get wristband data: {e}")
            raise ValueError(f"Wristband request failed: {str(e)}")
    
    def get_student_by_id(self, student_id: int) -> Dict[str, Any]:
        """Get student data by ID."""
        try:
            url = f"{self.base_url}/api/v1/students/{student_id}"
            headers = self.get_jwt_headers()
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get student data: {e}")
            raise ValueError(f"Student request failed: {str(e)}")
    
    def get_active_trips_by_driver(self, driver_id: int) -> list[Dict[str, Any]]:
        """Get active trips for a driver."""
        try:
            url = f"{self.base_url}/api/v1/trips/active/driver/{driver_id}"
            headers = self.get_jwt_headers()
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get active trips: {e}")
            raise ValueError(f"Active trips request failed: {str(e)}")
    
    def get_trip_by_id(self, trip_id: int) -> Dict[str, Any]:
        """Get trip data by ID."""
        try:
            url = f"{self.base_url}/api/v1/trips/{trip_id}"
            headers = self.get_jwt_headers()
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get trip data: {e}")
            raise ValueError(f"Trip request failed: {str(e)}")
    
    def post_tracking_to_backend(self, tracking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Post tracking record to backend."""
        try:
            url = f"{self.base_url}/api/v1/locations"
            headers = self.get_jwt_headers()
            response = self.session.post(url, json=tracking_data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to post tracking to backend: {e}")
            raise ValueError(f"Backend tracking post failed: {str(e)}")