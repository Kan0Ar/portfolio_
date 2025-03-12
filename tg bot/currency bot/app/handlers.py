from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods.delete_message import DeleteMessage

from main import updating_db


router = Router()

class Ask_Offers(StatesGroup):
    name = State()
    questions = State()


class Ask_Errors(StatesGroup):
    name = State()
    questions = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Здравствуй дорогой пользователь!\n\n▎ Описание бота валют Currency bot\n\nЗдравствуйте! Я ваш помощник в мире валют! 🌍\n\nЯ собираю актуальные курсы валют от различных банков, чтобы помочь вам быстро и удобно находить нужную информацию.\n\n▎ Банки представленные в боте\n\n1. Альфа Банк\n2. Беларусбанк\n3. Благропромбанк\n4. Белгазпромбанк\n5. Приорбанк\n\n▎ Как я могу помочь? \n\n- Узнайте текущие курсы валют. \n- Получите информацию о курсах от различных банков.\n- Сравните предложения и выберите лучшее. \n\n▎ Умения бота представлены в команде /help.\n\nНачните использовать меня, и вы всегда будете в курсе валютных изменений! 💱 \n\nСпасибо, что выбрали меня!')


@router.message(Command('banks'))
async def cmd_start(message : Message):
    await message.answer('Привет! Используй команду предложенные кнопки, чтобы увидеть список доступных банков. 💳\n\nПри активации этой команды появится клавиатура с кнопками для каждого банка. Просто нажми на интересующий тебя банк, и бот предоставит необходимую информацию! 🏦', reply_markup=kb.main)# сделан вывод с кнопками

@router.message(F.text == 'Вывод определенного банка')
async def one_banks(message : Message):
    await message.answer('▎ Информация о покупке/продаже валюты\n\n✨ Выберите банк для получения информации о курсах валют.\n\n📊 После нажатия на кнопку, вы получите актуальную информацию о курсах.\n\nНажмите на кнопку, чтобы продолжить!', reply_markup= kb.ask_bank)#.adjust(2))#.as_markup())


@router.callback_query(F.data == 'alpha_bank')
async def al_bank(callback: CallbackQuery):
    await callback.answer('Прошу подождать, добавляются актуальные данные.', show_alert=True)
    updating_db()
    conn = sqlite3.connect("myfin.db")
    cursor = conn.cursor()
    banks = cursor.execute("SELECT name, usd_sale, usd_buy, eur_sale, eur_buy, rub_sale, rub_buy FROM banks WHERE id == 1").fetchone()
    await callback.message.edit_text('💹 Курс валют '+ str(banks[0]) +'а на сегодня:' +
                            '\n\n🔹 Сдать доллар: ' + str(banks[1]) + '₽' + '\n🔸 Купить доллар: ' + str(banks[2]) + '₽' +
                            '\n🔹 Сдать евро: ' + str(banks[3]) + '₽' + '\n🔸 Купить евро: ' + str(banks[4]) + '₽' +
                            '\n🔹 Сдать российский рубль: ' + str(banks[5]) + '₽' + '\n🔸 Купить российский рубль: ' + str(banks[6]) + '₽' + '\n',
                            reply_markup=kb.ask_bank)

    conn.commit()
    conn.close()

@router.callback_query(F.data == 'belarusbank')
async def al_bank(callback: CallbackQuery):
    await callback.answer('Прошу подождать, добавляются актуальные данные.', show_alert=True)
    updating_db()
    conn = sqlite3.connect("myfin.db")
    cursor = conn.cursor()
    banks = cursor.execute("SELECT name, usd_sale, usd_buy, eur_sale, eur_buy, rub_sale, rub_buy FROM banks WHERE id == 3").fetchone()
    await callback.message.edit_text('💹 Курс валют '+ str(banks[0]) +'а на сегодня:' +
                            '\n\n🔹 Сдать доллар: ' + str(banks[1]) + '₽' + '\n🔸 Купить доллар: ' + str(banks[2]) + '₽' +
                            '\n🔹 Сдать евро: ' + str(banks[3]) + '₽' + '\n🔸 Купить евро: ' + str(banks[4]) + '₽' +
                            '\n🔹 Сдать российский рубль: ' + str(banks[5]) + '₽' + '\n🔸 Купить российский рубль: ' + str(banks[6]) + '₽' + '\n',
                            reply_markup=kb.ask_bank)

    conn.commit()
    conn.close()

@router.callback_query(F.data == 'belaroproprombank')
async def al_bank(callback: CallbackQuery):
    await callback.answer('Прошу подождать, добавляются актуальные данные.', show_alert=True)
    updating_db()
    conn = sqlite3.connect("myfin.db")
    cursor = conn.cursor()
    banks = cursor.execute("SELECT name, usd_sale, usd_buy, eur_sale, eur_buy, rub_sale, rub_buy FROM banks WHERE id == 2").fetchone()
    await callback.message.edit_text('💹 Курс валют '+ str(banks[0]) +'а на сегодня:' +
                            '\n\n🔹 Сдать доллар: ' + str(banks[1]) + '₽' + '\n🔸 Купить доллар: ' + str(banks[2]) + '₽' +
                            '\n🔹 Сдать евро: ' + str(banks[3]) + '₽' + '\n🔸 Купить евро: ' + str(banks[4]) + '₽' +
                            '\n🔹 Сдать российский рубль: ' + str(banks[5]) + '₽' + '\n🔸 Купить российский рубль: ' + str(banks[6]) + '₽' + '\n',
                            reply_markup=kb.ask_bank)

    conn.commit()
    conn.close()

@router.callback_query(F.data == 'belgazprombank')
async def al_bank(callback: CallbackQuery):
    await callback.answer('Прошу подождать, добавляются актуальные данные.', show_alert=True)
    updating_db()
    conn = sqlite3.connect("myfin.db")
    cursor = conn.cursor()
    banks = cursor.execute("SELECT name, usd_sale, usd_buy, eur_sale, eur_buy, rub_sale, rub_buy FROM banks WHERE id == 4").fetchone()
    await callback.message.edit_text('💹 Курс валют '+ str(banks[0]) +'а на сегодня:' +
                            '\n\n🔹 Сдать доллар: ' + str(banks[1]) + '₽' + '\n🔸 Купить доллар: ' + str(banks[2]) + '₽' +
                            '\n🔹 Сдать евро: ' + str(banks[3]) + '₽' + '\n🔸 Купить евро: ' + str(banks[4]) + '₽' +
                            '\n🔹 Сдать российский рубль: ' + str(banks[5]) + '₽' + '\n🔸 Купить российский рубль: ' + str(banks[6]) + '₽' + '\n',
                            reply_markup=kb.ask_bank)

    conn.commit()
    conn.close()

@router.callback_query(F.data == 'priorbank')
async def al_bank(callback: CallbackQuery):
    await callback.answer('Прошу подождать, добавляются актуальные данные.', show_alert=True)
    updating_db()
    conn = sqlite3.connect("myfin.db")
    cursor = conn.cursor()
    banks = cursor.execute("SELECT name, usd_sale, usd_buy, eur_sale, eur_buy, rub_sale, rub_buy FROM banks WHERE id == 5").fetchone()
    await callback.message.edit_text('💹 Курс валют '+ str(banks[0]) +'а на сегодня:' +
                            '\n\n🔹 Сдать доллар: ' + str(banks[1]) + '₽' + '\n🔸 Купить доллар: ' + str(banks[2]) + '₽' +
                            '\n🔹 Сдать евро: ' + str(banks[3]) + '₽' + '\n🔸 Купить евро: ' + str(banks[4]) + '₽' +
                            '\n🔹 Сдать российский рубль: ' + str(banks[5]) + '₽' + '\n🔸 Купить российский рубль: ' + str(banks[6]) + '₽' + '\n',
                            reply_markup=kb.ask_bank)

    conn.commit()
    conn.close()


@router.callback_query(F.data == '_to_main')
async def to_main(callback: CallbackQuery):
    await callback.message.edit_text('▎ Информация о покупке/продаже валюты\n\n✨ Выберите банк для получения информации о курсах валют.\n\n📊 После нажатия на кнопку, вы получите актуальную информацию о курсах.\n\nНажмите на кнопку, чтобы продолжить!', reply_markup=kb.ask_bank)


@router.message(F.text == 'Вывод всех банков')
async def all_banks(message : Message):
    await message.answer('Идет сбор информации, прошу подождать...')
    updating_db()
    conn = sqlite3.connect("myfin.db")
    cursor = conn.cursor()
    for a in range(1, 6):
        banks = cursor.execute("SELECT name, usd_sale, usd_buy, eur_sale, eur_buy, rub_sale, rub_buy FROM banks WHERE id == ?", (a,)).fetchone()
        await message.answer('💹 Курс валют '+ str(banks[0]) +'а на сегодня:' +
                            '\n\n🔹 Сдать доллар: ' + str(banks[1]) + '₽' + '\n🔸 Купить доллар: ' + str(banks[2]) + '₽' +
                            '\n🔹 Сдать евро: ' + str(banks[3]) + '₽' + '\n🔸 Купить евро: ' + str(banks[4]) + '₽' +
                            '\n🔹 Сдать российский рубль: ' + str(banks[5]) + '₽' + '\n🔸 Купить российский рубль: ' + str(banks[6]) + '₽' + '\n')
    conn.commit()
    conn.close()


@router.message(Command('help'))
async def ask(message : Message):
    await message.answer('Команды бота\n\n▎ Команда /start\nНачинает работу с ботом. После активации бот приветствует вас и представляется. 🎉 \n\n▎ Команда /banks\nВыводит список доступных кнопок с опциями. Позволяет выбрать определенный или весь список банков. 📋 \n\n▎ Команда /help\nПредоставляет подробную информацию о всех командах бота и их функционале. Полезно для новых пользователей! ❓\n\n▎ Команда /offer \nПозволяет сохранять предложения от пользователей.\nВы можете делиться своими идеями и предложениями, которые будут рассмотрены. 💡\n\n▎ Команда /error\nСлужит для сохранения сообщений об ошибках. Если вы столкнулись с проблемой, используйте эту команду, чтобы сообщить об этом. 🚨')


@router.message(Command('offer'))
async def step_f(message : Message, state : FSMContext):
    await state.set_state(Ask_Offers.name)
    await message.answer('Введите ваше имя.')


@router.message(Ask_Offers.name)
async def step_f(message : Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Ask_Offers.questions)
    await message.answer('Введите ваши предложения.')


@router.message(Ask_Offers.questions)
async def step_f(message : Message, state : FSMContext):
    await state.update_data(questions = message.text)
    data = await state.get_data()
    await message.answer(f'✨ Спасибо за ваш отзыв! ✨\n\n👤 Ваше имя: {data['name']}.\n💡 Ваше предложение: {data['questions']}.')
    connection = sqlite3.connect('offer.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_offer(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            offers TEXT
        )
    """)
    cursor.execute("INSERT INTO users_offer (name, offers) VALUES (?, ?)", (data['name'], data['questions'],),)
    connection.commit()
    connection.close()
    await state.clear()


@router.message(Command('error'))
async def step_f(message : Message, state : FSMContext):
    await state.set_state(Ask_Errors.name)
    await message.answer('Введите ваше имя.')


@router.message(Ask_Errors.name)
async def step_f(message : Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Ask_Errors.questions)
    await message.answer('Введите вашу ошибку которая возникла в процессе использования бота.')


@router.message(Ask_Errors.questions)
async def step_f(message : Message, state : FSMContext):
    await state.update_data(questions = message.text)
    data = await state.get_data()
    await message.answer(f'⚠️ Спасибо за ваш отзыв! ⚠️\n\n👤 Ваше имя: {data['name']}.\n❌ Ваша ошибка: {data['questions']}.')
    connection = sqlite3.connect('error.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_error(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            errors TEXT
        )
    """)
    cursor.execute("INSERT INTO users_error (name, errors) VALUES (?, ?)", (data['name'], data['questions'],),)
    connection.commit()
    connection.close()
    await state.clear()