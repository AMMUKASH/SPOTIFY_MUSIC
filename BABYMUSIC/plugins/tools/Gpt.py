import requests
from BABYMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Your AIML API Key
API_KEY = "e4de6eec07ad405390a630ddb65c6c38"  # Replace with your actual API key from aimlapi.com

# Base URL for AIML API
API_URL = "https://api.aimlapi.com/v1/query"  # Correct endpoint

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    try:
        # Typing action when the bot is processing the message
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            # If no question is asked, send an example message
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            # Extract the query from the user's message
            query = message.text.split(' ', 1)[1]
            print("Input query:", query)  # Debug input

            # Make a POST request to the AIML API with query in the body
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "query": query
            }

            # Send the request
            response = requests.post(API_URL, json=data, headers=headers)

            # Debugging: print raw response
            print("API Response Text:", response.text)  # Print raw response
            print("Status Code:", response.status_code)  # Check the status code

            # If the response is empty or not successful, handle the error
            if response.status_code != 200:
                await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status code: {response.status_code}")
            elif not response.text.strip():
                await message.reply_text("❍ ᴇʀʀᴏʀ: API se koi valid data nahi mil raha hai. Response was empty.")
            else:
                # Attempt to parse the JSON response
                try:
                    response_data = response.json()
                    print("API Response JSON:", response_data)  # Debug response JSON

                    if "response" not in response_data:
                        await message.reply_text("❍ ᴇʀʀᴏʀ: API response mein 'response' key nahi mili.")
                    else:
                        result = response_data["response"]
                        await message.reply_text(
                            f"{result} \n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)",
                            parse_mode=ParseMode.MARKDOWN
                        )
                except ValueError:
                    await message.reply_text("❍ ᴇʀʀᴏʀ: Invalid response format.")
    except Exception as e:
        # Catch any other exceptions and send an error message
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e} ")
