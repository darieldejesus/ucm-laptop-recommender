import time
import config
from spade import quit_spade
from agents.main_agent import MainAgent
from agents.lang_agent import LangAgent
from agents.intel_agent import IntelAgent
from agents.data_agent import DataAgent

if __name__ == "__main__":
  agent1 = MainAgent(config.AGENT_MAIN_USER, config.AGENT_MAIN_PASS)
  agent2 = LangAgent(config.AGENT_LANG_USER, config.AGENT_LANG_PASS)
  agent3 = IntelAgent(config.AGENT_INTEL_USER, config.AGENT_INTEL_PASS)
  agent4 = DataAgent(config.AGENT_DATA_USER, config.AGENT_DATA_PASS)

  print("Iniciando Agente 1 (Main Agent)")
  future1 = agent1.start()

  print("Iniciando Agente 2 (Language Agent)")
  future2 = agent2.start()

  print("Iniciando Agente 3 (Intelligence Agent)")
  future3 = agent3.start()

  print("Iniciando Agente 4 (Database Agent)")
  future4 = agent4.start()

  print("\nPara detener la ejecución, ejecutar Ctrl + C\n")
  while True:
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      break

  print("\nDeteniendo agentes...\n")
  agent1.stop()
  agent2.stop()
  agent3.stop()
  agent4.stop()

  quit_spade()
