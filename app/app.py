from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
from .block import create_block, check_integrity

app = FastAPI()

# Настроим логирование
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logging.info("Запрос на главную страницу")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def create_new_block(request: Request, lender: str = Form(...), amount: str = Form(...), borrower: str = Form(...)):
    logging.info(f"POST-запрос: lender={lender}, amount={amount}, borrower={borrower}")
    create_block(name=lender, amount=amount, to_whom=borrower)
    logging.info("Блок успешно создан")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/checking", response_class=HTMLResponse)
async def check(request: Request):
    logging.info("Запрос на проверку целостности блоков")
    results = check_integrity()
    logging.info(f"Результаты проверки: {results}")
    return templates.TemplateResponse('index.html', {"request": request, "results": results})