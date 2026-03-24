from bot.models import MinecraftBuild

def place_block(bot, block_type, x, y, z, direction=False):
    valid_directions = {"north", "south", "east", "west"}

    # Check if direction is a valid facing direction
    if direction in valid_directions:
        # Format the /setblock command with the facing property
        # Example: /setblock 10 64 10 oak_stairs[facing=north]
        command = f"/setblock {x} {y} {z} {block_type}[facing={direction}]"
    else:
        # Format the /setblock command without a facing property
        # Example: /setblock 10 64 10 stone
        command = f"/setblock {x} {y} {z} {block_type}"

    # Send the command to Minecraft via the bot
    bot.chat(command)

def build_from_json(bot, json_data):
    # Safety check: Ensure the bot is spawned and has a position
    if not bot.entity or not bot.entity.position:
        print("Error: Bot position not found. Is the bot spawned?")
        return

    pos = bot.entity.position
    base_x = int(pos.x) 
    base_y = int(pos.y)
    base_z = int(pos.z)

    # Parse the JSON data into a MinecraftBuild instance
    # This uses Pydantic to make sure the AI sent valid data
    minecraft_build = MinecraftBuild.model_validate(json_data)

    for block in minecraft_build.blocks:
        # Check for a 'facing' attribute, default to False if it doesn't exist
        direction = getattr(block, "facing", False)
        
        place_block(
            bot,
            block.block_type,
            block.x + base_x,
            block.y + base_y,
            block.z + base_z,
            direction,
        )