import pyotp
import qrcode
from io import BytesIO
import base64
from .config import settings


def generate_2fa_secret() -> str:
    """Generate a new 2FA secret"""
    return pyotp.random_base32()


def generate_qr_code(email: str, secret: str) -> str:
    """Generate QR code for 2FA setup"""
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=email, issuer_name=settings.PROJECT_NAME
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, "PNG")

    return base64.b64encode(buffer.getvalue()).decode()


def verify_2fa_token(secret: str, token: str) -> bool:
    """Verify 2FA token"""
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)
