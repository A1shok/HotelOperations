from fastapi import FastAPI

app = FastAPI()

@app.post("/webhook")
async def whatsapp(req: Request):
    from twilio.twiml.messaging_response import MessagingResponse
    from fastapi.responses import Response

    print("🔥 WEBHOOK HIT")

    resp = MessagingResponse()
    resp.message("FINAL WORKING 👍")

    return Response(content=str(resp), media_type="application/xml")
