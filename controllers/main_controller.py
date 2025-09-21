import tkinter as tk
from views.login_view import LoginView
from controllers.auth_controller import AuthController
from controllers.admin_controller import AdminController
from controllers.candidate_controller import CandidateController

# Controller หลักของระบบ
# จัดการการแสดงผล view ทั้งหมด และส่งต่อคำสั่งไปยัง sub-controllers
class MainController:
    def __init__(self, root):
        self.root = root
        self.current_user = None

        # สร้าง view และ controllers ย่อย
        self.login_view = LoginView(root, self)
        self.auth_ctrl = AuthController(self)
        self.admin_ctrl = AdminController(self, root)
        self.candidate_ctrl = CandidateController(self, root)

    # เริ่มต้นแอป: แสดงหน้า login
    def start(self):
        self.hide_all()
        self.login_view.pack(fill="both", expand=True)

    # ซ่อนทุก view ก่อนเปลี่ยนหน้า
    def hide_all(self):
        try: self.login_view.pack_forget()
        except: pass
        try: self.admin_ctrl.hide_all()
        except: pass
        try: self.candidate_ctrl.hide_all()
        except: pass

    # เรียก AuthController ทำการ login
    def login(self, username, password):
        self.auth_ctrl.login(username, password)

    # ตั้งค่าผู้ใช้ปัจจุบันหลัง login สำเร็จ
    def set_user(self, user_dict):
        self.current_user = user_dict

    # เปิดหน้า admin home (candidate list)
    def open_admin_home(self):
        self.hide_all()
        self.admin_ctrl.show_candidates()

    # เปิดหน้า candidate home (jobs list)
    def open_candidate_home(self, candidate_id):
        self.hide_all()
        self.candidate_ctrl.show_jobs()

    # เปิดหน้า profile ของ candidate ในฝั่ง admin
    def open_candidate_profile_admin(self, cid):
        self.hide_all()
        self.admin_ctrl.open_candidate_profile_admin(cid)

    # เปิดหน้า apply job สำหรับ candidate
    def open_apply(self, job_id):
        self.candidate_ctrl.open_apply(job_id)

    # กลับไปหน้า jobs list ของ candidate
    def back_to_jobs(self):
        self.candidate_ctrl.back_to_jobs()

    # ตรวจสอบ email ผ่าน candidate controller
    def validate_email(self, email):
        return self.candidate_ctrl.validate_email(email)

    # ตรวจสอบว่าผู้สมัครสมัคร job นี้แล้วหรือยัง
    def is_already_applied(self, candidate_id, job_id):
        return self.candidate_ctrl.is_already_applied(candidate_id, job_id)

    # ส่งข้อมูลสมัครงานไปที่ candidate controller
    def submit_application(self, candidate_id, job_id, date_str):
        self.candidate_ctrl.submit_application(candidate_id, job_id, date_str)

    # ทำ logout และกลับไปหน้า login
    def logout(self):
        self.current_user = None
        self.hide_all()
        self.login_view = LoginView(self.root, self)
        self.login_view.pack(fill="both", expand=True)

    # แสดง message popup
    def show_message(self, msg):
        tk.messagebox.showinfo("Info", msg)
