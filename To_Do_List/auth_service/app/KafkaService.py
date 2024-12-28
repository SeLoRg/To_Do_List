import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError
from fastapi import HTTPException
import asyncio
from pydantic import BaseModel


class KafkaMessageHeadersSchema(BaseModel):
    service_from: str
    method: str  # что именно сделать
    type_message: str  # ответ или запрос


class KafkaService:
    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str | None = None,
        auto_offset_reset: str = "earliest",
    ):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset
        self.consumer: AIOKafkaConsumer | None = None
        self.producer: AIOKafkaProducer | None = None
        self.active_auth_requests: dict = {}

    async def consume_messages(self):
        try:
            async for msg in self.consumer:
                print(f"Received message: {msg.value}")

                service_from = None
                method = None
                type_message = None

                for header in msg.headers:
                    if header[0] == "service_from":
                        service_from = header[1].decode()
                    if header[0] == "method":
                        method = header[1].decode()
                    if header[0] == "type_message":
                        type_message = header[1].decode()

                if type_message == "response":
                    if service_from == "users-service":
                        asyncio.create_task(self.handle_message_users_response(msg))
                elif type_message == "request":
                    pass
        except KafkaError as e:
            print(f"Error occurred while consuming messages: {e}")
        finally:
            print("consumer closed")
            await self.consumer.stop()

    async def send_and_wait(
        self, value: dict, topic: str, headers: KafkaMessageHeadersSchema
    ):
        try:
            print(f"try send message with: {headers}")
            await self.producer.send_and_wait(
                topic=topic,
                value=json.dumps(value).encode("utf-8"),
                headers=[
                    (key, value.encode()) for key, value in headers.model_dump().items()
                ],
            )
            print("message send")
        except KafkaError as e:
            print(f"Error while send message to users: {e}")
            raise HTTPException(status_code=500, detail=f"Error send: {e}")

    async def start_consumer(self, *topics):
        try:
            self.consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset=self.auto_offset_reset,
            )

            await self.consumer.start()
            print("consumer started")

        except KafkaError as e:
            print(f"Error occurred while creating consumer: {e}")
            raise HTTPException(status_code=500, detail=f"Kafka Error: {e}")

    async def stop_consumer(self):
        await self.consumer.stop()
        self.active_auth_requests.clear()
        self.consumer = None
        print("consumer stopped")

    async def start_producer(self):
        try:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self.producer.start()
            print("produces started")
        except KafkaError as e:
            print(f"Error while creating producer: {e}")
            raise HTTPException(status_code=500, detail=f"Kafka Error: {e}")

    async def stop_producer(self):
        await self.producer.stop()
        self.producer = None
        print("producer stopped")

    async def handle_message_users_response(self, msg):
        try:
            response_id: str = msg.value.get("response_id")
            if response_id in self.active_auth_requests:
                self.active_auth_requests[response_id].set_result(msg.value)
                print(f"Message from users-response-auth: {msg.value}")
            else:
                print(f"Message with response id: {response_id} is missing in requests")
        except Exception as e:
            print(f"Error while processing message: {e}")
