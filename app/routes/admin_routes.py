from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.audit_log import AuditLog

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/logs", methods=["GET"])
@jwt_required()
def get_logs():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify(message="No autorizado"), 403

    logs = AuditLog.query.all()
    return jsonify([
        {"user_id": l.user_id, "action": l.action}
        for l in logs
    ])