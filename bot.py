from MeowerBot import Bot
import sys
import os
from details import passwordd
from functions import admin_check
from config import version, license, developer, bot_admins
from messages import help_msg

bot = Bot()

@bot.command(args=0, aname="about")
def about(ctx):
    ctx.send_msg(f"Tabby Version {version}, licensed with the {license} license. Developed by {developer}")

@bot.command(args=0, aname="whoami")
def whoami(ctx):
    if ctx.message.user.username in bot_admins:
        is_bot_admin = "Yes"
    else:
        is_bot_admin = "No"
    ctx.send_msg(f'Username: {ctx.user.username}\nQuote: {ctx.user.quote}\nProfile Picture: {ctx.user.pfp}\nLevel: {ctx.user.level}\nBot Admin?: {is_bot_admin}')

@bot.command(args=0, aname="help")
def help(ctx):
    ctx.send_msg(help_msg)

@bot.command(args=1, aname="give_tempadmin")
def give_tempadmin(ctx, username):
    admin_check(ctx)
    bot_admins.append(username)
    ctx.send_msg(f"User {username} will be a bot admin until next restart!")

@bot.command(args=0, aname="restart")
def restart(ctx):
    admin_check(ctx)
    ctx.send_msg("Restarting...")
    os.execv(sys.executable, ['python3'] + sys.argv)

@bot.command(args=2, aname="config")
def config(ctx, var, val):
    admin_check(ctx)
    ctx.send_msg(f"Changed value of {var} to {val}!")
    var = val

@bot.command(args=1, aname="say")
def say(ctx, msg):
    admin_check(ctx)
    ctx.send_msg(f"{msg}")

@bot.command(args=0, aname="list_admins")
def list_admins(ctx):
    ctx.send_msg(bot_admins)

@bot.command(args=0, aname="spam")
def spam(ctx):
    ctx.send_msg("no.")

@bot.command(args=1, aname="run")
def run(ctx, code):
    admin_check(ctx)
    out = exec(code)
    ctx.send_msg(code)
    print(out)

@bot.command(args=0, aname="stop")
def stop(ctx):
    admin_check(ctx)
    ctx.send_msg("Stopping...")
    os._exit(0)

try:
    bot.run(
        username="Tabby",
        password=passwordd,
        server="wss://server.meower.org"
    )
except KeyboardInterrupt:
    ctx.send_msg("The hoster of the bot has pressed CTRL + C, shutting down!")
    print("Detecting interrupt, going away now...")
    exit()