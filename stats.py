import aiohttp
import json

from discord.ext import commands

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def games(self, ctx, *args):
        message = 'Invalid syntax. ?games <year> <school>'
        if len(args) <= 1:
            await ctx.send(message)
            return

        year = args[0]

        try:
            int(year)
        except ValueError:
            await ctx.send(message)
            return

        team = ' '.join(args[1:])

        url = f'https://api.collegefootballdata.com/games?year={year}&seasonType=regular&team={team}'

        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            if not response or len(response) is 0:
                message = 'No results.'
                await ctx.send(message)
                return
            else:
                message = f'**{team} in {year} (Regular season)**:\n'
                for value in response:
                    away_team = value['away_team']
                    home_team = value['home_team']
                    is_home_team = team.lower() == home_team.lower()
                    print_team = away_team if is_home_team else home_team
                    home_points = value['home_points']
                    away_points = value['away_points']
                    is_home_win = int(home_points) > int(away_points)
                    print_away_points = ('**' if not is_home_team else '') + str(value['away_points']) + ('**' if not is_home_team else '')
                    print_home_points = ('**' if is_home_team else '') + str(value['home_points']) + ('**' if is_home_team else '')
                    print_result = ('**WIN**' if ((is_home_team and is_home_win) or (not is_home_team and not is_home_win)) else 'LOSS') 

                    message += f'Week {value["week"]}: {print_result} {"vs." if is_home_team else "@"} {print_team}: {print_away_points} - {print_home_points}\n'

            await ctx.send(message)

        url = f'https://api.collegefootballdata.com/games?year={year}&seasonType=postseason&team={team}'

        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            if not response or len(response) is 0:
                message = ''
                return
            else:
                message = f'**{team} in {year} (Post season)**:\n'
                for value in response:
                    away_team = value['away_team']
                    home_team = value['home_team']
                    is_home_team = team.lower() == home_team.lower()
                    print_team = away_team if is_home_team else home_team
                    home_points = value['home_points']
                    away_points = value['away_points']
                    is_home_win = int(home_points) > int(away_points)
                    print_away_points = ('**' if not is_home_team else '') + str(value['away_points']) + ('**' if not is_home_team else '')
                    print_home_points = ('**' if is_home_team else '') + str(value['home_points']) + ('**' if is_home_team else '')
                    print_result = ('**WIN**' if ((is_home_team and is_home_win) or (not is_home_team and not is_home_win)) else 'LOSS') 

                    message += f'Week {value["week"]}: {print_result} {"vs." if is_home_team else "@"} {print_team}: {print_away_points} - {print_home_points}\n'

            await ctx.send(message)
