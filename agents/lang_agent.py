import config
from Sender import sendingMessage as sm
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.template import Template


res = "respuesta del agente 2"
class LangAgent(Agent):
  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      #print("RecvBehav running")
      msg = await self.receive()
      if msg:
        print("Mensage Recibo: {}".format(msg.body))
        await self.send(msg)
        await sm.SendM(self, res, config.AGENT_MAIN_USER)

     # else:
        #print("Did not received any message")

  async def setup(self):
    print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))
    b = self.RecvBehav(2)
    template = Template()
    template.set_metadata("test1", "val1")
    self.add_behaviour(b, template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
