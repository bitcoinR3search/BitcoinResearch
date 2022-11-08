
''' 
Este Script hace el login con el API de Twitter
'''

from dotenv import load_dotenv
import os, tweepy

def login(path=''):
    load_dotenv(path+'.env')
    API_KEY = os.getenv('api_key')
    API_SECRET_KEY = os.getenv('api_secret_key')
    ACCESS_TOKEN = os.getenv('access_token')
    ACCESS_TOKEN_SECRET = os.getenv('access_token_secret')

    auth = tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    print('autentificación - Twitter API')
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("sesión iniciada")
    except:
        print("ERROR")



if __name__ == '__main__':
    login(path='/home/ghost/rpibots/')
