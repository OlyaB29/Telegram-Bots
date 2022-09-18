import telebot
from telebot import types

token='5486797592:AAHIPUr-kG-lj3L9RUwMQwaVjJ0ZBVBuZos'
bot = telebot.TeleBot(token)


def create_keyboard(k):
    keyboard1 = types.InlineKeyboardMarkup()
    contacts_btn = types.InlineKeyboardButton(text="Контакты", callback_data='1')
    cons_btn = types.InlineKeyboardButton(text="Заказать консультацию", callback_data='2')
    order_btn = types.InlineKeyboardButton(text="Заказать услугу", callback_data='3')
    keyboard1.add(contacts_btn)
    keyboard1.add(cons_btn)
    keyboard1.add(order_btn)
    keyboard2 = types.InlineKeyboardMarkup()
    coffee_machine_btn=types.InlineKeyboardButton(text="Ремонт кофемашин", callback_data='4')
    washing_machine_btn = types.InlineKeyboardButton(text="Ремонт стиральных машин", callback_data='5')
    dishwasher_btn = types.InlineKeyboardButton(text="Ремонт посудомоечных машин", callback_data='6')
    keyboard2.add(coffee_machine_btn)
    keyboard2.add(washing_machine_btn)
    keyboard2.add(dishwasher_btn)
    if k==1:
        return keyboard1
    elif k==2:
        return keyboard2
@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard=create_keyboard(1)
    bot.send_message(message.chat.id, "Приветствуем Вас в нашем сервисе! Что Вас интересует",reply_markup=keyboard)
@bot.message_handler(content_types=['text'])
def direct_message(msg):
    to_send_message = '<b>Новое сообщение от клиента</b>\n'
    to_send_message += '   Имя клиента: <b>%s</b>\n' % str(msg.from_user.full_name)
    to_send_message += '   Имя ID клиента: <b>%s</b>\n' % str(msg.from_user.id)
    to_send_message += '   Сообщение: <b>%s</b>\n' % str(msg.text)
    bot.send_message(5187812315, to_send_message, parse_mode='html')

@bot.callback_query_handler(func=lambda call:True)
def keyboard_answer(call):
    if call.message:
        if call.data=="1":
            d = open('contacts.txt', 'r')
            bot.send_message(
                chat_id=call.message.chat.id,
                text=d.read(),
                reply_markup=create_keyboard(1))
            d.close()
        if call.data == "2":
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Напишите номер телефона, по которому наш менеджер сможет связться с Вами',
                reply_markup=create_keyboard(1))
        if call.data == "3":
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Ремонт какой техники вас интересует?',
                reply_markup=create_keyboard(2))
        if call.data == "4":
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Напишите модель Вашей кофемашины и вид поломки. Оставьте контактный номер телефона. Мастер свяжется с вами',
                reply_markup=create_keyboard(1))
        if call.data == "5":
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Напишите модель Вашей стиральной машины и вид поломки. Оставьте контактный номер телефона. Мастер свяжется с вами',
                reply_markup=create_keyboard(1))
        if call.data == "6":
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Напишите модель Вашей посудомоечной машины и вид поломки. Оставьте контактный номер телефона. Мастер свяжется с вами',
                reply_markup=create_keyboard(1))

if __name__ == "__main__":
    bot.polling(none_stop=True,interval=0)