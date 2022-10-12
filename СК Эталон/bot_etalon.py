import telebot
from telebot import types
import json
import itertools
from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP

token='здесь должен быть токен'
bot = telebot.TeleBot(token)
proposal={}
proposal['service']=[]
proposal['date']=[]
proposal['time']=[]
with open('inf.json', encoding='utf-8') as config:
    config_data = json.load(config)

def get_all_buttons():
    all_buttons = []
    for keyboard in config_data[1:]:
        for button in keyboard['buttons']:
            all_buttons.append(button)
    return all_buttons
def get_keyboard(keyboard_type):
    if keyboard_type=='main':
        proposal['service']=[]
        proposal['date'] = []
        proposal['time'] = []
    if keyboard_type=="":
        return None
    else:
        kb_info = list(filter(lambda el: el['keyboard_name'] == keyboard_type, config_data[1:]))[0]
        buttons = sorted(kb_info['buttons'], key=lambda el: int(el['position']))
        keyboard = types.InlineKeyboardMarkup()
        if keyboard_type=="date":
            chunked = list(itertools.zip_longest(*[iter(buttons)] * 2))
        else:
            chunked = list(itertools.zip_longest(*[iter(buttons)] * 3))
        for chunk in chunked:
            chunked_btn = []
            for button in list(filter(lambda el: el is not None, chunk)):
                chunked_btn.append(
                    types.InlineKeyboardButton(button['name'],
                                               callback_data=button['id'])
                )
            if len(chunked_btn) == 1:
                keyboard.row(chunked_btn[0])
            elif len(chunked_btn) == 2:
                keyboard.row(chunked_btn[0], chunked_btn[1])
            elif len(chunked_btn) == 3:
                keyboard.row(chunked_btn[0], chunked_btn[1], chunked_btn[2])
        return keyboard

@bot.message_handler(commands=['start'])
def start_bot(message):
    proposal['service'] = []
    proposal['date'] = []
    proposal['time'] = []
    keyboard=get_keyboard('main')
    bot.send_message(message.chat.id, '✂ '+'💋 '+config_data[0]['accost'],reply_markup=keyboard)

@bot.callback_query_handler(func=WMonthTelegramCalendar.func())
def cal(c):
    result, key, step = WMonthTelegramCalendar(locale='ru').process(c.data)
    if not result and key:
        bot.edit_message_text('👉 '+config_data[0]["date_select"],
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"👉 Вы выбрали {result}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=date_calendar)
        proposal['date'].append(str(result))

@bot.callback_query_handler(func=lambda call:True)
def keyboard_answer(call):
    button = list(filter(lambda btn: call.data == btn['id'], get_all_buttons()))[0]
    if button in config_data[1]['buttons'][:-1]:
        proposal['service'].append(button['name'].lower())
    elif button in config_data[2]['buttons'][:-1]:
        proposal['date'].append(button['name'].lower())
    elif button in config_data[3]['buttons'][:-1]:
        proposal['time'].append(button['name'])
    elif button == config_data[1]['buttons'][-1]:
        calendar, step = WMonthTelegramCalendar(locale='ru').build()
        bot.send_message(call.message.chat.id,
                         '👉 '+config_data[0]["date_select"],
                         reply_markup=calendar,
                         parse_mode='html')
        global date_calendar
        date_calendar = calendar
        bot.send_message(
            chat_id=call.message.chat.id,
            text='👉 '+button['to_print'],
            reply_markup=get_keyboard(button['next_keyboard']),
            parse_mode='html')
    elif button in config_data[4]['buttons'] or button['name']=='Далее':
        if button == config_data[2]['buttons'][-1] or button == config_data[4]['buttons'][-1]:
            add_text='👉 '
        elif button == config_data[3]['buttons'][-1]:
            add_text ='<b>👇 Вы выбрали:\nуслуги</b> - %s\n' % ', '.join(proposal['service']) + '<b>даты</b> - %s\n' \
                      % ', '.join(proposal['date']) +'<b>время</b> - %s\n\n' % ', '.join(proposal['time'])
        else:
            add_text='✍'
        bot.send_message(
            chat_id=call.message.chat.id,
            text=add_text+button['to_print'],
            reply_markup=get_keyboard(button['next_keyboard']),
            parse_mode='html'
        )

@bot.message_handler(content_types=['text'])
def direct_message(msg):
    if str(msg.text) not in '123456789':
        proposal['info']=str(msg.text)
        bot.send_message(msg.chat.id, '✌'+config_data[0]['ok'], parse_mode='html')
        to_send_message='<b>Поступила новая заявка:\nуслуги</b> - %s\n' % ', '.join(proposal['service']) + \
                        '<b>даты</b> - %s\n' % ', '.join(proposal['date']) + '<b>время</b> - %s\n' % ', '.join(proposal['time'])\
                        + '<b>информация о клиенте</b> - %s\n' % proposal['info']
        bot.send_message(5187812315, to_send_message, parse_mode='html')

if __name__ == "__main__":
    bot.polling(none_stop=True,interval=0)