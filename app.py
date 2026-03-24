from flask import Flask, jsonify, request
from bot.bot import BuilderBot
import json

import json
from pydantic import ValidationError
from bot.models import MinecraftBuild

def complete_schematic(data):
    # in case data is a string
    if not isinstance(data, dict):
        # Find the last completed object
        last_brace = data.rfind("}")
        if last_brace == -1:
            return None

        trimmed = data[: last_brace + 1] # get all the completed blocks
        # Close blocks array and top-level object if missing
        trimmed = trimmed.rstrip()

        if not trimmed.endswith("]}"):
            trimmed += "]}"

        return json.loads(trimmed)

    return data  # complete data

app = Flask(__name__)

BOT_INSTANCE = None  # global bot instance

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/spawn_bot")
def spawn_bot():
    # TODO: Reference the global BOT_INSTANCE variable so this function can read and modify it (hint: use the 'global' keyword)
    global BOT_INSTANCE
    # TODO: Get the "username" parameter from the request's query string
    username = request.args.get("username")
    # TODO: Check if the bot has not been started yet
    if BOT_INSTANCE is None:
        # If not, create a new BuilderBot instance using the username and assign it to BOT_INSTANCE
        BOT_INSTANCE = BuilderBot(username)
        # Then return a JSON response indicating the bot was just started
        return jsonify({"message": f"Bot started for user {username}!"})
    # TODO: Create a new BuilderBot instance using the username and assign it to BOT_INSTANCE if the bot hasn't been started. Then return a JSON response indicating the bot was just started
    else:
        return jsonify({"message": f"Bot is already running for user {username}!"})
    # TODO: If the bot has been started already, return a JSON response indicating the bot is already running
    
@app.route("/build", methods=["POST"])
def build():
    global BOT_INSTANCE
    
    # 1. Check if bot exists
    if BOT_INSTANCE is None:
        return jsonify({"error": "no_bot"}), 400

    # 2. Get JSON from request
    raw_data = request.get_json()

    # 3. Validate/Repair the data
    validated_data = complete_schematic(raw_data)

    # 4. Fallback if JSON is broken
    if validated_data is None:
        # Update this path based on where your triangle.json actually lives!
        fallback_path = os.path.join(os.path.dirname(__file__), "schematics", "triangle.json")
        try:
            with open(fallback_path, "r") as f:
                validated_data = json.load(f)
        except FileNotFoundError:
            return jsonify({"error": "schematic_not_found"}), 500

    # 5. Trigger the build
    # Assuming BuilderBot has a attribute '.bot' which is the Mineflayer instance
    build_from_json(BOT_INSTANCE.bot, validated_data)

    # 6. Return success
    blocks = validated_data.get("blocks", [])
    return jsonify({
        "status": "built",
        "blocks_placed": len(blocks)
    })


if __name__ == "__main__":
    app.run(debug=True)