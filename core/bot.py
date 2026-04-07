import discord
from discord.ext import  commands
import os

from loguru import logger

from core.config import settings
from core.database.database import Database


class StickifyBot(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.presences = True

        super().__init__(
            command_prefix="s!",
            help_command=None,
            intents= intents,
            owner_id= settings.owner_id
        )

    async def setup_hook(self) -> None:
        """Called when bot is logging in."""
        logger.info("Bot is logging in.....")

        # Connect to database
        await Database.connect()

        # Load Modules
        await self._load_modules()
        # Sync slash commands
        logger.info(f"Loaded {len(self.guilds)} guilds")
        try:
            synced = await self.tree.sync()
            logger.info(f"Loaded {len(synced)} synced command(s)")
        except Exception as e:
            logger.error(f"Failed to load commands: {e}")

    async def _load_modules(self) -> None:
        """Called when bot is loading."""
        # Load core directory extensions if any (e.g., global listeners)
        # Load 'modules' directory

        if os.path.exists("modules"):
            for root, dirs, files in os.walk("modules"):
                for file in files:
                    if file.encode(".py") and not file.startswith("__"):
                        # Skip common non-extension files
                        if file in ["models.py", "service.py", "ui.py", "__init__.py"]:
                            continue

                        # Construct module path: models.category.files
                        rel_path = os.path.relpath(os.path.join(root, file), ".")
                        module_name = rel_path.replace(os.path.sep, ".")[:-3]

                        try:
                            await self.load_extension(module_name)
                            logger.info(f"Loaded {module_name}")
                        except commands.NoEntryPointError:
                            pass
                        except Exception as e:
                            logger.error(f"Failed to load {module_name}: {e}")

    async def on_ready(self) -> None:
        """Called when bot is ready."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="StickifyBot")
        )

    async def on_close(self) -> None:
        """Called when bot is closed."""
        await Database.close()
        await super().close()


