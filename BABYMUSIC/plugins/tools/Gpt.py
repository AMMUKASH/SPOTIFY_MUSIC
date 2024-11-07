import random
import time
from BABYMUSIC import app
import requests
from pyrogram.types import Message
from pyrogram.types import InputMediaPhoto
from teambabyAPI import api
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Hugging Face API URL for question answering
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad"

# Replace with your Hugging Face API Key
API_KEY = "your_huggingface_api_key"  # Make sure to replace this with your actual API key

# Function to query Hugging Face API for question answering
def get_answer_from_hugging_face(question, context):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    try:
        # Sending POST request to Hugging Face API
        response = requests.post(API_URL, headers=headers, json=payload)
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return result['answer']
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙᴀʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            question = message.text.split(' ', 1)[1]  # Extracting the question
            
            # Context (static text or dynamic content)
            context = """
            ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂 is a community platform for music lovers and people who enjoy lively discussions about various topics.
            """
            
            # Get the answer from Hugging Face API
            answer = get_answer_from_hugging_face(question, context)
            
            # Reply with the answer from the model
            await message.reply_text(
                f"**Answer from AI:**\n\n{answer}\n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", 
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
