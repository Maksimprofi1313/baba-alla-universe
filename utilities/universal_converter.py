import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
import threading


# --- Фиатные валюты ---

FIAT_CURRENCIES = {
    "USD": "🇺🇸 Доллар США",
    "EUR": "🇪🇺 Евро",
    "RUB": "🇷🇺 Российский рубль",
    "CNY": "🇨🇳 Китайский юань",
    "GBP": "🇬🇧 Фунт стерлингов",
    "JPY": "🇯🇵 Японская йена",
    "KZT": "🇰🇿 Казахстанский тенге",
    "BYN": "🇧🇾 Белорусский рубль",
    "TRY": "🇹🇷 Турецкая лира",
    "CHF": "🇨🇭 Швейцарский франк",
    "CAD": "🇨🇦 Канадский доллар",
    "AUD": "🇦🇺 Австралийский доллар",
    "INR": "🇮🇳 Индийская рупия",
    "KRW": "🇰🇷 Южнокорейская вона",
    "BRL": "🇧🇷 Бразильский реал",
    "UAH": "🇺🇦 Украинская гривна",
}

# --- Криптовалюты (тикер: (coingecko_id, название)) ---

CRYPTO_CURRENCIES = {
    "BTC": ("bitcoin", "₿ Биткоин"),
    "ETH": ("ethereum", "Ξ Эфириум"),
    "USDT": ("tether", "💵 Tether (ERC20/TRC20)"),
    "USDT-BEP20": ("tether", "🟡 USDT (BEP20)"),
    "BNB": ("binancecoin", "🟡 Binance Coin"),
    "SOL": ("solana", "◎ Solana"),
    "XRP": ("ripple", "💧 XRP"),
    "TON": ("the-open-network", "💎 Toncoin"),
    "GRAM": ("the-open-network", "💎 Gram (бывш. TON)"),
    "DOGE": ("dogecoin", "🐕 Dogecoin"),
    "AVAX": ("avalanche-2", "🔺 Avalanche"),
    "DOT": ("polkadot", "🔴 Polkadot"),
    "MATIC": ("matic-network", "🟣 Polygon"),
    "LTC": ("litecoin", "Ł Litecoin"),
    "TRX": ("tron", "🔺 TRON"),
    "USDC": ("usd-coin", "🔵 USD Coin"),
}


# --- Фиатный курс через open.er-api.com ---

def get_fiat_rate(from_code, to_code):
    """Курс фиатной валюты через open.er-api.com (без ключа)."""
    url = f"https://open.er-api.com/v6/latest/{from_code}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("result") != "success":
            return None, "API вернул ошибку"
        rate = data.get("rates", {}).get(to_code)
        if rate is None:
            return None, f"Курс для {to_code} не найден"
        return rate, None
    except Exception as e:
        return None, str(e)


# --- Курс крипты через CoinGecko ---

def get_crypto_price(crypto_id, vs_currency):
    """Цена криптовалюты в фиате через CoinGecko (без ключа)."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={vs_currency.lower()}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        price = data.get(crypto_id, {}).get(vs_currency.lower())
        return price, None
    except Exception as e:
        return None, str(e)


# --- Цена USDT BEP20 через CoinGecko ---

def get_usdt_bep20_price(vs_currency="usd"):
    """Цена USDT BEP20 по контрактному адресу."""
    contract = "0x55d398326f99059ff775485246999027b3197955"
    url = f"https://api.coingecko.com/api/v3/simple/token_price/binance-smart-chain?contract_addresses={contract}&vs_currencies={vs_currency.lower()}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        price = data.get(contract.lower(), {}).get(vs_currency.lower())
        return price, None
    except Exception as e:
        return None, str(e)


# --- Графический интерфейс ---

class UniversalConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Универсальный конвертер — Валюты и Крипта")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        tk.Label(root, text="💱 Универсальный конвертер",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.fiat_frame = tk.Frame(self.notebook)
        self.notebook.add(self.fiat_frame, text="💵 Валюта → Валюта")
        self._build_fiat_tab()

        self.fiat_crypto_frame = tk.Frame(self.notebook)
        self.notebook.add(self.fiat_crypto_frame, text="💵→₿ Валюта → Крипта")
        self._build_fiat_crypto_tab()

        self.crypto_fiat_frame = tk.Frame(self.notebook)
        self.notebook.add(self.crypto_fiat_frame, text="₿→💵 Крипта → Валюта")
        self._build_crypto_fiat_tab()

        self.crypto_frame = tk.Frame(self.notebook)
        self.notebook.add(self.crypto_frame, text="₿→₿ Крипта → Крипта")
        self._build_crypto_tab()

        self.status_label = tk.Label(root, text="Готово", font=("Segoe UI", 9), fg="gray")
        self.status_label.pack(pady=5)

    def _build_fiat_tab(self):
        tk.Label(self.fiat_frame, text="Сумма:", font=("Segoe UI", 10)).pack(pady=5)
        self.fiat_amount = tk.StringVar(value="100")
        tk.Entry(self.fiat_frame, textvariable=self.fiat_amount,
                 font=("Segoe UI", 12), justify="center").pack(fill="x", padx=20)

        tk.Label(self.fiat_frame, text="Из валюты:", font=("Segoe UI", 10)).pack(pady=5)
        self.fiat_from = tk.StringVar(value="USD")
        ttk.Combobox(self.fiat_frame, textvariable=self.fiat_from,
                     values=[f"{k} — {v}" for k, v in FIAT_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Label(self.fiat_frame, text="В валюту:", font=("Segoe UI", 10)).pack(pady=5)
        self.fiat_to = tk.StringVar(value="RUB")
        ttk.Combobox(self.fiat_frame, textvariable=self.fiat_to,
                     values=[f"{k} — {v}" for k, v in FIAT_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Button(self.fiat_frame, text="Конвертировать", font=("Segoe UI", 11, "bold"),
                  bg="#2196F3", fg="white", padx=20, pady=8,
                  command=lambda: self.run_conversion("fiat")).pack(pady=15)

        self.fiat_result = tk.StringVar(value="—")
        tk.Entry(self.fiat_frame, textvariable=self.fiat_result, font=("Segoe UI", 14, "bold"),
                 justify="center", state="readonly",
                 readonlybackground="#f0f0f0").pack(fill="x", padx=20)

    def _build_fiat_crypto_tab(self):
        tk.Label(self.fiat_crypto_frame, text="Сумма:", font=("Segoe UI", 10)).pack(pady=5)
        self.fc_amount = tk.StringVar(value="100")
        tk.Entry(self.fiat_crypto_frame, textvariable=self.fc_amount,
                 font=("Segoe UI", 12), justify="center").pack(fill="x", padx=20)

        tk.Label(self.fiat_crypto_frame, text="Из валюты:", font=("Segoe UI", 10)).pack(pady=5)
        self.fc_from = tk.StringVar(value="USD")
        ttk.Combobox(self.fiat_crypto_frame, textvariable=self.fc_from,
                     values=[f"{k} — {v}" for k, v in FIAT_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Label(self.fiat_crypto_frame, text="В криптовалюту:", font=("Segoe UI", 10)).pack(pady=5)
        self.fc_to = tk.StringVar(value="BTC — ₿ Биткоин")
        ttk.Combobox(self.fiat_crypto_frame, textvariable=self.fc_to,
                     values=[f"{k} — {v[1]}" for k, v in CRYPTO_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Button(self.fiat_crypto_frame, text="Конвертировать", font=("Segoe UI", 11, "bold"),
                  bg="#FF9800", fg="white", padx=20, pady=8,
                  command=lambda: self.run_conversion("fiat_crypto")).pack(pady=15)

        self.fc_result = tk.StringVar(value="—")
        tk.Entry(self.fiat_crypto_frame, textvariable=self.fc_result, font=("Segoe UI", 14, "bold"),
                 justify="center", state="readonly",
                 readonlybackground="#f0f0f0").pack(fill="x", padx=20)

    def _build_crypto_fiat_tab(self):
        tk.Label(self.crypto_fiat_frame, text="Сумма:", font=("Segoe UI", 10)).pack(pady=5)
        self.cf_amount = tk.StringVar(value="1")
        tk.Entry(self.crypto_fiat_frame, textvariable=self.cf_amount,
                 font=("Segoe UI", 12), justify="center").pack(fill="x", padx=20)

        tk.Label(self.crypto_fiat_frame, text="Из криптовалюты:", font=("Segoe UI", 10)).pack(pady=5)
        self.cf_from = tk.StringVar(value="BTC — ₿ Биткоин")
        ttk.Combobox(self.crypto_fiat_frame, textvariable=self.cf_from,
                     values=[f"{k} — {v[1]}" for k, v in CRYPTO_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Label(self.crypto_fiat_frame, text="В валюту:", font=("Segoe UI", 10)).pack(pady=5)
        self.cf_to = tk.StringVar(value="RUB")
        ttk.Combobox(self.crypto_fiat_frame, textvariable=self.cf_to,
                     values=[f"{k} — {v}" for k, v in FIAT_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Button(self.crypto_fiat_frame, text="Конвертировать", font=("Segoe UI", 11, "bold"),
                  bg="#9C27B0", fg="white", padx=20, pady=8,
                  command=lambda: self.run_conversion("crypto_fiat")).pack(pady=15)

        self.cf_result = tk.StringVar(value="—")
        tk.Entry(self.crypto_fiat_frame, textvariable=self.cf_result, font=("Segoe UI", 14, "bold"),
                 justify="center", state="readonly",
                 readonlybackground="#f0f0f0").pack(fill="x", padx=20)

    def _build_crypto_tab(self):
        tk.Label(self.crypto_frame, text="Сумма:", font=("Segoe UI", 10)).pack(pady=5)
        self.crypto_amount = tk.StringVar(value="1")
        tk.Entry(self.crypto_frame, textvariable=self.crypto_amount,
                 font=("Segoe UI", 12), justify="center").pack(fill="x", padx=20)

        tk.Label(self.crypto_frame, text="Из криптовалюты:", font=("Segoe UI", 10)).pack(pady=5)
        self.crypto_from = tk.StringVar(value="BTC — ₿ Биткоин")
        ttk.Combobox(self.crypto_frame, textvariable=self.crypto_from,
                     values=[f"{k} — {v[1]}" for k, v in CRYPTO_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Label(self.crypto_frame, text="В криптовалюту:", font=("Segoe UI", 10)).pack(pady=5)
        self.crypto_to = tk.StringVar(value="ETH — Ξ Эфириум")
        ttk.Combobox(self.crypto_frame, textvariable=self.crypto_to,
                     values=[f"{k} — {v[1]}" for k, v in CRYPTO_CURRENCIES.items()],
                     state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20)

        tk.Button(self.crypto_frame, text="Конвертировать", font=("Segoe UI", 11, "bold"),
                  bg="#4CAF50", fg="white", padx=20, pady=8,
                  command=lambda: self.run_conversion("crypto")).pack(pady=15)

        self.crypto_result = tk.StringVar(value="—")
        tk.Entry(self.crypto_frame, textvariable=self.crypto_result, font=("Segoe UI", 14, "bold"),
                 justify="center", state="readonly",
                 readonlybackground="#f0f0f0").pack(fill="x", padx=20)

    @staticmethod
    def get_code(value):
        return value.split(" — ")[0]

    def run_conversion(self, mode):
        if mode == "fiat":
            amount_var, from_var, to_var, result_var = self.fiat_amount, self.fiat_from, self.fiat_to, self.fiat_result
        elif mode == "fiat_crypto":
            amount_var, from_var, to_var, result_var = self.fc_amount, self.fc_from, self.fc_to, self.fc_result
        elif mode == "crypto_fiat":
            amount_var, from_var, to_var, result_var = self.cf_amount, self.cf_from, self.cf_to, self.cf_result
        else:
            amount_var, from_var, to_var, result_var = self.crypto_amount, self.crypto_from, self.crypto_to, self.crypto_result

        try:
            amount = float(amount_var.get().replace(",", "."))
            if amount < 0:
                raise ValueError("Сумма не может быть отрицательной")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму")
            return

        from_code = self.get_code(from_var.get())
        to_code = self.get_code(to_var.get())

        self.status_label.config(text="Загрузка курса...", fg="blue")

        def worker():
            try:
                result = None

                # --- Фиат → Фиат ---
                if mode == "fiat":
                    rate, error = get_fiat_rate(from_code, to_code)
                    if error:
                        raise Exception(error)
                    result = amount * rate

                # --- Фиат → Крипта ---
                elif mode == "fiat_crypto":
                    crypto_id = CRYPTO_CURRENCIES[to_code][0]

                    if to_code == "USDT-BEP20":
                        price_usd, error = get_usdt_bep20_price("usd")
                        if error or price_usd is None:
                            raise Exception(error or "Не удалось получить цену USDT BEP20")
                        if from_code != "USD":
                            rate_fiat, err = get_fiat_rate(from_code, "USD")
                            if err:
                                raise Exception(err)
                            amount_usd = amount * rate_fiat
                        else:
                            amount_usd = amount
                        result = amount_usd / price_usd
                    else:
                        price, error = get_crypto_price(crypto_id, from_code)
                        if error or price is None:
                            raise Exception(error or f"Не удалось получить цену {to_code}")
                        result = amount / price

                # --- Крипта → Фиат ---
                elif mode == "crypto_fiat":
                    crypto_id = CRYPTO_CURRENCIES[from_code][0]

                    if from_code == "USDT-BEP20":
                        price_usd, error = get_usdt_bep20_price("usd")
                        if error or price_usd is None:
                            raise Exception(error or "Не удалось получить цену USDT BEP20")
                        amount_usd = amount * price_usd
                        if to_code != "USD":
                            rate_fiat, err = get_fiat_rate("USD", to_code)
                            if err:
                                raise Exception(err)
                            result = amount_usd * rate_fiat
                        else:
                            result = amount_usd
                    else:
                        price, error = get_crypto_price(crypto_id, to_code)
                        if error or price is None:
                            raise Exception(error or f"Не удалось получить цену {from_code}")
                        result = amount * price

                # --- Крипта → Крипта ---
                else:
                    from_id = CRYPTO_CURRENCIES[from_code][0]
                    to_id = CRYPTO_CURRENCIES[to_code][0]

                    if from_code == "USDT-BEP20":
                        from_price, err = get_usdt_bep20_price("usd")
                    else:
                        from_price, err = get_crypto_price(from_id, "USD")
                    if err or from_price is None:
                        raise Exception(err or f"Не удалось получить цену {from_code}")

                    if to_code == "USDT-BEP20":
                        to_price, err = get_usdt_bep20_price("usd")
                    else:
                        to_price, err = get_crypto_price(to_id, "USD")
                    if err or to_price is None:
                        raise Exception(err or f"Не удалось получить цену {to_code}")

                    result = amount * (from_price / to_price)

                self.root.after(0, lambda: result_var.set(f"{result:,.6f} {to_code}"))
                self.root.after(0, lambda: self.status_label.config(text="✅ Конвертация выполнена", fg="green"))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Не удалось конвертировать:\n{e}"))
                self.root.after(0, lambda: self.status_label.config(text="Ошибка", fg="red"))

        threading.Thread(target=worker, daemon=True).start()


# --- Запуск ---

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalConverterApp(root)
    root.mainloop()