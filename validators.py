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