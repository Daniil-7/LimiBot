import discord
import scripts
from discord.ext import commands


token = "token"

client = commands.Bot(intents=discord.Intents.all(), command_prefix="$")
scripts.Generaldb().create()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


# $help
client.remove_command("help")


@client.command()
async def help(ctx):
    await ctx.send(scripts.text_help)


# $addmemori
@client.command()
async def addmemori(ctx, *, title):
    c_id = ctx.message.channel.id
    u_id = ctx.message.author.name
    s_id = ctx.message.guild.id
    scripts.savememori(title, c_id, u_id, s_id)
    await ctx.send("Сообщение сохранено")


# $delmemori
@client.command()
async def delmemori(ctx, *, index):
    s_id = ctx.message.guild.id
    try:
        await ctx.send(scripts.deletememori(int(index), s_id))
    except Exception:
        await ctx.send("Введите число")


# $memori
@client.command()
async def memori(ctx):
    c_id = ctx.message.channel.id
    out = scripts.loadmemori(c_id, "channel")
    if out[1]:
        await ctx.send(out[0])
    else:
        await ctx.send("Сообщений нет")


# $allmemori
@client.command()
async def allmemori(ctx):
    s_id = ctx.message.guild.id
    out = scripts.loadmemori(s_id, "server")
    if out[1]:
        await ctx.send(out[0])
    else:
        await ctx.send("Сообщений нет")


client.run(token)
