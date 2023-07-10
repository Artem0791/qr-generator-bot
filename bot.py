import qrcode
import logging

from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InputFile

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

# Configure logging
logging.basicConfig(level=logging.INFO)

HELP_COMMAND = """
Just input text or URL in message to generate QR code
"""

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = "/help"
b2 = "/start"
kb.add(b1, b2)


async def on_startup(_):
    print("I've been started up")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Welcome to QR Bot! QR everything you want!",
                           reply_markup=kb)
    await message.delete()


@dp.message_handler()
async def send_text_based_qr(message: types.Message):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=20,
                       border=2)

    qr.add_data(message.text)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    img.save('photo.png')
    img = InputFile('photo.png')

    await message.reply_photo(img, caption="QR is ready!", parse_mode='HTML')

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
