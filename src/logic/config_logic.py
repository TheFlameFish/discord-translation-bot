import json
import logging
from typing import Optional

class ConfigLogic:
    def __init__(self, config, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def _check_permission(self, user, permission_key) -> Optional[str]:
        if not self.config.has_permission(user, permission_key):
            self.logger.info(f"User '{user}' does not have permission '{permission_key}'.")
            return "You do not have the required permission."
        return None

    def list_config(self, user) -> str:
        permission_error = self._check_permission(user, "config.read")
        if permission_error:
            return permission_error
        self.logger.info("List command triggered.")
        return f"# Config:\n{json.dumps(self.config.get(), indent=4)}"

    def get_permissions_for_user(self, user, target_user) -> str:
        permission_error = self._check_permission(user, "config.read")
        if permission_error:
            return permission_error
        self.logger.info("Check permissions command triggered.")
        return f"# Permissions for user '{target_user.name}':\n{json.dumps(self.config.get_permissions(target_user), indent=4)}"

    def add_permission(self, user, role_name: str, permission: str) -> str:
        permission_error = self._check_permission(user, "config.manage_perms")
        if permission_error:
            return permission_error
        self.logger.info("Add permission command triggered.")
        try:
            self.config.add_permission(role_name, permission)
            return f"Added permission '{permission}' to role '{role_name}'."
        except KeyError:
            return f"Permission '{permission}' does not exist."

    def remove_permission(self, user, role_name: str, permission: str) -> str:
        permission_error = self._check_permission(user, "config.manage_perms")
        if permission_error:
            return permission_error
        self.logger.info("Remove permission command triggered.")
        try:
            self.config.remove_permission(role_name, permission)
            return f"Removed permission '{permission}' from role '{role_name}'."
        except KeyError:
            return f"Permission '{permission}' does not exist."

    def set_reaction_translations(self, user, value: bool) -> str:
        permission_error = self._check_permission(user, "config.general_write")
        if permission_error:
            return permission_error
        self.logger.info("Set reaction translations command triggered.")
        self.config.set("reaction_translations", value)
        return f"Set reaction translations to '{value}'."

    def set_translator(self, user, translator_name: str) -> str:
        permission_error = self._check_permission(user, "config.general_write")
        if permission_error:
            return permission_error
        self.logger.info("Set translator command triggered.")
        if translator_name in self.config.valid_translators:
            self.config.set("translator", translator_name)
            return f"Set translator to '{translator_name}'."
        return f"Invalid translator '{translator_name}'.\nValid translators are: {self.config.valid_translators}"
