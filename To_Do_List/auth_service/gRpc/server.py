import asyncio
from fastapi.exceptions import HTTPException
import grpc
from . import auth_pb2
from . import auth_pb2_grpc
from app.shemas import (
    CheckAuthResponse,
    UserLoginSchema,
    UserLoginResponse,
    LogoutRequest,
)
from app import service
from app.logger import logger
from Core.Database.database import (
    database_sessions,
    database_users,
)
import signal
from google.protobuf.wrappers_pb2 import StringValue


class AuthServiceServicer(auth_pb2_grpc.AuthServiceServicer):
    async def CheckAuth(self, request, context):
        logger.info("CheckAuth call")
        access_token: str | None = (
            request.access_token.value if request.access_token else None
        )

        async with database_sessions.session_factory() as sess_sessions:
            res: CheckAuthResponse | None = await service.check_authenticate(
                access_token=access_token, session_sessions=sess_sessions
            )
            if res is None:
                return auth_pb2.CheckAuthResponse(auth_status=False)
            else:
                return auth_pb2.CheckAuthResponse(
                    auth_status=True,
                    token_is_updated=res.token_exp,
                    credentials=auth_pb2.RequestCredentials(
                        user_email=res.credentials.user_email,
                        session_id=str(res.credentials.session_id),
                        user_id=str(res.credentials.user_id),
                    ),
                    new_access_token=(
                        StringValue(value=res.new_token)
                        if res.new_token is not None
                        else None
                    ),
                )

    async def Login(self, request, context):
        logger.info("Login call")
        data: UserLoginSchema = UserLoginSchema(
            email=request.user_email, password=request.password
        )

        async with database_sessions.session_factory() as sess_sessions:
            async with database_users.session_factory() as sess_users:
                res: UserLoginResponse | HTTPException = await service.login(
                    data=data, session_user=sess_users, session_sessions=sess_sessions
                )

                if isinstance(res, HTTPException):
                    return auth_pb2.LoginResponse(
                        status_code=str(res.status_code),
                        detail=res.detail,
                    )

                return auth_pb2.LoginResponse(
                    status_code=str(200),
                    access_token=res.access_token,
                )

    async def Logout(self, request, context):
        logger.info("Logout call")
        data: LogoutRequest = LogoutRequest(
            user_email=request.user_email,
            session_id=int(request.session_id),
            user_id=int(request.user_id),
        )
        async with database_sessions.session_factory() as sess_sessions:
            res: HTTPException | None = await service.logout(
                credentials=data, session_sessions=sess_sessions
            )

            if isinstance(res, HTTPException):
                return auth_pb2.LogoutResponse(
                    status_code=str(res.status_code),
                    detail=res.detail,
                )

            return auth_pb2.LogoutResponse(
                status_code="201",
                detail="User logout",
            )


async def serve():
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Starting server on port 50051")

    stop_server = asyncio.Event()

    def signal_handler(signal, frame):
        print("Signal received, stopping server...")
        stop_server.set()

    signal.signal(signal.SIGINT, signal_handler)

    async def server_termination():
        await server.start()
        await server.wait_for_termination()

    server_task = asyncio.create_task(server_termination())

    await stop_server.wait()
    print("Stopping Server")
    await server.stop(grace=None)
    await server_task
    print("Server stopped")
