from fastapi import FastAPI, Cookie, Depends, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from To_Do_List.api.api_BD import router
from To_Do_List.api.api_auth.router import router as api_auth_router
from To_Do_List.api.api_auth import router as api_auth


# Инициализация Sentry (GlitchTip)
# sentry_sdk.init(
#     dsn="https://328ba29b708840beac8dfd5856d97c57@app.glitchtip.com/9575",  # Замените на ваш DSN из GlitchTip
#     traces_sample_rate=1.0,  # Уровень отслеживания (от 0.0 до 1.0)
# )
app = FastAPI()
app.include_router(router=router, prefix="/api")
app.include_router(router=api_auth_router, prefix="/api")
app.mount(
    "/front",
    StaticFiles(directory="C:/Users/rosti/PycharmProjects/FastAPI_DB/To_Do_List/front"),
    name="front",
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        if "text/html" in request.headers.get("Accept", ""):
            return RedirectResponse(url="/login")
        else:
            return JSONResponse(status_code=401, content={"detail": "Please login"})

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/login", response_class=FileResponse)
async def get_start_page():
    response = FileResponse("/To_Do_List/front/html/form-login.html")

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/registrate", response_class=FileResponse)
async def get_start_page():
    response = FileResponse("/To_Do_List/front/html/form-registrate.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/tokens")
async def get_token(payload: dict = Depends(api_auth.check_access_token)):
    return payload


@app.get("/")
async def get_main_page(cookie=Depends(api_auth.check_access_token)):
    response = FileResponse("/To_Do_List/front/index.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/confirm-email")
async def get_main_page():
    response = FileResponse("/To_Do_List/front/html/confirm-email.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/email-send")
async def get_main_page():
    response = FileResponse("/To_Do_List/front/html/email-send.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/user-verification")
async def get_main_page(token: str):
    response = FileResponse("/To_Do_List/front/html/email-confirmed.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/form-password-recovery")
async def get_main_page():
    response = FileResponse("/To_Do_List/front/html/form-password-recovery.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/update-password")
async def get_main_page(email: str):
    response = FileResponse("/To_Do_List/front/html/form-update-password.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
