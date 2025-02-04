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
    CheckAuthRequest,
)
from app import service
from app.logger import logger
from Core.Database.database import (
    database_sessions,
    database_users,
)
from sqlalchemy import text
from Core.redis_client.redis_client import redis_client
import signal
from google.protobuf.wrappers_pb2 import StringValue


class AuthServiceServicer(auth_pb2_grpc.AuthServiceServicer):
    async def CheckAuth(self, request, context):
        logger.info("-------------CheckAuth call-------------")
        access_token, refresh_token = (
            request.tokens.access_token,
            request.tokens.refresh_token,
        )

        async with database_sessions.session_factory() as sess_sessions:
            data: CheckAuthRequest = CheckAuthRequest(
                access_token=access_token,
                refresh_token=refresh_token,
                ip=request.ip,
                agent=request.agent,
            )
            res: CheckAuthResponse = await service.check_authenticate(
                data=data, session_sessions=sess_sessions
            )
            if not res.is_login:
                return auth_pb2.CheckAuthResponse(is_login=False)

            print(res)

            out = auth_pb2.CheckAuthResponse(
                is_login=True,
                credentials=auth_pb2.Credentials(
                    user_id=str(res.credentials.user_id),
                ),
            )

            if res.new_tokens is not None:
                out.new_tokens = auth_pb2.Tokens(
                    access_token=res.new_tokens.access_token,
                    refresh_token=res.new_tokens.refresh_token,
                )

            return out

    async def Login(self, request, context):
        logger.info("-------------Login call-------------")
        data: UserLoginSchema = UserLoginSchema(
            email=request.user_email,
            password=request.password,
            ip=request.ip,
            agent=request.agent,
        )

        async with database_sessions.session_factory() as sess_sessions:
            async with database_users.session_factory() as sess_users:
                res: UserLoginResponse | HTTPException = await service.login(
                    data=data, session_user=sess_users, session_sessions=sess_sessions
                )

                if isinstance(res, HTTPException):
                    logger.info(f"Error: {res.detail}")
                    return auth_pb2.LoginResponse(
                        is_login=False,
                    )

                return auth_pb2.LoginResponse(
                    is_login=True,
                    tokens=auth_pb2.Tokens(
                        access_token=res.access_token, refresh_token=res.refresh_token
                    ),
                )

    async def Logout(self, request, context):
        logger.info("-------------Logout call-------------")
        data: LogoutRequest = LogoutRequest(
            user_id=int(request.credentials.user_id),
        )
        async with database_sessions.session_factory() as sess_sessions:
            res: HTTPException | None = await service.logout(
                credentials=data, session_sessions=sess_sessions
            )

            if isinstance(res, HTTPException):
                return auth_pb2.LogoutResponse(is_logout=False)

            return auth_pb2.LogoutResponse(is_logout=True)


async def serve():
    server_options = [
        ("grpc.max_send_message_length", 1024 * 1024 * 10),  # 10 MB
        ("grpc.max_receive_message_length", 1024 * 1024 * 10),  # 10 MB
        ("grpc.keepalive_time_ms", 60000),  # 60 секунд
        ("grpc.keepalive_timeout_ms", 20000),  # 20 секунд
        ("grpc.keepalive_permit_without_calls", True),
        ("grpc.http2.min_ping_interval_without_data_ms", 60000),
        ("grpc.http2.max_pings_without_data", 1),
        ("grpc.http2.max_connection_age_ms", 3600000),  # 1 час
        ("grpc.http2.max_connection_idle_ms", 600000),  # 10 минут
        ("grpc.http2.min_recv_ping_interval_without_data_ms", 60000),
    ]

    server = grpc.aio.server(options=server_options)
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Starting server on port 50051")

    async with database_sessions.session_factory() as sess_sessions:
        async with database_users.session_factory() as sess_users:
            await asyncio.gather(
                redis_client.ping(),
                sess_users.execute(text("SELECT 1")),
                sess_sessions.execute(text("SELECT 1")),
            )

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
    await asyncio.gather(
        database_users.engine.dispose(),
        database_sessions.engine.dispose(),
        redis_client.close(),
        return_exceptions=True,
    )
    await server.stop(grace=None)
    await server_task
    print("Server stopped")
