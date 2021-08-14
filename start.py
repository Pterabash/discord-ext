from dscord import bot
import os

if __name__ == '__main__':
    bot.load('system')  # load ext from module
    bot.run(os.getenv("DISCORD_TOKEN"))  # start bot with token