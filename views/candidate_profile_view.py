import tkinter as tk
from tkinter import ttk

# View สำหรับแสดงรายละเอียดผู้สมัคร
# แสดงข้อมูลส่วนตัว และรายการงานที่สมัครไปแล้ว
class CandidateProfileView(tk.Frame):
    def __init__(self, root, controller, candidates_model, jobs_model, applications_model):
        super().__init__(root)
        self.controller = controller
        self.candidates_model = candidates_model
        self.jobs_model = jobs_model
        self.applications_model = applications_model

        # header แสดงชื่อผู้สมัคร
        self.header = tk.Label(self, text="", font=("Arial", 16))
        self.header.pack(pady=6)

        # frame แสดงข้อมูลผู้สมัคร
        info_f = tk.Frame(self)
        info_f.pack(fill=tk.X, padx=10)
        self.info_label = tk.Label(info_f, text="", justify=tk.LEFT)
        self.info_label.pack(anchor="w")

        # label สำหรับส่วน applied jobs
        tk.Label(self, text="Applied Jobs:", font=("Arial", 12)).pack(pady=6)

        # Treeview แสดงงานที่สมัคร
        self.tree = ttk.Treeview(self, columns=("job_id","title","company","applied_at"), show="headings")
        self.tree.heading("job_id", text="Job ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("company", text="Company")
        self.tree.heading("applied_at", text="Applied At")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        # ปุ่ม Back
        btnf = tk.Frame(self)
        btnf.pack(fill=tk.X, pady=8)
        
        # ตรวจสอบว่าควรเรียก back function ไหน ขึ้นกับ controller
        if hasattr(self.controller, "back_to_jobs"):
            back_cmd = self.controller.back_to_jobs
        else:
            back_cmd = self.controller.back_to_main

        tk.Button(btnf, text="Back", command=back_cmd).pack(side=tk.LEFT, padx=8)
    
    # แสดงรายละเอียดผู้สมัคร และงานที่สมัครแล้ว
    def show_candidate(self, candidate_id):
        c = self.candidates_model.find_by_candidate_id(candidate_id)
        if not c:
            return
        
        # แสดงชื่อและข้อมูลผู้สมัคร
        name = f"{c.get('first_name','')} {c.get('last_name','')}"
        self.header.config(text=f"Profile - {name}")
        info = f"ID: {c.get('candidate_id')}\nEmail: {c.get('email','')}"
        self.info_label.config(text=info)
        
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        self.applications_model.load()
        apps = self.applications_model.list_for_candidate(candidate_id)
        
        for a in apps:
            job_id = a["job_id"]
            applied_at = a["applied_at"]
            # ถ้ามี jobs_model จะดึงชื่อ job และ company
            if self.jobs_model:
                self.jobs_model.load()
                job = self.jobs_model.find(job_id)
                title = job.get("title") if job else f"Job {job_id}"
                
                if job and hasattr(self.controller, 'companies_model'):
                    self.controller.companies_model.load()
                    company = self.controller.companies_model.find(job.get("company_id"))
                    comp_name = company.get("name") if company else job.get("company_id", "Unknown Company")
                elif job:
                    comp_name = job.get("company_id", "Unknown Company")
                else:
                    comp_name = "Unknown Company"
            else:
                title = f"Job {job_id}"
                comp_name = "Unknown Company"
            # แทรกข้อมูลลง Treeview
            self.tree.insert("", tk.END, values=(job_id, title, comp_name, applied_at))