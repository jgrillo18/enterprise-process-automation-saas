from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@jwt_required(optional=True)
def register():
    identity = get_jwt_identity()
    claims = get_jwt()
    # if any users exist, only admin can create new ones
    if User.query.count() > 0:
        if not identity or claims.get("role") != "admin":
            return jsonify(message="No autorizado"), 403
    data = request.json
    user = User(username=data["username"], role=data.get("role", "user"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="Usuario creado"), 201

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify(message="No autorizado"), 403
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ])

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify(message="Faltan credenciales"), 400

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            # use user id as identity and put role in additional claims
            token = create_access_token(
                identity=str(user.id),
                additional_claims={"role": user.role}
            )
            return jsonify(access_token=token)

        return jsonify(message="Credenciales inválidas"), 401
    except Exception:
        from flask import current_app
        current_app.logger.exception("Error en login")
        return jsonify(message="Error interno"), 500