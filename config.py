import os
import json
import discord

config = {
    "permissions": {
        "use_translation": {
            "everyone": True
        }
    }
}

initialized = False
def init():
    if os.path.exists("config.json"):
        global config
        with open("config.json") as f:
            config = json.load(f)
    else:
        # Create config.json with default values
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

    global initialized
    initialized = True
    print("Config initialized. Config: ", config)

def _write():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get():
    if not initialized:
        init()
    return config

def set(key, value):
    if not initialized:
        init()
    config[key] = value

    _write()

def add_permission(role, permission):
    if not initialized:
        init()
    config["permissions"][permission][role] = True

    _write()

def remove_permission(role, permission):
    if not initialized:
        init()
    if role in config["permissions"][permission]:
        del config["permissions"][permission][role]

        _write()

def get_roles(user: discord.Member):
    if not initialized:
        init()
    return [role.name for role in user.roles]

def has_permission(user: discord.Member, permission):
    print("Checking permission for user ", user.display_name)
    if not initialized:
        init()
    roles = get_roles(user)
    for role in roles:
        if config["permissions"].get(permission, {}).get(role, False):
            return True
    return False