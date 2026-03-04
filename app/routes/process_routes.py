from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.process import Process
from app.models.audit_log import AuditLog
from app.extensions import db

process_bp = Blueprint("process", __name__)

@process_bp.route("/", methods=["POST"])
@jwt_required()
def create_process():
    identity = get_jwt_identity()
    # identity is user id string
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify(message="Campos 'title' y 'description' requeridos"), 422

    process = Process(title=title, description=description)
    db.session.add(process)
    db.session.commit()

    try:
        user_id = int(identity)
    except Exception:
        user_id = None
    log = AuditLog(user_id=user_id, action=f"Creó proceso {process.id}")
    db.session.add(log)
    db.session.commit()

    return jsonify(message="Proceso creado"), 201

@process_bp.route("/", methods=["GET"])
@jwt_required()
def list_processes():
    processes = Process.query.all()
    return jsonify([
        {"id": p.id, "title": p.title, "status": p.status}
        for p in processes
    ])