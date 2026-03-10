# Academic Query Chatbox

A simple rule-based Flask application for handling academic queries, managing timetables, and calculating attendance.

## Features

- **Chatbox**: Ask about exams, holidays, contacts, etc.
- **Attendance Calculator**: Calculate attendance percentage and classes needed for 75%.
- **Timetable**: View and generate study plans.
- **Admin Panel**: Add data to the system.

## How to Run

### Prerequisites
- Python 3.x installed.

### Quick Start (Windows PowerShell)

1. Open PowerShell in this folder.
2. Run the helper script:
   ```powershell
   .\run_server.ps1
   ```
   (If you get a permission error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).

### Manual Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate the environment:**
   - Windows: `.\.venv\Scripts\Activate`
   - Mac/Linux: `source .venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in Browser:**
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure

- `app.py`: Main Flask application and database logic.
- `schema.sql`: Database schema.
- `templates/`: HTML files.
- `static/`: CSS and JS files.
