import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

def calculate_expression(expression):
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except Exception as e:
        messagebox.showerror("Ошибка", f"Невозможно вычислить выражение:\n{e}")
        return "Ошибка"

def update_display(text):
    current_text = display.get()
    display.delete(0, tk.END)
    display.insert(tk.END, current_text + text)

def delete_last():
    current_text = display.get()
    display.delete(0, tk.END)
    display.insert(tk.END, current_text[:-1])

def calculate_result():
    expression = display.get()
    result = calculate_expression(expression)
    display.delete(0, tk.END)
    display.insert(tk.END, result)
    add_to_history(f"{expression} = {result}")

def add_to_history(entry):
    history.insert(tk.END, entry + "\n")
    history.yview(tk.END)
    save_history_to_file()

def clear_history():
    history.delete(1.0, tk.END)
    save_history_to_file()

def clear_display():
    display.delete(0, tk.END)

def handle_key(event):
    key = event.char
    if key.isdigit() or key in "+()-*/":
        update_display(key)
    elif key == "\r":  # Enter key
        calculate_result()
    elif key == "\x08":  # Backspace key
        delete_last()

def toggle_history():
    if history_frame.winfo_ismapped():
        history_frame.grid_forget()
    else:
        history_frame.grid(row=2, column=0, columnspan=4, padx=20, pady=5, sticky="nsew")

def save_history_to_file():
    history_content = history.get(1.0, tk.END)
    with open("history.txt", "w") as f:
        f.write(history_content)

def load_history_from_file():
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as f:
            return f.read()
    return ""

root = tk.Tk()
root.title("Калькулятор")
root.geometry("400x600")
root.configure(bg="#f5f5f5")

display = tk.Entry(root, font=("Arial", 24), bd=8, relief="sunken", justify="right", bg="#ffffff", fg="#333", borderwidth=2, highlightbackground="#ccc", highlightthickness=1)
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=20, pady=20)

history_button = tk.Button(root, text="История", font=("Arial", 12), bg="#4CAF50", fg="#fff", relief="flat", bd=4, command=toggle_history, activebackground="#45a049", activeforeground="#fff")
history_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

clear_history_button = tk.Button(root, text="Очистить историю", font=("Arial", 12), bg="#FF5722", fg="#fff", relief="flat", bd=4, command=clear_history, activebackground="#e64a19", activeforeground="#fff")
clear_history_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="nsew")

history_frame = tk.Frame(root)
history = scrolledtext.ScrolledText(history_frame, font=("Arial", 12), width=30, height=8, wrap=tk.WORD, bd=4, relief="flat", bg="#f0f0f0", fg="#333")
history.grid(row=0, column=0, padx=20, pady=5)

buttons = [
    ('AC', 2, 0), ('DEL', 2, 1), ('(', 2, 2), (')', 2, 3),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
    ('0', 6, 0), ('=', 6, 1), ('-', 6, 2)
]

def create_button(root, text, row, col, command=None):
    button = tk.Button(root, text=text, font=("Arial", 18), height=2, width=5, command=command,
                       bg="#f5f5f5", fg="#333", relief="flat", bd=4, activebackground="#e0e0e0", activeforeground="#000", highlightbackground="#ccc", highlightthickness=1)
    button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)

for (text, row, col) in buttons:
    if text == "=":
        create_button(root, text, row, col, calculate_result)
    elif text == "AC":
        create_button(root, text, row, col, clear_display)
    elif text == "DEL":
        create_button(root, text, row, col, delete_last)
    else:
        create_button(root, text, row, col, lambda t=text: update_display(t))

for i in range(9):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

history_content = load_history_from_file()
history.insert(tk.END, history_content)

root.bind("<Key>", handle_key)

root.mainloop()
