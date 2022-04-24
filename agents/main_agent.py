from telnetlib import STATUS
import config
import rules.welcome
from durable.lang import update_state, post, get_state
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
from Templates import message as sm

INITIAL_CONTEXT = {
  'status': 1,
  'person': '',
  'message': '',
}
estado= 0
nombre = ''
es_nombre = False
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
  class Saludar(OneShotBehaviour):
    async def run(self):
      msg = Message(to=config.END_USER)
      msg.body = await sm.pln("saludar", estado)
      globals()['estado'] = 1
      await self.send(msg)

  class RecvBehav(PeriodicBehaviour):
    async def run(self):
      msg_received = await self.receive()
      if msg_received:        
        if config.AGENT_LANG_USER in str(msg_received.sender):
          print("Ejecutar funcion para el agente lang", msg_received.body)
          msg_reply = Message(to=str(config.END_USER))
          msg_reply.body = msg_received.body
          await self.send(msg_reply)
        
        elif config.END_USER in str(msg_received.sender):
          await sm.EnviarMensaje(self, msg_received.body, config.AGENT_LANG_USER)
          print("Ejecutar funcion para el usuario final", msg_received.body)

        #print("Message received!: {}".format(msg_received.body))
        
  async def setup(self):
    print("Hola!. Soy el agente Asistente. Mi ID es \"{}\"".format(str(self.jid)))
   
    received = self.RecvBehav(period=1) 
    template = Template()
    self.add_behaviour(received, template)
    self.add_behaviour(self.BehavSubscribe())

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
