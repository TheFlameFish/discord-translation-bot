LABEL org.opencontainers.image.source=https://github.com/TheFlameFish/discord-translation-bot 
LABEL org.opencontainers.image.description="A Discord bot for translation."
LABEL org.opencontainers.image.licenses=GNU General Public License v3.0


FROM python:3.12.7

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]