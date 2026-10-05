from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from extensions import db
from models.mfa_factor import MfaFactor
from schemas.mfa_factor_schema import MfaFactorSchema


mfa_factor_schema = MfaFactorSchema()


class MfaFactorResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        factors = MfaFactor.query.filter_by(user_id=user_id).all()

        return {
            "items": mfa_factor_schema.dump(factors, many=True)
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        loaded = mfa_factor_schema.load(data)

        factor = MfaFactor(
            user_id=user_id,
            **loaded,
        )

        db.session.add(factor)
        db.session.commit()

        return mfa_factor_schema.dump(factor), 201

    @jwt_required()
    def patch(self, factor_id):
        user_id = get_jwt_identity()
        factor = MfaFactor.query.filter_by(
            id=factor_id,
            user_id=user_id,
        ).first()

        if not factor:
            return {"error": "MFA factor not found."}, 404

        data = request.get_json() or {}
        loaded = mfa_factor_schema.load(data, partial=True)

        for field, value in loaded.items():
            if field != "user_id":
                setattr(factor, field, value)

        db.session.commit()

        return mfa_factor_schema.dump(factor), 200

    @jwt_required()
    def delete(self, factor_id):
        user_id = get_jwt_identity()
        factor = MfaFactor.query.filter_by(
            id=factor_id,
            user_id=user_id,
        ).first()

        if not factor:
            return {"error": "MFA factor not found."}, 404

        db.session.delete(factor)
        db.session.commit()

        return {"message": "MFA factor removed successfully."}, 200
