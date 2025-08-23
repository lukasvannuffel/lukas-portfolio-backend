from flask import Blueprint, jsonify, request
from flask_mail import Mail, Message
import os

contact_bp = Blueprint('contact', __name__)

# This will be initialized in main.py
mail = None

def init_mail(app):
    global mail
    mail = Mail(app)

@contact_bp.route('/contact', methods=['POST'])
def send_contact_email():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create email message
        msg = Message(
            subject=f"Portfolio Contact: {data['subject']}",
            sender=data['email'],
            recipients=['lukasvannuffel02@gmail.com'],
            body=f"""
New contact form submission from your portfolio website:

Name: {data['name']}
Email: {data['email']}
Subject: {data['subject']}

Message:
{data['message']}

---
This message was sent from your portfolio contact form.
            """.strip()
        )
        
        # Send email
        mail.send(msg)
        
        return jsonify({'message': 'Email sent successfully'}), 200
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'error': 'Failed to send email'}), 500

@contact_bp.route('/contact/test', methods=['GET'])
def test_contact():
    return jsonify({'message': 'Contact endpoint is working'}), 200

