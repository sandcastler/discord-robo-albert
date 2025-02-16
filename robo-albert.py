import configparser

import recruiting
import stats

from discord.ext import commands

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['default']['token']

bot = commands.Bot(command_prefix='?')
bot.add_cog(recruiting.Recruiting(bot))
bot.add_cog(stats.Stats(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)
