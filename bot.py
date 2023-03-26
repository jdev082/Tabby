from MeowerBot import Bot
import sys
import random
import os
import platform
from details import passwordd
from functions import admin_check, home_check, is_disabled
from config import license, developer, bot_admins, repo, cat_breeds, quotes, debug
from messages import help_msg
from PyDictionary import PyDictionary
from random import randint
dictionary=PyDictionary()

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

@bot.command(args=2, aname="suggest")
def suggest(ctx, action="post", txt=""):
    is_disabled(ctx)
    if action == "post":
        with open("suggestions.txt", "a") as f:
         f.write(f"{txt} from {ctx.message.user.username}\n")
        ctx.send_msg("Suggestion posted!")
        print(f"New suggestion from {ctx.message.user.username}")
    elif action == "clear":
        admin_check(ctx)
        if os.path.exists('suggestions.txt'):
            os.remove("suggestions.txt")
            ctx.send_msg("Suggestions cleared!")
        else:
            ctx.send_msg("Suggestions already empty...")
    elif action == "list":
        if os.path.exists('suggestions.txt'):
            with open("suggestions.txt") as f:
                ctx.send_msg(f.read())
        else:
            ctx.send_msg("no posts to read...")
    else:
        ctx.send_msg("possible actions: post, clear, list")


@bot.command(args=2, aname="define")
def define(ctx, word, type="noun"):
    if type == "noun":
        meaning = dictionary.meaning(word)['Noun']
    elif type == "verb":
        meaning = dictionary.meaning(word)['Verb']
    else:
        ctx.send_msg("Invalid type.")
    ctx.send_msg(f"{word} means {' '.join(meaning)}")

@bot.command(args=3, aname="funny")
def funny(ctx, thing="help", user="", what=""):
    if thing == "does":
        answers = ["does", "does not"]
    elif thing == "isa":
        answers = ["is", "is not"]
    elif thing == "help":
        ctx.send_msg("@Tabby funny isa/does user custom")        
    answer = random.choice(answers)
    ctx.send_msg(f"{user} {answer} {what}")
    
@bot.command(args=1, aname="gayometer")
def gayometer(ctx, user):
    home_check(ctx)
    ctx.send_msg(f"{user} is {randint(1, 100)}% gay!")

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

plays = ["rock", "paper", "scissors"]
@bot.command(args=1, aname="rps")
def rps(ctx, play):
    home_check(ctx)
    bot_play = random.choice(plays)
    if bot_play == "scissors":
        if play == "rock":
            ctx.send_msg("you win!")
        if play == "paper":
            ctx.send_msg("you lose!")
    elif bot_play == "rock":
        if play == "scissors":
            ctx.send_msg("you lose!")
        if play == "paper":
            ctx.send_msg("you win!")
    elif bot_play == "paper":
        if play == "scissors":
            ctx.send_msg("you win!")
        if play == "rock":
            ctx.send_msg("you lose!")
    else:
        ctx.send_msg("tie!")
    ctx.send_msg(f"your play: {play}")
    ctx.send_msg(f"bot play: {bot_play}")

@bot.command(args=0, aname="cat")
def cat(ctx):
    ctx.send_msg(random.choice(cat_breeds))

@bot.command(args=1, aname="link")
def link(ctx, link=""):
    if link == "discord":
        ctx.send_msg("https://dsc.gg/meowermedia")
    elif link == "forums":
        ctx.send_msg("https://forums.meower.org")
    elif link == "wiki":
        ctx.send_msg("https://wiki.meower.org")
    elif link == "legal":
        ctx.send_msg("https://meower.org/legal")
    elif link == "website":
        ctx.send_msg("https://meower.org")
    #elif link == "list":
    #    ctx.send_msg("available links: forums, wiki, legal, website")
    else:
        ctx.send_msg("available links: discord, forums, wiki, legal, website")
    
@bot.command(args=1, aname="guide")
def guide(ctx, guide=""):
    if guide == "mod":
        ctx.send_msg("To get mod on meower you must first earn Mike's trust, be 13+, and ask for mod by either asking Mike directly or emailing contact@meower.org.")
    else:
        ctx.send_msg("available guides: mod")

@bot.command(args=1, aname="help")
def help(ctx, cmd=""):
    if cmd == "gayometer":
        ctx.send_msg("gayometer <user>")
    elif cmd=="guide":
        ctx.send_msg("guide <guide>")
    elif cmd=="give_tempadmin":
        ctx.send_msg("give_tempadmin <user>")
    elif cmd=="youtube":
        ctx.send_msg("youtube <user>")
    else:
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

@bot.command(args=0, aname="restart")
def restart(ctx):
    admin_check(ctx)
    ctx.send_msg("Restarting...")
    os.execv(sys.executable, ['python3'] + sys.argv)

@bot.command(args=0, aname="list")
def list(ctx):
    list_array = bot.wss.statedata["ulist"]["usernames"]
    list_array_string = str(list_array)
    list_array_nolbr = list_array_string.replace('[', '')
    list_array_norbr = list_array_nolbr.replace(']', '')
    list_array_noquo = list_array_norbr.replace("'", "")
    ctx.send_msg(f"online: {list_array_noquo}")

@bot.command(args=1, aname="youtube")
def youtube(ctx, user="null"):
    ctx.send_msg(f"Hey guys! {user} here, welcome back to yet another video!")

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

def login(bot=bot):
   bot.send_msg(f"Hello, I am Tabby v{version}, and I am a utility bot for Meower. To use me, type @Tabby help for a list of commands.")

if debug == "false":
    bot.callback(login)
elif debug == "true":
    print("Tabby is running in debug mode.")

try:
    bot.run(
        username="Tabby",
        password=passwordd,
        server="wss://server.meower.org"
    )
except KeyboardInterrupt:
    print("Detecting interrupt, going away now...")
    exit()