from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class ServiceRequest(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer, primary_key=True)
    problem_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    vehicle_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String(50), default="Pending")

    def to_dict(self):
        return {
            "id": self.id,
            "problem_type": self.problem_type,
            "location": self.location,
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id,
            "status": self.status
        }
        
class ServiceProvider(db.Model):
    __tablename__ = "service_providers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "location": self.location
        }