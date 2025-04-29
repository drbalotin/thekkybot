from flask import Flask, request
from twilio.rest import Client
import openai
import os

# Configurar as variáveis de ambiente
account_sid = os.environ.get('AC509e8e6917af68a8252c60272177f6a4')
auth_token = os.environ.get('2e7c16b889b68d74f1e894b4c95bf085')
twilio_whatsapp_number = os.environ.get('whatsapp:+14155238886')
openai_api_key = os.environ.get('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
')


# Configurar a chave da OpenAI
openai.api_key = openai_api_key

# Criar o cliente Twilio
client = Client(account_sid, auth_token)

# Criar a aplicação Flask
app = Flask(__name__)

# Definir a rota para receber mensagens
@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    if incoming_msg:
        try:
            # Fazer chamada para a OpenAI
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é o THEKKYBOT, assistente inteligente e eficiente da empresa THEKKY."},
                    {"role": "user", "content": incoming_msg}
                ]
            )

            reply = gpt_response['choices'][0]['message']['content']

            # Enviar resposta pelo WhatsApp
            message = client.messages.create(
                from_=twilio_whatsapp_number,
                body=reply,
                to=from_number
            )

        except Exception as e:
            print(f"Erro ao consultar OpenAI: {e}")
            client.messages.create(
                from_=twilio_whatsapp_number,
                body="Desculpe, houve um erro ao processar sua mensagem.",
                to=from_number
            )

    return 'OK', 200

# Executar a aplicação
if __name__ == '__main__':
    app.run()
