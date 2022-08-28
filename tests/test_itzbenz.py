# import os
# import itzbenz

# TOKEN = os.environ['TOKEN']
# CHANNEL = os.environ['CHANNEL']

# bot = itzbenz.Request(TOKEN)

# def test_send_message():
#     message = itzbenz.Message('`[TEST MESSAGE]`')
#     bot.post_message(CHANNEL, vars(message))

#     message.content = '`[TEST EMBED]`'
#     embed = vars(itzbenz.Embed(title='TEST', color=0x5865f2))
#     message.embeds = [embed, embed]
#     bot.post_message(CHANNEL, vars(message))

def test_default():
    assert True
