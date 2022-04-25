from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from pymongo import MongoClient
from bson.json_util import dumps, loads
from constants import actions
import database as db
import config

class RecvActionMainBehav(PeriodicBehaviour):
  async def run(self):
    msg_received = await self.receive()

    if msg_received and msg_received.get_metadata("action") == actions.LOOK_FOR_REQUIREMENT:
      """Buscar la "categoria" dada por el usuario en la base de datos para saber si existe o no"""
      category = db.find_category(msg_received.body)

      reply_msg = Message(to=config.AGENT_MAIN_USER)
      reply_msg.set_metadata("action", actions.LOOK_FOR_REQUIREMENT)
      reply_msg.body = dumps({
        "found": bool(category),
      })
      await self.send(reply_msg)
    elif msg_received and msg_received.get_metadata("action") == actions.LOOK_FOR_EDGE_COMPUTERS:
      """Buscar los extremos de los clusteres para compararlos e identificar categoria"""
      edges = db.find_edge_laptops()

      reply_msg = Message(to=config.AGENT_MAIN_USER)
      reply_msg.set_metadata("action", actions.LOOK_FOR_EDGE_COMPUTERS)
      reply_msg.body = dumps({
        "found": bool(edges),
        "body": edges,
      })
      await self.send(reply_msg)
    elif msg_received and msg_received.get_metadata("action") == actions.INSERT_REQUIREMENTS:
      """Actualizar respuesta del usuario para el requirement dado"""
      body = loads(msg_received.body)
      inserted = db.insert_category(body["requirements"], body["cluster"])
      reply_msg = Message(to=config.AGENT_MAIN_USER)
      reply_msg.set_metadata("action", actions.INSERT_REQUIREMENTS)
      reply_msg.body = dumps({ "success": inserted })
      await self.send(reply_msg)

class DataAgent(Agent):
  class RecvIntelBehav(PeriodicBehaviour):
    async def run(self):
      msg_received = await self.receive()
      # print("Mensaje en DataAgente recibido!: {}".format(msg_received))
      if msg_received and msg_received.get_metadata("action") == actions.LOAD_LAPTOPS:
        list_laptops = db.load_laptops_for_cluster()

        msg_reply = Message(to=config.AGENT_INTEL_USER)
        msg_reply.set_metadata("action", actions.LOAD_LAPTOPS)
        msg_reply.body = dumps(list_laptops)

        await self.send(msg_reply)
      
      if msg_received and msg_received.get_metadata("action") == actions.UPDATE_LAPTOPS:
        print("He recibido la lista de laptops a actualizar")
        list_laptops = loads(msg_received.body)
        db.update_laptops_with_cluster(list_laptops)

  async def setup(self):
    print("Hola!. Soy el agente encargado de la Base de Datos. Mi ID es \"{}\"".format(str(self.jid)))

    # Cargamos DataSet a la DB
    db.init_laptops()

    recieveBehavior = self.RecvIntelBehav(period=0.1) # Recibir mensajes cada 0.1 seg
    template = Template()
    template.to = config.AGENT_DATA_USER
    template.sender = config.AGENT_INTEL_USER
    self.add_behaviour(recieveBehavior, template)

    recv_action_main_behav = RecvActionMainBehav(period=0.1) # Recibir mensajes cada 0.1 seg
    recv_action_main_behav_template = Template()
    recv_action_main_behav_template.to = config.AGENT_DATA_USER
    recv_action_main_behav_template.sender = config.AGENT_MAIN_USER
    self.add_behaviour(recv_action_main_behav, recv_action_main_behav_template)

  def stop(self):
    print("Deteniendo agente \"{}\"".format(str(self.jid)))
    return Agent.stop(self)
