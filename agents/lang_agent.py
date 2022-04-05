from spade.agent import Agent
from spade.message import Message
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.template import Template

class LangAgent(Agent):
  # class BehavSubscribe(OneShotBehaviour):
  #   def on_available(self, jid, stanza):
  #     print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))

  #   def on_subscribed(self, jid):
  #     print("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
  #     print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

  #   def on_subscribe(self, jid):
  #     print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
  #     self.presence.approve(jid)
  #     self.presence.subscribe(jid)

  #   async def run(self):
  #     print("Habilitando subscribe")
  #     self.presence.on_subscribe = self.on_subscribe
  #     self.presence.on_subscribed = self.on_subscribed
  #     self.presence.on_available = self.on_available
  #     self.presence.set_available()

  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      print("RecvBehav running")
      msg = await self.receive()
      if msg:
        print("Message received: {}".format(msg.body))
        msg = Message(to=str(msg.sender))
        await self.send(msg)
      else:
        print("Did not received any message")

  async def setup(self):
    print("Hola!. Soy el agente encargado del Lenguaje Natural. Mi ID es \"{}\"".format(str(self.jid)))
    b = self.RecvBehav(10)
    template = Template()
    template.set_metadata("test1", "val1")
    self.add_behaviour(b, template)
    #self.add_behaviour(self.BehavSubscribe())

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
