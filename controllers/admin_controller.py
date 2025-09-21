from models.candidates_model import CandidatesModel
from models.applications_model import ApplicationsModel
from views.admin_candidates_view import AdminCandidatesView
from views.candidate_profile_view import CandidateProfileView
from models.companies_model import CompaniesModel

# Controller สำหรับจัดการหน้าฝั่ง Admin
class AdminController:
    def __init__(self, app, root):
        self.app = app
        self.root = root
        self.candidates_model = CandidatesModel()
        self.applications_model = ApplicationsModel()
        self.companies_model = CompaniesModel()
        self.view = AdminCandidatesView(root, self, self.candidates_model, self.applications_model)
        self.profile_view = CandidateProfileView(root, self, self.candidates_model, None, self.applications_model)

    # แสดงหน้าผู้สมัครทั้งหมด (admin home)
    def show_candidates(self):
        self.hide_all()
        self.applications_model.load()
        self.view.pack(fill="both", expand=True)
        self.view.load()

    # เปิดหน้ารายละเอียดผู้สมัคร (profile view)
    def open_candidate_profile_admin(self, candidate_id):
        self.hide_all()
        from models.jobs_model import JobsModel
        jobs_model = JobsModel()
        
        self.applications_model.load()
        jobs_model.load()
        self.companies_model.load()
        self.candidates_model.load()
        
        self.profile_view = CandidateProfileView(
            self.root, self, self.candidates_model, jobs_model, self.applications_model
        )
        
        self.profile_view.pack(fill="both", expand=True)
        self.profile_view.show_candidate(candidate_id)

    # ซ่อนทุก view ของ admin
    def hide_all(self):
        try:
            self.view.pack_forget()
        except: pass
        try:
            self.profile_view.pack_forget()
        except: pass

    # กลับไปหน้าผู้สมัครทั้งหมด (ใช้เรียกจาก back button)
    def back_to_main(self):
        self.show_candidates()

    # Logout จากระบบ
    def logout(self):
        self.app.logout()