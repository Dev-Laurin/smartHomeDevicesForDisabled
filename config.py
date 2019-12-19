import os 

class Config: 
	SECRET_KEY = 'dev'
	SQLALCHEMY_TRACK_MODIFICATIONS = False 

class ProdConfig(Config):
	DEBUG = False 
	TESTING = False 
	SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
	RECAPTCHA_PUBLIC_KEY = 'a public key'
	RECAPTCHA_PRIVATE_KEY = 'a private key'
	RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

class DevConfig(Config):
	DEBUG = True 
	TESTING = True 
	SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'