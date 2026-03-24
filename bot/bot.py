from javascript import require, On # mineflayer is a javascript package
from dotenv import load_dotenv
import os
import socket

load_dotenv(override=True)
claude_key = os.getenv("ANTHROPIC_API_KEY")

mineflayer = require("mineflayer")


class BuilderBot:
    def __init__(self, username):
        """
        Initializes a bot in Minecraft
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        try:
            host = ip
            port = 54569
            name = "R2D2"  # Replace with the desired bot username
            self.bot = mineflayer.createBot(
                {
                    "host": host,
                    "port": port,
                    "username": name,
                }
            )

            self.username = username
            self.setup_listeners()
        except Exception as e:
            print("Failed to start bot")
            return
    def setup_listeners(self):
        @On(self.bot, "spawn")
        def handle_spawn(*args):
            self.bot.chat(f"/tp {self.username}")

        @On(self.bot, "chat")
        def on_chat(this, sender, message, *args):
        # 1. Ignore messages sent by the bot itself.
            if sender == self.bot.username:
                return
        # 2. Convert the message to a string (if needed).
            message = str(message)  
        # 3. Check if the message (case-insensitive) equals "come".
            if message.lower() == "come":
                self.bot.chat(f"/tp {self.username}")
            if message.lower() == "follow":
                while message.lower()!="stop":
                    self.bot.chat(f"/tp {self.username}")

                self.bot.chat("Stopping bot.")
                self.bot.quit()
            @On(self.bot, "end")
            def on_end(*args):
                print("Bot disconnected.")