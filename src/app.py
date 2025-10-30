import tkinter as tk
from tkinter import messagebox
import json, os

from add import AddTaskWindow

TASK_FILE = "src/tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.tasks = load_tasks()

        root.geometry("750x500+585+290")

        # Title
        tk.Label(root, text="My Tasks", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=4, pady=10
        )

        # Scrollable task area
        self.task_frame = tk.Frame(root, bd=2, relief="groove")
        self.task_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

        self.canvas = tk.Canvas(self.task_frame)
        self.scrollbar = tk.Scrollbar(self.task_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Buttons
        tk.Button(root, text="Log out", command=self.log_out).grid(
            row=2, column=0, padx=10, pady=10, sticky="NSEW"
        )
        tk.Button(root, text="Add Task", command=self.open_add_window).grid(
            row=2, column=1, padx=10, pady=10, sticky="NSEW"
        )
        tk.Button(root, text="Delete Done", command=self.delete_done_tasks).grid(
            row=2, column=2, padx=10, pady=10, sticky="NSEW"
        )
        tk.Button(root, text="Doing Something", command=self.doing_something).grid(
            row=2, column=3, padx=10, pady=10, sticky="NSEW"
        )


        # Make grid resizable
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)

        self.refresh_list()

    def refresh_list(self):
        # Clear old tasks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add checkboxes for tasks
        for idx, task in enumerate(self.tasks):
            self.create_task_widget(idx, task)

    def create_task_widget(self, idx, task):
        frame = tk.Frame(self.scrollable_frame, bd=1, relief="solid", padx=5, pady=5)
        frame.pack(fill="both", pady=3)

        # Checkbox and title
        var = tk.BooleanVar(value=task["done"])
        chk = tk.Checkbutton(frame, text=task["title"], variable=var,
                            command=lambda i=idx, v=var: self.toggle_task(i, v))
        chk.pack(anchor="w")

        # Expand/collapse button
        expanded = tk.BooleanVar(value=False)

        def toggle_expand():
            expanded.set(not expanded.get())
            if expanded.get():
                show_details()
            else:
                for w in detail_widgets:
                    w.destroy()

        btn = tk.Button(frame, text="+", width=2, command=toggle_expand)
        btn.pack(side="right", anchor="n")

        # Detail area (lazy render)
        detail_widgets = []

        def show_details():
            # Show description
            lbl = tk.Label(frame, text=f"{task.get('desc','')}", fg="gray")
            lbl.pack(anchor="w", padx=15, pady=2)
            detail_widgets.append(lbl)

            # Subtasks
            subtasks = task.get("subtasks", [])
            for sidx, sub in enumerate(subtasks):
                svar = tk.BooleanVar(value=sub["done"])
                sub_chk = tk.Checkbutton(frame, text=f"- {sub['title']}", variable=svar,
                                        command=lambda s=sidx, v=svar, t=task: self.toggle_subtask(t, s, v))
                sub_chk.pack(anchor="w", padx=30)
                detail_widgets.append(sub_chk)

    def toggle_task(self, index, var):
        self.tasks[index]["done"] = var.get()
        save_tasks(self.tasks)
        

    def toggle_subtask(self, task, sub_idx, var):
        task["subtasks"][sub_idx]["done"] = var.get()
        save_tasks(self.tasks)


    def open_add_window(self):
        AddTaskWindow(self.root, self.add_task)

    def add_task(self, title, desc):
        self.tasks.append({"title": title, "desc": desc, "done": False})
        save_tasks(self.tasks)
        self.refresh_list()

    def delete_done_tasks(self):
        self.tasks = [t for t in self.tasks if not t["done"]]
        save_tasks(self.tasks)
        self.refresh_list()

    def log_out(self):
        self.root.destroy()
        from log_in import LoginWindow
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()

    def doing_something(self):
        print("Is your mom's name Something?")

