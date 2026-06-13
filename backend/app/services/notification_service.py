import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client = None
_db = None

def _get_db():
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
        _db = _client[settings.MONGODB_DB]
    return _db
class NotificationService:
    @staticmethod
    async def log_notification(delivery_type: str, recipient: str, subject: str, body: str, status: str = "success"):
        """Logs the notification dispatch to MongoDB for UI observability."""
        try:
            doc = {
                "type": delivery_type,
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            await _get_db().notification_logs.insert_one(doc)
        except Exception as e:
            print(f"Failed to log notification: {e}")

    @staticmethod
    async def send_sms_mock(phone_number: str, message: str):
        """Simulate sending an SMS."""
        print(f"[{datetime.now().isoformat()}] [SMS DISPATCHED] To: {phone_number} | Message: {message}")
        await asyncio.sleep(1) # Simulate network delay
        await NotificationService.log_notification("SMS", phone_number, "Urgent Alert", message)
        return True

    @staticmethod
    async def send_email_mock(email_address: str, subject: str, body: str):
        """Simulate sending an email."""
        print(f"[{datetime.now().isoformat()}] [EMAIL DISPATCHED] To: {email_address} | Subject: {subject} | Body: {body}")
        await asyncio.sleep(1) # Simulate network delay
        await NotificationService.log_notification("Email", email_address, subject, body)
        return True

    @staticmethod
    async def trigger_webhook(url: str, payload: dict):
        """Simulate triggering a webhook."""
        print(f"[{datetime.now().isoformat()}] [WEBHOOK TRIGGERED] URL: {url} | Payload: {payload}")
        await asyncio.sleep(1) # Simulate network delay
        await NotificationService.log_notification("Webhook", url, "System Webhook", str(payload))
        return True

    @classmethod
    async def dispatch_critical_alert(cls, alert_id: str, venue: str, severity: str, message: str):
        """Dispatches all notifications for a critical alert."""
        if severity.lower() in ["high", "critical"]:
            print(f"\n--- INITIATING CRITICAL ALERT NOTIFICATION SEQUENCE FOR {alert_id} ---")
            await asyncio.gather(
                cls.send_sms_mock("+1-555-0199", f"URGENT: {severity.upper()} Alert at {venue}. {message}"),
                cls.send_email_mock("operations@citygov.org", f"Operational Alert: {venue}", f"Severity: {severity}\n\nDetails: {message}"),
                cls.trigger_webhook("https://webhook.site/mock-city-dashboard", {"alert_id": alert_id, "venue": venue, "severity": severity, "message": message})
            )
            print("--- CRITICAL ALERT NOTIFICATIONS DISPATCHED ---\n")
