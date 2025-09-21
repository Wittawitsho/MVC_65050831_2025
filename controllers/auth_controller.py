from models.candidates_model import CandidatesModel

# Controller สำหรับจัดการการ login และ authentication
class AuthController:
    def __init__(self, app):
        self.app = app
        self.candidates_model = CandidatesModel()

    # ฟังก์ชัน login
    def login(self, username, password):
        u = self.candidates_model.authenticate(username, password)
        if not u:
            self.app.show_message("Login failed: wrong username/password")
            return
        # แยกการเปิดหน้า home ตาม role
        role = u.get("role")
        self.app.set_user(u)
        if role == "admin":
            self.app.open_admin_home()
        else:
            self.app.open_candidate_home(u.get("candidate_id"))
