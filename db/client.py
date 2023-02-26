from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local   # Localhost por defecto

client_password = "R7aylqv0WLMxZkLk"

db_client = MongoClient("mongodb+srv://eacanoz96:{client_password}@cluster0.rbxspxj.mongodb.net/?retryWrites=true&w=majority").tests