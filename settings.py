import os
import json
from dotenv import load_dotenv


load_dotenv()

platform_url = os.getenv('PLATFORM_URL')
billing_url = os.getenv('BILLING_URL')
headers = json.loads(os.getenv('HEADERS'))
