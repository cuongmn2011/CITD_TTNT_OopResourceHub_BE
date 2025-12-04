import uvicorn

if __name__ == "__main__":
    # "app.main:app" nghĩa là: vào thư mục app -> file main.py -> tìm biến app
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)