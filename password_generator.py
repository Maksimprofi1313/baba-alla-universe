import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import math


# --- Логика генерации пароля ---

def generate_password(length, use_lower, use_upper, use_digits, use_special):
    """Генерирует пароль заданной длины из выбранных наборов символов."""
    alphabet = ""
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += "!@#$%^&*()-_=+[]{};:,.<>?/|~"

    if not alphabet:
        return None, 0, "Не выбран ни один набор символов"

    # secrets — криптографически стойкий генератор
    password = "".join(secrets.choice(alphabet) for _ in range(length))

    # Оценка энтропии (в битах)
    entropy = length * math.log2(len(alphabet))

    # Оценка надёжности
    if entropy < 40:
        strength = "Очень слабый"
    elif entropy < 60:
        strength = "Слабый"
    elif entropy < 80:
        strength = "Средний"
    elif entropy < 100:
        strength = "Надёжный"
    else:
        strength = "Очень надёжный"

    return password, entropy, strength


# --- Графический интерфейс ---

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("560x480")
        self.root.resizable(False, False)

        # --- Заголовок ---
        title = tk.Label(
            root,
            text="🔐 Генератор паролей",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(pady=10)

        # --- Длина пароля ---
        length_frame = tk.LabelFrame(root, text="Длина пароля", padx=10, pady=10)
        length_frame.pack(fill="x", padx=15, pady=5)

        self.length_var = tk.IntVar(value=16)
        self.length_label = tk.Label(length_frame, text="16", width=3, font=("Segoe UI", 11, "bold"))
        self.length_label.pack(side="right", padx=5)

        self.length_scale = tk.Scale(
            length_frame,
            from_=4,
            to=64,
            orient="horizontal",
            variable=self.length_var,
            command=self.update_length_label,
            length=400
        )
        self.length_scale.pack(side="left", fill="x", expand=True)

        # --- Наборы символов ---
        chars_frame = tk.LabelFrame(root, text="Наборы символов", padx=10, pady=10)
        chars_frame.pack(fill="x", padx=15, pady=5)

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)

        tk.Checkbutton(chars_frame, text="Строчные (a-z)", variable=self.lower_var).grid(row=0, column=0, sticky="w", padx=5)
        tk.Checkbutton(chars_frame, text="Прописные (A-Z)", variable=self.upper_var).grid(row=0, column=1, sticky="w", padx=5)
        tk.Checkbutton(chars_frame, text="Цифры (0-9)", variable=self.digits_var).grid(row=1, column=0, sticky="w", padx=5)
        tk.Checkbutton(chars_frame, text="Спецсимволы (!@#$)", variable=self.special_var).grid(row=1, column=1, sticky="w", padx=5)

        # --- Кнопка генерации ---
        gen_btn = tk.Button(
            root,
            text="Сгенерировать пароль",
            font=("Segoe UI", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=20,
            pady=8,
            command=self.on_generate
        )
        gen_btn.pack(pady=15)

        # --- Результат ---
        result_frame = tk.LabelFrame(root, text="Результат", padx=10, pady=10)
        result_frame.pack(fill="x", padx=15, pady=5)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            result_frame,
            textvariable=self.password_var,
            font=("Consolas", 13),
            justify="center",
            state="readonly",
            readonlybackground="#f0f0f0"
        )
        self.password_entry.pack(fill="x", pady=5)

        # --- Надёжность ---
        self.strength_label = tk.Label(
            result_frame,
            text="Надёжность: —",
            font=("Segoe UI", 10, "italic")
        )
        self.strength_label.pack()

        self.entropy_label = tk.Label(
            result_frame,
            text="Энтропия: — бит",
            font=("Segoe UI", 9)
        )
        self.entropy_label.pack()

        # --- Кнопки копирования и очистки ---
        btn_frame = tk.Frame(result_frame)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="📋 Копировать", command=self.copy_to_clipboard, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑 Очистить", command=self.clear_password, width=15).pack(side="left", padx=5)

        # --- Статус ---
        self.status_label = tk.Label(root, text="", font=("Segoe UI", 9), fg="gray")
        self.status_label.pack(pady=5)

    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))

    def on_generate(self):
        length = self.length_var.get()
        use_lower = self.lower_var.get()
        use_upper = self.upper_var.get()
        use_digits = self.digits_var.get()
        use_special = self.special_var.get()

        password, entropy, strength = generate_password(
            length, use_lower, use_upper, use_digits, use_special
        )

        if password is None:
            messagebox.showwarning("Ошибка", strength)
            return

        self.password_var.set(password)
        self.strength_label.config(text=f"Надёжность: {strength}")
        self.entropy_label.config(text=f"Энтропия: {entropy:.1f} бит")
        self.status_label.config(text="Пароль сгенерирован", fg="green")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if not password:
            self.status_label.config(text="Сначала сгенерируйте пароль", fg="red")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.status_label.config(text="✅ Пароль скопирован в буфер обмена", fg="green")

    def clear_password(self):
        self.password_var.set("")
        self.strength_label.config(text="Надёжность: —")
        self.entropy_label.config(text="Энтропия: — бит")
        self.status_label.config(text="Поле очищено", fg="gray")


# --- Запуск ---

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()