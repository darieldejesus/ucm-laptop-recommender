import config
import spacy
from bson.json_util import dumps
from constants import actions
from Templates import pln, message as sm
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.template import Template
from spacy.lang.es.stop_words import STOP_WORDS

class RecvActionMainBehav(PeriodicBehaviour):
  async def run(self):
    msg_received = await self.receive()
    if msg_received and msg_received.get_metadata("action") == actions.EXTRACT_NAME:
      # Extraer nombre desde el texto
      res = pln.extract_name(msg_received.body)
      # print("IMPRIMIENDOOOOOOOOOOOOOOOO", res["found"])

      reply_msg = Message(to=config.AGENT_MAIN_USER)
      reply_msg.set_metadata("action", actions.EXTRACT_NAME)
      reply_msg.body = dumps({
        "found": res["found"],
        "body": res["name"]
      })
      await self.send(reply_msg)
    elif msg_received and msg_received.get_metadata("action") == actions.EXTRACT_REQUIREMENTS:
      # Extraer requerimientos desde el texto
      result = pln.extract_requirements(msg_received.body)
      reply_msg = Message(to=config.AGENT_MAIN_USER)
      reply_msg.set_metadata("action", actions.EXTRACT_REQUIREMENTS)
      reply_msg.body = dumps(result)
      await self.send(reply_msg)

class LangAgent(Agent): 
  async def setup(self):
    print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))

    recv_action_main_behav = RecvActionMainBehav(period=0.1)
    recv_action_main_behav_template = Template()
    recv_action_main_behav_template.to = config.AGENT_LANG_USER
    recv_action_main_behav_template.sender = config.AGENT_MAIN_USER
    self.add_behaviour(recv_action_main_behav)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
