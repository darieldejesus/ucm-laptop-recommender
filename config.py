import os
from dotenv import load_dotenv

load_dotenv()

AGENT_MAIN_USER = os.getenv("AGENT_MAIN_USER")
AGENT_MAIN_PASS = os.getenv("AGENT_MAIN_PASS")

AGENT_LANG_USER = os.getenv("AGENT_LANG_USER")
AGENT_LANG_PASS = os.getenv("AGENT_LANG_PASS")

AGENT_INTEL_USER = os.getenv("AGENT_INTEL_USER")
AGENT_INTEL_PASS = os.getenv("AGENT_INTEL_PASS")

AGENT_DATA_USER = os.getenv("AGENT_DATA_USER")
AGENT_DATA_PASS = os.getenv("AGENT_DATA_PASS")
