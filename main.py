from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.utils.recommend import recommend_build_with_compat


app = FastAPI()


# 이미지 불러오기
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
# ################################################################################
#hmtl 연결
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def get_search(request: Request, budget: int = None, purpose: str = None):
    result = None
    if budget and purpose:
        result = recommend_build_with_compat(budget, purpose)    
    return templates.TemplateResponse("search.html", {"request": request, 'result': result, 'budget':budget, 'purpose':purpose})

# result
@app.get("/search/result", response_class=HTMLResponse)
async def get_search(request: Request, budget: int = None, purpose: str = None):
    result = None
    if budget and purpose:
        result = recommend_build_with_compat(budget, purpose)    
    return templates.TemplateResponse("result.html", {"request": request, 'result': result, 'budget':budget, 'purpose':purpose})

@app.get("/faq", response_class=HTMLResponse)
async def get_faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})