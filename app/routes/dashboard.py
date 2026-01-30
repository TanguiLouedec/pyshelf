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
    db = SessionLocal()
    logs = db.query(Log).options(joinedload(Log.book)).all()
    books = db.query(Book).all()
    db.close()

    context = {"request": request, "title": "Dashboard", "logs": logs, "books": books}
    return templates.TemplateResponse("dashboard.html", context)


@router.post("/logs/add", response_class=HTMLResponse)
async def add_log(request: Request,
                  book_id: int = Form(...),
                  page_start: int = Form(...),
                  page_end: int = Form(...)):
    
    if page_end < page_start:
        page_end = page_start
    
    db = SessionLocal()

    log = Log(book_id = book_id, page_start = page_start, page_end = page_end)
    db.add(log)
    db.commit()

    db.close()

    return RedirectResponse("/", status_code=303)

@router.post("/books/add", response_class=HTMLResponse)
async def add_book(request: Request,
                   book_name: str = Form(...),
                   author: str = Form(...),
                   page_count: int = Form(...)):
    
    db = SessionLocal()

    book = Book(name = book_name, author = author, page_count = page_count)
    db.add(book) 
    db.commit()

    db.close()

    return RedirectResponse("/", status_code=303)
