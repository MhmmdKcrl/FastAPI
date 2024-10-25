from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = f"mongodb+srv://{os.environ.get("MONGODB_USERNAME")}:{os.environ.get("MONGODB_PASSWORD")}@{os.environ.get("MONGODB_HOST")}/?retryWrites=true&w=majority&appName={os.environ.get("MONGODB_APP")}"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo
collection = db["todo_app"]
