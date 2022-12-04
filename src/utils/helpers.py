from main import bot, ADMINS_ID
from utils.messages import BOT_STARTED
from utils.buttons import start_markup


# Send notification to admin that bot started working
async def on_startup(args):
    for one_admin_id in ADMINS_ID:
        await bot.send_message(one_admin_id, BOT_STARTED, reply_markup=start_markup)



