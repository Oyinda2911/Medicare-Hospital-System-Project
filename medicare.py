import sqlite3
from datetime import datetime
import re
import os
connection = sqlite3.connect("medicare.db")
cursor = connection.cursor()
# cursor.execute("PRAGMA foreign_key = ON")
# cursor.execute("PRAGMA table_info(medical_records)")
# print(cursor.fetchall())

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    address TEXT NOT NULL,
    blood_group TEXT NOT NULL,
    date_registered TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    availability_status TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medical_records (
    record_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    diagnosis TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    prescription TEXT NOT NULL,
    notes TEXT NOT NULL,
    date_of_visit TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)

""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS billing (
    bill_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    consultation_fee REAL NOT NULL,
    medication_cost REAL NOT NULL,
    other_charges REAL NOT NULL,
    discount REAL NOT NULL,
    subtotal REAL NOT NULL,
    total_amount REAL NOT NULL,
    amount_paid REAL NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
""")
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = cursor.fetchall()
# print("Tables in Medicare Database:")
# for table in tables:
#     print(table[0])
# connection.close


# create the registration function
def register_patients():
    print("\n---Patient Registration---")
    patient_id = int(input("Enter Patient ID: "))
    full_name = input("Enter full Name: ")
    email = input("Enter Email: ")
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        print("Invalid email address.")
        return #basically maens stop this function right here
    phone = input("Enter Phone Number: ")
    phone_pattern = r"^(0[789][01]\d{8}|\+234[789][01]\d{8})$"
    if not re.match(phone_pattern, phone):
        print("Invalid phone number")
        return
    date_of_birth = input("Enter Date of Birth (YYY-MM-DD): ")
    date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
    today = datetime.now()
    age = today.year - date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth):
        age -= 1
        print("patient age:", age)
    gender = input("Enter gender: ")
    address = input("Enter Address: ")
    blood_group = input("Enter Blood Group: ")
    date_registered = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO patients (
        patient_id,
        full_name,
        email,
        phone,
        date_of_birth,
        gender,
        address,
        blood_group,
        date_registered
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    patient_id,
    full_name,
    email,
    phone,
    date_of_birth.strftime("%Y-%m-%d"),
    gender,
    address,
    blood_group,
    date_registered
))
    connection.commit()
    print("Patient registered sucessfully.")


def view_patients():
    print("\n--------Registered Patients--------")
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    for p in patients:
        print(p)
# view_patients()

def add_doctor():
    print("\n---- Add Doctor ----")
    doctor_id = int(input("Enter Doctor ID: "))
    full_name = input("Enter Full Name: ")
    specialization = input("Enter Specialization: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")
    availability_status = input("Enter Availability status: ")


    cursor.execute("""
INSERT INTO doctors (
    doctor_id,
    full_name,
    specialization,
    email,
    phone,
    availability_status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        doctor_id,
        full_name,
        specialization,
        email,
        phone,
        availability_status

    ))

    connection.commit()
    print("Doctor added successfully.")
# add_doctor()

def view_doctors():
    print("\n---- Registered Doctors ----")
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    for doctor in doctors:
        print(doctor)
# view_doctors()

def search_doctors():
    print("\n---- Search Doctors ----")
    doctor_id = int(input("Enter ID to search: "))
    cursor.execute(
        "SELECT * FROM doctors WHERE doctor_id = ?",
        (doctor_id,)
    )
    doctor = cursor.fetchone()
    if doctor:
        print("Doctor found: ")
        print(doctor)
    else:
        print("Doctor not found.")
# search_doctors()

def update_doctor():
    print("\n---- Update Doctor ----")
    doctor_id = int(input("Enter Doctor ID to update: "))
    full_name = input("Enter New Full Name: ")
    specialization = input("Enter New Specialization: ")
    email = input("Enter New Email: ")
    phone = input("Enter New Phone Number: ")
    availability_status = input("Enter New Availability: ")
    cursor.execute("""
    UPDATE doctors
    SET full_name = ?,
        specialization = ?,
        email = ?,
        phone = ?,
        availability_status = ?
    WHERE doctor_id = ?
    """, (
        full_name,
        specialization,
        email,
        phone,
        availability_status,
        doctor_id
    ))
    connection.commit()
    print("Doctor update successfully.")
# update_doctor()

def remove_doctor():
    print("---- Remove Doctor ----")
    doctor_id = int(input("Enter Doctor ID to remove: "))
    cursor.execute(
        "DELETE FROM doctors WHERE doctor_id =?",
        (doctor_id,)
    )
    connection.commit()
    print("Doctor removed successfully.")
# remove_doctor()

def book_appointment():
    print("--- Book Appointment ----")
    appointment_id = int(input("Enter Appointment ID: "))
    patient_id = int(input("Enter Patient ID: "))
    doctor_id = int(input("Enter Doctor ID: "))
    appointment_date = input("Enter Appointment Date: ")
    appointment_time = input("Enter Appointment Time: ")
    reason = input("Enter Reason for the Appointment: ")
    status = "Scheduled"
    appointment_datetime = datetime.strptime(
        appointment_date + " " + appointment_time,
        "%Y-%m-%d %H:%M"
    )
    if appointment_datetime < datetime.now():
        print("Appointment date and time cannot be in the past.")
        return


    cursor.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,)
)
    if cursor.fetchone() is None:
        print("Patient does not exist.")
        return
   
    cursor.execute(
        "SELECT doctor_id FROM doctors WHERE doctor_id = ?",
        (doctor_id,)
    )

    if cursor.fetchone() is None:
        print("Doctor does not exist.")
        return

    cursor.execute("""
        SELECT appointment_id
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND status = "Scheduled"
    """, (doctor_id, appointment_date, appointment_time))
    existing_appointment = cursor.fetchone()
    if existing_appointment is not None:
        print("Doctor is already booked at this time.")
        return

    cursor.execute("""
    INSERT INTO appointments (
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    appointment_id,
    doctor_id,
    patient_id,
    appointment_date,
    appointment_time,
    reason,
    status
    ))
    connection.commit()
    print("Appointment booked successfully.")

def view_appointments():
    print("\n--- Appointments ----")
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    if len(appointments) == 0:
        print("No appointment found.")
    else:
        for appointment in appointments:
            print(appointment)
    # cursor.execute("SELECT * FROM appointments")
    # appointments = cursor.fetchall()
    # if len(appointments) == 0:
    #     print("No appointment found.")
    # else:
    #     for appointment in appointments:
    #         print(appointment)   

def add_medical_record():   
    cursor.execute("PRAGMA table_info(medical_records)")
    print("MEDICAL RECORD COLUMNS:")
    print(cursor.fetchall()) 
    print("\n---- Add Medical Record ----")
    record_id = int(input("Enter Record ID: "))
    patient_id = int(input("Enter Patient ID: "))
    doctor_id = int(input("Enter Doctor ID: "))
    diagnosis = input("Enter Diagnosis: ")
    symptoms = input("Enter Symptoms: ")
    prescription = input("Enter Prescription: ")
    notes = input("Enter Notes: ")
    date_of_visit = input("Enter Date of Visit: ")

    cursor.execute("""
        SELECT patient_id FROM patients
        WHERE patient_id = ?
    """, (patient_id,))
    if cursor.fetchone() is None:
        print("Patient does not exixt.")
        return
    cursor.execute("""
        SELECT doctor_id FROM doctors
        WHERE doctor_id = ?
    """, (doctor_id,))
    if cursor.fetchone() is None:
        print("Doctor does not exist.")
        return
    print("RECORD ID:", record_id)
    print("PATIENT ID:", patient_id)
    print("DOCTOR ID:", doctor_id)
    print("DIAGNOSIS:", diagnosis)
    print("SYMPTOMS:", symptoms)
    print("PRESCRIPTION:", prescription)
    print("NOTES:", notes)
    print("DATE:", date_of_visit)
    cursor.execute("""
        INSERT INTO medical_records
        (record_id, patient_id, doctor_id, diagnosis, symptoms, prescription, notes, date_of_visit)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_id,
        patient_id,
        doctor_id,
        diagnosis,
        symptoms,
        prescription,
        notes,
        date_of_visit
    ))
    connection.commit()
    print("Medical record added successfully.")

def view_medical_records():
    print("\n---- Medical Records ---- ")
    cursor.execute("SELECT * FROM medical_records")
    records = cursor.fetchall()
    if len(records) == 0:
        print("No medical records found.")
    else:
        for record in records:
            print(record)

def add_billing():
    print("\n---- Add Billing ----")

    bill_id = int(input("Enter Bill ID: "))
    patient_id = int(input("Enter Patient ID: "))
    consultation_fee = float(input("Enter Consultation Fee: "))
    medication_cost = float(input("Enter Medication Cost: "))
    other_charges = float(input("Enter Other Charges: "))
    discount = float(input("Enter Discount: "))
    amount_paid = float(input("Enter Amount Paid: "))

    cursor.execute(
        "SELECT patient_id FROM patients WHERE patient_id = ?",
        (patient_id,)
    )

    if cursor.fetchone() is None:
        print("Patient does not exit.")
        return

    subtotal = consultation_fee + medication_cost + other_charges
    total_amount = subtotal - discount
    balance = total_amount - amount_paid
    print("Subtotal:", subtotal)
    print("Total Amount:", total_amount)
    print("Balance", balance)

    cursor.execute("PRAGMA table_info(billing)")
    print("BILLING COLUMNS:")
    print(cursor.fetchall())
    cursor.execute("""
        INSERT INTO billing
        (bill_id, patient_id, consultation_fee, medication_cost, other_charges, discount, subtotal, total_amount, amount_paid, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bill_id,
        patient_id,
        consultation_fee,
        medication_cost,
        other_charges,
        discount,
        subtotal,
        total_amount,
        amount_paid,
        balance
    ))
    connection.commit()
    print("Billing record added successfully.")

def view_billing():
    print("\n---- View Billing ----")
    cursor.execute("SELECT subtotal, total_amount, amount_paid, balance FROM billing")
    bills = cursor.fetchall()
    if len(bills) == 0:
        print("No Billing records found.")
    else:
        for bill in bills:
            print("\nSubtotal:", bill[0])
            print("Total Amount:", bill[1])
            print("Amount Paid:", bill[2])
            print("Balance:", bill[3])
            print("--------------------------")


def search_doctor():
    print("\n---- Search Doctor ----")

    doctor_id = int(input("Enter Doctor Id: "))

    cursor.execute(
        "SELECT * FROM doctors WHERE doctor_id = ?",
        (doctor_id,)
    )

    doctor = cursor.fetchone()
    if doctor:
        print("\nDoctor Found:")
        print("Doctor ID:", doctor[0])
        print("Full Name:", doctor[1])
        print("Specialization:", doctor[2])
        print("Email:", doctor[3])
        print("Phone Number:", doctor[4])
        print("Availability Status:", doctor[5])
    else:
        print("Doctor does not exist.")

def update_doctor():
    print("\n---- Update Doctor ----")
    doctor_id = int(input("Enter Doctor ID: "))
    cursor.execute(
        "SELECT * FROM doctors WHERE doctor_id  = ?",
        (doctor_id,)
    )
    doctor = cursor.fetchone()
    if doctor is None:
        print("Doctor does not exist.")
        return

    print("Doctor Found.")
    full_name = input("Enter New Full Name: ")
    specialization = input("Enter New Specialization: ")
    email = input("Enter New Email: ")
    phone = input("Enter New New Phone Number: ")
    availability_status = input("Enter New Availability Status: ")
    cursor.execute("""
        UPDATE doctors
        SET full_name = ?,
            specialization = ?,
            email = ?,
            phone = ?,
            availability_status = ?
        WHERE doctor_id = ?
    """, (
        full_name,
        specialization,
        email,
        phone,
        availability_status,
        doctor_id
    ))

    connection.commit()
    print("Doctor Updated Successfully.")

def remove_doctor():
    print("\n---- Remove Doctor ----")
    doctor_id = int(input("Enter Doctor ID: "))
    cursor.execute(
        "SELECT * FROM doctors WHERE doctor_id = ?",
        (doctor_id,)
    )
    doctor = cursor.fetchone()
    if doctor is None:
        print("Doctor does not exist.")
        return

    print("Doctor Found:", doctor[1])
    cursor.execute(
        "DELETE FROM doctors WHERE doctor_id = ?",
        (doctor_id,)      
    )
    connection.commit()
    print("Doctor removed successfuly.")

def search_appointment():
    print("\n---- Search Appointment ----")
    appointment_id = int(input("Enter Appointment ID: "))
    cursor.execute(
            "SELECT * FROM appointments WHERE appointment_id = ?",
            (appointment_id,)
    )
    appointment = cursor.fetchone()

    if appointment:
        print("\nAppointment Found: ")
        print("Appointment ID:", appointment[0])
        print("Patient ID::", appointment[1])
        print("Doctor ID:", appointment[2])
        print("Appointment Date:", appointment[3])
        print("Appointment Time:", appointment[4])
        print("Reason:", appointment[5])
        print("Status:", appointment[6])
    else:
        print("Appointment does not exist.")

def cancel_appointment():
    print("\n---- Cancel Appointment ----")
    appointment_id = int(input("Enter Appointment ID: "))
    cursor.execute(
        "SELECT * FROM appointments WHERE appointment_id = ?",
        (appointment_id,)
    )
    appointment = cursor.fetchone()
    if appointment is None:
        print("Appointment does not exist.")
        return
    cursor.execute(
        "UPDATE appointments SET status = ? WHERE appointment_id = ?",
        ("Cancelled", appointment_id)
    )
    connection.commit()
    print("Appointment Cancelled Successfully.")

def reschedule_appointment():
    print("\n---- Reschedule Appointment ----")
    appointment_id = int(input("Enter Appointment ID: "))
    cursor.execute(
        "SELECT * FROM appointments WHERE appointment_id = ?",
        (appointment_id,)
    )
    appointment = cursor.fetchone()
    if appointment is None:
        print("Appointment does not exist.")
        return

    if appointment[6] == "Canceled":
        print("This appointment has been canceled and cannot be rescheduled.")
        return

    new_date = input("Enter new Appointment Date (YYY-MM-DD): ")
    new_time = input("Enter new Appointment Time (HH-MM): ")

    cursor.execute("""
        SELECT * FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND appointment_id = ?
        AND status = "Scheduled"
    """, (
        appointment[2],
        new_date,
        new_time,
        appointment_id
    ))
    existing = cursor.fetchone()
    if existing:
        print("Doctor is already booked at this time.")
        return

    cursor.execute("""
        UPDATE appointments
        SET appointment_date = ?,
            appointment_time = ?,
            status = 'Scheduled'
        WHERE appointment_id = ?
    """, (
        new_date,
        new_time,
        appointment_id
    ))
    connection.commit()
    print("Appointment rescheduled successfully.")

def view_medical_history():
    print("\n ---- Patient Medical History ----")
    patient_id = int(input("Enter Patient ID: "))
    cursor.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,)
    )
    patient = cursor.fetchone()
    if patient is None:
        print("Patient does not exist")
        return
    cursor.execute("""
        SELECT record_id, doctor_id, diagnosis, symptoms, prescription, notes, date_of_visit
        FROM medical_records
        WHERE patient_id = ?
        """, (patient_id,))
    records = cursor.fetchall()
    if len(records) == 0:
        print("No medical history found for this patient.")
    else:
        print("\nMedical history for:", patient[1])

        for record in records:
            print("\nRecord ID:", record[0])
            print("Doctor ID:", record[1])
            print("Diagnosis:", record[2])
            print("Symptoms:", record[3])
            print("Prescription:", record[4])
            print("Notes:", record[5])
            print("Date of Visit:", record[6])
            print("-----------------------------")

def total_patients_report():
    print("\n---- Total Nmber of Patients ----")
    cursor.execute("SELECT COUNT(*) FROM patients ")
    total = cursor.fetchone()[0]
    print("Total number of patients:", total)

def total_doctors_report():
    print("\n---- Total Number of Doctors ----")
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total = cursor.fetchone()[0]
    print("Total number of doctors:", total)

def appointment_by_date_report():
    print("\n---- Appointments for a Specific Date")
    appointment_date = input("Enter Appointment Date (YYY-MM-DD): ")

    cursor.execute("""
        SELECT appointment_date, patient_id, doctor_id, appointment_time, reason, status 
        FROM appointments
        WHERE appointment_date = ?
    """, (appointment_date,))

    appointments = cursor.fetchall()
    if len(appointments) == 0:
        print("No appointment found for this date.")
    else:
        print("\nAppointments on", appointment_date)

        for appointment in appointments:
            print("\nAppointment ID:", appointment[0])
            print("Patient ID:", appointment[1])
            print("Doctor ID:", appointment[2])
            print("Time:", appointment[3])
            print("Reason:", appointment[4])
            print("Status:", appointment[5])
            print("---------------------------------")

def appointments_per_doctor_report():
    print("\nNumber of Appointments Per Doctor: ")
    cursor.execute("""
        SELECT doctor_id, COUNT(*)
        FROM appointments
        GROUP BY doctor_id
    """)
    results = cursor.fetchall()
    if len(results) == 0:
        print("No appointment record found.")
    else:
        for result in results:
            print("Doctor ID:", result[0])
            print("Number of appointments:", result[1])
            print("------------------------------")

def total_revenue_report():
    print("\n---- Total Revenue -----")
    cursor.execute("SELECT SUM(total_amount) FROM billing")
    result = cursor.fetchone()[0]
    if result is None:
        result = 0
    print("Total Revenue:", result)

def most_common_conditions_report():
    print("\n---- Most Common Medical Conditions")
    cursor.execute("""
        SELECT diagnosis, COUNT(*)
        FROM medical_records
        GROUP BY diagnosis
        ORDER BY COUNT(*) DESC
    """)
    results = cursor.fetchall()

    if len(results) == 0:
        print("No medical records found.")
    else:
        for result in results:
            print("Diagnosis:", result[0])
            print("Number of Cases:", result[1])
            print("----------------------------")

def create_reports_folder():
    print("\n----- Reports Folder -----")

    if not os.path.exists("reports"):
        os.mkdir("reports")
        print("Report folder created successfully.")
    else:
        print("Report folder already exists.")

def save_patient_reports():
    
        file_path = "reports/patient_report.txt"
        if os.path.exists(file_path):
            print("Patient report file already exists.")

        cursor.execute("SELECT COUNT(*) FROM patients")
        total = cursor.fetchone()[0]

        with open(file_path, "w") as file:
            file.write("MEDICARE HOSPITAL PATIENT REPORT\n")
            file.write("======================================\n")
            file.write(f"Total Number of Patients: {total}\n")
        print("Patient report saved successfully.")

def save_all_reports():
    if not os.path.exists("reports"):
        os.mkdir("reports")

    patient_file = "reports/patient_report.txt"
    if os.path.exists(patient_file):
        print("Patient report file added successfully.")

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    with open(patient_file, "w") as file:
        file.write("MEDICARE HOSPITAL - PATIENT REPORTS")
        file.write("===============================\n")
        file.write(f"Total Number of Patients: {total_patients}\n")

        doctor_file = "reports/doctor_reort.txt"
        if os.path.exists(doctor_file):
            print("Doctor file already exists.")
        cursor.execute("SELECT COUNT(*) FROM doctors")
        total_doctors = cursor.fetchone()[0]

        with open(doctor_file, "w") as file:
            file.write("MEDICARE HOSPITAL - DOCTOR REPORT\n")
            file.write("=================================\n")
            file.write(f"Total Number of Doctors: {total_doctors}\n")

        appointment_file = "reports/appointment_report.txt"
        if os.path.exists(appointment_file):
                print("Appointment report file already exists.")
        cursor.execute("""
            SELECT appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status
            FROM appointments
        """)
        appointments = cursor.fetchall()

        with open(appointment_file, "w") as file:
            file.write("MEDICARE HOSPITAL - APPOINTMENT REPORT\n")
            file.write("=====================================\n")
            for appointment in appointments:
             file.write(f"Appointment ID: {appointment[0]}\n")
             file.write(f"Patient ID: {appointment[1]}\n")
             file.write(f"Doctor ID: {appointment[2]}\n")
             file.write(f"Date: {appointment[3]}\n")
             file.write(f"Time: {appointment[4]}\n")
             file.write(f"Reason: {appointment[5]}\n")
             file.write(f"Status: {appointment[6]}\n")
             file.write("=================================\n")


        revenue_file = "reports/revenue_report.txt"
        if os.path.exists(revenue_file):
            print("Revenue file already exists.")
        cursor.execute("SELECT SUM(total_amount) FROM billing")
        revenue = cursor.fetchone()[0]

        if revenue is None:
            revenue = 0
        with open(revenue_file, "w") as file:
            file.write("MEDICARE HOSPITAL - REVENUE REPORT\n")
            file.write("=================================\n")
            file.write(f"Total Revenue {revenue}\n")

        condition_file = "reports/medical_condition_reports.txt"
        if os.path.exists(condition_file):
            print("Medical condition report file already exists.")

        cursor.execute("""
            SELECT diagnosis, COUNT(*)
            FROM medical_records
            GROUP BY diagnosis
            ORDER BY COUNT(*) DESC
        """)
        conditions = cursor.fetchall()
        with open(condition_file, "w") as file:
            file.write("MEDICARE HOSPITAL - MEDICAL CONDITIONS REPORT\n")
            file.write("============================================\n")
            for condition in conditions:
                file.write(f"Diagnosis: {condition[0]}\n")
                file.write(f"Number of Cases: {condition[1]}\n")
                file.write("========================================\n")
        print("All reports saved successfully.")
             
def save_medical_history_report():
    if not os.path.exists("reports"):
        os.mkdir("reports")
    file_path = "reports/patient_medical_history.txt"
    if os.path.exists(file_path):
        print("Medical history file already exists.")

    cursor.execute("""
        SELECT record_id, patient_id, doctor_id, diagnosis, symptoms, prescription, notes, date_of_visit
        FROM medical_records
    """)
    records = cursor.fetchall()
    with open(file_path, "w") as file:
        file.write("MEDICARE HOSPITAL -PATIENT MEDICAL HISTORY\n")
        file.write("=========================================\n")
        if len(records) == 0:
            file.write("No medical records found.\n")
        else:
            for record in records:
                file.write(f"Record ID: {record[0]}\n")
                file.write(f"Patient ID: {record[1]}\n")
                file.write(f"Doctor ID: {record[2]}\n")
                file.write(f"Diagnosis: {record[3]}\n")
                file.write(f"Symptoms: {record[4]}\n")
                file.write(f"Prescription: {record[5]}\n")
                file.write(f"Notes: {record[6]}\n")
                file.write(f"Date of visit: {record[7]}\n")
                file.write("==============================\n")
    print("Medical history report saved successfully.")                


def main_menu():
    while True:

        print("\n==========================================")
        print("     MEDICARE HOSPITAL MANAGEMENT SYSYEM")
        print("=============================================")
        print("1. Register Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Search Doctor")
        print("6. Update Doctor")
        print("7. Remove Doctor")
        print("8. Book Appointment")
        print("9. View Appointments")
        print("10. Search Appointments")
        print("11. Cancel Appointment")
        print("12. Reschedule Appointment")
        print("13. Add Medical Record")
        print("14. View Medical Records")
        print("15. Add Billing")
        print("16. View Billing")
        print("17. Reports")
        print("18. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_patients()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            add_doctor()
        elif choice == "4":
            view_doctors()
        elif choice == "5":
            search_doctor()
        elif choice == "6":
            update_doctor()
        elif choice == "7":
            remove_doctor()
        elif choice == "8":
            book_appointment()
        elif choice == "9":
            view_appointments()
        elif choice == "10":
            search_appointment()
        elif choice == "11":
            cancel_appointment()
        elif choice == "12":
            reschedule_appointment()
        elif choice == "13":
            add_medical_record()
        elif choice == "14":
            view_medical_records()
        elif choice == "15":
            add_billing()
        elif choice == "16":
            view_billing()
        elif choice == "17":
            save_all_reports()
            save_medical_history_report()
        elif choice == "18":
            print("Thank you for using Medicare Hospital management System.")
            break           
        else:
            print("Invalid choice. Please try again.")
main_menu()


# register_patients()
# view_patients()
# add_doctor()
# view_doctors()
# book_appointment()
# view_appointments()
# add_medical_record()
# view_medical_records()
# add_billing()
# view_billing()
# search_doctor()
# update_doctor()
# remove_doctor()
# search_appointment()
# cancel_appointment()
# reschedule_appointment()
# view_medical_history()
# total_patients_report()
# total_doctors_report()
# appointment_by_date_report()
# appointments_per_doctor_report()
# total_revenue_report()
# most_common_conditions_report()
# create_reports_folder()
# save_patient_reports()
# save_all_reports()
# save_medical_history_report()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = cursor.fetchall()
# print(tables)
# cursor.execute("PRAGMA table_info(medical_records)")
# print(cursor.fetchall())
