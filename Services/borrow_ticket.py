from sqlalchemy.orm import Session
from Models.books import Books
from Models.statistics import Borrows, Borrows_detail
from datetime import date

class ServiceBorrow:
    @staticmethod
    def get_all_tickets(db: Session):
        today = date.today()
        tickets = db.query(Borrows).all()
        
        for ticket in tickets:
            if ticket.status != "Da tra" and ticket.end_date and ticket.end_date < today:
                ticket.status = "Qua han"
                db.commit()

        return tickets

    @staticmethod
    def get_all_details(db: Session):
        return db.query(Borrows_detail).all()

    @staticmethod
    def get_borrow_details(db: Session, ticket_id: str):
        return db.query(Borrows_detail).filter(Borrows_detail.ticket_id == ticket_id).all()

    @staticmethod
    def create_borrow(db: Session, ticket_id: str, reader_id: str, 
                     start_date: date, end_date: date, book_id: str):
        book = db.query(Books).filter(Books.book_id == book_id).first()
        if not book:
            return None, "Book not found"
        if book.quantity <= 0:
            return None, "Book out of stock"
        
        new_borrow = Borrows(
            ticket_id=ticket_id,
            reader_id=reader_id,
            start_date=start_date,
            end_date=end_date,
            status='Borrowed'
        )
        db.add(new_borrow)
        
        new_detail = Borrows_detail(
            ticket_id=ticket_id,
            book_id=book_id
        )
        db.add(new_detail)
        
        book.quantity -= 1
        db.commit()
        
        return new_borrow, None

    @staticmethod
    def delete_borrow(db: Session, ticket_id: str):
        db.query(Borrows_detail).filter(Borrows_detail.ticket_id == ticket_id).delete()
        
        borrow = db.query(Borrows).filter(Borrows.ticket_id == ticket_id).first()
        if not borrow:
            return None, "Borrow not found"
        
        db.delete(borrow)
        
        details = db.query(Borrows_detail).filter(Borrows_detail.ticket_id == ticket_id).all()
        for detail in details:
            book = db.query(Books).filter(Books.book_id == detail.book_id).first()
            if book:
                book.quantity += 1
        
        db.commit()
        return True, None