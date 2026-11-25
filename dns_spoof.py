import socket

# Ваш IP-адрес из ipconfig
LOCAL_IP = "192.168.0.50"

def build_dns_response(data):
    # Разбираем ID запроса (первые 2 байта)
    Transaction_ID = data[:2]
    
    # Флаги для ответа (Standard query response, No error)
    Flags = b'\x81\x80'
    
    # Количество вопросов и ответов
    QDCOUNT = data[4:6]
    ANCOUNT = b'\x00\x01' # Возвращаем 1 ответ
    NSCOUNT = b'\x00\x00'
    ARCOUNT = b'\x00\x00'
    
    # Блок вопроса (идет после 12 байт заголовка)
    end_of_name = data[12:].find(b'\x00') + 13
    Question_Block = data[12:end_of_name + 4] # Имя + тип + класс
    
    # Формируем блок ответа (Answer)
    Answer_Name = b'\xc0\x0c'
    Answer_Type = b'\x00\x01'  # Тип A (IPv4)
    Answer_Class = b'\x00\x01' # Класс IN
    Answer_TTL = b'\x00\x00\x00\x3c' # Время жизни записи (60 секунд)
    Answer_Len = b'\x00\x04'  # Длина IP-адреса (4 байта)
    
    # Превращаем IP в байты
    Answer_IP = bytes(map(int, LOCAL_IP.split('.')))
    
    return Transaction_ID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT + Question_Block + Answer_Name + Answer_Type + Answer_Class + Answer_TTL + Answer_Len + Answer_IP

def parse_domain_name(data):
    try:
        parts = []
        i = 12
        while True:
            length = data[i]
            if length == 0:
                break
            parts.append(data[i+1:i+1+length].decode('utf-8', errors='ignore'))
            i += 1 + length
        return ".".join(parts)
    except:
        return "unknown"

def start_dns_server():
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        udps.bind(('0.0.0.0', 53))
        print(f"[*] ГЛОБАЛЬНЫЙ DNS-перехватчик запущен на порту 53.")
        print(f"[*] Все запросы, содержащие 'yandex', идут на: {LOCAL_IP}")
        print("[*] Ожидание запросов от устройства... (Нажмите CTRL+C для выхода)")
    except OSError:
        print(f"[-] Ошибка: Не удалось занять порт 53. Проверьте, выключен ли режим TUN в VPN.")
        return

    while True:
        try:
            data, addr = udps.recvfrom(1024)
            domain = parse_domain_name(data)
            
            # Тотальный перехват любого домена Яндекса (главные облака, телеметрия, логи)
            if "yandex" in domain:
                print(f"[+] ПЕРЕХВАЧЕН ЗАПРОС от {addr} к домену: {domain}")
                response = build_dns_response(data)
                udps.sendto(response, addr)
                print(f"[->] Отправлен фейковый ответ: {domain} -> {LOCAL_IP}")
        except KeyboardInterrupt:
            print("\n[*] Остановка сервера.")
            break
        except Exception as e:
            print(f"[!] Ошибка обработки пакета: {e}")

if __name__ == "__main__":
    start_dns_server()
