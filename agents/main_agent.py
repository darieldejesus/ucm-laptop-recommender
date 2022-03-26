import config
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class MainAgent(Agent):

  class InformBehav(PeriodicBehaviour):
    async def run(self):
      print("InformBehav running")
      msg = Message(to=config.AGENT_LANG_USER)
      msg.set_metadata("test1", "val1")
      msg.set_metadata("test2", "val2")
      msg.body = "Hello World"

      await self.send(msg)
      print("Message sent!")

      self.exit_code = "Message successfully sent!";

  async def setup(self):
    print("Hola!. Soy el agente Asistente. Mi ID es \"{}\"".format(str(self.jid)))
    b = self.InformBehav(period=10) # Enviar un mensaje cada 10 segundos
    self.add_behaviour(b)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
