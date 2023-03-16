
''' 
Este Script hace el login con el API de Twitter
'''

from dotenv import load_dotenv
import os, tweepy

def login(path=''):
    load_dotenv(path+'.env')
    API_KEY = os.getenv('API_KEY')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    print('autentificación - Twitter API')
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Sesión iniciada")
        return api
    except:
        print("ERROR")
        return False


if __name__ == '__main__':
    login('/home/ghost/')
