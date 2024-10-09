import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
