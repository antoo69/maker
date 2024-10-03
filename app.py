from pyrogram import Client

api_id = 123456  # Your API ID
api_hash = "your_api_hash"
session_string = "your_session_string"  # Generated earlier

app = Client("my_userbot", api_id=api_id, api_hash=api_hash, session_string=session_string)

@app.on_message()
def handle_message(client, message):
    if message.text:
        print(f"Received a message: {message.text}")
        message.reply("Hello! I'm your userbot.")

if __name__ == "__main__":
    app.run()
