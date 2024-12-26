import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Listbox, messagebox
import json
import os

root = ttk.Window(themename="superhero") 
root.title("To-Do List")
root.geometry("500x500")
root.position_center()

TASKS_FILE = "tasks.json"

tasks = []

def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                tasks = []
    update_listbox()

def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def update_listbox():
    listbox.delete(0, END)
    for task in tasks:
        status = "✅" if task['completed'] else "❌"
        listbox.insert(END, f"{task['description']} [{status}]")

def add_task():
    task_description = entry.get()
    if task_description:
        tasks.append({"description": task_description, "completed": False})
        entry.delete(0, END)
        update_listbox()
        save_tasks()  
    else:
        messagebox.showwarning("Warning", "Task description cannot be empty.")

def mark_task_complete():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        index = selected_task_index[0]
        tasks[index]['completed'] = True
        update_listbox()
        save_tasks()  
    else:
        messagebox.showwarning("Warning", "No task selected.")

def delete_task():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        index = selected_task_index[0]
        tasks.pop(index)
        update_listbox()
        save_tasks() 
    else:
        messagebox.showwarning("Warning", "No task selected.")

frame = ttk.Frame(root, padding=10)
frame.pack(pady=10)

entry = ttk.Entry(frame, width=30)
entry.pack(side=LEFT, padx=10)

add_button = ttk.Button(frame, text="Add Task", bootstyle=SUCCESS, command=add_task)
add_button.pack(side=LEFT)

listbox = Listbox(root, width=50, height=15)
listbox.pack(pady=10)

buttons_frame = ttk.Frame(root, padding=10)
buttons_frame.pack()

complete_button = ttk.Button(buttons_frame, text="Mark Complete", bootstyle=PRIMARY, command=mark_task_complete)
complete_button.pack(side=LEFT, padx=10)

delete_button = ttk.Button(buttons_frame, text="Delete Task", bootstyle=DANGER, command=delete_task)
delete_button.pack(side=LEFT)

load_tasks()

root.mainloop()