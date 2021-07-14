import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path) # take environment variables from .env file

INSTRUMENTATION_KEY = os.getenv("INSTRUMENTATION_KEY")