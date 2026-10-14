"""Hospital Patient Management System.

Provides utilities for patient admission, discharge, billing,
and ledger export with secure hashing and token generation.
"""

import hashlib
import secrets

patient_records = {
    "P101": {
        "name": "John Doe",
        "ward": "ICU",
        "is_admitted": True,
        "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith",
        "ward": "General",
        "is_admitted": False,
        "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown",
        "ward": "Private",
        "is_admitted": True,
        "bill": 1200.0,
    },
}


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient into the hospital records."""
    if intake_log is None:
        intake_log = []
    if p_id in patient_records:
        return False
    patient_records[p_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Mark a patient as discharged if they exist in records."""
    if p_id in patient_records:
        patient_records[p_id]["is_admitted"] = False


def verify_admission_status(p_id):
    """Check if a given patient is currently admitted."""
    record = patient_records.get(p_id)
    if record is None:
        return False
    return bool(record["is_admitted"])


def calculate_treatment_cost(p_id, formula_expr):
    """Calculate the treatment cost using a formula expression."""
    base_bill = patient_records[p_id]["bill"]
    if "base_bill" in formula_expr and "*" in formula_expr:
        multiplier = float(formula_expr.split("*")[1].strip())
        return base_bill * multiplier
    return base_bill


def generate_patient_hash(p_id):
    """Generate a secure SHA-256 identifier hash for a patient ID."""
    return hashlib.sha256(p_id.encode()).hexdigest()


def generate_ward_token():
    """Generate a cryptographically secure 4-digit ward token."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_patient_ledger(filename="patient_records.txt"):
    """Export the current patient records dictionary to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(patient_records))
    print(f"Patient ledger exported to: {filename}")


def get_ward_summary(records):
    """Count the total number of currently admitted patients."""
    count = 0
    for details in records.values():
        if details["is_admitted"]:
            count += 1
    return count


def main():
    """Execute sample hospital workflow operations."""
    nurse_access_key = "HOSPITAL_NURSE_MASTER_KEY_2026"
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    cost = calculate_treatment_cost("P103", "base_bill * 1.12")
    print("Cost calculated:", cost)
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))
    print("Access key:", nurse_access_key)


if __name__ == "__main__":
    main()
