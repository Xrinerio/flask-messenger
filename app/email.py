from flask_mailman import EmailMessage
from itsdangerous import URLSafeTimedSerializer

from app import mail, app
from config import Config


def send_email(to, subject, letter):
    msg = EmailMessage(
        "title",
        "body",
        "mycoolmes@mail.ru",
        ["parappa.play@mail.ru"]
    )
    mail.send(msg)


def generate_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt = SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt = SECURITY_PASSWORD_SALT, max_age=expiration
        )
        return email
    except Exception:
        return False