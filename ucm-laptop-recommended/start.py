import time
import os
from dotenv import load_dotenv
from spade import quit_spade
from agents.main_agent import MainAgent
from agents.lang_agent import LangAgent
from agents.intel_agent import IntelAgent
from agents.data_agent import DataAgent

load_dotenv()

AGENT_MAIN_USER = os.getenv("AGENT_MAIN_USER")
AGENT_MAIN_PASS = os.getenv("AGENT_MAIN_PASS")

AGENT_LANG_USER = os.getenv("AGENT_LANG_USER")
AGENT_LANG_PASS = os.getenv("AGENT_LANG_PASS")

AGENT_INTEL_USER = os.getenv("AGENT_INTEL_USER")
AGENT_INTEL_PASS = os.getenv("AGENT_INTEL_PASS")

AGENT_DATA_USER = os.getenv("AGENT_DATA_USER")
AGENT_DATA_PASS = os.getenv("AGENT_DATA_PASS")

if __name__ == "__main__":
  agent1 = MainAgent(AGENT_MAIN_USER, AGENT_MAIN_PASS)
  agent2 = LangAgent(AGENT_LANG_USER, AGENT_LANG_PASS)
  agent3 = IntelAgent(AGENT_INTEL_USER, AGENT_INTEL_PASS)
  agent4 = DataAgent(AGENT_DATA_USER, AGENT_DATA_PASS)

  future1 = agent1.start()
  future1.result()

  future2 = agent2.start()
  future2.result()

  """ future3 = agent3.start()
  future3.result()

  future4 = agent4.start()
  future4.result() """

  print("\nPara detener la ejecución, ejecutar Ctrl + C\n")
  while True:
    try:
      time.sleep(3)
    except KeyboardInterrupt:
      break

  print("\nDeteniendo agentes...\n")
  agent1.stop()
  agent2.stop()
  agent3.stop()
  agent4.stop()

  quit_spade()
