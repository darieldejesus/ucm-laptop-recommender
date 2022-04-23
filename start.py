import time
import config
from spade import quit_spade
from agents.main_agent import MainAgent
from agents.lang_agent import LangAgent
from agents.intel_agent import IntelAgent
from agents.data_agent import DataAgent

def start_agent(agent, port):
  print("Iniciando Agente {0} disponible via http://localhost:{1}/spade".format(agent.alias, port))
  agent.start()
  agent.web.start(hostname="localhost", port=port)


if __name__ == "__main__":
  
  agent2 = LangAgent(config.AGENT_LANG_USER, config.AGENT_LANG_PASS)
  agent3 = IntelAgent(config.AGENT_INTEL_USER, config.AGENT_INTEL_PASS)
  agent4 = DataAgent(config.AGENT_DATA_USER, config.AGENT_DATA_PASS)
  agent1 = MainAgent(config.AGENT_MAIN_USER, config.AGENT_MAIN_PASS)

  agent2.alias = "Language Processer"
  agent3.alias = "Machine Learning"
  agent4.alias = "Database Manager"
  agent1.alias = "Asistance"

  start_agent(agent2, 10002)
  start_agent(agent3, 10003)
  start_agent(agent4, 10004)
  start_agent(agent1, 10001)

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
