from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, deep_linking


from api.API_wather import Weather
from api.API_currency import Currency
from api.API_photo import Photo
from secret_key import TG_BOT_KEY


storage = MemoryStorage()
bot = Bot(token=TG_BOT_KEY)
db = Dispatcher(bot, storage=storage)

weather_api = Weather()
currency_api = Currency()
photo_api = Photo()



# Обработка команды /start
@db.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """
       Обработка команды /start. Приветствие пользователя и предложение выбрать
       действие.
       """
    if message.chat.type == types.ChatType.PRIVATE:
        print(message.text)
        print(message.chat)
        print(types.ChatType.PRIVATE)
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2,
                                                    resize_keyboard=True)
        weather_button = types.KeyboardButton('/weather')
        currency_button = types.KeyboardButton('/currency')
        animal_button = types.KeyboardButton('/animal')
        poll_button = types.KeyboardButton(
            text="Создать опрос",
            request_poll=types.KeyboardButtonPollType(
                type=types.PollType.REGULAR
            )
        )
        keyboard_markup.add(
            weather_button,
            currency_button,
            animal_button,
            poll_button
        )
        await message.reply('Привет! Что вы хотите сделать?',
                            reply_markup=keyboard_markup)


# Обработка команды /weather

@db.message_handler(commands=['weather'])
async def get_weather_command(message: types.Message):
    """
    Обработка команды /weather. Запрос погоды в заданном городе.
    """

    try:

        city = message.text.split()[1]
        response = weather_api.get_weather(city)
        await message.reply(response, parse_mode=ParseMode.HTML)
    except IndexError:
        await message.reply('Введите команду в формате "/weather <город>"')


# Обработка команды /currency
@db.message_handler(commands=['currency'])
async def process_currency_command(message: types.Message):
    """
    Обработка команды /currency. Конвертация валют.
    """
    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            raise IndexError
        amount = float(args[0])
        from_currency = args[1].upper()
        to_currency = args[2].upper()
        result = currency_api.get_currency(amount,
                                           from_currency,
                                           to_currency)
        await message.reply(result)
    except (IndexError, ValueError):
        await message.reply(
            'Введите команду в формате /currency <сумма> <валюта источника> '
            '<валюта назначения>\nВалюту источника и назначения указывать в '
            'общепринятом формате (EUR, RUB USD и т.д.)')


# Обработка команды /animal
@db.message_handler(commands=['animal'])
async def process_animal_command(message: types.Message):
    """
    Обработка команды /animal. Отправка случайной картинки с милыми животными.
    """
    try:
        image = photo_api.get_photo()
        await message.reply_photo(image)
    except:
        await message.reply(f'Ошибка в получении изображения.')


if __name__ == '__main__':
    executor.start_polling(db)
