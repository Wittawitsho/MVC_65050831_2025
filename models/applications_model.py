import json, os

# โมเดลสำหรับจัดการใบสมัครงาน
class ApplicationsModel:
    def __init__(self, file_path="data/applications.json"):
        self.file_path = file_path
        self.items = []
        self.load()

    # โหลดข้อมูลจากไฟล์ JSON
    def load(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.items = json.load(f)
        else:
            self.items = []

    # บันทึกใบสมัครลงไฟล์ JSON
    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, indent=4, ensure_ascii=False)

    # คืนค่าใบสมัครทั้งหมด
    def list_all(self):
        return self.items

    # คืนค่าใบสมัครของ candidate
    def list_for_candidate(self, candidate_id):
        result = [a for a in self.items if str(a["candidate_id"]) == str(candidate_id)]
        return result

    # คืนค่าใบสมัครของ job
    def list_for_job(self, job_id):
        return [a for a in self.items if a["job_id"] == job_id]

    # ตรวจสอบว่าผู้สมัครสมัครงานนี้แล้วหรือยัง
    def is_applied(self, candidate_id, job_id):
        return any(a for a in self.items if a["candidate_id"] == candidate_id and a["job_id"] == job_id)

    # เพิ่มใบสมัครใหม่
    def add_application(self, candidate_id, job_id, date_str):
        self.items.append({"job_id": job_id, "candidate_id": candidate_id, "applied_at": date_str})
        self.save()

