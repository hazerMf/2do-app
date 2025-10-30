import tkinter as tk
from tkinter import messagebox
import json, os

from app import TodoApp 

ACCOUNT_FILE = "src/account.json"

def load_accounts():
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "r") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []
    return []

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.accounts = load_accounts()

        root.geometry("+960+540")

        tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=5)

        self.username = tk.Entry(root)
        self.password = tk.Entry(root, show="*")
        self.username.grid(row=0, column=1, padx=10, pady=5)
        self.password.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        for acc in self.accounts:
            if acc["username"] == user and acc["password"] == pwd:
                self.root.destroy()
                # open main To-Do window
                import tkinter as tk
                new_root = tk.Tk()
                TodoApp(new_root)
                new_root.mainloop()
                return

        messagebox.showerror("Error", "Invalid username or password.")
