import discord
from discord.ext import commands
import mysql.connector
import os

mysql = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_DATABASE'),
    port=3306
)

intents = discord.Intents.default()
intents.message_content = True
app = commands.Bot(command_prefix='!', intents=intents)


@app.event
async def on_ready():
    print(f'{app.user} is now running!')


@app.event
async def on_message(message):
    if message.author == app.user:
        return

    server_name = message.author.guild.name

    if app.user.mentioned_in(message):
        await send_message(message, server_name)


async def send_message(message, server_name):
    try:
        await message.channel.send(f'Hello World {server_name}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT `token` FROM `auth_tokens` WHERE bot_id=%s", ((os.environ.get('BOT_ID')),))
    bot_token = cursor.fetchone()
    cursor.close()

    TOKEN = bot_token['token']

    app.run(TOKEN)
