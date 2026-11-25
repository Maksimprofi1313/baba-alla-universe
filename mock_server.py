from flask import Flask, jsonify, request, Response

app = Flask(__name__)

@app.route('/generate_204', methods=['GET', 'HEAD', 'POST'])
def generate_204():
    print("\n[+] Колонка проверяет интернет через /generate_204")
    print(f"[*] Заголовки: {dict(request.headers)}")
    
    # Возвращаем фирменный пустой ответ со статусом 204 (No Content),
    # чтобы колонка подумала, что успешно подключилась к настоящему Яндексу
    resp = Response(status=204)
    resp.headers['Connection'] = 'close'
    return resp

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    print(f"\n[!] ПОЙМАН ДРУГОЙ HTTP-ЗАПРОС!")
    print(f"[*] Путь: /{path}")
    print(f"[*] Метод: {request.method}")
    print(f"[*] Заголовки: {dict(request.headers)}")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("[*] Запуск HTTP сервера с поддержкой статуса 204...")
    print("[*] Порт: 80. Ожидание...")
    app.run(host='0.0.0.0', port=80, debug=False)
