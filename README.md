# Discord Translation bot

## Purpose:
A translation bot for Discord. It includes a translation command, as well as the ability to translate in response to flag emoji reactions (may be disabled within config).

## Setup:
---
#### Requirements:
Installed:
* Python 3 & Pip
* Git

---
1. Clone git repository on host machine
2. (Sort of optional) Create and activate a virtualenv
3. Pip Install:
    - py-cord
    - deep-translator
4. Create a .env file in the project's root directory. Add your discord bot's token for the variable `DISCORD_TOKEN`.
5. Run main.py (you'll probably want to have it automatically run)

## Usage:
### Translation
You can use translation with the slash command `/translate {text} {target language}`, or by reacting to a message with a flag emoji.
### Config
You can edit config via slash commands. Configuable stuff includes:
- Permissions
- Whether or not to use reaction-based translations
- The translator module to use (currently only Google translate is available.)