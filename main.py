import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from gtm_model import get_class

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user}')

@bot.command
async def photo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith('.jpg') or \
            attachment.filename.endswith('.jpeg') or \
            attachment.filename.endswith('.png'):
                image_path = f'./images/{attachment.filename}'
                attachment.save(image_path)
                temp_msg = await ctx.send('Обработка изображения...')
                
                class_name, score = get_class(image_path, 'gtm_model/keras_model.h5', 'gtm_model/labels.txt')

                await temp_msg.delete()
                await ctx.send(f'{class_name} с вероятностью {score}')                              
                os.remove(image_path)


            else:
                await ctx.send('👉 .jpg / .jpeg / .png')
                return
    else:
        await ctx.send('нет')


bot.run(TOKEN)
