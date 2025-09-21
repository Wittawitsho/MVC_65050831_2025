from models.candidates_model import CandidatesModel
from models.jobs_model import JobsModel
from models.companies_model import CompaniesModel
from models.applications_model import ApplicationsModel

from views.jobs_view import JobsView
from views.apply_view import ApplyView
from views.candidate_profile_view import CandidateProfileView

# Controller สำหรับจัดการหน้าผู้สมัคร (Candidate)
class CandidateController:
    def __init__(self, app, root):
        self.app = app
        self.root = root
        self.candidates_model = CandidatesModel()
        self.jobs_model = JobsModel()
        self.companies_model = CompaniesModel()
        self.applications_model = ApplicationsModel()

        self.jobs_view = JobsView(root, self, self.jobs_model, self.companies_model, self.applications_model)
        self.apply_view = None
        self.profile_view = CandidateProfileView(root, self, self.candidates_model, self.jobs_model, self.applications_model)

    # แสดงหน้า job list ของ candidate
    def show_jobs(self):
        self.hide_all()
        self.jobs_view.pack(fill="both", expand=True)
        self.jobs_view.load()

    # เปิดหน้าสมัครงาน (ApplyView) สำหรับ job ที่เลือก
    def open_apply(self, job_id):
        self.hide_all()
        candidate = self.app.current_user
        job = self.jobs_model.find(job_id)
        if not job:
            self.app.show_message("Job not found")
            return
        self.apply_view = ApplyView(self.root, self, job, candidate, self.jobs_model)
        self.apply_view.pack(fill="both", expand=True)

    # กลับไปหน้า jobs list
    def back_to_jobs(self):
        self.hide_all()
        self.show_jobs()

    # ตรวจสอบความถูกต้องของ email
    def validate_email(self, email):
        return self.candidates_model.validate_email(email)

    # ตรวจสอบว่าผู้สมัครสมัครงานนี้ไปแล้วหรือยัง
    def is_already_applied(self, candidate_id, job_id):
        return self.applications_model.is_applied(candidate_id, job_id)

    # เพิ่ม application ใหม่
    def submit_application(self, candidate_id, job_id, date_str):
        self.applications_model.add_application(candidate_id, job_id, date_str)

    # แสดง profile ของ candidate
    def show_profile(self, candidate_id):
        self.hide_all()
        self.profile_view.pack(fill="both", expand=True)
        self.profile_view.show_candidate(candidate_id)

    # ซ่อนทุก view ของ candidate
    def hide_all(self):
        try:
            self.jobs_view.pack_forget()
        except: pass
        try:
            self.apply_view.pack_forget()
        except: pass
        try:
            self.profile_view.pack_forget()
        except: pass
        
    # Logout จากระบบ
    def logout(self):
        self.app.logout()