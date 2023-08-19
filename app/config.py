from dotenv import load_dotenv
import os

load_dotenv('.env')


class Envs:
    algorithm = os.getenv('ALGORITHM')
    access_token_expire_time = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    secret_key = os.getenv('SECRET_KEY')


settings = Envs()
