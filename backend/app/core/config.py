import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "medextract")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")