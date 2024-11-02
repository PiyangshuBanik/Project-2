import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.master.geometry("800x600")
        self.master.configure(bg="#e0f7fa")  # Light cyan background

        self.tasks = []
        self.load_tasks()

        # Create a title label
        self.title_label = tk.Label(master, text="Piyangshu's Task Manager", bg="#e0f7fa", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # Create a frame for task list
        self.task_frame = tk.Frame(master, bg="#e0f7fa")
        self.task_frame.pack(pady=10)

        # Create a task listbox
        self.task_listbox = tk.Listbox(self.task_frame, selectmode=tk.SINGLE, width=60, height=15, font=("Helvetica", 12))
        self.task_listbox.pack(side=tk.LEFT, padx=10)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Create a frame for buttons
        self.button_frame = tk.Frame(master, bg="#e0f7fa")
        self.button_frame.pack(pady=10)

        # Create buttons
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white", font=("Helvetica", 12))
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.complete_button = tk.Button(self.button_frame, text="Mark as Complete", command=self.mark_task_complete, bg="#FFC107", fg="black", font=("Helvetica", 12))
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear All Tasks", command=self.clear_tasks, bg="#9c27b0", fg="white", font=("Helvetica", 12))
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.load_tasks_to_listbox()

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)

    def load_tasks_to_listbox(self):
        self.task_listbox.delete(0, tk.END)  # Clear the listbox
        for task in self.tasks:
            status = "✓" if task["completed"] else "✗"
            color = "#4CAF50" if task["completed"] else "#F44336"
            self.task_listbox.insert(tk.END, f"[{status}] {task['task']}")
            self.task_listbox.itemconfig(tk.END, {'bg': color})

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter the task:")
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.save_tasks()
            self.load_tasks_to_listbox()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            current_task = self.tasks[selected_index[0]]["task"]
            new_task = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=current_task)
            if new_task:
                self.tasks[selected_index[0]]["task"] = new_task
                self.save_tasks()
                self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Edit Task", "Please select a task to edit.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.save_tasks()
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Delete Task", "Please select a task to delete.")

    def mark_task_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]["completed"] = True
            self.save_tasks()
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Complete Task", "Please select a task to mark as complete.")

    def clear_tasks(self):
        self.tasks = []
        self.save_tasks()
        self.load_tasks_to_listbox()

# Create the main window
root = tk.Tk()
app = TaskManagerApp(root)
root.mainloop()