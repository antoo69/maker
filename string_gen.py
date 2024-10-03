from pyrogram import Client

def generate_session(api_id, api_hash):
    with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:
        session_string = app.export_session_string()
        return session_string

if __name__ == "__main__":
    api_id = int(input("Enter API ID: "))
    api_hash = input("Enter API Hash: ")
    session_string = generate_session(api_id, api_hash)
    print(f"Your session string: {session_string}")
