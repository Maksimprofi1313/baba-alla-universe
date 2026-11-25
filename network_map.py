import tkinter as tk
import subprocess
import threading
import time
import os
import math

class NetworkMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Карта моей сети (Глубокое сканирование)")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")

        self.canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.btn_refresh = tk.Button(root, text="🔄 Сканировать сеть (займет ~10 сек)", 
                                     font=("Segoe UI", 10, "bold"),
                                     bg="#4CAF50", fg="white", command=self.start_scan_thread)
        self.btn_refresh.pack(pady=10)

        self.start_scan_thread()

    def start_scan_thread(self):
        self.canvas.delete("all")
        self.canvas.create_text(450, 350, text="Глубокое сканирование сети...\n(это может занять 10-15 секунд)", 
                                fill="white", font=("Segoe UI", 14), justify="center")
        threading.Thread(target=self.deep_scan, daemon=True).start()

    def ping_ip(self, ip):
        """Пингует IP (быстро, 1 пакет, таймаут 200мс)."""
        try:
            # Создаем скрытое окно для subprocess (чтобы не мелькало)
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            result = subprocess.run(
                ["ping", "-n", "1", "-w", "200", ip], 
                capture_output=True, text=True, encoding="cp866", errors="ignore",
                startupinfo=startupinfo
            )
            return "TTL=" in result.stdout
        except:
            return False

    def get_mac(self, ip):
        """Получает MAC-адрес для IP через ARP."""
        try:
            result = subprocess.run(["arp", "-a", ip], capture_output=True, text=True, encoding="cp866", errors="ignore")
            # Ищем MAC в выводе
            import re
            match = re.search(r'([0-9a-fA-F\-]{17})', result.stdout)
            if match:
                return match.group(1).upper().replace('-', ':')
        except:
            pass
        return "00:00:00:00:00:00"

    def deep_scan(self):
        """Пингует всю подсеть и собирает данные."""
        # Определяем нашу подсеть (например, 192.168.0.)
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            subnet = ".".join(local_ip.split('.')[:3]) + "."
        except:
            subnet = "192.168.0."

        devices = []
        
        # Сканируем диапазон 1-254
        # Чтобы не вешать систему, делаем это в несколько потоков
        threads = []
        
        def check_host(i):
            ip = f"{subnet}{i}"
            if self.ping_ip(ip):
                mac = self.get_mac(ip)
                devices.append({"ip": ip, "mac": mac})

        for i in range(1, 255):
            t = threading.Thread(target=check_host, args=(i,))
            t.start()
            threads.append(t)
            
            # Не запускаем больше 50 потоков одновременно
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []

        # Ждем оставшиеся
        for t in threads:
            t.join()

        # Сортируем по IP
        devices.sort(key=lambda x: int(x['ip'].split('.')[-1]))
        
        self.root.after(0, lambda: self.draw_map(devices))

    def draw_map(self, devices):
        self.canvas.delete("all")
        
        # Отфильтровываем наш ПК и роутер
        router_ip = "192.168.0.1"
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
        except:
            local_ip = "192.168.0.50"

        other_devices = [d for d in devices if d['ip'] not in [router_ip, local_ip]]

        # Рисуем роутер
        cx, cy = 450, 350
        self.canvas.create_oval(cx-40, cy-40, cx+40, cy+40, fill="#2196F3", outline="white", width=2)
        self.canvas.create_text(cx, cy, text="🌐\nРоутер", fill="white", font=("Segoe UI", 10, "bold"), justify="center")

        if not other_devices:
            self.canvas.create_text(cx, cy+100, text="Кроме роутера и твоего ПК никого нет.", fill="gray")
            return

        # Рисуем остальные
        angle_step = 2 * math.pi / len(other_devices)
        radius = 220
        
        for i, dev in enumerate(other_devices):
            angle = i * angle_step
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            # Рисуем линию
            self.canvas.create_line(cx, cy, x, y, fill="#4CAF50", width=2)
            
            # Кружок устройства
            r = 30
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#4CAF50", outline="white", width=1)
            
            # Иконка
            icon = "💻"
            mac = dev['mac']
            if mac.startswith("D8:E2:DF"):
                icon = "🎮"
            elif mac.startswith("DE:92"):
                icon = "📱"
            elif mac.startswith("98:BA:5F"):
                icon = "🌐"
                
            self.canvas.create_text(x, y, text=icon, font=("Segoe UI", 16))
            
            # Подписи
            label_y = y + r + 15
            self.canvas.create_text(x, label_y, text=dev['ip'], fill="white", font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x, label_y + 15, text=dev['mac'], fill="#aaaaaa", font=("Consolas", 8))


if __name__ == "__main__":
    import socket # Импорт для deep_scan
    root = tk.Tk()
    app = NetworkMapApp(root)
    root.mainloop()