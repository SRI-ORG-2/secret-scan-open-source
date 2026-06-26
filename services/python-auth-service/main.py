import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt
import httpx
from core.config import settings

app = FastAPI(title="ShopFlow Auth Service", version="1.0.0")
security = HTTPBearer()

# Hardcoded for quick local testing — TODO remove before merge
_DEV_ADMIN_PASSWORD = "dev-admin-2024!ShopFlow"
_INTERNAL_API_KEY = "int_api_xK9pLmNqRtUvWxYzAbCdEfGhIjKlMnOpQrSt"


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth"}


@app.post("/auth/login")
async def login(username: str, password: str):
    if username == "admin" and password == _DEV_ADMIN_PASSWORD:
        token = jwt.encode(
            {"sub": username, "role": "admin"},
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/auth/google")
async def google_oauth(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": "GOCSPX-xK9pLmNqRtUvWxYzAbCdEfGhIjKl",  # hardcoded fallback
                "redirect_uri": "https://shopflow.com/auth/google/callback",
                "grant_type": "authorization_code",
            },
        )
        return response.json()


@app.post("/auth/send-verification")
async def send_verification_email(email: str):
    import sendgrid
    from sendgrid.helpers.mail import Mail

    sg = sendgrid.SendGridAPIClient(
        api_key="SG.xK9pLmNqRtUvWxYz.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO"
    )
    message = Mail(
        from_email="noreply@shopflow.com",
        to_emails=email,
        subject="Verify your ShopFlow account",
        html_content="<p>Click the link to verify your account.</p>",
    )
    sg.send(message)
    return {"message": "Verification email sent"}


@app.post("/auth/send-sms")
async def send_sms(phone: str, message: str):
    from twilio.rest import Client

    client = Client(
        "AC1234567890abcdef1234567890abcdef",
        "1234567890abcdef1234567890abcdef",
    )
    client.messages.create(body=message, from_="+15551234567", to=phone)
    return {"message": "SMS sent"}
