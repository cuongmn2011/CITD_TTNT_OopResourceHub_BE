"""
Script to seed DATA STRUCTURES & ALGORITHMS (DSA)
SAFE VERSION: Schema Adjusted & Duplicate Handling
"""

import requests
import sys

# Cấu hình endpoint
BASE_URL = "http://localhost:8000/api/v1"

# 1. Dữ liệu Tags (DSA)
dsa_tags = [
    {"name": "DSA Core", "slug": "dsa-core", "description": "Kiến thức cốt lõi về CTDL & GT"},
    {"name": "Big O", "slug": "complexity", "description": "Độ phức tạp thuật toán"},
    {"name": "Linear Structures", "slug": "linear-structures", "description": "Cấu trúc tuyến tính (List, Stack, Queue)"},
    {"name": "Non-linear Structures", "slug": "non-linear-structures", "description": "Cấu trúc phi tuyến (Tree, Graph)"},
    {"name": "Trees", "slug": "trees", "description": "Cây và các biến thể"},
    {"name": "Graphs", "slug": "graphs", "description": "Đồ thị và thuật toán tìm kiếm"},
    {"name": "Hashing", "slug": "hashing", "description": "Bảng băm và hàm băm"},
    {"name": "Sorting", "slug": "sorting", "description": "Các thuật toán sắp xếp"},
    {"name": "Searching", "slug": "searching", "description": "Các thuật toán tìm kiếm"},
]

# 2. Cấu trúc dữ liệu Kiến thức
dsa_data = {
    "category": {"name": "Cấu trúc dữ liệu & Giải thuật", "slug": "dsa"},
    
    "topics": [
        # --- Group 1: Complexity ---
        {
            "title": "1. Độ phức tạp & Big O",
            "short_definition": "Đánh giá hiệu năng thuật toán (Thời gian & Bộ nhớ)",
            "tag_slugs": ["dsa-core", "complexity"],
            "sections": [
                {
                    "heading": "Big O Notation",
                    "content": "Big O mô tả giới hạn trên của thời gian chạy khi dữ liệu đầu vào (n) tăng lên. Các độ phức tạp phổ biến:\n- O(1): Hằng số (Truy cập index).\n- O(n): Tuyến tính (Vòng lặp).\n- O(log n): Logarit (Binary Search).\n- O(n^2): Bình phương (Nested loops).",
                    "code_snippet": "# O(n) - Linear Time\ndef print_items(n):\n    for i in range(n):\n        print(i)\n\n# O(n^2) - Quadratic Time\ndef print_pairs(n):\n    for i in range(n):\n        for j in range(n):\n            print(i, j)",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Time vs Space Complexity",
                    "content": "- **Time Complexity:** Thời gian chạy tăng thế nào theo input.\n- **Space Complexity:** Bộ nhớ tiêu tốn thêm tăng thế nào theo input.",
                    "order_index": 2
                }
            ]
        },

        # --- Group 2: Linked Lists ---
        {
            "title": "2. Danh sách liên kết (Linked Lists)",
            "short_definition": "Chuỗi các node liên kết với nhau qua con trỏ",
            "tag_slugs": ["linear-structures", "dsa-core"],
            "sections": [
                {
                    "heading": "Singly Linked List",
                    "content": "Mỗi node chứa giá trị (data) và con trỏ (next) trỏ đến node tiếp theo. Khác với Array, các node không nằm liền kề trong bộ nhớ.",
                    "code_snippet": "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None\n\nclass LinkedList:\n    def __init__(self, value):\n        new_node = Node(value)\n        self.head = new_node\n        self.tail = new_node\n        self.length = 1",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Ưu & Nhược điểm",
                    "content": "- **Ưu:** Thêm/Xóa ở đầu list cực nhanh O(1). Kích thước động.\n- **Nhược:** Truy cập phần tử chậm O(n) (phải duyệt từ đầu).",
                    "order_index": 2
                }
            ]
        },

        # --- Group 3: Stacks & Queues ---
        {
            "title": "3. Stack & Queue",
            "short_definition": "LIFO (Ngăn xếp) và FIFO (Hàng đợi)",
            "tag_slugs": ["linear-structures", "stack-queue"],
            "sections": [
                {
                    "heading": "Stack (Ngăn xếp)",
                    "content": "Hoạt động theo nguyên tắc **LIFO** (Last In, First Out) - Vào sau ra trước. Ứng dụng: Undo, Call stack, Duyệt DFS.",
                    "code_snippet": "stack = []\nstack.append(1) # Push\nstack.append(2)\nprint(stack.pop()) # Pop -> 2\nprint(stack.pop()) # Pop -> 1",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Queue (Hàng đợi)",
                    "content": "Hoạt động theo nguyên tắc **FIFO** (First In, First Out) - Vào trước ra trước. Ứng dụng: Xử lý task, Máy in, Duyệt BFS.",
                    "code_snippet": "from collections import deque\nqueue = deque([])\nqueue.append(1) # Enqueue\nqueue.append(2)\nprint(queue.popleft()) # Dequeue -> 1",
                    "language": "python",
                    "order_index": 2
                }
            ]
        },

        # --- Group 4: Hash Tables ---
        {
            "title": "4. Hash Tables (Bảng băm)",
            "short_definition": "Cấu trúc Key-Value với tốc độ truy cập O(1)",
            "tag_slugs": ["hashing", "dsa-core"],
            "sections": [
                {
                    "heading": "Cơ chế hoạt động",
                    "content": "Sử dụng hàm băm (hash function) để biến đổi Key thành chỉ số (index) trong bộ nhớ. Cho phép tìm kiếm, thêm, xóa trung bình đạt O(1).",
                    "code_snippet": "my_dict = {'name': 'Cuong', 'age': 25}\n\n# Truy cập O(1)\nprint(my_dict['name'])\n\n# Kiểm tra tồn tại O(1)\nif 'age' in my_dict:\n    print('Found')",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Xử lý va chạm (Collision)",
                    "content": "Khi 2 key khác nhau ra cùng 1 index.\n- **Linear Probing:** Tìm ô trống tiếp theo.\n- **Chaining:** Mỗi ô chứa một Linked List các phần tử trùng index.",
                    "order_index": 2
                }
            ]
        },

        # --- Group 5: Trees ---
        {
            "title": "5. Trees & BST",
            "short_definition": "Cấu trúc phân cấp: Cây nhị phân tìm kiếm",
            "tag_slugs": ["non-linear-structures", "trees"],
            "sections": [
                {
                    "heading": "Binary Search Tree (BST)",
                    "content": "Cây nhị phân với quy tắc: Node con bên trái nhỏ hơn cha, Node con bên phải lớn hơn cha. Giúp tìm kiếm nhanh O(log n).",
                    "code_snippet": "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\n# Insert logic would go here",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Tree Traversal (Duyệt cây)",
                    "content": "- **BFS:** Duyệt theo tầng (Level Order).\n- **DFS:** Duyệt theo chiều sâu (Pre-order, In-order, Post-order).",
                    "order_index": 2
                }
            ]
        },

        # --- Group 6: Heaps ---
        {
            "title": "6. Heaps (Priority Queue)",
            "short_definition": "Cây nhị phân hoàn chỉnh dùng để tìm Max/Min nhanh nhất",
            "tag_slugs": ["trees", "dsa-core"],
            "sections": [
                {
                    "heading": "Min Heap & Max Heap",
                    "content": "- **Max Heap:** Node cha luôn lớn hơn con. Gốc là Max.\n- **Min Heap:** Node cha luôn nhỏ hơn con. Gốc là Min.\nThường dùng để cài đặt Priority Queue.",
                    "code_snippet": "import heapq\n\nmin_heap = []\nheapq.heappush(min_heap, 5)\nheapq.heappush(min_heap, 1)\nheapq.heappush(min_heap, 10)\n\nprint(heapq.heappop(min_heap)) # 1 (Smallest out first)",
                    "language": "python",
                    "order_index": 1
                }
            ]
        },

        # --- Group 7: Graphs ---
        {
            "title": "7. Graphs (Đồ thị)",
            "short_definition": "Tập hợp các đỉnh (Vertices) và cạnh (Edges)",
            "tag_slugs": ["non-linear-structures", "graphs"],
            "sections": [
                {
                    "heading": "Biểu diễn Đồ thị",
                    "content": "- **Adjacency Matrix:** Ma trận 2 chiều (tốn bộ nhớ).\n- **Adjacency List:** Dictionary chứa list các đỉnh kề (phổ biến hơn).",
                    "code_snippet": "graph = {\n    'A': ['B', 'C'],\n    'B': ['A', 'D'],\n    'C': ['A', 'D'],\n    'D': ['B', 'C']\n}",
                    "language": "python",
                    "order_index": 1
                },
                {
                    "heading": "Graph Traversal",
                    "content": "- **BFS (Breadth First):** Dùng Queue, tìm đường ngắn nhất trong đồ thị không trọng số.\n- **DFS (Depth First):** Dùng Stack/Đệ quy, dùng để giải mê cung, kiểm tra chu trình.",
                    "order_index": 2
                }
            ]
        },

        # --- Group 8: Sorting ---
        {
            "title": "8. Sorting Algorithms",
            "short_definition": "Các thuật toán sắp xếp phổ biến",
            "tag_slugs": ["sorting", "dsa-core"],
            "sections": [
                {
                    "heading": "Bubble & Selection Sort",
                    "content": "Các thuật toán cơ bản, độ phức tạp O(n^2). Dễ cài đặt nhưng chậm với dữ liệu lớn.",
                    "order_index": 1
                },
                {
                    "heading": "Merge Sort & Quick Sort",
                    "content": "Thuật toán chia để trị (Divide and Conquer). Hiệu năng tốt O(n log n).",
                    "code_snippet": "# Quick Sort idea\ndef quick_sort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)",
                    "language": "python",
                    "order_index": 2
                }
            ]
        }
    ],
    
    # 3. Related Topics
    "related_topics": [
        {"src": "1. Độ phức tạp & Big O", "dest": "2. Danh sách liên kết (Linked Lists)"},
        {"src": "1. Độ phức tạp & Big O", "dest": "8. Sorting Algorithms"},
        {"src": "2. Danh sách liên kết (Linked Lists)", "dest": "3. Stack & Queue"},
        {"src": "2. Danh sách liên kết (Linked Lists)", "dest": "4. Hash Tables (Bảng băm)"},
        {"src": "3. Stack & Queue", "dest": "7. Graphs (Đồ thị)"}, # Stack cho DFS, Queue cho BFS
        {"src": "5. Trees & BST", "dest": "6. Heaps (Priority Queue)"},
        {"src": "5. Trees & BST", "dest": "1. Độ phức tạp & Big O"}, # O(log n)
        {"src": "7. Graphs (Đồ thị)", "dest": "5. Trees & BST"}, # Tree là Graph đặc biệt
        {"src": "8. Sorting Algorithms", "dest": "1. Độ phức tạp & Big O"},
        {"src": "8. Sorting Algorithms", "dest": "6. Heaps (Priority Queue)"}, # Heap Sort
    ]
}

def seed_dsa_safe():
    print("🚀 Starting SAFE DSA Seed...")
    print("=" * 60)
    
    # --- 1. Tags ---
    print("\n🏷️  Processing Tags...")
    tag_map = {}
    name_map = {}
    
    try:
        existing = requests.get(f"{BASE_URL}/tags/").json()
        for t in existing:
            tag_map[t["slug"]] = t["id"]
            name_map[t["name"]] = t["id"]
    except:
        print("  ⚠️ Cannot fetch existing tags. Assuming empty DB.")

    for tag in dsa_tags:
        if tag["slug"] in tag_map:
            print(f"  ⏭️  Tag exists (slug): {tag['name']}")
        elif tag["name"] in name_map:
            old_id = name_map[tag["name"]]
            tag_map[tag["slug"]] = old_id 
            print(f"  ⚠️  Tag name '{tag['name']}' exists. Reusing ID: {old_id}")
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
        cats = requests.get(f"{BASE_URL}/categories/").json()
        for c in cats:
            if c["slug"] == dsa_data["category"]["slug"]:
                cat_id = c["id"]
                print(f"  ⏭️  Category exists (ID: {cat_id})")
                break
        
        if not cat_id:
            res = requests.post(f"{BASE_URL}/categories/", json=dsa_data["category"])
            if res.status_code in [200, 201]:
                cat_id = res.json()["id"]
                print(f"  ✅ Category created: {dsa_data['category']['name']}")
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
    topic_id_map = {}
    
    for idx, topic in enumerate(dsa_data["topics"], 1):
        try:
            current_tag_ids = [tag_map[slug] for slug in topic["tag_slugs"] if slug in tag_map]
            
            topic_payload = {
                "title": topic["title"],
                "short_definition": topic["short_definition"],
                "category_id": cat_id,
                "tag_ids": current_tag_ids,
                "sections": []
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
    for item in dsa_data["related_topics"]:
        src = item["src"]
        dest = item["dest"]
        
        if src in topic_id_map and dest in topic_id_map:
            try:
                requests.post(f"{BASE_URL}/related-topics/", 
                            json={"topic_id": topic_id_map[src], "related_topic_id": topic_id_map[dest]})
            except:
                pass
    
    print("\n✨ DSA SEED COMPLETED!")

if __name__ == "__main__":
    seed_dsa_safe()