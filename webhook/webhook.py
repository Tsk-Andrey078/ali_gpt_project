from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

# Установите свой API-ключ OpenAI
openai.api_key = 'your-openai-api-key'

# Конфигурация AmoCRM API
AMOCRM_ACCESS_TOKEN = 'your-amocrm-access-token'
AMOCRM_WEBHOOK_URL = 'https://your-amocrm-webhook-url'

# Вебхук для получения сообщений от AmoCRM
@app.route('/webhook', methods=['POST'])
def webhook():
    
    # Вывод заголовков запроса
    print("Headers: ", request.headers)
    
    # Вывод типа содержимого
    print("Content-Type: ", request.content_type)
    
    # Вывод содержимого запроса
    print("Data: ", request.data.decode('utf-8'))

    data = request.json
    print("Webhook Activated")
    # Извлекаем сообщение от Instagram через AmoCRM
    if 'message' in data:
        message = data['message']
        print(message)
        # Вызываем GPT API с сообщением
#        gpt_response = get_gpt_response(message)

        # Отправляем ответ обратно в AmoCRM
#       send_response_to_amocrm(gpt_response, data)
#
#    return jsonify({"status": "success"}), 200
    return 0
# Функция для отправки запроса в GPT API
def get_gpt_response(message):

    return message

# Функция для отправки ответа обратно в AmoCRM/Instagram
def send_response_to_amocrm(gpt_response, original_data):
    # Здесь вы можете использовать оригинальные данные, чтобы вернуть ответ обратно в Instagram через AmoCRM
    chat_id = original_data.get('chat_id')

    # Пример запроса на отправку сообщения в AmoCRM
    headers = {
        'Authorization': f'Bearer {AMOCRM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'chat_id': chat_id,
        'text': gpt_response
    }

    response = requests.post(f'{AMOCRM_WEBHOOK_URL}/send-message', headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent successfully to Instagram")
    else:
        print("Failed to send message:", response.text)

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
