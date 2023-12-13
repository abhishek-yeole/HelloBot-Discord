import discord
from discord.ext import commands
import mysql.connector
import os
from flask import Flask

app = Flask(__name__)

mysql = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_DATABASE'),
    port=3306
)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    server_name = message.author.guild.name

    if bot.user.mentioned_in(message):
        await send_message(message, server_name)


async def send_message(message, server_name):
    try:
        await message.channel.send(f'Hello World {server_name}')
    except Exception as e:
        print(e)


# Flask route for health check or any other purposes
@app.route('/')
def home():
    return "Discord Bot is running!"


def run_discord_bot():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT `token` FROM `auth_tokens` WHERE bot_id=%s", ((os.environ.get('BOT_ID')),))
    bot_token = cursor.fetchone()
    cursor.close()

    TOKEN = bot_token['token']

    bot.run(TOKEN)


if __name__ == '__main__':
    # Run the Flask application alongside the Discord bot
    app.run(debug=True, host='0.0.0.0')

    # Run the Discord bot
    run_discord_bot()
