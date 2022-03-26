from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import time

class LangAgent(Agent):
  class RecBehav(OneShotBehaviour):
    async def run(self):
      msg = await self.receive(timeout=5)
      if msg:
        print("Mensaje recibida: {}".format(msg.body))
      else:
        print("No ha recibido ningun mensaje")

  async def setup(self):
    print("Agente 2 en ejecución")
    b = self.RecBehav()
    template = Template()
    template.set_metadata("performative", "inform")
    self.add_behaviour(b, template)
    #print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
