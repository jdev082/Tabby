from MeowerBot import Bot
import sys
import random
import os
import platform
from details import passwordd
from functions import admin_check, home_check, is_disabled
from config import license, developer, bot_admins, repo, cat_breeds, quotes
from messages import help_msg

version = open('release.txt', 'r').read()

if os.name == "nt":
    name = "Windows NT"
elif os.name == "posix":
    name = "Linux"
release = platform.release()
relver = platform.version()

with open("bot.py", 'r') as fp:
    lines_count = len(fp.readlines())

bot = Bot(autoreload=0)

@bot.command(args=0, aname="about")
def about(ctx):
    ctx.send_msg(f"Tabby Version {version}, licensed with the {license} license. Developed by {developer}! You can contribute at {repo}.")

@bot.command(args=1, aname="setver")
def setver(ctx, ver):
    admin_check(ctx)
    os.remove('release.txt')
    f = open("release.txt", "w")
    f.write(ver)
    f.close()
    ctx.send_msg(f"Version bumped to {ver}! This change will be applied when I am restarted.")

@bot.command(args=0, aname="lines")
def lines(ctx):
    ctx.send_msg(f"I have {lines_count} lines of code!")

@bot.command(args=0, aname="system")
def system(ctx):
    ctx.send_msg(f"I am running on {name} {relver}!")

@bot.command(args=0, aname="whoami")
def whoami(ctx):
    if ctx.message.user.username in bot_admins:
        is_bot_admin = "Yes"
    else:
        is_bot_admin = "No"
    ctx.send_msg(f'Username: {ctx.user.username}\nQuote: {ctx.user.quote}\nProfile Picture: {ctx.user.pfp}\nLevel: {ctx.user.level}\nBot Admin?: {is_bot_admin}')

@bot.command(args=0, aname="cat")
def cat(ctx):
    home_check(ctx)
    ctx.send_msg(random.choice(cat_breeds))

@bot.command(args=1, aname="link")
def link(ctx, link):
    #if link == "discord":
    #    ctx.send_msg("https://dsc.gg/meowermedia")
    if link == "forums":
        ctx.send_msg("https://forums.meower.org")
    elif link == "wiki":
        ctx.send_msg("https://wiki.meower.org")
    elif link == "legal":
        ctx.send_msg("https://meower.org/legal")
    elif link == "website":
        ctx.send_msg("https://meower.org")
    else:
        ctx.send_msg("available links: forums, wiki, legal, website")
    

@bot.command(args=0, aname="help")
def help(ctx):
    ctx.send_msg(help_msg)

@bot.command(args=1, aname="give_tempadmin")
def give_tempadmin(ctx, username):
    admin_check(ctx)
    if username == "*":
        for x in bot.wss.statedata["ulist"]["usernames"]:
            bot_admins.append(x)
            ctx.send_msg("All users have been given bot admin!")
            exit()
    if username in bot_admins:
        ctx.send_msg(f"User {username} is already a bot admin!")
        exit()
    if "Tabby" in username:
        ctx.send_msg("You cannot give Tabby admin permissions!")
        exit()
    bot_admins.append(username)
    ctx.send_msg(f"User {username} will be a bot admin until next restart!")

@bot.command(args=2, aname="conf")
def conf(ctx, conf, val):
    admin_check(ctx)
    if conf == "developer":
        developer = val
    else:
        ctx.send_msg("Error, invalid config parameter.")
        exit()
    ctx.send_msg(f"Value {conf} set to {val}!")

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

@bot.command(args=2, aname="say")
def say(ctx, msg, byp="none"):
    is_disabled(ctx)
    if byp != "hm":
        admin_check(ctx)
        home_check(ctx)
    if "@" in msg and byp != "at":
        ctx.send_msg("Disallowed character: @!")
        exit()
    if byp == "at":
        admin_check(ctx)
    ctx.send_msg(f"{msg}")

@bot.command(args=0, aname="list")
def list(ctx):
    list_array = bot.wss.statedata["ulist"]["usernames"]
    list_array_string = str(list_array)
    list_array_nolbr = list_array_string.replace('[', '')
    list_array_norbr = list_array_nolbr.replace(']', '')
    list_array_noquo = list_array_norbr.replace("'", "")
    ctx.send_msg(f"online: {list_array_noquo}")

@bot.command(args=0, aname="list_admins")
def list_admins(ctx):
    ctx.send_msg(bot_admins)

@bot.command(args=0, aname="spam")
def spam(ctx):
    ctx.send_msg("no.")

@bot.command(args=1, aname="run")
def run(ctx, code):
    admin_check(ctx)
    ctx.send_msg(str(exec(code)))

@bot.command(args=0, aname="quote")
def quote(ctx):
    home_check(ctx)
    ctx.send_msg(random.choice(quotes))

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
    print("Detecting interrupt, going away now...")
    exit()