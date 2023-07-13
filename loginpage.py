import tkinter as tk
from tkinter import messagebox
import sqlite3

def validate_login():
    username = entry_username.get()
    password = entry_password.get()
    role = selected_role.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if role == "Admin" and username == "admin" and password == "adminpass":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        window.destroy()
        import AdminPage
    else:
        # Retrieve user details from the database
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user is not None:
            messagebox.showinfo("Login Successful", f"Welcome, {user[1]}!")
            window.destroy()
            import UserPage
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

def create_new_user():
    new_user_window = tk.Toplevel(window)
    new_user_window.title("New User Registration")

    frame_new_user = tk.Frame(new_user_window, bg="#FFFFFF", padx=20, pady=20)
    frame_new_user.pack(pady=50)

    label_name = tk.Label(frame_new_user, text="Name:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))
    label_car_number = tk.Label(frame_new_user, text="Car Number:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))
    label_car_color = tk.Label(frame_new_user, text="Car Color:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))
    label_username = tk.Label(frame_new_user, text="Username:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))
    label_password = tk.Label(frame_new_user, text="Password:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))

    entry_name = tk.Entry(frame_new_user, width=20, font=("Arial", 12))
    entry_car_number = tk.Entry(frame_new_user, width=20, font=("Arial", 12))
    entry_car_color = tk.Entry(frame_new_user, width=20, font=("Arial", 12))
    entry_username_new = tk.Entry(frame_new_user, width=20, font=("Arial", 12))
    entry_password_new = tk.Entry(frame_new_user, show="*", width=20, font=("Arial", 12))

    label_name.grid(row=0, column=0, sticky=tk.E, pady=(10, 5))
    label_car_number.grid(row=1, column=0, sticky=tk.E, pady=5)
    label_car_color.grid(row=2, column=0, sticky=tk.E, pady=5)
    label_username.grid(row=3, column=0, sticky=tk.E, pady=5)
    label_password.grid(row=4, column=0, sticky=tk.E, pady=5)
    entry_name.grid(row=0, column=1, pady=(10, 5))
    entry_car_number.grid(row=1, column=1, pady=5)
    entry_car_color.grid(row=2, column=1, pady=5)
    entry_username_new.grid(row=3, column=1, pady=5)
    entry_password_new.grid(row=4, column=1, pady=5)

    def save_new_user():
        name = entry_name.get()
        car_number = entry_car_number.get()
        car_color = entry_car_color.get()
        username = entry_username_new.get()
        password = entry_password_new.get()

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Create the "users" table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            car_number TEXT NOT NULL,
                            car_color TEXT NOT NULL,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL)''')

        cursor.execute("INSERT INTO users (name, car_number, car_color, username, password) VALUES (?, ?, ?, ?, ?)",
                       (name, car_number, car_color, username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("New User Created", "New user has been successfully created!")
        new_user_window.destroy()

    btn_save = tk.Button(frame_new_user, text="Save", command=save_new_user, width=10, bg="#4CAF50", fg="white",
                         font=("Arial", 12))
    btn_save.grid(row=5, column=0, pady=20, columnspan=2, sticky=tk.EW)

def cancel_login():
    window.destroy()

window = tk.Tk()
window.title("Car Parking System Login")
window.configure(bg="#F0F0F0")

frame_login = tk.Frame(window, bg="#FFFFFF", padx=20, pady=20)
frame_login.pack(pady=50)

label_username = tk.Label(frame_login, text="Username:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))
label_password = tk.Label(frame_login, text="Password:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))
label_role = tk.Label(frame_login, text="Role:", bg="#FFFFFF", fg="#333333", font=("Arial", 12))

entry_username = tk.Entry(frame_login, width=20, font=("Arial", 12))
entry_password = tk.Entry(frame_login, show="*", width=20, font=("Arial", 12))

selected_role = tk.StringVar()
selected_role.set("Admin")

option_menu = tk.OptionMenu(frame_login, selected_role, "Admin", "User")

btn_login = tk.Button(frame_login, text="Login", command=validate_login, width=10, bg="#4CAF50", fg="white",
                      font=("Arial", 12))
btn_cancel = tk.Button(frame_login, text="Cancel", command=cancel_login, width=10, bg="#FF0000", fg="white",
                       font=("Arial", 12))
new_user = tk.Button(frame_login, text="New User", command=create_new_user, width=10, bg="#FFFFFF", fg="black",
                       font=("Arial", 12))
label_username.grid(row=0, column=0, sticky=tk.E, pady=(10, 5))
label_password.grid(row=1, column=0, sticky=tk.E, pady=5)
label_role.grid(row=2, column=0, sticky=tk.E, pady=5)
entry_username.grid(row=0, column=1, pady=(10, 5))
entry_password.grid(row=1, column=1, pady=5)
option_menu.grid(row=2, column=1, pady=5)
btn_login.grid(row=3, column=0, pady=20, columnspan=2, sticky=tk.EW)
btn_cancel.grid(row=4, column=0, pady=5, columnspan=2, sticky=tk.EW)
new_user.grid(row=5, column=0, pady=5, columnspan=2, sticky=tk.EW)

window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.mainloop()

