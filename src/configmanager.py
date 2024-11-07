import os
import json
import discord

from src.translation.googletranslator import GoogleTranslator

class ConfigManager:
    valid_translators = {
        "google": lambda: GoogleTranslator()
    }
    
    def __init__(self, config_path="/app/data/config.json", valid_translators: dict=valid_translators):
        self.config_path = config_path
        self.config = {}

        self.valid_translators = valid_translators

        self.initialized = False
        self.load()

    def load(self):
        '''Loads the config from config.json. 
        If config.json does not exist, it will create the file with default values.'''
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                self.config = json.load(f)
        else:
            # Create config.json with default values
            default_config = {
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
            with open(self.config_path, "w") as f:
                json.dump(default_config, f, indent=4)
            self.config = default_config

        self.initialized = True
        print("Config loaded:", self.config)

    def _write(self):
        '''Writes the config object to config.json.'''
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self):
        '''Returns the config object.'''
        if not self.initialized:
            self.load()
        return self.config

    def get_key(self, key):
        '''Returns the value of a key in the config object.'''
        if not self.initialized:
            self.load()
        return self.config.get(key)

    def set(self, key, value):
        '''Sets a key in the config object to a given value.'''
        if not self.initialized:
            self.load()
        self.config[key] = value
        self._write()

    def add_permission(self, role, permission):
        '''Gives a role a permission.'''
        if not self.initialized:
            self.load()
        self.config["permissions"][permission][role] = True
        self._write()

    def remove_permission(self, role, permission):
        '''Removes a permission from a role.'''
        if not self.initialized:
            self.load()
        if role in self.config["permissions"][permission]:
            del self.config["permissions"][permission][role]
            self._write()

    def get_roles(self, user: discord.Member):
        '''Gets the roles of a member.'''
        if not self.initialized:
            self.load()
        return [role.name for role in user.roles]

    def has_permission(self, user: discord.Member, permission):
        '''Checks if a user has a permission.'''
        if not self.initialized:
            self.load()
        roles = self.get_roles(user)
        for role in roles:
            if self.config["permissions"].get(permission, {}).get(role, False):
                return True
        return False
    
    def get_permissions(self, user: discord.Member):
        '''Returns the permissions of a user.'''
        if not self.initialized:
            self.load()
        roles = self.get_roles(user)
        permissions = {}
        for permission in self.config["permissions"]:
            for role in roles:
                if self.config["permissions"][permission].get(role, False):
                    permissions[permission] = True
        return permissions
