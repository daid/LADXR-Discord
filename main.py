import discord
import discord.ext.commands
from discord import ui
import random


intents = discord.Intents.default()
intents.message_content = True

client = discord.ext.commands.Bot(command_prefix='$', intents=intents)


puzzles = [
    ("Keyblock", "Small Key"),
    ("Nightmare Door", "Nightmare Key"),
    ("Pit/Hole", "Feather"),
    ("Rock", "Power Bracelet"),
    ("Cracked Wall", "Bomb"),
    ("Moblin", "Sword"),
    ("Shop", "Rupees"),
]


class Questionnaire(ui.Modal, title='Entry Puzzle. You should know this.'):
    def __init__(self):
        super().__init__()
        self.questions = []
        for n in range(3):
            q, a = random.choice(puzzles)
            idx = 1
            if random.random() < 0.5:
                q, a, idx = a, q, 0
            opts = [n[idx] for n in puzzles if n[idx] != a]
            random.shuffle(opts)
            opts = opts[:3] + [a]
            random.shuffle(opts)
            self.questions.append((q, a, opts))

        self.selects = []
        for q, a, opts in self.questions:
            self.selects.append(ui.Select(options=[discord.SelectOption(label=o) for o in opts]))
            self.add_item(ui.Label(text=q, component=self.selects[-1]))

    async def on_submit(self, interaction: discord.Interaction):
        ok = True
        for (q, a, opts), select in zip(self.questions, self.selects):
            if len(select.values) != 1 or a != select.values[0]:
                ok = False
        print(f"{interaction.user}: {self.questions} = {[s.values[0] for s in self.selects]}")
        if ok:
            role = discord.utils.get(interaction.guild.roles, name='Awakened')
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Thanks for your response. Access has been granted.', ephemeral=True)
        else:
            await interaction.response.send_message('Sorry, that was wrong.', ephemeral=True)


class DoorKeeper(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start puzzle...', style=discord.ButtonStyle.green)
    async def start_test(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Questionnaire())


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == "wake-the-fish":
                print(repr(guild), repr(channel))
                async for message in channel.history():
                    await message.delete()
                await channel.send("Welcome. Due to Discord unable to handle the spam problem. We do not like that we have to do this, as we like to be open and inclusive. But we now require you to solve this puzzle before you can enter. If you encounter any problems, send a private message to Daid.", view=DoorKeeper())

@client.hybrid_command(description="Use this to give yourself the Rando Racer role, so you get pinged when there are races happening")
async def irace(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Rando Racer')
    await ctx.author.add_roles(role)
    await ctx.send('Your wish is my command.')

@client.hybrid_command(description="Use this to take away the Rando Racer role")
async def inorace(ctx):
    await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name='Rando Racer'))
    await ctx.send('Your wish is my command.')

client.run(open("token.txt", "rt").read().strip())
