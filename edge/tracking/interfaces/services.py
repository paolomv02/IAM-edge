from flask import Blueprint, request, jsonify
from tracking.application.services import TrackingRecordApplicationService
import os

tracking_api = Blueprint("tracking_api", __name__)

# Initialize with backend URL from environment variable
backend_url = os.getenv('BACKEND_URL', 'http://localhost:8080')
jwt_token = os.getenv('JWT_TOKEN')
tracking_service = TrackingRecordApplicationService(backend_url, jwt_token)

@tracking_api.route("/api/v1/tracking", methods=["POST"])
def create_tracking():
    """
    Create a new tracking record with authentication.
    Expected JSON: { "rfid_code": "...", "api_key": "...", "latitude": ..., "longitude": ..., "created_at": optional }
    """
    
    data = request.json
    try:
        rfid_code = data["rfid_code"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        speed = data["speed"]
        created_at = data.get("created_at")
        use_backend = data.get("use_backend", True)

        if use_backend:
            # Guardar local Y enviar al backend
            record = tracking_service.create_tracking_record_with_backend(
                rfid_code=rfid_code,
                api_key=request.headers.get("X-API-Key"),
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                created_at=created_at
            )
        else:
            # Solo guardar local
            record = tracking_service.create_tracking_record(
                rfid_code=rfid_code,
                api_key=request.headers.get("X-API-Key"),
                latitude=latitude,
                longitude=longitude,
                created_at=created_at
            )

        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "speed": record.speed,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@tracking_api.route('/api/v1/tracking', methods=['GET'])
def get_locations():
    """Get all tracking records (admin endpoint)."""
    locations = tracking_service.get_all_locations()
    return jsonify([
        {
            'id': loc.id,
            'device_id': loc.device_id,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'created_at': loc.created_at.isoformat() + "Z" if loc.created_at else None
        }
        for loc in locations
    ])