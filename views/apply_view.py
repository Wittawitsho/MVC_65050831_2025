import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# View สำหรับสมัครงาน
# แสดงรายละเอียด job และให้ candidate กรอก email แล้ว submit
class ApplyView(tk.Frame):
    def __init__(self, root, controller, job, candidate, jobs_model):
        super().__init__(root)
        self.controller = controller
        self.job = job
        self.candidate = candidate
        self.jobs_model = jobs_model

        # แสดงหัวข้อ job
        tk.Label(self, text=f"Apply: {job['title']}", font=("Arial", 16)).pack(pady=8)
        info = f"Company ID: {job['company_id']}\nDeadline: {job['deadline']}\nDescription: {job['description']}"
        tk.Label(self, text=info, justify=tk.LEFT).pack(padx=10, anchor="w")

        # form สำหรับกรอก email
        form = tk.Frame(self)
        form.pack(pady=10)
        tk.Label(form, text="Your Email:").grid(row=0, column=0, sticky="e")
        self.email_entry = tk.Entry(form, width=40)
        self.email_entry.grid(row=0, column=1, padx=6)
        self.email_entry.insert(0, candidate.get("email", ""))

        # ปุ่ม submit และ back
        tk.Button(self, text="Submit Application", command=self.submit).pack(pady=8)
        tk.Button(self, text="Back", command=self.controller.back_to_jobs).pack()
    
    # ฟังก์ชัน submit application
    def submit(self):
        email = self.email_entry.get().strip()

        # ตรวจสอบ email
        if not self.controller.validate_email(email):
            messagebox.showerror("Invalid email", "Please enter a valid email")
            return

        # ตรวจสอบ deadline
        today = datetime.today().date().strftime("%Y-%m-%d")
        if self.jobs_model.is_deadline_passed(self.job["job_id"], today):
            messagebox.showerror("Deadline passed", "Cannot apply because the deadline has passed")
            return

        # ตรวจสอบว่าผู้สมัครสมัครแล้วหรือยัง
        if self.controller.is_already_applied(self.candidate["candidate_id"], self.job["job_id"]):
            messagebox.showinfo("Already applied", "You already applied to this job")
            return

        self.controller.submit_application(self.candidate["candidate_id"], self.job["job_id"], today)
        messagebox.showinfo("Success", "Application submitted")
        # กลับไปหน้า jobs
        self.controller.back_to_jobs()
