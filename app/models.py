from app import db


# =========================
# USER TABLE
# =========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationship
    requests = db.relationship("ServiceRequest", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


# =========================
# SERVICE REQUEST TABLE
# =========================
class ServiceRequest(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer, primary_key=True)

    problem_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    vehicle_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Provider who accepted the request
    provider_id = db.Column(
        db.Integer,
        db.ForeignKey("service_providers.id"),
        nullable=True
    )

    # Request status
    status = db.Column(db.String(50), default="pending")

    def to_dict(self):
        return {
            "id": self.id,
            "problem_type": self.problem_type,
            "location": self.location,
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id,
            "provider_id": self.provider_id,
            "status": self.status
        }


# =========================
# SERVICE PROVIDER TABLE
# =========================
class ServiceProvider(db.Model):
    __tablename__ = "service_providers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    # Requests handled by provider
    requests = db.relationship(
        "ServiceRequest",
        backref="provider",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "location": self.location
        }