from messages import no_perms
from config import bot_admins

def admin_check(ctx):
    if not ctx.message.user.username in bot_admins:
        ctx.send_msg(no_perms)
        exit()

def home_check(ctx):
    if ctx.message.chat == "home":
        exit()