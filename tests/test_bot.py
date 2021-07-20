from descord import bot
from multiprocessing import Process

def test_bot():
    def start_bot():
        bot.run(os.environ['TOKEN'])
    p = Process(target=start_bot, name='Start Bot')
    p.start()
    p.join(timeout=10)
    assert True

