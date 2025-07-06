from flask import Blueprint, request, jsonify
from iam.application.services import AuthApplicationService

iam_api = Blueprint("iam", __name__)
auth_service = AuthApplicationService()

@iam_api.route("/api/v1/register", methods=["POST"])
def register_device():
    data = request.json
    
    if not data or not data.get("rfid_code"):
        return jsonify({"error": "RFID code is required"}), 400
    
    rfid_code = data.get("rfid_code")
    
    # Verificar si el RFID code ya existe
    existing_device = auth_service.get_device_by_rfid_code(rfid_code)
    if existing_device:
        return jsonify({"error": "RFID code already registered"}), 409

    device = auth_service.register_rfid(rfid_code)

    return jsonify({
        "rfid_code": device.rfid_code,
        "api_key": device.api_key
    }), 201


