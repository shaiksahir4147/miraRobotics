import json
from flask import Blueprint, request, jsonify
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
            return jsonify({"error": "Validation failed", "details": errors}), 400

        patient_id = create_patient(data)

        ai_result = predict_health(data)  # dict: risk, health_score, good_news, medical_advice, lifestyle, hospital

        update_remarks(patient_id, json.dumps(ai_result))

        return jsonify({
            "status": "success",
            "patient_id": patient_id,
            **ai_result
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

    errors = validate_patient(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

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

from datetime import datetime

def validate_patient(data):

    errors = []

    # Name
    if not data.get("name"):
        errors.append("Name is required")

    # Email
    email = data.get("email", "")
    if "@" not in email or "." not in email:
        errors.append("Invalid email format")

    # Date of Birth
    try:
        dob = datetime.strptime(
            data["dob"],
            "%Y-%m-%d"
        ).date()

        if dob > datetime.today().date():
            errors.append(
                "Date of birth cannot be a future date"
            )

    except:
        errors.append(
            "Invalid DOB format"
        )

    # Numeric values
    numeric_fields = [
        "blood_sugar",
        "cholesterol",
        "hemoglobin"
    ]

    for field in numeric_fields:
        try:
            float(data[field])
        except:
            errors.append(
                f"{field} must be numeric"
            )

    return errors