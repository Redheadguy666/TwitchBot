import settings
import bot

def main():
	twitch_bot = bot.Bot(settings.HOST, settings.PORT, settings.CHAN, settings.NICK, settings.PASS)

	try:
		print("Подключение...")
		twitch_bot.connect()
		print("Успешное подключение!")
		print("Запуск...")
		twitch_bot.run()
	except Exception as e:
		print("Что-то пошло не так: {}".format(e))

if __name__ == "__main__":
	main()