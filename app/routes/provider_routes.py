from flask import Blueprint, request, jsonify
from app.models import ServiceProvider, ServiceRequest
from app import db

provider_bp = Blueprint("providers", __name__)


# REGISTER SERVICE PROVIDER
@provider_bp.route("/register", methods=["POST"])
def register_provider():

    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")

    if not name or not phone or not location:
        return jsonify({"error": "Missing fields"}), 400

    provider = ServiceProvider(
        name=name,
        phone=phone,
        location=location
    )

    db.session.add(provider)
    db.session.commit()

    return jsonify({
        "message": "Provider registered successfully",
        "provider": provider.to_dict()
    })


# VIEW ALL PENDING REQUESTS
@provider_bp.route("/requests", methods=["GET"])
def view_requests():

    requests = ServiceRequest.query.filter_by(status="Pending").all()

    return jsonify([r.to_dict() for r in requests])


# ACCEPT A SERVICE REQUEST
@provider_bp.route("/accept-request/<int:request_id>", methods=["PUT"])
def accept_request(request_id):

    request_obj = ServiceRequest.query.get(request_id)

    if not request_obj:
        return jsonify({"error": "Request not found"}), 404

    request_obj.status = "Accepted"
    db.session.commit()

    return jsonify({
        "message": "Request accepted successfully",
        "request": request_obj.to_dict()
    })