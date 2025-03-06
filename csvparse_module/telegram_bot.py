import telebot, os, token_file, csvparse
from telebot import types

bot = telebot.TeleBot(token_file.token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btn = types.KeyboardButton("Посмотреть файлы")
    keyboard.add(btn)
    bot.send_message(message.chat.id, 'Отправьте файл формата CSV', reply_markup=keyboard)

@bot.message_handler(commands=['get_res'])
def get_res(message):
    args = message.text.split()[1:]
    if len(args) == 3:
        filename, delimeter, header = args[0], args[1], args[2]
        data_table = csvparse.get_data_table(os.path.join('files', filename), delimeter)
        data_map = csvparse.get_dict_from_table(data_table)
        result = csvparse.get_parse_result(data_map, header)
        res_to_show = ''
        table_to_show = ''

        for key, value in result.items():
            res_to_show += f'{key} : {value}\n'

        for row in data_table:
            for elem in row:
                table_to_show += f'{elem} '
            table_to_show += '\n'

        bot.reply_to(message, table_to_show)
        bot.send_message(message.chat.id, res_to_show)
    else:
        bot.reply_to(message, 'Неправильный формат команды /get_res файл разделитель заголовок')


@bot.message_handler(commands=['delete_table'])
def delete_table(message):
    args = message.text.split()[1:]
    if len(args) == 1:
        table_name = args[0]
        os.remove(os.path.join('files', table_name))
    else:
        bot.reply_to(message, "Неправильный формат команды /delete_table файл")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    if message.text == "Посмотреть файлы":
        bot.send_message(message.chat.id, 'Список файлов:\n\n' + '\n'.join(os.listdir('files')), reply_markup=keyboard)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = message.document.file_name
    if filename.endswith('.csv'):
        with open(os.path.join("files", filename), 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, f"Файл {filename} отправлен на сервер")


bot.polling(non_stop=True)