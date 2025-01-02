from ..Core.config.config import settings
from To_Do_List.Core.kafka_service.KafkaService import (
    KafkaService,
    KafkaMessageHeadersSchema,
)
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
