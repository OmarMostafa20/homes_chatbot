import os
import urllib
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_DIALECT = os.getenv('DB_DIALECT', 'mysql')
    DB_USERNAME = os.getenv('DB_USERNAME', 'beltone')
    DB_PASSWORD = urllib.parse.quote_plus(os.getenv('DB_PASSWORD', 'beltone'))
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'beltone_db')

    SQLALCHEMY_DATABASE_URI = f"{
        DB_DIALECT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
