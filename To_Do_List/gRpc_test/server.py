import asyncio
import grpc
from concurrent import futures
from . import test_pb2
from . import test_pb2_grpc
from auth_service.app.shemas import CheckAuthResponse
from auth_service.app import service
from auth_service.Core.Database.database import (
    database_sessions,
    database_users,
)
import signal
import logging


class AuthServiceServicer(test_pb2_grpc.AuthServiceServicer):
    async def CheckAuth(self, request, context):
        print("CheckAuth call")
        access_token: str | None = (
            request.access_token.value if request.access_token else None
        )

        async with database_sessions.session_factory() as sess_sessions:
            res: CheckAuthResponse | None = await service.check_authenticate(
                access_token=access_token, session_sessions=sess_sessions
            )
            print(res)
            if res is None:
                return test_pb2.CheckAuthResponse(auth_status=False)
            else:
                return test_pb2.CheckAuthResponse(
                    auth_status=True,
                    token_is_updated=res.token_exp,
                    credentials=test_pb2.RequestCredentials(
                        user_email=res.credentials.user_email,
                        session_id=str(res.credentials.session_id),
                        user_id=str(res.credentials.user_id),
                    ),
                    new_access_token=(
                        res.new_token if res.new_token is not None else None
                    ),
                )


async def serve():
    server = grpc.aio.server()
    test_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
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


if __name__ == "__main__":
    asyncio.run(serve())
