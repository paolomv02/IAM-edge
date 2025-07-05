from flask import Blueprint, request, jsonify
from tracking.application.services import TrackingRecordApplicationService

tracking_api = Blueprint("tracking_api", __name__)
tracking_service = TrackingRecordApplicationService()

@tracking_api.route("/api/v1/tracking", methods=["POST"])
def create_tracking():
    """
    Create a new tracking record with authentication.
    Expected JSON: { "rfid_code": "...", "api_key": "...", "latitude": ..., "longitude": ..., "created_at": optional }
    """
    try:
        data = request.json
        rfid_code = data["rfid_code"]
        api_key = data["api_key"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        created_at = data.get("created_at")

        record = tracking_service.create_tracking_record(
            rfid_code=rfid_code,
            api_key=api_key,
            latitude=latitude,
            longitude=longitude,
            created_at=created_at
        )

        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "latitude": record.latitude,
            "longitude": record.longitude,
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

@tracking_api.route('/api/v1/tracking/my-locations', methods=['GET'])
def get_my_locations():
    """Get tracking records for authenticated device."""
    try:
        rfid_code = request.headers.get('X-RFID-Code')
        api_key = request.headers.get('X-API-Key')
        
        if not rfid_code or not api_key:
            return jsonify({"error": "Authentication headers required"}), 401

        locations = tracking_service.get_locations_by_device(rfid_code, api_key)
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

    except ValueError as e:
        return jsonify({"error": str(e)}), 401