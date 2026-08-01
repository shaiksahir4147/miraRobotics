import json
from flask import Blueprint, request, jsonify
from validators import validate_patient
from health_service import predict_health

from patient_db import (
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
        errors = validate_patient(data)
        if errors:
            return jsonify({"error": "Validation failed ", "detials": errors}),400
        
        patient_id = create_patient(data)

        ai_result = predict_health(data)  # dict: risk, health_score, good_news, medical_advice, lifestyle, hospital

        # store as JSON text so it round-trips cleanly from the DB later
        update_remarks(patient_id, json.dumps(ai_result))

        return jsonify({
            "status": "success",
            "patient_id": patient_id,
            **ai_result  # flattens risk/health_score/good_news/etc to top level for the frontend
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

