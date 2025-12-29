"""
Script to seed COMPLETE Basic Programming knowledge (Python)
SAFE VERSION: Schema Adjusted & Duplicate Handling
"""

import requests
import sys

# Cấu hình endpoint
BASE_URL = "http://localhost:8000/api/v1"

# 1. Dữ liệu Tags (Python Basics)
basic_tags = [
    {"name": "Python Basics", "slug": "python-basics", "description": "Kiến thức nền tảng Python"},
    {"name": "Syntax", "slug": "syntax", "description": "Cú pháp ngôn ngữ"},
    {"name": "Variables", "slug": "variables", "description": "Biến và lưu trữ dữ liệu"},
    {"name": "Data Types", "slug": "data-types", "description": "Các kiểu dữ liệu cơ sở"},
    {"name": "Collections", "slug": "collections", "description": "Cấu trúc dữ liệu nhóm"},
    {"name": "Control Flow", "slug": "control-flow", "description": "Luồng điều khiển"},
    {"name": "Loops", "slug": "loops", "description": "Vòng lặp"},
    {"name": "Functions", "slug": "functions", "description": "Hàm và tái sử dụng code"},
    {"name": "OOP", "slug": "oop", "description": "Lập trình hướng đối tượng"},
    {"name": "Error Handling", "slug": "error-handling", "description": "Xử lý lỗi"},
    {"name": "File IO", "slug": "file-io", "description": "Đọc ghi file"},
    {"name": "Modules", "slug": "modules", "description": "Module và package"},
]

# 2. Cấu trúc dữ liệu Kiến thức
basics_data = {
    "category": {"name": "Lập trình cơ bản (Python)", "slug": "basics"},
    
    "topics": [
        # --- Group 1: Syntax & Output ---
        {
            "title": "Cú pháp & Output",
            "short_definition": "Quy tắc viết code, in kết quả và chú thích",
            "tag_slugs": ["python-basics", "syntax"],
            "sections": [
                {
                    "heading": "Syntax & Indentation",
                    "content": "Python sử dụng thụt đầu dòng (indentation) để xác định khối lệnh thay vì dấu ngoặc nhọn {}. Đây là quy tắc bắt buộc.",
                    "code_snippet": "if 5 > 2:\n    print('Five is greater than two!') # Correct\nif 5 > 2:\nprint('Error!') # Syntax Error",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Output & Comments",
                    "content": "Sử dụng hàm `print()` để xuất dữ liệu ra màn hình. Comments bắt đầu bằng dấu `#` và không được thực thi.",
                    "code_snippet": "# Đây là comment một dòng\nprint('Hello, World!')\n\n\"\"\"\nĐây là comment\nnhiều dòng\n\"\"\"",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 2: Variables & Data Types ---
        {
            "title": "Biến & Kiểu dữ liệu",
            "short_definition": "Lưu trữ và phân loại dữ liệu (Number, Boolean, Casting)",
            "tag_slugs": ["variables", "data-types"],
            "sections": [
                {
                    "heading": "Variables (Biến)",
                    "content": "Biến là vùng chứa để lưu trữ giá trị dữ liệu. Trong Python, không cần khai báo kiểu dữ liệu tường minh.",
                    "code_snippet": "x = 5       # int\ny = 'John'  # str\nprint(x, y)",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Numbers & Booleans",
                    "content": "• Numbers: `int` (số nguyên), `float` (số thực), `complex`.\n• Booleans: Chỉ có hai giá trị `True` hoặc `False`.",
                    "code_snippet": "x = 10      # int\ny = 3.14    # float\nis_active = True # bool",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Casting (Ép kiểu)",
                    "content": "Chuyển đổi giữa các kiểu dữ liệu sử dụng các hàm constructor: `int()`, `float()`, `str()`.",
                    "code_snippet": "x = int(2.8)    # x = 2\ny = float(1)    # y = 1.0\nz = str(3)      # z = '3'",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 3: Operators ---
        {
            "title": "Toán tử (Operators)",
            "short_definition": "Toán tử số học, so sánh, logic, và assignment",
            "tag_slugs": ["python-basics"],
            "sections": [
                {
                    "heading": "Toán tử số học",
                    "content": "Các phép toán cơ bản: `+`, `-`, `*`, `/`, `//` (chia lấy phần nguyên), `%` (chia lấy dư), `**` (lũy thừa).",
                    "code_snippet": "a = 10\nb = 3\nprint(a + b)  # 13\nprint(a // b) # 3\nprint(a ** b) # 1000",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Toán tử so sánh & logic",
                    "content": "So sánh: `==`, `!=`, `>`, `<`, `>=`, `<=`.\nLogic: `and`, `or`, `not`.",
                    "code_snippet": "x = 5\nprint(x > 3 and x < 10)  # True\nprint(x > 10 or x < 4)   # False\nprint(not(x > 3))        # False",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 4: Strings ---
        {
            "title": "Strings (Chuỗi)",
            "short_definition": "Xử lý văn bản và ký tự",
            "tag_slugs": ["data-types"],
            "sections": [
                {
                    "heading": "Khái niệm String",
                    "content": "Chuỗi trong Python được bao quanh bởi dấu nháy đơn hoặc nháy kép. Chuỗi là mảng các bytes ký tự unicode.",
                    "code_snippet": "a = 'Hello'\nprint(a[1])  # Output: e\nprint(a[2:5]) # llo",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Các phương thức phổ biến",
                    "content": "Python cung cấp nhiều hàm xử lý chuỗi: `strip()` (cắt khoảng trắng), `lower()/upper()`, `replace()`, `split()`.",
                    "code_snippet": "txt = ' Hello World '\nprint(txt.strip())      # 'Hello World'\nprint(txt.replace('H', 'J')) # ' Jello World '\nprint('a,b,c'.split(',')) # ['a', 'b', 'c']",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "String Formatting",
                    "content": "Sử dụng f-strings (Python 3.6+) hoặc `.format()` để định dạng chuỗi.",
                    "code_snippet": "name = 'John'\nage = 36\ntxt = f'My name is {name}, I am {age}'\nprint(txt)",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 5: Lists ---
        {
            "title": "Lists (Danh sách)",
            "short_definition": "Cấu trúc dữ liệu có thứ tự, có thể thay đổi",
            "tag_slugs": ["collections", "data-types"],
            "sections": [
                {
                    "heading": "List Basics",
                    "content": "List là tập hợp có thứ tự và có thể thay đổi (mutable). Cho phép trùng lặp thành phần.",
                    "code_snippet": "fruits = ['apple', 'banana', 'cherry']\nfruits.append('orange')\nprint(fruits[1])  # banana\nprint(len(fruits)) # 4",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "List Methods",
                    "content": "Các phương thức: `append()`, `insert()`, `remove()`, `pop()`, `sort()`, `reverse()`, `clear()`.",
                    "code_snippet": "nums = [3, 1, 4, 1, 5]\nnums.sort()\nprint(nums)  # [1, 1, 3, 4, 5]\nnums.remove(1)\nprint(nums)  # [1, 3, 4, 5]",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "List Comprehension",
                    "content": "Cách ngắn gọn để tạo list mới dựa trên list hiện có.",
                    "code_snippet": "numbers = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in numbers]\nprint(squares)  # [1, 4, 9, 16, 25]\n\neven = [x for x in numbers if x % 2 == 0]\nprint(even)     # [2, 4]",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 6: Tuples & Sets ---
        {
            "title": "Tuples & Sets",
            "short_definition": "Tuple (bất biến), Set (không trùng lặp)",
            "tag_slugs": ["collections", "data-types"],
            "sections": [
                {
                    "heading": "Tuples",
                    "content": "Tuple là tập hợp có thứ tự và KHÔNG thể thay đổi (immutable). Sử dụng dấu ngoặc đơn `()`.",
                    "code_snippet": "fruits = ('apple', 'banana', 'cherry')\nprint(fruits[1])  # banana\n# fruits[1] = 'orange'  # ❌ Error!",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Sets",
                    "content": "Set là tập hợp không có thứ tự, có thể thay đổi, và KHÔNG cho phép trùng lặp. Sử dụng `{}`.",
                    "code_snippet": "fruits = {'apple', 'banana', 'cherry', 'apple'}\nprint(fruits)  # {'apple', 'banana', 'cherry'}\nfruits.add('orange')\nfruits.remove('banana')",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 7: Dictionaries ---
        {
            "title": "Dictionaries (Từ điển)",
            "short_definition": "Cấu trúc key-value, truy cập nhanh",
            "tag_slugs": ["collections", "data-types"],
            "sections": [
                {
                    "heading": "Dictionary Basics",
                    "content": "Dictionary lưu trữ dữ liệu dạng key:value. Có thứ tự (từ Python 3.7+), có thể thay đổi và không cho phép trùng key.",
                    "code_snippet": "car = {\n  'brand': 'Ford',\n  'model': 'Mustang',\n  'year': 1964\n}\nprint(car['model'])  # Mustang\ncar['color'] = 'red'",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Dictionary Methods",
                    "content": "Các phương thức: `get()`, `keys()`, `values()`, `items()`, `pop()`, `update()`.",
                    "code_snippet": "car = {'brand': 'Ford', 'year': 1964}\nprint(car.get('model', 'N/A'))  # N/A\nprint(car.keys())   # dict_keys(['brand', 'year'])\nfor k, v in car.items():\n    print(f'{k}: {v}')",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 8: Conditions ---
        {
            "title": "Câu lệnh điều kiện",
            "short_definition": "If...Else và Match Case",
            "tag_slugs": ["control-flow"],
            "sections": [
                {
                    "heading": "If ... Else",
                    "content": "Hỗ trợ các điều kiện logic toán học. Sử dụng `elif` nếu điều kiện trước đó sai.",
                    "code_snippet": "a = 200\nb = 33\nif b > a:\n  print('b > a')\nelif a == b:\n  print('a == b')\nelse:\n  print('a > b')",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Ternary Operator",
                    "content": "Viết if-else trên một dòng (conditional expression).",
                    "code_snippet": "age = 18\nstatus = 'Adult' if age >= 18 else 'Minor'\nprint(status)  # Adult",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Match Case",
                    "content": "Tương tự Switch Case ở ngôn ngữ khác (có từ Python 3.10). Kiểm tra biến khớp với các pattern.",
                    "code_snippet": "status = 404\nmatch status:\n    case 200:\n        print('OK')\n    case 404:\n        print('Not Found')\n    case _:\n        print('Something else')",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 9: Loops ---
        {
            "title": "Vòng lặp (Loops)",
            "short_definition": "While Loops và For Loops",
            "tag_slugs": ["loops", "control-flow"],
            "sections": [
                {
                    "heading": "While Loop",
                    "content": "Thực thi khối lệnh miễn là điều kiện còn đúng (`True`). Cần cẩn thận với vòng lặp vô hạn.",
                    "code_snippet": "i = 1\nwhile i < 6:\n  print(i)\n  i += 1",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "For Loop",
                    "content": "Dùng để lặp qua một sequence (list, tuple, dict, set, string) hoặc dùng `range()`.",
                    "code_snippet": "fruits = ['apple', 'banana', 'cherry']\nfor x in fruits:\n  if x == 'banana':\n    break\n  print(x)\n\nfor i in range(5):\n    print(i)  # 0 1 2 3 4",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Loop Control (break, continue, pass)",
                    "content": "`break`: Thoát khỏi vòng lặp.\n`continue`: Bỏ qua iteration hiện tại.\n`pass`: Placeholder không làm gì.",
                    "code_snippet": "for i in range(10):\n    if i == 3:\n        continue  # Skip 3\n    if i == 7:\n        break     # Stop at 7\n    print(i)",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 10: Functions ---
        {
            "title": "Functions (Hàm)",
            "short_definition": "Định nghĩa và tái sử dụng khối code",
            "tag_slugs": ["functions", "python-basics"],
            "sections": [
                {
                    "heading": "Định nghĩa Function",
                    "content": "Function được định nghĩa bằng từ khóa `def`. Có thể có parameters và return value.",
                    "code_snippet": "def greet(name):\n    return f'Hello, {name}!'\n\nmessage = greet('Alice')\nprint(message)  # Hello, Alice!",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Default & Keyword Arguments",
                    "content": "Có thể đặt giá trị mặc định cho tham số. Gọi hàm với keyword arguments để rõ ràng.",
                    "code_snippet": "def describe_pet(name, animal='dog'):\n    print(f'I have a {animal} named {name}')\n\ndescribe_pet('Willie')\ndescribe_pet(animal='cat', name='Whiskers')",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "*args và **kwargs",
                    "content": "`*args`: Nhận số lượng tham số tùy ý (tuple).\n`**kwargs`: Nhận keyword arguments tùy ý (dict).",
                    "code_snippet": "def make_pizza(size, *toppings):\n    print(f'{size}-inch pizza with:')\n    for t in toppings:\n        print(f'  - {t}')\n\nmake_pizza(12, 'mushrooms', 'peppers')",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 11: Lambda ---
        {
            "title": "Lambda Functions",
            "short_definition": "Hàm vô danh (anonymous), viết trên 1 dòng",
            "tag_slugs": ["functions"],
            "sections": [
                {
                    "heading": "Lambda Syntax",
                    "content": "Lambda function là hàm nhỏ không tên, có thể có nhiều tham số nhưng chỉ một biểu thức.",
                    "code_snippet": "# Normal function\ndef add(x, y):\n    return x + y\n\n# Lambda equivalent\nadd = lambda x, y: x + y\nprint(add(5, 3))  # 8",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Lambda với map/filter",
                    "content": "Lambda thường được dùng với các hàm bậc cao như `map()`, `filter()`, `sorted()`.",
                    "code_snippet": "nums = [1, 2, 3, 4, 5]\nsquares = list(map(lambda x: x**2, nums))\nprint(squares)  # [1, 4, 9, 16, 25]\n\neven = list(filter(lambda x: x % 2 == 0, nums))\nprint(even)     # [2, 4]",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 12: Classes ---
        {
            "title": "Classes & Objects (OOP cơ bản)",
            "short_definition": "Lập trình hướng đối tượng trong Python",
            "tag_slugs": ["oop", "python-basics"],
            "sections": [
                {
                    "heading": "Class & Object",
                    "content": "Class là blueprint để tạo objects. Object là instance của class.",
                    "code_snippet": "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def greet(self):\n        return f'Hi, I am {self.name}'\n\np1 = Person('John', 36)\nprint(p1.greet())",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Inheritance (Kế thừa)",
                    "content": "Class con có thể kế thừa thuộc tính và phương thức từ class cha.",
                    "code_snippet": "class Student(Person):\n    def __init__(self, name, age, student_id):\n        super().__init__(name, age)\n        self.student_id = student_id\n\ns1 = Student('Alice', 20, 'S123')\nprint(s1.greet())  # Inherited method",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 13: Modules ---
        {
            "title": "Modules & Packages",
            "short_definition": "Tổ chức code thành các file/thư viện riêng",
            "tag_slugs": ["modules", "python-basics"],
            "sections": [
                {
                    "heading": "Import Modules",
                    "content": "Module là file Python chứa code. Sử dụng `import` để tái sử dụng code từ module khác.",
                    "code_snippet": "# Import toàn bộ module\nimport math\nprint(math.sqrt(16))  # 4.0\n\n# Import specific function\nfrom math import pi, sqrt\nprint(pi)  # 3.14159...",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Tạo Module riêng",
                    "content": "Bất kỳ file Python nào cũng có thể là module. Đặt các hàm trong file và import từ file khác.",
                    "code_snippet": "# File: mymodule.py\ndef greeting(name):\n    print(f'Hello, {name}')\n\n# File: main.py\nimport mymodule\nmymodule.greeting('Alice')",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Built-in Modules",
                    "content": "Python có nhiều module tích hợp sẵn: `math`, `random`, `datetime`, `os`, `sys`, `json`.",
                    "code_snippet": "import random\nprint(random.randint(1, 10))\n\nimport datetime\nnow = datetime.datetime.now()\nprint(now.strftime('%Y-%m-%d'))",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 14: File Handling ---
        {
            "title": "File Handling (Đọc/Ghi file)",
            "short_definition": "Làm việc với files trên hệ thống",
            "tag_slugs": ["file-io", "python-basics"],
            "sections": [
                {
                    "heading": "Đọc file",
                    "content": "Sử dụng `open()` với mode `'r'` (read). Nên dùng `with` statement để tự động đóng file.",
                    "code_snippet": "# Read entire file\nwith open('data.txt', 'r') as f:\n    content = f.read()\n    print(content)\n\n# Read line by line\nwith open('data.txt', 'r') as f:\n    for line in f:\n        print(line.strip())",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Ghi file",
                    "content": "Mode `'w'` (write - ghi đè), `'a'` (append - nối thêm), `'x'` (create - tạo mới, lỗi nếu tồn tại).",
                    "code_snippet": "# Write (overwrite)\nwith open('output.txt', 'w') as f:\n    f.write('Hello World\\n')\n    f.write('Python is awesome!')\n\n# Append\nwith open('output.txt', 'a') as f:\n    f.write('\\nNew line appended')",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "File Methods",
                    "content": "Các phương thức: `read()`, `readline()`, `readlines()`, `write()`, `writelines()`, `close()`.",
                    "code_snippet": "with open('data.txt', 'r') as f:\n    # Read first 10 characters\n    print(f.read(10))\n    \n    # Read one line\n    print(f.readline())\n    \n    # Read all lines as list\n    lines = f.readlines()",
                    "language": "python",
                    "order_index": 3
                }
            ]
        },

        # --- Group 15: Error Handling ---
        {
            "title": "Try...Except (Xử lý lỗi)",
            "short_definition": "Bắt và xử lý exceptions/errors",
            "tag_slugs": ["error-handling", "python-basics"],
            "sections": [
                {
                    "heading": "Try...Except",
                    "content": "Sử dụng `try` để chạy code có thể gây lỗi, `except` để xử lý khi có lỗi.",
                    "code_snippet": "try:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')\nexcept Exception as e:\n    print(f'Error: {e}')",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Finally & Else",
                    "content": "`finally`: Luôn chạy dù có lỗi hay không.\n`else`: Chạy nếu KHÔNG có lỗi trong try block.",
                    "code_snippet": "try:\n    f = open('file.txt', 'r')\n    content = f.read()\nexcept FileNotFoundError:\n    print('File not found')\nelse:\n    print('File read successfully')\nfinally:\n    print('Cleanup done')",
                    "language": "python",
                    "order_index": 2
                },
                {
                    "heading": "Raise Exceptions",
                    "content": "Sử dụng `raise` để chủ động ném lỗi.",
                    "code_snippet": "def check_age(age):\n    if age < 0:\n        raise ValueError('Age cannot be negative')\n    return age\n\ntry:\n    check_age(-5)\nexcept ValueError as e:\n    print(e)",
                    "language": "python",
                    "order_index": 3
                }
            ]
        }
    ],
    
    # 3. Related Topics
    "related_topics": [
        {"src": "Biến & Kiểu dữ liệu", "dest": "Strings (Chuỗi)"},
        {"src": "Biến & Kiểu dữ liệu", "dest": "Lists (Danh sách)"},
        {"src": "Biến & Kiểu dữ liệu", "dest": "Tuples & Sets"},
        {"src": "Biến & Kiểu dữ liệu", "dest": "Dictionaries (Từ điển)"},
        {"src": "Biến & Kiểu dữ liệu", "dest": "Toán tử (Operators)"},
        {"src": "Lists (Danh sách)", "dest": "Tuples & Sets"},
        {"src": "Lists (Danh sách)", "dest": "Dictionaries (Từ điển)"},
        {"src": "Lists (Danh sách)", "dest": "Vòng lặp (Loops)"},
        {"src": "Tuples & Sets", "dest": "Lists (Danh sách)"},
        {"src": "Tuples & Sets", "dest": "Dictionaries (Từ điển)"},
        {"src": "Dictionaries (Từ điển)", "dest": "Lists (Danh sách)"},
        {"src": "Dictionaries (Từ điển)", "dest": "Tuples & Sets"},
        {"src": "Câu lệnh điều kiện", "dest": "Toán tử (Operators)"},
        {"src": "Câu lệnh điều kiện", "dest": "Vòng lặp (Loops)"},
        {"src": "Vòng lặp (Loops)", "dest": "Câu lệnh điều kiện"},
        {"src": "Vòng lặp (Loops)", "dest": "Lists (Danh sách)"},
        {"src": "Vòng lặp (Loops)", "dest": "Functions (Hàm)"},
        {"src": "Functions (Hàm)", "dest": "Lambda Functions"},
        {"src": "Functions (Hàm)", "dest": "Modules & Packages"},
        {"src": "Functions (Hàm)", "dest": "Try...Except (Xử lý lỗi)"},
        {"src": "Lambda Functions", "dest": "Functions (Hàm)"},
        {"src": "Lambda Functions", "dest": "Lists (Danh sách)"},
        {"src": "Classes & Objects (OOP cơ bản)", "dest": "Functions (Hàm)"},
        {"src": "Classes & Objects (OOP cơ bản)", "dest": "Modules & Packages"},
        {"src": "File Handling (Đọc/Ghi file)", "dest": "Try...Except (Xử lý lỗi)"},
        {"src": "File Handling (Đọc/Ghi file)", "dest": "Strings (Chuỗi)"},
        {"src": "Try...Except (Xử lý lỗi)", "dest": "Functions (Hàm)"},
        {"src": "Try...Except (Xử lý lỗi)", "dest": "File Handling (Đọc/Ghi file)"},
        {"src": "Modules & Packages", "dest": "Functions (Hàm)"},
        {"src": "Modules & Packages", "dest": "Classes & Objects (OOP cơ bản)"},
        {"src": "Strings (Chuỗi)", "dest": "Biến & Kiểu dữ liệu"},
        {"src": "Strings (Chuỗi)", "dest": "File Handling (Đọc/Ghi file)"},
        {"src": "Toán tử (Operators)", "dest": "Biến & Kiểu dữ liệu"},
        {"src": "Toán tử (Operators)", "dest": "Câu lệnh điều kiện"},
    ]
}

def seed_basics_safe():
    print("🚀 Starting SAFE Basic Programming Seed...")
    print("=" * 60)
    
    # --- 1. Tags (FIX 500 ERROR) ---
    print("\n🏷️  Processing Tags...")
    tag_map = {} # Map: slug -> id
    name_map = {} # Map: name -> id (Check trùng tên)
    
    try:
        existing = requests.get(f"{BASE_URL}/tags/").json()
        for t in existing:
            tag_map[t["slug"]] = t["id"]
            name_map[t["name"]] = t["id"]
    except:
        print("  ⚠️ Cannot fetch existing tags. Assuming empty DB.")

    for tag in basic_tags:
        # Case 1: Exists by Slug -> Reuse
        if tag["slug"] in tag_map:
            print(f"  ⏭️  Tag exists (by slug): {tag['name']}")
        
        # Case 2: Exists by Name (diff slug) -> Reuse to avoid 500
        elif tag["name"] in name_map:
            old_id = name_map[tag["name"]]
            tag_map[tag["slug"]] = old_id 
            print(f"  ⚠️  Tag name '{tag['name']}' exists. Reusing ID: {old_id}")
            
        # Case 3: Create New
        else:
            try:
                res = requests.post(f"{BASE_URL}/tags/", json=tag)
                if res.status_code == 201:
                    new_tag = res.json()
                    tag_map[tag["slug"]] = new_tag["id"]
                    name_map[tag["name"]] = new_tag["id"]
                    print(f"  ✅ Created tag: {tag['name']}")
                else:
                    print(f"  ❌ Failed tag {tag['name']}: {res.status_code}")
            except Exception as e:
                print(f"  ❌ Exception tag: {e}")

    # --- 2. Category ---
    print("\n📁 Processing Category...")
    cat_id = None
    try:
        # Check by slug first
        cats = requests.get(f"{BASE_URL}/categories/").json()
        for c in cats:
            if c["slug"] == basics_data["category"]["slug"]:
                cat_id = c["id"]
                print(f"  ⏭️  Category exists (ID: {cat_id})")
                break
        
        # If not found, create
        if not cat_id:
            res = requests.post(f"{BASE_URL}/categories/", json=basics_data["category"])
            if res.status_code in [200, 201]:
                cat_id = res.json()["id"]
                print(f"  ✅ Category created: {basics_data['category']['name']}")
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
    
    for idx, topic in enumerate(basics_data["topics"], 1):
        try:
            # 3.1 Get Tag IDs
            current_tag_ids = []
            for slug in topic["tag_slugs"]:
                if slug in tag_map:
                    current_tag_ids.append(tag_map[slug])
            
            # 3.2 Create Topic Payload
            topic_payload = {
                "title": topic["title"],
                "short_definition": topic["short_definition"],
                "category_id": cat_id,
                "tag_ids": current_tag_ids,
                "sections": [] # Create sections separately
            }

            res_topic = requests.post(f"{BASE_URL}/topics/", json=topic_payload)
            current_topic_id = None
            
            if res_topic.status_code == 201:
                current_topic_id = res_topic.json()["id"]
                print(f"  ✅ [{idx}] Topic created: {topic['title']}")
            elif res_topic.status_code == 400:
                print(f"  ⏭️  Topic probably exists: {topic['title']}")
                continue 
            else:
                print(f"  ❌ Failed topic: {res_topic.text}")
                continue

            # 3.3 Create Sections (With Fixed Schema)
            topic_id_map[topic["title"]] = current_topic_id
            
            for sec in topic["sections"]:
                # Construct payload matching your Section Schema
                section_payload = {
                    "topic_id": current_topic_id,
                    "heading": sec["heading"],
                    "content": sec["content"],
                    "order_index": sec["order_index"],
                    "code_snippet": sec.get("code_snippet"), # Safe access
                    "language": sec.get("language"),         # Safe access
                    "image_url": None
                }
                
                res_sec = requests.post(f"{BASE_URL}/sections/", json=section_payload)
                if res_sec.status_code != 201:
                    print(f"      ❌ Section failed: {sec['heading']}")
                
        except Exception as e:
            print(f"  ❌ Error loop: {e}")

    # --- 4. Related Topics ---
    print("\n🔗 Linking Related Topics...")
    for item in basics_data["related_topics"]:
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
    
    print("\n✨ SEED BASICS COMPLETED!")

if __name__ == "__main__":
    seed_basics_safe()