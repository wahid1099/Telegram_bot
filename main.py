from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = Bot(token="6534040597:AAFlOkO734vy-ibtswI1UDiCgUBKpocndMI")



def welcome(update: Update, context: CallbackContext) -> None:
    new_member = update.message.new_chat_members[0]
    welcome_message = f"Welcome, {new_member.first_name}! Feel free to introduce yourself."
    update.message.reply_text(welcome_message)

def start(update, context):
    update.message.reply_text("Hello sir....")



def remove_links(update: Update, context: CallbackContext) -> None:
    # Get the message text
    message_text = update.message.text

    # Check if the message contains any links
    if any("http" in word for word in message_text.split()):
        # Remove the message containing links
        update.message.delete()
    else:
        # Message doesn't contain links, no action needed
        # update.message.reply_text("You can't send any links....")
        pass
        
        
        
def lock_messages(update: Update, context: CallbackContext) -> None:
    message = update.message
    
    if (message.document or message.audio or message.voice or message.photo or message.video) or message.from_user.is_bot or (message.entities and message.entities[0].type == "bot_command"):
        message.delete()

def send_recurring_message(context: CallbackContext) -> None:
    context.bot.send_message(chat_id=context.job.context, text="This is a recurring message!")

def start_recurring(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    interval = 100 # 1 hour (in seconds)
    
    # Schedule the recurring message
    context.job_queue.run_repeating(send_recurring_message, interval, context=chat_id)

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater(token='6534040597:AAFlOkO734vy-ibtswI1UDiCgUBKpocndMI', use_context=True)
    dispatcher = updater.dispatcher

    # Call the 'welcome' function when a new member joins the group
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
     
    dispatcher.add_handler(CommandHandler('start',start)) 
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, remove_links))
    dispatcher.add_handler(MessageHandler(Filters.all, lock_messages))
    dispatcher.add_handler(CommandHandler('startrecurring', start_recurring))



             

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
