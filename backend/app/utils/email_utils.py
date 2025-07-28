import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from app.extensions import get_mail_config

# Setup Jinja2 environment for email templates
template_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_template(template_name, **context):
    """Render Jinja2 email template."""
    template = template_env.get_template(template_name)
    return template.render(context)

def send_email(to, subject, body=None, html=None, template_name=None, context=None, attachments=None, cc=None, bcc=None):
    """
    Send an email using SMTP with support for HTML, templates, and attachments.

    :param to: str or list of recipient emails
    :param subject: Email subject
    :param body: Plaintext fallback message
    :param html: Raw HTML message (if not using template)
    :param template_name: Name of Jinja2 template in /templates (e.g. 'monthly_report.html')
    :param context: Dictionary of template variables
    :param attachments: List of (filename, content_bytes, mimetype)
    :param cc: Optional list of CC addresses
    :param bcc: Optional list of BCC addresses
    """
    config = get_mail_config()
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = config['MAIL_DEFAULT_SENDER']
    msg['To'] = to if isinstance(to, str) else ', '.join(to)
    if cc:
        msg['Cc'] = ', '.join(cc)
    if bcc:
        msg['Bcc'] = ', '.join(bcc)

    # Generate content
    if template_name:
        html_body = render_template(template_name, **(context or {}))
        text_body = body or "This is an HTML email. Please view in a compatible client."
    else:
        html_body = html
        text_body = body

    msg.set_content(text_body)

    if html_body:
        msg.add_alternative(html_body, subtype='html')

    if attachments:
        for filename, content, mimetype in attachments:
            maintype, subtype = mimetype.split('/')
            msg.add_attachment(content, maintype=maintype, subtype=subtype, filename=filename)

    # Send via SMTP
    try:
        with smtplib.SMTP(config["MAIL_SERVER"], config["MAIL_PORT"]) as server:
            server.ehlo()
            print("SMTP server features:", server.esmtp_features)

            if config.get("MAIL_USE_TLS"):
                server.starttls()
                server.ehlo()   
                print("SMTP server features after STARTTLS:", server.esmtp_features)

            if (config["MAIL_USERNAME"] and config["MAIL_PASSWORD"] and'auth' in server.esmtp_features):
                print("SMTP server supports AUTH, logging in...")
                server.login(config["MAIL_USERNAME"], config["MAIL_PASSWORD"])
            else:
                print("SMTP server does not support AUTH or credentials missing, skipping login.")
            
            server.send_message(msg)
        print(f"Email sent to {msg['To']}")
    except Exception as e:
        print(f"Error sending email to {msg['To']}: {e}")
         