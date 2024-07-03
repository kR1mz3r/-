import telebot
import sqlite3
import smtplib
from email.mime.text import MIMEText
from telebot import types

token = '6259451243:AAEMShdfVSw3mJ22kzB8r1rDVa1vuG4Wxik'

bot = telebot.TeleBot(token)

user_dict = {}

class User:
    def __init__(self, surname):
        self.surname = surname

        user_data = ['name', 'status', 'email', 'email_key', 'id']

        for i in user_data:
            self.i = None

user_email = {}

class These_email:
    def __init__(self, recipient):
        self.recipient = recipient

        mail_data = ['title', 'email_content']

        for i in mail_data:
            self.i = None

@bot.message_handler(commands=['start'])
def start(message):

    text_start = 'Привет, я помощник по работе компании "Айти мир". Чем я могу помочь вам?\nЧтобы узнать, что я могу ' \
                 'нажмите кнопку "Помощь"'


    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    id = int(message.from_user.id)

    query = f"SELECT id FROM users WHERE id='{id}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result is not None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_send_doc = types.KeyboardButton('Отправить файлы')
        button_send_an_email = types.KeyboardButton('Написать письмо')
        button_get_doc = types.KeyboardButton('Получить файлы')
        button_about = types.KeyboardButton('О нас')
        button_help = types.KeyboardButton('Помощь')
        markup.add(button_send_doc, button_send_an_email, button_get_doc, button_about, button_help)
        bot.send_message(message.chat.id, '<b>' + text_start + '</b>', parse_mode='html', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_registration = types.KeyboardButton('Регистрация')
        button_about = types.KeyboardButton('О нас')
        button_help = types.KeyboardButton('Помощь')
        markup.add(button_registration, button_about, button_help)
        bot.send_message(message.chat.id, '<b>' + text_start + '</b>', parse_mode='html', reply_markup=markup)

    conn.close()

@bot.message_handler(commands=['Регистрация'])
def registration(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        hide_button = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id,
                               '<b>Чтобы бот мог отправлять вам все необходимые файлы для работы нужно пройти '
                               'регистрацию.\nУкажите свою фамилию:</b>',
                               parse_mode='html', reply_markup=hide_button)
        bot.register_next_step_handler(msg, register_surname)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def register_surname(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.surname = message.text

        msg = bot.send_message(message.chat.id,
                               '<b>Укажите свое имя:</b>',
                               parse_mode='html')
        bot.register_next_step_handler(msg, register_name)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def register_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.name = message.text

        msg = bot.send_message(message.chat.id,
                               '<b>Укажите свою должность(Джуниор, Мидл, Сеньор):</b>',
                               parse_mode='html')

        bot.register_next_step_handler(msg, register_status)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def register_status(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.status = message.text

        msg = bot.send_message(message.chat.id,
                               '<b>Теперь нам нужна ваша рабочая почта.\nСоветуем создать новую почту gmail и '
                               'отправить ее сюда\nУкажите свой email:</b>',
                               parse_mode='html')
        bot.register_next_step_handler(msg, register_email)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def register_email(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.email = message.text

        msg = bot.send_message(message.chat.id,
                               '<b>Теперь вам нужно отправить специальный ключ, чтобы я мог отправлять письма на '
                               'вашу почту от других сотрудников.'
                               '\nДля этого перейдите по ссылке '
                               'https://myaccount.google.com/u/1/security?hl=ru и включите двухэтапную аунтефикацию'
                               ', после этого нужно в поиск ввести "Пароли приложений" и подключить свою почту к'
                               'приложению (в списке приложений главное выбрать "другое" и написать любое слово).'
                               '\nПосле этого вам выдадут ключ, который необходимо отправить мне.'
                               '\nУкажите ключ от вашей почты:</b>',
                               parse_mode='html')
        bot.register_next_step_handler(msg, register_email_key)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def register_email_key(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.email_key = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_right = types.KeyboardButton('Все верно')
        button_wrong = types.KeyboardButton('Нет')
        markup.add(button_right, button_wrong)

        msg = bot.send_message(message.chat.id,
                               '<b>Ваши данные\n'
                               'Фамилия: '+user.surname+'\n'
                               'Имя: '+user.name+'\n'
                               'Должность: '+user.status+'\n'
                               'Почта: '+user.email+'\n'
                               'Ключ от почты: '+user.email_key+'</b>',
                               parse_mode='html', reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def add_user(message):
    # подключаемся к базе данных
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    chat_id = message.chat.id
    user = user_dict[chat_id]

    if user.status == 'Джуниор':
        working_group = 'A'
    elif user.status == 'Мидл':
        working_group = 'B'
    elif user.status == 'Сеньор':
        working_group = 'C'
    id = int(message.from_user.id)

    # создаем новую запись в таблице
    new_record = (user.surname, user.name, user.status, id, working_group, user.email, user.email_key)
    cursor.execute(
        "INSERT INTO users (surname, name, status, id, working_group, email, email_key) VALUES (?, ?, ?, ?, ?, ?, ?)",
        new_record)

    # сохраняем изменения
    conn.commit()

    # закрываем соединение с базой данных
    conn.close()

def emailing(message):
    try:
        chat_id = message.chat.id
        user_email[chat_id] = These_email(message.text)

        hide_button = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id,
                               '<b>Укажите почту получателя:</b>',
                               parse_mode='html', reply_markup=hide_button)
        bot.register_next_step_handler(msg, get_recipient)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def get_recipient(message):
    try:
        chat_id = message.chat.id
        email_data = user_email[chat_id]
        email_data.recipient = message.text

        msg = bot.send_message(message.chat.id,
                               '<b>Укажите тему письма:</b>',
                               parse_mode='html')
        bot.register_next_step_handler(msg, get_subject)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def get_subject(message):
    try:
        chat_id = message.chat.id
        email_data = user_email[chat_id]
        email_data.title = message.text

        msg = bot.send_message(message.chat.id,
                               '<b>Напишите содержимое письма:</b>',
                               parse_mode='html')
        bot.register_next_step_handler(msg, get_email_content)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def get_email_content(message):
    try:
        chat_id = message.chat.id
        email_data = user_email[chat_id]
        email_data.email_content = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_send = types.KeyboardButton('Отправить')
        button_retry = types.KeyboardButton('Написать письмо заново')
        markup.add(button_send, button_retry)

        msg = bot.send_message(message.chat.id,
                               '<b>Данные письма\n'
                               'Получатель: '+email_data.recipient+'\n'
                               'Заголовок: '+email_data.title+'\n'
                               'Содержимое: '+email_data.email_content+'</b>',
                               parse_mode='html', reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def send_email(message):

    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    id = int(message.from_user.id)

    query = f"SELECT email, email_key FROM users WHERE id='{id}'"
    cursor.execute(query)
    result = cursor.fetchone()

    sender_email = result[0]
    sender_email_key = result[1]

    chat_id = message.chat.id
    email_data = user_email[chat_id]
    recipient_email = email_data.recipient
    title = email_data.title
    email_content = email_data.email_content

    conn.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender_email, sender_email_key)
        msg = MIMEText(email_content)
        msg["Subject"] = title
        server.sendmail(sender_email, recipient_email, msg.as_string())

        bot.send_message(message.chat.id,parse_mode='html', reply_markup=markup)

    except Exception as _ex:
        return f"{_ex}\nCheck you login or password please!"

@bot.message_handler(content_types=['text'])
def bot_get_message(message):


    if message.text == 'Регистрация':
        registration(message)

    elif message.text == 'Помощь':
        help(message)

    elif message.text == 'О нас':
        about(message)

    elif message.text == 'Местоположение':
        location(message)

    elif message.text == 'Комнаты нашего офиса':
        rooms(message)

    elif message.text == 'Вернуться в "О нас"':
        about(message)

    elif message.text == 'Вернуться в главное меню':
        start(message)

    elif message.text == 'Все верно':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_send_doc = types.KeyboardButton('Отправить файлы')
        button_send_an_email = types.KeyboardButton('Написать письмо')
        button_get_doc = types.KeyboardButton('Получить файлы')
        button_about = types.KeyboardButton('О нас')
        button_help = types.KeyboardButton('Помощь')
        markup.add(button_send_doc, button_send_an_email, button_get_doc, button_about, button_help)
        add_user(message)
        bot.send_message(message.chat.id, 'Вы зарегистрированы', reply_markup=markup)


    elif message.text == 'Нет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_try_reg = types.KeyboardButton('Зарегистрироваться снова')
        button_menu = types.KeyboardButton('Вернуться в главное меню')
        markup.add(button_try_reg, button_menu)

        bot.send_message(message.chat.id, 'Вы можете повторить попытку или вернуться в главное меню', reply_markup=markup)

    elif message.text == 'Зарегистрироваться снова':
        registration(message)

    elif message.text == 'Вернуться в главное меню':
        start(message)

    elif message.text == 'Написать письмо':
        emailing(message)

    elif message.text == 'Отправить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_send_doc = types.KeyboardButton('Отправить файлы')
        button_send_an_email = types.KeyboardButton('Написать письмо')
        button_get_doc = types.KeyboardButton('Получить файлы')
        button_about = types.KeyboardButton('О нас')
        button_help = types.KeyboardButton('Помощь')
        send_email(message)
        markup.add(button_send_doc, button_send_an_email, button_get_doc, button_about, button_help)
        bot.send_message(message.chat.id, '<b>Письмо отправлено</b>', parse_mode='html', reply_markup=markup)

    elif message.text == 'Написать письмо заново':
        emailing(message)

    elif message.text == 'Отправить файлы':
        handle_message(message)

    elif message.text == 'Получить файлы':
        handle_doc(message)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'office':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back_about = types.KeyboardButton('Вернуться в "О нас"')
        markup.add(button_back_about)
        bot.send_photo(call.message.chat.id, photo=open("office.jpg", 'rb'),
                       caption='<b>На 2 этаже находится рабочая зона, где и предстоит нам писать код, который никак не '
                               'хочет работать.</b>',
                       parse_mode='html', reply_markup=markup)

    elif call.data == 'kitchen':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back_about = types.KeyboardButton('Вернуться в "О нас"')
        markup.add(button_back_about)
        bot.send_photo(call.message.chat.id, photo=open("kitchen.jpg", 'rb'),
                       caption='<b>На 3 этаже находится кухня, где вы можете перекусить.</b>',
                       parse_mode='html', reply_markup=markup)

    elif call.data == 'entertainment':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back_about = types.KeyboardButton('Вернуться в "О нас"')
        markup.add(button_back_about)
        bot.send_photo(call.message.chat.id, photo=open("entertainment.jpg", 'rb'),
                       caption='<b>На 4 этаже находится комната развлечений, где можно отдохнуть от работы и показать, '
                               'кто лучше играет в пинг понг.</b>',
                       parse_mode='html', reply_markup=markup)

    elif call.data == 'rest':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back_about = types.KeyboardButton('Вернуться в "О нас"')
        markup.add(button_back_about)
        bot.send_photo(call.message.chat.id, photo=open("rest.jpg", 'rb'),
                       caption='<b>На 4 этаже находится комната отдыха, где можно вместе с коллегами отдохнуть и '
                               'обсудить новости из реального мира :).</b>',
                       parse_mode='html', reply_markup=markup)

    elif call.data == 'other':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back_about = types.KeyboardButton('Вернуться в "О нас"')
        markup.add(button_back_about)
        bot.send_photo(call.message.chat.id, photo=open("other.jpg", 'rb'),
                       caption='<b>Если вы не знаете куда вам идти, то можно спросить на ресепшене. Вам точно '
                               'помогут.</b>',
                       parse_mode='html', reply_markup=markup)

def help(message):
    bot.send_message(message.chat.id,
                     '<b>Привет! Этот бот позволяет облегчить работу в нашей компании и быстро адаптироваться нашим '
                     'новым сотрудникам.</b>',
                     parse_mode='html')

def about(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_location = types.KeyboardButton('Местоположение')
    button_rooms = types.KeyboardButton('Комнаты нашего офиса')
    button_menu = types.KeyboardButton('Вернуться в главное меню')
    markup.add(button_location,button_rooms, button_menu)
    bot.send_message(message.chat.id, '<b>Компания "Айти мир" это лучшее убежище для программистов, где они могут '
                                      'комфортно писать код.</b>',
                     parse_mode='html', reply_markup=markup)

def location(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_about = types.KeyboardButton('Вернуться в "О нас"')
    button_menu = types.KeyboardButton('Вернуться в главное меню')
    markup.add(button_about, button_menu)
    bot.send_photo(message.chat.id, photo=open("build.jpg", 'rb'),
                   caption='<b>Компания "Айти мир" находится в Екатеринбурге по адресу: ул.8 март,62/45.</b>',
                   parse_mode='html', reply_markup=markup)

def rooms(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    office = types.InlineKeyboardButton('Офис', callback_data='office')
    kitchen = types.InlineKeyboardButton('Кухня', callback_data='kitchen')
    entertainment = types.InlineKeyboardButton('Развлечения', callback_data='entertainment')
    rest = types.InlineKeyboardButton('Отдых', callback_data='rest')
    other = types.InlineKeyboardButton('Прочее', callback_data='other')

    markup.add(office, kitchen, entertainment, rest, other)
    bot.send_message(message.chat.id,
                     '<b>Наш офис предоставляет всем сотрудникам самые лучшие условия для работы.'
                     '\nЗдесь находится все необходимое: от кухни первоклассного уровня до комнаты развлечений, '
                     'где вы можете отдохнуть.</b>',
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['Отправить файлы'])
def handle_message(message):
    if message.text == 'Отправить файлы':
        bot.reply_to(message, '<b>Отправь мне кому нужно выдать задание со всеми необходимыми файлами.</b>',
                     parse_mode='html')
        bot.register_next_step_handler(message, process_media)

def process_media(message):

    last_name = message.caption.split()[0]

    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE surname=?", (last_name,))
    result = cursor.fetchone()

    if result is not None:
        user_id = result[0]

        if message.document:
            file_id = message.document.file_id
            file_name = message.document.file_name
        elif message.photo:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_name = file_info.file_path.split('/')[-1]
        elif message.video:
            file_id = message.video.file_id
            file_info = bot.get_file(file_id)
            file_name = file_info.file_path.split('/')[-1]

        message_text = ' '.join(message.caption.split()[1:])

        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_content = sqlite3.Binary(downloaded_file)
        received = 0

        cursor.execute('INSERT INTO documents (user_id, file_id, file_name, file_content, message_text, received) VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, file_id, file_name, file_content, message_text, received))
        conn.commit()


        bot.reply_to(message, f'Документ и сообщение отправлены сотруднику {last_name}')
    else:
        bot.reply_to(message, f'Сотрудник с фамилией {last_name} не найден')

@bot.message_handler(commands=['Получить файлы'])
def handle_doc(message):

    user_id = message.from_user.id

    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE user_id=? AND received=0", (user_id,))
    result = cursor.fetchall()

    if len(result) > 0:
        for row in result:
            file_name = row[2]
            file_content = row[3]
            message_text = row[4]
            received = row[5]

            # Проверяем значение received
            if received == 0:
                received_text = "✔️ Получено"

            document_info = f"Название файла: {file_name}\nСообщение: {message_text}\nСтатус получения: {received_text}"
            bot.send_message(message.chat.id, "<b>"+ document_info +"</b>", parse_mode='html')

            bot.send_document(message.chat.id, file_content, caption=file_name)

        cursor.execute("UPDATE documents SET received=1 WHERE user_id=? AND received=0", (user_id,))
        conn.commit()
        conn.close()
        # Отправляем пользователю список документов
        bot.send_message(message.chat.id, "<b>Все документы успешно получены</b>", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "<b>У вас нет новых документов</b>", parse_mode='html')

bot.polling(none_stop=True)