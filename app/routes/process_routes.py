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
    processes = Process.query.order_by(Process.created_at.desc()).all()
    return jsonify([
        {"id": p.id, "title": p.title, "description": p.description, "status": p.status, "created_at": p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else ""}
        for p in processes
    ])


DEMO_PROCESSES = [
    {"title": "Aprobación de nómina Q1", "description": "Revisión y aprobación de planilla salarial del primer trimestre para 120 empleados."},
    {"title": "Cierre contable mensual", "description": "Proceso de reconciliación de cuentas y generación de estados financieros de marzo."},
    {"title": "Onboarding – Ana Rodríguez", "description": "Incorporación de nueva analista de datos: accesos, laptop, orientación y firma de contrato."},
    {"title": "Renovación contrato proveedor TI", "description": "Revisión legal y firma de renovación anual con Proveedor CloudServ por USD 48,000."},
    {"title": "Auditoría interna ISO 9001", "description": "Preparación de evidencias y reunión de revisión para certificación ISO 9001:2015."},
    {"title": "Migración VPN corporativa", "description": "Cambio de proveedor VPN de Cisco a Fortinet para 80 usuarios remotos."},
    {"title": "Capacitación RGPD equipos", "description": "Sesiones de formación en protección de datos para departamentos de Ventas y RRHH."},
    {"title": "Solicitud equipos Q2", "description": "Compra de 15 laptops y 3 servidores para expansión del equipo de desarrollo."}
]

STATUSES = ["pending", "in_progress", "completed", "completed", "in_progress", "pending", "completed", "in_progress"]


@process_bp.route("/demo", methods=["POST"])
@jwt_required()
def load_demo():
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except Exception:
        user_id = None

    if Process.query.count() >= 8:
        return jsonify(message="Demo ya cargado"), 200

    for i, item in enumerate(DEMO_PROCESSES):
        p = Process(title=item["title"], description=item["description"], status=STATUSES[i])
        db.session.add(p)

    db.session.commit()
    log = AuditLog(user_id=user_id, action="Cargó datos de demostración")
    db.session.add(log)
    db.session.commit()
    return jsonify(message="Demo cargado correctamente"), 201