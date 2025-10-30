import tkinter as tk
from tkinter import messagebox

class AddTaskWindow(tk.Toplevel):
    def __init__(self, master, on_save):
        super().__init__(master)
        self.title("Add New Task")
        self.geometry("300x200+1350+350")
        self.on_save = on_save

        tk.Label(self, text="Task Title:").pack(pady=5)
        self.title_entry = tk.Entry(self, width=30)
        self.title_entry.pack(pady=5)

        tk.Label(self, text="Description:").pack(pady=5)
        self.desc_entry = tk.Entry(self, width=30)
        self.desc_entry.pack(pady=5)

        tk.Button(self, text="Save", command=self.save_task).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.destroy).pack()

    def save_task(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty.")
            return
        self.on_save(title, desc)
        self.destroy()
