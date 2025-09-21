import json, os

# โมเดลสำหรับจัดการข้อมูลบริษัท
class CompaniesModel:
    def __init__(self, file_path="data/companies.json"):
        self.file_path = file_path
        self.items = []
        self.load()

    # โหลดข้อมูลบริษัทจากไฟล์ JSON
    def load(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.items = json.load(f)
        else:
            self.items = []

    # คืนค่ารายชื่อบริษัททั้งหมด
    def list_all(self):
        return self.items

    # ค้นหาบริษัทโดยใช้ company_id
    def find(self, company_id):
        for c in self.items:
            if c["company_id"] == company_id:
                return c
        return None