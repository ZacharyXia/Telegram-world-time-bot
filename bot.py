import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from datetime import datetime
import pytz
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm group world time bot, please add me into a group!")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    infoText = '''A convenient Telegram bot designed to enhance communication in global chat groups. 
This bot can be easily added to any group and is capable of managing multiple time zones. 
For any inquiry or feedback, please contact zachary.xia@student.unsw.edu.au '''
    await context.bot.send_message(chat_id=update.effective_chat.id, text=infoText)

async def showTimeZone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = str(context._chat_id)
    with open('groupData.json', 'r') as file:
        jsonData = json.load(file)

    # Append query.data to the list corresponding to chatID
    # This will create the list if chatID doesn't exist
    if chatID not in jsonData:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="There is no timezone added in this chat!")
        return
    else:
        timeTable = ''
        for city in jsonData[chatID]:
            cityName = city.split("/")
            timeTable += f'{cityName[1]}:\n'
            timeTable += f'{datetime.now(pytz.timezone(city)).strftime("%X    %d %B")}\n'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=timeTable)

        
async def addTimeZone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (len(context.args) == 0):
       await context.bot.send_message(chat_id=update.effective_chat.id, text="Incorrect argument number.\nUseage: /addtimezone countryname")
       return
    
    countryName = ''
    for i in range(len(context.args)):
        if (i >= 1):
            countryName += ' '
        countryName += context.args[i].capitalize()
    countryKey = None

    for key, val in pytz.country_names.items():
        if val == countryName:
            countryKey = key
            break
    if countryKey == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid country name! That can because of typo or using language other than English.")
        return

    keyboard = []
    for i in range(len(pytz.country_timezones[countryKey])):
        keyboard.append([InlineKeyboardButton(f"{pytz.country_timezones[countryKey][i]}", callback_data=f"{pytz.country_timezones[countryKey][i]}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose a city:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    chatID = str(context._chat_id)
    with open('groupData.json', 'r') as file:
        jsonData = json.load(file)

    # Append query.data to the list corresponding to chatID
    # This will create the list if chatID doesn't exist
    if chatID not in jsonData:
        jsonData[chatID] = []
    if query.data in jsonData[chatID]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="This city is already existed in this chat.")
        return
    jsonData[chatID].append(query.data)

    # Write the updated JSON data back to the file
    with open('groupData.json', 'w') as file:
        json.dump(jsonData, file, indent=4)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"All done! {query.data} has been added to this chat!")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def removeTimeZone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (len(context.args) == 0):
       await context.bot.send_message(chat_id=update.effective_chat.id, text="Incorrect argument number.\nUseage: /removetimezone cityname")
       return
    
    cityName = ''
    for i in range(len(context.args)):
        if (i >= 1):
            cityName += '_'
        cityName += context.args[i].capitalize()
    chatID = str(context._chat_id)
    with open('groupData.json', 'r') as file:
        jsonData = json.load(file)
    if chatID not in jsonData:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="There is no timezone added in this chat!")
        return
    
    for city in jsonData[chatID]:
        name = city.split("/")
        if cityName == name[1]:
            jsonData[chatID].remove(city)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{cityName} has been removed from this chat")
            with open('groupData.json', 'w') as file:
                json.dump(jsonData, file, indent=4)
            return
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{cityName} didn't find in this chat.")
    return

if __name__ == '__main__':
    
    application = ApplicationBuilder().token('6711537357:AAEKVTtG0FOuABQnsgkKYJQ5Xlx3fUZ7OHw').build()
    
    starthandler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    addTimeZoneHandler = CommandHandler('addtimezone', addTimeZone)
    buttonHandler = CallbackQueryHandler(button)
    showTimeZoneHandler = CommandHandler('showTimeZone', showTimeZone)
    infoHandler = CommandHandler('info', info)
    removeTimeZoneHandler = CommandHandler('removetimezone', removeTimeZone)


    application.add_handler(starthandler)
    application.add_handler(buttonHandler)
    application.add_handler(addTimeZoneHandler)
    application.add_handler(caps_handler)
    application.add_handler(showTimeZoneHandler)
    application.add_handler(infoHandler)
    application.add_handler(removeTimeZoneHandler)
    
    application.run_polling()