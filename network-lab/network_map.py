import tkinter as tk
import subprocess
import threading
import time
import os
import math
import socket

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
        """Пингует IP (Windows, 1 пакет)."""
        try:
            startupinfo = None
            creationflags = 0
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            else:
                # На Unix-подобных системах используем совместимые параметры ping.
                pass
            command = ["ping", "-n", "1", "-w", "200", ip] if os.name == "nt" else ["ping", "-c", "1", "-W", "1", ip]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="ignore",
                                    startupinfo=startupinfo, creationflags=creationflags, timeout=3)
            return result.returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False

    def get_mac(self, ip):
        """Получает MAC-адрес для IP через ARP."""
        try:
            result = subprocess.run(["arp", "-a", ip], capture_output=True, text=True,
                                    encoding="utf-8", errors="ignore", timeout=3)
            import re
            match = re.search(r'([0-9a-fA-F\-]{17})', result.stdout)
            if match:
                return match.group(1).upper().replace("-", ":")
        except (OSError, subprocess.SubprocessError):
            pass
        return "00:00:00:00:00:00"

    def deep_scan(self):
        """Пингует адреса локальной IPv4 /24 подсети."""
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            subnet = ".".join(local_ip.split(".")[:3]) + "."
        except OSError:
            self.root.after(0, lambda: self.draw_map([]))
            return

        devices = []
        threads = []
        lock = threading.Lock()

        def check_host(i):
            ip = f"{subnet}{i}"
            if self.ping_ip(ip):
                mac = self.get_mac(ip)
                with lock:
                    devices.append({"ip": ip, "mac": mac})

        for i in range(1, 255):
            thread = threading.Thread(target=check_host, args=(i,), daemon=True)
            thread.start()
            threads.append(thread)
            if len(threads) >= 32:
                for thread in threads:
                    thread.join()
                threads = []
        for thread in threads:
            thread.join()
        devices.sort(key=lambda item: int(item["ip"].split(".")[-1]))
        self.root.after(0, lambda: self.draw_map(devices))

    def draw_map(self, devices):
        self.canvas.delete("all")
        router_ip = "192.168.0.1"
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
        except OSError:
            local_ip = ""
        other_devices = [d for d in devices if d["ip"] not in (router_ip, local_ip)]
        cx, cy = 450, 350
        self.canvas.create_oval(cx-40, cy-40, cx+40, cy+40, fill="#2196F3", outline="white", width=2)
        self.canvas.create_text(cx, cy, text="🌐\nРоутер", fill="white", font=("Segoe UI", 10, "bold"), justify="center")
        if not other_devices:
            self.canvas.create_text(cx, cy+100, text="Другие устройства не обнаружены.", fill="gray")
            return
        angle_step = 2 * math.pi / len(other_devices)
        radius = 220
        for i, dev in enumerate(other_devices):
            angle = i * angle_step
            x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
            self.canvas.create_line(cx, cy, x, y, fill="#4CAF50", width=2)
            r = 30
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#4CAF50", outline="white", width=1)
            self.canvas.create_text(x, y, text="💻", font=("Segoe UI", 16))
            label_y = y + r + 15
            self.canvas.create_text(x, label_y, text=dev["ip"], fill="white", font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x, label_y + 15, text=dev["mac"], fill="#aaaaaa", font=("Consolas", 8))

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMapApp(root)
    root.mainloop()
