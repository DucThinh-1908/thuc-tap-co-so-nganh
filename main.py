from fastapi import FastAPI
from Controllers.Users import router as user_router
from Controllers.Readers import router as reader_router
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Tạo FastAPI app
app = FastAPI(title="Users API MVC", description="CRUD API cho bảng Users với SQL Server sử dụng mô hình MVC")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả nguồn, có thể đổi thành ["http://localhost"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức HTTP (GET, POST, ...)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Tạo bảng nếu chưa tồn tại
Base.metadata.create_all(bind=engine)

# Đăng ký routers
app.include_router(user_router)
app.include_router(reader_router)
# Endpoint mặc định
@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Users API using MVC pattern"}

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

print('Vai ca cut')
