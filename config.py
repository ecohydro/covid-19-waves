import os
from dotenv import load_dotenv
load_dotenv()

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

# Read Config Settings from .env file:
config = {}
config['LOCAL'] = str2bool(os.getenv('LOCAL'))
config['DEBUG'] = str2bool(os.getenv('DEBUG'))
