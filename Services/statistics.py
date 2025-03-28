from sqlalchemy import func
from sqlalchemy.orm import Session
from Models.Pulisher_Author import Publisher, Author
from Models.books import Books
from Models.statistics import Borrows, Borrows_detail
from database import get_db


class ServiceStatistics:
    @staticmethod
    def get_borrow_statistics(db: Session):
    # Truy vấn thống kê sách, mã sách, tác giả, mã tác giả và tổng số lần mượn
        stats = (
            db.query(
                Author.author_id.label("author_id"),
                Author.name.label("author_name"),
                Books.book_id.label("book_id"),
                Books.name.label("book_name"),
                func.count(Borrows.ticket_id).label("total_borrows")
            )
            .join(Books, Books.author_id == Author.author_id)
            .join(Borrows_detail, Borrows_detail.book_id == Books.book_id)
            .join(Borrows, Borrows.ticket_id == Borrows_detail.ticket_id)
            .group_by(Author.author_id, Author.name, Books.book_id, Books.name)
            .order_by(func.count(Borrows_detail.ticket_id).desc())
            .all()
        )
        
        # Định dạng kết quả
        result = []
        for stat in stats:
            result.append({
                "author_id": stat.author_id,
                "author_name": stat.author_name,
                "book_id": stat.book_id,
                "book_name": stat.book_name,
                "total_borrows": stat.total_borrows
            })
        
        return result
