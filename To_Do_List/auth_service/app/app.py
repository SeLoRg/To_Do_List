import asyncio

from fastapi import FastAPI
from .router import router

from .kafka_interaction import kafka_service, KafkaMessageHeadersSchema

app = FastAPI()

app.include_router(router=router)


@app.on_event("startup")
async def startup_event():
    await kafka_service.start_consumer("users-response-auth")
    await kafka_service.start_producer()
    asyncio.create_task(kafka_service.consume_messages())


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await kafka_service.stop_consumer()
        await kafka_service.stop_producer()
    except Exception as e:
        print(str(e))


@app.post("/")
async def send_to_users(email: str, request_id: str):
    await kafka_service.send_and_wait(
        topic="users-requests",
        value={"request_id": request_id, "email": email},
        headers=KafkaMessageHeadersSchema(
            service_from="auth-service",
            type_message="request",
            method="get",
        ),
    )

    return {"status": "ok"}
