import config
import rules.welcome
from durable.lang import update_state, post, get_state
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

INITIAL_CONTEXT = {
  'status': 1,
  'person': '',
  'message': '',
}

class MainAgent(Agent):

  class BehavSubscribe(OneShotBehaviour):
    def on_available(self, jid, stanza):
      print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))

    def on_subscribed(self, jid):
      print("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
      print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

    def on_subscribe(self, jid):
      print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
      self.presence.approve(jid)

    async def run(self):
      print("Intentar subscribir")
      self.presence.on_subscribe = self.on_subscribe
      self.presence.on_subscribed = self.on_subscribed
      self.presence.on_available = self.on_available
      self.presence.set_available()
      # self.presence.subscribe(config.AGENT_LANG_USER)
      self.presence.subscribe(config.END_USER)

  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      # state = get_state('welcome')
      # print(state)

      msg = await self.receive()
      if msg:
        message_body = msg.body
        print("Message received!: {}".format(msg.body))
        msg = Message(to=str(msg.sender))
        msg.body = "He recibido tu mensaje: \"{}\"".format(message_body)
        await self.send(msg)

  async def setup(self):
    print("Hola!. Soy el agente Asistente. Mi ID es \"{}\"".format(str(self.jid)))

    # Iniciamos state para dar bienvenida al usuario
    # update_state("welcome", INITIAL_CONTEXT)

    b = self.RecvBehav(period=1) # Recibir mensajes cada 1 seg
    template = Template()
    self.add_behaviour(b, template)
    self.add_behaviour(self.BehavSubscribe())

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
