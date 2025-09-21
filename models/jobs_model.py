import json, os
from datetime import datetime

# โมเดลสำหรับจัดการข้อมูลตำแหน่งงาน
class JobsModel:
    def __init__(self, file_path="data/jobs.json"):
        self.file_path = file_path
        self.jobs = []
        self.load()

    # โหลดข้อมูลงานจากไฟล์ JSON
    def load(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.jobs = json.load(f)
        else:
            self.jobs = []

    # บันทึกข้อมูลงานลงไฟล์ JSON
    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.jobs, f, indent=4, ensure_ascii=False)

    # คืนค่ารายการงานทั้งหมด
    def list_all(self):
        return self.jobs

    # คืนค่ารายการงานที่เปิดรับสมัคร (status = "open")
    def list_open(self):
        return [j for j in self.jobs if j.get("status","").lower() == "open"]

    # ค้นหางานโดยใช้ job_id
    def find(self, job_id):
        job_id = str(job_id)
        for j in self.jobs:
            if str(j["job_id"]) == job_id:
                return j
        return None

    # ตรวจสอบว่า deadline ของงานผ่านหรือไม่
    def is_deadline_passed(self, job_id, date_str):
        job = self.find(job_id)
        if not job:
            return True
        deadline = datetime.strptime(job["deadline"], "%Y-%m-%d").date()
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return d > deadline