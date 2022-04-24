import config
from Templates import procesamientoLenguajeNatural as pln, message as sm
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.template import Template

import spacy
from spacy.lang.es.stop_words import STOP_WORDS

class LangAgent(Agent): 
  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      msg = await self.receive()
      if msg:
        res = await pln.procesarTexto(msg.body)
        await sm.EnviarMensaje(self, res, str(config.AGENT_MAIN_USER))

  async def setup(self):
    print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))
    b = self.RecvBehav(2)
    template = Template()
    template.set_metadata("test1", "val1")
    self.add_behaviour(b, template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
