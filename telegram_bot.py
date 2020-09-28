# -*- coding: utf-8 -*- 

import numpy as np
import telebot as bt
from telebot import types

bot=bt.TeleBot('token')

users={}

@bot.message_handler(commands=['start'])
def hi(message):
	#keyboar
	markup=types.InlineKeyboardMarkup(row_width=1)
	one=types.InlineKeyboardButton('Начнем',callback_data='start')

	markup.add(one)
	bot.send_message(message.chat.id,('Привет{}! Если тебе было интересно выжил бы ты на Титанике, то я помогу тебе.'.format(message.from_user.first_name)),reply_markup=markup)
	
@bot.message_handler(commands=['again'])
def again_go(message):
	#keyboar
	markup=types.InlineKeyboardMarkup(row_width=1)
	one=types.InlineKeyboardButton('Начнем',callback_data='start')
	markup.add(one)

	bot.send_message(message.chat.id,'Нажимай кнопку',reply_markup=markup)
	

@bot.message_handler(content_types=['text'])
def anket(message):
	try:
		if users[message.chat.id][2]:
			message.text=message.text.replace(',','.')
			if float(message.text)>=0:
				users[message.chat.id].append((float(message.text)/26.8))
				x=[ 0.38579743,  0.30827652,  -0.02129545,   0.00040962]
				answer=round(np.dot(x,users[message.chat.id]))
				
				ancet='Пол-'
				if users[message.chat.id][1]==0:
						ancet+='♂️(мужской)\n'
				else:
					ancet+='♀️(женский)\n'
				ancet+='Класс билета-{}\nТы потратишь на корабле-${}(с учетом инфляции-${})\n\n'.format(users[message.chat.id][2],round(users[message.chat.id][3]*26.8,2),round(users[message.chat.id][3],2))

				if answer==1:
					if users[message.chat.id][1]==0:
						ancet+='Ты бы выжил'
					else:
						ancet+='Ты бы выжилa'
				else:
					if users[message.chat.id][1]==0:
						ancet+='Ты бы умер ☠️'
					else:
						ancet+='Ты бы умерла ☠️'

				mrk=types.InlineKeyboardMarkup(row_width=1)
				again=types.InlineKeyboardButton('Заново',callback_data='again')
				mrk.add(again)
				bot.send_message(message.chat.id,ancet,reply_markup=mrk)

				del users[message.chat.id]#до этого добавить алгоритм и базу данных(это конечная строчка)

			else:
				bot.send_message(message.chat.id,'Введи ЧИСЛО больше нуля')
	except (KeyError,IndexError):

		try:
			users[message.chat.id]
			bot.send_message(message.chat.id,'Ответь на вопросы, которые были до этого')
		except KeyError:
			bot.send_message(message.chat.id,':)')

	except ValueError:
		bot.send_message(message.chat.id,'Введи ЧИСЛО больше нуля')
	except Exception as e:
		bot.send_message(message.chat.id,'ошибка- {err}, напиши пожалуйста об ошибке: https://t.me/NeMoNaklz'.format(err=e))

@bot.callback_query_handler(func=lambda call:True)
def keyboard(call):
	try:
		if call.data=='start':
			mrk=types.InlineKeyboardMarkup(row_width=2)
			man=types.InlineKeyboardButton('♂️(мужской)',callback_data='m')
			woman=types.InlineKeyboardButton('♀️(женский)',callback_data='w')

			mrk.add(man,woman)#,item2)

			bot.send_message(call.message.chat.id,'Выбери пол',reply_markup=mrk)
			bot.delete_message(call.message.chat.id, call.message.message_id-1)
			bot.delete_message(call.message.chat.id, call.message.message_id)
						
		if call.data=='m'or call.data=='w':
			users[call.message.chat.id]=[1]
			if call.data=='m':
				users[call.message.chat.id].append(0)
			else:
				users[call.message.chat.id].append(1)
			markup=types.InlineKeyboardMarkup(row_width=1)
			one=types.InlineKeyboardButton('Первый',callback_data='oneC')
			two=types.InlineKeyboardButton('Второй',callback_data='twoC')
			three=types.InlineKeyboardButton('Третий',callback_data='threeC')

			markup.add(one)#,item2)
			markup.add(two)#,item2)
			markup.add(three)#,item2)
			bot.send_message(call.message.chat.id,'Какой класс ты бы выбрал для путешествия?',reply_markup=markup)
			bot.delete_message(call.message.chat.id, call.message.message_id)
		
		if call.data=='oneC'or call.data=='twoC' or call.data=='threeC':
			if call.data=='oneC':
				users[call.message.chat.id].append(1)
			elif call.data=='twoC':
				users[call.message.chat.id].append(2)
			else:
				users[call.message.chat.id].append(3)

			bot.send_message(call.message.chat.id,'Сколько ты потратишь на корабле?(в долларах)')
			bot.delete_message(call.message.chat.id, call.message.message_id)

		if call.data=='again':
			again_go(call.message)

	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)

#0-male 1-female
#умереть-0.8533526290400386
#[ 0.38579743  0.30827652  -0.02129545   0.00040962]
#		one			sex			pclass		fare
