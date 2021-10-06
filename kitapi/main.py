from dotenv import load_dotenv

from kitapi.v1 import api


load_dotenv()


app = api.app
