-- SQLite schema for Academic Chatbox project

-- Add deleted_at columns to all tables for soft delete
CREATE TABLE IF NOT EXISTS faq (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT,
  question TEXT,
  answer TEXT,
  deleted_at TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS timetable (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  day TEXT,
  period INTEGER,
  subject TEXT,
  room TEXT,
  faculty TEXT,
  deleted_at TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS calendar (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  event TEXT,
  deleted_at TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS assignments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  course TEXT,
  title TEXT,
  due_date TEXT,
  description TEXT,
  submission_link TEXT,
  deleted_at TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  department TEXT,    
  faculty_name TEXT,
  email TEXT,
  phone TEXT,
  deleted_at TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS exams (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_name TEXT,
  date TEXT,
  subject TEXT,
  venue TEXT,
  deleted_at TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

-- Audit log table for tracking changes
CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  table_name TEXT NOT NULL,
  row_id INTEGER NOT NULL,
  action TEXT NOT NULL, -- 'create', 'update', 'delete', 'bulk_delete'
  old_data TEXT, -- JSON string of old data
  new_data TEXT, -- JSON string of new data
  changed_by TEXT NOT NULL,
  changed_at TEXT NOT NULL
);