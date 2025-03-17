from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_cors import CORS
import json
import os
import smtplib
from email.message import EmailMessage
from chatbot import chatbot_response

app = Flask(__name__, template_folder="../frontend", static_folder='frontend')
application=app
CORS(app)

app.secret_key = os.getenv("SECRET_KEY", "your_default_secret_key")

# Ensure necessary folders exist
os.makedirs("backend/data", exist_ok=True)

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_FILE = os.path.join(BASE_DIR, "data", "notes_data.json")
ASSIGNMENT_FILE = os.path.join(BASE_DIR, "data", "assignments.json")
SURVEY_FILE = os.path.join(BASE_DIR, "data", "surveys.json")
STUDENT_FILE = os.path.join(BASE_DIR, "data", "students.json")
FACULTY_FILE = os.path.join(BASE_DIR, "data", "faculty.json")

# Load JSON
def load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file) or []
        except json.JSONDecodeError:
            return []
    return []

# Save JSON
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

@app.route("/upload_notes", methods=["GET"])
def show_upload_notes_form():
    print("Trying to render upload_notes.html")
    return render_template("upload_notes.html")

# Upload Notes API
@app.route('/upload_notes', methods=['POST'])
def upload_file():
    subject = request.form.get("subject")
    date = request.form.get("date")
    drive_link = request.form.get("drive_link")

    if not subject or not date or not drive_link:
        return jsonify({"message": "All fields are required!"}), 400

    notes = load_json(NOTES_FILE)
    if any(note["subject"].lower() == subject.lower() and note["date"] == date for note in notes):
        return jsonify({"message": "Notes for this subject and date already exist!"}), 400

    notes.append({"subject": subject.lower(), "date": date, "link": drive_link})
    save_json(NOTES_FILE, notes)

    return jsonify({"message": "File uploaded successfully!"})

# Chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    response = chatbot_response(user_input)
    return jsonify({"response": response})

# Faculty Registration
@app.route("/register", methods=["POST"])
def register():
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")

    if not (fullname and email and password):
        return jsonify({"message": "All fields are required"}), 400

    faculty_data = load_json(FACULTY_FILE)
    if any(faculty["email"] == email for faculty in faculty_data):
        return jsonify({"message": "Email already registered"}), 400

    faculty_data.append({"fullname": fullname, "email": email, "password": password})
    save_json(FACULTY_FILE, faculty_data)

    return jsonify({"message": "Registration successful"}), 200

# Faculty Login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    faculty_data = load_json(FACULTY_FILE)
    if any(user["email"] == email and user["password"] == password for user in faculty_data):
        session["logged_in"] = True
        session["email"] = email
        return redirect(url_for("uploads"))

    return jsonify({"message": "Invalid credentials. Please try again."}), 400

# Faculty Dashboard
@app.route("/uploads")
def uploads():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("uploads.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

# Send Email
def send_email(teacher_email, subject, message):
    student_emails = load_json(STUDENT_FILE)
    if not student_emails:
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = ", ".join(student_emails)
    msg.set_content(message)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

# Show the HTML form page
@app.route("/upload_assignment", methods=["GET"])
def show_upload_assignment_form():
    return render_template("upload_assignment.html")

# Upload Assignment
@app.route("/upload_assignment", methods=["POST"])
def handle_upload_assignment():
    teacher_email = request.form.get("teacher_email")
    class_name = request.form.get("class_name")
    assignment_link = request.form.get("assignment_link")

    if not teacher_email or not class_name or not assignment_link:
        return jsonify({"error": "Missing data"}), 400

    assignment_data = {"teacher_email": teacher_email, "class_name": class_name, "assignment_link": assignment_link}
    save_json(ASSIGNMENT_FILE, assignment_data)

    send_email(teacher_email, f"New Assignment for {class_name}!", f"A new assignment has been uploaded.\nLink: {assignment_link}")

    return jsonify({"message": "Assignment uploaded and notification sent!"}), 200

@app.route("/upload_survey", methods=["GET"])
def show_upload_survey_form():
    return render_template("upload_survey.html")

# Upload Survey
@app.route("/upload_survey", methods=["POST"])
def handle_upload_survey():
    teacher_email = request.form.get("teacher_email")
    class_name = request.form.get("class_name")
    section = request.form.get("section")
    survey_link = request.form.get("survey_link")

    if not teacher_email or not class_name or not section or not survey_link:
        return jsonify({"error": "Missing data"}), 400

    survey_data = {"teacher_email": teacher_email, "class_name": class_name, "section": section, "survey_link": survey_link}
    save_json(SURVEY_FILE, survey_data)

    send_email(teacher_email, f"New Survey for {class_name} - {section}", f"A new survey has been uploaded.\nLink: {survey_link}")

    return jsonify({"message": "Survey uploaded and notification sent!"}), 200

# Serve HTML Pages
@app.route('/')
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
