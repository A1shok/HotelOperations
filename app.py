import os
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import FastAPI, Request
from db import SessionLocal, Task
from ai import parse_message
from response_engine import reply
from datetime import datetime
import uuid

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

def twilio_reply(message):
    resp = MessagingResponse()
    resp.message(message)
    return Response(content=str(resp), media_type="application/xml")

app = FastAPI()

# -------------------------
# TWILIO WEBHOOK
# -------------------------
@app.post("/webhook")
async def whatsapp_webhook(req: Request):
    from twilio.twiml.messaging_response import MessagingResponse
    from fastapi.responses import Response
    from urllib.parse import parse_qs

    resp = MessagingResponse()

    try:
        print("🔥 WEBHOOK HIT")

        body = await req.body()
        print("RAW BODY:", body)

        data = parse_qs(body.decode())

        msg = data.get("Body", [""])[0]
        phone = data.get("From", [""])[0]

        print("📩 msg:", msg)
        print("📱 phone:", phone)

        resp.message("Now working 👍")

        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        print("❌ ERROR:", str(e))

        resp.message(f"Error: {str(e)}")
        return Response(content=str(resp), media_type="application/xml")

'''
@app.post("/webhook")
async def whatsapp_webhook(req: Request):
    form = await req.form()

    msg = form.get("Body")
    phone = form.get("From")

    room = phone[-3:]

    ai = parse_message(msg)

    db = SessionLocal()

    # -------------------------
    # TASK
    # -------------------------
    if ai["intent"] == "task":
        existing = db.query(Task).filter(
            Task.room == room,
            Task.category == ai["category"],
            Task.status != "closed"
        ).first()

        if existing:
            reply_text = reply("duplicate", {
                "task": ai["category"]
            })
            return twilio_reply(reply_text)

        new_task = Task(
            id=str(uuid.uuid4()),
            room=room,
            category=ai["category"],
            status="created",
            priority="urgent" if ai["category"] == "ac" else "normal",
            escalation_level=0,
            quantity=1,
            created_at=datetime.now()
        )

        db.add(new_task)
        db.commit()

        reply_text = reply("task_created", {
            "task": ai["category"],
            "eta": "10 minutes"
        })

        return twilio_reply(reply_text)

    # -------------------------
    # CANCEL
    # -------------------------
    if ai["intent"] == "cancel":
        task = db.query(Task).filter(
            Task.room == room,
            Task.status != "closed"
        ).first()

        if task:
            task.status = "cancelled"
            db.commit()

            reply_text = reply("cancelled", {
                "task": task.category
            })

            return twilio_reply(reply_text)

    # -------------------------
    # NOT RECEIVED
    # -------------------------
    if ai["intent"] == "not_received":
        task = db.query(Task).filter(
            Task.room == room,
            Task.status == "completed_unverified"
        ).first()

        if task:
            task.status = "in_progress"
            task.escalation_level += 1
            db.commit()

            reply_text = reply("escalation", {
                "task": task.category,
                "eta": "5 minutes"
            })

            return twilio_reply(reply_text)

    # -------------------------
    # DEFAULT (IMPORTANT FIX)
    # -------------------------
    reply_text = reply("default", {})
    return twilio_reply(reply_text)


    return reply("default", {}) '''
