import discord
import discord.ext.commands


intents = discord.Intents.default()
intents.message_content = True

client = discord.ext.commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

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
