import os
import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace with your own token
TOKEN = '1616743590:AAH5daeLqc7QuKzS_HitBsNwA78lKMOMAWY'

# Define the photo and music directories
PHOTO_DIR = 'photos'
MUSIC_DIR = 'music'

# Create the directories if they don't exist
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# Create a Telegram bot object
bot = telegram.Bot(TOKEN)

# Define the function to save a photo
def save_photo(update, context):
    # Get the photo object
    photo = context.bot.get_file(update.message.photo[-1].file_id)
    # Save the photo to the photo directory
    photo.download(os.path.join(PHOTO_DIR, f'{photo.file_id}.jpg'))

# Define the function to save music
def save_music(update, context):
    # Check if the command was sent via a private chat
    if update.message.chat.type == 'private' and update.message.from_user.username == 684653448:
        # Get the audio object
        audio = context.bot.get_file(update.message.audio.file_id)
        # Save the audio to the music directory
        audio.download(os.path.join(MUSIC_DIR, f'{audio.file_id}.mp3'))

# Define the function to send a random photo and a 1-minute audio clip
def send_photo_and_music(update, context):
    # Send a random photo from the photo directory
    photo_files = os.listdir(PHOTO_DIR)
    if photo_files:
        photo_file = random.choice(photo_files)
        photo_path = os.path.join(PHOTO_DIR, photo_file)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(photo_path, 'rb'))
    # Send a 1-minute audio clip from the music directory
    music_files = os.listdir(MUSIC_DIR)
    if music_files:
        music_file = random.choice(music_files)
        music_path = os.path.join(MUSIC_DIR, music_file)
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(music_path, 'rb'), duration=60)
        # Send the audio to the @Logobass channel with a caption
        context.bot.send_audio(chat_id='@Logobass', audio=open(music_path, 'rb'), caption='Check out this cool track!')

# Create the handlers
photo_handler = MessageHandler(Filters.photo, save_photo)
music_handler = MessageHandler(Filters.audio & Filters.command, save_music)
send_handler = CommandHandler('send', send_photo_and_music)

# Create the updater and add the handlers
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(music_handler)
dispatcher.add_handler(send_handler)

# Start the bot
updater.start_polling()
