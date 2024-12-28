from ..Core.config.config import settings
from .KafkaService import KafkaService, KafkaMessageHeadersSchema
import asyncio
from fastapi import HTTPException
import uuid

kafka_service: KafkaService = KafkaService(bootstrap_servers=settings.KAFKA_BROKER)


async def get_user_from_users_service(email: str) -> int:
    future = asyncio.Future()
    request_id: str = str(uuid.uuid4())
    while True:
        if request_id in kafka_service.active_auth_requests:
            request_id: str = str(uuid.uuid4())
        else:
            break
    await kafka_service.send_and_wait(
        topic="users-requests",
        value={"request_id": request_id, "email": email},
        headers=KafkaMessageHeadersSchema(
            **{
                "service_from": "auth-service",
                "type_message": "request",
                "method": "get-user-id",
            }
        ),
    )

    kafka_service.active_auth_requests[request_id] = future
    try:
        res: dict = await asyncio.wait_for(future, timeout=300)
        return res.get("user_id")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout")
    finally:
        del kafka_service.active_auth_requests[request_id]


# async def send_message_to_users_service(topic: str, value: dict) -> str:
#     request_id: str = str(uuid.uuid4())
#
#     try:
#         await producer.send_and_wait(
#             topic=topic,
#             value=json.dumps(value).encode(),
#             headers=[("service", SERVICE_NAME)],
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Message dont send",
#         )
#
#     return request_id


# async def read_messages():
#     async for msg in consumer:
#         await messages.put(msg)


# Для каждого сервиса отдельный топик для ответа от users
# async def get_user_from_users_service(data: UserLoginSchema, request_id: str) -> int:
#     try:
#         async for msg in consumer:
#             service_name = None
#             for header in msg.headers:
#                 if header[0] == "service":
#                     service_name = header[1].decode("utf-8")
#                     break
#
#             if service_name == SERVICE_NAME:
#                 response: dict = json.loads(msg.values.decode())
#
#                 if "error" in response:
#                     raise HTTPException(
#                         status_code=status.HTTP_404_NOT_FOUND,
#                         detail="User not founded",
#                     )
#
#                 if (
#                     response.get("request_id") == request_id
#                     and response.get("email") == data.email
#                 ):
#                     return response.get("user_id")
#
#     except Exception as e:
#
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
#         )
