import discord
import requests
from discord.ext import commands, tasks

# Discord Bot Token
DISCORD_TOKEN = 'OTIyMTk0NDk0ODE0ODIyNDgw.GU5zO4.y9-KUlVXOyxm6uN__0oB5-Coqq8KxwJjUmJoMU'

# Pterodactyl API URL and Token
PTERO_API_URL = 'https://ronbohosting.ddns.net/admin/api'
PTERO_API_TOKEN = 'ptla_mxumziwihmo3arNUg4VrXZiOpqRguP9U92mTZAi71sF'

# Discord Channel ID for Alerts
CHANNEL_ID = '1190726246062100643'

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guilds = True

# Create a bot instance with specified intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Store DDoS status globally
ddos_status = "No DDoS activity detected."


# Function to send an alert to Discord
async def send_discord_alert(message):
  channel = bot.get_channel(int(CHANNEL_ID))
  await channel.send(message)


# Function to send a power command to the Pterodactyl panel
def send_ptero_command(command):
  headers = {'Authorization': f'Bearer {PTERO_API_TOKEN}'}
  requests.post(PTERO_API_URL, headers=headers, json={'signal': command})


# Function to update the DDoS status
@tasks.loop(minutes=5)
async def update_ddos_status():
  global ddos_status
  # Add your logic to check DDoS status and update ddos_status accordingly
  # For example, you might query logs or other indicators
  ddos_status = "No DDoS activity detected."


# Command to check the DDoS status
@bot.command(name='ddosstatus')
async def ddos_status_command(ctx):
  embed = discord.Embed(title="DDoS Status",
                        description=ddos_status,
                        color=0x00ff00)
  await ctx.send(embed=embed)


# Command to simulate a fake attack
@bot.command(name='test')
async def test_attack(ctx):
  await ctx.send('Simulating a fake attack!')
  # You can add your logic here to simulate an attack or trigger the Pterodactyl panel


# Event listener for when the bot is ready
@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user.name}')
  update_ddos_status.start(
  )  # Start the loop to periodically update DDoS status


# Run the bot
bot.run(DISCORD_TOKEN)
