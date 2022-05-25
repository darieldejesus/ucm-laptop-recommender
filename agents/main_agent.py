import config
import rules.welcome
import datetime
from bson.json_util import dumps
from constants import states, actions
from telnetlib import STATUS
from durable.lang import update_state, post, get_state
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour, TimeoutBehaviour
from spade.message import Message
from spade.template import Template
from Templates import message as sm, pln

INITIAL_CONTEXT = {
  "status": states.WELCOME,
  "prev_status": "",
  "person": "",
  "message": "",
  "reply": "",
  "action": "",
  "response": "",
  "requirements": "",
  "budget": 0,
  "selected_cluster": "",
  "satisfaction": ""
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
      state["message"] = msg_received.body.lower()

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
    if state["action"] == actions.RESET:
      update_state("welcome", INITIAL_CONTEXT)
    elif state["action"] == actions.EXTRACT_NAME and state["message"] != "":
      msg = Message(to=config.AGENT_LANG_USER)
      msg.set_metadata("action", actions.EXTRACT_NAME)
      msg.body = state["message"]
      await self.send(msg)

      state["message"] = ""
      update_state("welcome", state)
    elif state["action"] == actions.EXTRACT_REQUIREMENTS and state["message"] != "":
      msg = Message(to=config.AGENT_LANG_USER)
      msg.set_metadata("action", actions.EXTRACT_REQUIREMENTS)
      msg.body = state["message"]
      await self.send(msg)

      state["message"] = ""
      update_state("welcome", state)
    elif state["action"] == actions.LOOK_FOR_REQUIREMENT and state["requirements"] != "":
      msg = Message(to=config.AGENT_DATA_USER)
      msg.set_metadata("action", actions.LOOK_FOR_REQUIREMENT)
      msg.body = state["requirements"]
      await self.send(msg)

      state["action"] = actions.LOOK_FOR_REQUIREMENT_RESPONSE
      update_state("welcome", state)
    elif state["action"] == actions.LOOK_FOR_EDGE_COMPUTERS:
      msg = Message(to=config.AGENT_DATA_USER)
      msg.set_metadata("action", actions.LOOK_FOR_EDGE_COMPUTERS)
      await self.send(msg)

      state["action"] = actions.LOOK_FOR_EDGE_COMPUTERS_RESPONSE
      update_state("welcome", state)
    elif state["action"] == actions.INSERT_REQUIREMENTS:
      msg = Message(to=config.AGENT_DATA_USER)
      msg.set_metadata("action", actions.INSERT_REQUIREMENTS)
      msg.body = dumps({
        "cluster": state["selected_cluster"],
        "requirements": state["requirements"],
      })
      await self.send(msg)

      state["action"] = actions.INSERT_REQUIREMENTS_RESPONSE
      state["message"] = ""
      update_state("welcome", state)
    elif state["action"] == actions.LOOK_FOR_COMPUTERS_RECOMMEND:
      msg = Message(to=config.AGENT_DATA_USER)
      msg.set_metadata("action", actions.LOOK_FOR_COMPUTERS_RECOMMEND)
      msg.body = dumps({
        "requirements": state["requirements"],
      })
      await self.send(msg)

      state["message"] = ""
      state["response"] = ""
      state["action"] = actions.LOOK_FOR_COMPUTERS_RECOMMEND_RESPONSE
      update_state("welcome", state)
    elif state["action"] == actions.INSERT_SATISFACTION and state["reply"] == "":
      msg = Message(to=config.AGENT_DATA_USER)
      msg.set_metadata("action", actions.INSERT_SATISFACTION)
      msg.body = dumps({
        "satisfaction": int(state["satisfaction"]),
      })
      await self.send(msg)

      state["message"] = ""
      state["response"] = ""
      state["action"] = actions.RESET
      update_state("welcome", state)

"""
Behavior para capturar los mensajes por parte del agente de datos
"""
class RecvDataBehav(PeriodicBehaviour):
  async def run(self):
    msg_received = await self.receive()
    if msg_received and msg_received.get_metadata("action") == actions.LOOK_FOR_REQUIREMENT:
      ## Actualizar el estado global del motor de reglas
      state = get_state("welcome")
      state["response"] = msg_received.body
      update_state("welcome", state)
    elif msg_received and msg_received.get_metadata("action") == actions.LOOK_FOR_EDGE_COMPUTERS:
      ## Actualizar el estado global del motor de reglas
      state = get_state("welcome")
      state["response"] = msg_received.body
      update_state("welcome", state)
    elif msg_received and msg_received.get_metadata("action") == actions.INSERT_REQUIREMENTS:
      ## Actualizar el estado global del motor de reglas
      state = get_state("welcome")
      state["response"] = msg_received.body
      update_state("welcome", state)
    elif msg_received and msg_received.get_metadata("action") == actions.LOOK_FOR_COMPUTERS_RECOMMEND:
      ## Actualizar el estado global del motor de reglas
      state = get_state("welcome")
      state["response"] = msg_received.body
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
    elif msg_received and msg_received.get_metadata("action") == actions.EXTRACT_REQUIREMENTS:
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

    recv_data_behav = RecvDataBehav(period=0.1)
    recv_data_behav_template = Template()
    recv_data_behav_template.to = config.AGENT_MAIN_USER
    recv_data_behav_template.sender = config.AGENT_DATA_USER
    self.add_behaviour(recv_data_behav, recv_data_behav_template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
