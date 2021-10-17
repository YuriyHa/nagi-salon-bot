from telebot import types
API_TOKEN = "1921023958:AAEw6wHmYZ5zgRpGO8yHD0dMElxq1Z6gWT0"
admin_token = '1467382210'
admin_username='NAGI_SALON'

def standart_keyboarddef():
    standart_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ex1 = types.KeyboardButton("/makeorder"); 
    standart_keyboard.add(ex1)
    ex2 = types.KeyboardButton('/language')
    ex3=types.KeyboardButton("/commands")
    ex5 = types.KeyboardButton("/admin")
    ex4 = types.KeyboardButton('/am')
    standart_keyboard.add(ex2, ex3)
    standart_keyboard.add(ex4, ex5)
    return standart_keyboard