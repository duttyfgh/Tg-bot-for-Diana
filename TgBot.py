from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from background import keep_alive
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pytz

import os
import datetime

TOKEN = '6465575232:AAHIkY9wl72ICzr_UgKpKAJOGmFBhdyM6qo'

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=storage )
#1034111472 DIANA'S ID 
#910013627 DIMA'S ID 

@dp.message_handler(commands=['start'])
async def startDef(message: types.Message):
    await message.answer('Представляю вашему вниманию бота для самой прекрасной, самой милой, самой любимой девочеки - Дианы Васильевны'
                         '\nЕсли отправите свое фото📸 я буду безумно рад'
                         )
    await message.answer('Вы также можете мне отправить любое сообщение 💌', reply_markup=mainKeyboard)

mainKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
mainKeyboard.add(
    KeyboardButton("Напомнить💗"),
)
mainKeyboard.add(
    KeyboardButton("Как долго мы встречаемся🤔?")
)
mainKeyboard.add(
  KeyboardButton("Мой список желаний🎁")
)
mainKeyboard.add(
    KeyboardButton("Admin⚙️")
)

# Определяем киевский часовой пояс
kiev_timezone = pytz.timezone('Europe/Kiev')

# Получаем текущую дату и время в киевском часовом поясе
current_datetime = datetime.datetime.now(kiev_timezone)

# Форматируем вывод
formatted_date = current_datetime.strftime("%Y-%m-%d")
formatted_time = current_datetime.strftime("%H:%M")

message_text = f'На дворе {formatted_date}, время {formatted_time}, а я все также сильно люблю тебя!💗'

#Считаем как долго встречаемся
def days_since():
  # Начальная дата
  start_date = datetime.datetime(2023, 9, 8)

  # Текущая дата
  current_date = datetime.datetime.now()

  # Вычисляем разницу между текущей датой и начальной датой
  delta = current_date - start_date

  # Количество месяцев, дней и часов
  months = delta.days // 30
  days = delta.days % 30
  hours = delta.seconds // 3600

  # Формируем строку с результатом
  result = f"Мы встречаемся уже {months} месяцев, {days} дней и {hours} часов💗"

  return result

#Хендлер для команди /howLong
@dp.message_handler(commands=['howLong'])
async def notify_user(message: types.Message):

    dateTime = days_since()
    await message.reply(dateTime)

# Хендлер для команды /getId
@dp.message_handler(commands=['getId'])
async def notify_user(message: types.Message):
    # Получите user_id пользователя, который отправил команду
    user_id = message.from_user.id

    # Отправьте сообщение "привет" пользователю с указанным user_id
    print(message.chat.first_name,  user_id)
    await bot.send_message(910013627, f'{message.chat.first_name}👤: {user_id}')

    # Отправьте вам подтверждение
    await message.reply("Ваш id теперь есть у dutyfgh!")


# Определим состояния
class SendToDiana(StatesGroup):
    waiting_for_text = State()

    # Создаем клавиатуру

keyboard = types.InlineKeyboardMarkup()
cancel_button = types.InlineKeyboardButton("Отмена 🚫", callback_data="cancel")
change_button = types.InlineKeyboardButton("Изменить ✏", callback_data="change")
send_button = types.InlineKeyboardButton("Отправить ✅", callback_data="send")

# Добавляем кнопки в клавиатуру
keyboard.add(cancel_button, change_button, send_button)

# Хендлер для команды /notify
@dp.message_handler(commands="notify", state=None)
async def notify(message: types.Message, state: FSMContext):
    # Отправляем сообщение с клавиатурой
    await message.answer("Что отправим Диане?💌")
    await SendToDiana.waiting_for_text.set()

# Обработчик для ввода текста
@dp.message_handler(state=SendToDiana.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ChangedText'] = message.text

    # Отправляем сообщение с клавиатурой
    await message.answer(
        f"Текст для отправки: {message.text}\nВыберите действие:",
        reply_markup=keyboard
    )

#callbacks
@dp.callback_query_handler(lambda query: query.data == "cancel", state=SendToDiana.waiting_for_text)
async def cancel_text(callback_query: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.from_user.id, text="Отменено.")


@dp.callback_query_handler(lambda query: query.data == "change", state=SendToDiana.waiting_for_text)
async def change_text(callback_query: CallbackQuery):
    await SendToDiana.waiting_for_text.set()
    await bot.send_message(callback_query.from_user.id, text="Введите новый текст:")

@dp.callback_query_handler(lambda query: query.data == "send", state=SendToDiana.waiting_for_text)
async def send_text(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        changed_text = data['ChangedText']

    # Здесь можно добавить логику отправки текста Диане
    await bot.send_message(1034111472, changed_text)
    # Например, отправить текст через бота

    # Удаляем сообщение с клавиатурой
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    # Отменяем состояние
    await state.finish()

    # Отправляем ответ
    await bot.send_message(callback_query.from_user.id, text=f"Текст успешно отправлен Диане: {changed_text}")

# Определим состояние для работы с списком желаний
class WishListState(StatesGroup):
    waiting_for_wish = State()

# Обработчик для команды "Мой список желаний🎁"
@dp.message_handler(lambda message: message.text == "Мой список желаний🎁")
async def show_wishlist(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    view_button = InlineKeyboardButton("Посмотреть список желаний 👁️🎁", callback_data="view_wishlist")
    add_button = InlineKeyboardButton("Добавить в список желаний✍➕", callback_data="add_to_wishlist")
    keyboard.add(view_button, add_button)

    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработчик для кнопки "Посмотреть список желаний"
@dp.callback_query_handler(lambda query: query.data == "view_wishlist", state="*")
async def view_wishlist(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # Прочитать содержимое файла wishList.txt
        try:
            with open("wishList.txt", "r", encoding="utf-8") as file:
                wishlist_content = file.read()
        except FileNotFoundError:
            wishlist_content = "Список желаний пуст, сначала добавьте желание!"

    await bot.send_message(callback_query.from_user.id, f"Список желаний:\n{wishlist_content}")

# Обработчик для кнопки "Добавить в список желаний"
@dp.callback_query_handler(lambda query: query.data == "add_to_wishlist", state="*")
async def add_to_wishlist(callback_query: types.CallbackQuery, state: FSMContext):
    await WishListState.waiting_for_wish.set()
    await bot.send_message(callback_query.from_user.id, "Введите ваше желание:")

# Обработчик для ввода желания
@dp.message_handler(state=WishListState.waiting_for_wish)
async def process_wish(message: types.Message, state: FSMContext):
    wish = message.text

    # Записать желание в файл
    with open("wishList.txt", "a", encoding="utf-8") as file:
        file.write(wish + "\n")

    with open("wishList.txt", "r", encoding="utf-8") as file:
        wishlist_content = file.read()

    await state.finish()
    await message.answer("Желание успешно добавлено в список✅")
    await message.answer("Список желаний теперь выглядит так📋:")
    await message.answer(wishlist_content)

#Выход с админ панели
@dp.message_handler(commands=['back'])
async def handle_message(message: types.Message):
    await message.answer('Вы вернулись в главное меню', reply_markup=mainKeyboard)

# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    # Проверяем, является ли сообщение командой для администратора
    if message.text.strip() == "Admin⚙️":
        adminKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        adminKeyboard.add(
            KeyboardButton("/notify"),
        )
        adminKeyboard.add(
            KeyboardButton("/getId")
        )
        adminKeyboard.add(
            KeyboardButton("/back")
        )
        if message.from_user.id == 910013627:
            await message.answer('Вы вошли в админ панель⚙️✔️', reply_markup=adminKeyboard)
        else:                               
            await message.answer('Вы не похожи на админа😒🙄❌')
    else:
        # Проверка на остальные сообщения
        if message.text.strip().lower() == "я самая красивая девочка?":
            await message.answer('Да ты самая красивая девочка!💘, что за вопросы?!?')
        elif message.text.strip().lower() == "покажи мне самую красивую девочку":
            with open('photo.jpg', 'rb') as photo:
                await message.answer_photo(photo, caption="Вот она!😍")
        elif message.text.strip().lower() == "у кого самые красивые ноготочки?":
            await message.answer('У тебя!!')
        elif message.text.strip() == "Напомнить💗":
            await message.answer(message_text)
        elif message.text.strip() == "Как долго мы встречаемся🤔?":
            await message.answer(days_since())    
        else:
            await message.answer(
                'К сожалению, я понимаю совсем немного сообщений, но я всегда знаю, что люблю тебя')  ## .reply то ответ на сообщение
            await message.answer('Вот сообщения, которые ты можешь написать, и я их распознаю:\n'
                                 '1. я самая красивая девочка?\n'
                                 '2. покажи мне самую красивую девочку\n'
                                 '3. у кого самые красивые ноготочки?')
            if(message.from_user.id != 910013627):
              await bot.send_message(910013627, f'‼Неизвестное сообщение от‼ {message.chat.first_name}👤: "{message.text}"')

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_photo(message: types.Message):
    #Получаем и отправляем себе фото которое отправил пользователь
    if(message.from_user.id == 1034111472):
        photo_id = message.photo[-1].file_id
        await bot.send_photo(910013627, photo_id, caption="Диана отправила фото😍")
    else:
      await message.answer('dutyfgh отправил фото сам себе😍')
    #Пишем ответ на фото
    await message.answer("Вау😍, Ты прекрасна🛐")

keep_alive()
executor.start_polling(dp, skip_updates=True)