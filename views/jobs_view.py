import tkinter as tk
from tkinter import ttk, messagebox

# View สำหรับแสดงรายการงานที่เปิดให้สมัคร
class JobsView(tk.Frame):
    def __init__(self, root, controller, jobs_model, companies_model, applications_model):
        super().__init__(root)
        self.controller = controller
        self.jobs_model = jobs_model
        self.companies_model = companies_model
        self.applications_model = applications_model

        # header section
        header = tk.Frame(self)
        header.pack(fill=tk.X, pady=6)
        tk.Label(header, text="Open Jobs", font=("Arial", 16)).pack(side=tk.LEFT, padx=8)

        # control section: sort, refresh, logout
        ctrl = tk.Frame(self)
        ctrl.pack(fill=tk.X, pady=6)
        tk.Label(ctrl, text="Sort by:").pack(side=tk.LEFT)
        self.sort_var = tk.StringVar(value="title")
        ttk.Combobox(ctrl, textvariable=self.sort_var, values=["title","company","deadline"], state="readonly").pack(side=tk.LEFT, padx=6)
        tk.Button(ctrl, text="Refresh", command=self.load).pack(side=tk.LEFT, padx=6)
        tk.Button(ctrl, text="Logout", command=self.controller.logout).pack(side=tk.RIGHT, padx=6)

        # Treeview แสดงข้อมูล job
        self.tree = ttk.Treeview(self, columns=("job_id","title","company","deadline","applied"), show="headings")
        self.tree.heading("job_id", text="Job ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("company", text="Company")
        self.tree.heading("deadline", text="Deadline")
        self.tree.heading("applied", text="Applied")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double)

        # bottom frame สำหรับปุ่ม Apply Selected
        bottom = tk.Frame(self)
        bottom.pack(fill=tk.X, pady=6)
        tk.Button(bottom, text="Apply Selected", command=self.apply_selected).pack(side=tk.LEFT, padx=8)
        self.load()

    # โหลด jobs และแสดงใน Treeview
    def load(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        jobs = self.jobs_model.list_open()
        sort_by = self.sort_var.get()
        if sort_by == "title":
            jobs.sort(key=lambda j: j["title"])
        elif sort_by == "company":
            jobs.sort(key=lambda j: j["company_id"])
        elif sort_by == "deadline":
            jobs.sort(key=lambda j: j["deadline"])
        for j in jobs:
            comp = self.companies_model.find(j["company_id"])
            comp_name = comp["name"] if comp else j.get("company_id")
            applied_count = len(self.applications_model.list_for_job(j["job_id"]))
            self.tree.insert("", tk.END, values=(j["job_id"], j["title"], comp_name, j["deadline"], applied_count))

    # double-click บน Treeview -> เปิดหน้า apply
    def on_double(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        job_id = self.tree.item(sel[0])["values"][0]
        self.controller.open_apply(job_id)

    # ปุ่ม Apply Selected
    def apply_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Apply", "Select a job to apply")
            return
        job_id = self.tree.item(sel[0])["values"][0]
        self.controller.open_apply(job_id)
