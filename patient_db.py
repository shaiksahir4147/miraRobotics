from routes.database.db import conn, cursor

# CREATE
def create_patient(data):
    query = """
        INSERT INTO patients
        (name,email,dob,gender,blood_sugar,cholesterol,hemoglobin,remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["name"],
        data["email"],
        data["dob"],
        data["gender"],
        data["blood_sugar"],
        data["cholesterol"],
        data["hemoglobin"],
        data.get("remarks", "")
    )

    cursor.execute(query, values)
    conn.commit()

    return cursor.lastrowid


# READ ALL
def get_patients():
    cursor.execute("SELECT * FROM patients")
    return cursor.fetchall()


# READ ONE
def get_patient(patient_id):
    query = "SELECT * FROM patients WHERE id=%s"
    cursor.execute(query, (patient_id,))
    return cursor.fetchone()


# UPDATE
def update_patient(patient_id, data):
    query = """
        UPDATE patients
        SET
            name=%s,
            email=%s,
            dob=%s,
            gender=%s,
            blood_sugar=%s,
            cholesterol=%s,
            hemoglobin=%s,
            remarks=%s
        WHERE id=%s
    """

    values = (
        data["name"],
        data["email"],
        data["dob"],
        data["gender"],
        data["blood_sugar"],
        data["cholesterol"],
        data["hemoglobin"],
        data["remarks"],
        patient_id
    )

    cursor.execute(query, values)
    conn.commit()


# DELETE
def delete_patient(patient_id):
    query = "DELETE FROM patients WHERE id=%s"
    cursor.execute(query, (patient_id,))
    conn.commit()

# UPDATE REMARKS
def update_remarks(patient_id, remarks):
    query = """
    UPDATE patients
    SET remarks = %s
    WHERE id = %s
    """
    cursor.execute(query, (remarks, patient_id))
    conn.commit()