import asyncio
from gRpc import server

if __name__ == "__main__":
    asyncio.run(server.serve())
