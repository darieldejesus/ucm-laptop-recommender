from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.template import Template

class LangAgent(Agent):
  
  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      print("RecvBehav running")

      msg = await self.receive()
      if msg:
        print("Message received!: {}".format(msg.body))
      else:
        print("Did not received any message")

  async def setup(self):
    print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))
    b = self.RecvBehav(period=2)
    template = Template()
    template.set_metadata("test1", "val1")
    self.add_behaviour(b, template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
