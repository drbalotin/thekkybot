from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# Chave da OpenAI pega das variáveis de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route("/", methods=['GET'])
def home():
    return "👋 Olá! O TECBOT está ativo!"

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    if not incoming_msg:
        return "Nenhuma mensagem recebida", 400

    try:
        # Faz a consulta ao ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente educado e prestativo."},
                {"role": "user", "content": incoming_msg}
            ]
        )

        resposta_chatgpt = response['choices'][0]['message']['content'].strip()

    except Exception as e:
        resposta_chatgpt = "Desculpe, houve um erro ao processar sua mensagem."

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(resposta_chatgpt)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
