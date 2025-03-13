import smtplib
import random
import string
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from jinja2 import Environment, FileSystemLoader

# Setup Jinja2 environment
template_dir = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(str(template_dir)))


def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return ''.join(random.choices(string.digits, k=6))


def send_verification_email(email: str, otp: str) -> bool:
    """
    Send a verification email with OTP using HTML template.

    Args:
        email (str): Recipient's email address
        otp (str): OTP code to be sent

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Get the email template
        template = env.get_template("email_verification.html")

        # Render the template with the OTP
        html_content = template.render(otp_code=otp)

        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.SMTP_USERNAME
        msg["To"] = email
        msg["Subject"] = "Verify Your Email - Health Connect"

        # Attach HTML content
        msg.attach(MIMEText(html_content, "html"))

        # Connect to SMTP server and send email
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
