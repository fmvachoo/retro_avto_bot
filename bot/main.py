import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.config import BOT_TOKEN, ADMIN_ID
from bot.database import db, sticker_manager

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния для FSM
class UserState(StatesGroup):
    waiting_for_name = State()

# Глобальные переменные для управления сессией
admin_message_id = None
game_active = False

# Клавиатура для пользователя
def get_user_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Отсканировать QR-код", request_contact=False))
    return keyboard

# Клавиатура для админа
def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if game_active:
        keyboard.add(KeyboardButton("Закончить сессию"))
    else:
        keyboard.add(KeyboardButton("Начать игровую сессию"))
    return keyboard

# Функция для обновления сообщения админа
async def update_admin_message():
    global admin_message_id
    
    players = db.get_all_players()
    total_cars = sticker_manager.get_all_cars_count()
    
    message_text = "🎮 *Игровая сессия активна!*\n\n" if game_active else "⏸ *Игровая сессия остановлена*\n\n"
    message_text += "📊 *Список игроков:*\n"
    
    if not players:
        message_text += "Пока нет зарегистрированных игроков"
    else:
        for i, player in enumerate(players, 1):
            collected_count = len(player['collected_stickers'])
            message_text += f"{i}. {player['first_name']} {player['last_name']} - {collected_count}/{total_cars}\n"
    
    if admin_message_id:
        try:
            await bot.edit_message_text(
                chat_id=ADMIN_ID,
                message_id=admin_message_id,
                text=message_text,
                parse_mode='Markdown'
            )
        except:
            # Если сообщение не найдено, создаем новое
            msg = await bot.send_message(ADMIN_ID, message_text, parse_mode='Markdown')
            admin_message_id = msg.message_id
    else:
        msg = await bot.send_message(ADMIN_ID, message_text, parse_mode='Markdown')
        admin_message_id = msg.message_id

# Обработчик команды /start для пользователей
@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        # Админ получает админскую клавиатуру
        await message.answer("Панель администратора", reply_markup=get_admin_keyboard())
        await update_admin_message()
        return
    
    # Приветственное сообщение для пользователя
    welcome_text = (
        "Добро пожаловать на выставку команды RetroAuto!\n\n"
        "Мы создали для вас интерактивного бота, чтобы вы могли не только любоваться нашими авто, "
        "но и узнать информацию о них.\n"
        "За каждый отсканированный QR-код вы будете получать стикер. В конце выставки вас ждёт тест с призами. "
        "Тот, кто соберёт весь стикер-пак и правильно ответит на вопросы получит вещь нашего мерча.\n\n"
        "Готов начать путешествие? Вперед!"
    )
    
    await message.answer(welcome_text)
    await message.answer("Как вас зовут? (Введите имя и фамилию)")
    await UserState.waiting_for_name.set()

# Обработчик ввода имени пользователя
@dp.message_handler(state=UserState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name_parts = message.text.split()
    if len(name_parts) < 2:
        await message.answer("Пожалуйста, введите имя и фамилию через пробел")
        return
    
    first_name = name_parts[0]
    last_name = ' '.join(name_parts[1:])
    
    # Сохраняем пользователя в базу
    db.add_player(
        message.from_user.id,
        message.from_user.username,
        first_name,
        last_name
    )
    
    await state.finish()
    await message.answer(
        f"Отлично, {first_name}! Теперь вы можете сканировать QR-коды рядом с автомобилями.",
        reply_markup=get_user_keyboard()
    )
    
    # Обновляем сообщение админа
    if game_active:
        await update_admin_message()

# Обработчик кнопки "Отсканировать QR-код"
@dp.message_handler(lambda message: message.text == "Отсканировать QR-код")
async def scan_qr(message: types.Message):
    # Запрос сканирования QR-кода
    await message.answer(
        "Наведите камеру на QR-код",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Открыть камеру", switch_inline_query_current_chat="")
        )
    )

# Обработчик inline-запросов (симуляция сканирования QR)
@dp.inline_handler()
async def handle_qr_scan(inline_query: types.InlineQuery):
    # В реальном боте здесь бы обрабатывались данные QR-кода
    # Для демонстрации предлагаем выбрать автомобиль для "сканирования"
    
    results = []
    cars = [
        {"id": "chevy_57", "title": "Chevrolet Bel Air", "description": "1957 год"},
        {"id": "mercedes_gullwing", "title": "Mercedes Gullwing", "description": "1954 год"},
        {"id": "jaguar_etype", "title": "Jaguar E-Type", "description": "1961 год"},
        {"id": "ford_mustang", "title": "Ford Mustang", "description": "1964 год"},
        {"id": "cadillac_59", "title": "Cadillac Series 62", "description": "1959 год"},
    ]
    
    for car in cars:
        results.append(types.InlineQueryResultArticle(
            id=car["id"],
            title=car["title"],
            description=car["description"],
            input_message_content=types.InputTextMessageContent(
                message_text=f"Сканирую {car['title']}..."
            )
        ))
    
    await bot.answer_inline_query(inline_query.id, results)

# Обработчик выбора результата inline-запроса
@dp.message_handler(lambda message: message.text.startswith('Сканирую'))
async def process_qr_scan(message: types.Message):
    user_id = message.from_user.id
    player = db.get_player(user_id)
    
    if not player:
        await message.answer("Пожалуйста, сначала зарегистрируйтесь через /start")
        return
    
    # Извлекаем ID автомобиля из текста сообщения
    car_name = message.text.replace('Сканирую ', '').replace('...', '')
    car_id = None
    
    for cid, car in sticker_manager.CARS.items():
        if car['name'].split(' (')[0] in car_name:
            car_id = cid
            break
    
    if not car_id:
        await message.answer("Автомобиль не найден")
        return
    
    car_info = sticker_manager.get_car_info(car_id)
    
    if not car_info:
        await message.answer("Ошибка: информация об автомобиле не найдена")
        return
    
    # Проверяем, есть ли уже этот стикер у пользователя
    if car_id in player['collected_stickers']:
        await message.answer("У вас уже есть стикер этого автомобиля!")
        await message.answer(car_info['info'], parse_mode='Markdown')
        return
    
    # Добавляем стикер пользователю
    db.add_sticker_to_player(user_id, car_id)
    
    # Отправляем стикер и информацию
    try:
        await message.answer_sticker(car_info['sticker'])
    except:
        await message.answer("🎉 Стикер получен!")
    
    await message.answer(car_info['info'], parse_mode='Markdown')
    await message.answer("Отличная работа! Продолжайте в том же духе!", reply_markup=get_user_keyboard())
    
    # Обновляем статистику у админа
    if game_active:
        await update_admin_message()

# Обработчики для админа
@dp.message_handler(lambda message: message.text == "Начать игровую сессию" and message.from_user.id == ADMIN_ID)
async def start_game_session(message: types.Message):
    global game_active
    game_active = True
    db.start_game_session()
    await message.answer("Игровая сессия начата!", reply_markup=get_admin_keyboard())
    await update_admin_message()

@dp.message_handler(lambda message: message.text == "Закончить сессию" and message.from_user.id == ADMIN_ID)
async def end_game_session(message: types.Message):
    global game_active
    game_active = False
    db.end_game_session()
    await message.answer("Игровая сессия завершена!", reply_markup=get_admin_keyboard())
    await update_admin_message()

# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
