import discord
import mysql.connector
import os

mysql = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_DATABASE'),
    port=3306
)

from http.server import BaseHTTPRequestHandler
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world! Discord Bot'.encode('utf-8'))
        run_discord_bot()
        return

    async def send_message(message, server_name):
        try:
            await message.channel.send(f'Hello World {server_name}')
        except Exception as e:
            print(e)
    
    
    def run_discord_bot():
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT `token` FROM `auth_tokens` WHERE bot_id=%s", ((os.environ.get('BOT_ID')),))
        bot_token = cursor.fetchone()
        cursor.close()
    
        TOKEN = bot_token['token']
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
    
        @client.event
        async def on_ready():
            print(f'{client.user} is now running!')
    
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
    
            server_name = message.author.guild.name
    
            if client.user.mentioned_in(message):
                await send_message(message, server_name)
    
        client.run(TOKEN)
