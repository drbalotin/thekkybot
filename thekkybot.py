from flask import Flask, request
from twilio.rest import Client
import openai
import os

# Configurações
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = Client(account_sid, auth_token)

# Iniciar o app Flask
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    if incoming_msg:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o THEKKYBOT, assistente inteligente e eficiente da empresa THEKKY."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = gpt_response['choices'][0]['message']['content']

        message = client.messages.create(
            from_=twilio_whatsapp_number,
            to=from_number,
            body=reply
        )
        
        return 'Mensagem enviada!', 200

    return 'Nenhuma mensagem recebida.', 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
