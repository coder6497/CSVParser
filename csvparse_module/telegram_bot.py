import os, token_file, csvparse, asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot import types


bot = AsyncTeleBot(token_file.token)

@bot.message_handler(commands=['start'])
async def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    show_btn = types.KeyboardButton("📁Посмотреть файлы🗃️📃")
    delete_btn = types.KeyboardButton("🚮🗑Удалить файлы🗑️")
    keyboard.add(show_btn, delete_btn)
    await bot.send_message(message.chat.id, 'Отправьте файл формата CSV📁📃', reply_markup=keyboard)

@bot.message_handler(commands=['getres'])
async def get_res(message):
    args = message.text.split()[1:]
    user_dir = os.path.join('files', str(message.from_user.id))
    if len(args) == 3:
        try:
            filename, delimeter, header = args[0], args[1], args[2]
            data_table = csvparse.get_data_table(os.path.join(user_dir, filename), delimeter)
            data_map = csvparse.get_dict_from_table(data_table)
            result = csvparse.get_parse_result(data_map, header)
            res_to_show = ''
            for key, value in result.items():
                res_to_show += f'{key} : {value}\n'
            await bot.reply_to(message, res_to_show)
        except Exception:
            await bot.reply_to(message, "❗❗❗Неправильный формат данных(возможно неправильный заголовок или разделитель)")
    else:
        await bot.reply_to(message, '‼️‼️‼️Неправильный формат команды /getres файл разделитель заголовок')

@bot.message_handler(commands=['help'])
async def get_help(message):
    with open('FAQ.txt', 'r', encoding='utf-8') as f:
        await bot.reply_to(message, f.read())
    f.close()


@bot.message_handler(func=lambda message: True)
async def delete_table(message):
    user_dir = os.path.join('files', str(message.from_user.id))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    list(map(lambda btn: keyboard.add(btn), os.listdir(user_dir)))
    keyboard.add("/start")
    if message.text == "🚮🗑Удалить файлы🗑️":
        await bot.send_message(message.chat.id, "🗑️Выберите то что надо удалить\n", reply_markup=keyboard)
    if message.text in os.listdir(user_dir):
        os.remove(os.path.join(user_dir, message.text))
        await bot.reply_to(message, f"Файл {message.text} успешно удален🗑️")
    if message.text == "📁Посмотреть файлы🗃️📃":
        await bot.send_message(message.chat.id, '📃📃Список файлов:\n\n' + '\n'.join(os.listdir(user_dir)))


@bot.message_handler(content_types=['document'])
async def handle_document(message):
    try:
        os.mkdir(os.path.join('files', str(message.from_user.id)))
    except FileExistsError:
        pass
    user_dir = os.path.join('files', str(message.from_user.id))
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    filename = message.document.file_name
    if filename.endswith('.csv'):
        with open(os.path.join(user_dir, filename), 'wb') as new_file:
            new_file.write(downloaded_file)
            await bot.reply_to(message, f"Файл {filename} отправлен на сервер😊😊")
        new_file.close()


asyncio.run(bot.polling(non_stop=True))