import asyncio

from loguru import logger

from core.bot import StickifyBot
from core.config import settings


async def main() -> None:
    bot = StickifyBot()
    async with bot:
        await bot.start(settings.discord_token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Critical error: {e}")