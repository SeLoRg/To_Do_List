# from fastapi import FastAPI, BackgroundTasks
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import BaseModel, EmailStr
# from fastapi.responses import JSONResponse
# import logging
# from To_Do_List.Core.config import settings
#
# app = FastAPI()
# logging.basicConfig(level=logging.INFO)
# # Конфигурация SMTP
# conf = ConnectionConfig(
#     MAIL_USERNAME="rostislavmarinov@bk.ru",
#     MAIL_PASSWORD=settings.MAIL_KEY,
#     MAIL_FROM="rostislavmarinov@bk.ru",
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.mail.ru",  # Замените на ваш SMTP сервер
#     MAIL_FROM_NAME="Ros",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
# )
#
#
# class EmailSchema(BaseModel):
#     email: EmailStr
#     subject: str
#     message: str
#
#
# async def send_email_task(fm: FastMail, message: MessageSchema):
#     try:
#         await fm.send_message(message)
#         logging.info("Email sent successfully")
#     except Exception as e:
#         logging.error(f"Failed to send email: {e}")

#
# @app.post("/send-email/")
# async def send_email(email: EmailSchema, background_tasks: BackgroundTasks):
#     message = MessageSchema(
#         subject=email.subject,
#         recipients=[email.email],
#         body=email.message,
#         subtype="html",
#     )
#
#     fm = FastMail(conf)
#
#     background_tasks.add_task(send_email_task, fm, message)
#
#     return JSONResponse(status_code=200, content={"message": "Email sent successfully"})

from To_Do_List.Core.config import settings
from To_Do_List.api.api_auth import dependencies
import asyncio


# async def test():
#     jwt = dependencies.create_jwt_token(email="ros@bk.ru", user_id=1)
#     return jwt


print(bool(int(settings.MAIL_SSL_TLS)), bool(int(settings.MAIL_STARTTLS)))
