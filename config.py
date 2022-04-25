import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONNECTION_STRING = "mongodb://root:qaz123@localhost:27017/"
DATABASE_NAME = "dasi"
LAPTOPS_COLLECTION_NAME = "laptops"
CATEGORIES_COLLECTION_NAME = "categories"
SETTINGS_COLLECTION_NAME = "settings"

AGENT_MAIN_USER = os.getenv("AGENT_MAIN_USER")
AGENT_MAIN_PASS = os.getenv("AGENT_MAIN_PASS")

AGENT_LANG_USER = os.getenv("AGENT_LANG_USER")
AGENT_LANG_PASS = os.getenv("AGENT_LANG_PASS")

AGENT_INTEL_USER = os.getenv("AGENT_INTEL_USER")
AGENT_INTEL_PASS = os.getenv("AGENT_INTEL_PASS")

AGENT_DATA_USER = os.getenv("AGENT_DATA_USER")
AGENT_DATA_PASS = os.getenv("AGENT_DATA_PASS")

END_USER = os.getenv("END_USER")
