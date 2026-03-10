from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ServiceRequest
from app import db

request_bp = Blueprint("requests", __name__)


# CREATE BREAKDOWN REQUEST
@request_bp.route("/create", methods=["POST"])
@jwt_required()
def create_request():
    data = request.get_json()

    problem_type = data.get("problem_type")
    location = data.get("location")
    vehicle_id = data.get("vehicle_id")

    # Validate input
    if not problem_type or not location or not vehicle_id:
        return jsonify({"error": "Missing fields"}), 400

    user_id = get_jwt_identity()

    new_request = ServiceRequest(
        problem_type=problem_type,
        location=location,
        vehicle_id=vehicle_id,
        user_id=user_id
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({
        "message": "Breakdown request created successfully",
        "request": new_request.to_dict()
    }), 201


# GET REQUESTS OF LOGGED-IN USER
@request_bp.route("/my-requests", methods=["GET"])
@jwt_required()
def get_my_requests():
    user_id = get_jwt_identity()

    # Get requests for the logged-in user (latest first)
    requests = ServiceRequest.query.filter_by(user_id=user_id) \
        .order_by(ServiceRequest.id.desc()) \
        .all()

    if not requests:
        return jsonify({
            "message": "No breakdown requests found"
        }), 404

    return jsonify({
        "count": len(requests),
        "requests": [req.to_dict() for req in requests]
    })

@request_bp.route("/update-status/<int:request_id>", methods=["PUT"])
@jwt_required()
def update_request_status(request_id):
    data = request.get_json()

    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    service_request = ServiceRequest.query.get(request_id)

    if not service_request:
        return jsonify({"error": "Request not found"}), 404

    service_request.status = new_status
    db.session.commit()

    return jsonify({
        "message": "Request status updated",
        "request": service_request.to_dict()
    })