import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

def send_email(recipient_email, subject, body):
    """
    Send an email notification using Gmail SMTP
    
    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Subject of the email
        body (str): Body content of the email
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Checking if email sending is enabled
        if not current_app.config.get('MAIL_ENABLED', True):
            current_app.logger.info(f"Email sending disabled. Would have sent to: {recipient_email}")
            return True
            
        # Getting Gmail credentials from app config
        smtp_username = current_app.config.get('SMTP_USERNAME')
        smtp_password = current_app.config.get('SMTP_PASSWORD')
        
        if not smtp_username or not smtp_password:
            current_app.logger.error("SMTP credentials not configured")
            return False
            
        # Creating message
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = recipient_email
        message['Subject'] = subject
        
        # Attaching body
        message.attach(MIMEText(body, 'plain'))
        
        # Connecting to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade to secure connection
        server.login(smtp_username, smtp_password)
        
        # Sending email
        server.send_message(message)
        server.quit()
        
        current_app.logger.info(f"Email sent to {recipient_email}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False

def notify_task_assignment(user_email, task_title, project_name):
    """
    Send notification for task assignment
    """
    subject = "New Task Assignment"
    body = f"""
    Dear Team Member,
    
    You have been assigned a new task:
    
    Task: {task_title}
    Project: {project_name}
    
    Please log in to the application to view more details.
    
    Regards,
    Project Management Team
    """
    
    return send_email(user_email, subject, body)

def notify_team_addition(user_email, team_name):
    """
    Send notification when user is added to a team
    """
    subject = "Team Membership Update"
    body = f"""
    Dear Team Member,
    
    You have been added to team: {team_name}
    
    Please log in to the application to view your team's projects and tasks.
    
    Regards,
    Project Management Team
    """
    
    return send_email(user_email, subject, body)

def notify_task_status_change(user_email, task_title, old_status, new_status):
    """
    Send notification when task status changes
    """
    subject = "Task Status Update"
    body = f"""
    Dear Team Member,
    
    The status of your task has been updated:
    
    Task: {task_title}
    Previous Status: {old_status}
    New Status: {new_status}
    
    Please log in to the application for more information.
    
    Regards,
    Project Management Team
    """
    
    return send_email(user_email, subject, body)
