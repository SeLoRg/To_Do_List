from fastapi import (
    Response,
    Cookie,
    APIRouter,
    BackgroundTasks,
    status,
    Depends,
    HTTPException,
)
from .shemas import UserLoginSchema
from . import service
from sqlalchemy.ext.asyncio import AsyncSession
from ...Core.Database.database import database
from . import dependencies


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    data: UserLoginSchema,
    session: AsyncSession = Depends(database.get_session),
):
    try:
        login_result: dict = await service.login_user(data, session, response)
        return login_result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    # token_refresh = await dependencies.create_jwt_token(
    #     refresh_id=1,
    #     user_id=2,
    #     typ="refresh",
    # )
    # return {"detail": token_refresh}


# @router.post("/send-email-update-password", status_code=status.HTTP_200_OK)
# async def update_password(
#     request: EmailVerificationRequest,
#     background_tasks: BackgroundTasks,
# ):
#     html_path = os.path.join("To_Do_List/api/api_auth/html", "update-password.html")
#     async with aiofiles.open(html_path, "r", encoding="utf-8") as file:
#         html_content = await file.read()
#     html_content = html_content.replace("{{email}}", request.email)
#     email_message: MessageSchema = MessageSchema(
#         subject="Обновление пароля",
#         recipients=[request.email],
#         body=html_content,
#         subtype="html",
#     )
#
#     fm = FastMail(config=settings.smtp_conf)
#     background_tasks.add_task(dependencies.send_email_task, fm, email_message)
#
#     return {"detail": "email send"}
#

# @router.post("/send-email-verification", status_code=status.HTTP_200_OK)
# async def send_email_verification(
#     request: EmailVerificationRequest,
#     background_tasks: BackgroundTasks,
#     session: AsyncSession = Depends(database.get_session),
# ):
#     html_path = os.path.join("To_Do_List/api/api_auth/html", "email_verification.html")
#
#     if request.token is None:
#         token = await dependencies.create_temp_jwt_token(
#             email=request.email, session=session
#         )
#     else:
#         token = request.token.decode("utf-8")
#
#     async with aiofiles.open(html_path, "r", encoding="utf-8") as file:
#         html_content = await file.read()
#
#     html_content = html_content.replace("{{token}}", token)
#
#     email_message: MessageSchema = MessageSchema(
#         subject="Подтверждение электронной почты",
#         recipients=[request.email],
#         body=html_content,
#         subtype="html",
#     )
#
#     fm = FastMail(config=settings.smtp_conf)
#     background_tasks.add_task(dependencies.send_email_task, fm, email_message)
#
#     return {"detail": "email successfully send"}


# @router.get("/user-verification", status_code=status.HTTP_200_OK)
# async def user_verification(
#     token: str,
#     session: AsyncSession = Depends(database.get_session),
# ):
#     try:
#         payload = jwt.decode(
#             jwt=token.encode(),
#             key=settings.auth_jwt.publik_key.read_text(),
#             algorithms=settings.auth_jwt.algorithm,
#         )
#     except jwt.ExpiredSignatureError as a:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
#         )
#     except jwt.InvalidTokenError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
#         )
#
#     user_id: int = payload.get("sub")
#
#     stmt = select(UsersOrm).where(UsersOrm.id == user_id)
#     res: Result = await session.execute(stmt)
#
#     user: UsersOrm = res.scalars().first()
#     user.is_active = True
#
#     await session.commit()
#
#     return {"message": "User is active"}
