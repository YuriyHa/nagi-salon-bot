
from telebot import types
import telebot 
import config
import db
from datetime import datetime


bot = telebot.TeleBot(config.API_TOKEN)

            # GENERAL DEFS
def chooseOrderType(message: types.Message): 
    ord_types = db.select_all_types()[0]
    haveWrite = False
    for i in ord_types: 
        if message.text ==i : 
            haveWrite = True

    if haveWrite: 
        hideBoard = types.ReplyKeyboardRemove()
        golater = translate(db.read_sqlite_table(message.from_user.id)[0], 'напишите подробности ващего заказа(длину, время, цвети и так далее)', 'Buyurtma tafsilotlarini yozing (uzunlik, rang va boshqalar)', 'write the details of your order (length, color and so on)')

        types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, golater, reply_markup=hideBoard)
        bot.register_next_step_handler(message, forwardToAdmin)
        negative = types.InlineKeyboardButton('отклонить', callback_data='negative' + str(message.from_user.id))
        write_answer = types.InlineKeyboardButton('написать', callback_data='write' + str(message.from_user.id))
        mark = types.InlineKeyboardMarkup().add( negative, write_answer)

        bot.send_message(config.admin_token, 'пользователь @'+message.from_user.username+" хочет записаться на: ")
        bot.send_message(config.admin_token, message.text, reply_markup = mark)

    else:
        text = translate(db.read_sqlite_table(message.from_user.id), 'неправильно, попробуйте снова',  "noto'g'ri, qaytadan urinib ko'ring", "wrong, try again")
        bot.send_message(message.from_user.id, text)
        bot.register_next_step_handler(message, chooseOrderType)
def Callback_toInt(callb, starts): 
    ff = int(callb.replace(starts, ''))
    return ff
def forwardToAdmin(message: types.Message): 

    standart= config.standart_keyboarddef()
    result= db.read_sqlite_table(message.from_user.id)
    wait = translate(result[0], 'пожалуйста, подождите пока админ ответит вам','Iltimos, admin sizga javob berishini kuting' ,'please wait for the admin to answer you')
    bot.send_message(message.from_user.id, wait, reply_markup=standart)

    bot.send_message(config.admin_token,'@' +message.from_user.username + ' :' + message.text)
def translate(id, ru, uzb, eng): 

    if (id == 1): 
        return ru
    elif(id == 2): 
        return uzb 
    else: 
        return eng
###########################################
            #general commands

@bot.message_handler(commands=["instruction"])
def instrdef(message: types.Message): 
    instt = "/instruction"
    makedef = "\"/makeorder\""
    Result = db.read_sqlite_table(message.from_user.id)
    ru = instt + ": инструкции использования бота\n*Если хотите сделать заказ можете ввести команду " + makedef + ", после этого вы получите сообщение \"выберите вид услуги, через `клавиатуру`\" через встроенную клавиатуру выбираете тип заказа, после этого пишете подробности, мы отправляем это админу, и скоро админ вам ответит!/если пришел положительный ответ можете нажать на кнопку \"продолжить разговор\""
    uz = instt + ": botdan foydalanish bo'yicha ko'rsatmalar \n * Agar siz buyurtma berishni xohlasangiz," + makedef + "buyrug'ini kiritishingiz mumkin, shundan so'ng siz \"xabarini olasiz, xizmat turini tanlang, klaviaturadan foydalaning\" Buyurtma turini tanlash uchun o'rnatilgan klaviatura orqali, keyin tafsilotlarni yozing, biz uni adminga yuboramiz va admin tez orada sizga javob beradi!"
    eng = instt + ": instructions for using the bot \n * If you want to place an order, you can enter the command" + makedef + ", after that you will receive the message \"select the type of service, use the `keyboard`\" through the built-in keyboard to select the type of order, then write details, we send it to the admin, and the admin will answer you soon!"
    bot.send_message(message.from_user.id, translate(Result[0], ru, uz, eng))


@bot.message_handler(commands=['start'])
def welcome(message:types.Message):
    bot.send_message(message.chat.id, 'Start!',reply_markup=config.standart_keyboarddef())
    if (not db.user_in_base(message.from_user.id)): 
        ru = types.InlineKeyboardButton('RUS', callback_data= 'lan1')
        uz = types.InlineKeyboardButton('UZB', callback_data= 'lan2')
        eng = types.InlineKeyboardButton('ENG', callback_data= 'lan3')
        inline_addOrder_m = types.InlineKeyboardMarkup().add(ru, uz, eng)
        bot.send_message(message.from_user.id, 'ЗДРАВСТВУЙТЕ ' + message.from_user.username + "!\nпожалуйста, выберите язык", reply_markup=inline_addOrder_m)
    else: 
        result = db.read_sqlite_table(message.from_user.id)

        ru ='Здравствуйте, ' + message.from_user.first_name + "\nЯ - бот который помогает клиетам салона \"NAGI Salon\", связаться с администраторами"

        uz = "Men \"NAGI Salon\" salonining mijozlariga ma'murlar bilan bog'lanishiga yordam beradigan botman"

        eng = 'WELCOME ' + message.from_user.first_name + "\nI`m a telegram bot, who helps clients of the salon \"NAGI Salon\" to contact the administrators!"
        aaa = translate(result[0], ru, uz, eng)
        message_text = aaa

        languageTranslate = translate(result[0], 'сменить язык', 'tildi almashtirish', 'change language')
        changeLanguage = languageTranslate

        keshbackTrancslate = translate(result[0], 'скидки', 'skidka', 'keshback')
        keshback = keshbackTrancslate

        orderTranslate = translate(result[0], 'сделать заказ', 'zakaz qilish', 'make an order')
        makeOrder = orderTranslate

        lanbutton = types.InlineKeyboardButton(text = changeLanguage, callback_data= 'chl')
        keshbackbutton = types.InlineKeyboardButton(keshback, callback_data = 'kesh')
        orderButton = types.InlineKeyboardButton(makeOrder, callback_data='ord')

        inline_addOrder_m =types.InlineKeyboardMarkup().add(lanbutton, keshbackbutton).add(orderButton)
        bot.send_message( message.from_user.id, message_text, reply_markup=inline_addOrder_m)
        commandsdef(message)
        
@bot.message_handler(commands=['commands'])
def commandsdef(message: types.Message): 
    result = db.read_sqlite_table(message.from_user.id)
    bot.send_message(message.from_user.id, translate(result[0], "/commands - список команд бота\n/start - начать!\n/makeorder - сделать заказ\n/language - сменить язык\n/keshback - скидки", "/ buyruqlar - bot buyruqlari ro'yxati \n /start- boshlash! \n /makeorder - buyurtma berish \n /language - tilni o'zgartirish \n /keshback - chegirmalar", "/commands - list of bot commands \n /start - start! \n/makeorder - place an order \n /language - change language \n /keshback - discounts"))
    statisticsdef(message)


@bot.message_handler(commands=['language'])
def textEdition(message: types.Message): 

    result = db.read_sqlite_table(message.from_user.id) 
    message_text = translate(result[0], 'выберите язык на котором вам удобно общаться', "muloqot qilish uchun qulay bo'lgan tilni tanlang", 'choose the language in which it is convenient for you to communicate')
    
    ru = types.InlineKeyboardButton('RUS', callback_data= 'nlan1')
    uz = types.InlineKeyboardButton('UZB', callback_data= 'nlan2')
    eng = types.InlineKeyboardButton('ENG', callback_data= 'nlan3')
    markub = types.InlineKeyboardMarkup().add(ru, uz, eng)
    bot.send_message(message.chat.id, message_text, reply_markup=markub)

@bot.message_handler(commands=['admin'])
def admindef(message: types.Message): 
    continueConversation(message)

###############################################
###############################################
############/STATISTICS COMMANDS
    
def doStatistics_client(message:types.Message, date_time):
    clientlist = db.return_byTime("'start of " + date_time+ "'", datetime.now(), "`user_name`")
    index = 1
    querytext = ''
    for column in clientlist: 
        strindex = str(index)
        strcount = str(column[2])
        querytext = querytext +  "\n\n" + strindex + '. username: @' + column[0] + "\n - order count: " + strcount + "\n - last order time: " + column[1]
        index += 1
    bot.send_message(message.from_user.id, "/statistics📈(" + date_time+ ") : \n10 clients which had do the order at this " + date_time+ ":")
    bot.send_message(message.from_user.id, querytext)
def doStatistics_order(message:types.Message, date_time):
    clientlist = db.return_byTime("'start of " + date_time+ "'", datetime.now(), "`order_type`")
    index = 1
    querytext = ''
    for column in clientlist: 
        strindex = str(index)
        strcount = str(column[2])
        querytext = querytext +  "\n\n" + strindex + '. order: ' + column[0] + "\n - count: " + strcount + "\n - last time: " + column[1]
        index += 1
    bot.send_message(message.from_user.id, "/statistics📈(" + date_time+ ") : \norders which had having more client(!limit 10!) " + date_time+ ":")
    bot.send_message(message.from_user.id, querytext)

@bot.message_handler(commands=["statistics"])
def statisticsdef(message: types.Message): 
    result = db.read_sqlite_table(message.from_user.id)
    orderlist = db.return_byTime("'start of " + "year"+ "'", datetime.now(), "`order_type`")
    theorder = "\n --order: "  + orderlist[0][0] + "\n--count: " + str(orderlist[0][2])+ "\n--last time: " + orderlist[0][1]
    statext = "-/statistics📈 - commands:\n~order commands:" + translate(result[0], "\n/dayorder - наичастеший заказ за этот день\n/monthorder - в месяц\n/yearorder - в год", "\n /dayorder - bu kun uchun qisman buyurtma \n /monthorder - oyiga \n /yearorder - yiliga", "\n /dayorder - partial order for this day \n /monthorder - per month \n /yearorder - per year")
    bot.send_message(message.from_user.id, statext)
    ordertext= translate(result[0] , "-✅самые частые заказы/", "-✅eng kop zakaz/", "-✅order with more count/")
    bot.send_message(message.from_user.id, ordertext + theorder)

@bot.message_handler(commands=['dayorder'])
def dayorderdef(message:types.Message): 
    doStatistics_order(message, "day")

@bot.message_handler(commands=['monthorder'])
def monthorderdef(message: types.Message): 
    doStatistics_order(message, "month")

@bot.message_handler(commands=['yearorder'])
def yearorderdef(message: types.Message): 
    doStatistics_order(message, "year")

@bot.message_handler(commands = ['dayclient'])
def dayclientdef(message: types.Message):
    doStatistics_client(message, "day")

@bot.message_handler(commands=['monthclient'])
def monthclientdef(message: types.Message): 
    doStatistics_client(message, "month")

@bot.message_handler(commands=['yearclient'])
def yearclientdef(message: types.Message): 
    doStatistics_client(message, "year")

@bot.message_handler(commands=['makeorder'])
def makeorderdef(message: types.Message): 
    order_type_list = db.select_all_types()[0]
    result= db.read_sqlite_table(message.from_user.id)
    choose =translate(result[0],'выберите вид услуги, через `клавиатуру`', 'Buyurtmani yozing yoki "klaviatura"ni tanlang', 'write your order or select via the `keyboard`')
    order_types_m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in order_type_list: 
        new_button = types.KeyboardButton(i)
        order_types_m.add(new_button)
    types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, choose, reply_markup=order_types_m)
    bot.register_next_step_handler(message, chooseOrderType)

@bot.callback_query_handler(lambda c: c.data == 'ord')
def make_order(call:types.CallbackQuery): 
    order_type_list = db.select_all_types()[0]
    result= db.read_sqlite_table(call.from_user.id)
    choose =translate(result[0],'выберите вид услуги, через `клавиатуру`', 'Buyurtmani yozing yoki "klaviatura"ni tanlang', 'write your order or select via the `keyboard`')
    order_types_m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in order_type_list: 
        new_button = types.KeyboardButton(i)
        order_types_m.add(new_button)
        if i == order_type_list[(len(order_type_list)-1)]: 
            print ('last order type!')
            bot.send_message(call.from_user.id, choose, reply_markup=order_types_m)
            bot.register_next_step_handler(call.message, chooseOrderType)

# @bot.message_handler(commands=['statistics'])
# def botcammands(message: types.Message): 
#     reb = db.read_sqlite_table()
#     text  = translate(reb[0], "")
#     bot.send_message(message.from_user.id, '')

# def monthClient(): 
#     db.createExecute('SELECT')
#######################################
######################################
########################################
#######################CALLBACK HANDLERS

@bot.callback_query_handler(lambda c:c.data=='chl')
def get_nlan(call: types.CallbackQuery): 
    ru = types.InlineKeyboardButton('RUS', callback_data= 'nlan1')
    uz = types.InlineKeyboardButton('UZB', callback_data= 'nlan2')
    eng = types.InlineKeyboardButton('ENG', callback_data= 'nlan3')
    markub = types.InlineKeyboardMarkup().add(ru, uz, eng)

    result = db.read_sqlite_table(call.from_user.id)
    message_translation = translate(result[0], 'выберите язык', 'tildi tanlang', 'choose language')
    message_text = message_translation
    print ('translate succsesfuled')
    bot.send_message(call.from_user.id, message_text, reply_markup= markub)

@bot.callback_query_handler(lambda c: c.data.startswith('lan'))
def language(call: types.CallbackQuery): 
    if (call.data == 'lan1'): 
        db.add_user(call.from_user.id, call.from_user.username, 1)
        m1 = types.InlineKeyboardButton('сменить язык', callback_data= 'nlan1')
        m2 = types.InlineKeyboardButton('скидки', callback_data= 'kesh')
        m3 = types.InlineKeyboardButton('первый заказ', callback_data='ord')
        markub = types.InlineKeyboardMarkup().add(m1, m2)
        markub.add(m3)
        bot.send_message(call.from_user.id, 'Здравствуйте!, @' + call.from_user.username + "\nЯ - бот, который помогает клиетам салона \"NAGI Salon\", связаться с администраторами!", reply_markup=markub)
            
    if (call.data == 'lan2'): 
        db.add_user(call.from_user.id, call.from_user.username, 2)
        bot.send_message(call.from_user.id, "Men \"NAGI Salon\" salonining mijozlariga ma'murlar bilan bog'lanishiga yordam beradigan botman")
    if (call.data == 'lan3'): 
        db.add_user(call.from_user.id, call.from_user.username, 3)
        m1 = types.InlineKeyboardButton('change language', callback_data= 'nlan')
        m2 = types.InlineKeyboardButton('keshback', callback_data= 'kesh')
        m3 = types.InlineKeyboardButton('first orders!', callback_data='ord')
        markub = types.InlineKeyboardMarkup().add(m1, m2)
        markub.add(m3)
        bot.send_message(call.from_user.id, 'Welcome, @' + call.from_user.username + "\nI`m a telegram bot, \
            who helps clients of the salon \"NAGI Salon\" to contact the administrators!", reply_markup= markub)
    instrdef(call.message)
#######################################################################################
@bot.callback_query_handler(lambda c: c.data.startswith('nlan'))
def change_language(call: types.CallbackQuery): 
    if call.data == 'nlan1': 
        db.update_data(call.from_user.id, 'lan', 1)
        bot.send_message(call.from_user.id, 'вы успешно поменяли язык!')
    if call.data == 'nlan2': 
        db.update_data(call.from_user.id, 'lan', 2)
        bot.send_message(call.from_user.id, 'siz tilni muvaffaqiyatli tushundingiz!')
    if call.data == 'nlan3': 
        db.update_data(call.from_user.id, 'lan', 3)
        bot.send_message(call.from_user.id, 'you have successfully understood the language!')

@bot.callback_query_handler(lambda c: c.data == 'kesh')
def kesh(call: types.CallbackQuery):
     
    result = db.read_sqlite_table(call.from_user.id)
    kesh0 = translate(result[0], '/kesh, ваша скидка на данный момент состовляет ' + str(result[2]) +'% ', "sizning hozirgi chegirmangiz" + str(result[2] )+ '%', "your keshback is " + str(result[2]) + '%')
    kesh1 = translate(result[0], 'что бы получить скидку в 30%, вам нужно три раза подряд воспользоваться нашими услугами!',"keyin siz 30% /chegirmaga ega bo'lar edingiz, siz bizning xizmatlarimizni ketma -ket uch marta ishlatishingiz kerak!", "then you would get a 30% /discount, you need to use our services three times in a row!")
    kesh2 =translate(result[0], 'что бы получить скидку в 50% после начала вам нужно восемь раз подряд воспользоваться нашим/и услугами!(только после начала!)', "boshlanganidan keyin 50%/ chegirma olish uchun siz bizning xizmatlarimizdan ketma -ket sakkiz marta foydalanishingiz kerak! (faqat boshlanganidan keyin!)", "to get a 50% /discount after the start, you need to use our / and services eight times in a row! (only after the start!)")
    kesh3 =translate(result[0], 'что бы получить скидку в 40% вы можете прийти со своей подругой!', "40% /chegirma olish uchun siz qiz do'stingiz bilan kelishingiz mumkin!", "to get a 40% /discount, you can come with your friend!")
    kesh4 =translate(result[0], 'что бы получить скидку в 45% вы можете прийти с двумя своими подругами!',"45% /chegirma olish uchun siz ikki do'stingiz bilan kelishingiz mumkin!", "to get a 45%/ discount, you can bring two of your friends!")
    keshs = [kesh0, kesh1, kesh2, kesh3, kesh4]# поотм сделать с базой данный и добавлением админа 
    for i in keshs: 
        bot.send_message(call.from_user.id, i)

# @bot.callback_query_handler(lambda c: c.data.startswith('done'))
# def done(call: types.CallbackQuery): 
#     user_id=  Callback_toInt(call.data, 'done')
#     result = db.read_sqlite_table(user_id)
#     board= types.ReplyKeyboardMarkup(resize_keyboard= True)
#     yes = types.KeyboardButton('yes')
#     no = types.KeyboardButton('no')
#     board.add(yes, no)
#     text = translate(result[0], 'отлично, хотите обсудить подробности(время, место, и т.д)?\n (yes/ no)', 'ajoyib, tafsilotlarni (vaqt, joy) muhokama qilmoqchimisiz?\n(yes/ no)','great, would you like to discuss the details (time, place)?\n(yes/ no)')
#     bot.register_next_step_handler(call.message, later)
#     bot.send_message(user_id, text, reply_markup=board)
#     current_time = datetime.now()
#     db.add_time(user_id, result[1], current_time, call.message.text)
#     print ('ID: ',user_id)
#     print('USERNAME: ', result[1])
#     print('TIME: ', current_time)
#     print('TEXT: ', call.message.(
@bot.message_handler(commands=['am'])
def am(message:types.Message): 
    userorderslist = db.returnData("SELECT `order_type`, date(`time`) FROM `occurred_at` where `user_id`= ?", (message.from_user.id, ))
    readtable = db.read_sqlite_table(message.from_user.id)
    text = "id: " + str(readtable[4]) + "\norders: "
    for column in userorderslist: 
        text = text + "\n-" + column[0] + ", time - " + column[1]
    bot.send_message(message.from_user.id, text)


@bot.callback_query_handler(lambda c : c.data.startswith('negative'))
def negative(call: types.CallbackQuery): 
    user_id=  Callback_toInt(call.data, 'negative')
    result = db.read_sqlite_table(user_id)
    text = translate(result[0], "проститеб но у админа не было времени, попробуйте написать попоже", "Kechirasiz, lekin adminning vaqti yo'q edi, yana yozishga urinib ko'ring", "sorry, but the admin did not have time, try to write again")
    bot.send_message(user_id, text)

@bot.callback_query_handler(lambda c: c.data.startswith('write'))
def write_answer_admin(call: types.CallbackQuery): 
    user_id = Callback_toInt(call.data, 'write')
    res = db.read_sqlite_table(user_id)
    bot.send_message(call.from_user.id, 'напишите сообщение')

    def Answer(message: types.Message):
        db.add_time(user_id, res[1], datetime.now(), call.message.text)
        
        m3 = types.InlineKeyboardMarkup()
        mb31= types.InlineKeyboardButton(translate(res[0], 'продолжить разговор', 'suhbatni davom ettiring', 'continue the conversation'), callback_data="admin")
        m3.add(mb31)
        bot.send_message(user_id, translate(res[0], 'ответ администратора (полоцительный): ', "ma'mur javobi (ijobiy)", "administrator response (positive)" ) + '\n' + message.text, reply_markup=m3)
        bot.reply_to(call.message, 'клиентка пришла?(это для базы данных)')
        mb41 = types.KeyboardButton('да')
        mb42 = types.KeyboardButton('нет')
        m4 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(mb41, mb42)
        bot.send_message(call.from_user.id, 'ответ выслан пользователю!', reply_markup=m4)        
        def user_on(message: types.Message): 
            if message.text == "да": 
                buyed_cont = res[3] + 1
                db.update_data(user_id, "buyed_cont", buyed_cont)
                bot.send_message(config.admin_token, 'Круто!', reply_markup=config.standart_keyboarddef())


            elif message.text == "нет": 
                bot.send_message(config.admin_token, 'эхх жаль(', reply_markup=config.standart_keyboarddef())
            else : 
                bot.send_message(config.admin_token, "ой, ошибочка, попробуйте снова")
                bot.register_next_step_handler(message, user_on)
        bot.register_next_step_handler(call.message,user_on)

    bot.register_next_step_handler(call.message, Answer)

@bot.callback_query_handler(lambda c: c.data.startswith('adm'))
def continueConversation(call: types.CallbackQuery): 
    bot.send_message(call.from_user.id, translate(db.read_sqlite_table(call.from_user.id)[0], 'для продолжение разговора напишите админу лично!\n наш админ: @', "suhbatni davom ettirish uchun adminga shaxsan yozing! \n bizning admin:", "to continue the conversation, write to the admin personally! \n our admin: ") + "@" + config.admin_username)








######################
###################for
#admins###############
@bot.message_handler(commands=['aot'])
def addOrdertypes(message :types.Message): 
    bot.send_message(message.from_user.id, 'что хотите добавить?')
    bot.register_next_step_handler(message, addOrder)
def addOrder(message: types.Message): 
    db.add_order_types(message.text)
    bot.send_message(message.from_user.id, 'Добавлено!')
@bot.message_handler(commands=['dot'])
def deleteords(message: types.Message): 
    bot.send_message(message.from_user.id, 'напишите индекс услуги которую хотите удалить')
    text = 'услуги по индексам: '
    result = db.select_all_types()
    gr = 0
    for id in result[1]: 
        text += ( '\nID: ' + str(id) + ", вид услуги: " + str(result[0][gr]))
        gr += 1
    bot.send_message(message.from_user.id, text)
    bot.register_next_step_handler(message, delord)
def delord(message: types.Message): 
    try:
        id = int(message.text)
    except:
        bot.send_message('это не ID')
    finally: 
        db.delete_order_types(id)
        bot.send_message(message.from_user.id, "успешно удалено")
bot.polling(non_stop=True)
