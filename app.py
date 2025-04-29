from flask import Flask, request
from twilio.rest import Client
import openai
import os

# Configurações
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
openai_api_key = os.environ.get('OPENAI_API_KEY')

client = Client(account_sid, auth_token)

# Iniciar o app Flask
app = Flask(__name__)
openai.api_key = openai_api_key

@app.route("/", methods=['GET'])
def home():
    return "👋 Olá! O TECBOT está ativo!"

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    if incoming_msg:
        try:
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é o THEKKYBOT, assistente inteligente da empresa THEKKY."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            reply = gpt_response.choices[0].message['content']
        except Exception as e:
            print(f"Erro ao consultar OpenAI: {e}")
            reply = "Desculpe, estou fora do ar no momento. Por favor, tente mais tarde."

        # Enviar resposta via WhatsApp
        client.messages.create(
            from_=twilio_whatsapp_number,
            body=reply,
            to=from_number
        )
    return "OK", 200
