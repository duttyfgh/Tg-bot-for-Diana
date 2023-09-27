from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
import os
import datetime

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot,storage=storage )
#1034111472 ID DIANA

@dp.message_handler(commands=['start'])
async def startDef(message: types.Message):
    await message.answer('Представляю вашему вниманию бота для самой прекрасной, самой милой, самой любимой девочеки - Дианы Васильевны'
                         '\nФункционал пока что скромный:'
                         '\n 1. "/reminder"'
                         '\n 2. Отправь свое фото📸'
                         )
    await message.answer('Вы также можете мне отправить любое сообщение 💌')


# Получаем текущую дату и время
current_datetime = datetime.datetime.now()

# Форматируем вывод
formatted_date = current_datetime.strftime("%Y-%m-%d")
formatted_time = current_datetime.strftime("%H:%M")

message_text = f'На дворе {formatted_date}, время {formatted_time}, а я все также сильно люблю тебя!💗'
@dp.message_handler(commands=['reminder'])
async def remindedDef(message: types.Message):
    await message.answer(message_text)

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
    await message.answer("Что отправим любимой девчуле?")
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
    await bot.answer_callback_query(callback_query.id, text="Отменено.")


@dp.callback_query_handler(lambda query: query.data == "change", state=SendToDiana.waiting_for_text)
async def change_text(callback_query: CallbackQuery):
    await SendToDiana.waiting_for_text.set()
    await bot.answer_callback_query(callback_query.id, text="Введите новый текст:")

@dp.callback_query_handler(lambda query: query.data == "send", state=SendToDiana.waiting_for_text)
async def send_text(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        changed_text = data['ChangedText']

    # Здесь можно добавить логику отправки текста Диане
    await bot.send_message(1034111472, changed_text)
    # Например, отправить текст через бота

    # Отменяем состояние
    await state.finish()

    # Отправляем ответ
    await bot.answer_callback_query(callback_query.id, text=f"Текст успешно отправлен Диане: {changed_text}")


@dp.message_handler(content_types=types.ContentTypes.TEXT)#
async def handle_message(message: types.Message):
    # Проверка на сообщение "я самая красивая девочка?"
    if message.text.strip().lower() == "я самая красивая девочка?":
        await message.answer('Да ты самая красивая девочка!💘, что за вопросы?!?')
    # Проверка на сообщение "кто самая красивая девочка?"
    elif message.text.strip().lower() == "кто самая красивая девочка?":
        with open('photo.jpg', 'rb') as photo:
            await message.answer_photo(photo, caption="Вот она!😍")
    elif message.text.strip().lower() == "у кого самые красивые ноготочки?":
        await message.answer('У тебя!!')
    else:
        await message.answer(
            'К сожелению я понимаю совсем немного сообщений, но я всегда знаю что люблю тебя')  ## .reply то ответ на сообщение
        await message.answer('Вот сообщения которые ты можешь написать и я их распознаю:\n'
                             '1. я самая красивая девочка?\n'
                             '2. кто самая красивая девочка?\n'
                             '3. у кого самые красивые ноготочки?')
        await bot.send_message(910013627, f'‼Неизвествое сообщение от‼ {message.chat.first_name}👤: "{message.text}"')
    
@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_photo(message: types.Message):
    # Отправляем ответное сообщение
    await message.answer("Вау! Ты прекрасна!😍")




executor.start_polling(dp, skip_updates=True)