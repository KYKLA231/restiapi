from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database import Base, engine, get_db
from app.routers import user
from app.routers import chat
# Ensure model modules are imported so SQLAlchemy knows all tables/columns
import app.models.user
import app.models.chat
import app.models.post
import app.models.group
import app.models.comment
import app.models.notification
import app.models.event
from app.crud import user as crud_user
from app.schemas import user as schemas
from pydantic import ValidationError
from sqlalchemy.orm import Session
import traceback
import logging

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Мой проект",
    description="Пример веб-приложения на FastAPI",
    version="1.0.0"
)

# Создаем базу данных при запуске — выполняем в событии startup чтобы
# гарантировать, что все модули моделей импортированы и видны SQLAlchemy.
@app.on_event("startup")
def create_db_tables_on_startup():
    Base.metadata.create_all(bind=engine)

# Монтируем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутер API (роутер уже содержит префикс)
app.include_router(user.router)
app.include_router(chat.router)
# new resource routers so they show in /docs
try:
    from app.routers import post as post_router
    app.include_router(post_router.router)
except Exception:
    app.logger and app.logger.warning('post router import failed')
try:
    from app.routers import group as group_router
    app.include_router(group_router.router)
except Exception:
    app.logger and app.logger.warning('group router import failed')
try:
    from app.routers import comment as comment_router
    app.include_router(comment_router.router)
except Exception:
    app.logger and app.logger.warning('comment router import failed')
try:
    from app.routers import notification as notification_router
    app.include_router(notification_router.router)
except Exception:
    app.logger and app.logger.warning('notification router import failed')
try:
    from app.routers import event as event_router
    app.include_router(event_router.router)
except Exception:
    app.logger and app.logger.warning('event router import failed')


# Вспомогательная функция: получаем текущего пользователя по cookie (email)
def get_current_user_from_request(request: Request, db: Session):
    email = request.cookies.get("user_email")
    if not email:
        return None
    return crud_user.get_user_by_email(db, email)


# Простые routes для веб-интерфейса (с cookie-based простым логином)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_request(request, db)
    # Отладочная печать cookies и найденного пользователя в лог сервера
    try:
        logging.getLogger("uvicorn.access").debug(f"Request cookies: {request.cookies}")
        logging.getLogger("uvicorn.access").debug(f"Resolved user: {getattr(user, 'email', None)}")
    except Exception:
        pass
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_request(request, db)
    if user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request, "user": None})


@app.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    try:
        form = await request.form()
        try:
            user_in = schemas.UserCreate(
                name=form.get("name"),
                email=form.get("email"),
                password=form.get("password")
            )
        except ValidationError as ve:
            # user provided invalid data (e.g. malformed email) — show form with message
            return templates.TemplateResponse("register.html", {"request": request, "user": None, "error": "Некорректные данные: проверьте email и заполнение полей"})
        # простая проверка
        if crud_user.get_user_by_email(db, user_in.email):
            # Если email уже существует, показываем форму регистрации с ошибкой
            return templates.TemplateResponse("register.html", {"request": request, "user": None, "error": "Email уже зарегистрирован"})
        crud_user.create_user(db, user_in)
        return RedirectResponse(url="/login", status_code=303)
    except HTTPException:
        raise
    except Exception as e:
        # Логируем полный traceback в файл для отладки
        tb = traceback.format_exc()
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(tb + '\n')
        # Возвращаем 500 с общим сообщением
        raise HTTPException(status_code=500, detail='Internal Server Error')


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_request(request, db)
    if user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = await request.form()
        email = form.get("email")
        password = form.get("password")
        user = crud_user.authenticate_user(db, email, password)
        if not user:
            # Неверные учетные данные — вернуть страницу логина с сообщением об ошибке
            return templates.TemplateResponse("login.html", {"request": request, "user": None, "error": "Неверный email или пароль"})
        # Устанавливаем cookie с email пользователя
        response = RedirectResponse(url='/', status_code=303)
        response.set_cookie(key='user_email', value=user.email, httponly=True, max_age=3600*24)
        return response
    except HTTPException:
        raise
    except Exception:
        tb = traceback.format_exc()
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(tb + '\n')
        raise HTTPException(status_code=500, detail='Internal Server Error')


@app.get("/logout")
async def logout():
    response = RedirectResponse(url='/', status_code=303)
    response.delete_cookie('user_email')
    return response


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(get_db)):
    """Профиль пользователя (удобно для проверки состояния сессии)."""
    try:
        user = get_current_user_from_request(request, db)
        if not user:
            return RedirectResponse(url='/login', status_code=303)
        return templates.TemplateResponse("profile.html", {"request": request, "user": user})
    except Exception:
        tb = traceback.format_exc()
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(tb + '\n')
        raise HTTPException(status_code=500, detail='Internal Server Error')


@app.post("/profile")
async def profile_update(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user_from_request(request, db)
        if not user:
            return RedirectResponse(url='/login', status_code=303)
        form = await request.form()
        name = form.get('name')
        password = form.get('password')
        avatar = form.get('avatar')
        bio = form.get('bio')
        data = {}
        if name:
            data['name'] = name
        if password:
            data['password'] = password
        if avatar is not None:
            data['avatar'] = avatar
        if bio is not None:
            data['bio'] = bio
        if data:
            crud_user.update_user(db, user.id, data)
        return RedirectResponse(url='/profile', status_code=303)
    except Exception:
        tb = traceback.format_exc()
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(tb + '\n')
        raise HTTPException(status_code=500, detail='Internal Server Error')
