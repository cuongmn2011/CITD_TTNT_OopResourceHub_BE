"""
Script to seed DETAILED OOP knowledge
SAFE VERSION: Checks both Slug & Name to prevent 500 Errors
"""

import requests
import sys

# Cấu hình endpoint
BASE_URL = "http://localhost:8000/api/v1"

# 1. Dữ liệu Tags
oop_tags = [
    {"name": "OOP Core", "slug": "oop-core", "description": "Kiến thức cốt lõi"},
    {"name": "Architecture", "slug": "architecture", "description": "Tư duy thiết kế"},
    {"name": "Python Syntax", "slug": "python-syntax", "description": "Cú pháp Python"},
    {"name": "The 4 Pillars", "slug": "oop-pillars", "description": "4 Trụ cột OOP"},
    {"name": "Best Practices", "slug": "best-practices", "description": "Lời khuyên thực hành"},
]

# 2. Dữ liệu Nội dung OOP
oop_data = {
    "category": {
        "name": "Lập trình hướng đối tượng (OOP)", 
        "slug": "oop"
    },
    
    "topics": [
        # --- TOPIC 1 ---
        {
            "title": "1. Giới thiệu về OOP",
            "short_definition": "OOP là mô hình lập trình dựa trên các 'đối tượng' chứa dữ liệu và mã lệnh.",
            "tag_slugs": ["oop-core", "architecture"],
            "sections": [
                {
                    "heading": "Định nghĩa và Tư duy",
                    "content": "Lập trình Hướng đối tượng (OOP) mô hình hóa các sự vật thực tế thành code.\n\nMỗi đối tượng gồm:\n1. **Thuộc tính (Attributes):** Dữ liệu mô tả (Màu sắc, kích thước).\n2. **Phương thức (Methods):** Hành động thực hiện (Chạy, tính toán).",
                    "order_index": 1
                },
                {
                    "heading": "Ví dụ: Mario & Hộp dụng cụ",
                    "content": "Ví dụ thực tế từ tài liệu:\n- **Mario:** Có thuộc tính (mạng, điểm) và phương thức (nhảy, bắn).\n- **Hộp dụng cụ:** Là đối tượng chứa các công cụ (thuộc tính) và chức năng sửa chữa (phương thức).",
                    "order_index": 2
                },
                {
                    "heading": "Lợi ích của OOP",
                    "content": "1. **Hệ thống hóa:** Tư duy thiết kế mạch lạc.\n2. **Tái sử dụng:** Kế thừa code, tránh lặp lại.\n3. **Đóng gói:** Bảo mật và quản lý dữ liệu tốt hơn.",
                    "order_index": 3
                }
            ]
        },

        # --- TOPIC 2 ---
        {
            "title": "2. Lớp (Class) và Đối tượng (Object)",
            "short_definition": "Phân biệt Bản thiết kế (Class) và Thực thể cụ thể (Object).",
            "tag_slugs": ["oop-core", "python-syntax"],
            "sections": [
                {
                    "heading": "Sự khác biệt cốt lõi",
                    "content": "- **Class (Bản thiết kế):** Khuôn mẫu, chưa chiếm bộ nhớ cụ thể (Ví dụ: Bản vẽ nhà).\n- **Object (Thực thể):** Được tạo ra từ Class, chiếm vùng nhớ riêng (Ví dụ: Ngôi nhà thực tế).",
                    "code_snippet": "class Car:\n    pass\n\n# Tạo 2 object riêng biệt từ 1 class\ntoyota = Car()\nhonda = Car()\n\nprint(toyota is honda) # False",
                    "language": "python",
                    "order_index": 1
                }
            ]
        },

        # --- TOPIC 3 ---
        {
            "title": "3. Cấu trúc của Class",
            "short_definition": "Constructor, Thuộc tính và Phương thức.",
            "tag_slugs": ["python-syntax", "oop-core"],
            "sections": [
                {
                    "heading": "Hàm khởi tạo (__init__)",
                    "content": "Chạy tự động khi tạo đối tượng. Dùng để thiết lập giá trị ban đầu. Tham số `self` là bắt buộc.",
                    "code_snippet": "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n        print(f'{name} created!')\n\np = Person('Nam', 25)",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Instance vs Class Attribute",
                    "content": "- **Instance Attribute:** Riêng biệt cho từng object (gắn với self).\n- **Class Attribute:** Dùng chung cho mọi object.",
                    "code_snippet": "class Student:\n    school = 'BK U' # Class Attr\n    def __init__(self, name):\n        self.name = name # Instance Attr",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- TOPIC 4 ---
        {
            "title": "4.1. Tính Đóng gói (Encapsulation)",
            "short_definition": "Che giấu dữ liệu để bảo vệ tính toàn vẹn.",
            "tag_slugs": ["oop-pillars", "best-practices"],
            "sections": [
                {
                    "heading": "Private Members",
                    "content": "Sử dụng `__` (2 gạch dưới) để tạo biến Private. Không thể truy cập trực tiếp từ bên ngoài.",
                    "code_snippet": "class Account:\n    def __init__(self):\n        self.__balance = 1000 # Private\n\nacc = Account()\n# print(acc.__balance) # Error",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Getter & Setter",
                    "content": "Truy cập dữ liệu thông qua phương thức public để kiểm soát logic.",
                    "code_snippet": "def deposit(self, amount):\n    if amount > 0:\n        self.__balance += amount\n\ndef get_balance(self):\n    return self.__balance",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- TOPIC 5 ---
        {
            "title": "4.2. Tính Kế thừa (Inheritance)",
            "short_definition": "Tái sử dụng mã nguồn từ lớp cha.",
            "tag_slugs": ["oop-pillars"],
            "sections": [
                {
                    "heading": "Cơ chế hoạt động",
                    "content": "Lớp con (Child) hưởng mọi thuộc tính/phương thức của Lớp cha (Parent). Giúp code DRY (Don't Repeat Yourself).",
                    "code_snippet": "class Animal:\n    def speak(self):\n        print('...')\n\nclass Dog(Animal):\n    pass\n\nd = Dog()\nd.speak() # ...",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Override & Extend",
                    "content": "- **Override:** Ghi đè phương thức cũ.\n- **Extend:** Thêm phương thức mới.",
                    "code_snippet": "class Dog(Animal):\n    def speak(self): # Override\n        print('Gâu gâu')\n    \n    def run(self): # Extend\n        print('Running...')",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- TOPIC 6 ---
        {
            "title": "4.3. Tính Đa hình (Polymorphism)",
            "short_definition": "Một hành động, nhiều cách phản hồi.",
            "tag_slugs": ["oop-pillars"],
            "sections": [
                {
                    "heading": "Ví dụ thực tế",
                    "content": "Các đối tượng khác nhau phản hồi cùng một lệnh gọi hàm theo cách riêng.",
                    "code_snippet": "animals = [Dog(), Cat()]\nfor a in animals:\n    a.speak() \n# Output: Gâu gâu / Meo meo",
                    "language": "python",
                    "order_index": 1
                }
            ]
        },

        # --- TOPIC 7 ---
        {
            "title": "4.4. Tính Trừu tượng (Abstraction)",
            "short_definition": "Ẩn chi tiết implementation (How), chỉ hiện interface (What).",
            "tag_slugs": ["oop-pillars", "architecture"],
            "sections": [
                {
                    "heading": "Abstract Base Class",
                    "content": "Sử dụng module `abc`. Định nghĩa 'hợp đồng' bắt buộc lớp con phải tuân thủ.",
                    "code_snippet": "from abc import ABC, abstractmethod\n\nclass Vehicle(ABC):\n    @abstractmethod\n    def brake(self):\n        pass\n\nclass Car(Vehicle):\n    def brake(self):\n        print('Stop')",
                    "language": "python",
                    "order_index": 1
                }
            ]
        }
    ],
    
    # 3. Related Topics
    "related_topics": [
        {"src": "1. Giới thiệu về OOP", "dest": "2. Lớp (Class) và Đối tượng (Object)"},
        {"src": "2. Lớp (Class) và Đối tượng (Object)", "dest": "3. Cấu trúc của Class"},
        {"src": "3. Cấu trúc của Class", "dest": "4.1. Tính Đóng gói (Encapsulation)"},
        {"src": "3. Cấu trúc của Class", "dest": "4.2. Tính Kế thừa (Inheritance)"},
        {"src": "4.2. Tính Kế thừa (Inheritance)", "dest": "4.3. Tính Đa hình (Polymorphism)"},
        {"src": "4.2. Tính Kế thừa (Inheritance)", "dest": "4.4. Tính Trừu tượng (Abstraction)"},
    ]
}

def seed_oop_safe():
    print("🚀 Starting SAFE OOP Seed...")
    print("=" * 60)
    
    # --- 1. Tags (FIX 500 ERROR) ---
    print("\n🏷️  Processing Tags...")
    tag_map = {} # Map: slug -> id
    name_map = {} # Map: name -> id (Để check trùng tên)
    
    # 1.1 Lấy dữ liệu cũ
    try:
        existing = requests.get(f"{BASE_URL}/tags/").json()
        for t in existing:
            tag_map[t["slug"]] = t["id"]
            name_map[t["name"]] = t["id"]
    except:
        print("  ⚠️ Cannot fetch existing tags. Assuming empty DB.")

    # 1.2 Tạo mới hoặc Reuse
    for tag in oop_tags:
        # Case 1: Đã tồn tại Slug -> Reuse
        if tag["slug"] in tag_map:
            print(f"  ⏭️  Tag exists (by slug): {tag['name']}")
        
        # Case 2: Đã tồn tại Name (nhưng khác Slug) -> Reuse để tránh 500 Error
        elif tag["name"] in name_map:
            old_id = name_map[tag["name"]]
            # Cập nhật vào tag_map để các topic bên dưới dùng được
            tag_map[tag["slug"]] = old_id 
            print(f"  ⚠️  Tag name '{tag['name']}' exists with different slug. Reusing ID: {old_id}")
            
        # Case 3: Chưa có -> Tạo mới
        else:
            try:
                res = requests.post(f"{BASE_URL}/tags/", json=tag)
                if res.status_code == 201:
                    new_tag = res.json()
                    tag_map[tag["slug"]] = new_tag["id"]
                    name_map[tag["name"]] = new_tag["id"]
                    print(f"  ✅ Created tag: {tag['name']}")
                else:
                    print(f"  ❌ Failed tag {tag['name']}: {res.status_code} - {res.text}")
            except Exception as e:
                print(f"  ❌ Exception tag: {e}")

    # --- 2. Category ---
    print("\n📁 Processing Category...")
    cat_id = None
    try:
        # Check slug trước
        cats = requests.get(f"{BASE_URL}/categories/").json()
        for c in cats:
            if c["slug"] == oop_data["category"]["slug"]:
                cat_id = c["id"]
                print(f"  ⏭️  Category exists (ID: {cat_id})")
                break
        
        if not cat_id:
            res = requests.post(f"{BASE_URL}/categories/", json=oop_data["category"])
            if res.status_code in [200, 201]:
                cat_id = res.json()["id"]
                print(f"  ✅ Category created: {oop_data['category']['name']}")
            else:
                print(f"  ❌ Error category: {res.text}")
                return
    except Exception as e:
        print(f"  ❌ Exception category: {e}")
        return

    if not cat_id:
        print("  ⛔ Cannot proceed without Category ID")
        return

    # --- 3. Topics & Sections ---
    print("\n📚 Processing Topics & Sections...")
    topic_id_map = {} # Map: Title -> ID
    
    for idx, topic in enumerate(oop_data["topics"], 1):
        try:
            # 3.1 Get Tag IDs (An toàn)
            current_tag_ids = []
            for slug in topic["tag_slugs"]:
                if slug in tag_map:
                    current_tag_ids.append(tag_map[slug])
            
            # 3.2 Create Topic
            topic_payload = {
                "title": topic["title"],
                "short_definition": topic["short_definition"],
                "category_id": cat_id,
                "tag_ids": current_tag_ids,
                "sections": [] # Tạo section sau
            }

            # Check duplicate title logic (Optional but good)
            # Ở đây mình cứ POST, nếu 400 thì thôi
            res_topic = requests.post(f"{BASE_URL}/topics/", json=topic_payload)
            current_topic_id = None
            
            if res_topic.status_code == 201:
                current_topic_id = res_topic.json()["id"]
                print(f"  ✅ [{idx}] Topic created: {topic['title']}")
            elif res_topic.status_code == 400:
                print(f"  ⏭️  Topic probably exists: {topic['title']}")
                # Nếu muốn update sections cho topic cũ, cần tìm ID của nó
                # (Logic tìm ID topic cũ phức tạp hơn chút, tạm skip để script gọn)
                continue 
            else:
                print(f"  ❌ Failed topic: {res_topic.text}")
                continue

            # 3.3 Create Sections
            topic_id_map[topic["title"]] = current_topic_id
            
            for sec in topic["sections"]:
                section_payload = {
                    "topic_id": current_topic_id,
                    "heading": sec["heading"],
                    "content": sec["content"],
                    "order_index": sec["order_index"],
                    "code_snippet": sec.get("code_snippet"),
                    "language": sec.get("language"),
                    "image_url": None
                }
                
                res_sec = requests.post(f"{BASE_URL}/sections/", json=section_payload)
                if res_sec.status_code != 201:
                    print(f"      ❌ Section failed: {sec['heading']}")
                
        except Exception as e:
            print(f"  ❌ Error loop: {e}")

    # --- 4. Related Topics ---
    print("\n🔗 Linking Related Topics...")
    for item in oop_data["related_topics"]:
        src = item["src"]
        dest = item["dest"]
        
        if src in topic_id_map and dest in topic_id_map:
            s_id = topic_id_map[src]
            d_id = topic_id_map[dest]
            
            try:
                requests.post(f"{BASE_URL}/related-topics/", 
                            json={"topic_id": s_id, "related_topic_id": d_id})
            except:
                pass
    
    print("\n✨ SEED COMPLETED!")

if __name__ == "__main__":
    seed_oop_safe()