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
class DiscordApp:
    def __init__(self, root):
        self.root = root
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.title("Discord Message Sender")

        ttk.Label(root, text="Digite sua mensagem: ", font=("Bold", 12), relief="raised").grid(row=1, column=3)

        self.text_area = ScrolledText(root, wrap=tk.WORD, width=45, height=9, font=("Times New Roman", 11))
        self.text_area.grid(row=3, column=3, pady=5)

        self.channel_var = StringVar(root, value="Selecione o Canal: ")
        self.channel_menu = tk.OptionMenu(root, self.channel_var, "")
        self.channel_menu.grid(row=0, column=3, pady=3)

        self.send_button = tk.Button(root, text="Enviar mensagem", command=self.on_send_message, bg='green4', relief="raised")
        self.send_button.grid(row=4, column=3, pady=3)

        self.close_button = tk.Button(root, text="Fechar", command=self.on_close, bg='red2', relief="raised")
        self.close_button.grid(row=5, column=3, pady=5, padx=5)

        self.fetch_button = tk.Button(root, text="Fetch Last Message", command=self.fetch_last_message)
        self.fetch_button.grid(row=6, column=3, pady=10)

        self.reply_var = StringVar(value="No")
        self.reply_radio_yes = tk.Radiobutton(root, text="Reply", variable=self.reply_var, value="Yes")
        self.reply_radio_no = tk.Radiobutton(root, text="Not a Reply", variable=self.reply_var, value="No")
        self.reply_radio_yes.grid(row=7, column=3, sticky='w')
        self.reply_radio_no.grid(row=8, column=3, sticky='w')


    async def populate_channel_dropdown(self):
        channel_ids = await self.fetch_channel_ids(1267322342577537147)
        self.channel_menu['menu'].delete(0, 'end')

        for channel_id, channel_name in sorted(channel_ids, key=lambda x: x[1]):
            self.channel_menu['menu'].add_command(label=channel_name, command=lambda value=channel_id: self.channel_var.set(value))

    async def fetch_channel_ids(self, guild_id):
        guild = bot.get_guild(guild_id)
        if guild:
            return [(channel.id, channel.name) for channel in guild.channels if isinstance(channel, discord.TextChannel)]
        return []

    async def update_last_message(self, channel_id):
        channel = bot.get_channel(channel_id)
        if channel:
            messages = await channel.history(limit=1).flatten()
            last_message = messages[0] if messages else None
            if last_message:
                messagebox.showinfo("Last Message", last_message.content)
            else:
                messagebox.showinfo("Last Message", "No messages found.")

    def fetch_last_message(self):
        selected_channel = self.channel_var.get()
        if selected_channel != "Selecione o Canal: ":
            channel_id = int(selected_channel)  # Convert to int
            asyncio.run_coroutine_threadsafe(self.update_last_message(channel_id), bot.loop)
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione um canal.")

    async def send_message_to_discord(self, message, channel_id):
        channel = bot.get_channel(channel_id)
        if channel:
            if self.reply_var.get() == 'Yes':
                await channel.send(f"Replying: {message}")
            else:
                await channel.send(message)

    def on_send_message(self):
        selected_channel = self.channel_var.get()
        message = self.text_area.get("1.0", tk.END).strip()
        if message and selected_channel != "Selecione o Canal: ":
            channel_id = int(selected_channel)  # Convert to int
            asyncio.run_coroutine_threadsafe(self.send_message_to_discord(message, channel_id), bot.loop)
            self.text_area.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Aviso", "Mensagem não pode estar vazia ou canal sem seleção!")

    def on_close(self, event=None):
        bot.loop.stop()
        self.root.destroy()


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
    # Populate the channel dropdown when the bot is ready
    await app.populate_channel_dropdown()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordApp(root)

    # Run the Discord bot in a separate thread
    def run_bot():
        bot.run(TOKEN)

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    root.mainloop()
