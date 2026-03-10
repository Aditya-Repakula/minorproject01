#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Rule-Based Chatbot with Pre-defined Answers
Provides basic responses with HTML table display for academic queries
"""

import sqlite3
from datetime import datetime

class SimpleAcademicChatbot:
    def __init__(self):
        self.responses = {
            'exam': {
                'patterns': ['exam', 'test', 'midterm', 'final', 'quiz'],
                'response': "📚 Here are your upcoming exams:\n\n{table_data}\n\n💡 Tip: Start preparing early and review your notes regularly!"
            },
            'timetable': {
                'patterns': ['timetable', 'schedule', 'class', 'when', 'time'],
                'response': "📅 Here's your class schedule:\n\n{table_data}\n\n🎯 Don't forget to attend all classes!"
            },
            'assignment': {
                'patterns': ['assignment', 'homework', 'project', 'deadline'],
                'response': "📝 Here are your assignment deadlines:\n\n{table_data}\n\n⏰ Submit your work on time!"
            },
            'attendance': {
                'patterns': ['attendance', 'present', 'absent'],
                'response': "📊 Your attendance details:\n\n{table_data}\n\n✅ Maintain good attendance for better grades!"
            },
            'contact': {
                'patterns': ['contact', 'teacher', 'faculty', 'phone', 'email'],
                'response': "📞 Faculty contact information:\n\n{table_data}\n\n💬 Feel free to reach out to your teachers!"
            },
            'greeting': {
                'patterns': ['hello', 'hi', 'good morning', 'good afternoon', 'good evening', 'hey'],
                'response': "👋 Hello! How can I help you with your academic queries today?\n\nI can help you with:\n• Exam schedules 📚\n• Class timetables 📅\n• Assignment deadlines 📝\n• Attendance records 📊\n• Faculty contacts 📞\n\nJust ask me anything!"
            },
            'help': {
                'patterns': ['help', 'what can you do', 'assist', 'support'],
                'response': "🤖 I'm here to help you with your academic needs!\n\nI can provide information about:\n• 📚 Exam schedules and results\n• 📅 Class timetables\n• 📝 Assignment deadlines\n• 📊 Attendance records\n• 📞 Faculty contacts\n• 💰 Fee payment details\n\nJust type your question and I'll do my best to help!"
            },
            'thanks': {
                'patterns': ['thank', 'thanks', 'appreciate'],
                'response': "😊 You're very welcome! I'm always here to help you with your academic queries. Don't hesitate to ask if you need anything else!"
            },
            'fees': {
                'patterns': ['fee', 'payment', 'dues', 'money'],
                'response': "💰 For fee payment details, please contact the accounts department or check your student portal.\n\nYou can also visit the admin office during working hours for assistance."
            },
            'marks': {
                'patterns': ['marks', 'grade', 'score', 'result'],
                'response': "📊 For your marks and grades, please check your student portal or contact your subject teacher.\n\nResults are usually published within 2-3 weeks after exams."
            },
            'holiday': {
                'patterns': ['holiday', 'vacation', 'leave'],
                'response': "🏖️ For holiday schedules and academic calendar, please check the college notice board or official website.\n\nMajor holidays are usually announced well in advance."
            },
            'default': {
                'response': "ERROR !"
            }
        }
    
    def detect_intent(self, query):
        """Simple intent detection based on keyword matching"""
        query_lower = query.lower()
        
        # Check for assignment-related keywords first (to avoid conflicts with 'when')
        assignment_patterns = ['assignment', 'homework', 'project', 'deadline']
        for pattern in assignment_patterns:
            if pattern in query_lower:
                return 'assignment'
        
        # Check for contact-related keywords
        contact_patterns = ['contact', 'teacher', 'faculty', 'phone', 'email']
        for pattern in contact_patterns:
            if pattern in query_lower:
                return 'contact'
        
        # Check for exam-related keywords
        exam_patterns = ['exam', 'test', 'midterm', 'final', 'quiz']
        for pattern in exam_patterns:
            if pattern in query_lower:
                return 'exam'
        
        # Check other intents
        for intent, data in self.responses.items():
            if intent in ['assignment', 'contact', 'exam', 'default']:
                continue
            
            patterns = data.get('patterns', [])
            for pattern in patterns:
                if pattern.lower() in query_lower:
                    return intent
        
        return 'default'
    
    def format_timetable_table(self, timetable_data):
        """Format timetable data into a simple HTML table"""
        if not timetable_data:
            return "No timetable data available. Please contact admin."
        
        html = """
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="color: #495057; margin-bottom: 10px;">📅 Class Schedule</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 5px;">
                <thead style="background: #007bff; color: white;">
                    <tr>
                        <th style="padding: 8px; text-align: left;">Day</th>
                        <th style="padding: 8px; text-align: left;">Period</th>
                        <th style="padding: 8px; text-align: left;">Subject</th>
                        <th style="padding: 8px; text-align: left;">Faculty</th>
                        <th style="padding: 8px; text-align: left;">Room</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for i, class_info in enumerate(timetable_data):
            row_style = "background: #f8f9fa;" if i % 2 == 0 else "background: white;"
            html += f"""
                    <tr style="{row_style}">
                        <td style="padding: 8px;">{class_info['day']}</td>
                        <td style="padding: 8px;">{class_info['period']}</td>
                        <td style="padding: 8px;">{class_info['subject']}</td>
                        <td style="padding: 8px;">{class_info['faculty']}</td>
                        <td style="padding: 8px;">{class_info['room']}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""
        return html
    
    def format_exam_schedule(self, exam_data):
        """Format exam schedule data into a simple HTML table"""
        if not exam_data:
            return "No exam data available. Please contact admin."
        
        html = """
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="color: #856404; margin-bottom: 10px;">📚 Exam Schedule</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 5px;">
                <thead style="background: #ffc107; color: #212529;">
                    <tr>
                        <th style="padding: 8px; text-align: left;">Exam</th>
                        <th style="padding: 8px; text-align: left;">Subject</th>
                        <th style="padding: 8px; text-align: left;">Date</th>
                        <th style="padding: 8px; text-align: left;">Venue</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for i, exam_info in enumerate(exam_data):
            row_style = "background: #fff3cd;" if i % 2 == 0 else "background: white;"
            html += f"""
                    <tr style="{row_style}">
                        <td style="padding: 8px;">{exam_info['exam_name']}</td>
                        <td style="padding: 8px;">{exam_info['subject']}</td>
                        <td style="padding: 8px;">{exam_info['date']}</td>
                        <td style="padding: 8px;">{exam_info['venue']}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""
        return html
    
    def format_assignment_list(self, assignment_data):
        """Format assignment data into a simple HTML list"""
        if not assignment_data:
            return "No assignment data available."
        
        html = """
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="color: #0c5460; margin-bottom: 10px;">📝 Assignment Deadlines</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 5px;">
                <thead style="background: #17a2b8; color: white;">
                    <tr>
                        <th style="padding: 8px; text-align: left;">Course</th>
                        <th style="padding: 8px; text-align: left;">Assignment</th>
                        <th style="padding: 8px; text-align: left;">Due Date</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for i, assignment_info in enumerate(assignment_data):
            row_style = "background: #d1ecf1;" if i % 2 == 0 else "background: white;"
            html += f"""
                    <tr style="{row_style}">
                        <td style="padding: 8px;">{assignment_info['course']}</td>
                        <td style="padding: 8px;">{assignment_info['title']}</td>
                        <td style="padding: 8px;">{assignment_info['due_date']}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""
        return html
    
    def format_contact_list(self, contact_data):
        """Format contact data into a simple HTML list"""
        if not contact_data:
            return "No contact information available."
        
        html = """
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="color: #155724; margin-bottom: 10px;">📞 Faculty Contacts</h4>
            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 5px;">
                <thead style="background: #28a745; color: white;">
                    <tr>
                        <th style="padding: 8px; text-align: left;">Department</th>
                        <th style="padding: 8px; text-align: left;">Faculty Name</th>
                        <th style="padding: 8px; text-align: left;">Email</th>
                        <th style="padding: 8px; text-align: left;">Phone</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for i, contact_info in enumerate(contact_data):
            row_style = "background: #d4edda;" if i % 2 == 0 else "background: white;"
            html += f"""
                    <tr style="{row_style}">
                        <td style="padding: 8px;">{contact_info['department']}</td>
                        <td style="padding: 8px;">{contact_info['faculty_name']}</td>
                        <td style="padding: 8px;">{contact_info['email']}</td>
                        <td style="padding: 8px;">{contact_info['phone']}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""
        return html
    
    def fetch_timetable_from_db(self, db_connection, academic_info=None):
        """Fetch timetable data from database"""
        if not db_connection:
            return None
        
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT DISTINCT day, period, subject, faculty, room FROM timetable WHERE deleted_at IS NULL ORDER BY day, period")
            return cursor.fetchall()
        except:
            return None
    
    def fetch_exam_schedule_from_db(self, db_connection, academic_info=None):
        """Fetch exam schedule data from database"""
        if not db_connection:
            return None
        
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT DISTINCT exam_name, subject, date, venue FROM exams WHERE deleted_at IS NULL ORDER BY date")
            return cursor.fetchall()
        except:
            return None
    
    def fetch_assignment_deadlines_from_db(self, db_connection, academic_info=None):
        """Fetch assignment deadline data from database"""
        if not db_connection:
            return None
        
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT DISTINCT course, title, due_date FROM assignments WHERE deleted_at IS NULL ORDER BY due_date")
            return cursor.fetchall()
        except:
            return None
    
    def fetch_contacts_from_db(self, db_connection, academic_info=None):
        """Fetch contact data from database"""
        if not db_connection:
            return None
        
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT DISTINCT department, faculty_name, email, phone FROM contacts WHERE deleted_at IS NULL ORDER BY faculty_name")
            return cursor.fetchall()
        except:
            return None
    
    def process_query(self, query, db_connection=None):
        """Process user query and return pre-defined response"""
        intent = self.detect_intent(query)
        
        # Get response template
        response_template = self.responses.get(intent, self.responses['default'])['response']
        
        # Handle different intents with database data
        table_data = ""
        
        if intent == 'timetable' and db_connection:
            timetable_data = self.fetch_timetable_from_db(db_connection)
            table_data = self.format_timetable_table(timetable_data)
        elif intent == 'exam' and db_connection:
            exam_data = self.fetch_exam_schedule_from_db(db_connection)
            table_data = self.format_exam_schedule(exam_data)
        elif intent == 'assignment' and db_connection:
            assignment_data = self.fetch_assignment_deadlines_from_db(db_connection)
            table_data = self.format_assignment_list(assignment_data)
        elif intent == 'contact' and db_connection:
            contact_data = self.fetch_contacts_from_db(db_connection)
            table_data = self.format_contact_list(contact_data)
        
        # Replace table placeholder with actual data
        final_response = response_template.replace("{table_data}", table_data)
        
        return {
            'original_query': query,
            'intent': intent,
            'response': final_response,
            'confidence': 1.0 if intent != 'default' else 0.5
        }

def enhanced_rule_based_response(query: str, db_connection=None):
    """Simple rule-based response function"""
    chatbot = SimpleAcademicChatbot()
    result = chatbot.process_query(query, db_connection)
    return result['response']

if __name__ == "__main__":
    print("🤖 Simple Rule-Based Academic Chatbot")
    print("=" * 50)
    
    test_queries = [
        "What is my exam schedule?",
        "Show me my timetable",
        "When are my assignments due?",
        "Who are my teachers?",
        "Hello!",
        "Help me with exams"
    ]
    
    for query in test_queries:
        print(f"\n👤 Student: {query}")
        response = enhanced_rule_based_response(query)
        print(f"🤖 Assistant: {response}")
        print("-" * 50)