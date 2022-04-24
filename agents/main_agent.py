import config
import rules.welcome
import datetime
from constants import states, actions
from telnetlib import STATUS
from durable.lang import update_state, post, get_state
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour, TimeoutBehaviour
from spade.message import Message
from spade.template import Template
from Templates import message as sm

INITIAL_CONTEXT = {
  "status": states.WELCOME,
  "person": "",
  "message": "",
  "reply": "",
  "action": "",
  "response": ""
}
estado= 0
nombre = ''
es_nombre = False

class InitConversatopmBehav(TimeoutBehaviour):
  async def run(self):
    update_state("welcome", INITIAL_CONTEXT)
    ## Agregamos behaviour para recibir mensajes desde el usuario
    recv_user_message_behv = RecvUserMessageBehav(period=0.1)
    recv_user_message_behv_template = Template()
    recv_user_message_behv_template.to = config.AGENT_MAIN_USER
    self.agent.add_behaviour(recv_user_message_behv)

    reply_user_message_behv = ReplyUserMessageBehav(period=0.1)
    self.agent.add_behaviour(reply_user_message_behv)

    rules_actions_behav = RulesActionsBehav(period=0.1)
    self.agent.add_behaviour(rules_actions_behav)

"""
Behavior para recibir los mensajes desde el usuario final
y actualizar el estado global del motor de reglas
"""
class RecvUserMessageBehav(PeriodicBehaviour):
  async def run(self):
    msg_received = await self.receive()
    if msg_received and config.END_USER in str(msg_received.sender):

      ## Obtengo el state actual para actualizarlo
      state = get_state("welcome")
      state["message"] = msg_received.body

      ## Actualizamos el status global
      update_state("welcome", state)

"""
Behavior para enviar mensajes al usuario basado en la propiedad "reply"
desde el estado global del motor de reglas
"""
class ReplyUserMessageBehav(PeriodicBehaviour):
  async def run(self):
    state = get_state("welcome")
    if state["reply"]:
      ## Enviamos Reply al usuario
      msg_reply = Message(to=config.END_USER)
      msg_reply.body = state["reply"]
      await self.send(msg_reply)

      ## Actualizamos el status global
      state["reply"] = ""
      update_state("welcome", state)

"""
Behavior para ejecutar acciones dado por el motor de reglas
"""
class RulesActionsBehav(PeriodicBehaviour):
  async def run(self):
    state = get_state("welcome")
    if state["action"] == actions.EXTRACT_NAME and state["message"] != "":
      ## Enviamos el action y texto al agente Lang
      msg = Message(to=config.AGENT_LANG_USER)
      msg.set_metadata("action", actions.EXTRACT_NAME)
      msg.body = state["message"]
      await self.send(msg)

      state["message"] = ""
      update_state("welcome", state)

"""
Behavior para capturar los mensajes por parte del agente language
"""
class RecvLangBehav(PeriodicBehaviour):
  async def run(self):
    msg_received = await self.receive()
    if msg_received and msg_received.get_metadata("action") == actions.EXTRACT_NAME:
      ## Actualizar el estado global del motor de reglas
      state = get_state("welcome")
      state["response"] = msg_received.body
      update_state("welcome", state)

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
    # self.add_behaviour(received, template)
    self.add_behaviour(self.BehavSubscribe())

    start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
    init_user_conversation_behv = InitConversatopmBehav(start_at=start_at)
    self.add_behaviour(init_user_conversation_behv)

    recv_lang_behav = RecvLangBehav(period=0.1)
    recv_lang_behav_template = Template()
    recv_lang_behav_template.to = config.AGENT_MAIN_USER
    recv_lang_behav_template.sender = config.AGENT_LANG_USER
    self.add_behaviour(recv_lang_behav, recv_lang_behav_template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
