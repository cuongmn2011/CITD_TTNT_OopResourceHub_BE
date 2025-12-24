"""
Script to seed COMPLETE OOP knowledge (Detailed & Advanced)
Run this to populate: Tags -> Category -> Topics -> Sections -> Related Topics
"""

import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Dữ liệu Tags cho OOP
oop_tags = [
    {"name": "OOP Core", "slug": "oop-core", "description": "Cốt lõi hướng đối tượng"},
    {"name": "Class & Object", "slug": "class-object", "description": "Lớp và Đối tượng"},
    {"name": "Methods", "slug": "methods", "description": "Phương thức và tham số"},
    {"name": "Properties", "slug": "properties", "description": "Thuộc tính đối tượng"},
    {"name": "Pillars of OOP", "slug": "oop-pillars", "description": "4 trụ cột OOP"},
    {"name": "Advanced OOP", "slug": "advanced-oop", "description": "OOP nâng cao"},
    {"name": "Design Patterns", "slug": "design-patterns", "description": "Mẫu thiết kế"},
]

# 2. Cấu trúc dữ liệu Kiến thức OOP
oop_data = {
    "category": {"name": "Lập trình hướng đối tượng (OOP)", "slug": "oop"},
    
    "topics": [
        # --- Group 1: Class & Object ---
        {
            "title": "Class & Object",
            "short_definition": "Khuôn mẫu (Class) và Thực thể (Object)",
            "tag_slugs": ["oop-core", "class-object"],
            "sections": [
                {
                    "heading": "Khái niệm",
                    "content": "• **Class**: Là bản thiết kế (blueprint) định nghĩa các thuộc tính và hành vi.\n• **Object**: Là một thực thể cụ thể được tạo ra từ Class đó.",
                    "code_snippet": "class Car:  # Class\n    pass\n\ntoyota = Car()  # Object A\nhonda = Car()   # Object B",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Thuộc tính Class vs Instance",
                    "content": "• **Class Attribute**: Dùng chung cho tất cả objects.\n• **Instance Attribute**: Riêng biệt cho từng object.",
                    "code_snippet": "class Student:\n    school = 'ABC School'  # Class attribute\n    \n    def __init__(self, name):\n        self.name = name  # Instance attribute\n\ns1 = Student('John')\ns2 = Student('Jane')\nprint(Student.school)  # ABC School (shared)",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 2: Constructor & Destructor ---
        {
            "title": "Constructor & Destructor",
            "short_definition": "Khởi tạo và hủy đối tượng",
            "tag_slugs": ["oop-core", "methods"],
            "sections": [
                {
                    "heading": "__init__ (Constructor)",
                    "content": "Phương thức đặc biệt được gọi tự động khi tạo object. Dùng để khởi tạo giá trị ban đầu.",
                    "code_snippet": "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n        print(f'{name} được tạo')\n\np = Person('John', 25)  # Tự động gọi __init__",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "__del__ (Destructor)",
                    "content": "Được gọi khi object bị hủy (garbage collected). Ít dùng trong Python vì có auto garbage collection.",
                    "code_snippet": "class Person:\n    def __del__(self):\n        print(f'{self.name} bị xóa')\n\np = Person('John', 25)\ndel p  # Gọi __del__",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 3: Properties & Methods ---
        {
            "title": "Properties & Methods",
            "short_definition": "Thành phần cấu tạo nên Class: Dữ liệu và Hành vi",
            "tag_slugs": ["properties", "methods"],
            "sections": [
                {
                    "heading": "Properties (Thuộc tính)",
                    "content": "Là các biến được gắn vào Object để lưu trữ trạng thái dữ liệu. Thường được khai báo trong hàm `__init__`.",
                    "code_snippet": "class Student:\n    def __init__(self, name, age):\n        self.name = name  # Property\n        self.age = age    # Property",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Methods (Phương thức)",
                    "content": "Là các hàm được định nghĩa bên trong Class mô tả hành vi của Object.",
                    "code_snippet": "class Student:\n    def study(self):\n        print('Studying...')\n    \n    def greet(self, msg):\n        print(f'{self.name} says: {msg}')",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Parameters & Self",
                    "content": "• **self**: Tham số đầu tiên bắt buộc trong method, đại diện cho instance hiện tại.\n• **Parameters**: Các giá trị truyền vào method để xử lý.",
                    "code_snippet": "s = Student('John', 20)\ns.greet('Hello')  # self tự động = s, msg = 'Hello'",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 4: Static & Class Methods ---
        {
            "title": "Static & Class Methods",
            "short_definition": "Phương thức không phụ thuộc vào instance",
            "tag_slugs": ["methods", "advanced-oop"],
            "sections": [
                {
                    "heading": "@staticmethod",
                    "content": "Method không cần truy cập instance hay class. Hoạt động như function độc lập nhưng nằm trong class namespace.",
                    "code_snippet": "class Math:\n    @staticmethod\n    def add(x, y):\n        return x + y\n\nprint(Math.add(5, 3))  # 8, không cần tạo object",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "@classmethod",
                    "content": "Method nhận class (cls) thay vì instance (self). Thường dùng cho factory methods hoặc thao tác với class attributes.",
                    "code_snippet": "class Student:\n    count = 0\n    \n    @classmethod\n    def increment_count(cls):\n        cls.count += 1\n\nStudent.increment_count()\nprint(Student.count)  # 1",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 5: Encapsulation ---
        {
            "title": "Encapsulation (Đóng gói)",
            "short_definition": "Che giấu dữ liệu và kiểm soát truy cập",
            "tag_slugs": ["oop-pillars"],
            "sections": [
                {
                    "heading": "Private Members",
                    "content": "Sử dụng hai dấu gạch dưới `__` trước tên biến để ngăn truy cập trực tiếp từ bên ngoài (Private).",
                    "code_snippet": "class Account:\n    def __init__(self):\n        self.__balance = 1000  # Private variable\n\n    def get_balance(self):     # Public method\n        return self.__balance\n    \n    def deposit(self, amount):\n        if amount > 0:\n            self.__balance += amount",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Getter & Setter",
                    "content": "Sử dụng method để đọc/ghi dữ liệu private một cách an toàn.",
                    "code_snippet": "acc = Account()\n# print(acc.__balance) -> Lỗi\nprint(acc.get_balance())  # 1000\nacc.deposit(500)\nprint(acc.get_balance())  # 1500",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "@property Decorator",
                    "content": "Cho phép truy cập method như attribute, giúp code clean hơn.",
                    "code_snippet": "class Circle:\n    def __init__(self, radius):\n        self._radius = radius\n    \n    @property\n    def area(self):\n        return 3.14 * self._radius ** 2\n\nc = Circle(5)\nprint(c.area)  # 78.5, gọi như attribute",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 6: Inheritance ---
        {
            "title": "Inheritance (Kế thừa)",
            "short_definition": "Tái sử dụng code từ Class cha",
            "tag_slugs": ["oop-pillars"],
            "sections": [
                {
                    "heading": "Cú pháp Kế thừa",
                    "content": "Class con (Child) thừa hưởng toàn bộ thuộc tính và phương thức của Class cha (Parent). Dùng `super()` để gọi Class cha.",
                    "code_snippet": "class Animal:\n    def __init__(self, name):\n        self.name = name\n    \n    def speak(self):\n        print('Animal sound')\n\nclass Dog(Animal):  # Kế thừa từ Animal\n    def __init__(self, name, breed):\n        super().__init__(name)  # Gọi __init__ của cha\n        self.breed = breed\n    \n    def run(self):\n        print(f'{self.name} is running')",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Method Resolution Order (MRO)",
                    "content": "Thứ tự Python tìm kiếm method trong inheritance hierarchy. Xem bằng `ClassName.__mro__`.",
                    "code_snippet": "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\n\nprint(D.__mro__)\n# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 7: Multiple Inheritance ---
        {
            "title": "Multiple Inheritance",
            "short_definition": "Kế thừa từ nhiều class cha",
            "tag_slugs": ["oop-pillars", "advanced-oop"],
            "sections": [
                {
                    "heading": "Cú pháp",
                    "content": "Python cho phép một class kế thừa từ nhiều class cha. Cẩn thận với Diamond Problem.",
                    "code_snippet": "class Flyer:\n    def fly(self):\n        print('Flying')\n\nclass Swimmer:\n    def swim(self):\n        print('Swimming')\n\nclass Duck(Flyer, Swimmer):  # Multiple inheritance\n    pass\n\nd = Duck()\nd.fly()   # Flying\nd.swim()  # Swimming",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Diamond Problem",
                    "content": "Khi nhiều class cha có cùng method, Python dùng MRO (Method Resolution Order) để quyết định gọi method nào.",
                    "code_snippet": "class A:\n    def method(self):\n        print('A')\n\nclass B(A):\n    def method(self):\n        print('B')\n\nclass C(A):\n    def method(self):\n        print('C')\n\nclass D(B, C):  # B được ưu tiên hơn C\n    pass\n\nd = D()\nd.method()  # Output: B",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 8: Polymorphism ---
        {
            "title": "Polymorphism (Đa hình)",
            "short_definition": "Nhiều hình thái của cùng một hành động",
            "tag_slugs": ["oop-pillars"],
            "sections": [
                {
                    "heading": "Method Overriding",
                    "content": "Class con định nghĩa lại (ghi đè) phương thức của Class cha để thực hiện hành vi riêng biệt.",
                    "code_snippet": "class Animal:\n    def speak(self):\n        print('Animal sound')\n\nclass Dog(Animal):\n    def speak(self):\n        print('Woof')  # Override\n\nclass Cat(Animal):\n    def speak(self):\n        print('Meow')  # Override\n\nanimals = [Dog(), Cat()]\nfor a in animals:\n    a.speak()  # Output khác nhau tùy object",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Duck Typing",
                    "content": "Python không quan tâm kiểu dữ liệu, chỉ cần object có method cần thiết. 'If it walks like a duck...'",
                    "code_snippet": "class Duck:\n    def quack(self):\n        print('Quack!')\n\nclass Person:\n    def quack(self):\n        print('I can quack too!')\n\ndef make_it_quack(thing):\n    thing.quack()  # Không check type\n\nmake_it_quack(Duck())\nmake_it_quack(Person())  # Cũng work!",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 9: Abstraction ---
        {
            "title": "Abstraction (Trừu tượng)",
            "short_definition": "Ẩn chi tiết implementation, chỉ hiển thị interface",
            "tag_slugs": ["oop-pillars", "advanced-oop"],
            "sections": [
                {
                    "heading": "Abstract Base Class (ABC)",
                    "content": "Sử dụng module `abc` để tạo abstract class. Abstract method bắt buộc class con phải implement.",
                    "code_snippet": "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass  # Bắt buộc override\n\nclass Circle(Shape):\n    def __init__(self, radius):\n        self.radius = radius\n    \n    def area(self):  # Phải implement\n        return 3.14 * self.radius ** 2",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Interface vs Implementation",
                    "content": "Abstract class định nghĩa 'What' (interface), class con định nghĩa 'How' (implementation).",
                    "code_snippet": "# s = Shape()  # Error! Cannot instantiate abstract class\nc = Circle(5)\nprint(c.area())  # 78.5",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 10: Special Methods (Magic Methods) ---
        {
            "title": "Special Methods (Magic Methods)",
            "short_definition": "Các method đặc biệt với __name__ để customize behavior",
            "tag_slugs": ["advanced-oop", "methods"],
            "sections": [
                {
                    "heading": "__str__ và __repr__",
                    "content": "• `__str__`: Trả về string dễ đọc cho người dùng (dùng bởi `print()`).\n• `__repr__`: Trả về string mô tả chi tiết cho developer (dùng trong console).",
                    "code_snippet": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    \n    def __str__(self):\n        return f'Point({self.x}, {self.y})'\n    \n    def __repr__(self):\n        return f'Point(x={self.x}, y={self.y})'\n\np = Point(3, 4)\nprint(p)  # Point(3, 4) - calls __str__",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Operator Overloading",
                    "content": "Định nghĩa lại các toán tử (+, -, *, ==, <, ...) cho class của bạn.",
                    "code_snippet": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    \n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n    \n    def __eq__(self, other):\n        return self.x == other.x and self.y == other.y\n\nv1 = Vector(1, 2)\nv2 = Vector(3, 4)\nv3 = v1 + v2  # Gọi __add__\nprint(v3.x, v3.y)  # 4, 6",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "__len__, __getitem__, __iter__",
                    "content": "Làm cho object hoạt động như container (list, dict).",
                    "code_snippet": "class MyList:\n    def __init__(self, items):\n        self.items = items\n    \n    def __len__(self):\n        return len(self.items)\n    \n    def __getitem__(self, index):\n        return self.items[index]\n\nml = MyList([1, 2, 3])\nprint(len(ml))  # 3\nprint(ml[1])    # 2",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 11: Composition vs Inheritance ---
        {
            "title": "Composition vs Inheritance",
            "short_definition": "Chọn 'has-a' hay 'is-a' relationship",
            "tag_slugs": ["advanced-oop", "design-patterns"],
            "sections": [
                {
                    "heading": "Inheritance (Is-a)",
                    "content": "Dùng khi class con **là một loại** của class cha. Ví dụ: Dog **is an** Animal.",
                    "code_snippet": "class Animal:\n    def eat(self):\n        print('Eating')\n\nclass Dog(Animal):  # Dog IS-A Animal\n    def bark(self):\n        print('Woof')",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Composition (Has-a)",
                    "content": "Dùng khi class **có** một object khác làm thành phần. Ví dụ: Car **has an** Engine. Linh hoạt hơn inheritance.",
                    "code_snippet": "class Engine:\n    def start(self):\n        print('Engine started')\n\nclass Car:  # Car HAS-A Engine\n    def __init__(self):\n        self.engine = Engine()  # Composition\n    \n    def drive(self):\n        self.engine.start()\n        print('Car driving')\n\ncar = Car()\ncar.drive()",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Favor Composition over Inheritance",
                    "content": "Design principle: Ưu tiên composition để tránh tight coupling và hierarchy phức tạp.",
                    "code_snippet": "# Bad: Inheritance abuse\nclass FlyingCar(Car, Airplane):  # Multiple inheritance mess\n    pass\n\n# Good: Composition\nclass FlyingCar:\n    def __init__(self):\n        self.car = Car()\n        self.airplane = Airplane()",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 12: Design Patterns Intro ---
        {
            "title": "OOP Design Patterns (Intro)",
            "short_definition": "Các mẫu thiết kế phổ biến trong OOP",
            "tag_slugs": ["design-patterns", "advanced-oop"],
            "sections": [
                {
                    "heading": "Singleton Pattern",
                    "content": "Đảm bảo class chỉ có duy nhất một instance trong suốt chương trình.",
                    "code_snippet": "class Singleton:\n    _instance = None\n    \n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n\ns1 = Singleton()\ns2 = Singleton()\nprint(s1 is s2)  # True, cùng object",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Factory Pattern",
                    "content": "Dùng method để tạo object thay vì gọi constructor trực tiếp. Linh hoạt trong việc chọn class con.",
                    "code_snippet": "class Animal:\n    @staticmethod\n    def create(animal_type):\n        if animal_type == 'dog':\n            return Dog()\n        elif animal_type == 'cat':\n            return Cat()\n\nanimal = Animal.create('dog')  # Factory method\nanimal.speak()  # Woof",
                    "language": "python",
                    "order_index": 2
                }
            ]
        }
    ],
    
    # 3. Related Topics - Liên kết các topics với nhau
    "related_topics": [
        # Core concepts
        {"topic_title": "Class & Object", "related_titles": ["Constructor & Destructor", "Properties & Methods", "Encapsulation (Đóng gói)"]},
        {"topic_title": "Constructor & Destructor", "related_titles": ["Class & Object", "Properties & Methods"]},
        {"topic_title": "Properties & Methods", "related_titles": ["Class & Object", "Static & Class Methods", "Special Methods (Magic Methods)"]},
        
        # Advanced methods
        {"topic_title": "Static & Class Methods", "related_titles": ["Properties & Methods", "OOP Design Patterns (Intro)"]},
        {"topic_title": "Special Methods (Magic Methods)", "related_titles": ["Properties & Methods", "Polymorphism (Đa hình)"]},
        
        # 4 Pillars
        {"topic_title": "Encapsulation (Đóng gói)", "related_titles": ["Class & Object", "Properties & Methods", "Abstraction (Trừu tượng)"]},
        {"topic_title": "Inheritance (Kế thừa)", "related_titles": ["Polymorphism (Đa hình)", "Multiple Inheritance", "Composition vs Inheritance"]},
        {"topic_title": "Polymorphism (Đa hình)", "related_titles": ["Inheritance (Kế thừa)", "Special Methods (Magic Methods)"]},
        {"topic_title": "Abstraction (Trừu tượng)", "related_titles": ["Encapsulation (Đóng gói)", "Inheritance (Kế thừa)"]},
        
        # Advanced topics
        {"topic_title": "Multiple Inheritance", "related_titles": ["Inheritance (Kế thừa)", "Composition vs Inheritance"]},
        {"topic_title": "Composition vs Inheritance", "related_titles": ["Inheritance (Kế thừa)", "Multiple Inheritance", "OOP Design Patterns (Intro)"]},
        {"topic_title": "OOP Design Patterns (Intro)", "related_titles": ["Static & Class Methods", "Composition vs Inheritance"]},
    ]
}

def seed_oop():
    print("🚀 Starting COMPLETE OOP Seed...")
    print("=" * 60)
    
    # 1. Create Tags
    print("\n🏷️  Creating Tags...")
    tag_map = {}
    
    # Get existing tags first
    try:
        existing_tags = requests.get(f"{BASE_URL}/tags/").json()
        for t in existing_tags:
            tag_map[t["slug"]] = t["id"]
    except:
        pass

    for tag in oop_tags:
        if tag["slug"] not in tag_map:
            try:
                res = requests.post(f"{BASE_URL}/tags/", json=tag)
                if res.status_code == 201:
                    tag_map[tag["slug"]] = res.json()["id"]
                    print(f"  ✅ Created tag: {tag['name']}")
                else:
                    print(f"  ⚠️  Tag error {tag['name']}: {res.status_code}")
            except Exception as e:
                print(f"  ❌ Error tag {tag['name']}: {e}")
        else:
            print(f"  ⏭️  Tag exists: {tag['name']}")

    # 2. Create Category
    print("\n📁 Creating Category...")
    cat_id = None
    try:
        res = requests.post(f"{BASE_URL}/categories/", json=oop_data["category"])
        if res.status_code == 201:
            cat_id = res.json()["id"]
            print(f"  ✅ Created category: {oop_data['category']['name']}")
        elif res.status_code == 400:
            cats = requests.get(f"{BASE_URL}/categories/").json()
            for c in cats:
                if c["slug"] == oop_data["category"]["slug"]:
                    cat_id = c["id"]
                    print(f"  ⏭️  Category exists, using ID: {cat_id}")
                    break
    except Exception as e:
        print(f"  ❌ Error category: {e}")
        return

    if not cat_id:
        print("  ❌ Cannot proceed without Category ID")
        return

    # 3. Create Topics & Sections
    print("\n📚 Creating Topics & Sections...")
    topic_id_map = {}
    
    for idx, topic in enumerate(oop_data["topics"], 1):
        try:
            topic_tag_ids = [tag_map[slug] for slug in topic["tag_slugs"] if slug in tag_map]
            
            topic_payload = {
                "title": topic["title"],
                "short_definition": topic["short_definition"],
                "category_id": cat_id,
                "tag_ids": topic_tag_ids
            }

            res_topic = requests.post(f"{BASE_URL}/topics/", json=topic_payload)
            if res_topic.status_code == 201:
                topic_id = res_topic.json()["id"]
                topic_id_map[topic["title"]] = topic_id
                print(f"  ✅ [{idx:2d}/12] Topic: {topic['title']}")
                
                for section in topic["sections"]:
                    section["topic_id"] = topic_id
                    res_sec = requests.post(f"{BASE_URL}/sections/", json=section)
                    if res_sec.status_code != 201:
                        print(f"      ❌ Section failed: {section['heading']}")
            else:
                print(f"  ❌ Failed Topic {topic['title']}: {res_topic.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error processing topic {topic['title']}: {e}")

    # 4. Create Related Topics
    print("\n🔗 Creating Related Topics Links...")
    related_count = 0
    for relation in oop_data["related_topics"]:
        topic_title = relation["topic_title"]
        if topic_title not in topic_id_map:
            print(f"  ⚠️  Topic not found: {topic_title}")
            continue
            
        topic_id = topic_id_map[topic_title]
        
        for related_title in relation["related_titles"]:
            if related_title not in topic_id_map:
                print(f"  ⚠️  Related topic not found: {related_title}")
                continue
                
            related_id = topic_id_map[related_title]
            
            try:
                payload = {"topic_id": topic_id, "related_topic_id": related_id}
                res = requests.post(f"{BASE_URL}/related-topics/", json=payload)
                if res.status_code == 201:
                    related_count += 1
                    print(f"  ✅ {topic_title} ↔️ {related_title}")
                elif res.status_code == 400 and "đã tồn tại" in res.text:
                    print(f"  ⏭️  Link exists: {topic_title} ↔️ {related_title}")
                else:
                    print(f"  ❌ Failed link: {res.status_code}")
            except Exception as e:
                print(f"  ❌ Error creating link: {e}")

    print("\n" + "=" * 60)
    print("✨ COMPLETE OOP Seed Finished!")
    print(f"📊 Summary:")
    print(f"  • Tags: {len(oop_tags)}")
    print(f"  • Category: 1")
    print(f"  • Topics: {len(oop_data['topics'])}")
    print(f"  • Related Links: {related_count}")
    print("=" * 60)

if __name__ == "__main__":
    seed_oop()
