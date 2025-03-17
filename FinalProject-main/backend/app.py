from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import json
import os
import smtplib
from email.message import EmailMessage
from chatbot import chatbot_response

app = Flask(__name__, template_folder="../frontend",static_folder='frontend')

application = app


CORS(app)

app.secret_key = "76f4c00a15ebee42bf4772e8c1f8fa5220285117af40933c9ca738e78410d468"

# Ensure necessary folders exist
os.makedirs("backend/data", exist_ok=True)

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_FILE = os.path.join(BASE_DIR, "data", "notes_data.json")
ASSIGNMENT_FILE = os.path.join(BASE_DIR, "data", "assignments.json")
SURVEY_FILE = os.path.join(BASE_DIR, "data", "surveys.json")
STUDENT_FILE = os.path.join(BASE_DIR, "data", "students.json")
FACULTY_FILE = os.path.join(BASE_DIR, "data", "faculty.json")

# Load JSON safely
def load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file) or []
        except json.JSONDecodeError:
            return []
    return []

# Save JSON safely
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save the updated notes to the JSON file
def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Serve Upload Notes Page (GET request to load HTML page)
@app.route('/upload_notes.html', methods=['GET'])
def upload_notes_page():
    return render_template('upload_notes.html')

# Upload Notes API (POST request to handle form submission)
@app.route('/upload_notes', methods=['POST'])
def upload_file():
    print("Upload API hit!")  # Debugging log

    subject = request.form.get("subject")
    date = request.form.get("date")
    drive_link = request.form.get("drive_link")

    print(f"Received Data: Subject={subject}, Date={date}, Link={drive_link}")  # Debugging log

    if not subject or not date or not drive_link:
        return jsonify({"message": "All fields are required!"}), 400

    notes = load_json(NOTES_FILE)
    print(f"Existing Notes: {notes}")  # Debugging log

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

# Send Email Notifications
def send_email(teacher_email, subject, message):
    student_emails = load_json(STUDENT_FILE)
    if not student_emails:
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "saisamhithanadipena@gmail.com"
    msg["To"] = ", ".join(student_emails)
    msg.set_content(message)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("saisamhithanadipena@gmail.com", "uqtn zjxo qhvu gsbv")  # Use environment variables instead!
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

# Handle Assignment Upload
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

# Handle Survey Upload
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

@app.route('/upload_assignment.html')
def upload_assignment_page():
    return render_template('upload_assignment.html')

@app.route('/upload_survey.html')
def upload_survey_page():
    return render_template('upload_survey.html')

@app.route('/')
def serve():
    return send_from_directory('frontend', 'index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
