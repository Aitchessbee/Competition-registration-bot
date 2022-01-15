
# variables user has to enter --> link, server id, Dictionary(teamcode: role id)


import discord
from discord.ext import commands
import urllib.parse as up
import psycopg2

up.uses_netloc.append("postgres")
url = up.urlparse("link")  # Enter link here
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

c = conn.cursor()

# sample dictionary with team code, and role id as key and value.
D = {'7529': 743772476521185290, '7880': 743776462682980422, '9741': 743782057104375859, '3187': 743781004971343892, '8258': 743772425229041757, '5384': 743782288684351549, '6122': 743782364320235561, '2153': 743782421048328313, '8443': 743782451393986652, '6319': 743782457589104660, '1387': 743782460688433173, '4803': 743782463675039844, '7697': 743782466405400619, '3228': 743782469857181778, '4619': 743782472625553448, '6118': 743782474575773717, '5474': 745490760308359230, '4009': 745490856936734800, '5670': 745490912905265193, '5369': 745490964914765904, '8294': 745491013715623936, '9426': 745491065221414923, '2326': 745491110079627405, '7101': 745491141159551047, '7835': 745491239994130563, '8267': 745491277159596143, '2769': 745491310298791949, '5694': 745491342859173928, '1780': 745491379245023332, '7789': 745491414841819277, '1151': 745491453001596980, '5385': 745491487927828530}

client = commands.Bot(command_prefix = "!")

@client.command(pass_context=True)
async def register(ctx, msg1, msg2):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        try:
            if msg2 in D:
                c.execute(f"select disc_name from players where team_id = '{msg2}'")
                player = c.fetchall()
                cond = False
                for i in player:
                    if i[0] == str(ctx.author):
                        cond = True
                        break
                if cond == False:    
                    if len(player) < 5:
                        c.execute(f"INSERT INTO Players(disc_name, Ingame_name, team_id) VALUES('{ctx.author}','{msg1}', '{msg2}');")
                        conn.commit()
                        await ctx.author.send("Registration successful")
                        
                        target_server_id = SERVER_ID  # Enter server id here
                        target_role_id = D[msg2]
                        target_server = client.get_guild(target_server_id)
                        author_id = ctx.author.id
                        try:
                            member = target_server.get_member(author_id)
                        except:
                            await ctx.author.send(f"You are not a member of the {target_server.name}.")
                        role_name = discord.utils.get(target_server.roles, id=target_role_id)
                        await member.add_roles(role_name)
                        await ctx.author.send("Voice channel joined")
                        return
                    else:
                        await ctx.author.send("You can register maximum 5 players from a team")
                else:
                    await ctx.author.send("You can only register once")
            else:
                await ctx.author.send("Use a valid team code")
        except:
            pass

client.run('token')
