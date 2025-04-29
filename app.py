from flask import Flask, request
from twilio.rest import Client
import openai
import os

# Carregar variáveis de ambiente
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
openai_api_key = os.environ.get('OPENAI_API_KEY')

client = Client(account_sid, auth_token)
openai.api_key = openai_api_key

# Criar o app Flask
app = Flask(__name__)

# Rota principal para teste
@app.route("/", methods=['GET'])
def home():
    return "👋 TECBOT online!"

# Webhook para receber mensagens do WhatsApp
@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    if not incoming_msg or not from_number:
        return "Mensagem inválida.", 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o THEKKYBOT, assistente inteligente da empresa THEKKY."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao consultar OpenAI: {str(e)}")
        reply = "⚠️ Desculpe, estou fora do ar no momento. Por favor, tente novamente mais tarde."

    try:
        client.messages.create(
            from_=twilio_whatsapp_number,
            body=reply,
            to=from_number
        )
    except Exception as e:
        print(f"Erro ao enviar mensagem pelo Twilio: {str(e)}")
    
    return "OK", 200

