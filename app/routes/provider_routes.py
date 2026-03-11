from flask import Blueprint, request, jsonify
from app import db
from app.models import ServiceProvider, ServiceRequest

provider_bp = Blueprint("providers", __name__)


# REGISTER A NEW SERVICE PROVIDER
@provider_bp.route("/register", methods=["POST"])
def register_provider():

    data = request.get_json()

    # Validate input
    if not data.get("name") or not data.get("phone") or not data.get("location"):
        return jsonify({"error": "Missing required fields"}), 400

    provider = ServiceProvider(
        name=data.get("name"),
        phone=data.get("phone"),
        location=data.get("location")
    )

    db.session.add(provider)
    db.session.commit()

    return jsonify({
        "message": "Provider registered successfully",
        "provider": provider.to_dict()
    }), 201


# GET ALL PROVIDERS
@provider_bp.route("/all", methods=["GET"])
def get_all_providers():

    providers = ServiceProvider.query.all()

    return jsonify({
        "count": len(providers),
        "providers": [p.to_dict() for p in providers]
    })


# VIEW ALL BREAKDOWN REQUESTS
@provider_bp.route("/requests", methods=["GET"])
def view_requests():

    requests = ServiceRequest.query.all()

    return jsonify({
        "count": len(requests),
        "requests": [r.to_dict() for r in requests]
    })


# PROVIDER ACCEPTS A REQUEST
@provider_bp.route("/accept-request/<int:request_id>", methods=["PUT"])
def accept_request(request_id):

    data = request.get_json()
    provider_id = data.get("provider_id")

    if not provider_id:
        return jsonify({"error": "provider_id is required"}), 400

    req = ServiceRequest.query.get(request_id)

    if not req:
        return jsonify({"error": "Request not found"}), 404

    req.provider_id = provider_id
    req.status = "accepted"

    db.session.commit()

    return jsonify({
        "message": "Request accepted successfully",
        "request": req.to_dict()
    })


# VIEW REQUESTS ASSIGNED TO A PROVIDER
@provider_bp.route("/assigned/<int:provider_id>", methods=["GET"])
def get_assigned_requests(provider_id):

    requests = ServiceRequest.query.filter_by(provider_id=provider_id).all()

    return jsonify({
        "count": len(requests),
        "requests": [r.to_dict() for r in requests]
    })