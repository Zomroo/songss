import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re


# create a new Pyrogram client instance
api_id = os.environ.get("16844842")
api_hash = os.environ.get("f6b0ceec5535804be7a56ac71d08a5d4")
bot_token = os.environ.get("6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU")
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# define a function to search for songs on YouTube
def search_youtube(query):
    url = "https://www.youtube.com/results"
    params = {"search_query": query}
    response = requests.get(url, params=params)
    search_results = re.findall(r'/watch\?v=(.{11})" title="(.*?)"', response.text)
    results = []
    for search_result in search_results[:5]:
        video_id = search_result[0]
        title = search_result[1]
        results.append({"title": title, "video_id": video_id})
    return results

# define a command handler for the /start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    # send a welcome message
    client.send_message(chat_id=message.chat.id, text="Hi there! I can help you find and play songs from YouTube. Just send me the name of a song and I'll give you a list of 5 results to choose from.")

# define a command handler for the /song command
@app.on_message(filters.command("song"))
def song_command(client, message):
    # get the query from the message
    query = message.text.replace("/song", "").strip()
    
    # search for the query on YouTube
    results = search_youtube(query)
    
    # create a list of InlineKeyboardButton objects for the search results
    buttons = []
    for i, result in enumerate(results):
        button_label = f"{i+1}. {result['title']}"
        button = InlineKeyboardButton(button_label, callback_data=result["video_id"])
        buttons.append(button)
    keyboard = InlineKeyboardMarkup([buttons])
    
    # send a message with the search results as buttons
    message_text = f"Here are 5 results for '{query}':"
    client.send_message(chat_id=message.chat.id, text=message_text, reply_markup=keyboard)

# define a callback query handler for the search result buttons
@app.on_callback_query()
def callback_query(client, callback_query):
    # get the video ID from the callback data
    video_id = callback_query.data
    
    # send the audio of the selected video to the user
    url = f"https://www.youtube.com/watch?v={video_id}"
    video = pafy.new(url)
    bestaudio = video.getbestaudio()
    audio_url = bestaudio.url
    client.send_audio(chat_id=callback_query.message.chat.id, audio=audio_url)

# start the client
app.run()
