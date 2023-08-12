import asyncio
from dotenv import load_dotenv
load_dotenv('../dev.env')

from handlers import serve_forever


if __name__ == "__main__":
    asyncio.run(serve_forever())
