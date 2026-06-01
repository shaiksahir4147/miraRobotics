from flask import Blueprint, request, jsonify
from routes.utils.validators import validate_patient
from routes.services.health_service import predict_health

from routes.database.patient_db import (
    create_patient,
    get_patients,
    get_patient,
    update_patient,
    delete_patient,
    update_remarks
)

prediction_bp = Blueprint(
    "prediction",
    __name__
)


# CREATE PATIENT
@prediction_bp.route(
    "/patients",
    methods=["POST"]
)
def create():
    try:
        data = request.get_json()

        print("Received Data:", data)

        patient_id = create_patient(data)

        remarks = predict_health(data)

        update_remarks(patient_id, remarks)

        return jsonify({
            "status": "success",
            "patient_id": patient_id,
            "remarks": remarks
        }), 201

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# UPDATE PATIENT
@prediction_bp.route(
    "/patients/<int:id>",
    methods=["PUT"]
)
def update(id):

    data = request.get_json()

    update_patient(
        id,
        data
    )

    return jsonify({
        "message": "Patient Updated"
    })


# DELETE PATIENT
@prediction_bp.route(
    "/patients/<int:id>",
    methods=["DELETE"]
)
def delete(id):

    delete_patient(id)

    return jsonify({
        "message": "Patient Deleted"
    })