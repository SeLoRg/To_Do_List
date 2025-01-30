import asyncio
import logging
import grpc

# from google.protobuf.wrappers_pb2 import StringValue
import auth_pb2
import auth_pb2_grpc
from To_Do_List.auth_service.app.shemas import CheckAuthResponse

logging.basicConfig(level=logging.INFO)


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)

        # Создание запроса
        request = auth_pb2.CheckAuthRequest()
        request.access_token.value = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMiwidXNlcl9lbWFpbCI6InJvc0Biay5ydSIsInNlc3Npb25faWQiOjQ3LCJpYXQiOjE3MzcyMzUzNjEuODYwODAxLCJleHAiOjE3MzcyMzU2NjEuODYwODAxLCJ0eXAiOiJhY2Nlc3MifQ.SVxmjVcGKtL76nIAw5r3gRL24-vaYnNmdyr0CJRXSRa0_MT_LnnFr4KRT7MGvAiaI8p4DrvQahw6jhk9LNSODypC83kEWY-S0B-SRdNsvCYb2K-RvYgXg1T4VRvm2WR5YEgNPHB3ibv365SQfR2YaAoZ9vewtLCxXUzsIYik75eY4FvuXYB2RgwAShuXH3XTQxgjxRwmPz8x9_IvKSHsUXK1ScwADH82AVECr0TSifbcf8u6UrD2Pti2RhYueNGW_XMMPQ536I6M9Mkear507o91hXQcExNOq_YMsUm2OAn4Gs8ELh7-QkDpF3i4NJWTEYDShGrf8eP5B6nGHMij8A"
        # Отправка запроса и получение ответа
        try:
            response = await stub.CheckAuth(request)
            if response is None:
                print("Invalid token")
            print(f"Response received: {response}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.details()}")

        request = auth_pb2.LoginRequest()
        request.user_email = "ros@bk.ru"
        request.password = "123"

        # Отправка запроса и получение ответа
        try:
            response = await stub.Login(request)
            if response is None:
                print("Invalid email or password")
            print(f"Response received: {response}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.details()}")


if __name__ == "__main__":

    asyncio.run(main())
