import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def create_self_signed_cert():
    print("[*] Генерация приватного ключа RSA (2048 бит)...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Настройка имени эмитента и субъекта (для тестов делаем одинаковыми)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Yandex LLC Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, "quasar.yandex.net"),
    ])

    # Настройка альтернативных имён (SAN), на которые будет отзываться сертификат
    alt_names = x509.SubjectAlternativeName([
        x509.DNSName("quasar.yandex.net"),
        x509.DNSName("alisa.yandex.ru"),
        x509.DNSName("penda.yandex.net"),
    ])

    print("[*] Формирование структуры сертификата...")
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        # Сертификат будет валиден в течение 1 года
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).add_extension(
        alt_names, critical=False
    ).sign(private_key, hashes.SHA256())

    print("[->] Запись файлов ключа и сертификата на диск...")
    # Сохраняем приватный ключ
    with open("server.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Сохраняем сам сертификат
    with open("server.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print("[+] Готово! Файлы 'server.key' и 'server.crt' успешно созданы в текущей папке.")

if __name__ == "__main__":
    create_self_signed_cert()
