import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import joinedload

from app.models.models import SessionLocal, Book, Log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Render dashboard with logs and form
    """
    db = SessionLocal()
    logs = db.query(Log).options(joinedload(Log.book)).all()
    db.close()

    context = {"request": request, "title": "Dashboard", "logs": logs}
    return templates.TemplateResponse("dashboard.html", context)


@router.post("/", response_class=HTMLResponse)
async def add_log(request: Request,
                  book_name: str = Form(...),
                  page_start: int = Form(...),
                  page_end: int = Form(...)):
    
    if page_end < page_start:
        page_end = page_start
    
    db = SessionLocal()

    book = db.query(Book).filter(Book.name == book_name).first()
    if not book:
        book = Book(name = book_name)
        db.add(book)
        db.commit()
        db.refresh(book)

    log = Log(book_id = book.id, page_start = page_start, page_end = page_end)
    db.add(log)
    db.commit()

    logs = db.query(Log).all()
    db.close()

    return RedirectResponse("/", status_code=303)