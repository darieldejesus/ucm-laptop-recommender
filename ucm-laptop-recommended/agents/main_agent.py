from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class MainAgent(Agent):

  class InformBeahv(OneShotBehaviour):
    async def run(self):
      msg = Message(to="agente2@localhost")
      msg.set_metadata("performative", "inform")
      msg.set_metadata("ontology", "myOntology")
      msg.set_metadata("language", "OWL-S")
      msg.body = "Hola!. Soy el agente Asistente."

      await self.send(msg)
      print("Agente 1 en ejecucion")

  async def setup(self):
    self.b = self.InformBeahv()
    self.add_behaviour(self.b)
    """ print("Hola!. Soy el agente Asistente. Mi ID es \"{}\"".format(str(self.jid))) """
   
  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
