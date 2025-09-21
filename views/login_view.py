import tkinter as tk
from tkinter import messagebox

# View สำหรับหน้าจอ Login
class LoginView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller

        tk.Label(self, text="Job Fair System - Login", font=("Arial", 18)).pack(pady=20)

        # Frame สำหรับช่องกรอก username/password
        frm = tk.Frame(self)
        frm.pack(pady=10)

        # Label แสดงข้อความ
        tk.Label(frm, text="Username:").grid(row=0, column=0, sticky="e")
        tk.Label(frm, text="Password:").grid(row=1, column=0, sticky="e")

        # Entry สำหรับกรอก username และ password
        self.user_entry = tk.Entry(frm)
        self.pass_entry = tk.Entry(frm, show="*")
        self.user_entry.grid(row=0, column=1, padx=8, pady=4)
        self.pass_entry.grid(row=1, column=1, padx=8, pady=4)

        # ปุ่ม Login
        tk.Button(self, text="Login", command=self.do_login).pack(pady=10)

    # ฟังก์ชันเรียกเมื่อกดปุ่ม Login
    def do_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Login", "Please enter username and password")
            return
        self.controller.login(username, password)
