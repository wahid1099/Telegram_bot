import telegram.ext
import random
import string
import logging
from io import BytesIO
from telegram import Update
from PIL import Image, ImageDraw, ImageFont
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to generate a new CAPTCHA
def generate_and_send_captcha(update, context):
    captcha_text = generate_captcha()
    context.user_data['captcha'] = captcha_text
    context.user_data['captcha_verified'] = False

    # Create and send the CAPTCHA image
    captcha_image = create_captcha_image(captcha_text)
    bio = BytesIO()
    captcha_image.save(bio, 'PNG')
    bio.seek(0)

    update.message.reply_photo(photo=bio, caption="Please enter the CAPTCHA to proceed with /start:")

def start(update, context):
    if 'captcha_verified' in context.user_data and not context.user_data['captcha_verified']:
        update.message.reply_text("CAPTCHA verification failed. Please try again with /start.")
    else:
        generate_and_send_captcha(update, context)

def handle_captcha_response(update, context):
    user_input = update.message.text.strip()
    if 'captcha' in context.user_data:
        captcha_text = context.user_data['captcha']
        if user_input.lower() == captcha_text.lower():
            # Correct CAPTCHA
            context.user_data['captcha_verified'] = True
            update.message.reply_text("CAPTCHA verification successful. You can now proceed .")
            # You can perform additional actions for successful verification if needed
        else:
            context.user_data['captcha_verified'] = False  # Set captcha_verified to False for the first attempt
            update.message.reply_text("CAPTCHA verification failed. Please try again with /start.")
            generate_and_send_captcha(update, context)  # Generate and send a new CAPTCHA for the second attempt
    else:
        update.message.reply_text("Please start with /start command to get a CAPTCHA.")


# Function to generate a random CAPTCHA string
def generate_captcha():
    captcha_length = 6
    captcha_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(captcha_chars) for _ in range(captcha_length))


def create_captcha_image(captcha_text):
    image_width = 200
    image_height = 100

    # Create a blank image with white background
    image = Image.new('RGB', (image_width, image_height), color='white')

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Add the CAPTCHA text to the image
    font = ImageFont.truetype("arial.ttf", 30)  # You can adjust the font and size
    text_bbox = draw.textbbox((0, 0), captcha_text, font=font)
    x = (image_width - text_bbox[2] - text_bbox[0]) / 2
    y = (image_height - text_bbox[3] - text_bbox[1]) / 2
    draw.text((x, y), captcha_text, font=font, fill='black')

    return image

def help(update,context):
    update.message.reply_text("""
    The following commands are avilable:
    
    /start -> Welcome to the channel
    /help -> This message
    /contact-> Contact
    
     """)
    


def contact(update, context):
    update.message.reply_text("You can contact on the official mail id")

def handle_message(update, context):
    update.message.reply_text(f"You said {update.message.text}, use the commands using /")


Token = ("6534040597:AAFlOkO734vy-ibtswI1UDiCgUBKpocndMI")
#print(bot.get_me())
updater = telegram.ext.Updater("6534040597:AAFlOkO734vy-ibtswI1UDiCgUBKpocndMI", use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler('start',start))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, handle_captcha_response))

disp.add_handler(telegram.ext.CommandHandler('help',help))

disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

disp.add_handler(telegram.ext.CommandHandler('contact',contact))

# Error handler to log exceptions
def error(update, context):
    logging.error(f"Update {update} caused error {context.error}")

disp.add_error_handler(error)
updater.start_polling()
updater.idle()


# pip install python-telegram-bot==13.7
