# Odoo Hackathon - Team 315 Backend

## Email Notifications Setup

The application now supports email notifications for important events:
- Task assignments
- Team membership changes
- Task status updates

### Configuration

To enable email notifications, set the following environment variables:

```
SMTP_USERNAME=your_gmail_address@gmail.com
SMTP_PASSWORD=your_app_password
MAIL_ENABLED=True  # Set to False to disable emails
```

### Gmail Setup Instructions

1. You'll need to use an "App Password" instead of your regular Gmail password:
   - Go to your Google Account settings (https://myaccount.google.com/)
   - Go to Security → App passwords (you may need to enable 2-step verification first)
   - Select "Mail" as the app and "Other" as the device (name it "Project Management App")
   - Click "Generate"
   - Use the generated 16-character password as your SMTP_PASSWORD

2. Make sure you don't commit your SMTP credentials to version control.
   - Add them to your .env file (which should be in .gitignore)
   - Or set them as environment variables in your deployment environment

### Testing Emails

You can disable email sending during development by setting:
```
MAIL_ENABLED=False
```

When emails are disabled, the application will log what would have been sent instead of actually sending emails. 