import tkinter as tk
from tkinter import ttk

# View สำหรับหน้าแอดมินดูรายชื่อผู้สมัคร
# แสดง Candidate ทั้งหมด พร้อมจำนวนใบสมัครของแต่ละคน
class AdminCandidatesView(tk.Frame):
    def __init__(self, root, controller, candidates_model, applications_model):
        super().__init__(root)
        self.controller = controller
        self.candidates_model = candidates_model
        self.applications_model = applications_model

        # header แสดงชื่อหน้าจอ
        header = tk.Frame(self)
        header.pack(fill=tk.X, pady=6)
        tk.Label(header, text="Admin - Candidate List", font=("Arial", 16)).pack(side=tk.LEFT, padx=8)

        # frame สำหรับ search, refresh, logout
        mid = tk.Frame(self)
        mid.pack(fill=tk.X, pady=6)
        tk.Label(mid, text="Search name:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(mid)
        self.search_entry.pack(side=tk.LEFT, padx=6)
        tk.Button(mid, text="Search", command=self.do_search).pack(side=tk.LEFT, padx=6)
        tk.Button(mid, text="Refresh", command=self.load).pack(side=tk.LEFT, padx=6)
        tk.Button(mid, text="Logout", command=self.controller.logout).pack(side=tk.RIGHT, padx=6)

        # Treeview แสดง candidate list
        self.tree = ttk.Treeview(self, columns=("id","name","email","applied_count"), show="headings")
        self.tree.heading("id", text="Candidate ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("applied_count", text="Applied Count")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # double-click ที่ row จะเปิด profile ของ candidate
        self.tree.bind("<Double-1>", self.on_double)

        # โหลดข้อมูล candidate
        self.load()

    # โหลด candidate ทั้งหมด
    def load(self):
        # ลบ row เก่า
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # loop candidate และใส่ข้อมูลลง treeview
        for c in self.candidates_model.list_candidates():
            cid = c.get("candidate_id")
            name = f"{c.get('first_name','')} {c.get('last_name','')}"
            email = c.get("email","")
            applied = len(self.applications_model.list_for_candidate(cid))
            self.tree.insert("", tk.END, values=(cid, name, email, applied))

    # search candidate ตามชื่อ
    def do_search(self):
        q = self.search_entry.get().strip().lower()
        for r in self.tree.get_children():
            self.tree.delete(r)
        for c in self.candidates_model.list_candidates():
            name = f"{c.get('first_name','')} {c.get('last_name','')}".lower()
            if q in name:
                cid = c.get("candidate_id")
                applied = len(self.applications_model.list_for_candidate(cid))
                self.tree.insert("", tk.END, values=(cid, f"{c.get('first_name','')} {c.get('last_name','')}", c.get("email",""), applied))
    
    # double-click เปิด profile candidate
    def on_double(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        cid = self.tree.item(sel[0])["values"][0]
        self.controller.open_candidate_profile_admin(cid)
