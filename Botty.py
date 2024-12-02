import discord
from discord.ext import commands
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

#Load enviornment variable from .env file
load_dotenv("token.env")


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

#Retrieve EC2 metadata
region = None
availability_zone = None
ip_address = None
try:
    ip_address = ec2_metadata.public_ipv4 or ec2_metadata.private_ipv4
    region = ec2_metadata.region
    availability_zone = ec2_metadata.availability_zone
except Exception as e:
    ip_address = "ip"
    region = "region"
    availability_zone = "zone"

#Initialize Dicord Client
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=intents)

#Define command to respond to "ping"
@client.command() 
async def ping(ctx): 
    await ctx.send('Pong!') 

#Retrive bot token from env variables
token = os.getenv('TOKEN')

#Display event handler when the bot is ready
@client.event 
async def on_ready(): 
	print("Logged in as a bot {0.user}".format(client))
	print(f'Your EC2 Data are as follows: IP Address: {ip_address}, Region: {region}, Availability Zone: {availability_zone}')

#Event handler when a message is received
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}') 

    if channel == "random":
        print(f'Message {user_message}')
        if user_message.lower() == "hello" or user_message.lower() == "hi": 
            await message.channel.send(f'Hello {username}') 
            return
        
        elif user_message.lower() == "bye": 
            await message.channel.send(f'Bye {username}')
            return
         
        elif user_message.lower() == "tell me a joke": 
            jokes = ["Why don't skeletons fight each other? They don't have the guts!","Why don't eggs tell jokes? They might crack up!","How does a penguin build its house? Igloos it together!"] 
            await message.channel.send(random.choice(jokes))
            return
        
        elif user_message.lower() == "ip":
            await message.channel.send(f'Your public ip is {ip_address}')
            return
        
        elif user_message.lower() == "zone":
            await message.channel.send(f'Your availbility zone is {availability_zone}')
            return
        
        elif user_message.lower() == "tell me about my server":
            await message.channel.send(f'Your EC2 region is {region}, Your public ip is {ip_address}, Your availbility zone is {availability_zone} ')
            return

client.run(token)