from messages import no_perms, disabled
from config import bot_admins

def admin_check(ctx):
    if not ctx.message.user.username in bot_admins:
        ctx.send_msg(no_perms)
        exit()

def home_check(ctx):
    if ctx.message.chat == "home":
        exit()

def is_disabled(ctx):
    ctx.send_msg(disabled)
    exit()