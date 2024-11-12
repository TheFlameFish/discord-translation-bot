# Discord Translation bot

## Purpose:
A translation bot for Discord. It includes a translation command, as well as the ability to translate in response to flag emoji reactions (may be disabled within config).

## Setup:
### Building from source 
---
#### Requirements:
Installed:
* Git
* Docker

---
1. Clone git repository on host machine
2. Create a volume for the docker container
    - The `run` and `runtest` scripts assume you have it named `discord-translation-bot`. If you name it something else and want to use the script, ensure you modify the `-v` parameter accordingly.
3. To build, either run the `run` script or use the command `docker build -t TheFlameFish/discord-translation-bot .`. If you use the `run` script, you can do `ctrl+C` to terminate it.
4. Set up a .env file with the variable `DISCORD_TOKEN`.
5. Set up your host machine to automatically run `docker run --rm --env-file {path to your .env file} -v {your volume's name}:/app/data TheFlameFish/discord-translation-bot`

## Usage:
### Translation
You can use translation with the slash command `/translate {text} {target language}`, or by reacting to a message with a flag emoji.
### Config
You can edit config via slash commands. Configuable stuff includes:
- Permissions
- Whether or not to use reaction-based translations
- The translator module to use (currently only Google translate is available.)