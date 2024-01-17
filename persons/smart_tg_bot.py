# Пример работы со SmartTgBot.
# У нас должен быть TgBot с действующим Telegram токеном.
# from bots.models import TgBot
# from bots.smart_tg_bot import SmartTgBot
# tg_bot = TgBot.objects.get(id=1)
# smart_bot = SmartTgBot(tg_bot)
# Для отправки сообщений у нас должен быть telegram id пользователя.
# Пользователь должен стартануть бота.
# smart_bot.send_msg('Тут нужно указать telegram id получателя', 'Тут сообщение которое хотим отправить')
import telegram


class SmartTgBot:
    def __init__(self, acc):
        self._acc = acc

    @property
    def account(self):
        return self._acc

    def send_msg(self, chat_id: str, message: str):
        print(f'Отправляю сообщение для {chat_id}...')
        try:
            bot = telegram.Bot(token=self._acc.token)
            bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(e)
