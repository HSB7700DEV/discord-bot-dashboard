import discord
from discord import Forbidden, HTTPException
from discord.ui import Button, View
from discord.commands.options import Option
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions

bot = discord.Bot()

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = True

TOKEN = "YOUR_BOT_TOKEN"

@bot.event
async def on_ready():
    print("Online")

@bot.slash_command(name="botdashboard", description="This is owner's dashboard.")
async def botdashboard(ctx:discord.ApplicationContext, ephemeral:bool):
    if ctx.user.id == "YOUR_USER_ID":
        listGuild = []
        for guild in bot.guilds:
            listGuild.append(f"{guild.name}: {guild.member_count} members\n")

        main = Button(label="Show status", style=discord.ButtonStyle.blurple)
        close = Button(label="Close", style=discord.ButtonStyle.red)
        back = Button(label="Back", style=discord.ButtonStyle.gray)
        guilds = Button(label="Guilds detail", style=discord.ButtonStyle.blurple)

        embedStart = discord.Embed(title="Your bot Dashboard", description=f"Choose one of the options to continue...\nPing: {round(bot.latency * 1000)}ms", color=0xffffff)
        viewStart= View()
        viewStart.add_item(main)
        viewStart.add_item(close)

        embedMain = discord.Embed(title="Your bot Status", description=f"Ping is {round(bot.latency * 1000)}ms\nProviding service to **{len(bot.guilds)}** guilds", color=0xffffff)
        viewMain = View()
        viewMain.add_item(guilds)
        viewMain.add_item(back)

        embedGuilds = discord.Embed(title="Servers running with your bot", description=f"{''.join(map(str, listGuild))}", color=0xffffff)
        viewGuilds = View()
        viewGuilds.add_item(back)
        viewGuilds.add_item(close)

        async def main_callback(interaction):
            await interaction.response.edit_message(embed=embedMain, view=viewMain)

        async def close_callback(interaction):
            if ephemeral == True:
                embedStart.set_footer(text="Ephemeral is true!")
                await interaction.response.edit_message(embed=embedStart, view=viewStart)
            else:
                await interaction.message.delete()

        async def back_callback(interaction):
            await interaction.response.edit_message(embed=embedStart, view=viewStart)

        async def guilds_callback(interaction):
            await interaction.response.edit_message(embed=embedGuilds, view=viewGuilds)
        
        main.callback = main_callback
        close.callback = close_callback
        back.callback = back_callback
        guilds.callback = guilds_callback


        await ctx.respond(embed=embedStart, view=viewStart, ephemeral=ephemeral)

    else:
        await ctx.respond(embed=PermissionErrUser, ephemeral=True)

bot.run(TOKEN)