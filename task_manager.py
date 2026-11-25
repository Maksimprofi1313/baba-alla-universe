import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import uuid
from datetime import datetime


# --- Файл для сохранения задач ---

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


# --- Логика работы с задачами ---

class TaskManager:
    """Хранит задачи и управляет ими."""

    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из JSON."""
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_tasks(self):
        """Сохраняет задачи в JSON."""
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def add_task(self, title, description="", priority="Обычный"):
        """Добавляет новую задачу."""
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "todo",  # todo / in_progress / done
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def update_task(self, task_id, **kwargs):
        """Обновляет поля задачи."""
        for task in self.tasks:
            if task["id"] == task_id:
                task.update(kwargs)
                self.save_tasks()
                return

    def delete_task(self, task_id):
        """Удаляет задачу."""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()

    def get_by_status(self, status):
        """Возвращает задачи с указанным статусом."""
        return [t for t in self.tasks if t["status"] == status]


# --- Графический интерфейс ---

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("900x600")

        self.manager = TaskManager()

        # --- Заголовок и кнопки ---
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="📋 Менеджер задач", font=("Segoe UI", 16, "bold")).pack(side="left", padx=15)

        tk.Button(top_frame, text="➕ Новая задача", font=("Segoe UI", 10, "bold"),
                  bg="#4CAF50", fg="white", padx=15, pady=5,
                  command=self.add_task_dialog).pack(side="right", padx=10)

        # --- Три колонки ---
        columns_frame = tk.Frame(root)
        columns_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.columns = {}
        for status, title, color in [
            ("todo", "📝 К выполнению", "#f0f0f0"),
            ("in_progress", "⚙️ В работе", "#fff8e1"),
            ("done", "✅ Готово", "#e8f5e9"),
        ]:
            col = tk.LabelFrame(columns_frame, text=title, font=("Segoe UI", 11, "bold"),
                                bg=color, padx=5, pady=5)
            col.pack(side="left", fill="both", expand=True, padx=5)

            # Прокручиваемый список
            canvas = tk.Canvas(col, bg=color, highlightthickness=0)
            scrollbar = tk.Scrollbar(col, orient="vertical", command=canvas.yview)
            inner_frame = tk.Frame(canvas, bg=color)

            inner_frame.bind(
                "<Configure>",
                lambda e, c=canvas: c.configure(scrollregion=c.bbox("all"))
            )
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.columns[status] = inner_frame

        self.refresh_columns()

    def refresh_columns(self):
        """Перерисовывает все колонки."""
        for status, frame in self.columns.items():
            for widget in frame.winfo_children():
                widget.destroy()

            tasks = self.manager.get_by_status(status)
            if not tasks:
                tk.Label(frame, text="Пусто", font=("Segoe UI", 9, "italic"),
                         fg="gray", bg=frame["bg"]).pack(pady=10)
                continue

            for task in tasks:
                self.render_task(frame, task)

    def render_task(self, parent, task):
        """Рисует карточку задачи."""
        card = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=8, pady=6)
        card.pack(fill="x", pady=4, padx=2)

        # Заголовок
        title = tk.Label(card, text=task["title"], font=("Segoe UI", 10, "bold"),
                         bg="white", anchor="w", wraplength=220, justify="left")
        title.pack(fill="x")

        # Описание (если есть)
        if task.get("description"):
            desc = tk.Label(card, text=task["description"], font=("Segoe UI", 9),
                            bg="white", fg="#555", anchor="w", wraplength=220, justify="left")
            desc.pack(fill="x", pady=(2, 0))

        # Приоритет + дата
        meta = tk.Label(card, text=f"{task.get('priority', '—')} • {task.get('created', '')}",
                        font=("Segoe UI", 8), bg="white", fg="#888", anchor="w")
        meta.pack(fill="x", pady=(4, 0))

        # Кнопки управления
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill="x", pady=(5, 0))

        # Кнопка «назад» (если не todo)
        if task["status"] != "todo":
            tk.Button(btn_frame, text="←", width=3, font=("Segoe UI", 9),
                      command=lambda t=task: self.move_task(t, "prev")).pack(side="left", padx=1)

        # Кнопка «вперёд» (если не done)
        if task["status"] != "done":
            tk.Button(btn_frame, text="→", width=3, font=("Segoe UI", 9),
                      command=lambda t=task: self.move_task(t, "next")).pack(side="left", padx=1)

        # Удалить
        tk.Button(btn_frame, text="🗑", width=3, font=("Segoe UI", 9), fg="red",
                  command=lambda t=task: self.delete_task(t)).pack(side="right", padx=1)

        # Редактировать
        tk.Button(btn_frame, text="✏", width=3, font=("Segoe UI", 9),
                  command=lambda t=task: self.edit_task_dialog(t)).pack(side="right", padx=1)

    def move_task(self, task, direction):
        """Перемещает задачу между колонками."""
        order = ["todo", "in_progress", "done"]
        current = order.index(task["status"])
        if direction == "next" and current < len(order) - 1:
            new_status = order[current + 1]
        elif direction == "prev" and current > 0:
            new_status = order[current - 1]
        else:
            return
        self.manager.update_task(task["id"], status=new_status)
        self.refresh_columns()

    def delete_task(self, task):
        """Удаляет задачу с подтверждением."""
        if messagebox.askyesno("Удалить задачу", f"Удалить «{task['title']}»?"):
            self.manager.delete_task(task["id"])
            self.refresh_columns()

    def add_task_dialog(self):
        """Диалог добавления новой задачи."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новая задача")
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Название:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        title_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=40)
        title_entry.pack()
        title_entry.focus()

        tk.Label(dialog, text="Описание:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        desc_entry = tk.Text(dialog, font=("Segoe UI", 10), width=40, height=5)
        desc_entry.pack()

        tk.Label(dialog, text="Приоритет:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        priority_var = tk.StringVar(value="Обычный")
        ttk.Combobox(dialog, textvariable=priority_var,
                     values=["Низкий", "Обычный", "Высокий", "Критичный"],
                     state="readonly", font=("Segoe UI", 10)).pack()

        def save():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Ошибка", "Название не может быть пустым")
                return
            desc = desc_entry.get("1.0", "end").strip()
            self.manager.add_task(title, desc, priority_var.get())
            dialog.destroy()
            self.refresh_columns()

        tk.Button(dialog, text="Сохранить", font=("Segoe UI", 10, "bold"),
                  bg="#4CAF50", fg="white", padx=20, pady=5,
                  command=save).pack(pady=20)

    def edit_task_dialog(self, task):
        """Диалог редактирования задачи."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать задачу")
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Название:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        title_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=40)
        title_entry.insert(0, task["title"])
        title_entry.pack()

        tk.Label(dialog, text="Описание:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        desc_entry = tk.Text(dialog, font=("Segoe UI", 10), width=40, height=5)
        desc_entry.insert("1.0", task.get("description", ""))
        desc_entry.pack()

        tk.Label(dialog, text="Приоритет:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        priority_var = tk.StringVar(value=task.get("priority", "Обычный"))
        ttk.Combobox(dialog, textvariable=priority_var,
                     values=["Низкий", "Обычный", "Высокий", "Критичный"],
                     state="readonly", font=("Segoe UI", 10)).pack()

        def save():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Ошибка", "Название не может быть пустым")
                return
            desc = desc_entry.get("1.0", "end").strip()
            self.manager.update_task(task["id"], title=title, description=desc,
                                     priority=priority_var.get())
            dialog.destroy()
            self.refresh_columns()

        tk.Button(dialog, text="Сохранить", font=("Segoe UI", 10, "bold"),
                  bg="#2196F3", fg="white", padx=20, pady=5,
                  command=save).pack(pady=20)


# --- Запуск ---

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()