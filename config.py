import os
import json
import discord

config = {
    "permissions": {
        "use_translation": {
            "@everyone": True
        },

        "config.read": {
            "@everyone": True
        },
        "config.general_write": {
            "@everyone": True
        },
        "config.manage_perms": {
            "@everyone": True
        },
    },
    "reaction_translations": True
}

initialized = False
def load():
    '''Loads the config from config.json. 
    If config.json does not exist, it will create the file with default values.
    
    This function should be called whenever the config is needed to be accessed.'''
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
    print("Config loaded. Config: ", config)

def _write():
    '''Writes the config object to config.json.'''
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get():
    '''Returns the config object.'''
    load()
    return config

def get_key(key):
    '''Returns the value of a key in the config object.'''
    load()
    return config[key]

def set(key, value):
    '''Sets a key in the config object to a given value.'''
    load()
    config[key] = value

    _write()

def add_permission(role, permission):
    '''Gives a role a permission.'''
    load()
    config["permissions"][permission][role] = True

    _write()

def remove_permission(role, permission):
    '''Removes a permission from a role.'''
    load()
    if role in config["permissions"][permission]:
        del config["permissions"][permission][role]

        _write()

def get_roles(user: discord.Member): # Maybe move this elsewhere. It's not really config-related.
    '''Gets the roles of a member.'''
    load()
    return [role.name for role in user.roles]

def has_permission(user: discord.Member, permission):
    '''Checks if a user has a permission.'''
    print("Checking permission for user ", user.display_name)
    load()
    roles = get_roles(user)
    for role in roles:
        if config["permissions"].get(permission, {}).get(role, False):
            return True
        else:
            print("Role ", role, " does not have permission ", permission)
    return False