import asyncio, discord, signal,threading, os
import tkinter as tk
import keyboard as kb
from discord.ext import commands
from tkinter import messagebox, StringVar, ttk
from tkinter.scrolledtext import ScrolledText

TOKEN = os.getenv(DISCORD_TOKEN)
# Initialize Discord bot
intent = discord.Intents.all()
bot = commands.Bot(intents=intent, command_prefix="!")

# Tkinter GUI

# Button view for restoring permissions
class RestorePermissionsButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Restaurar permissões", style=discord.ButtonStyle.green)
    async def restore_permissions(self,interaction: discord.Interaction, button: discord.ui.Button):

        member = interaction.guild.get_member(716390085896962058)
        role = member.roles[1]
        if role:
            role = member.roles[1]  # Assuming the first role is the main role
            SendMsg = role.permissions
            SendMsg.update(send_messages=True)
            await role.edit(permissions=SendMsg)
        
        try:
            await interaction.response.send_message(f"Permissões restauradas para {member.mention}!", ephemeral=True)
        except NameError:
            await interaction.response.send_message("Membro não encontrado ou já liberado.", ephemeral=True)


# Discord bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
   

@bot.event
async def on_message(message):
    guild = bot.get_guild(1267322342577537147)

    cont = message.content
    Aname = message.author.name
    AId = message.author.id
    Cname = message.channel.name
    CId = message.channel.id

    print(f'==================================\nLog: \n{cont} \n{Aname} | {AId} \n{Cname} | {CId}\n==================================')

    if message.author.id == 854233015475109888:
        member = await guild.fetch_member(716390085896962058)     
        role = member.roles[1]
        print(role)
        if role:
            # Remove send messages permission
            NoMsgissions = role.permissions
            NoMsgissions.update(send_messages=False)
            await role.edit(permissions=NoMsgissions)

            # Send a message to the channel with a button to restore permissions
            await message.channel.send(
                f"-# || <@&{1299199288957468752}> ||,\n\n Um pokémon raro spawnou e o Pokétwo foi silenciado para a captura. Após pegar, certifique-se de apertar o botão para liberar o pokétwo novamente.\n\n Att., Mod",
                view=RestorePermissionsButton()
            )

# Discord bot Listener
@bot.listen('on_message')
async def my_message(ctx):
    if ctx.author == bot.user:
        return
    else:
        msg = input()
        await ctx.reply(msg)

bot.run(TOKEN)
