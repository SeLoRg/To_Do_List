from . import auth_pb2, auth_pb2_grpc
import grpc
import logging


class GrpcClient:
    def __init__(self, url):
        self.url = url
        self.connection: auth_pb2_grpc.AuthServiceStub | None = None

    @classmethod
    async def connect(cls, url) -> auth_pb2_grpc.AuthServiceStub | None:
        try:
            logging.info(f"Try create gRpc channel to auth service...")
            channel: grpc.aio.Channel = grpc.aio.insecure_channel(url)
            stub = auth_pb2_grpc.AuthServiceStub(channel)
            logging.info(f"gRpc connection to auth service success")
            return stub
        except Exception as e:
            logging.error(f"Error during connect to auth service: {str(e)}")
            return None

    @classmethod
    async def reconnect(cls, url) -> auth_pb2_grpc.AuthServiceStub | None:
        logging.info(f"Try reconnect...")
        new_connection: auth_pb2_grpc.AuthServiceStub | None = await cls.connect(
            url=url
        )

        reconnect: int = 5
        while new_connection is None:
            logging.info(f"Couldn't connect")
            logging.info(f"Try reconnect...")
            if reconnect <= 0:
                logging.error(f"Connection to auth service is fault")
                return None

            new_connection = await cls.connect(url=url)
            reconnect -= 1

        logging.info(f"Connection to auth service was success")
        return new_connection

    async def get_connection(self) -> auth_pb2_grpc.AuthServiceStub | None:
        if self.connection is None:
            logging.info(f"No connection")
            connection: auth_pb2_grpc.AuthServiceStub | None = await self.reconnect(
                url=self.url
            )
            self.connection = connection

        res = self.connection.get_state()
        if res != (
            grpc.ChannelConnectivity.READY
            or grpc.ChannelConnectivity.CONNECTING
            or grpc.ChannelConnectivity.IDLE
        ):
            logging.info(f"Connection to auth service is fault")
            new_connection: auth_pb2_grpc.AuthServiceStub | None = await self.reconnect(
                url=self.url
            )

            self.connection = new_connection

        if self.connection is None:
            logging.error(f"Connection to auth service is fault")
            return

        logging.info(f"Connection to auth service is ok")
        return self.connection
