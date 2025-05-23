from fastapi import FastAPI
from Controllers.Users import router as user_router
from Controllers.Readers import router as reader_router
from Controllers.books import router as book_router
from Controllers.statistics import router as statistics_router
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from Controllers.Library_staff import router as Library_staff_router
from Controllers.borrow_ticket import router as borrow_ticket_router

# Tạo FastAPI app
app = FastAPI(title="Users API MVC", description="CRUD API cho bảng Users với SQL Server sử dụng mô hình MVC")

origins = [
    "http://127.0.0.1:5500",  # Địa chỉ frontend
    "http://localhost:5500"
]
# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả nguồn, có thể đổi thành ["http://localhost"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức HTTP (GET, POST, ...)
    allow_headers=["*"],  # Cho phép tất cả headers
    expose_headers=["*"]
)

# Tạo bảng nếu chưa tồn tại
Base.metadata.create_all(bind=engine)

# Đăng ký routers
app.include_router(user_router)
app.include_router(reader_router)
app.include_router(book_router)
app.include_router(statistics_router)
app.include_router(Library_staff_router)
app.include_router(borrow_ticket_router)
# Endpoint mặc định
@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Users API using MVC pattern"}

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
