import telebot, os, token_file, csvparse
from telebot import types

bot = telebot.TeleBot(token_file.token)
try:
    os.mkdir('files')
except FileExistsError:
    pass

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    show_btn = types.KeyboardButton("Посмотреть файлы")
    delete_btn = types.KeyboardButton("Удалить файлы")
    keyboard.add(show_btn, delete_btn)
    bot.send_message(message.chat.id, 'Отправьте файл формата CSV', reply_markup=keyboard)

@bot.message_handler(commands=['getres'])
def get_res(message):
    args = message.text.split()[1:]
    if len(args) == 3:
        try:
            filename, delimeter, header = args[0], args[1], args[2]
            data_table = csvparse.get_data_table(os.path.join('files', filename), delimeter)
            data_map = csvparse.get_dict_from_table(data_table)
            result = csvparse.get_parse_result(data_map, header)
            res_to_show = ''
            for key, value in result.items():
                res_to_show += f'{key} : {value}\n'
            bot.reply_to(message, res_to_show)
        except Exception:
            bot.reply_to(message, "Неправильный формат данных(возможно неправильный заголовок или разделитель)")
    else:
        bot.reply_to(message, 'Неправильный формат команды /get_res файл разделитель заголовок')


@bot.message_handler(commands=['help'])
def get_help(message):
    with open('FAQ.txt', 'r', encoding='utf-8') as f:
        bot.reply_to(message, f.read())
    f.close()


@bot.message_handler(func=lambda message: True)
def delete_table(message):
    keyboard = types.ReplyKeyboardMarkup()
    list(map(lambda btn: keyboard.add(btn), os.listdir("files")))
    keyboard.add("/start")
    if message.text == "Удалить файлы":
        bot.send_message(message.chat.id, "Выберите то что надо удалить\n", reply_markup=keyboard)
    if message.text in os.listdir("files"):
        os.remove(os.path.join('files', message.text))
    if message.text == "Посмотреть файлы":
        bot.send_message(message.chat.id, 'Список файлов:\n\n' + '\n'.join(os.listdir('files')))


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = message.document.file_name
    if filename.endswith('.csv'):
        with open(os.path.join("files", filename), 'wb') as new_file:
            new_file.write(downloaded_file)
        new_file.close()
        bot.reply_to(message, f"Файл {filename} отправлен на сервер")

bot.polling(non_stop=True)