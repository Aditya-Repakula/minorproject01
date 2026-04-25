# minorproject01

📚 Academic Query Chatbox
A smart Flask-based web application designed to help students manage their academic life efficiently. This chatbot-powered system provides instant answers to academic queries, manages schedules, tracks attendance, and gives admins a central hub for academic data management.

✨ Features
🎓 For Students
Smart Chatbot - Ask questions about exams, timetables, assignments, faculty contacts, and more
Attendance Calculator - Track your attendance percentage and calculate classes needed to reach 75%
Class Timetable - View your complete class schedule
Study Plan Generator - Generate personalized weekly study plans
Quick Access - Easy-to-use dashboard for all academic information
🔧 For Admins
Data Management - Add, update, and delete academic information
Exam Scheduling - Manage exam dates, subjects, and venues
Faculty Directory - Maintain faculty contacts and departments
Assignment Tracking - Post and track assignment deadlines
Calendar Management - Set holidays and important dates
Soft Delete System - Safe data deletion with recovery capability
🛠️ Tech Stack
Component	Technology
Backend	Python 3.x with Flask 3.0
Database	SQLite (lightweight & portable)
Frontend	HTML5, CSS3, JavaScript
Templating	Jinja2
Scripting	PowerShell & Batch (Windows support)
📋 Prerequisites
Python 3.7+ installed on your system
pip package manager
A modern web browser (Chrome, Firefox, Edge, Safari)
🚀 Quick Start
Option 1: Windows PowerShell (Easiest)
Open PowerShell in the academic-chatbox folder
Run the helper script:
PowerShell
.\run_server.ps1
Note: If you get a permission error, run this first:

PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Open your browser and visit: http://127.0.0.1:5000
Option 2: Manual Setup (Cross-platform)
Step 1: Create Virtual Environment
bash
python -m venv .venv
Step 2: Activate Virtual Environment
Windows (CMD):
bash
.venv\Scripts\activate
Windows (PowerShell):
bash
.\.venv\Scripts\Activate
Mac/Linux:
bash
source .venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Run the Application
bash
python app.py
Step 5: Open in Browser
Visit http://127.0.0.1:5000

🔑 Default Credentials
Role	Username	Password
Student	student	student123
Admin	admin	admin123
⚠️ Security Note: Change these credentials in production!

📁 Project Structure
Code
academic-chatbox/
├── app.py                      # Main Flask application
├── enhanced_chatbot.py         # Rule-based chatbot engine
├── schema.sql                  # Database schema
├── requirements.txt            # Python dependencies
├── academic.db                 # SQLite database (auto-created)
├── run_server.ps1             # PowerShell startup script
├── start.bat                  # Batch startup script
├── templates/                 # HTML templates
│   ├── login_simple.html
│   ├── chat.html
│   ├── attendance.html
│   ├── timetable.html
│   ├── admin_enhanced.html
│   └── ...
└── static/                    # CSS and JavaScript files
    ├── styles.css
    └── script.js
💬 Chatbot Capabilities
The chatbot understands queries about:

Topic	Example Questions
📚 Exams	"When is my exam?" "Show exam schedule"
📅 Timetable	"What's my class schedule?" "When is Math class?"
📝 Assignments	"What are my deadlines?" "Show assignments"
👨‍🏫 Faculty	"Who is my teacher?" "Faculty contact?"
📊 Attendance	"Check my attendance" "How many classes?"
🏖️ Holidays	"When are holidays?" "College calendar?"
💰 Fees	"Fee payment details" "Dues information"
📈 Grades	"Show my grades" "What's my result?"
🔐 User Roles & Access
Student Role
✅ Chat with the academic chatbot
✅ View timetable
✅ Calculate attendance
✅ Generate study plans
❌ Cannot modify any data
Admin Role
✅ Full CRUD operations on all academic data
✅ Manage FAQs and announcements
✅ View audit logs (framework ready)
✅ Bulk delete operations
✅ Can change any information
🗄️ Database Schema
The system uses SQLite with the following main tables:

SQL
users          # Student and admin accounts
faq            # Frequently asked questions and answers
timetable      # Class schedules
exams          # Exam information
assignments    # Assignment details
contacts       # Faculty directory
calendar       # Holidays and events
All tables support soft delete via deleted_at timestamp.

🐛 Troubleshooting
Port 5000 Already in Use
Python
# Edit app.py and change the port:
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 instead
Database Issues
Delete academic.db and restart the app - it will auto-create a fresh database with seed data.

Virtual Environment Not Activating
Try using Python directly:

bash
python -m flask run
ModuleNotFoundError
Make sure your virtual environment is activated and dependencies are installed:

bash
pip install -r requirements.txt
📚 API Endpoints
Authentication
GET / - Login page
POST / - Handle login
GET /logout - Logout
Student Routes
GET /chat - Chat interface
POST /chat/respond - Chatbot response
GET /timetable - View timetable
POST /timetable/generate - Generate study plan
GET /attendance - Attendance calculator
POST /attendance/calc - Calculate attendance
Admin Routes
GET /admin - Admin dashboard
GET /admin/data/<kind> - Fetch data
POST /admin/add/<kind> - Add new record
POST /admin/update/<kind>/<id> - Update record
POST /admin/delete/<kind>/<id> - Delete record
POST /admin/bulk-delete - Delete multiple records
🤖 Chatbot Engine
The chatbot uses a rule-based approach with:

Intent detection through keyword matching
Pre-defined response templates
Database-driven content
HTML table formatting for data display
Emoji support for friendly interface
File: enhanced_chatbot.py

🔄 How to Use
For Students:
Login with student credentials
Use the chatbot to ask academic questions
View your timetable and attendance
Generate study plans to stay organized
For Admins:
Login with admin credentials
Go to Admin Panel
Add/Edit/Delete academic information
Keep all data up-to-date for students
🚀 Future Enhancements
 Integration with AI chatbot (GPT, Gemini)
 Email notifications for deadlines
 Mobile app version
 Export reports (PDF, CSV)
 Dark mode theme
 Multi-language support
 Marks submission portal
 Assignment submission system
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Author
Aditya Repakula

💡 Tips
📖 Read the chatbot responses carefully - they contain helpful tips!
📱 The interface is responsive and works on tablets too
🔒 Always logout after using shared computers
📞 For technical issues, contact your college IT department
🤝 Contributing
Found a bug? Want to suggest a feature? Feel free to create an issue or contact the developer.

❓ FAQ
Q: Can I change the admin password? A: Yes, you can edit the database directly or modify seed_data() in app.py.

Q: How do I add more subjects to the timetable? A: Use the Admin Panel → Timetable section to add new entries.

Q: Is my attendance data secure? A: Yes, data is only visible to logged-in users with proper role validation.

Q: Can multiple admins access the system? A: Yes, you can create more admin accounts through the database.
