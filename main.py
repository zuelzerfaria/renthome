# main.py
import os
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Carrega as variáveis definidas em .env
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# (Opcional) se você quiser enviar mensagens pro usuário depois
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "RentHome API ativa"}

@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
):
    """
    Recebe o POST do Twilio (form data), processa e retorna XML com TwiML.
    """
    incoming_msg = Body.strip().lower()
    resp = MessagingResponse()

    if incoming_msg == "oi":
        reply = "Olá! Bem-vindo ao RentHome. Como posso ajudar com sua reserva?"
    elif incoming_msg.startswith("reservar"):
        reply = "Ótimo! Para qual das casas (A ou B) você gostaria de reservar?"
    else:
        reply = "Desculpe, não entendi. Digite 'reservar' para iniciar uma reserva."

    resp.message(reply)
    # FastAPI vai enviar com Content-Type: application/xml
    return Response(content=str(resp), media_type="application/xml")
