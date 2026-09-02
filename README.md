Medical Hospital Management System: This project built as a project after my completion of python class. The goal was to design and build a working system that could manage the day-to-day operations of an Hospital, from patient records to the doctors, billing patients to booking appointments and appointment schedulling.


Problem being solved: Many Hospital and clients rely on paper records or scattered spreadsheets to manage patients, doctors, appointments, and billings. This leads to lost of records, double-booked appointments, difficulty tracking a patient's medical history over time. This system solves that by centralizing hospital data in a single, structured database.


Project Objectives: It provides a simple way to register and manage patient record
                    maintain doctor information and availability
                    Track patient medical history and prescriptions
                    Manage billing and payment as well as generating receipts
                    Generate reports for hospital administration


Features:    Doctor Management
             Prescription/medical records
             Billing and Payment handling
             Patient registration and record management
             Report generation(appointments, doctors, patients, revenue, medical                     conditions, medical history)


Technology used:  Python 3.10
                  SQlite3
                  datetime
                  regular expression
                  operating system
                  Built-in python libaries for file handling and reporting


Python Concepts Demonstrated: Function and modular program design
                              Working with SQlite database from python(via the sqlite3                                 module)
                              File handling (generating .txt reports)

Database Structure:  
    Tables:
        Patients stores patient personal and medical information
        doctors stores doctor information, specialization and availability
        appointments links patients to doctors with date, time, reason, and status
        billing tracks and billing records
        medical records stores patients medical records


Challenges Encountered: The most difficult part of building this system was designing the database structure-specifically figuring out how to correctly link tables together(for example, connecting appointments to both a specific patient and specific doctor) without creating conflicts or duplicate records.




Solution to the Challenges: This was solved by carefully planning the relationships between tables before writing code, using unique ID's(such as appointment_id, doctor_id and patient_id) to correctly link records across tables, and testing the database structure with sample data to catch errors like duplicate or conflicting entries early.                              

             
             
