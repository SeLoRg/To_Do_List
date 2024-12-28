import redis
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError
from To_Do_List.Core.config.config import settings
from fastapi import HTTPException
import asyncio
import redis


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
        self.active_requests: dict = {}

    async def consume_messages(self):
        try:
            async for msg in self.consumer:
                print(f"Received message: {msg.value}")
                await asyncio.create_task(self.handle_message(msg))
        except KafkaError as e:
            print(f"Error occurred while consuming messages: {e}")
        finally:
            print("consumer closed")
            await self.consumer.stop()

    async def start_consumer(self, *topics):
        try:
            self.consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset=self.auto_offset_reset,
            )

            await self.consumer.start()
        except KafkaError as e:
            print(f"Error occurred while creating consumer: {e}")
            raise HTTPException(status_code=500, detail=f"Kafka Error: {e}")

    async def stop_consumer(self):
        await self.consumer.stop()
        self.active_requests.clear()
        self.consumer = None

    async def start_producer(self):
        try:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self.producer.start()
        except KafkaError as e:
            print(f"Error while creating producer: {e}")
            raise HTTPException(status_code=500, detail=f"Kafka Error: {e}")

    async def stop_producer(self):
        await self.producer.stop()
        self.producer = None

    async def handle_message(self, msg):
        request_id: str = msg.value.get("request_id")
        if request_id in self.active_requests:
            self.active_requests[request_id].set_result(msg.value)
            print(f"Message from users-response-auth: {msg.value}")
