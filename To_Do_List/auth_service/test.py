from app.service import login, logout, check_authenticate
from Core.Database.database import database_users, database_sessions
from Core.config.config import settings
from app.shemas import (
    UserLoginSchema,
    UserLoginResponse,
    LogoutRequest,
    CheckAuthRequest,
    CheckAuthResponse,
    Tokens,
    Credentials,
)
from fastapi import HTTPException
import asyncio
import grpc
from gRpc import auth_pb2_grpc, auth_pb2


async def main():
    channel = grpc.aio.insecure_channel("localhost:50051")
    stub = auth_pb2_grpc.AuthServiceStub(channel)

    # request = auth_pb2.LoginRequest(
    #     ip="127.0.0.1", agent="Mozilla", user_email="ros@bk.ru", password="123"
    # )
    # res = await stub.Login(request)
    # if res.is_login:
    #     print(
    #         UserLoginResponse(
    #             is_login=res.is_login,
    #             access_token=res.tokens.access_token,
    #             refresh_token=res.tokens.refresh_token,
    #         )
    #     )
    # else:
    #     print(res.is_login)
    #
    # request = auth_pb2.CheckAuthRequest(
    #     ip="127.0.0.1",
    #     agent="Mozilla",
    #     tokens=auth_pb2.Tokens(
    #         access_token=res.tokens.access_token, refresh_token=res.tokens.refresh_token
    #     ),
    # )
    #
    # res = await stub.CheckAuth(request)
    #
    # if res.is_login:
    #     out = CheckAuthResponse(
    #         is_login=res.is_login,
    #         credentials=Credentials(user_id=res.credentials.user_id),
    #     )
    #
    #     if res.new_tokens is not None:
    #         out.new_tokens = Tokens(
    #             access_token=res.new_tokens.access_token,
    #             refresh_token=res.new_tokens.refresh_token,
    #         )
    #     print(out)
    # else:
    #     print(res.is_login)

    request = auth_pb2.LogoutRequest(credentials=auth_pb2.Credentials(user_id="12"))

    res = await stub.Logout(request)

    print(res.is_logout)


if __name__ == "__main__":
    asyncio.run(main())
