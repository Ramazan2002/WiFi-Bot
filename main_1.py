import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import config
import speedtest
from manager import Manage
from get_wifi_list import Get_list

config_file = open('config.txt', 'r')
API_TOKEN = config_file.readline()
config_file.close()

logging.basicConfig(level = logging.INFO)
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
st = speedtest.Speedtest()
manage = Manage()
get_list_wifi = Get_list

class Conditions(StatesGroup):
    passw = State()
    mac = State()

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton('📝Список ранее подключеных WiFi сетей📝'))
    keyboard.add(types.KeyboardButton('🌐Тест WiFi🌐'))
    keyboard.add(types.KeyboardButton('📝Список пользователей WiFi📝'))
    keyboard.add(types.KeyboardButton('⚙️Изменить пароль WiFi сети⚙️'))
    keyboard.add(types.KeyboardButton('❌Заблокировать юзера сети❌'))
    await message.answer('Привет, я супер бот!🦾🤖', reply_markup = keyboard)

@dp.message_handler(lambda message: message.text == '📝Список пользователей WiFi📝')
async def wifi_vis(message: types.Message):
    remove_k = types.ReplyKeyboardRemove()
    await message.answer('Вот ваш список⤵️⤵️', reply_markup = remove_k)
    manage.browse_window()
    manage.log()
    await message.answer(manage.check_visitors())
    manage._exit()

@dp.message_handler(lambda message: message.text == '📝Список ранее подключеных WiFi сетей📝')
async def wifi_speed(message: types.Message):
    remove_k = types.ReplyKeyboardRemove()
    await message.answer('Вот ваш список⤵️⤵️', reply_markup = remove_k)
    await message.answer(get_list_wifi.get_list())


@dp.message_handler(lambda message: message.text == '🌐Тест WiFi🌐')
async def wifi_speed(message: types.Message):
    print('Start speed test')
    remove_k = types.ReplyKeyboardRemove()
    await message.answer('Сейчас вы получите тест скорости своей WiFi сети⚙️\nПодождите немного⌚️', reply_markup = remove_k)
    await message.answer(f'''
    Wifi Speed:\n
✅Download: {int(st.download())/1000000} Mbit/s\n
✅Upload: {int(st.upload())/1000000} Mbit/s\n
✅Ping: {st.results.ping} ms''')
    print('Speed test comlete')

@dp.message_handler(lambda message: message.text == '⚙️Изменить пароль WiFi сети⚙️')
async def wifi_change_pass(message: types.Message):
    remove_k = types.ReplyKeyboardRemove()
    await Conditions.passw.set()
    await message.answer('Введите новый пароль🔐', reply_markup = remove_k)

@dp.message_handler(state = Conditions.passw)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        password = data['text']
        last_message = 'Готово✅'
        await bot.send_message(
            message.from_user.id,
            last_message,
            parse_mode = 'HTML',
        )
        manage.browse_window()
        manage.log()
        manage.change_pass(password)
    await state.finish()

@dp.message_handler(lambda message: message.text == '❌Заблокировать юзера сети❌')
async def block(message: types.Message):
    remove_k = types.ReplyKeyboardRemove()
    await Conditions.mac.set()
    await message.answer('Введите MAC адрес🔑', reply_markup = remove_k)

@dp.message_handler(state = Conditions.mac)
async def block_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        mac_adress = data['text']
        last_message = 'Готово✅'
        await bot.send_message(
            message.from_user.id,
            last_message,
            parse_mode = 'HTML',
        )
        manage.browse_window()
        manage.log()
        manage.block_profile(mac_adress)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
