import json, os
import re

# Regular expression สำหรับตรวจสอบความถูกต้องของอีเมล
EMAIL_RE = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

# โมเดลสำหรับจัดการข้อมูลผู้สมัครและแอดมิน
class CandidatesModel:
    def __init__(self, file_path="data/candidates.json"):
        self.file_path = file_path
        self.users = []
        self.load()

    # โหลดข้อมูลจากไฟล์ JSON ถ้าไฟล์ไม่มีหรือว่าง ให้ users เป็น list ว่าง
    def load(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        else:
            self.users = []
    
    # คืนค่ารายชื่อผู้สมัครทั้งหมด (role="candidate") ไม่รวม admin
    def list_candidates(self):
        candidates = [users for users in self.users if users.get("role") == "candidate"]
        return candidates

    # ค้นหาผู้สมัครโดยใช้ candidate_id
    def find_by_candidate_id(self, cid):
        for users in self.users:
            if users.get("role") == "candidate" and str(users.get("candidate_id")) == str(cid):
                return users
        return None
    
    # ตรวจสอบ username และ password สำหรับ login
    def authenticate(self, username, password):
        for users in self.users:
            if users.get("username") == username and users.get("password") == password:
                return users
        return None

    # ตรวจสอบรูปแบบของอีเมล ใช้ regex
    def validate_email(self, email):
        return bool(EMAIL_RE.match(email))